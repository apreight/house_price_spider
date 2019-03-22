# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo


class HousepricescrapyPipeline(object):
    price_collection_name = 'price_house'  # 数据库中 collection 的命名
    address_collection_name = 'address'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI'),
            mongo_db=crawler.settings.get('MONGO_DATABASE')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        # addr = self.db[self.address_collection_name].find_one({"area": item["area"]})
        # if addr is None:
        #     object_id = ObjectId(self.db[self.address_collection_name].insert({'area': item["area"],
        #                                                                        'region': item["region"]}))
        # else:
        #     object_id = addr['_id']
        self.db[self.price_collection_name].insert(dict(item))
        return item
