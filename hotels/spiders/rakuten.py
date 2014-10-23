#-*- coding: utf-8 -*-

import sys, exceptions
import time, datetime
import socket
import re

from scrapy.contrib.spiders import CrawlSpider
from hotels.items import RakutenHotel

import selenium.webdriver.support.ui as ui

from pyvirtualdisplay import Display
from selenium import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, UnexpectedAlertPresentException

class RakutenSpider(CrawlSpider):
    name = "Rakuten"
    allowed_domains = ["travel.rakuten.com.tw"]
    start_urls = ["http://travel.rakuten.com.tw/"]
    search_url = "http://travel.rakuten.com.tw/hotellist/Japan-%s/JP_JP-%s/?checkin_date=%s&checkout_date=%s&rooms=1&adults=2&children=0"

    def __init__(self, city, num, plusDate):
        self.city = city
        self.num = num
        self.plusDate = int(plusDate)

        CrawlSpider.__init__(self)
        self.startWebDriver()
 
    def startWebDriver(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()

        self.webDriver = webdriver.Chrome()

    def quitWebDriver(self):
        self.webDriver.quit()
        self.display.stop()

    def parse(self, response):
        browser = self.webDriver

        dateStart = 7
        for plusDate in range(dateStart, dateStart+self.plusDate+1):
            dateBooking = datetime.date.today() + datetime.timedelta(days=plusDate)
            dateReturn = datetime.date.today() + datetime.timedelta(days=plusDate+1)

            maxTries = 3
            while maxTries > -1:
                try:
                    browser.get(RakutenSpider.search_url %(self.city, self.num, dateBooking.strftime("%Y-%m-%d"), dateReturn.strftime("%Y-%m-%d")))

                    while True:
                        try:
                            if ui.WebDriverWait(browser, 20).until(lambda broswer: browser.find_element_by_link_text(u"更多飯店") != None):
                                browser.find_element_by_xpath("//a[@class='btn']").click()
                                time.sleep(1)
                            else:
                                break
                        except TimeoutException as e:
                            break

                    hotels = browser.find_elements_by_class_name("list-item")
                    stars = browser.find_elements_by_class_name("rank")
                    for idx in range(0, len(hotels)):
                        hotel = hotels[idx]
                        star = stars[idx].get_attribute("title")

                        if len(hotel.text) == 0:
                            continue

                        try:
                            infos = hotel.text.split("\n")
                            name = infos[0]
                            ranking = infos[1]
                            location = infos[2]
                            price = infos[3]
                            comment = None
                            if len(infos) > 4:
                                comment = infos[4]

                            item = RakutenHotel()
                            item["city"] = self.city
                            item["name"] = name
                            item["bookingDate"] = dateBooking.strftime("%Y-%m-%d")

                            item["star"] = star
                            item["ranking"] = ranking
                            item["comment"] = comment
                            item["location"] = location

                            item["currency"] = price[0]
                            item["priceMin"] = price[1]
                            item["priceMax"] = price[3]

                            yield item
                        except exceptions.ValueError as e:
                            print hotel.text
                            print e
                            time.sleep(600)

                    maxTries = -1
                except NoSuchElementException as e:
                    print e
                except exceptions.IndexError as e:
                    print e

                maxTries -= 1

        self.quitWebDriver()
