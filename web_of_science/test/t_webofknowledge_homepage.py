from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from WOS_settings import path_to_chromedriver

browser = webdriver.Chrome(executable_path=(path_to_chromedriver))
url_one = "http://apps.webofknowledge.com/Search.do?product=WOS&SID=6CkZ5mVPpvHHkcUIaqI&search_mode=GeneralSearch&prID=7985804d-95ba-4321-8200-5a30ab3f535c"
browser.get(url_one)

last_page_num_index = browser.find_element_by_id('pageCount.top').text
print(last_page_num_index)

# 如果只有一页
if last_page_num_index == 1:
    last_paper_numbers = len(
        browser.find_elements_by_xpath('//div[@class="search-results-content"]/div/div/a'))


browser.find_element_by_xpath('//input[@name="page"][@size="5"]').clear()
time.sleep(1)
browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(last_page_num_index)
time.sleep(1)
browser.find_element_by_xpath('//input[@name="page"][@size="5"]').send_keys(Keys.ENTER)
last_paper_numbers = len(browser.find_elements_by_xpath('//div[@class="search-results-content"]/div/div/a'))
print(last_paper_numbers)