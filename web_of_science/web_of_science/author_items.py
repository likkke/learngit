# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field

class WebOfScienceItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class Author_Item(scrapy.Item):
    # 作者 索引号
    author_index = Field()
    # 作者 名称
    author_name = Field()


class Basic_information_of_the_paper_author_Item(scrapy.Item):
    #----------------其他辅助信息-------------------开始----------
    # 高引用论文 文章位置（仅仅作为标记使用）
    page_doc_tuple = Field()
    # 高引用论文 可能的引用数目
    paper_the_number_of_quotes_possible = Field()
    # ----------------其他辅助信息-------------------结束----------

    #-----------------正文内容-----------------------开始----------
    # 高引用论文 标题
    paper_title = Field()
    # 高引用论文 索引号
    paper_index = Field()
    # 高引用论文 作者
    paper_authors = Field()
    # 团体作者名称
    #paper_group_authors = Field()

    # 高引用论文 Volume
    paper_volume = Field()
    # 高引用论文 DOI
    paper_DOI = Field()
    # 高引用论文 出版年
    paper_publication_year = Field()
    # 高引用论文 文献类型
    paper_ducument_type = Field()
    # 高引论文 可能的引文数量 --新加
    paper_the_number_of_quotes_possible = Field()



    # 期刊 索引号
    journal_index = Field()
    # 期刊 名称
    journal_name = Field()

    # ------查看期刊影响力内容-------开始------
    # 期刊 影响因子
    Journal_Impact_factor = Field()
    # Journal_Citation_Reports_info 包含 JCR@ Category、Rank in Category、Quartile in Category 三项信息
    Journal_Citation_Reports_info = Field()
    # 期刊 ISSN
    Journal_ISSN = Field()
    # 期刊 eISSN
    Journal_eISSN = Field()
    # 期刊 研究领域
    Journal_Research_Domain = Field() #没有
    # ------查看期刊影响力内容-------结束------

    # 高引用论文 摘要
    abstract = Field()

    # 高引用论文 关键词
    # 高引用论文 作者关键词
    Author_keywords = Field()
    # 高引用论文 增强关键词
    Keywords_plus = Field()

    # 高引用论文 作者信息
    # 高引用论文 通讯作者地址
    paper_communication_author_reprint = Field()
    # 高引用论文 地址
    paper_communication_author_info_addresses = Field()
    # 高引用论文 电子邮件地址
    paper_e_mail_addresses = Field()

    # 基金资助致谢，
    # 基金资助机构和授权号两项信息
    Funding_info = Field()
    # 基金文字描述信息 fouding text
    Fouding_text = Field()

    # 出版商
    Publisher = Field()

    # 类别/分类
    # 研究方向
    research_areas = Field()
    # Web of Science 类别
    web_of_science_categories = Field()

    # 文档信息
    Document_Information = Field()

    # 其他信息
    Other_Information = Field()
    # -----------------正文内容-----------------------结束----------


class Basic_information_of_the_quoted_paper_author_Item(scrapy.Item):
    #----------------其他辅助信息-------------------开始----------
    # 期刊 索引号 应为被引论文的title
    quoted_paper_index = Field()
    # 期刊 名称 应为被引论文的title_index
    quoted_paper_name = Field()
    # ----------------其他辅助信息-------------------结束----------

    #-----------------正文内容-----------------------开始----------
    # 标题
    paper_title = Field()
    # 索引号
    paper_index = Field()
    # 作者
    paper_authors = Field()
    # 团体作者名称
    #paper_group_authors = Field()

    # Volume
    paper_volume = Field()
    # DOI
    paper_DOI = Field()
    # 出版年
    paper_publication_year = Field()
    # 文献类型
    paper_ducument_type = Field()


    # ------查看期刊影响力内容-------开始------
    # 期刊 影响因子
    Journal_Impact_factor = Field()
    # Journal_Citation_Reports_info 包含 JCR@ Category、Rank in Category、Quartile in Category 三项信息
    Journal_Citation_Reports_info = Field()
    # 期刊 出版商 （已经知道）
    #Journal_Publisher = Field()
    # 期刊 ISSN
    Journal_ISSN = Field()
    # 期刊 eISSN
    Journal_eISSN = Field()
    # 期刊 研究领域 （与 research_areas 内容一致）
    #Journal_Research_Domain = Field()
    # ------查看期刊影响力内容-------结束------

    # 摘要
    abstract = Field()

    # 关键词
    # 作者关键词
    Author_keywords = Field()
    # 增强关键词
    Keywords_plus = Field()

    # 作者信息
    # 通讯作者地址
    paper_communication_author_reprint = Field()
    # 地址
    paper_communication_author_info_addresses = Field()
    # 电子邮件地址
    paper_e_mail_addresses = Field()

    # 基金资助致谢，
    # 基金资助机构和授权号两项信息
    Funding_info = Field()
    # 基金文字描述信息 fouding text
    Fouding_text = Field()

    # 出版商
    Publisher = Field()

    # 类别/分类
    # 研究方向
    research_areas = Field()
    # Web of Science 类别
    web_of_science_categories = Field()

    # 文档信息
    Document_Information = Field()

    # 其他信息
    Other_Information = Field()
    # -----------------正文内容-----------------------结束----------