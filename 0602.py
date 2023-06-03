import pandas as pd
import json

# JSON 파일로부터 데이터 불러오기
with open("//Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/json모아둠/강서구.json", encoding='utf-8') as file:
    json_data = json.load(file)


# "병원정보" 키의 값을 추출
hospital_info = json_data["병원정보"]

# 데이터프레임 생성을 위한 리스트 초기화
data_list = []

# 각 병원 정보를 순회하며 필요한 데이터 추출
for hospital in hospital_info:
    name = hospital["이름"]
    address = hospital["병원주소"]
    hospital_type = hospital["병원종류"]
    time_list = hospital["영업시간"]
    phone_number = hospital["전화번호"]
    
    # 요일별 운영시간, 휴게시간 초기화
    monday_time = ""
    tuesday_time = ""
    wednesday_time = ""
    thursday_time = ""
    friday_time = ""
    saturday_time = ""
    sunday_time = ""
    lunch_break = ""
    
    # 각 요일별 운영시간, 휴게시간 추출
    for time in time_list:
        if time.startswith("월"):
            monday_time = time.split("\n")[1].split(" ")[1].strip()
            if "휴게시간" in time:
                lunch_break = time.split("휴게시간")[1].strip()
        elif time.startswith("화"):
            tuesday_time = time.split("\n")[1].split(" ")[1].strip()
        elif time.startswith("수"):
            wednesday_time = time.split("\n")[1].split(" ")[1].strip()
            if "휴게시간" in time:
                lunch_break = time.split("휴게시간")[1].strip()
        elif time.startswith("목"):
            thursday_time = time.split("\n")[1].split(" ")[1].strip()
        elif time.startswith("금"):
            friday_time = time.split("\n")[1].split(" ")[1].strip()
        elif time.startswith("토"):
            saturday_time = time.split("\n")[1].split(" ")[1].strip()
        elif time.startswith("일"):
            sunday_time = time.split("\n")[1].strip()
    
    # 데이터 리스트에 추가
    data_list.append([name, address, hospital_type, monday_time, tuesday_time, wednesday_time, thursday_time, friday_time, saturday_time, sunday_time, lunch_break, phone_number])

# 데이터프레임 생성
columns = ["이름", "병원주소", "병원종류", "월요일", "화요일", "수요일", "목요일", "금요일", "토요일", "일요일", "휴게시간", "전화번호"]
data = pd.DataFrame(data_list, columns=columns)

# 데이터프레임을 CSV 파일로 저장
data.to_csv('/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/modified.csv', index=False, encoding='utf-8-sig')
