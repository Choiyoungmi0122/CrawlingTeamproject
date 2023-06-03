import pandas as pd
import csv

data = pd.read_csv("/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/csv모아둠/강서구.csv", encoding='utf-8')

# 병원 종류별로 분류
grouped_data = data.groupby('병원종류')

# 분류된 데이터를 CSV 파일로 저장
for group_name, group_data in grouped_data:
    # 데이터를 CSV 파일로 저장
    group_data.to_csv('/Users/choiyoungmi/anaconda3/envs/bigdata/teamproject/csv모아둠/강서구.csv', encoding='utf-8-sig', index=False, mode='w')
