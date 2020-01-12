# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class QdreaderItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class SquareHongbaoItem(scrapy.Item):
    hongbaoId = scrapy.Field()
    Status = scrapy.Field()
    BookName = scrapy.Field()
    BookId = scrapy.Field()
    Signature = scrapy.Field()
    Type = scrapy.Field()
