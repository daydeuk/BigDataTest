# 1유형 최종 복습 — 문제는 retake/1유형_최종복습.md
# 실행: .venv/bin/python workspace/final_t1.py
# 채점: .venv/bin/python workspace/grade_t1.py   (세트마다 채점해도 됨)
# 시작 시각: __:__   (노트 보지 않기 — 막히면 문제지의 🆘 한 칸)
import pandas as pd
import numpy as np

raw = pd.read_csv('retake/data/final_t1/cafe_orders.csv')

# ===== Set A — 기초 체력 =====
# A1 (원본 raw) 중복 행 개수 / 중복 제거 후 행 수 → 이후 df 사용
print(raw.duplicated().sum())
df = raw.drop_duplicates().copy()
print(len(df))
# A2 결측치 있는 컬럼 이름 전부 (목록)
#print(df.info())
a2 = df.isnull().sum()
print(a2[a2>0].index.tolist())

# A3 menu 종류 수
print(len(df['menu'].value_counts().index.tolist()))

# A4 store에 '서울'이 들어간 주문 수
#print(df.head(50))
print(len(df[(df['store'].str.contains("서울"))])) # *** 그냥 df['store'].str.contains("서울") 했더니 320건 나와버리네

# A5 amount = price * qty → amount 상위 5건의 price 평균 (정수)
df['amount'] = df['price'] * df['qty']
#print(df.head())
print(int(df.sort_values('amount',ascending=False).head(5)['price'].mean()))

# A6 amount 3번째로 큰 주문의 order_id
print(df)
a6 = df.sort_values('amount', ascending=False).reset_index(drop=True).loc[2,'order_id'] # *** 어.. amount 순으로 정렬하려면 어떻게해야함?
# df.columns.get_loc
print(a6)

# A7 d7 = df.copy() → size 'L'의 price 500원 낮추기 → d7 price 평균 (소수 둘째) ⭐️⭐️⭐️⭐️
d7 = df.copy()
print(d7.head())
cond = d7['size'] == 'L'
d7.loc[cond, 'price'] = d7.loc[cond, 'price'] - 500
print(round(d7['price'].mean(),2))


# A8 d8 = df.copy() → coupon 결측 'N' → 'Y' 비율 (소수 셋째) ⭐️⭐️⭐️⭐️
d8 = df.copy()
d8['coupon'] = d8['coupon'].fillna('N')
print(round((d8['coupon']=='Y').mean(),3))


# ===== Set B — 집계 · 날짜 · 문자열 =====
# B1 지점별 amount 합계 2번째 지점 이름 / 합계

# 지점별 amount 합계
#print(df.head())
print(df.groupby('store')['amount'].sum().sort_values(ascending=False).index[1])
print(df.groupby('store')['amount'].sum().sort_values(ascending=False).iloc[1])

# B2 gmail 계정 주문 수 (대소문자 구분 없이)
b2 = df.copy()
b2['email'] = b2['email'].str.lower()
print(b2['email'].str.endswith('@gmail.com').sum())

# B3 order_dt 날짜 변환 → 가장 많은 월 / 건수
print(df.info())
df['order_dt'] = pd.to_datetime(df['order_dt'])
print(df['order_dt'].dt.month.value_counts().index[0])
print(df['order_dt'].dt.month.value_counts().iloc[0])

# B4 주말(토·일) amount 평균 (소수 둘째)
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['dayofweek'] = df['order_dt'].dt.dayofweek
print(round(df[(df['dayofweek']==5) | (df['dayofweek']==6)]['amount'].mean(),2))

# B5 자기 지점 price 평균보다 큰 주문 수
# transform 활용 문제
df['store_mean'] = df.groupby('store')['price'].transform('mean')
print(df[(df['price'] > df['store_mean'])].shape[0])

# B6 amount 구간 (10000 이하 소 / 30000 이하 중 / 초과 대) → '중' 건수
# help(pd.cut)
df['grade'] = pd.cut(df['amount'], bins=[0, 10000, 30000, np.inf], labels=['소', '중', '대'], right=True)
print(df[df['grade']=='중'].shape[0])

# B7 amount IQR 이상치 개수
# IQR = Q3 - Q1
# 이상치는 q1-(1.5*IQR) 보다 작거나, q3+(1.5 *IQR) 큰 경우
q1 = df['amount'].quantile(0.25)
#print(q1)
q3 = df['amount'].quantile(0.75)
#print(q3)
iqr = q3-q1
#print(iqr)
a_iqr = q1-(1.5*iqr) # *** 음수가 나오네? 음수가 나오면 안되는거 아닌가
b_iqr = q3+(1.5*iqr)
print(a_iqr, b_iqr)

print(len(df[(df['amount']<a_iqr) | (df['amount']>b_iqr)]))


# ===== Set C — 실전형 복합 =====
# C1 d14 = df.copy() → rating 결측을 category 평균으로 → 지점별 rating 평균 최고 지점 / 값 (소수 셋째)
d14 = df.iloc[:,:13].copy()
print(d14)
print(d14.info())
# ⭐️⭐️⭐️⭐️⭐️ 이거 어렵다
d14['cate_rating'] = d14.groupby('category')['rating'].transform('mean')
d14['rating'] = d14['rating'].fillna(d14['cate_rating'])
print(d14.groupby('store')['rating'].mean().sort_values(ascending=False).idxmax())
print(round(d14.groupby('store')['rating'].mean().sort_values(ascending=False).max(),3))

# C2 시/도별 VIP 비율 최저 시/도 / 비율 (소수 셋째)
# 시/도 정리
print('--C2--')
d14['is_vip'] = d14['member_grade']=='VIP'
d14['place'] = d14['store'].str.split(' ').str[0]
#print(d14)

print(d14.groupby('place')['is_vip'].mean().idxmin()) # ⭐️⭐️⭐️⭐️⭐️ cond로 True/False 열을 만들어놓고 mean()을 때리면 비율이 되는구나!!!
print(round(d14.groupby('place')['is_vip'].mean().min(),3))

#d15 = d14[['place', 'member_grade']].value_counts(normalize=True).reset_index() # ⭐️⭐️⭐️⭐️ normalize=True 기억 안나서 개념 찾아봤음.. 이거 까먹었네.
#d15 = d15.sort_values('proportion', ascending=False)
#d15 = d15[d15['member_grade'] =='VIP']
#print(d15.iloc[-1]['place'])
#print(round(d15.iloc[-1]['proportion'],3))

# C3 2024년 3월 amount 상위 10건 qty 평균 (정수)
c3 = df.copy()
print(int(c3[(c3['order_dt'].dt.year==2024) & (c3['order_dt'].dt.month==3)].sort_values('amount', ascending=False).head(10)['qty'].mean()))

# C4 |커피 평균 price − 디저트 평균 price| (정수)
c4 = df.copy()
print(c4.info())
a = c4[c4['category']=='커피']['price'].mean()
b = c4[c4['category']=='디저트']['price'].mean()
print(int(abs(a-b)))

# C5 지점별 amount 표준편차 최대 지점 / 값 (소수 둘째)
c5 = df.copy()
print(c5)
print(c5.groupby('store')['amount'].std().idxmax())
print(round(c5.groupby('store')['amount'].std().max(),2))

# ⭐️⭐️⭐️⭐️⭐️ 근데 문제중에 agg 사용하는 문제가 1개도 없네?
# agg 쓰는 방법 기억 안나는데, 몰라도 문제를 다 풀 수 있나?


# ---------------------------------------------------------------
# 답 적기 — 코드로 구한 변수를 넣는다 (손으로 옮겨 적지 않기)
# ---------------------------------------------------------------
answer = {
    'A1-a': 7, 'A1-b': 320, 'A2': ['coupon', 'rating'] #답 이렇게 적는게 맞나
    , 'A3': 7, 'A4': 132,
    'A5': 7260, 'A6': 'C0166', 'A7': 5653.12, 'A8': 0.394,
    'B1-a': '서울 강남점', 'B1-b': 837000, 'B2': 124, 'B3-a': 3, 'B3-b': 94,
    'B4': 12751.85, 'B5': 161, 'B6': 174, 'B7': 2,
    'C1-a': '서울 강남점', 'C1-b': 3.051, 'C2-a': '대전', 'C2-b': 0.0,
    'C3': 4, 'C4': 276, 'C5-a': '경기 수원점', 'C5-b': 8934.44,
}
