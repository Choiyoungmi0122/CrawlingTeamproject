# from selenium import webdriver
# from webdriver_manager.chrome import ChromeDriverManager
# import time

# import pandas as pd #csv를 읽고 dataframe을 사용하기 위한 pandas

# # from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException #예외처리를 위한 예외들 
# # 웹 드라이버 초기화
# chrome_driver= ChromeDriverManager().install()
# driver=webdriver.Chrome(chrome_driver)
# print(chrome_driver)
# # # 웹 페이지 접속
# driver.get('https://naver.com')
# # driver.implicitly_wait(5)  #로딩완료될때까지 10초정도 기다리기

# # # for i in range(10):
# # #     //*[@id="_pcmap_list_scroll_container"]/ul/li[i].click()

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd #csv를 읽고 dataframe을 사용하기 위한 pandas
from selenium import webdriver #브라우저를 띄우고 컨트롤하기 위한 webdriver
from selenium.webdriver.common.keys import Keys #브라우저에 키입력 용
from selenium.webdriver.common.by import By #webdriver를 이용해 태그를 찾기 위함
from selenium.webdriver.support.ui import WebDriverWait #Explicitly wait을 위함
# from webdriver_manager.chrome import ChromeDriverManager #크롬에서 크롤링 진행 크롬 웹 드라이버 설치시 필요
from selenium.webdriver.support import expected_conditions as EC #브라우저에 특정 요소 상태 확인을 위해
from selenium.webdriver.support.ui import Select  # 드롭다운 메뉴를 위해 Select를 가져옵니다.
from bs4 import BeautifulSoup #브라우저 태그를 가져오고 파싱하기 위함
import time
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException,TimeoutException #예외처리를 위한 예외들 
import csv
# 브라우저 꺼짐 방지 옵션
chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=chrome_options)

# result = pd.DataFrame(columns=['병원종류 ', '병원이름', '주소',  '운영시간', '전화번호', '특징', '진료과목', '전문의 수'])
hospitaltype = []
# //_ngcontent-oke-c113
driver.get('https://map.naver.com/v5/search/%EB%B3%91%EC%9B%90?c=14,0,0,0,dh')
time.sleep(5)
driver.switch_to.frame('searchIframe')
time.sleep(5)

# 대기 시간 설정
wait = WebDriverWait(driver, 10)

# 요소가 나타날 때까지 대기 후 클릭
element_to_click = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="_pcmap_list_scroll_container"]/ul/li[3]')))
element_to_click.click()

driver.switch_to.default_content()  # frame 초기화

driver.switch_to.frame('entryIframe')

wait
temperature_xpath = driver.find_element(By.XPATH, '//*[@id="_title"]/span[1]')

temperature = temperature_xpath.text

print(temperature)
# type = driver.find_element(By.XPATH, '//*[@id="_title"]/span[1]')
# hospitaltype = type.txt()
# print(hospitaltype)


