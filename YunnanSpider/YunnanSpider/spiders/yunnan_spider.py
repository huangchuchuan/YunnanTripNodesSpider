# -*- coding: utf-8 -*-

import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor as sle
from scrapy.utils.response import get_base_url
from YunnanSpider.items import YunnanspiderItem


def position_dict_str2unicode(d):
    desc = d['description']
    desc = desc.replace(' ', '').replace('"', "'").replace('\r', '').replace('\n', '')
    desc = 'u"' + desc + '"'
    d['description'] = eval(desc)
    title = d['title']
    title = title.replace(' ', '').replace('"', "'").replace('\r', '').replace('\n', '')
    title = 'u"' + title + '"'
    d['title'] = eval(title)


class YunnanSpider(CrawlSpider):
    name = 'yunnan_spider'
    search_keyword = '云南'
    allowed_domains = ['chanyouji.com']
    start_urls = ['http://chanyouji.com/search/trips?q={}'.format(search_keyword)]
    rules = [  # 定义爬取URL的规则
        Rule(sle(allow=(u"/search/trips\?page=\d{,4}")), follow=True, callback='parse_item')
    ]
    index_flag = True

    def parse_item(self, response):
        if YunnanSpider.index_flag:
            YunnanSpider.index_flag = False
            yield scrapy.Request(YunnanSpider.start_urls[0], callback=self.parse_item)

        sub_urls = response.xpath('//div[@class="cover-image"]/a/@href').extract()
        for sub_url in sub_urls:
            yield scrapy.Request(url='http://chanyouji.com'+sub_url+'/map', callback=self.parse_detail)

    def parse_detail(self, response):
        item = YunnanspiderItem()
        item['youji_url'] = get_base_url(response)[:-4]
        nodes = response.xpath('//li[@class="trip-node"]')
        place_list = []
        star_list = []
        for node in nodes:
            place_list.append(node.xpath('./span/text()').extract_first())
            star_node = node.xpath('./div/@class')
            if star_node and star_node.extract_first().startswith('star'):
                star = int(star_node.extract_first().split('-')[-1])
            else:
                star = 1
            star_list.append(star)
        item['place_name'] = place_list
        item['place_star'] = star_list
        item['place_position'] = []
        js_data = response.xpath('//script').extract()[4]
        p = js_data.find('Gmaps.map.markers =')
        if p != -1:
            line = js_data[p:]
            p = line.find('[')
            pe = line.find('}]')
            array = line[p:pe+2]
            position_list = eval(array)  # [{lat:xxx, lng:xxx, description:xxx, title:xxx}]
            for position_dict in position_list:
                position_dict_str2unicode(position_dict)
                item['place_position'].append(position_dict)

        return item
