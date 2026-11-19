# Day 1 복습 — isin 연습문제 (문제는 retake/복습_day1.md ⑥)
# 실행: .venv/bin/python workspace/day1_isin.py   (프로젝트 폴더에서)
import pandas as pd

df = pd.read_csv('retake/data/day1_employees.csv')
d = df.drop_duplicates()   # I4~I6에서 사용

# I1. 원본: city가 서울·부산·대구 중 하나인 직원 수
print("Q1")
print(df['city'].isin(['서울', '부산', '대구']).sum())
# I2. 원본: dept가 '개발'도 '영업'도 아닌 직원 수
print("Q2")
print(len(df[~df['dept'].isin(['개발','영업'])]))

# I3. 원본: city가 서울도 부산도 아닌 직원 수 (도시가 비어 있는 직원 제외)
df = pd.read_csv('retake/data/day1_employees.csv')
df = df.dropna(subset=['city'])
print("Q3")
print(len(df[(df['city'] != '서울') & (df['city'] != '부산')]));

# I4. 중복 제거: city 서울 또는 부산 & 나이 30세 이상 → salary 평균 (소수 둘째)
df = pd.read_csv('retake/data/day1_employees.csv')
df = df.drop_duplicates()
print("Q4")
print(round(df[(df['city'].isin(['서울', '부산'])) & (df['age'] >= 30)]['salary'].mean(),2))

# I5. 중복 제거: id가 E003, E007, E012인 직원의 salary 합계 (정수)
df = pd.read_csv('retake/data/day1_employees.csv')
df = df.drop_duplicates()
print("Q5")
print(int(df[df['id'].isin(['E003', 'E007', 'E012'])]['salary'].sum()))

# I6. 중복 제거: dept 개발 또는 인사 & 성별 F → score 가장 높은 직원의 id
df = pd.read_csv('retake/data/day1_employees.csv')
df = df.drop_duplicates()
df = df[(df['dept'].isin(['개발', '인사'])) & (df['gender']=='F')].sort_values('score', ascending=False).reset_index(drop=True);
print("Q6")
print(df.loc[0, 'id'])