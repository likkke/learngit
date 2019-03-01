from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
import random
import pickle

from tool_case.read_input_task_files import  read_publication_names_file_xlrd,read_highly_cited_author_names_txt

from WOS_settings import display_operation_browser, path_to_chromedriver,\
    way_to_access_the_WOS_web_site, select_a_database_index, basic_search_channel_index,\
    IS_Highly_Cited_in_Field, time_span_index, time_span_start_year, time_span_end_year, \
    path_to_publication_names_xlsx_file,Web_of_Science_Categories

class WebOfKnowledge_homepage(object):
    """ 处理 http://apps.webofknowledge.com 网站的类"""
    # 根据输入基本搜索框的内容：作者名字、论文名字、出版机构等信息
    # 返回针对该搜索内容，爬虫所需要的初始化信息：Cookie、论文的 url
    def __init__(self, path_to_chromedriver="", display_operation_browser=True,
                 way_to_access_the_WOS_web_site='one',select_a_database_index=2,
                 basic_search_channel_index=7, time_span_start_year=2009, time_span_end_year=2019):
        chrome_options = Options()
        # 是否显示浏览器
        self.display_operation_browser = display_operation_browser
        if not self.display_operation_browser:
            chrome_options.add_argument("--headless")
        # 谷歌驱动器的位置
        self.path_to_chromedriver = path_to_chromedriver
        # 谷歌驱动器的对象
        self.browser = webdriver.Chrome(executable_path=(self.path_to_chromedriver), chrome_options=chrome_options)
        # 访问 wos 网站的途径
        self.way_to_access_the_WOS_web_site = way_to_access_the_WOS_web_site
        # 访问 wos 网站的数据库序号
        self.select_a_database_index = select_a_database_index
        # 访问 wos 网站的搜索通道
        self.basic_search_channel_index = basic_search_channel_index
        # 访问 wos 网站论文的时间跨度
        self.time_span_start_year = time_span_start_year
        self.time_span_end_year = time_span_end_year
        # wos 网站的 cookie
        self.wos_cookies = None
        # wos 网站的任务信息（根据任务列表产生，包含 wos_cookies）
        self.wos_task_url_info_list = None

    #获取WOS网址，通过官网网址
    def get_wos_url_by_wos_official_network(self,):
        '''直接通过官网访问'''
        self.browser.get("http://apps.webofknowledge.com")
        start_url = self.browser.current_url
        start_url_wen_index = start_url.find('?')
        new_p_start_url = start_url[:start_url_wen_index + 1] + \
                          'locale=en_US&errorKey=&viewType=input&' + start_url[start_url_wen_index + 1:]
        time.sleep(3)
        self.browser.get(new_p_start_url)
        time.sleep(3)
        start_url = self.browser.current_url
        return start_url

    #获取WOS网址，通过百度搜索
    def get_wos_url_by_baidu(self):
        self.browser.get("https://www.baidu.com/s?ie=UTF-8&wd=WOS")
        handle_index = self.browser.current_window_handle
        time.sleep(2)
        self.browser.find_element_by_xpath('//h3[@class="t"]/a').click()
        time.sleep(3)
        handles = self.browser.window_handles
        for newhandle in handles:
            if newhandle != handle_index:
                self.browser.switch_to_window(newhandle)
        start_url = self.browser.current_url
        start_url = start_url+'&locale=en_US'
        self.browser.get(start_url)
        time.sleep(5)
        start_url = self.browser.current_url
        return  start_url

    # 设置网站语言（默认英语）
    def set_website_language(self, language='English'):
        self.browser.find_element_by_xpath('//div[@class="navBar clearfix"]/ul[2]/li[3]').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//div[@class="navBar clearfix"]/ul[2]/li[3]/ul/li[3]').click()
        #print('已经设置网站语言为{}'.format(language))

    # 设置查询的数据库
    def set_database_type(self, a_database_index):
        # 更换查询的数据库
        database_index = str(a_database_index)
        self.browser.find_element_by_id('select2-databases-container').click()
        time.sleep(1)
        self.browser.find_element_by_id('select2-databases-results').\
            find_element_by_xpath('./li[{}]'.format(database_index)).click()
        time.sleep(1)
        url_0 = self.browser.current_url
        self.browser.get(url_0)

    # 设置查询通道（通过论文名字、作者名字、期刊名字...）
    def set_search_channel_index(self, search_channel_index):
        self.browser.find_element_by_id('select2-select1-container').click()
        time.sleep(1)
        self.browser.find_element_by_xpath('//span[@class="select2-search select2-search--dropdown"]/input').click()
        time.sleep(1)
        if search_channel_index not in [3, 7]:
            raise ValueError(
                "目前只支持通过作者名字、期刊名称通道搜索")
        if search_channel_index==3:
            self.browser.find_element_by_xpath('//span[@class="select2-search select2-search--dropdown"]/input').\
                send_keys('Author')
        elif search_channel_index==7:
            self.browser.find_element_by_xpath('//span[@class="select2-search select2-search--dropdown"]/input').\
                send_keys('Publication Name')
        time.sleep(1)
        self.browser.find_element_by_xpath('//span[@class="select2-search select2-search--dropdown"]/input').send_keys(Keys.ENTER)
        time.sleep(2)

    # 设置 Highly Cited in Field 过滤论文查询结果
    def set_highly_cited_field(self, is_filter=False):
        if is_filter:
            self.browser.find_element_by_id("ESITopPapers_1").click()
            time.sleep(1)
            self.browser.find_element_by_xpath('//button[@class="standard-button ghost-button refine-button button3"]').click()

    # 设置查询论文的时间间隔
    def set_time_span(self, time_span_index, start_year, end_year):
        '''暂时无法定位元素位置，改用 set_publication_year 方法'''
        if time_span_index==7:
            self.browser.find_element_by_id('timespan').find_element_by_xpath('./div[2]').click()
            time.sleep(3)

    # 设置指定论文 WOS类别
    def set_Web_of_Science_Categories(self, Web_of_Science_Categories=None):
        # 点击 Web of Science Categories 的 more options / values...
        self.browser.find_element_by_id("JCRCategories_tr").find_element_by_xpath("./div[2]/a").click()
        time.sleep(1)
        # 点击 查看 Analyze results
        self.browser.find_element_by_xpath('//a[@class="snowplow-refine-analyze-results"]').click()
        # 解析表格内容 TODO：目前没有翻页，因为默认显示100个类别，同一个作者几乎不可能涵盖那么多类别，所以涵盖了所有种类数据
        time.sleep(3)
        trs_list = self.browser.find_elements_by_xpath('//table[@class="RA-NEWresultsSectionTable"]//tr')
        click_target_category_times = 0
        for tr in trs_list[1:]:  # 排除0号表头
            tr_html_content = str(tr.get_attribute('textContent'))
            for a_category in Web_of_Science_Categories:
                if a_category in tr_html_content:
                    # print(tr_html_content)
                    tr.find_element_by_xpath('./td[1]/input').click()
                    click_target_category_times +=1
        if click_target_category_times==0:
            # 该作者指定领域的论文数量为零，则只更新 cookies
            self.wos_cookies = self.browser.get_cookies()
            self.wos_task_url_info_list = {'wos_cookies': self.wos_cookies, 'task_url_info_list':[]}
        # 点击查看选择的结果
        self.browser.find_element_by_xpath('//div[@class="d-flex justify-content-start"]/div[2]/button').click()
        return click_target_category_times

    # 设置指定年份
    def set_publication_years(self, start_year, end_year):
        #生成指定年份的集合{2018, 2017, 2016...2008}
        def product_legitimate_years_set(start_year, end_year):
            return set(range(start_year, end_year+1))
        legitimate_years_set = product_legitimate_years_set(start_year, end_year)

        # 按 batch_size 取 a_list 中元素
        def get_batch_size_sample(a_list, batch_size):
            for i in range(0, len(a_list), batch_size):
                yield a_list[i:min(len(a_list), i + batch_size)]

        # 先取消勾选 Highly Cited in Field 勾选框
        #self.browser.find_element_by_xpath('//div[@class="refine-item refine-item-open FilterButton"]/button').click()
        self.browser.find_element_by_id('PublicationYear').find_element_by_xpath('./div/div[2]/a').click()
        tr_items = self.browser.find_element_by_id('PublicationYear_raMore_tr').find_elements_by_xpath('.//tr')

        checked_years_numbers = 0
        # 按先读取列在读取行的顺序处理 publication years
        for publication_years_column_number in range(0, 4):
            for tr_item in tr_items:
                td_items = tr_item.find_elements_by_xpath('.//td')
                td_3_items_list = list(get_batch_size_sample(td_items, batch_size=3))
                last_row = 0
                try:
                    td_3_item = td_3_items_list[publication_years_column_number]
                except:
                    last_row = 1
                if last_row == 0:
                    contain_brackets = td_3_item[1].text
                    # 只处理合法年份
                    if "(" in contain_brackets or ")" in contain_brackets:
                        td_item_year = int(td_3_item[1].find_element_by_xpath('./label').text[:4])
                        # 只处理处于指定区间的年份
                        if td_item_year in legitimate_years_set:
                            td_3_item[0].find_element_by_xpath('./input').click()
                            checked_years_numbers = checked_years_numbers + 1
                            time.sleep(0.2)
        # Publication Years Refine
        self.browser.find_element_by_id('raMore').find_element_by_xpath(
            './table/tbody/tr/td/table/tbody/tr/td[2]/div/button').click()

    # 获取论文查询结果列表第一页第一篇论文的 url
    def get_first_page_first_page_url(self):
        page_url_first = self.browser.current_url
        self.browser.find_element_by_xpath('//div[@class="search-results-content"]/div/div/a').click()
        time.sleep(1)
        First_Paper_URL = self.browser.current_url
        #self.browser.get(page_url_first)
        return First_Paper_URL

    # 获取论文查询结果列表最后一页论文的个数
    def get_last_paper_info(self):
        # 获取最后一页页码数目
        last_page_num_index = self.browser.find_element_by_id('pageCount.top').text
        last_page_num_index = self._get_int_from_str(last_page_num_index)
        self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').clear()
        time.sleep(1)
        self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(last_page_num_index)
        time.sleep(1)
        self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(Keys.ENTER)
        last_paper_numbers = len(self.browser.find_elements_by_xpath('//div[@class="search-results-content"]/div/div/a'))
        return last_page_num_index, last_paper_numbers


    # 根据 WOS_setting 的设置解析 http://apps.webofknowledge.com 首页，
    # 获取爬虫的初始 url 种子和 cookies
    def parse_WOS_home_page_options(self, task_list):
        # 设置进入 WOS 网站途径
        if self.way_to_access_the_WOS_web_site == 'two':
            start_url = self.get_wos_url_by_wos_official_network()
        else:
            start_url = self.get_wos_url_by_baidu()
        # 设置网站语言
        self.set_website_language()
        # 选择一个数据库
        self.set_database_type(self.select_a_database_index)
        # 选择基本搜索途径
        self.set_search_channel_index(self.basic_search_channel_index)
        # 设置搜索时间跨度（暂时用其他方法解决）
        #set_time_span(browser, time_span_index,time_span_start_year, time_span_end_year)

        #if basic_search_channel_index==7:
            # 获取出版物名单列表
        #    publication_names_list = read_publication_names_file_xlrd(path_to_publication_names_xlsx_file)

        # 用来装载任务相关信息传递给爬虫的列表
        task_url_info_list = []
        for task_name in task_list:
            # 删除上一次输入 任务名
            self.browser.find_element_by_id('clearIcon1').click()
            time.sleep(1)
            # 输入本次 任务名
            self.browser.find_element_by_xpath('//input[@aria-role="textbox"]').send_keys(task_name)
            time.sleep(1)
            self.browser.find_element_by_xpath('//input[@aria-role="textbox"]').send_keys(Keys.ENTER)
            time.sleep(1)
            # 设置年份
            if basic_search_channel_index==7: #如果任务索引是出版商，需要设置年份才执行
                # 设置 Publication Years
                self.set_publication_years(self.time_span_start_year, self.time_span_end_year)
            # 勾选 Highly_Cited_in_Field
            if IS_Highly_Cited_in_Field or basic_search_channel_index==3:
                #当任务是高引作者名或者设置IS_Highly_Cited_in_Field 时执行
                # 勾选 highly_cited_field
                self.set_highly_cited_field(is_filter=True)
            # 设置 Web of Science Categories
            if Web_of_Science_Categories is not None:
                click_target_category_times = self.set_Web_of_Science_Categories(Web_of_Science_Categories)
                if click_target_category_times==0:
                    #该作者指定领域的论文数量为零
                    wos_task_name_cookie_info_dict = {'wos_cookies': self.browser.get_cookies(), 'task_url_info_list':[]}
                    # TODO:这里目前用 return 和 quit 是因为每次只处理了一个任务，若一次同时处理则要改为continue 后续逻辑也要改变
                    self.browser.quit()
                    return wos_task_name_cookie_info_dict
                #因为执行set_Web_of_Science_Categories操作会使当前url错误所以通过下面方法重置回正确url
                self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').clear()
                time.sleep(1)
                self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(1)
                time.sleep(1)
                self.browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(Keys.ENTER)

            # 经过各种设置之后的当前的url_CFDD
            after_allkindsof_set = self.browser.current_url
            #获取第一页中第一个论文的URL
            First_Paper_URL = self.get_first_page_first_page_url()
            #回到经过各种设置之后的url_CFDD
            self.browser.get(after_allkindsof_set)
            time.sleep(3)
            # 获取最后一页序号和最后一页论文个数
            last_page_num_index, last_paper_numbers = self.get_last_paper_info()
            task_url_info_list.append((task_name, First_Paper_URL, last_page_num_index, last_paper_numbers))
            # 回到任务输入界面
            self.browser.get(start_url)
            cookies = self.browser.get_cookies()
            wos_task_name_cookie_info_dict = {'wos_cookies': cookies, 'task_url_info_list':task_url_info_list}
            self.browser.quit()
            # 保存分析 wos 所得的信息
            self.wos_cookies = cookies
            self.wos_task_url_info_list = wos_task_name_cookie_info_dict

            return wos_task_name_cookie_info_dict

    # 把 webofknowledge_homepage 解析的数据存入 pickle 文件
    def store_wos_task_info_to_pickle_file(self, task_list):
        wos_task_name_cookie_info_dict = self.parse_WOS_home_page_options(task_list)
        #print(wos_task_name_cookie_info_dict['wos_cookies'])
        #print(wos_task_name_cookie_info_dict['task_url_info_list'])
        cookies = wos_task_name_cookie_info_dict['wos_cookies']
        task_url_info_list = wos_task_name_cookie_info_dict['task_url_info_list']
        pickle.dump(cookies, open("temporary_documents/cookies.pickle", "wb"))
        with open('temporary_documents/task_url_info_list.pickle','wb') as f:
            pickle.dump(task_url_info_list, f)

    # 从字符串中获取整数
    def _get_int_from_str(self, a_str):
        p = ''
        for a in a_str:
            if a in ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']:
                p += a
        return int(p)



if __name__=="__main__":
    #publication_names_list  =  read_publication_names_file_xlrd(path_to_publication_names_xlsx_file)
    publication_names_list = ['IEEE WIRELESS COMMUNICATIONS LETTERS', 'PEDIATRICS', 'BIRTH DEFECTS RESEARCH']
    author_names_list = read_highly_cited_author_names_txt("E:\web_of_science\input_task_file\高引学者.txt")

    task_list = [random.choice(author_names_list)]

    wos_homepage = WebOfKnowledge_homepage(path_to_chromedriver=path_to_chromedriver,
                                           display_operation_browser=display_operation_browser,
                                           way_to_access_the_WOS_web_site=way_to_access_the_WOS_web_site,
                                           select_a_database_index=select_a_database_index,
                                           basic_search_channel_index=basic_search_channel_index,
                                           time_span_start_year=time_span_start_year,
                                           time_span_end_year=time_span_end_year)

    wos_homepage.store_wos_task_info_to_pickle_file(task_list)
    print(wos_homepage.wos_cookies)
    print(wos_homepage.wos_task_url_info_list)


"""
测试输出：
{
'wos_cookies': [{'domain': '.webofknowledge.com', 'expiry': 1605777658, 'httpOnly': False, 'name': '_sp_id.630e', 'path': '/', 'secure': False, 'value': '5561d220-f194-4193-a3e8-b9deb68d7b2d.1542705613.1.1542705658.1542705613.e5a847ab-6407-4a17-9935-fd00e54522fd'}, {'domain': '.webofknowledge.com', 'httpOnly': True, 'name': 'SID', 'path': '/', 'secure': False, 'value': '"5Bi8w1kfpXb8UVFLB8D"'},
 {'domain': '.webofknowledge.com', 'httpOnly': False, 'name': 'dotmatics.elementalKey', 'path': '/', 'secure': False, 'value': 'SLsLWlMhrHnTjDerSrlG'}, 
{'domain': '.webofknowledge.com', 'expiry': 1542712807.13399, 'httpOnly': True, 'name': 'ak_bmsc', 'path': '/', 'secure': False, 'value': 'B4892EACAFA40DBEEFBD96D16BF37814CB6A55E9B73B0000C6D1F35B43931E53~plzLPy9JUP4ZWKsnl3sKJykNVnerkNUeLAnfM2il98ut/BnsxCi2rdrQOH7TG6CbAfsCdsRrgQm+zzD19GPwDQ6FMQa45rq50907jNhDBjlTvaITQRmE6AZcnd6SUDl8bzQFNhZfQai9WvggdtSGW7Us4ulvOoKueX3EJcgriygY6ErYBm6SnxI31u7gl7fI6w30hX5/6b0Jir2qzdZSO8Iqozs4Er1MFRTLV93OugcGrZtS02PXhdYeLJdRhMimza'}, 
{'domain': '.webofknowledge.com', 'httpOnly': True, 'name': 'CUSTOMER', 'path': '/', 'secure': False, 'value': '"Sichuan University"'}, 
{'domain': '.webofknowledge.com', 'httpOnly': True, 'name': 'E_GROUP_NAME', 'path': '/', 'secure': False, 'value': '"Sichuan University"'}, 
{'domain': '.webofknowledge.com', 'expiry': 1542720006.690896, 'httpOnly': True, 'name': 'bm_sz', 'path': '/', 'secure': False, 'value': 'BBB97F6F5116FD2EB05267D3DC4DAEB8~QAAQ6VVqywmkY+RmAQAAZW1rMJHuZ5nzBPKXr4ZBNmVGlFla4P4T91n0wXerorCbGUR/fjhfnGEFaN1rBXwokbph5QBJl7bhz9IEbkse5xc7hQPdtDsJa3DKINhOpNECf7F3DAB7jvqZ45sujAGsMDSuw/eO+0BAqNArnkVQAo7zBIM4movY57rf8CO26YAUxHYwORaxXQ=='}, 
{'domain': '.webofknowledge.com', 'expiry': 1574241613.28121, 'httpOnly': False, 'name': '_abck', 'path': '/', 'secure': False, 'value': '551CDB5417D1419E6A17384E7B8AD103CB6A55E9B73B0000C5D1F35BF3FE5D3A~0~pGmiadxi1nDRd64KuDXucMbRJcF6urDXqICbh98wH5c=~-1~-1'}, {
'domain': '.webofknowledge.com', 'expiry': 1542707458, 'httpOnly': False, 'name': '_sp_ses.630e', 'path': '/', 'secure': False, 'value': '*'}, 
{'domain': 'apps.webofknowledge.com', 'httpOnly': True, 'name': 'JSESSIONID', 'path': '/', 'secure': False, 'value': 'C4B6D551D80DF789589131BC8CD6B954'}, 
{'domain': '.webofknowledge.com', 'expiry': 1542712807.567543, 'httpOnly': True, 'name': 'bm_sv', 'path': '/', 'secure': False, 'value': 'A1E764A5BBF1B21B053300E2609C4F21~73UwV72DdZl54WOe7oQZM7SrI92QWq5OTus3wjaGy3nzdP1FxK43rqzzjRe7kuq1CsccGZxdSTLb+Q2zzD6lGQqVwf36u/7K0hocXZ8Pp1cOtSEQCuhW/ENn/xCf5XfG5zubzf4toS96Wi59YOD/LyfzUBb+OUTzz/83+gfr9TQ='}], 
'task_url_info_list': [('IEEE WIRELESS COMMUNICATIONS LETTERS', 'http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=2&SID=5Bi8w1kfpXb8UVFLB8D&page=1&doc=1', 128, 1)]}
"""