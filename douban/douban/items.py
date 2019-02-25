# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field() # 评论用户
    score = scrapy.Field() # 评分
    comment = scrapy.Field() # 评论
    date = scrapy.Field() # 评论日期
    href = scrapy.Field() # 用户个人主页

class CityItem(scrapy.Item):
    city = scrapy.Field() # 用户常居地址