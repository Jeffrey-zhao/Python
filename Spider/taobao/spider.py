from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re
from pyquery import PyQuery as pq
import pymongo
from config import *


client=pymongo.MongoClient(MONGO_URL)
db=client[MONGO_DB]
#browser=webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser=webdriver.Chrome()
wait=element=WebDriverWait(browser,10)
browser.set_window_size(1400,900)

def search():
    print('searching...')
    try:
        headers={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"}
        browser.get('https://www.taobao.com')
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#q')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#J_TSearchForm > div.search-button > button')))
        input.send_keys(KEYWORD)
        submit.click()
        total=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.total')))
        return total.text
    except TimeoutException:
        return search()

def next_page(page_number):
    print('loading page',page_number)
    try:
        input=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > input')))
        submit=wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')))
        input.clear()
        input.send_keys(page_number)
        submit.click()
        wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR,'#mainsrp-pager > div > div > div > ul > li.item.active > span'),str(page_number)))
        get_products()

    except TimeoutException:
        next_page(page_number)

def get_products():
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR,'#mainsrp-itemlist .items .item')))
    html=browser.page_source
    doc=pq(html)
    items=doc('#').items()
    for item in items:
        product={
            'image':item.find('.pic .img').attr('src'),
            'price':item.find('.price').text(),
            'deal':item.find('.deal-cnt').text()[:-3],
            'title':item.find('.title').text(),
            'shop':item.find('.shop').text(),
            'location':item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    try:
        if db[MONGO_TABLE].insert_one(result):
            print('save into mongodb successfully',result)
    except Exception:
        print('save into mongodb failed',result)

def main():
    try:
        total=search()
        total=int(re.compile('(\d+)').search(total).group(1))
        #print(total)
        for i in range(2,total+1):
            next_page(i)
    except Exception:
        print('error ...')
    finally:
        browser.close()

if __name__ =="__main__":
    main()