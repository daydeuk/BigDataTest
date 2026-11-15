# 재도전 Day 1 풀이 — 문제는 retake/day1.md 참고
# 실행: .venv/bin/python workspace/day1.py   (프로젝트 폴더에서)
import pandas as pd

df = pd.read_csv('retake/data/day1_employees.csv')

# 1. 데이터 불러오기와 훑어보기
#print(df.head())
#print(df.shape)
#print(df.info())
#print(df.describe())
#print(df.columns)

# 2. 컬럼 선택
#print(df['salary'])
#print(df[['dept', 'salary']])

# 3. 조건 필터 ⭐ 1유형의 기본기
#print(df[df['age'] >= 30])
#print(df[ (df['dept'] == '개발') & (df['age'] >= 30) ])
#print(df[ (df['city'] =='서울') | (df['city'] == '부산') ])
#print( df[ df['city'].isin(['서울', '부산']) ])
#print(df[ ~df['city'].isin(['서울', '부산']) ])
# 판다스에서는 and or 를 사용할 수 없다. 반드시 & 나 | 를 사용해야한다.
# 조건마다 괄호는 필수이다.
# 같다는 == (등호 두개)

# 4. loc / iloc
#print(df)
#print(df.iloc[0]) # 0번째 행 (위치 기준, 0부터 센다.)
#print(df.iloc[0:3]) # 0, 1, 2번째 행 (끝번호 3은 포함 안 됨)
#print(df.iloc[2]['salary']) # 3번째 행의 salary
#print(df.loc[df['age'] >= 30, 'salary']) # 조건으로 행 고르고 + 컬럼 고르기
#iloc는 숫자, loc는 조건 * reset_index(drop=True) 반드시 활용 *

# 5. 정렬과 N번째 값 꺼내기 * 시험 단골 *
#print(df)
#print(df.sort_values('salary')) # 오름차순
#print(df.sort_values('salary', ascending=False)) # 내림차순
# 'salary'가 3번째로 높은 사람의 age
#s = df.sort_values('salary', ascending=False).reset_index(drop=True)
#print(s.iloc[2]['age'])
# 상위 N개
#print(df.sort_values('salary', ascending=False).head(5))

# 6. 결측치
#print(df.isnull().sum()) # 컬럼별 결측치 개수
#print(df.isnull().sum().idxmax()) # 결측치가 가장 많은 컬럼 이름
#print(df['salary'].isnull().sum())

# 결측치 행 삭제 : dropna * DataFrame 단위
#print(df.dropna().reset_index(drop=True)) # 결측치가 하나라도 있는 행 삭제
#print(df.dropna(subset=['salary']).reset_index(drop=True)) # salary가 결측치인 행만 삭제

# 결측치 행 채우기 : fillna * Series 단위
# 평균으로 채우기
    #print(df['salary'].mean())
    #df['salary'] = df['salary'].fillna(df['salary'].mean());
    #print(df)
# 중앙값으로 채우기
    #print(df['salary'].median())
    #df['salary'] = df['salary'].fillna(df['salary'].median());
    #print(df)
# 문자로 채우기
    #df['salary'] = df['salary'].fillna('없음')
    #print(df)
# 재할당 필수! df.dropna()만 쓰면 원본은 그대로다.
# df = df.dropna() 로 다시 담아야한다.

# 7. 중복
# 완전히 똑같은 행의 개수 (첫 번째는 빼고 센다.)
#print(df.duplicated().sum())
#print(df)
# 중복 행 제거 (첫 번째만 남김)
#df = df.drop_duplicates()   
#print(df)
#df = df.drop_duplicates(subset=['id']) # id가 같으면 중복으로 보고 제거
#print(df)

# 8. 출력 패턴 - 답을 정확하게 내는 법
# 행 개수
#print(len(df))
# 소수 둘째자리에서 반올림 - 괄호 주의 !!!
#print(round(df['salary'], 2))
# 정수로 (소수점 버림)
#print(int(df.loc[0]['salary']))
# 아래 모두 결측치(NaN) 값은 제외하고 계산
#df['salary'].mean() # 평균
#df['salary'].sum() # 합계
#df['salary'].max() # 최댓값
#df['salary'].min() # 최솟값
#df['salary'].median() # 중앙값 ()

#print(df['salary'].idxmax()) # 최댓값이 있는 행의 인덱스
#print(df.loc[df['salary'].idxmax(), 'id']) # 그래서 꺼낼 때는 iloc는 아니라 loc


print('--- Q1 ---')
# 행 수와 열 수
print(len(df))
print(df.shape[1])

print('--- Q2 ---')
# 결측치가 가장 많은 컬럼의 이름
print(df.isnull().sum().idxmax())

print('--- Q3 ---')
# 중복 행 개수 + 중복 제거 후 행 수
print(df.duplicated().sum())
print(len(df.drop_duplicates()))
# duplictaed(), drop_duplicates() 함수 이름 생각이 잘 안났음.

print('--- Q4 ---')
# 중복 제거 후, dept == '개발' 이고 age >= 30 인 직원 수
df4 = df.drop_duplicates().copy()
print(len(df4[(df4['dept']=='개발') & (df4['age'] >= 30)]))# *** loc로는 어떻게 풀어야할지 모르겠음.

print('--- Q5 ---')
# 중복 제거 후, salary 결측치를 중앙값으로 채우고 salary 평균 (소수 둘째 자리)
df5 = df.drop_duplicates().copy()
df5['salary'] = df5['salary'].fillna(df5['salary'].median())
print(round(df5['salary'].mean(), 2))

print('--- Q6 ---')
# 중복 제거 후, score 결측 행 삭제 → score 상위 5명의 salary 평균 (정수)
df6 = df.drop_duplicates().copy()
df6 = df6.dropna(subset=['score']).sort_values('score', ascending=False).reset_index(drop=True)
print(int(df6['salary'].head(5).mean()))

print('--- Q7 ---')
# 중복 제거 후, city가 서울/부산 이고 gender == 'F' 중 salary 최고인 직원의 id
df7 = df.drop_duplicates()
print(df7.loc[df7[((df7['city'] == '서울') | (df7['city'] == '부산')) & (df7['gender']== 'F')]['salary'].idxmax(), 'id'])

print('--- Q8 ---')
# 중복 제거 → salary 결측 행 삭제 → 나이 많은 순 정렬 → 3번째 직원의 salary
df8 = df.drop_duplicates().copy()
df8 = df8.dropna(subset=['salary'])
df8 = df8.sort_values('age', ascending=False).reset_index(drop=True)
print(df8.loc[2, 'salary'])