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

class AgodaHotel(scrapy.Item):
    city = scrapy.Field()
    bookingDate = scrapy.Field()

    name = scrapy.Field()
    location = scrapy.Field()
    ranking = scrapy.Field()
    comment = scrapy.Field()

    room = scrapy.Field()

class RakutenHotel(scrapy.Item):
    city = scrapy.Field()
    bookingDate = scrapy.Field()

    name = scrapy.Field()
    location = scrapy.Field()
    star = scrapy.Field()
    ranking = scrapy.Field()
    comment = scrapy.Field()

    currency = scrapy.Field()
    priceMin = scrapy.Field()
    priceMax = scrapy.Field()
