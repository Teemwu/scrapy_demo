# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item


class Top250Item(Item):
    rank = Field()
    name = Field()
    des = Field()
    star = Field()
    evaluate = Field()
    quote = Field()
    images = Field()
    image_urls = Field()
    image_paths = Field()

    # 详情页
    types = Field()
    summary = Field()
    runtime = Field()
