# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class HousepricescrapyItem(scrapy.Item):
    region = scrapy.Field()
    area = scrapy.Field()
    title = scrapy.Field()
    price = scrapy.Field()
    speed = scrapy.Field()
    pass
