###############################################################
"""
동아일보 검색 사이트에서 기사링크와 제목을 수집하는 프로그램  

뉴스만 검색하여 제목과 사이트를 찾아
아래와 같이 겁색 결과를 주소와 제목을 쌍으로 파일로 저장함

https://www.donga.com/news/article/all/20220506/113264071/1, "SKTSK스퀘어, 넥스트 플랫폼 이끈다한국판 로블록스 해긴에 공동 투자"
https://www.donga.com/news/article/all/20220506/113261610/1, "[스타트업] 개발만큼 중요한 것은 고객과의 소통, 당근마켓 서비스 운영 이야기"
https://www.donga.com/news/article/all/20220506/113261418/1, "[모빌리티 인사이트] 일상 속 자율주행, 로봇청소기"
...

"""
###############################################################

import requests # 인터넷 접속을 위한 라이브러리
from bs4 import BeautifulSoup as bs 
# css selector를 이용하여 웹 데이터 추출을 편리하게 도와주는 라이브러리
import re # 정규 표현식(regular expression)을 이용하게 해 주는 라이브러리




query = '인공지능'       
# 기사 검색어

extracts = re.compile('[^ 가-힣|a-z|A-Z|0-9|\[|\]|(|)|-|~|?|!|.|,|:|;|%]+')
# 추출된 내용에서 특수 문자나 필요없는 문자들을 제외하고 위와 같은 문자들만 남기기 위한 정규식 설정값
# 여기서는 제목 내용 확인을 편리하게 하도록 특수 문자들을 최대한 살려 놓음


fout = open('/Users/choiyoungmi/anaconda3/envs/bigdata/webcrawling_2023/data/search_list_result_donga(' + query + ').csv', 'w', encoding='utf8')  
# 결과 리스트를 저장할 파일 이름(검색어를 넣어줌)

page=1 #페이지를 증가시키면서 검색 결과를 가져오기 위한 변수
page_num = 1 #pagination 에서 보고싶은 총 페이지수 
num = 15 * (page_num - 1) + 1 #동아일보의 경우, 기사 개수가 URL에 들어가서, 그게 맞는 계산법

while page <= num:

    rs = requests.get(f'https://www.donga.com/news/search?p={page}&query={query}&check_news=93&more=1&sorting=1&search_date=1&v1=&v2=')
    

    # 동아일보 검색 사이트의 검색 주소창 내용으로 검색 요청
    # 이 주소 데이터를 얻기 위해서는 검색 사이트에서 검색 결과를 반복 조회하는 동작 필요
       
    rs.encoding = None      # 한글 깨짐을 방지하기 위한 인코딩 자동 변환 방지

    html = rs.text      # 검색 결과 페이지의 html 문서를 통채로 가져옴

    # html 문서를 파싱하기 위해 BeautifulSoup 형식으로 저장
    soup = bs(html, 'html.parser')
    
    # 검색 결과의 제목과 사이트 주소가 포함되어 있는 부분의 css selector. 이 실렉터로 해당 데이터 가져옴
    # 리스트 형식으로 여러개 반환
    titles = soup.select('div.articleList > div.rightList > span.tit > a:nth-of-type(1)')       #articleList가 class 여서 .이 붙음
    print(len(titles))   # scraping 한 기사 링크 개수 출력

   
    #검색 결과가 여러 개(동아일보의 경우 15개)인 경우 리스트 요소들로부터 하나씩 불러와서 작업하기 위한 반복문
    for title in titles:    
       
        #print(title.get('href'))   #href에 있는 링크주소 가져오기
        #print(title.get_text())    #태그의 문자열 가져오기
        
       
        fout.write(title.get('href')) # 출력파일에 주소 출력
        fout.write(', ') 
        
        fout.write(title.get_text())  # 출력파일에 제목 출력
         
        fout.write('\n') # 한줄에 한쌍씩 나오도록 줄바꿈



    page += 15      
    # 검색 페이지 하나가 종료되면 다음 페이지를 위해 변수값 증가 (동아일보의 경우 기사 개수만큼 증가)

fout.close() 

