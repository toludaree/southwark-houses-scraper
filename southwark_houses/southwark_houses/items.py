# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import Join, MapCompose
from lxml.etree import HTML


def sh_transaction_history_in(d):
    return {"date_sold": d["dateSold"],
            "price": d["displayPrice"],
            "tenure": d["tenure"]}

def shs_transaction_history_in(d):
    html = HTML(d)
    date_sold = html.xpath("//td[@class='date-sold']/text()")[0]
    price = html.xpath("//td[@class='price']/text()")[0]
    tenure = html.xpath("//td[contains(@class, 'tenure')]/text()")[0]

    return {"date_sold": date_sold,
            "price": price,
            "tenure": tenure}

class SouthwarkHousesItem(scrapy.Item):
    area = scrapy.Field(output_processor=Join())
    address = scrapy.Field(output_processor=Join())
    type = scrapy.Field(output_processor=Join())
    last_known_price = scrapy.Field(output_processor=Join())
    last_known_tenure = scrapy.Field(output_processor=Join())
    transaction_history = scrapy.Field(input_processor=MapCompose(sh_transaction_history_in))

class SoouthwarkHousesSeleniumItem(scrapy.Item):
    address = scrapy.Field(output_processor=Join())
    type = scrapy.Field(output_processor=Join())
    last_known_price = scrapy.Field(output_processor=Join())
    last_known_tenure = scrapy.Field(output_processor=Join())
    transaction_history = scrapy.Field(input_processor=MapCompose(shs_transaction_history_in))
