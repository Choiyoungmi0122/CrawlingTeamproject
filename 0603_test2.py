import json

# JSON 파일 열기
with open('/Users/kim/Desktop/youngmi/json모아둠/강서구.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# 이름을 출력합니다.
name = data['병원정보'][1]['영업시간']

eng_columns = ["name", "address", "type", "address", "phone"]

data.columns = eng_columns

