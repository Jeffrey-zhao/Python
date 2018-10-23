from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

browser=webdriver.Chrome()

def search():
    browser.get('https://www.taobao.com')
    try:
        element=WebDriverWait(browser,10).until(
            EC.presence_of_element_located(By.ID,''))
        )
    finally:
        browser.quit()