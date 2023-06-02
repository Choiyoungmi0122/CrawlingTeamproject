from bs4 import BeautifulSoup

html = '<div class="O8qbU pSavy"><strong class="Aus_8"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 16 18" class="DNzQ2" aria-hidden="true"><path d="M8 16A7 7 0 108 2a7 7 0 000 14zm0 1A8 8 0 118 1a8 8 0 010 16zm.5-7.8l3.02 1.76a.5.5 0 01.19.68.5.5 0 01-.69.19L7.8 9.96a.5.5 0 01-.3-.46v-5a.5.5 0 011 0v4.7z"></path></svg><span class="place_blind">영업시간</span></strong><div class="vV_z_"><a href="#" target="_self" role="button" class="gKP9i RMgN0" aria-expanded="true"><div class="w9QyJ vI8SM"><div class="y6tNq"><div class="A_cdD"><em>진료 중</em><span class="U7pYf"><time aria-hidden="true">18:30에 진료 종료</time><span class="place_blind">18시 30분에 진료 종료</span></span></div></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">수</span><div class="H3ua4">09:00 - 18:30<br>13:00 - 14:00 휴게시간</div></span></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">목</span><div class="H3ua4">14:00 - 18:30</div></span></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">금</span><div class="H3ua4">09:00 - 18:30<br>13:00 - 14:00 휴게시간</div></span></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">토</span><div class="H3ua4">09:00 - 13:30</div></span></div></div><div class="w9QyJ undefined"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">일</span><div class="H3ua4"><span>정기휴무 (매주 일요일)</span></div></span></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">월</span><div class="H3ua4">09:00 - 18:30<br>13:00 - 14:00 휴게시간</div></span></div></div><div class="w9QyJ"><div class="y6tNq"><span class="A_cdD"><span class="i8cJw">화</span><div class="H3ua4">09:00 - 18:30<br>13:00 - 14:00 휴게시간</div></span></div></div><div class="w9QyJ yN6TD"><div class="y6tNq"><span class="A_cdD">05/27  부처님 오신 날 휴무</span><span class="_UCia"><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 12 7" class="DNzQ2" aria-hidden="true"><path d="M11.47.52a.74.74 0 00-1.04 0l-4.4 4.45v.01L1.57.52A.74.74 0 10.53 1.57l5.12 5.08a.5.5 0 00.7 0l5.12-5.08a.74.74 0 000-1.05z"></path></svg><span class="place_blind">접기</span></span></div></div></a></div></div>'  # 주어진 HTML 코드

soup = BeautifulSoup(html, 'html.parser')

# 운영 시간과 요일 추출
operating_time_div = soup.find('div', class_='O8qbU pSavy')

operating_hours = {}  # 운영 시간과 요일을 저장할 딕셔너리

if operating_time_div:
    time_divs = operating_time_div.find_all('div', class_='H3ua4')
    for time_div in time_divs:
        time_span = time_div.find_previous_sibling('span', class_='i8cJw')
        if time_span:
            time = time_div.get_text(strip=True)
            day = time_span.get_text(strip=True)
            operating_hours[day] = time

filename = 'operating_times.csv'  # 저장할 CSV 파일명

with open(filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Day', 'Operating Hours'])  # 헤더 추가
    for day, time in operating_hours.items():
        writer.writerow([day, time])  # 요일과 운영 시간 추가

print(f'{filename} 파일이 저장되었습니다.')
