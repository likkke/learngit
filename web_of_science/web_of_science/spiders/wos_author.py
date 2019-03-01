import scrapy
import random
import queue
import time
from dependency_function import MD5_ID, get_int_from_str, generate_initial_task_URL_list
from DataBase_manager.MongoDB_manager import MongoDB_info_manager
from WOS_settings import path_to_auhthor_names_txt_file

from ..author_items import Basic_information_of_the_paper_author_Item,\
    Basic_information_of_the_quoted_paper_author_Item

from dependency_function import Help_Analysis_Information_of_Paper,get_first_and_del_first_item_from_list,\
    find_last_two_numbers

from tool_case.read_input_task_files import read_highly_cited_author_names_txt

from webofknowledge_homepage import WebOfKnowledge_homepage
from WOS_settings import display_operation_browser, path_to_chromedriver,\
    way_to_access_the_WOS_web_site, select_a_database_index, basic_search_channel_index,\
    time_span_start_year, time_span_end_year,\
    CONCURRENT_REQUESTS,DOWNLOAD_DELAY, LOG_LEVEL,LOG_FILE,DataBase_name,K_per_request,M_second


class WOS_Author_Spider(scrapy.Spider):
    name = 'author_spider'
    md5_id = MD5_ID()
    cookeis = None
    author_url_list = None
    custom_settings = {
        'DOWNLOAD_DELAY': DOWNLOAD_DELAY,
        'CONCURRENT_REQUESTS':CONCURRENT_REQUESTS,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'COOKIES_ENABLED':True,
#        'LOG_LEVEL':LOG_LEVEL,
#        'LOG_FILE':LOG_FILE,
       # 'COOKIES_DEBUG':True,
       'ITEM_PIPELINES':{ 'web_of_science.author_pipelines.WebOfScienceItem_author_Pipeline': 300,},
        #'SPIDER_MIDDLEWARES':{'web_of_science.middlewares_selenium.SeleniumMiddleware': 250,}
    }

    def __init__(self, category=None, *args, **kwargs):
        super(WOS_Author_Spider, self).__init__(*args, **kwargs)
        self.mongoDB_info_manager = MongoDB_info_manager(DataBase_name)



    #1  初始化任务和任务相关论文URL链接，生成该任务所有论文URL
    def start_requests(self):
        # 读取任务名称列表，读其它格式文件，直接写在 E:\web_of_science\tool_case\read_input_task_files.py
        author_name_list = read_highly_cited_author_names_txt(path_to_auhthor_names_txt_file)
        # Example: ['Abecasis, GR', 'Acharya, UR', 'Akyildiz, IF']
        a_task_url_index = 0
        task_names_queue = queue.Queue()
        # 把任务名放入任务队列
        for a_task_index,a_task_name in enumerate(author_name_list):
            print('正在往任务队列中放入任务{}'.format(a_task_name))
            task_names_queue.put(a_task_name)
        while not task_names_queue.empty():
            # time.sleep(150)
            new_task_name = task_names_queue.get()
            print('本次的任务名称：{}'.format(new_task_name))
            wos_homepage = WebOfKnowledge_homepage(path_to_chromedriver=path_to_chromedriver,
                                                   display_operation_browser=display_operation_browser,
                                                   way_to_access_the_WOS_web_site=way_to_access_the_WOS_web_site,
                                                   select_a_database_index=select_a_database_index,
                                                   basic_search_channel_index=basic_search_channel_index,
                                                   time_span_start_year=time_span_start_year,
                                                   time_span_end_year=time_span_end_year)
            new_wos_task_name_cookie_info_dict = wos_homepage.parse_WOS_home_page_options([new_task_name])
            cookies = new_wos_task_name_cookie_info_dict['wos_cookies']
            self.cookeis = cookies
            new_task_url_info_list = new_wos_task_name_cookie_info_dict['task_url_info_list']
            # 获取该任务已经处理的论文
            already_processed_paper_location = self.mongoDB_info_manager.get_paper_location(basic_search_channel_index,
                                                                                       new_task_name)
            for task_name, First_Paper_URL, last_page_num_index, last_paper_numbers in new_task_url_info_list:
                new_last_page_num_index = get_int_from_str(last_page_num_index)
                new_last_paper_numbers = get_int_from_str(last_paper_numbers)
                initial_task_URL_list = generate_initial_task_URL_list(First_Paper_URL, new_last_page_num_index,
                                                                       new_last_paper_numbers)
            random.shuffle(initial_task_URL_list) #打乱任务请求的顺序
            # initial_task_URL_list = initial_task_URL_list[:100]
            a_task_url = get_first_and_del_first_item_from_list(initial_task_URL_list)

            while a_task_url is not None:
                print('task_url_index', a_task_url_index)
                a_task_url_index += 1
                # 每发送 K_per_request 个请求，爬虫暂停 M_second 秒，并且更新 cookies
                if (a_task_url_index+1)%K_per_request==0:
                    time.sleep(M_second)
                    wos_homepage.parse_WOS_home_page_options([new_task_name])
                    cookies = new_wos_task_name_cookie_info_dict['wos_cookies']
                    self.cookeis = cookies
                # 获取当前论文的位置
                page_doc_tuple = find_last_two_numbers(a_task_url)
                # 只处理爬虫没有处理的论文
                if page_doc_tuple not in already_processed_paper_location:
                    yield scrapy.Request(url=a_task_url, callback=self.analysis_basic_information_of_the_paper,
                                         dont_filter=True,
                                         cookies=self.cookeis,
                                         meta={'cookiejar':True, 'task_name': task_name, "page_doc_tuple":page_doc_tuple})

                a_task_url = get_first_and_del_first_item_from_list(initial_task_URL_list)
                print("当前剩余任务量{}".format(len(initial_task_URL_list)))

    # 2  根据某个论文URL链接，解析该论文内容，同时获取引用该论文的首页导航链接
    def analysis_basic_information_of_the_paper(self, response):
        #-------------分析爬虫状态是否正常，如果异常直接主动关闭爬虫------------------
        error_trigger_conditions_list = [False]
        now_url = response.url
        #if "error" in now_url:
        #    error_trigger_condition_1 = True
        #    error_trigger_conditions_list.append(error_trigger_condition_1)
        if any(error_trigger_conditions_list)==True:
            self.crawler.engine.close_spider(self, '爬虫抓取数据状态异常，主动关闭爬虫')

        task_name = response.meta['task_name']
        page_doc_tuple = response.meta['page_doc_tuple']

        help_analysis_information_of_paper =  Help_Analysis_Information_of_Paper(response)

        # -----------------------------调用解析文章元素函数，获取文章元素值--------开始---
        author_name = response.meta['task_name']
        author_index = self.md5_id.create_uid(response.meta['task_name'])

        paper_title = help_analysis_information_of_paper.analysis_paper_title()
        paper_index = help_analysis_information_of_paper.analysis_paper_index(paper_title)
        paper_volume = help_analysis_information_of_paper.analysis_paper_volume()
        paper_DOI = help_analysis_information_of_paper.analysis_paper_DOI()
        paper_publication_year = help_analysis_information_of_paper.analysis_paper_publication_year()
        paper_ducument_type = help_analysis_information_of_paper.analysis_paper_ducument_type()

        Journal_Impact_factor = help_analysis_information_of_paper.analysis_Journal_Impact_factor()
        Journal_Citation_Reports_info = help_analysis_information_of_paper.analysis_papar_Journal_Citation_Reports_info()
        Journal_ISSN = help_analysis_information_of_paper.analysis_paper_Journal_ISSN()
        Journal_eISSN = help_analysis_information_of_paper.analysis_paper_Journal_eISSN()

        Funding_info = help_analysis_information_of_paper.analysis_paper_Funding_info()
        Fouding_text = help_analysis_information_of_paper.analysis_paper_Fouding_text()

        paper_the_number_of_quotes_possible = help_analysis_information_of_paper.analysis_paper_the_number_of_quotes_possible()

        paper_authors, abstract, Author_keywords, Keywords_plus, paper_communication_author_reprint, \
        paper_communication_author_info_addresses, paper_e_mail_addresses, Publisher, \
        research_areas, web_of_science_categories, Document_Information, Other_Information = \
            help_analysis_information_of_paper.analysis_paper_block_record_many_info()

        # -----------------------------调用解析文章元素函数，获取文章元素值--------结束---

        # -----------------------------将元素值赋值给 items 并且传送给 pipelines---开始---
        basic_information_of_the_paper_item = Basic_information_of_the_paper_author_Item()
        basic_information_of_the_paper_item['paper_title'] = paper_title
        basic_information_of_the_paper_item['paper_index'] = paper_index
        basic_information_of_the_paper_item['paper_volume'] = paper_volume
        basic_information_of_the_paper_item['paper_DOI'] = paper_DOI
        basic_information_of_the_paper_item['paper_publication_year'] = paper_publication_year
        basic_information_of_the_paper_item['paper_ducument_type'] = paper_ducument_type
        basic_information_of_the_paper_item['Journal_Impact_factor'] = Journal_Impact_factor
        basic_information_of_the_paper_item['Journal_Citation_Reports_info'] = Journal_Citation_Reports_info
        basic_information_of_the_paper_item['Journal_ISSN'] = Journal_ISSN
        basic_information_of_the_paper_item['Journal_eISSN'] =Journal_eISSN
        basic_information_of_the_paper_item['Funding_info'] = Funding_info
        basic_information_of_the_paper_item['Fouding_text'] = Fouding_text
        basic_information_of_the_paper_item['paper_the_number_of_quotes_possible'] = paper_the_number_of_quotes_possible
        basic_information_of_the_paper_item['paper_authors'] = paper_authors
        basic_information_of_the_paper_item['abstract'] = abstract
        basic_information_of_the_paper_item['Author_keywords'] = Author_keywords
        basic_information_of_the_paper_item['paper_communication_author_reprint'] = paper_communication_author_reprint
        basic_information_of_the_paper_item['paper_communication_author_info_addresses'] = paper_communication_author_info_addresses
        basic_information_of_the_paper_item['paper_e_mail_addresses'] = paper_e_mail_addresses
        basic_information_of_the_paper_item['Publisher'] = Publisher
        basic_information_of_the_paper_item['research_areas'] = research_areas
        basic_information_of_the_paper_item['web_of_science_categories'] = web_of_science_categories
        basic_information_of_the_paper_item['Document_Information'] = Document_Information
        basic_information_of_the_paper_item['Other_Information'] = Other_Information
        basic_information_of_the_paper_item['page_doc_tuple'] = page_doc_tuple
        yield basic_information_of_the_paper_item
        # -----------------------------将元素值赋值给 items 并且传送给 pipelines---结束---

        # 获取引用该论文的论文页数（一页默认有 10 篇论文）
        if paper_the_number_of_quotes_possible is None:
            paper_the_number_of_quotes_possible = 0
        if (paper_the_number_of_quotes_possible%10)!=0:
            paper_the_number_of_quotes_possible = int(paper_the_number_of_quotes_possible / 10) + 1
        else:
            paper_the_number_of_quotes_possible = int(paper_the_number_of_quotes_possible / 10)

        # 论文发表年份不能为 None 值
        if paper_publication_year is None:
            raise ValueError("paper_publication_year is None")

         # 获取论文 引文网络链接，当论文有引文时进入引文网络
        if paper_the_number_of_quotes_possible > 0 and paper_publication_year:
            citation_network = response.xpath('//div[@class="flex-row flex-justify-start flex-align-start box-div"]/div/a/@href').extract_first()
            citation_network_URL = response.urljoin(citation_network)
            yield scrapy.Request(
                url=citation_network_URL,callback=self.analysis_list_paper_of_the_quoted_paper,dont_filter=True,
                meta={'cookiejar':True,'paper_title':paper_title,'paper_index':paper_index,
                      "paper_publication_year":paper_publication_year,
                      "paper_url":citation_network_URL,
                      "citation_url_page_number":paper_the_number_of_quotes_possible})
        else:
            #print("该论文没有引用它的文献！")
            pass

    #3  通过引用某论文的首页导航链接，获取其他页导航链接（如果有）
    def analysis_list_paper_of_the_quoted_paper(self,response):
        citation_network_url_list = []
        quoted_paper_title = response.meta['paper_title']
        quoted_paper_index = response.meta['paper_index']
        citation_network_url_list.append(response.meta['paper_url'])
        citation_url_page_number = response.meta['citation_url_page_number']
        paper_publication_year = response.meta['paper_publication_year']
        if citation_url_page_number > 1:
            navigation_to_next = response.xpath('//a[@class="paginationNext snowplow-navigation-nextpage-top"]/@href').extract_first()
            navigation_to_other = str(navigation_to_next).replace('page=2', "page={}")
            for citation_url_page in range(2, citation_url_page_number + 1):
                if citation_url_page:
                    citation_network_url_list.append(navigation_to_other.format(citation_url_page))
        #random.shuffle(citation_network_url_list)
        for citation_network_url in citation_network_url_list:
            yield scrapy.Request(url=citation_network_url,
                                 callback=self.access_all_web_pages_of_citation_network_url_list, dont_filter=True,
                                 meta={'cookiejar':True,'quoted_paper_index' : quoted_paper_index, 
                                       'quoted_paper_title': quoted_paper_title })

    #3  通过引用某论文的首页导航链接，获取其他页导航链接（如果有）
    def access_all_web_pages_of_citation_network_url_list(self, response):
        quoted_paper_title = response.meta['quoted_paper_title']
        quoted_paper_index = response.meta['quoted_paper_index']
     
        search_resultes_items = response.xpath('//div[@class="search-results-item"]')
        for search_resultes in search_resultes_items:
                quoted_paper_index_temporary_url = search_resultes.xpath(
                    './/div[@class="search-results-content"]/div/div/a/@href').extract_first()
                quoted_paper_index_temporary_url = response.urljoin(quoted_paper_index_temporary_url)
                yield scrapy.Request(url=quoted_paper_index_temporary_url, callback=self.analysis_basic_information_of_the_quoted_paper,
                                     dont_filter=True,
                                     meta={'cookiejar':True,'quoted_paper_title': quoted_paper_title
                                           ,'quoted_paper_index' : quoted_paper_index})

    #5  通过引文链接，获取引文内容，内容同 def analysis_paper_the_number_of_quotes_possible():
    def analysis_basic_information_of_the_quoted_paper(self,response):
        help_analysis_information_of_paper =  Help_Analysis_Information_of_Paper(response)

        # -----------------------------调用解析文章元素函数，获取文章元素值--------开始---
        quoted_paper_name = response.meta['quoted_paper_title']
        quoted_paper_index = response.meta['quoted_paper_index']

        paper_title = help_analysis_information_of_paper.analysis_paper_title()
        paper_index = help_analysis_information_of_paper.analysis_paper_index(paper_title)
        paper_volume = help_analysis_information_of_paper.analysis_paper_volume()
        paper_DOI = help_analysis_information_of_paper.analysis_paper_DOI()
        paper_publication_year = help_analysis_information_of_paper.analysis_paper_publication_year()
        paper_ducument_type = help_analysis_information_of_paper.analysis_paper_ducument_type()

        Journal_Impact_factor = help_analysis_information_of_paper.analysis_Journal_Impact_factor()
        Journal_Citation_Reports_info = help_analysis_information_of_paper.analysis_papar_Journal_Citation_Reports_info()
        Journal_ISSN = help_analysis_information_of_paper.analysis_paper_Journal_ISSN()
        Journal_eISSN = help_analysis_information_of_paper.analysis_paper_Journal_eISSN()

        Funding_info = help_analysis_information_of_paper.analysis_paper_Funding_info()
        Fouding_text = help_analysis_information_of_paper.analysis_paper_Fouding_text()

        # paper_the_number_of_quotes_possible = help_analysis_information_of_paper.analysis_paper_the_number_of_quotes_possible()

        paper_authors, abstract, Author_keywords, Keywords_plus, paper_communication_author_reprint, \
        paper_communication_author_info_addresses, paper_e_mail_addresses, Publisher, \
        research_areas, web_of_science_categories, Document_Information, Other_Information = \
            help_analysis_information_of_paper.analysis_paper_block_record_many_info()

        # quoted_paper_title = help_analysis_information_of_paper.analysis_paper_title()
        # quoted_paper_index = help_analysis_information_of_paper.analysis_paper_index(quoted_paper_title)
        # #quoted_paper_group_authors = help_analysis_information_of_paper.analysis_paper_group_authors()
        # quoted_paper_publication_year = help_analysis_information_of_paper.analysis_paper_publication_year()
        # quoted_paper_the_number_of_quotes_possible = help_analysis_information_of_paper.analysis_paper_the_number_of_quotes_possible()
        # -----------------------------调用解析文章元素函数，获取文章元素值--------结束---



        # -----------------------------将元素值赋值给 items 并且传送给 pipelines---开始---
        basic_information_of_the_quoted_paper_item = Basic_information_of_the_quoted_paper_author_Item()
        basic_information_of_the_quoted_paper_item['quoted_paper_name'] = quoted_paper_name
        basic_information_of_the_quoted_paper_item['quoted_paper_index'] = quoted_paper_index

        basic_information_of_the_quoted_paper_item['paper_title'] = paper_title
        basic_information_of_the_quoted_paper_item['paper_index'] = paper_index
        basic_information_of_the_quoted_paper_item['paper_volume'] = paper_volume
        basic_information_of_the_quoted_paper_item['paper_DOI'] = paper_DOI
        basic_information_of_the_quoted_paper_item['paper_publication_year'] = paper_publication_year
        basic_information_of_the_quoted_paper_item['paper_ducument_type'] = paper_ducument_type
        basic_information_of_the_quoted_paper_item['Journal_Impact_factor'] = Journal_Impact_factor
        basic_information_of_the_quoted_paper_item['Journal_Citation_Reports_info'] = Journal_Citation_Reports_info
        basic_information_of_the_quoted_paper_item['Journal_ISSN'] = Journal_ISSN
        basic_information_of_the_quoted_paper_item['Journal_eISSN'] = Journal_eISSN
        basic_information_of_the_quoted_paper_item['Funding_info'] = Funding_info
        basic_information_of_the_quoted_paper_item['Fouding_text'] = Fouding_text
        # basic_information_of_the_quoted_paper_item['paper_the_number_of_quotes_possible'] = paper_the_number_of_quotes_possible
        basic_information_of_the_quoted_paper_item['paper_authors'] = paper_authors
        basic_information_of_the_quoted_paper_item['abstract'] = abstract
        basic_information_of_the_quoted_paper_item['Author_keywords'] = Author_keywords
        basic_information_of_the_quoted_paper_item['paper_communication_author_reprint'] = paper_communication_author_reprint
        basic_information_of_the_quoted_paper_item[
            'paper_communication_author_info_addresses'] = paper_communication_author_info_addresses
        basic_information_of_the_quoted_paper_item['paper_e_mail_addresses'] = paper_e_mail_addresses
        basic_information_of_the_quoted_paper_item['Publisher'] = Publisher
        basic_information_of_the_quoted_paper_item['research_areas'] = research_areas
        basic_information_of_the_quoted_paper_item['web_of_science_categories'] = web_of_science_categories
        basic_information_of_the_quoted_paper_item['Document_Information'] = Document_Information
        basic_information_of_the_quoted_paper_item['Other_Information'] = Other_Information
        yield basic_information_of_the_quoted_paper_item
        # -----------------------------将元素值赋值给 items 并且传送给 pipelines---结束---

