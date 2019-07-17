# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import MapCompose, TakeFirst, Join, Compose, Identity
from w3lib.html import remove_tags_with_content, replace_escape_chars


def converStr(vals):
    _str = ''
    for val in vals:
        _str += ''.join(val.split()).strip()
    return _str


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


class DefineItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


class Top250ItemLoader(Item):
    rank = Field(
        output_processor=Compose(lambda i: int(i[0]))
    )
    name = Field(
        output_processor=Compose(converStr)
    )
    des = Field(
        output_processor=Compose(converStr)
    )
    star = Field(
        output_processor=Compose(lambda i: float(i[0]))
    )
    evaluate = Field(
        output_processor=TakeFirst()
    )
    quote = Field()
    images = Field(
        output_processor=Identity()
    )
    image_urls = Field(
        output_processor=Identity()
    )
    image_paths = Field(
        output_processor=Identity()
    )

    # 详情页
    types = Field(
        output_processor=Identity()
    )
    summary = Field(
        output_processor=Compose(converStr)
    )
    runtime = Field()
