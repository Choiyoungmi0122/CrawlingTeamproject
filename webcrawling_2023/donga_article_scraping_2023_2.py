###############################################################
"""
파일로 저장된 동아일보 기사 링크와 제목쌍 데이터 파일에서 
해당 기사링크의 기사 날짜, 제목, 내용을 수집하는 프로그램  

기사링크와 제목쌍 데이터 파일은 아래와 같은 형식이어야 함


https://www.donga.com/news/article/all/20220506/113264071/1, "SKTSK스퀘어, 넥스트 플랫폼 이끈다한국판 로블록스 해긴에 공동 투자"
https://www.donga.com/news/article/all/20220506/113261610/1, "[스타트업] 개발만큼 중요한 것은 고객과의 소통, 당근마켓 서비스 운영 이야기"
https://www.donga.com/news/article/all/20220506/113261418/1, "[모빌리티 인사이트] 일상 속 자율주행, 로봇청소기"
"""
###############################################################


import requests # 인터넷 접속을 위한 라이브러리
from bs4 import BeautifulSoup as bs 
# css selector를 이용하여 웹 데이터 추출을 편리하게 도와주는 라이브러리
import re # 정규 표현식(regular expression)을 이용하게 해 주는 라이브러리
import csv # csv 형식의 파일을 다루기 위한 라이브러리
import datetime # 날짜, 시간 함수를 위한 라이브러리

f = open('/Users/choiyoungmi/anaconda3/envs/bigdata/webcrawling_2023/data/search_list_result_donga(인공지능).csv', 'r', encoding='utf8')     
# scraping하려는 기사링크, 제목쌍의 리스트 파일 이름 

rdr = csv.reader(f) # csv 형식으로 읽어 들임

now = datetime.datetime.now() # 현재 날짜와 시간
nowDatetime = now.strftime('%Y-%m-%d(%H,%M,%S)') # 해당 형식으로 변환

fout = open('/Users/choiyoungmi/anaconda3/envs/bigdata/webcrawling_2023/data/scraped_articles_donga[' + nowDatetime +'].csv', 'w', encoding='utf8')    
#결과 출력 파일 이름(수집한 날짜와 시간을 자동으로 달아 줌)

# 제목줄 출력
fout.write('"adate"')   
fout.write(', ')
fout.write('"atitle"')
fout.write(', ')
fout.write('"article"')
fout.write('\n')

extracts = re.compile('[^ 가-힣|0-9|.|-|~|?|%]+')
# 추출된 텍스트에서 특수 문자나 필요없는 문자들을 제외하고 위와 같은 문자들만 남기기 위한 정규식 설정값

# 분석을 위한 추출 데이터에서는 각 칼럼 데이터에 ,가 들어가지 않도록 주의.
# R 언어에서는 컬럼 데이터를 큰따옴표 한쌍으로 "..." 형식을 잘 만들어 줄 경우 중간에 콤마가 들어 있어도 
# csv 형식으로 읽어서 분석할 때 문제가 없음.
# 그러나 Python에서는 큰따옴표가 있어도 csv 형식으로 읽을 경우 무조건 콤마를 기준으로 끊어 읽으므로, 
# 추후 Python에서 다른 처리나 분석을 위해서는 저장할 때 데이터 내에는 콤마가 들어가지 않도록 주의하여 함
# 그래서 정규 표현식에서 ,를 남기지 않도록 제외하였음.


for line in rdr:    # 기사링크, 제목 쌍 파일에서 한 줄씩 읽어 들임

    addr = line[0]
    # csv 형식으로 읽을 경우 한 줄은 2개의 요소로 구성되면 리스트 형식으로 보관되어 있음
    # 따라서 line[0]은 기사링크 문자열, line[1]은 제목 문자열

    print(line[0]) # 수집 진행 상황을 보여주기 위해 기사 링크 주소를 콘솔에 출력  
    
    r2 = requests.get(addr) # 이 주소로 기사 사이트 방문
    
    r2.encoding = None      #한글이 깨지는 것을 방지하기 위해 인코딩의 원래값을 유지하도록 함
    
    html2 = r2.text # 전송된 웹 데이터에서 텍스트 데이터만 걸러 냄
    
    soup = bs(html2, 'html.parser')
    # html 문서를 파싱하기 위해 BeautifulSoup 형식으로 저장

############# 기사 날짜 추출하는 부분    
    tagsdate = soup.select('div.article_title > div.title_foot > span.date01')

   
    #기사 날짜 부분의 실렉터로 요소 추출. 리스트 형식으로 반환
    
    adate = tagsdate[0].getText() # 해당 요소에서 태그를 제외한 순수 텍스트만 추출
    # 리스트에서 두번쨰 요소가 실제 날짜임
    
    adate = adate[3:13]    # 2018.02.26 처럼 숫자 부분만 추출하기 위한 문자열 슬라이싱   
    
    adate = '"'+adate+'"' # 큰따옴표를 감싸 줌

############## 기사 제목 추출하는 부분
    tagstitle = soup.select('h1.title')  
    #기사 제목 부분 실렉터로 요소 추출. 리스트 형식으로 반환
                                
    atitle = tagstitle[0].getText() 
    # 실제 요소 한개만 추출되므로 첫번째 리스트 요소가 제목임
    
    atitle = str(atitle) 
    # 정규식 함수 적용을 위해 뷰티플수프에서 리턴해 주는 데이터를 문자열 형식으로 변환
    
    atitle = extracts.sub('', atitle)
    # 제목 문자열에서 정규식에 의해 지정된 문자만 남김

    atitle = re.sub(' +', ' ', atitle) 
    # 정규 표현식을 사용하여 중복된 공백을 하나로 줄임  


    atitle = '"'+atitle+'"'

############## 기사 본문 추출하는 부분
    tagsarticle = soup.select('div.article_txt')
    # 기사 본문을 의미하는 실렉터로 요소 추출
    # 중간에 그림이나 광고등이 있을 경우 기사 본문이 여러 단락으로 구성되어 있기 때문에
    # 각 부분을 요소로 갖는 리스트 형식으로 추출됨
    # 리스트 형식으로 반환
    
    article = ''
    
    # 기사 각 부분을 하나의 문자열로 합치기 위해 리스트의 각 요소를 읽어 들이면서 반복
    for text in tagsarticle:   
        article = article + text.getText()
    
    article = extracts.sub('', article)
    # 본문 문자열에서 정규식에 의해 지정된 문자만 남김
    
    article = re.sub(' +', ' ', article)
    # 정규 표현식을 사용하여 중복된 공백을 하나로 줄임

    article = '"'+article+'"'
    
    
    #CSV 형식으로 저장하기 위한 출력문
    fout.write(adate)   
    fout.write(', ')
    fout.write(atitle)
    fout.write(', ')
    fout.write(article)
    fout.write('\n')

f.close()        
fout.close()




    
 




