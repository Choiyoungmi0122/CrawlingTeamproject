# selenium의 webdriver를 사용하기 위한 import
from selenium import webdriver

# selenium으로 키를 조작하기 위한 import
from selenium.webdriver.common.keys import Keys

# 페이지 로딩을 기다리는데에 사용할 time 모듈 import
import time

# 크롬드라이버 실행
# 경로 예: '/Users/Name/Downloads/chromedriver'(Mac OS)
driver = webdriver.Chrome('/Users/choiyoungmi/Downloads/chromedriver_mac_arm64.exe') 

#크롬 드라이버에 url 주소 넣고 실행
driver.get('https://www.google.co.kr/')

# 페이지가 완전히 로딩되도록 3초동안 기다림
time.sleep(3)

# 검색어 창을 찾아 search 변수에 저장 (css_selector 이용방식)
search_box = driver.find_element_by_css_selector('input.gLFyf.gsfi')

# 검색어 창을 찾아 search 변수에 저장 (xpath 이용방식)
search_box = driver.find_element_by_xpath('//*[@id="google_search"]')

search_box.send_keys('파이썬')
search_box.send_keys(Keys.RETURN)
time.sleep(1)
