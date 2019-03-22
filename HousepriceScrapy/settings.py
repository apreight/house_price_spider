# -*- coding: utf-8 -*-

# Scrapy settings for HousepriceScrapy project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'HousepriceScrapy'

SPIDER_MODULES = ['HousepriceScrapy.spiders']
NEWSPIDER_MODULE = 'HousepriceScrapy.spiders'
ITEM_PIPELINES = {'HousepriceScrapy.pipelines.HousepricescrapyPipeline': 100}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

DOWNLOAD_DELAY = 2.25


COOKIES_ENABLED = False

MONGO_URI = 'mongodb://admin:131415@47.101.174.230:27017'
MONGO_DATABASE = 'house_price'  # 可以自定义MONGODB_DBNAME = 'house_price'
