# -*- coding: utf-8 -*-
import scrapy
import time
import random
import pandas as pd
from douban.items import CityItem


class ShortSpider(scrapy.Spider):
    name = 'city'
    allow_domains = ['www.douban.com']

    def start_requests(self):
        '''
        重写start_requests方法
        '''

        # 浏览器用户代理
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'
        }
        # 指定cookies
        self.cookies = {
            'll':'"108288"',
            'bid':'7Yl2TZlzfSI',
            '__utmc':'30149280',
            'push_noty_num':'0',
            'push_doumail_num':'0',
            '__utmv':'30149280.18235',
            '__yadk_uid':'lPCMCt02tT9gaajKHuvTS3WpTDpgaapq',
            'ps':'y',
            'douban-fav-remind':'1',
            '_vwo_uuid_v2':'D1749BD014B125860682207D4A487E7EE|f22e1cb1f65f729c8f49ee69a39b5fd9',
            'ct':'y',
            '__utmz':'30149280.1551065390.16.5.utmcsr=movie.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/subject/26266893/comments',
            '_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1551077028%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3D9e985decb975f32f%26alias%3D%22%5D',
            '_pk_ses.100001.8cb4':'*',
            'ck':'Jhip',
            '_pk_id.100001.8cb4':'6d50491579a8b10f.1550911347.11.1551077144.1551065400.',
            '__utma':'30149280.239591189.1550911349.1551065390.1551077146.17',
            '__utmt':'1',
            '__utmb':'30149280.1.10.1551077146',
            'dbcl2':'"182356526:y/1DW5cCz+8"'
        }
        urls = [
            'https://www.douban.com/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        '''
        获取下一页链接
        '''
        p = 1
        df = pd.read_csv('./comments.csv', names=['name', 'score', 'comments', 'date', 'href'])
        hrefs = df.href
        for href in hrefs:
            print('正在爬取第%d页数据' % p)
            p += 1
            yield scrapy.Request(url=href, headers=self.headers, cookies=self.cookies, callback=self.city_parse)
            time.sleep(round(random.uniform(2, 3), 2))

    def city_parse(self, response):
        '''
        获取用户评论信息
        '''
        item = CityItem()
        city = response.xpath('//div[@class="user-info"]/a/text()')
        # 有些用户没有填写居住城市
        if city:
            item['city'] = city.extract()[0]
        else:
            item['city'] = '--'
        yield item # 返回item