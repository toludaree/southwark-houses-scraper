import scrapy


class PeckhamSpider(scrapy.Spider):
    name = "peckham"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://www.rightmove.co.uk/house-prices/peckham.html?showMapView=showMapView"]

    def parse(self, response):
        pass
