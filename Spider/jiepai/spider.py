import requests
from urllib.parse import urlencode
from requests.exceptions import RequestException
import json
import random
import re
from bs4 import BeautifulSoup
from config import *
import pymongo
import os
from hashlib import md5
from multiprocessing import Pool

client =pymongo.MongoClient(MONGO_URL,connect=False)
db=client[MONGO_DB]

def get_page_index(headers, offset, keyword):
    data = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': 20,
        'cur_tab': 1,
        'from': 'search_tab'
    }
    url = 'https://www.toutiao.com/search_content/?' + urlencode(data)
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('request index page error...')
        return None


def parse_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

def get_page_detail(url,headers):
  try:
    response=requests.get(url,headers)
    if response.status_code ==200:
      return response.text
    return None
  except RequestException:
    print('{0} requests detail page error... '.format(url))
    return None

def parse_page_detail(html,url):
  soup=BeautifulSoup(html,'lxml')
  title=soup.select('title')[0].get_text()
  
  pattern=re.compile('gallery: JSON.parse\("(.*?)"\),',re.S)
  result=re.search(pattern,html)
  if result:
    result=eval("'{}'".format(result.group(1)))
    data=json.loads(result)
    if data and 'sub_images' in data.keys():
      sub_images=data.get('sub_images')
      images=[item.get('url') for item in sub_images]
      for image in images:
        download_image(image)
      return {
        'title':title,
        'url':url,
        'images':images
      }

def save_to_mongo(result):
    if db[MONGO_TABLE].insert_one(result):
      print('save into mongodb',result)
      return True
    return False
  
def download_image(url):
  print('download image...',url)
  try:
    response=requests.get(url)
    if response.status_code ==200:
      save_iamge(response.content) 
    return None
  except RequestException:
    print('{0} requests image error... '.format(url))
    return None
    
def save_iamge(content):
  file_path='{0}/{1}.{2}'.format(os.getcwd(), md5(content).hexdigest(),'jpg')
  if not os.path.exists(file_path):
    with open(file_path,'wb') as f:
      f.write(content)
      
def main(offset):
    my_headers = ["Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36",
                  "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:30.0) Gecko/20100101 Firefox/30.0",
                  "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.75.14 (KHTML, like Gecko) Version/7.0.3 Safari/537.75.14",
                  "Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.2; Win64; x64; Trident/6.0)"
                  ]
    random_header = random.choice(my_headers)
    headers = {"User-Agent": random_header}
    html = get_page_index(headers, offset, KEYWORD)
    # print(html)
    for url in parse_page_index(html):
      if url:
        html=get_page_detail(url, headers)
        if html:
          result=parse_page_detail(html,url)
          if result:
            save_to_mongo(result)
        


if __name__ == "__main__":
    #main()
    groups=[x*20 for x in range(GROUP_START,GROUP_END)]
    pool =Pool()
    pool.map(main,groups)
