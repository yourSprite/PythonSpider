# -*- coding: utf-8 -*-
import scrapy
import time
import random
from douban.items import DoubanItem


class ShortSpider(scrapy.Spider):
    name = 'short'
    allow_domains = ['movie.douban.com']

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
            'll':''"108288"'',
            'bid':'7Yl2TZlzfSI',
            '__utmc':'30149280',
            'push_noty_num':'0',
            'push_doumail_num':'0',
            '__utmv':'30149280.18235',
            '__yadk_uid':'lPCMCt02tT9gaajKHuvTS3WpTDpgaapq',
            'ps':'y',
            'douban-fav-remind':'1',
            '_vwo_uuid_v2':'D1749BD014B125860682207D4A487E7EE|f22e1cb1f65f729c8f49ee69a39b5fd9',
            'ap_v':'0,6.0',
            'ct':'y',
            '_pk_ref.100001.8cb4':'%5B%22%22%2C%22%22%2C1551016087%2C%22https%3A%2F%2Faccounts.douban.com%2Fsafety%2Funlock_sms%2Fresetpassword%3Fconfirmation%3D9e985decb975f32f%26alias%3D%22%5D',
            '_pk_ses.100001.8cb4':'*',
            '__utma':'30149280.239591189.1550911349.1551011979.1551016088.12',
            '__utmz':'30149280.1551016088.12.4.utmcsr=accounts.douban.com|utmccn=(referral)|utmcmd=referral|utmcct=/safety/unlock_sms/resetpassword',
            '__utmt':'1',
            'dbcl2':'"182356526:v3gOdkeBjIU"',
            'ck':'Mu7m',
            '_pk_id.100001.8cb4':'6d50491579a8b10f.1550911347.9.1551016114.1551013903.',
            '__utmb':'30149280.3.10.1551016088'
        }
        urls = [
            'https://movie.douban.com/subject/26266893/comments?start=0&limit=20&sort=new_score&status=P'
        ]
        for url in urls:
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.parse)

    def parse(self, response):
        '''
        获取下一页链接
        '''
        k = 0
        p = 1
        # 豆瓣只开放500条评论
        while k <= 480:
            url = 'https://movie.douban.com/subject/26266893/comments?start=' + str(k) + '&limit=20&sort=new_score&status=P'
            print('正在爬取第%d页数据' % p)
            p += 1
            yield scrapy.Request(url=url, headers=self.headers, cookies=self.cookies, callback=self.content_parse)
            k += 20
            time.sleep(round(random.uniform(2, 3), 2))

    def content_parse(self, response):
        '''
        获取用户评论信息
        '''
        contents = response.xpath('//div[@class="comment"]')
        for content in contents:
            item = DoubanItem()
            name = content.xpath('./h3/span[@class="comment-info"]/a/text()').extract()[0]
            score = content.xpath('./h3/span[@class="comment-info"]/span[2]').attrib.get('title')
            # 这里span标签内的文字换行会导致写入数据出现问题，因此直接把评论带标签拿出来，之后再做处理
            comment = content.xpath('./p/span[@class="short"]').extract()[0]
            date = content.xpath('./h3/span[@class="comment-info"]/span[@class="comment-time "]/text()').extract()[0].strip()
            # 获取评论用户主页链接，用于爬取用户常居城市
            href = content.xpath('./h3/span[@class="comment-info"]/a/@href').extract()[0]
            item['name'] = name
            # 判断用户是否评分，未评分第二个span标签是时间，这里通过长度判断
            if len(score) < 5:
                item['score'] = score
            else:
                item['score'] = '--'
            item['comment'] = comment
            item['date'] = date
            item['href'] = href
            yield item # 返回item