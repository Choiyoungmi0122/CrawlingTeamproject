import json
import time
from time import sleep

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException

# 브라우저 꺼짐 방지 옵션
chrome_options = Options() 
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

url = 'https://map.naver.com/v5/search'
driver.get(url)

key_word = '부산 동래구 병원'  # 검색어


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


# dictionary 생성
parking_dict = {'병원정보': []}
# 시작시간
start = time.time()

print('[크롤링 시작...]')


#크롤링 (페이지 리스트 만큼)
for _ in range(6):
    page_down(40)
    sleep(3)
    
    # 장소 리스트
    parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')

    for index, data in enumerate(parking_list, start=0): #장소 리스트 만큼    enumerate = 이름 적는거 
        work=[]
        try:
            print(len(parking_list))
            if(index+1 == len(parking_list)):
                driver.find_element(By.XPATH, '//*[@id="app-root"]/div/div[2]/div[2]/a[7]').click()

            print(index+1)
            
            # (1) 상세정보 버튼 누르기 
            driver.find_element(By.CSS_SELECTOR, '#_pcmap_list_scroll_container > ul > li:nth-child({}) > div.IPtqD > a:nth-child(1) > div.LYTmB > div > span.place_bluelink.q2LdB'.format(index+1)).click()
            sleep(3)
            
            #프레임전환
            switch_frame('entryIframe')
            sleep(1)

            # (3) 장소명
            names = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/span[1]') 
            name = names[0].text
            print(name)
            # (4) 병원 유형 
            types = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[2]/div[1]/div[1]/span[2]') 
            type = types[0].text
            #(5) 병원 주소
            addresses = driver.find_elements(By.XPATH, '/html/body/div[3]/div/div/div/div[6]/div/div[1]/div/div/div[1]/div/a/span[1]') 
            if len(addresses) > 0:
                address = addresses[0].text
            else:
                phone = "No address number available"
                index+=1
                

            # (6) 전화번호
            phones = driver.find_elements(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.nbXkr > div > span.xlx7Q')
            if len(phones) > 0:
                phone = phones[0].text
            else:
                phone = "No phone number available"
                index+=1

            # (7) 영업시간 상세 버튼 누르기
            driver.find_element(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy > div > a > div.w9QyJ.vI8SM > div > div > span').click()
            sleep(1)

            #(8) 영업시간 불러오기
            for day in range(2,9):
                working = driver.find_elements(By.CSS_SELECTOR, '#app-root > div > div > div > div:nth-child(6) > div > div.place_section.no_margin.vKA6F > div > div > div.O8qbU.pSavy > div > a > div:nth-child({})'.format(day))
                working = [element.text for element in working]
                work.extend(working)

        except NoSuchElementException:
            print("요소를 찾을 수 없습니다.")
            index+=1
        except ElementClickInterceptedException:
            print("클릭할 수 없는 요소입니다. 다른 방법으로 시도해보세요.")
            index+=1


        # dict에 데이터 집어넣기
        dict_temp = {
            '이름': name,

            '병원주소' : address,
            '병원종류' : type,
            '영업시간' : work,
            '전화번호' : phone
        }
        parking_dict['병원정보'].append(dict_temp)
        print(f'{name}...완료')
        with open('/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/중구.json', 'w', encoding='utf-8') as f:
            json.dump(parking_dict, f, indent=4, ensure_ascii=False)

        # 프레임 전환
        switch_frame('searchIframe')
        sleep(1)
    


    


sleep(1)        
print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.


