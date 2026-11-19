# 재도전 Day 2 풀이 — 문제는 retake/day2.md 참고
# 실행: .venv/bin/python workspace/day2.py   (프로젝트 폴더에서)
import pandas as pd
import numpy as np

# ---------------------------------------------------------------
# 개념 연습 (미니 데이터 t) — 다 쳐 봤으면 주석 처리해도 된다
# ---------------------------------------------------------------
t = pd.DataFrame({
    'name':  ['A', 'B', 'C', 'D', 'E', 'F'],
    'team':  ['red', 'blue', 'red', 'blue', 'red', 'green'],
    'score': [80, 90, 70, np.nan, 60, 85],
    'age':   [25, 32, 41, 28, 36, 30],
})

# 1. value_counts
print(t['team'].value_counts())
print(t['team'].value_counts(normalize=True))
print(t['team'].unique())
print(t['team'].nunique())

# 가장 많은 값의 이름
print(t['team'].value_counts().index[0]) # group by는 이름순이지만, value_counts는 데이터 순

# 가장 많은 값의 개수
print(t['team'].value_counts().iloc[0])

# 특정 값의 개수
print(t['team'].value_counts()['blue'])


# 특정 값의 비율
print(t['team'].value_counts(normalize=True)['red'])


# 2. groupby 기본
#print('-----2------')
# 특정 그룹 값 ['red']
#print(t.groupby('team')['score'].mean().loc['red'])
#print(t.groupby('team')['score'].mean().idxmax())
#print(t.groupby('team')['score'].mean().max())
#print(t.groupby('team')['score'].mean().sort_values(ascending=False).iloc[1])
#print(t.groupby('team')['score'].mean().sort_values(ascending=False).index[1])
# groupby 에서 자주 쓰는 함수
# mean() : 평균, sum() : 합계, max() : 최대값, idxmax() : 최대인덱스, min() : 최소값, idxmin() : 최소 인덱스
# median() : 중앙값, std() : 표준편차, size() : 행 수, count() : 결측이 아닌 행 수, nunique() : 고유값 수

# 3. size vs count
print('-----3------')
print(t.groupby('team').size()) # 행 수
print(t.groupby('team')['score'].count()) # score가 결측치가 아닌 행 수

# 4. agg
# aggregate? 여러 계산을 한번에.
print('-----4------')
# 방법1. 리스트로 - 컬럼 이름이 함수 이름이 된다.
print(t.groupby('team')['score'].agg(['mean', 'max', 'count']))
# 방법2. 이름=(컬럼, 함수) - 결과 컬럼 이름을 내가 정한다
a = t.groupby('team').agg(평균=('score', 'mean'), 인원=('name', 'size'))
#print(a[a['인원']>2])
print("*")
#print(a[a['인원']>=2]['평균'].idxmin())
print(a.loc['blue', '인원'])

# 5. transform
# 각 행에 "자기 그룹 값" 붙이기
# print('-----5------')
# print(t)
# print('*')
# t['team_mean'] = t.groupby('team')['age'].transform('mean')
# print(t[ t['age'] > t['team_mean']])

# 6. 두 컬럼 groupby + reset_index
print('-----6------')
t2 = t.copy()
t2['grade'] = ['x', 'x', 'y', 'y', 'y', 'x']
print(t2)
print(t2.groupby(['team', 'grade'])['age'].mean())
print(t2.groupby(['team', 'grade'])['age'].mean().reset_index())

# 7. 그룹별 상위 N
## 무조건 sorting 가장 먼저
print('-----7------')
print(t.sort_values('age', ascending=False).groupby('team').head(2))

# 8. 그룹별 최빈값 ***** 중요 까먹기 쉬움
#print(t.groupby('team')['score'].mode())
print(t.groupby('team')['score'].agg(lambda x: x.mode()[0]))

# ---------------------------------------------------------------
# 연습문제
# ---------------------------------------------------------------
df = pd.read_csv('retake/data/day2_orders.csv')

print('------------Q1------------')
# Q1. (기본) 주문 건수가 가장 많은 지역(region)의 이름과 건수를 출력하라.
print(df['region'].value_counts().idxmax())
print(df['region'].value_counts().max())
#print(df.groupby('region')['qty'].count())

# Q2. category별 price 평균이 가장 높은 분류의 이름과 평균(정수)
#print(df.groupby('category')['price'].mean())
print('------------Q2------------')
print(df.groupby('category')['price'].mean().idxmax())
print(int(df.groupby('category')['price'].mean().max()))

# Q3. (기본) 전체 주문 중 category가 '식품'인 주문의 비율을 소수 셋째 자리까지 반올림해 출력하라.
# *** 어려움 ***
print('------------Q3------------')
print(round(df['category'].value_counts(normalize=True)['식품'],3));

# Q4. (응용) price × qty로 주문 금액 컬럼 amount를 만들어라. 지역별 amount 합계를 구했을 때, 2번째로 큰 지역의 이름과 합계를 출력하라.
print('------------Q4------------')
df['amount'] = df['price'] * df['qty']
print(df.groupby('region')['amount'].sum().sort_values(ascending=False).index[1])
print(df.groupby('region')['amount'].sum().sort_values(ascending=False).iloc[1])

# Q5. 분류별로 주문 건수와 rating 평균을 구하라. 주문 건수가 10건 이상인 분류 중 rating 평균이 가장 낮은 분류의 이름을 출력하라.

print('------------Q5------------')
q5 = df.groupby('category').agg(qty_count =('qty', 'count'), rating_mean=('rating', 'mean'));
q5 = q5.sort_values('rating_mean', ascending=True).reset_index()
print(q5[q5['qty_count'] >= 10]['category'].iloc[0])

# Q6. 각 주문의 price가 자신이 속한 지역의 price 평균보다 큰 주문은 몇 건인가?
print('------------Q6------------')
df['price_mean'] = df.groupby('region')['price'].transform('mean')
print(len(df[df['price'] > df['price_mean']]))

# Q7. 회원 주문만 → 지역별 건수·rating 평균 → 건수 5건 이상 중 평균 가장 낮은 지역 이름과 평균(소수 둘째)
print('------------Q7------------')
q7 = df.copy()
q7 = q7[q7['member'] == 'Y']
q7= q7.groupby('region').agg(주문건수=('qty', 'count'), rating평균=('rating', 'mean'))
q7 = q7.sort_values('rating평균', ascending=False)
q7 = q7[q7['주문건수'] >= 5]
print(q7.index[-1])
print(round(q7.iloc[-1]['rating평균'], 2))
#print(q6[q6['주문건수'] >= 5].index[-1])
#print(q6[q6['주문건수'] >= 5].iloc[-1])


# Q8. 각 분류에서 amount 상위 2건씩 (총 8건) → amount 평균(정수)
print('------------Q8------------')
#print(df)
#print(df.sort_values('amount', ascending=False).groupby('category')['amount'].head(2))
print(int(df.sort_values('amount', ascending=False).groupby('category')['amount'].head(2).mean()))