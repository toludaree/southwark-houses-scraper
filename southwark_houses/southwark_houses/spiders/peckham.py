import time

from scrapy import Selector, Spider
from itemloaders import ItemLoader
from southwark_houses.items import SoouthwarkHousesSeleniumItem

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException


class PeckhamSpider(Spider):
    name = "peckham"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView"]

    def parse(self, r):
        options = webdriver.ChromeOptions()
        driver = webdriver.Chrome(options=options)
        driver.implicitly_wait(10)
        driver.get(self.start_urls[0])
        
        cookies_element = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        cookies_element.click()
        time.sleep(3)
        year_select_element = driver.find_element(By.XPATH,
            "//div[@class='filter-bar  ']//select[@name='soldIn']")
        Select(year_select_element).select_by_value("1")
        time.sleep(3)

        while True:
            extra_records_element = driver.find_elements(By.CLASS_NAME, "expand-toggle")
            for element in extra_records_element:
                element.click()
                time.sleep(1)
            time.sleep(3)
            response = driver.page_source

            selector = Selector(text=response)
            gallery = selector.xpath("//div[@class='propertyCard']")
            for listing in gallery:
                item = ItemLoader(item=SoouthwarkHousesSeleniumItem(), response=response, selector=listing)
                item.add_xpath("address", ".//a[@data-gtm='title']/text()")
                item.add_xpath("type", ".//span[@class='propertyType']/text()")
                item.add_xpath("last_known_price", ".//table//tr[1]/td[@class='price']/text()")
                item.add_xpath("last_known_tenure", ".//table//tr[1]/td[contains(@class, 'tenure')]/text()")
                item.add_xpath("transaction_history", ".//table//tr")
                yield item.load_item()

            try:
                next_element = driver.find_element(By.XPATH, "//div[@class='pagination pagination-next ']")
                next_element.click()
            except NoSuchElementException:
                self.logger.info("Last page scraped... Quitting Selenium")
                break

            time.sleep(5)

        driver.quit()
