import pandas as pd

# CSV 파일 읽기
file = pd.read_csv('/Users/kim/Desktop/youngmi/0603/강서구1.csv')

# 요일 컬럼 이름 생성
days = ["월", "화", "수", "목", "금", "토", "일"]

# 필요한 컬럼 선택
columns_to_keep = ["name", "type", "phone", "address", "월", "화", "수", "목", "금", "토", "일"]
file = file[columns_to_keep]

# "Mon" 컬럼을 "work"와 "break"으로 분할
file[['work', 'break']] = file['월'].str.split('\n', expand=True, n=1)
print(file)

# CSV 파일로 저장
file.to_csv('/Users/kim/Desktop/youngmi/0603/강서구workbreak.csv', index=False, encoding='UTF-8')