# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SouthwarkHousesItem(scrapy.Item):
    address = scrapy.Field()
    last_known_price = scrapy.Field()
    type = scrapy.Field()
    tenure = scrapy.Field()
    price_history = scrapy.Field()
