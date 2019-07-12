# -*- coding: utf-8 -*-
import scrapy
from top250.items import Top250Item


class BasicSpider(scrapy.Spider):
    name = 'basic'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        items = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        for item in items:
            top250_item = Top250Item()
            # 排名
            top250_item['rank'] = item.xpath('.//div/div[1]/em/text()').extract_first()
            # 名称
            names = item.xpath('.//div/div[2]/div[1]/a/span')
            name_str = ''
            for name in names:
                name_str += ''.join(name.xpath('.//text()').extract_first().split()).strip()
            top250_item['name'] = name_str
            # 简介
            contents = item.xpath('.//div/div[2]/div[2]/p[1]/text()').extract()
            content_str = ''
            for content in contents:
                content_str += ''.join(content.split())
            top250_item['des'] = content_str
            # 评分
            top250_item['star'] = item.xpath('.//div/div[2]/div[2]/div/span[2]/text()').extract_first()
            # 评价
            top250_item['evaluate'] = item.xpath('.//div/div[2]/div[2]/div/span[4]/text()').extract_first()
            # 描述
            top250_item['quote'] = item.xpath('.//div/div[2]/div[2]/p[2]/span/text()').extract_first()
            # 海报
            top250_item['image_urls'] = item.xpath('.//div/div[1]/a/img/@src').extract()
            top250_item['images'] = item.xpath('.//div/div[1]/a/img/@src').re(r'[^/]*.[jpg|png|gif|webp]$')

            yield top250_item

        next_link = response.xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/link/@href').extract()

        if next_link:
            next_link = next_link[0]
            yield scrapy.Request('https://movie.douban.com/top250'+next_link, callback=self.parse)
