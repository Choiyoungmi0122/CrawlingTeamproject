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

# 장소 리스트
parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')
# dictionary 생성
parking_dict = {'병원정보': []}
# 시작시간
start = time.time()

print('[크롤링 시작...]')
print(parking_list)

# 크롤링 (페이지 리스트 만큼)
for btn in range(2): 
    parking_list = driver.find_elements(By.CSS_SELECTOR, 'li.DWs4Q')
    names = driver.find_elements(By.CSS_SELECTOR, '.q2LdB')  # (3) 장소명
    types = driver.find_elements(By.CSS_SELECTOR, '.lHBM6')  # (4) 장소 유형


    for data in range(len(parking_list)):  #장소 리스트 만큼
        print(data)

        sleep(1)
        try:
            # 지번, 도로명 초기화
            jibun_address = ''
            road_address = ''

            # (3) 병원명 가져오기
            parking_name = names[data].text
            print(parking_name)

            # (4) 유형
            parking_type = types[data].text
            print(parking_type)

            # # (5) 주소 버튼 누르기
            # address_buttons = driver.find_elements(By.CSS_SELECTOR, '.berX5 > a')
            # address_buttons.__getitem__(data).click()

            # # 로딩 기다리기
            # sleep(1)

            # # (7) 주소 눌렀을 때 상세정보 나오는 div
            # addr = driver.find_elements(By.CSS_SELECTOR, '.tAvTy > div')

            # # 지번만 있는 경우
            # if len(addr) == 1 and addr.__getitem__(0).text[0:2] == '지번':
            #     jibun = addr.__getitem__(0).text
            #     last_index = jibun.find('복사우\n')    # 복사버튼, 우편번호 제외하기 위함
            #     jibun_address = jibun[2:last_index]
            #     print("지번 주소:", jibun_address)

            # # 도로명만 있는 경우
            # elif len(addr) == 1 and addr.__getitem__(0).text[0:2] == '도로':
            #     road = addr.__getitem__(0).text
            #     last_index = road.find('복사우\n')     # 복사버튼, 우편번호 제외하기 위함
            #     road_address = road[3:last_index]
            #     print("도로명 주소:", road_address)

            # # 도로명, 지번 둘 다 있는 경우
            # else:
            #     # 도로명
            #     road = addr.__getitem__(0).text
            #     road_address = road[3:(len(road) - 2)]
            #     print("도로명 주소:", road_address)

            #     # 지번
            #     jibun = addr.__getitem__(1).text
            #     last_index = jibun.find('복사우\n')    # 복사버튼, 우편번호 제외하기 위함
            #     jibun_address = jibun[2:last_index]
            #     print("지번 주소:", jibun_address)

            # # dict에 데이터 집어넣기
            # dict_temp = {
            #     'name': parking_name,
            #     'parking_type': parking_type,
            #     'road_address': road_address,
            #     'jibun_address': jibun_address
            # }

            for i in range(1,10):
            # (8) 상세정보 버튼 누르기 
                infor_buttons = driver.find_element(By.XPATH, f'//*[@id="_pcmap_list_scroll_container"]/ul/li[(i)]/div[2]/a[1]/div/div/span[1]').click()
                sleep(1)

                # (9) 상세정보 눌렀을 때 도로명, 지번 나오는 div
                infor = driver.find_elements(By.CSS_SELECTOR, '.main > div')

                #프레임전환
                driver.switch_to.default_content()
                switch_frame('entryIframe')
                sleep(3)
            
                # (10) 일정 버튼 누르기
                work_button = driver.find_elements(By.CSS_SELECTOR, '.vV_z_ > a')
                work_button.__getitem__(data).click()

                #로딩기다리기
                sleep(2)

                # (11) 일정 눌렀을 때 상세정보 나오는 div
                addr = driver.find_elements(By.CSS_SELECTOR, '.pSavy > div')

            # (11) 일정 눌렀을 때 상세정보 나오는 div
            

            parking_dict['병원정보'].append(dict_temp)
            print(f'{parking_name} ...완료')

            sleep(1)

        except Exception as e:
            print(e)
            print('ERROR!' * 3)

            # dict에 데이터 집어넣기
            dict_temp = {
                'name': parking_name,
                'parking_type': parking_type,
                'road_address': road_address,
                'jibun_address': jibun_address
                # 'infor_buttons' : infor_buttons,
                # 'work_button' : work_button
            }

            parking_dict['병원정보'].append(dict_temp)
            print(f'{parking_name} ...완료')

            sleep(1)

print('[데이터 수집 완료]\n소요 시간 :', time.time() - start)
driver.quit()  # 작업이 끝나면 창을 닫는다.

# json 파일로 저장
with open('/Users/kim/Desktop/youngmi/data_test.json', 'w', encoding='utf-8') as f:
    json.dump(parking_dict, f, indent=4, ensure_ascii=False)