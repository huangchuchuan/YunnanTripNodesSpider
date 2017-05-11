# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.utils.response import get_base_url
from YunnanSpider.items import YunnanHotplacesItem



class YunnanHotplacesSpider(CrawlSpider):
    name = 'yunnan_hotplaces_spider'
    allowed_domains = ['chanyouji.com']
    start_urls = ['http://chanyouji.com/search/attractions?q=%E4%BA%91%E5%8D%97']
    rules = [  # 定义爬取URL的规则
        Rule(sle(allow=(u"/search/attractions\?page=\d{,4}")), follow=True, callback='parse_item')
    ]
    index_flag = True

    def parse_item(self, response):
        if YunnanHotplacesSpider.index_flag:
            YunnanHotplacesSpider.index_flag = False
            yield scrapy.Request(YunnanHotplacesSpider.start_urls[0], callback=self.parse_item)

        articles = response.xpath('//article[@class="attration-list-item"]')
        sub_urls = articles.xpath('.//a/@href').extract()
        places = articles.xpath('.//h1/text()').extract()
        stars = []
        for article in articles:
            score = article.xpath('.//div[@class="score"]').extract_first()
            score = score.count(u'★')
            stars.append(score)

        item = YunnanHotplacesItem()
        item['place_url'] = map(lambda x: 'http://chanyouji.com'+x, sub_urls)
        item['place_name'] = places
        item['place_score'] = stars

        yield item