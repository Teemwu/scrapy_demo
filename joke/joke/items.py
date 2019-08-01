# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst, Identity, Compose, MapCompose, Join
from w3lib.html import remove_tags
import re


class DefineItemLoader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_tags_not_br(val):
    article_str = ''
    article_str = remove_tags(val, keep=('br'))
    return article_str


def extract_int(val):
    num = 0
    num = int(re.findall(r'\d+', val)[0])
    return num

def extract_name(val):
    return val.split('/')[-1]

def extract_urls(val):
    return 'http://down1.laifudao.com/tupian/' + val.split('/')[-1]

class JokeItem(Item):
    title = Field()
    tags = Field(
        ouput_processor=Identity()
    )
    uploader = Field()
    article = Field(
        input_processor=MapCompose(remove_tags_not_br),
        ouput_processor=Join()
    )
    image_thumbs=Field(
        output_processor=Identity()
    )
    image_names = Field(
        output_processor=MapCompose(extract_name)
    )
    image_urls = Field(
        output_processor=MapCompose(extract_urls)
    )
    image_paths = Field(
        output_processor=Identity()
    )
    upload_time = Field(
        input_processor=Compose(lambda i: i[0].strip())
    )
    like = Field(
        input_processor=MapCompose(extract_int)
    )
    dislike = Field(
        input_processor=MapCompose(extract_int)
    )
