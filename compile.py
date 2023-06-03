import json
import csv

# JSON 파일 열기
with open('/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/json모아둠/강서구.json', 'r', encoding='utf-8') as json_file:
    data = json.load(json_file)

# CSV 파일 열기
with open('/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/csv모아둠/강서구.csv', 'w', newline='', encoding='utf-8-sig') as csv_file:
    writer = csv.writer(csv_file)

    # 헤더 쓰기
    header = ['이름', '병원종류', '병원주소', '영업시간', '전화번호']  # 헤더를 직접 정의합니다.
    writer.writerow(header)

    # 데이터 쓰기
    for item in data['병원정보']:
        # 영업시간
        영업시간 = []
        for time in item['영업시간']:
            day, operating_time = time.split('\n', 1)
            영업시간.append(f"{day} {operating_time.strip()}")

        # 전화번호
        전화번호 = item['전화번호']
        
        # 병원주소
        병원주소 = item['병원주소']
        주소_영업시간 = 병원주소 + '\n' + '\n'.join(영업시간)

        # CSV 행으로 작성
        row = [item['이름'], item['병원종류'], 주소_영업시간, 전화번호]
        writer.writerow(row)

print("JSON 파일을 CSV 파일로 변환하였습니다.")
