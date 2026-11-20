# 재도전 Day 3 풀이 — 문제는 retake/day3.md 참고
# 실행: .venv/bin/python workspace/day3.py   (프로젝트 폴더에서)
import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# 개념 연습 (미니 데이터 t) — 다 쳐 봤으면 주석 처리해도 된다
# ---------------------------------------------------------------
t = pd.DataFrame({
    'name':  ['Kim Minsu', 'lee jihye', 'PARK Sora', 'choi Dan'],
    'dt':    ['2024-03-02 09:30', '2024-03-15 18:05', '2024-04-06 21:40', '2024-05-20 13:00'],
    'join':  ['2024-02-25', '2024-01-10', '2024-04-06', '2024-03-01'],
    'phone': ['010-1234-5678', '010-9876-5432', '011-2222-3333', '010-5555-0000'],
    'score': [55, 72, 90, 30],
})

# t['dt'] = pd.to_datetime(t['dt'])
# t['join'] = pd.to_datetime(t['join'])
# x = t['dt']
# print(x.dt.dayofweek)
# print(x.dt.day_name())

# #str
# s = t['name']
# print(s)
# # 소문자
# print(s.str.lower())
# # 대문자
# print(s.str.upper())
# # 글자 수
# print(s.str.len())
# # 앞 3글자 (슬라이싱)
# print(s.str[:3])
# # 'kim'이 들어있나
# print(s.str.contains('kim'))
# # ~로 시작하나
# print(s.str.startswith('~'))
# # ~로 끝나나
# print(s.str.endswith('~'))
# # 바꾸기
# print(s.str.replace(' ','-'))
# # 쪼개기 -> 목록
# print(s.str.split(' '))
# # 쪼갠 것 중 2번째 조각
# print(s.str.split(' ').str[1])

# # 5. 파생컬럼 - np.where (조건에 따라 2가지 값)
# t['pass'] = np.where(t['score']>= 60, '합격', '불합격')

# # 6. 파생컬럼 pd.cut (경계값에 따라 어디로 갈지 정하는 함수)
# t['grade'] = pd.cut(t['score'], bins=[0,40,70,100], labels=['C','B','A'])
# print(t)
# t['grade'] = pd.cut(t['score'], bins=[0, 30, 60, np.inf], labels=['C','B','U'], right=True)
# print(t)

#7. quantile(사분위수), 표준편차
# sc = t['score']
# # 1사분위수 (하위 25%)
# print(sc.quantile(0.25))
# # 2사분위수 (중앙값)
# print(sc.quantile(0.50))
# # 3사분위수 (상위 25%)
# print(sc.quantile(0.75))
# # 표준편차
# print(sc.std())
# # 위 값들 한번에
# print(sc.describe())

# 1. pd.to_datetime

# 2. .dt.year / month / day / hour / dayofweek / day_name()

# 3. 두 날짜의 차이 → .dt.days

# 4. 문자열 .str.lower / contains / split / str[N]

# 5. np.where

# 6. pd.cut (경계값 확인)

# 7. quantile / std / describe


# ---------------------------------------------------------------
# 연습문제
# ---------------------------------------------------------------
df = pd.read_csv('retake/data/day3_delivery.csv')

# Q1. 주문이 가장 많은 월과 건수
#print(df.info())
print('---------Q1---------')
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['order_month'] = df['order_dt'].dt.month
#print(df)
print(df.value_counts('order_month').index[0])
print(df.value_counts('order_month').iloc[0])

# Q2. 주말(토·일) 주문 건수
print('---------Q2---------')
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['dayofweek'] = df['order_dt'].dt.dayofweek
q2=df[(df['dayofweek']==5) | (df['dayofweek']==6)]
print(len(q2))

# Q3. gmail 계정 주문 수 (대소문자 구분 없이)
print('---------Q3---------')
# *** 대소문자 구분 없이 하려면 일단 그냥 .lower() 로 소문자로 만들어서 비교하는게 국룰??
df['lower_eamil'] = df['email'].str.lower()
print(df['lower_eamil'].str.endswith('@gmail.com').sum()) # *** True/False는 sum()으로 세자.

# Q4. address 첫 단어(시/도) 중 주문이 가장 많은 시/도 이름
print('---------Q4---------')
df['city'] = df['address'].str.split(' ').str[0]
print(df['city'].value_counts().idxmax())

# Q5. 가입~주문 일수 30일 이내 '신규' / 아니면 '기존' → type 컬럼 → '신규' amount 평균 (소수 둘째)
print('---------Q5---------')
#print(df.info())
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['signup_date'] = pd.to_datetime(df['signup_date'])
#print(df['order_dt'].dt.days)
diff = df['order_dt'] - df['signup_date']
df['diff'] = diff.dt.days
df['type'] = np.where(df['diff']<=30, '신규', '기존')
print(round(df.groupby('type')['amount'].mean().loc['신규'], 2))

# Q6. deliver_min 구간: 30 이하 빠름 / 30 초과 60 이하 보통 / 60 초과 느림 → '빠름' 건수
print('---------Q6---------')
df['speed'] = pd.cut(df['deliver_min'], bins=[0, 30, 60, np.inf], labels=['빠름', '보통', '느림'])
print(df['speed'].value_counts().loc['빠름'])

# Q7. amount 1사분위수, 3사분위수, IQR
print('---------Q7---------')
print(df['amount'].describe())
q1 = df['amount'].quantile(0.25)
q3 = df['amount'].quantile(0.75)
iqr = q3-q1
print(q1, q3, iqr)

# Q8. 18시~21시대 주문만 → 시/도별 amount 표준편차 가장 큰 시/도 이름과 값 (소수 둘째)
print('---------Q8---------')
#print(df)
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['order_hour'] = df['order_dt'].dt.hour
q8 = df[(df['order_hour']>=18) & (df['order_hour']<=21)]
print(q8.groupby('city')['amount'].std().sort_values(ascending=False).index[0])
print(round(q8.groupby('city')['amount'].std().sort_values(ascending=False).iloc[0],2))