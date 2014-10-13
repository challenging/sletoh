# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HotelsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AgodaItem(scrapy.Item):
    city = scrapy.Field()
    bookingDate = scrapy.Field()

    name = scrapy.Field()
    location = scrapy.Field()
    ranking = scrapy.Field()
    comment = scrapy.Field()

    room = scrapy.Field()
