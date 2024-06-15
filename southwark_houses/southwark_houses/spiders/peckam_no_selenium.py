import json
from scrapy import Spider
from itemloaders import ItemLoader
from southwark_houses.items import SouthwarkHousesItem


class PeckhamNoSeleniumSpider(Spider):
    name = "peckham_no_selenium"
    allowed_domains = ["rightmove.co.uk"]
    url_template = "https://www.rightmove.co.uk/house-prices/result?soldIn=1&filterName=Sold%20in&locationType=REGION&locationId=85428&page={}"
    current_page = 1
    start_urls = [url_template.format(current_page)]

    def parse(self, response):
        payload = json.loads(response.body)
        total = payload["pagination"]["last"]

        for house in payload["results"]["properties"]:
            item = ItemLoader(item=SouthwarkHousesItem(),
                              response=response,
                              selector=house)
            item.add_value("address", house["address"])
            item.add_value("type", house["propertyType"])
            item.add_value("last_known_price", house["transactions"][0]["displayPrice"])
            item.add_value("last_known_tenure", house["transactions"][0]["tenure"])
            item.add_value("transaction_history", house["transactions"])

            yield item.load_item()

        for page in range(2, total+1):
            yield response.follow(self.url_template.format(page), callback=self.parse)


