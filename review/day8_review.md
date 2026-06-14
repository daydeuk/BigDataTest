# 8일차 복습 — 파생 컬럼 + 피벗 + 상관계수

## 데이터 세팅

```python
import pandas as pd
import numpy as np

data = {
    'name':   ['김민준', '이서연', '박지호', '최유진', '정승현',
               '강민서', '윤지원', '장하은', '임도현', '한소율'],
    'age':    [22, 35, 28, 45, 19, 52, 31, 27, 41, 38],
    'gender': ['M', 'F', 'M', 'F', 'M', 'F', 'F', 'M', 'M', 'F'],
    'score':  [88, 72, 95, 61, 45, 83, 77, 90, 55, 68],
    'salary': [3200, 4500, 3800, 5200, 2800, 6100, 4200, 3600, 4800, 4100],
    'dept':   ['개발', '마케팅', '개발', '인사', '개발',
               '마케팅', '인사', '개발', '마케팅', '인사']
}
df = pd.DataFrame(data)
```

---

## Q1. score가 90 이상이면 'A', 70 이상이면 'B', 미만이면 'C'인 `grade` 컬럼을 추가하라. grade별 인원수를 출력하라.

### 내 풀이 ✅
```python
df['grade'] = np.where(df['score'] >= 90, 'A',
              np.where(df['score'] >= 70, 'B', 'C'))
print(df.groupby('grade')['grade'].count())
```

> 중첩 np.where: "90 이상이면 A, 아니면 (70 이상이면 B, 아니면 C)"

---

## Q2. age를 기준으로 `bins=[0,30,40,60]`, `labels=['청년','중년','장년']`으로 구간을 나눠 `age_group` 컬럼을 추가하라. age_group별 salary 평균을 출력하라.

### 내 풀이 ✅
```python
df['age_group'] = pd.cut(df['age'], bins=[0, 30, 40, 60], labels=['청년', '중년', '장년'])
print(df.groupby('age_group', observed=True)['salary'].mean())
```

> `observed=True` — FutureWarning 제거. 데이터 없는 그룹은 출력 안 함.

---

## Q3. gender 컬럼의 'M'→'남성', 'F'→'여성'으로 변환한 `gender_kor` 컬럼을 추가하라.

### 내 풀이 ✅
```python
mapping = {'M': '남성', 'F': '여성'}
df['gender_kor'] = df['gender'].map(mapping)
print(df['gender_kor'])
```

---

## Q4. score가 60 이상이면 '합격', 미만이면 '불합격'인 `result` 컬럼을 추가하라. 합격자의 salary 평균을 소수 둘째 자리까지 출력하라.

### 내 풀이 ✅
```python
df['result'] = np.where(df['score'] >= 60, '합격', '불합격')
print(round(df[df['result'] == '합격']['salary'].mean(), 2))
```

---

## Q5. `apply`와 람다를 사용해 salary를 만 단위로 변환한 `salary_man` 컬럼을 추가하라.

### 내 풀이 ✅
```python
df['salary_man'] = df['salary'].apply(lambda x: x / 10000)
print(df['salary_man'])
```

> `lambda x: x / 10000` — x를 받아서 x/10000 반환. 간단한 함수를 한 줄로 표현.

---

## Q6. dept × gender 기준으로 salary 평균을 피벗 테이블로 출력하라.

### 내 풀이 ✅
```python
print(pd.pivot_table(df, values='salary', index='dept', columns='gender', aggfunc='mean'))
```

> `A × B` → `index=A`, `columns=B`
> `columns` 파라미터명 주의 — `category` 아님.

---

## Q7. score와 salary의 상관계수를 소수 셋째 자리까지 출력하라.

### 내 풀이 ✅
```python
print(round(df['score'].corr(df['salary']), 3))
```

---

## Q8. 전체 수치 컬럼 간 상관계수 행렬을 출력하라. age와 salary의 상관계수만 따로 출력하라.

### 내 풀이 ✅
```python
print(df.corr(numeric_only=True))
print(df['age'].corr(df['salary']))
```

> `df.corr()` 단독 사용 시 에러 → `numeric_only=True` 필수.
> `df = df.select_dtypes(include='number')` 로 원본 덮어쓰면 이후 문자열 컬럼 사라짐 — 주의.
