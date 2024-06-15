import scrapy


class HousesSpider(scrapy.Spider):
    name = "houses"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://rightmove.co.uk"]

    def parse(self, response):
        pass
