import scrapy


class HousesCrawlSpider(scrapy.Spider):
    name = "houses_crawl"
    allowed_domains = ["rightmove.co.uk"]
    start_urls = ["https://rightmove.co.uk"]

    def parse(self, response):
        pass
