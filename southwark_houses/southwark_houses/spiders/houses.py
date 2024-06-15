import json
from scrapy import Spider
from itemloaders import ItemLoader
from southwark_houses.items import SouthwarkHousesItem


class HousesSpider(Spider):
    name = "houses"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices-in-Southwark.html?showMapView=showMapView"]
    xhr_url_template = "https://www.rightmove.co.uk/house-prices/result?soldIn=1&filterName=Sold%20in&locationType=REGION&locationId={}&page={}"

    def parse(self, response):
        areas = response.xpath("//ul[contains(@class, 'sidemenu')]/li[contains(@id, 'sidemenu')]")
        for area in areas:
            area_id = area.attrib["id"].split("sidemenu")[1]
            url = self.xhr_url_template.format(area_id, 1)
            yield response.follow(url, callback=self.parse_item, cb_kwargs=dict(area_id=area_id))

    def parse_item(self, response, area_id):
        payload = json.loads(response.body)
        total_pages = payload["pagination"]["last"]
        area_name = payload["searchLocation"]["displayName"]

        for house in payload["results"]["properties"]:
            item = ItemLoader(item=SouthwarkHousesItem(),
                              response=response,
                              selector=house)
            item.add_value("area", area_name)
            item.add_value("address", house["address"])
            item.add_value("type", house["propertyType"])
            item.add_value("last_known_price", house["transactions"][0]["displayPrice"])
            item.add_value("last_known_tenure", house["transactions"][0]["tenure"])
            item.add_value("transaction_history", house["transactions"])

            yield item.load_item()

        for page in range(2, total_pages+1):
            yield response.follow(self.xhr_url_template.format(area_id, page),
                                  callback=self.parse_item,
                                  cb_kwargs=dict(area_id=area_id))
