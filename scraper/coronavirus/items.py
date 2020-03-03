# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CoronavirusCountry(scrapy.Item):
    country = scrapy.Field()
    cases = scrapy.Field()
    deaths = scrapy.Field()
    recovered = scrapy.Field()
    serious = scrapy.Field()
    critical = scrapy.Field()
    time = scrapy.Field()
    notes = scrapy.Field()
    source = scrapy.Field()
    pass
