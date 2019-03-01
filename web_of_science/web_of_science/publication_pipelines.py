# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from .publication_items import Basic_information_of_the_paper_publication_Item, \
    Basic_information_of_the_quoted_paper_publication_Item


class WebOfSciencePipeline(object):
    def process_item(self, item, spider):
        return item

from WOS_settings import DataBase_name

class WebOfScienceItem_publication_Pipeline(object):
    def __init__(self):
        client = pymongo.MongoClient()
        tdb = client[DataBase_name]
        self.post_Basic_information_of_the_paper = tdb['Basic_information_of_the_paper']
        self.post_Basic_information_of_the_quoted_paper = tdb['Basic_information_of_the_quoted_paper']


    def process_item(self, item, spider):
        '''先判断itme类型，在放入相应数据库'''
        if isinstance(item, Basic_information_of_the_paper_publication_Item):
            try:
                basic_information_of_the_paper = dict(item)  # 把item转化成字典形式
                self.post_Basic_information_of_the_paper.insert(basic_information_of_the_paper)
            except Exception as e:
                print(e)

        if isinstance(item, Basic_information_of_the_quoted_paper_publication_Item):
            try:
                basic_information_of_the_quoted_paper = dict(item)  # 把item转化成字典形式
                self.post_Basic_information_of_the_quoted_paper.insert(basic_information_of_the_quoted_paper)
            except Exception as e:
                print(e)

        return item