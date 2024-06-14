import scrapy
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


class PeckhamSpider(scrapy.Spider):
    name = "peckham"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView"]

    def parse(self, response):
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
        extra_records_element = driver.find_elements(By.CLASS_NAME, "expand-toggle")
        for element in extra_records_element:
            element.click()
            time.sleep(1)
        time.sleep(3)

        
        driver.quit()

