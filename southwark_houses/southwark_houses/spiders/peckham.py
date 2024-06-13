import scrapy


class PeckhamSpider(scrapy.Spider):
    name = "peckham"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://rightmove.co.uk"]

    def parse(self, response):
        pass
