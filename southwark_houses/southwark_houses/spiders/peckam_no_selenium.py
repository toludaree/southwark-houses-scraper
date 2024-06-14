import scrapy


class PeckamNoSeleniumSpider(scrapy.Spider):
    name = "peckam_no_selenium"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://rightmove.co.uk"]

    def parse(self, response):
        pass
