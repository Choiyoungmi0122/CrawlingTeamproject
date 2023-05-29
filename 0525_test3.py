import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

url = 'https://map.naver.com/v5/search'
driver.get(url)
key_word = '병원'  # 검색어

# css 찾을때 까지 10초대기
def time_wait(num, code):
    try:
        wait = WebDriverWait(driver, num).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, code)))
    except:
        print(code, '태그를 찾지 못하였습니다.')
        driver.quit()
    return wait

res = driver.page_source  # 페이지 소스 가져오기
soup = BeautifulSoup(res, 'html.parser')  # html 파싱하여  가져온다

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경

# 페이지 다운
def page_down(num):
    body = driver.find_element(By.CSS_SELECTOR, 'body')
    body.click()
    for i in range(num):
        body.send_keys(Keys.PAGE_DOWN)

# css를 찾을때 까지 10초 대기
time_wait(10, 'div.input_box > input.input_search')

# (1) 검색창 찾기
search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys(key_word)  # 검색어 입력
search.send_keys(Keys.ENTER)  # 엔터버튼 누르기

sleep(5)

# frame 변경 메소드
def switch_frame(frame):
    driver.switch_to.default_content()  # frame 초기화
    driver.switch_to.frame(frame)  # frame 변경
    res
    soup



# (2) frame 변경 
switch_frame('searchIframe')
page_down(40)
sleep(5)

# 병원 리스트
parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')

# dictionary 생성
parking_dict = {'병원정보': []}

# 시작시간
start = time.time()

print('[크롤링 시작...]')
print(parking_list)

# 크롤링 (페이지 리스트 만큼)
for btn in range(2): 
    parking_list
    for data in range(len(parking_list)):   # 병원 리스트 만큼
        page = driver.find_element(By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[data]').click
        sleep(2)

        try:
            # 상세 페이지로 이동
            switch_frame('entryIframe')
            time_wait(5, '._3XamX')
            # 스크롤을 맨밑으로 1초간격으로 내린다.
            for down in range(3):
                sleep(1)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # -----매장명 가져오기-----
            store_name = driver.find_element(By.CSS_SELECTOR('.Fc1rA')).text
            print(store_name)
        except:
            pass
        