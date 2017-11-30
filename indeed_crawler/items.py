# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# need to define .Field if you want to scrapy to save csv

import scrapy
from scrapy.item import Item, Field

class JobObj(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    name = scrapy.Field()
    company = scrapy.Field()
    pass