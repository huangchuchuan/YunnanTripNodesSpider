# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YunnanspiderItem(scrapy.Item):
    # define the fields for your item here like:
    youji_url = scrapy.Field()
    place_name = scrapy.Field()
    place_star = scrapy.Field()
    place_position = scrapy.Field()
    pass
