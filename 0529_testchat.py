import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

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

# (2) frame 변경
switch_frame('searchIframe')
page_down(40)
sleep(3)

# dictionary 생성
parking_dict = {'병원정보': []}
# 시작시간
start = time.time()

print('[크롤링 시작...]')
# 장소 리스트
parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')
print(parking_list)

#[<selenium.webdriver.remote.webelement.WebElement (session="bdea8eeab0f544ba4b7bed03e2e30ace", element="9E2D84DE1F26E97B6AD3EA3FE59FB171_element_130")>]
for index, data in enumerate(parking_list, start=0):  #장소 리스트 만큼
    
    print(index+1)

    sleep(5)
    try:
        # (1) 상세정보 버튼 누르기 
        driver.find_element(By.XPATH, '/html/body/div[3]/div/div[2]/div[1]/ul/li[{}]/div[2]/a[1]/div[1]/div/span[1]'.format(index+1)).click()
        sleep(3)

        #프레임전환
        switch_frame('entryIframe')
        sleep(2)

        names = driver.find_elements(By.CSS_SELECTOR, '.Fc1rA')  # (3) 장소명

        name = names[index - 1].text
        print(name)

        # dict에 데이터 집어넣기
        dict_temp = {
            'ho': name
        }
        parking_dict['병원정보'].append(dict_temp)
        print(f'{name}...완료')
        
        sleep(3)

        # 프레임 전환
        switch_frame('searchIframe')
        sleep(2)
            
    except ValueError as e:
        print("ValueError:", e)
    except Exception as e:
        print("Exception:", e)

sleep(2)        
print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.

# json 파일로 저장
with open('/Users/kim/Desktop/youngmi/data_test.json', 'w', encoding='utf-8') as f:
    json.dump(parking_dict, f, indent=4, ensure_ascii=False)