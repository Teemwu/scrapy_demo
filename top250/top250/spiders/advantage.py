# -*- coding: utf-8 -*-
import scrapy
from top250.items import DefineItemLoader
from top250.items import Top250ItemLoader


class AdvantageSpider(scrapy.Spider):
    name = 'advantage'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        """ This function parses a property page
        @url https://movie.douban.com/top250
        @returns items 1
        @returns request 1
        @scrapes rank name des evaluate quote image_urls images
        """

        items = response.xpath('//*[@id="content"]/div/div[1]/ol/li')
        print(len(items))
        for item in items:
            l = DefineItemLoader(item=Top250ItemLoader(), response=response, selector=item)
            l.add_xpath('rank', 'div/div[1]/em/text()')
            l.add_xpath('name', 'div/div[2]/div[1]/a/span/text()')
            l.add_xpath('des', 'div/div[2]/div[2]/p[1]/text()')
            l.add_xpath('star', 'div/div[2]/div[2]/div/span[2]/text()')
            l.add_xpath('evaluate', 'div/div[2]/div[2]/div/span[4]/text()')
            l.add_xpath('quote', 'div/div[2]/div[2]/p[2]/span/text()')
            l.add_xpath('image_urls', 'div/div[1]/a/img/@src')
            l.add_xpath('images', 'div/div[1]/a/img/@src')

            detail_url = l.get_xpath('div/div[2]/div[1]/a/@href')[0]
            yield scrapy.Request(detail_url, meta={'item': l.load_item()}, callback=self.parse_item)
            
        next_link = l.get_xpath('//*[@id="content"]/div/div[1]/div[2]/span[3]/link/@href')
        if next_link:
            yield scrapy.Request('https://movie.douban.com/top250'+next_link[0], callback=self.parse)

    def parse_item(self, response):
        item = response.meta['item']
        l = DefineItemLoader(item=item, response=response)
        l.add_xpath('types', '//*[@property="v:genre"]/text()')
        l.add_xpath('runtime', '//*[@property="v:runtime"]/text()')
        l.add_xpath('summary', '//*[@property="v:summary"]/text()')
        yield l.load_item()
