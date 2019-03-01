import hashlib
import re
# md5 哈希类
class MD5_ID(object):
    def __init__(self):
        self.hash_md5 = hashlib.md5()
    def create_uid(self,a_str):
        if a_str:
            hash_md5 = self.hash_md5
            hash_md5.update((a_str + 'wangzichao').encode(encoding='utf-8'))
            return hash_md5.hexdigest()
        return -1

# 在字符串中找到特殊标记符号位置，并且删除它
def find_special_markup_and_delete_it(a_str, special_markup):
    return a_str[a_str.index(special_markup)+len(special_markup):]


#获取字符串中的最后两个数字
def find_last_two_numbers(a_string):
    it = re.finditer(r"\d+",a_string)
    it_list = [int(x.group()) for x in it]
    it_list = it_list[-2:]
    it_tuple = tuple(it_list)
    return it_tuple

# 合并多个空格为一个
def delete_multiple_spaces_and_leave_a(a_str):
    return ' '.join(a_str.split()).strip()

# 从字符串中获取整数
def get_int_from_str(a_str):
    '''
    :param a_str: '1s2d3,56'
    :return: int: 12356
    '''
    p = ''
    a_str = str(a_str)
    for a in a_str:
        if a in ['0','1','2','3','4','5','6','7','8','9']:
            p+=a
    return int(p)

# 获取列表首元素，并且删除它，代替先进先出队列使用
def get_first_and_del_first_item_from_list(a_list):
    if len(a_list)>=1:
        first_item = a_list[0]
        a_list.remove(first_item)
        return first_item
    else:
        return None

# 根据 webofknowledge_homepage_Class.py 解析的数据产生爬虫的初始化任务 URL 列表
def generate_initial_task_URL_list(First_Paper_URL, last_page_num_index, last_paper_numbers):
    First_Paper_URL_demo = str(First_Paper_URL).replace('page=1&doc=1', 'page={}&doc={}')
    UURL_LIST = []
    if last_page_num_index == 1:
        for i in range(1, last_paper_numbers + 1):
            famous_paper_url = First_Paper_URL_demo.format(1, i)
            UURL_LIST.append(famous_paper_url)
    else:
        for j in range(1, last_page_num_index):
            for k in range(1, 11):
                doc = (j - 1) * 10 + k
                famous_paper_url = First_Paper_URL_demo.format(j, doc)
                UURL_LIST.append(famous_paper_url)
        for k in range(1, last_paper_numbers + 1):
            doc = (last_page_num_index - 1) * 10 + k
            famous_paper_url = First_Paper_URL_demo.format(last_page_num_index, doc)
            UURL_LIST.append(famous_paper_url)
    return UURL_LIST

class Help_Analysis_Information_of_Paper(object):

    def __init__(self, response):
        self.response = response
        self.md5_id = MD5_ID()

    #---------------------解析文章元素信息的函数范例------------------------
    # 解析 论文 some_info
    def analysis_paper_some_info(self,):
        # 解析部分
        some_info = ''
        # .....
        # 如果 some_info 成功解析，直接返回该值
        if True:
            return some_info
        # 如果 some_info 解析失败，返回 None
        else:
            return None
    #-------------------------------------------------------------------------

    # -----------------------------解析文章元素信息的函数-------------------开始------
    # 解析 论文标题
    def analysis_paper_title(self,):
        paper_title_value = self.response.xpath('//div[@class="title"]/value')
        paper_title = paper_title_value.xpath('string(.)').extract_first()
        if paper_title:
            return paper_title.strip()
        return None

    # 解析 论文标题索引号
    def analysis_paper_index(self, paper_title):
        return self.md5_id.create_uid(paper_title)
    #解析 论文杂志

    def analysis_paper_quote_journal(self):
        paper_quote_journal = self.response.xpath('//span[@class = "sourceTitle" ]/value/text()').extract_first()
        return paper_quote_journal
    # 解析 论文出版年
    def analysis_paper_publication_year(self,):
        nFR_fields = self.response.xpath('//div[@class="block-record-info block-record-info-source"]/p[@class="FR_field"]')
        for FR_field in nFR_fields:
            FR_field_str = FR_field.xpath('string(.)').extract_first()
            if 'Published' in FR_field_str:
                # print(FR_field_str)
                paper_publication_year = str(FR_field_str).replace('Published:', '').strip()
                return paper_publication_year
        return None

    # 解析 论文Volume
    def analysis_paper_volume(self,):
        FR_fields = self.response.xpath(
            '//div[@class="block-record-info block-record-info-source"]/div[@class="block-record-info-source-values"]')
        if FR_fields is not None:
            FR_field_str = FR_fields.xpath('string(.)').extract_first()
            paper_volume = str(FR_field_str).replace('Volume:', '').strip()
            paper_volume = delete_multiple_spaces_and_leave_a(paper_volume)
            return paper_volume
        return None

    # 解析 论文DOI
    def analysis_paper_DOI(self,):
        nFR_fields = self.response.xpath('//div[@class="block-record-info block-record-info-source"]/p[@class="FR_field"]')
        for FR_field in nFR_fields:
            FR_field_str = FR_field.xpath('string(.)').extract_first()
            if 'DOI' in FR_field_str:
                paper_DOI = str(FR_field_str).replace('DOI:', '').strip()
                return paper_DOI
        return None

    # 解析 论文文档类型
    def analysis_paper_ducument_type(self,):
        nFR_fields = self.response.xpath(
            '//div[@class="block-record-info block-record-info-source"]/p[@class="FR_field"]')
        for FR_field in nFR_fields:
            FR_field_str = FR_field.xpath('string(.)').extract_first()
            if 'Document Type' in FR_field_str:
                paper_ducument_type = str(FR_field_str).replace('Document Type:', '').strip()
                return paper_ducument_type
        return None

    # 解析 论文影响因子
    def analysis_Journal_Impact_factor(self,):
        # flag = True
        # try:
        #     Impact_factor_table_trs = self.response.xpath('//table[@class="Impact_Factor_table"]/tr')
        # except:
        #     flag = False
        #     raise ValueError("解析 论文影响因子 失败！")
        # if flag:
        #     Impact_factor_table_tr_td = Impact_factor_table_trs[0].xpath('./td/text()').extract()
        #     Impact_factor_table_tr_td = [str(tr_td).replace(' ', '') for tr_td in Impact_factor_table_tr_td]
        #     Impact_factor_table_tr_th = Impact_factor_table_trs[1].xpath('./th/text()').extract()
        #     Impact_factor_table_tr_th = [str(th).replace(' ', '') for th in Impact_factor_table_tr_th]
        #     Journal_Impact_factor = list(zip(Impact_factor_table_tr_th, Impact_factor_table_tr_td))
        #     return Journal_Impact_factor
        # return None
        ##################修改 11.22
        Impact_factor_table_trs = self.response.xpath('//table[@class="Impact_Factor_table"]/tr')
        if  Impact_factor_table_trs:
            Impact_factor_table_tr_td = Impact_factor_table_trs[0].xpath('./td/text()').extract()
            Impact_factor_table_tr_td = [str(tr_td).replace(' ', '') for tr_td in Impact_factor_table_tr_td]
            Impact_factor_table_tr_th = Impact_factor_table_trs[1].xpath('./th/text()').extract()
            Impact_factor_table_tr_th = [str(th).replace(' ', '') for th in Impact_factor_table_tr_th]
            Journal_Impact_factor = list(zip(Impact_factor_table_tr_th, Impact_factor_table_tr_td))
            return Journal_Impact_factor
        return None
    #############完




    # 解析 论文Journal_Citation_Reports_info 表格信息
    def analysis_papar_Journal_Citation_Reports_info(self,):
        Journal_Citation_Reports_info = []
        # flag = True
        # try:
        #     JCR_table_trs = self.response.xpath('//table[@class="JCR_Category_table"]/tr')
        # except:
        #     flag = False
        #     raise ValueError("解析 论文Journal_Citation_Reports_info 表格信息失败！")
        # if flag:
        #     # 略过表头[1:]
        #     for tr in JCR_table_trs[1:]:
        #         td1 = tr.xpath('./td[1]/text()').extract_first()
        #         td2 = tr.xpath('./td[2]/text()').extract_first()
        #         td3 = tr.xpath('./td[3]/text()').extract_first()
        #         td_list = []
        #         for td in [td1, td2, td3]:
        #             if td is not None:
        #                 td = str(td).strip()
        #                 td_list.append(td)
        #         Journal_Citation_Reports_info.append(td_list)
        #     if len(Journal_Citation_Reports_info)>0:
        #         return Journal_Citation_Reports_info
        # return None
        JCR_table_trs = self.response.xpath('//table[@class="JCR_Category_table"]/tr')
        if JCR_table_trs:
            # 略过表头[1:]
            for tr in JCR_table_trs[1:]:
                td1 = tr.xpath('./td[1]/text()').extract_first()
                td2 = tr.xpath('./td[2]/text()').extract_first()
                td3 = tr.xpath('./td[3]/text()').extract_first()
                td_list = []
                for td in [td1, td2, td3]:
                    if td is not None:
                        td = str(td).strip()
                        td_list.append(td)
                Journal_Citation_Reports_info.append(td_list)
            if len(Journal_Citation_Reports_info)>0:
                return Journal_Citation_Reports_info
        return None


    # 解析 论文 ISSN
    def analysis_paper_Journal_ISSN(self,):
        ISSN = self.response.xpath('//p[@class="FR_field sameLine"]/value[1]/text()').extract_first()
        if ISSN is not None:
            return ISSN
        return None

    # 解析 论文 eISSN
    def analysis_paper_Journal_eISSN(self,):
        eISSN = self.response.xpath('//p[@class="FR_field sameLine"]/value[2]/text()').extract_first()
        if eISSN is not None:
            return eISSN
        return None

    # 解析 论文可能的引用数目
    def analysis_paper_the_number_of_quotes_possible(self,):
        paper_the_number_of_quotes_possible = self.response.xpath(
            '//div[@class="flex-row flex-justify-start flex-align-start box-div"]/div/a/span/text()').extract_first()
        if paper_the_number_of_quotes_possible is None:
            return None
        else:
            paper_the_number_of_quotes_possible = get_int_from_str(paper_the_number_of_quotes_possible)
            return paper_the_number_of_quotes_possible

    # 解析 论文基金文字描述信息 fouding text
    def analysis_paper_Fouding_text(self):
        Fouding_text = self.response.xpath('//span[@id="show_fund_blurb"]/p/text()').extract_first()
        if Fouding_text is not None:
            return Fouding_text
        return None

    # 解析 论文基金资助机构和授权号两项信息
    def analysis_paper_Funding_info(self):
        Funding_info = []
        Fouding_table_titles = self.response.xpath('//div[@class="title3"]')
        for title in Fouding_table_titles:
            Fouding_table_title_str = title.xpath('string(.)').extract_first()
            if 'Funding' in Fouding_table_title_str:

                Fouding_table_trs = title.xpath('../table//tr')
                # l略过表头
                Grant_Number = ''
                for tr in Fouding_table_trs[1:]:
                    Funding_Agency = tr.xpath('./td[1]/text()').extract_first()
                    Funding_Agency = str(Funding_Agency).replace('\xa0', '')
                    Grant_Numbers = tr.xpath('./td[2]/div/text()').extract()
                    if len(Grant_Numbers) > 1:
                        for G in Grant_Numbers:
                            Grant_Number += str(G).replace('\xa0', '') + '|'
                        Grant_Number = Grant_Number[:-1]
                    else:
                        Grant_Number = tr.xpath('./td[2]/div/text()').extract_first()
                        if Grant_Number == None:
                            Grant_Number = ''
                        else:
                            Grant_Number = str(Grant_Number).replace('\xa0', '')
                    Funding_info.append([Funding_Agency, Grant_Number])
        if len(Funding_info)==0:
            return None
        return Funding_info

    def analysis_paper_block_record_many_info(self, ):
        """ 12 种信息
        paper_authors, abstract, Author_keywords, Keywords_plus, paper_communication_author_reprint, \
        paper_communication_author_info_addresses, paper_e_mail_addresses, Publisher, \
        research_areas, web_of_science_categories, Document_Information, Other_Information
        """
        paper_authors, abstract, Author_keywords, Keywords_plus, paper_communication_author_reprint, \
        paper_communication_author_info_addresses, paper_e_mail_addresses, Publisher, \
        research_areas, web_of_science_categories, Document_Information, Other_Information = \
        None, None, None, None, None,\
        None, None, None, \
        None, None, None, None

        block_record_many_info = self.response.xpath('//div[@class="block-record-info"]')
        for FR_fields in block_record_many_info:
            FR_fields_str = FR_fields.xpath('string(.)').extract_first()
            # paper_authors
            if "By:" in FR_fields_str:
                paper_authors = find_special_markup_and_delete_it(FR_fields_str, "By:")
                paper_authors = delete_multiple_spaces_and_leave_a(paper_authors)
            # abstract
            if "Abstract" in FR_fields_str:
                abstract = find_special_markup_and_delete_it(FR_fields_str, 'Abstract')
                abstract = delete_multiple_spaces_and_leave_a(abstract)
            if "Keywords" in FR_fields_str:
                Keywords_plus_index = None
                # Keywords_plus
                if "KeyWords Plus:" in FR_fields_str:
                    Keywords_plus_index = FR_fields_str.index("KeyWords Plus:")
                    Keywords_plus = find_special_markup_and_delete_it(FR_fields_str, 'KeyWords Plus:')
                    Keywords_plus = delete_multiple_spaces_and_leave_a(Keywords_plus)
                if Keywords_plus_index is not None:
                    FR_fields_str = FR_fields_str[:Keywords_plus_index]
                # Author_keywords
                if "Author Keywords:" in FR_fields_str:
                    Author_keywords = find_special_markup_and_delete_it(FR_fields_str, 'Author Keywords:')
                    Author_keywords = delete_multiple_spaces_and_leave_a(Author_keywords)
            if "Author Information" in FR_fields_str:
                paper_e_mail_addresses_index = None
                paper_communication_author_info_addresses_index = None
                # paper_e_mail_addresses
                if "E-mail Addresses:" in FR_fields_str:
                    paper_e_mail_addresses_index = FR_fields_str.index("E-mail Addresses:")
                    paper_e_mail_addresses = find_special_markup_and_delete_it(FR_fields_str, "E-mail Addresses:")
                    paper_e_mail_addresses = delete_multiple_spaces_and_leave_a(paper_e_mail_addresses)

                if paper_e_mail_addresses_index is not None:
                    FR_fields_str = FR_fields_str[:paper_e_mail_addresses_index]
                # paper_communication_author_info_addresses
                if "Addresses:" in FR_fields_str:
                    paper_communication_author_info_addresses_index = FR_fields_str.index("Addresses:")
                    paper_communication_author_info_addresses = find_special_markup_and_delete_it(
                                                                                     FR_fields_str, "Addresses:")
                    paper_communication_author_info_addresses = delete_multiple_spaces_and_leave_a(
                                                                        paper_communication_author_info_addresses)

                if paper_communication_author_info_addresses_index is not None:
                    FR_fields_str = FR_fields_str[:paper_communication_author_info_addresses_index]
                # paper_communication_author_reprint
                if "Reprint Address:" in FR_fields_str:
                    paper_communication_author_reprint = find_special_markup_and_delete_it(FR_fields_str,
                                                                                           "Reprint Address:")
                    paper_communication_author_reprint = delete_multiple_spaces_and_leave_a(
                                                                                paper_communication_author_reprint)
            # Publisher
            if "Publisher" in FR_fields_str:
                Publisher = find_special_markup_and_delete_it(FR_fields_str, "Publisher")
                Publisher = delete_multiple_spaces_and_leave_a(Publisher)
            if "Categories / Classification" in FR_fields_str:
                web_of_science_categories_index = None
                # web_of_science_categories
                if "Web of Science Categories:" in FR_fields_str:
                    web_of_science_categories_index = FR_fields_str.index("Web of Science Categories:")
                    web_of_science_categories = find_special_markup_and_delete_it(FR_fields_str, "Web of Science Categories:")
                    web_of_science_categories = delete_multiple_spaces_and_leave_a(web_of_science_categories)
                if web_of_science_categories_index is not None:
                    FR_fields_str = FR_fields_str[:web_of_science_categories_index]
                # research_areas
                if "Research Areas:" in FR_fields_str:
                    research_areas = find_special_markup_and_delete_it(FR_fields_str, "Research Areas:")
                    research_areas = delete_multiple_spaces_and_leave_a(research_areas)
            # Document_Information
            if "Document Information" in FR_fields_str:
                Document_Information = find_special_markup_and_delete_it(FR_fields_str, "Document Information")
                Document_Information = delete_multiple_spaces_and_leave_a(Document_Information)
            # Other_Information
            if "Other Information" in FR_fields_str:
                Other_Information = find_special_markup_and_delete_it(FR_fields_str, "Other Information")
                Other_Information = delete_multiple_spaces_and_leave_a(Other_Information)
        return (paper_authors, abstract, Author_keywords, Keywords_plus, paper_communication_author_reprint, \
        paper_communication_author_info_addresses, paper_e_mail_addresses, Publisher, \
        research_areas, web_of_science_categories, Document_Information, Other_Information )

    # -----------------------------解析文章元素信息的函数-------------------结束------
