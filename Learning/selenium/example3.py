from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

driver = webdriver.Remote(
   command_executor='http://127.0.0.1:4444/wd/hub',
   desired_capabilities=DesiredCapabilities.CHROME)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.OPERA)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)

# driver = webdriver.Remote(
#    command_executor='http://127.0.0.1:4444/wd/hub',
#    desired_capabilities={'browserName': 'htmlunit',
#                          'version': '2',
#                         'javascriptEnabled': True})

driver.get('http://www.python.org')
assert "Python" in driver.title
print(driver.window_handles)
elem=driver.find_element_by_name('q')
elem.clear()
elem.send_keys('pycon')
elem.send_keys(Keys.RETURN)
assert 'No results found.' not in driver.page_source
driver.close()