import scrapy
from dependency_function import delete_multiple_spaces_and_leave_a,\
    find_special_markup_and_delete_it
start_url = "http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=2&SID=7CRmoCdRvNgUdMmmtTG&page=820&doc=8199"
start_url = "http://apps.webofknowledge.com/full_record.do?product=WOS&search_mode=GeneralSearch&qid=2&SID=5Bi8w1kfpXb8UVFLB8D&page=92&doc=912"
class JUST_A_PAGE_TEST_Spider(scrapy.Spider):
    name = 'a_page_test_spider'
    start_urls = [start_url]

    "作者、摘要、关键词、作者信息（通讯作者地址、作者地址、Email）、资助、"
    def parse(self, response):
        print("一页测试爬虫测试开始...")

        def analysis_paper_block_record_many_info():
            Funding_info = []
            Fouding_table_titles = response.xpath('//div[@class="title3"]')
            for title in Fouding_table_titles:
                Fouding_table_title_str = title.xpath('string(.)').extract_first()
                if 'Funding' in Fouding_table_title_str:
                    print("yes")
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
                    Fouding_text = response.xpath('//span[@id="show_fund_blurb"]/p/text()').extract_first()
                    print(Funding_info)
                    print(Fouding_text)
        analysis_paper_block_record_many_info()