# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import time
import jsonlib2 as json

class HotelsPipeline(object):
    def spider_opened(self, spider):
        self.file = open("%s.%s.json" %(spider.name, time.strftime("%Y%m%d")), "ab")

    def process_item(self, item, spider):
        line = json.dumps(dict(item)) + "\n"
        self.file.write(line)

        return item

    def spider_closed(self, spider):
        self.file.close()
