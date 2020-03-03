# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os

from pymongo import MongoClient
from scrapy.utils import log


class MongoPipeline(object):
    def __init__(self):
        client = MongoClient(os.getenv("MONGO_URI"))
        self.countries_collection = client['coronavirus']['countries']

    def process_item(self, item, spider):
        valid = True
        if valid:
            self.countries_collection.insert(dict(item))
        return item
