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
                  'https://www.anjuke.com/fangjia/nanjing2014/',
                  'https://www.anjuke.com/fangjia/nanjing2013/',
                  'https://www.anjuke.com/fangjia/nanjing2012/',
                  'https://www.anjuke.com/fangjia/nanjing2019/',
                  'https://www.anjuke.com/fangjia/nanjing2010/']

    def parse(self, response):
        # 处理首页
        self.handle_response(response)
        links = response.xpath("//span[@class=\"elem-l\"]/a/@href").extract()
        for link in links:
            # print("一级节点---" + link)
            yield scrapy.Request(link, callback=self.parse_next)
        pass

    def handle_response(self, response):
        region = response.xpath("//span[@class=\"elem-l\"]/span[@class=\"selected-item\"]/text()")
        area = response.xpath("//h3[@class=\"pagemod-tit\"]/text()").extract()[0]
        area = area.split("房价")[0]
        area = area.split("年")[1]

        logging.log(logging.DEBUG, "开始爬取: [ " + region.extract()[0] + "区| " + area+" ] 地区房价数据")

        prices = response.xpath("//div[@class=\"fjlist-wrap clearfix\"]/div[1]/ul/li").css("a:first-child")
        for each_price in prices:
            item = HousepricescrapyItem()
            item["region"] = region.extract()[0]
            item["area"] = area
            item["title"] = each_price.xpath("./b/text()").extract()[0].split("房价")[0]
            item["price"] = each_price.xpath("./span/text()").extract()[0]
            speed = each_price.xpath("./em/text()").extract()[0]
            if speed[-1] == "↑":
                speed = speed[0:-2]
            elif speed[-1] == "↓":
                speed = "-" + speed[0:-2]
            else:
                speed = "0"
            item["speed"] = speed
            yield item
        pass

    def parse_next(self, response):
        self.handle_response(response)
        links = response.xpath("//div[@class=\"sub-items\"]//a/@href").extract()
        for link in links:
            # print("二级节点---" + link)
            yield scrapy.Request(link, callback=self.handle_response)
        pass
