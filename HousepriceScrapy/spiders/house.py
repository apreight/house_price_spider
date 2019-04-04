# -*- coding: utf-8 -*-
import logging

import scrapy

from HousepriceScrapy.items import HousepricescrapyItem


class HouseSpider(scrapy.Spider):
    name = 'house'
    allowed_domains = ['anjuke.com']
    start_urls = ['https://www.anjuke.com/fangjia/nanjing2019/',
                  'https://www.anjuke.com/fangjia/nanjing2018/',
                  'https://www.anjuke.com/fangjia/nanjing2017/',
                  'https://www.anjuke.com/fangjia/nanjing2016/',
                  'https://www.anjuke.com/fangjia/nanjing2015/',
                  "https://www.anjuke.com/fangjia/nanjing2014/",
                  'https://www.anjuke.com/fangjia/nanjing2013/',
                  'https://www.anjuke.com/fangjia/nanjing2012/',
                  'https://www.anjuke.com/fangjia/nanjing2011/',
                  'https://www.anjuke.com/fangjia/nanjing2010/']

    def parse(self, response):
        # 首节点
        for start_url in self.start_urls:
            logging.debug("首节点:[ " + start_url + " ]")
            yield scrapy.Request(start_url, callback=lambda res=response, url=start_url: self.handle_response(res, url),
                                 dont_filter=True)

        for link1 in response.xpath("//span[@class=\"elem-l\"]/a/@href").extract():
            logging.debug("一级节点:[ "+link1+" ]")
            if "nanjing" in str(link1):
                yield scrapy.Request(link1, callback=lambda res=response, url=link1: self.handle_response(res, url),
                                     dont_filter=True)
                yield scrapy.Request(link1, callback=lambda res=response, url=link1: self.parse_next(res),
                                     dont_filter=True)
        pass

    @staticmethod
    def handle_response(response, url):
        region = response.xpath("//span[@class=\"elem-l\"]/span[@class=\"selected-item\"]/text()")
        area = response.xpath("//div[@class=\"crumbs_wrap_top\"]/following::h2[1]/text()").extract()[0]
        area = area.split("房价")[0]
        area = area.split("年")[1]

        logging.log(logging.DEBUG, "开始爬取: [ " + region.extract()[0] + "区| " + area+" ] 地区房价数据")

        prices = response.xpath("//div[@class=\"fjlist-wrap clearfix\"]/div[1]/ul/li").css("a:first-child")
        for each_price in prices:
            item = HousepricescrapyItem()
            item["origin_url"] = url
            item["region"] = region.extract()[0]
            item["area"] = area
            item["title"] = each_price.xpath("./b/text()").extract()[0].split("房价")[0]
            try:
                item["price"] = float(each_price.xpath("./span/text()").extract()[0].split("元")[0])
            except ValueError:
                item["price"] = 0.0
            item["time_year"] = int(each_price.xpath("./b/text()").extract()[0].split("房价")[0].split("年")[0])
            item["time_mon"] = int(each_price.xpath("./b/text()").extract()[0].split("房价")[0].split("年")[1].split("月")[0])
            speed = each_price.xpath("./em/text()").extract()[0]
            if speed[-1] == "↑":
                speed = speed[0:-2]
            elif speed[-1] == "↓":
                speed = "-" + speed[0:-2]
            else:
                speed = "0"
            item["speed"] = float(speed)
            yield item
        pass

    @staticmethod
    def parse_next(response):
        links = response.xpath("//div[@class=\"sub-items\"]//a/@href").extract()
        for link in links:
            logging.debug("二级节点:[ " + link + " ]")
            yield scrapy.Request(link, callback=lambda res=response, url=link: HouseSpider.handle_response(res, url),
                                 dont_filter=True)
        pass
