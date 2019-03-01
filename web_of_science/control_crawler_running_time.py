from multiprocessing import Process
from scrapy import cmdline
import time
import logging

from WOS_settings import spider_1_name,time_interval_between_start_up_spider

# 配置参数即可, 爬虫名称，运行频率
confs = [
    {
        "spider_name": spider_1_name,
        "delay_time":600, # delay_time表示某一只爬虫运行结束后等待的时间
    },
 #   {
 #       "spider_name": spider_2_name,
 #       "delay_time": 600,
 #   },
]



def start_spider(spider_name, delay_time):
    args = ["scrapy", "crawl", spider_name]
    while True:
        start = time.time()
        p = Process(target=cmdline.execute, args=(args,))
        p.start()
        p.join()
        logging.debug("### use time: %s" % (time.time() - start))
        time.sleep(delay_time)


if __name__ == '__main__':
    for conf in confs:
        process = Process(
            target=start_spider, args=(conf["spider_name"], conf["delay_time"]))
        process.start()
        time.sleep(time_interval_between_start_up_spider) #等待time_interval_between_start_up_spider秒，再开启下一个爬虫
        # 爬虫只要开启，爬虫之间就各自独立运行不在干涉。比如这里时间设置为0，则同时开启三只爬虫。

