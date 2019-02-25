# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pandas as pd

class DoubanPipeline(object):
    def __init__(self):
        self.i = 0

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    '''
    def process_item(self, item, spider):
        name = item['name']
        score = item['score']
        comment = item['comment']
        date = item['date']
        href = item['href']
        # 保存用户评论临时信息
        df = pd.DataFrame({
            'name': ['1'],
            'score': ['1'],
            'comment': ['1'],
            'date': ['1'],
            'href': ['1']
        })
        df['name'] = name
        df['score'] = score
        df['comment'] = comment
        df['date'] = date
        df['href'] = href
        df.rename(index={0: self.i}, inplace=True)
        self.i += 1
        print('正在向comments.csv写入第%d条数据' % self.i)
        df.to_csv('comments.csv', mode='a', encoding='utf-8-sig', header=False)
    '''

    def process_item(self, item, spider):
        city = item['city']
        # 保存用户评论临时信息
        df = pd.DataFrame({
            'city': ['1']
        })
        df['city'] = city
        df.rename(index={0: self.i}, inplace=True)
        self.i += 1
        print('正在向cities.csv写入第%d条数据' % self.i)
        df.to_csv('cities.csv', mode='a', encoding='utf-8-sig', header=False)