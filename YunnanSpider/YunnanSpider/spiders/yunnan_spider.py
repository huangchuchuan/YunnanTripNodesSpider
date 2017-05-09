# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.utils.response import get_base_url
import json
import traceback
from YunnanSpider.items import YunnanspiderItem


class YunnanSpider(CrawlSpider):
    name = 'yunnan_spider'
    allowed_domains = ['chanyouji.com']
    start_urls = ['http://chanyouji.com/search/trips?q=%E4%BA%91%E5%8D%97']
    rules = [  # 定义爬取URL的规则
        Rule(sle(allow=(u"/search/trips\?page=\d{,4}")), follow=True, callback='parse_item')
    ]
    index_flag = True

    def parse_item(self, response):
        if YunnanSpider.index_flag:
            YunnanSpider.index_flag = False
            yield scrapy.Request(YunnanSpider.start_urls[0], callback=self.parse_item)

        sel = scrapy.Selector(response)
        sub_urls = sel.xpath('//div[@class="cover-image"]/a/@href').extract()
        for sub_url in sub_urls:
            yield scrapy.Request(url='http://chanyouji.com'+sub_url+'/map', callback=self.parse_detail)

    def parse_detail(self, response):
        item = YunnanspiderItem()
        item['youji_url'] = get_base_url(response)[:-4]
        sel = scrapy.Selector(response)
        item['place_name'] = sel.xpath('//li[@class="trip-node"]/span/text()').extract()
        return item
