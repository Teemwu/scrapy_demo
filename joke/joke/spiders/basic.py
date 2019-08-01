# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from joke.items import DefineItemLoader, JokeItem
# from urllib import request
# import os


class BasicSpider(CrawlSpider):
    name = 'basic'
    allowed_domains = ['laifudao.com']
    start_urls = ['http://www.laifudao.com']

    rules = (
        Rule(LinkExtractor(allow=r'/index_\d+.htm', unique=True), callback='parse_item', follow=True),
    )

    def parse_item(self, response):

        # path = os.getcwd()
        # images = os.path.join(path, 'images')
        # full_path = os.path.join(images, 'full')
        # thumb_path = os.path.join(images, 'thumb')
        # if not os.path.exists(images):
        #     os.mkdir(images)
        # if not os.path.exists(full_path):
        #     os.mkdir(full_path)
        # if not os.path.exists(thumb_path):
        #     os.mkdir(thumb_path)

        items = response.xpath('//article')
        for item in items:
            l = DefineItemLoader(item=JokeItem(), selector=item, response=response)
            l.add_xpath('title', 'header/h1/a/text()')
            l.add_xpath('uploader', 'header/p/a/text()')
            l.add_xpath('upload_time', 'header/p/time/text()')
            l.add_xpath('tags', 'header/p/span[2]/a/text()')
            l.add_xpath('article', 'div/section[1]/p')
            url_str = 'div/section[1]/a/img/@src'
            l.add_xpath('image_urls', url_str)
            l.add_xpath('image_names', url_str)
            l.add_xpath('image_thumbs', url_str)
            l.add_xpath('like', 'div/section[2]/div/a[1]/@title')
            l.add_xpath('like', 'div/section[3]/div/a[1]/@title')
            l.add_xpath('dislike', 'div/section[2]/div/a[2]/@title')
            l.add_xpath('dislike', 'div/section[3]/div/a[2]/@title')

            # 下载图片
            # names = l.get_output_value('image_names')
            # images = l.get_output_value('image_urls')
            # thumbs = l.get_output_value('image_thumbs')

            # for idx, name in enumerate(names):
            #     filename = full_path + os.sep + name
            #     thumbname = thumb_path + os.sep + name
            #     request.urlretrieve(images[idx], filename)
            #     request.urlretrieve(thumbs[idx], thumbname)

            yield l.load_item()
