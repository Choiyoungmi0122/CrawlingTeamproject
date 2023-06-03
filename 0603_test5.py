import csv
import json
import pandas as pd

# JSON 파일 열기
with open('/Users/kim/Desktop/youngmi/json모아둠/강서구.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 변환된 데이터를 담을 리스트 생성
transformed_data = []

# 각 객체에 대해 변환 수행
for item in data['병원정보']:
    working_hours = item['영업시간']
    working_hours_dict = {}
    for working_hour in working_hours:
        day, hours = working_hour.split('\n', 1)
        working_hours_dict[day] = hours.strip()
    
    transformed_item = {
        'name': item['이름'],
        'address': item['병원주소'],
        'type': item['병원종류'],
        **working_hours_dict,
        'phone': item['전화번호']
    }
    transformed_data.append(transformed_item)

# CSV 파일로 저장
all_keys = set().union(*(item.keys() for item in transformed_data))
fieldnames = list(all_keys)

with open('/Users/kim/Desktop/youngmi/0603/강서구1.csv', 'w', encoding='utf-8-sig', newline='') as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(transformed_data)

# CSV 파일 읽기
file = pd.read_csv('/Users/kim/Desktop/youngmi/0603/강서구1.csv')

en_columns = ["name", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

re=pd.DataFrame()

re.columns = en_columns

# "Mon" 컬럼을 "work"와 "break"으로 분할
file[['work', 'break']] = file['Mon'].str.split('\n', expand=True, n=1)

# "work"와 "break" 컬럼만 선택하여 새로운 데이터프레임 생성
new_df = file[["name", "work", "break"]].copy()

# "break" 컬럼에서 "휴게시간"을 기준으로 분리하여 "break"과 "Submission_deadline" 컬럼으로 나누기
new_df["break"] = new_df["break"].str.split(" 휴게시간").str[0]
new_df["Submission_deadline"] = new_df["break"].str.split(" 휴게시간\n").str[-1]

# CSV 파일로 저장 (인코딩 설정 추가)
new_df.to_csv('/Users/kim/Desktop/youngmi/0603/강서구2.csv', index=False, encoding='utf-8-sig')




# file = re.copy()

# en_columns = ["name", "type", "address", "phone", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

# file.columns = en_columns

# print(file.head())