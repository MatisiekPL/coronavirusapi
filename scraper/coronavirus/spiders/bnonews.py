# -*- coding: utf-8 -*-
import glob
import os
import re
from os import path

import scrapy
from dateutil import parser
from pymongo import MongoClient

from coronavirus.items import CoronavirusCountry

files = glob.glob(path.join(os.getcwd(), "coronavirus-*.txt"))

start_files = []
for file in files:
    start_files.append('file:' + file)

class BnonewsSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        client = MongoClient(os.getenv("MONGO_URI"))
        self.countries_collection = client['coronavirus']['countries']

    name = 'bnonews'
    allowed_domains = ['bnonews.com']
    start_urls = ['https://bnonews.com/index.php/2020/02/the-latest-coronavirus-cases/'] + start_files

    def parse(self, response):
        countries = response.xpath('//table[@class="wp-block-table aligncenter is-style-regular"]//tbody//tr')
        if self.countries_collection.count_documents({
            'time': parser.parse(
                response.xpath('//*[contains(text(), "Last update")]//text()').extract_first().replace(
                    'Last update: ', '').replace('at', '').replace('ET', ''))
        }) == 0:
            for country in countries[1:]:
                item = self.convert(country)
                if item['country'] != 'TOTAL':
                    item['time'] = parser.parse(
                        response.xpath('//*[contains(text(), "Last update")]//text()').extract_first().replace(
                            'Last update: ', '').replace('at', '').replace('ET', ''))
                    yield item
        countries = response.xpath('//table[@class="wp-block-table aligncenter is-style-stripes"]//tbody//tr')
        if self.countries_collection.count_documents({
            'time': parser.parse(
                response.xpath('//*[contains(text(), "Last update")]//text()').extract_first().replace(
                    'Last update: ', '').replace('at', '').replace('ET', ''))
        }) == 0:
            for country in countries[1:]:
                item = self.convert(country)
                if item['country'] != 'TOTAL':
                    item['time'] = parser.parse(
                        response.xpath('//*[contains(text(), "Last update")]//text()').extract_first().replace(
                            'Last update: ', '').replace('at', '').replace('ET', ''))
                    yield item

    def convert(self, country):
        item = CoronavirusCountry()
        item['country'] = country.xpath('td[1]//text()').extract_first()
        item['cases'] = int(
            re.sub('[^0-9]', '', country.xpath('td[2]//text()').extract_first().strip().replace(',', '')))
        item['deaths'] = int(
            re.sub('[^0-9]', '', country.xpath('td[3]//text()').extract_first().strip().replace(',', '')))
        item['notes'] = country.xpath('td[4]//text()').extract_first()
        item['source'] = country.xpath('td[5]//text()').extract_first()
        return item
