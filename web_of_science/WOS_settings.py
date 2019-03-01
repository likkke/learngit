# 本文件是针对 http://apps.webofknowledge.com 网站的配置文件
# -----项目环境配置-----开始-----
# 对应的chromedriver的放置目录
# 注意要保持谷歌浏览器的驱动器和谷歌浏览器版本相对应，最好都使用最新版
path_to_chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
# 该项目文件所用的python.exe所在位置
path_to_python = r'C:/Python/Python36/python.exe'
# 项目依赖库

# -----项目环境配置-----结束-----


# -----selenium 配置-----开始-----
# Web of Science 基本选项 （通过 selenium 执行）
# 谷歌浏览器的驱动器访问WOS网站方式,根据本机运行情况选择
# 方式一：通过百度转跳到WOS网站；方式二：直接访问WOS官网情况
way_to_access_the_WOS_web_site = 'one'
#way_to_access_the_WOS_web_site = 'two'

# 是否显示Python操作浏览器的情况(不影响结果)
#display_operation_browser = False
display_operation_browser = True #显示爬虫操作浏览器过程
#display_operation_browser_insert_Highly_Cited_Paper = True # 显示更新 Highly_Cited_Paper 过程


# -----关于 http://apps.webofknowledge.com/ 首页的配置---开始-----
# 选择数据库，默认所有数据库
# 数据库编号 1-8，与 WOS 网站选择数据库顺序对应
# 1：所有数据库，2：Web of Science 核心合集，3：Derwent Innovations Index...
select_a_database_index = 2

# 基本检索途径，默认出版物名称
# 检索途径 1-10，与 WOS 网站检索途径顺序对应
# 1：主题，2：标题，3：作者...7：出版物名称...
basic_search_channel_index = 3
# -----关于 http://apps.webofknowledge.com/ 首页的配置---结束-----

# -----关于 http://apps.webofknowledge.com/查询结果过滤页面 Refine Results 的配置---开始-----
# Filter results by
#勾选 Highly_Cited_in_Field，默认不勾选；当 basic_search_channel_index = 3 时默认勾选
IS_Highly_Cited_in_Field = False

#Web of Science Categories:处理指定学科的论文，可以指定多个，默认为None
#Web_of_Science_Categories = None
Web_of_Science_Categories = ["COMPUTER SCIENCE",]

# 时间跨度，默认所有年份
# 时间跨度选择编号 1-7，与 WOS 网站时间跨度顺序对应
# 1：所有年份，2：最近5年，3：本年迄今...,7：自定义年份
time_span_index = 1
# 当 time_span_index = 7 时下面配置有效
time_span_start_year = 2008
time_span_end_year = 2018
# -----关于 http://apps.webofknowledge.com/查询结果过滤页面的配置---结束-----
# -----selenium 配置-----结束-----


# ---------------单个爬虫运行配置----------------------------开始-----
# 爬虫发次向目标网站发出多少个请求，越大越快
CONCURRENT_REQUESTS = 10
# 每次请求抓取网站后等待多少秒再发出下一次请求，越小越快
DOWNLOAD_DELAY = 1
# 每向网站请求 K 次时 暂停爬虫 M 秒
K_second = 18000
K_per_request = K_second/(CONCURRENT_REQUESTS/DOWNLOAD_DELAY)
M_second = 30

# ---------------单个爬虫运行配置----------------------------结束-----



# ---------------多个爬虫运行控制配置------------------------开始-----
# 爬虫的名字
spider_1_name = 'author_spider'
#spider_2_name = 'publication_spider'
#spider_3_name = 'publication_spider'
# 启动不同爬虫之间的时间间隔，单位秒
time_interval_between_start_up_spider = 1200
# ---------------多个爬虫运行控制配置------------------------结束-----



#------------------------------------任务输入文件存放位置---------------------开始-------------------
# 出版物名称文件放置位置
path_to_publication_names_xlsx_file = r'E:\web_of_science\input_task_file\publication_names_file.xlsx'
path_to_publication_names_txt_file = r'E:\web_of_science\input_task_file\publication_names.txt'
#高引作者名称文件放置位置
path_to_auhthor_names_txt_file = r'E:\web_of_science\input_task_file\高引学者.txt'
#------------------------------------任务输入文件存放位置---------------------结束-------------------



#------------------------------------任务输出文件位置-------------------------开始-------------------
#任务输出的cookies和任务url等中间临时信息
path_to_cookeis_pickle = r"E:\web_of_science\temporary_documents\cookies.pickle"
path_to_task_url_info_list_pickle = r"E:\web_of_science\temporary_documents\task_url_info_list.pickle"

#爬虫运行日志
# 日志记录等级：CRITICAL - 严重错误 ERROR - 一般错误 WARNING - 警告信息 INFO - 一般信息 DEBUG - 调试信息
LOG_LEVEL = 'INFO'
#  日志记录文件路径
LOG_FILE = 'log.txt'

# 存储文件的数据库名称
DataBase_name = "te"
#------------------------------------任务输出文件位置-------------------------结束-------------------



