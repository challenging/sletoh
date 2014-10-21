#-*- coding: utf-8 -*-

import sys, exceptions
import time, datetime, socket

from hotels.items import AgodaHotel
from scrapy.contrib.spiders import CrawlSpider

from pyvirtualdisplay import Display
from selenium import selenium
from selenium import webdriver

import selenium.webdriver.support.ui as ui

from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException, TimeoutException, NoSuchElementException, StaleElementReferenceException

class AgodaSpider(CrawlSpider):
    name = "Agoda"
    allowed_domains = ["www.agoda.com"]
    start_urls = ["http://www.agoda.com"]
    search_url = "http://www.agoda.com/zh-tw/"

    def __init__(self, city, plusDate, nightCount):
        self.city = city
        self.plusDate = int(plusDate)
        self.nightCount = nightCount 

        CrawlSpider.__init__(self)       
        self.startWebDriver()
 
    def startWebDriver(self):
        self.display = Display(visible=0, size=(800, 600))
        self.display.start()
        self.webDriver = webdriver.Firefox()

    def quitWebDriver(self):
        self.webDriver.quit()
        self.display.stop()

    def parse(self, response):
        browser = self.webDriver

        for date in range(1, self.plusDate+1):
            flyingDate = datetime.date.today() + datetime.timedelta(days=date)

            maxTries = 3
            while maxTries > 0:
                try:
                    browser.get(AgodaSpider.search_url)
                    browser.find_element_by_name("SearchInput").clear()
                    browser.find_element_by_name("SearchInput").send_keys(self.city.decode("utf-8"))
                    time.sleep(1)
                    browser.find_element_by_class_name("ui-menu-promote").click()

                    Select(browser.find_element_by_id("CheckInMonthYear")).select_by_value(flyingDate.strftime("%m-%Y"))
                    Select(browser.find_element_by_id("CheckInDay")).select_by_value(flyingDate.strftime("%d"))
                    Select(browser.find_element_by_id("NightCount")).select_by_value("1")

                    browser.find_element_by_class_name("search-form").submit()

                    while True:
                        try:
                            if ui.WebDriverWait(browser, 10).until(lambda browser: browser.find_element_by_name("hotelInfoPlaceholder")):
                                #hotels = browser.find_element_by_name("hotelInfoPlaceholder").find_elements_by_tag_name("li")
                                hotels = browser.find_elements_by_xpath("//section[@class='entry']")

                                for hotel in hotels:
                                    comment = hotel.find_element_by_tag_name("h3").text

                                    center = hotel.find_element_by_class_name("flex-center")
                                    name = center.find_element_by_tag_name("a").text
                                    ranking = center.find_element_by_tag_name("i").text

                                    location = center.find_element_by_tag_name("ul").text

                                    item = AgodaHotel()
                                    item["city"] = self.city
                                    item["bookingDate"] = flyingDate.strftime("%Y%m%d")
                                    item["name"] = name
                                    item["location"] = location
                                    item["ranking"] = ranking
                                    item["comment"] = comment
                                    item["room"] = []

                                    rooms = hotel.find_element_by_class_name("ssr-room-grid").find_elements_by_tag_name("li")
                                    for room in rooms:
                                        roomType = room.find_element_by_class_name("room-type").text
                                        roomRate = room.find_element_by_class_name("room-rate").text

                                        item["room"].append([roomType, roomRate])

                                    yield item

                            browser.find_element_by_class_name("pager-right").click()
                            time.sleep(1)
                        except StaleElementReferenceException as e:
                            browser.refresh()
                            print "1. ", e
                        except WebDriverException as e:
                            maxTries = -1
                            break
                        except NoSuchElementException as e:
                            maxTries = -1
                            break
                except socket.timeout as e:
                    print e
                except NoSuchElementException as e:
                    print e
                except TimeoutException as e:
                    print e

                maxTries -= 1

        self.quitWebDriver()
