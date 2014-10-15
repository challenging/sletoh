# -*- coding: utf-8 -*-

# Scrapy settings for hotels project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'China Happy New Year'

SPIDER_MODULES = ['hotels.spiders']
NEWSPIDER_MODULE = 'hotels.spiders'

ITEM_PIPELINES = {
    "hotels.pipelines.HotelPipeline": 11
}

DUPEFILTER_CLASS = 'hotels.duplicated_filter.SeenURLFilter'

# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = 'hotels (+http://www.yourdomain.com)'
