import json
from scrapy import Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from itemloaders import ItemLoader
from southwark_houses.items import SouthwarkHousesItem

class HousesCrawlSpider(CrawlSpider):
    name = "houses_crawl"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices-in-Southwark.html?showMapView=showMapView"]
    xhr_url_template = "https://www.rightmove.co.uk/house-prices/result?soldIn=1&filterName=Sold%20in&locationType=REGION&locationId={}&page={}"

    rules = (
        Rule(
            LinkExtractor(restrict_xpaths="//ul[contains(@class, 'sidemenu')]"),
            follow=True,
            process_request="parse_requests",
        ),
    )

    def parse_requests(self, request, response):
        parent_list_elem = response.xpath(f"//a[@href='{request.url}']/parent::li")[0]
        area_id = parent_list_elem.attrib["id"].split("sidemenu")[1]
        return Request(url=self.xhr_url_template.format(area_id, 1),
                      callback=self.parse,
                      cb_kwargs=dict(area_id=area_id))

    def parse(self, response, area_id):
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
                                  callback=self.parse,
                                  cb_kwargs=dict(area_id=area_id))
