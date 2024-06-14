# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose


class SouthwarkHousesItem(scrapy.Item):
    address = scrapy.Field(output_processor=Join())
    type = scrapy.Field(output_processor=Join())
    last_known_price = scrapy.Field(output_processor=Join())
    last_known_tenure = scrapy.Field(output_processor=Join())
    price_history = scrapy.Field()
