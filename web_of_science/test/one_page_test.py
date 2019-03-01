path_to_chromedriver = r'C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe'
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
url3 = "http://apps.webofknowledge.com/RAMore.do?product=WOS&search_mode=GeneralSearch&SID=6FjJ1xgjRbuHVldMg1W&qid=1&ra_mode=more&ra_name=PublicationYear&colName=WOS&viewType=raMore"
url2 = "http://apps.webofknowledge.com/RAMore.do?product=WOS&search_mode=GeneralSearch&SID=6DDB4HTXSgcvRB9nNYG&qid=1&ra_mode=more&ra_name=PublicationYear&colName=WOS&viewType=raMore"
url = "http://apps.webofknowledge.com/RAMore.do?product=WOS&search_mode=GeneralSearch&SID=8FwXgipnJJ3APCPlrM8&qid=2&ra_mode=more&ra_name=PublicationYear&colName=WOS&viewType=raMore"
browser = webdriver.Chrome(executable_path=(path_to_chromedriver))
browser.get(url3)
tr_items = browser.find_element_by_id('PublicationYear_raMore_tr').find_elements_by_xpath('.//tr')
time.sleep(1)
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
    p = int(p)
    return p


def product_legitimate_years_set(start_year, end_year):
    return set(range(start_year, end_year + 1))


legitimate_years_set = product_legitimate_years_set(2008, 2018)

def get_batch_size_sample(a_list, batch_size):
    for i in range(0, len(a_list), batch_size):
        yield a_list[i:min(len(a_list), i + batch_size)]

checked_years_numbers = 0
for publication_years_column_number in range(0, 4):
    for tr_item in tr_items:
        td_items = tr_item.find_elements_by_xpath('.//td')
        td_3_items_list = list(get_batch_size_sample(td_items, batch_size=3))
        last_row = 0
        try:
            td_3_item = td_3_items_list[publication_years_column_number]
        except:
            last_row = 1
        if last_row==0:
            contain_brackets = td_3_item[1].text
            if "(" in contain_brackets and ")" in contain_brackets:
                td_item_year = int(td_3_item[1].find_element_by_xpath('./label').text[:4])
                if td_item_year in legitimate_years_set:
                    td_3_item[0].find_element_by_xpath('./input').click()
                    checked_years_numbers = checked_years_numbers + 1
                    time.sleep(0.3)


browser.find_element_by_id('raMore').find_element_by_xpath(
    './table/tbody/tr/td/table/tbody/tr/td[2]/div/button').click()

task_current_url_first = browser.current_url
# 获取第一页中第一个高引论文的URL
browser.find_element_by_xpath('//div[@class="search-results-content"]/div/div/a').click()
time.sleep(1)
First_Paper_URL = browser.current_url
# 获取最后一页页码数目
browser.get(task_current_url_first)
time.sleep(3)
last_page_num = browser.find_element_by_id('pageCount.top').text
last_page_num = get_int_from_str(last_page_num)
# 清空页码输入框
browser.find_element_by_xpath('//input[@name="page"][@size="5"]').clear()
time.sleep(3)
# 输入最后一页页码，并进入
browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(last_page_num)
time.sleep(3)
browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(Keys.ENTER)

zui_hou_yi_ye_paper_num = len(browser.find_elements_by_xpath('//div[@class="search-results-content"]/div/div/a'))
print(zui_hou_yi_ye_paper_num)

print(zui_hou_yi_ye_paper_num)
print(last_page_num)
