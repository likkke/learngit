from pymongo import MongoClient
import random

class MongoDB_table(object):
    def __init__(self, databace, collection, host='localhost', port=27017, ):
        self.client = MongoClient(host=host, port=port)
        self.databace = self.client[databace]
        self.collection = self.databace[collection]

    def close(self):
        self.client.close()

    # 自动释放与数据库的链接
    def __del__(self):
        self.client.close()

class MongoDB_info_manager(object):
    def __init__(self, databace_name):
        self.DB_name = databace_name
        self.basic_information_of_the_paper = MongoDB_table(self.DB_name,'Basic_information_of_the_paper')
        self.basic_information_of_the_quoted_paper = MongoDB_table(self.DB_name,'Basic_information_of_the_quoted_paper')

    def get_paper_location(self, basic_search_channel_index,task_name):
        if basic_search_channel_index==7:
            task_name_key="journal_name"
        elif basic_search_channel_index==3:
            task_name_key="author_name"
        else:
            raise ValueError("暂时不支持该basic_search_channel_index")
        #获取指向指定任务所有的高引论文信息的游标
        basic_information_of_the_paper_info_cursor = self.basic_information_of_the_paper.collection.find({task_name_key: task_name})
        #遍历任务所有的高引论文信息
        already_processed_paper_location = []
        for basic_information_of_the_paper_info in basic_information_of_the_paper_info_cursor:
            #获取高引论文处于任务高引论文集的位置
            page_doc_tuple = basic_information_of_the_paper_info['page_doc_tuple']
            already_processed_paper_location.append(tuple(page_doc_tuple))
        return already_processed_paper_location

from WOS_settings import DataBase_name,basic_search_channel_index
if __name__ == '__main__':
    mongoDB_info_manager = MongoDB_info_manager(DataBase_name)
    task_name = "IEEE WIRELESS COMMUNICATIONS LETTERS"
    already_processed_paper_location = mongoDB_info_manager.get_paper_location(basic_search_channel_index,task_name)
    print(already_processed_paper_location)