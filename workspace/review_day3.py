# Day 3 복습 셀프 퀴즈 — 문제는 retake/복습_day3.md "4. 셀프 퀴즈"
# 실행: .venv/bin/python workspace/review_day3.py   (프로젝트 폴더에서)
import pandas as pd
import numpy as np

df = pd.read_csv('retake/data/day3_delivery.csv')

# split
# df.str.split('-).str[1]

# dt.dayofweek / dt.day_name()

# R1. naver 계정(대소문자 구분 없이) 주문 수
print('--- R1 ---')
print(df)
df['email'] = df['email'].str.lower()
print(df['email'].str.endswith('@naver.com').sum())

# R2. 일요일 주문의 amount 평균 (소수 둘째)
print('--- R2 ---')
# print(df.info())
df['order_dt'] = pd.to_datetime(df['order_dt'])
# print(df.info())
df['dayofweek'] = df['order_dt'].dt.dayofweek
r2 = df[df['dayofweek']==6]
print(round(r2['amount'].mean(),2))

# R3. deliver_min 30분 미만 '정시' / 30분 이상 '지연' (pd.cut, right 주의) → '지연' 건수
print('--- R3 ---')
df['grade'] = pd.cut(df['deliver_min'], bins=[0, 30, np.inf], labels=['정시', '지연'], right=False)
print(len(df[df['grade']=='지연']))

# R4. amount의 IQR 방식 이상치 개수
print('--- R4 ---')
#print(df)
q1 = df['amount'].quantile(0.25)
q3 = df['amount'].quantile(0.75)
iqr = q3-q1
print(len(df[(df['amount'] < (q1-1.5*iqr)) | (df['amount'] > (q3 + 1.5*iqr))]))


# R5. 시/도별 주말 주문 비율이 가장 높은 시/도 이름과 비율 (소수 셋째)
print('--- R5 ---')
# print(df)
df['city'] = df['address'].str.split(' ').str[0]

# 분모
r5_2=df.groupby('city')['dayofweek'].count();

# 분자
df['is_weekend'] = df['dayofweek'] >= 5
print(df.groupby('city')['is_weekend'].mean())
#r5_1 = df[df['dayofweek'] >= 5].groupby('city')['dayofweek'].count()
#print(r5_2)
#print(r5_1)

#r = r5_1 / r5_2
#print(r.idxmax(), round(r.max(), 3))

#print(df[['city', 'dayofweek']].value_counts(normalize=True))