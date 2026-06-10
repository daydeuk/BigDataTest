# 3일차 연습문제 — Pandas 기초 2

## 데이터 세팅

```python
import pandas as pd

data = {
    'name':   ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank'],
    'age':    [25, 30, 35, 22, 28, 40],
    'score':  [88.5, 72.0, 91.0, 65.5, 80.0, 55.0],
    'gender': ['F', 'M', 'M', 'M', 'F', 'M'],
    'dept':   ['영업', '개발', '개발', '영업', '인사', '인사']
}
df = pd.DataFrame(data)
```

---

## Q1. .iloc로 3번째 행(Charlie)의 score 값만 출력하세요.

### 내 풀이 ✅
```python
df.iloc[2, 2]
```

---

## Q2. .loc로 인덱스 0~2행의 name, dept 컬럼만 출력하세요.

### 내 풀이 ✅
```python
df.loc[0:2, ['name', 'dept']]
```

> `.loc` 슬라이싱은 끝 인덱스 **포함** — `0:2` 는 0, 1, 2행 모두 반환.

---

## Q3. score가 70 미만인 사람의 name과 score를 출력하세요.

### 내 풀이 ✅
```python
df.loc[df['score'] < 70, ['name', 'score']]
```

---

## Q4. dept가 '개발'이고 age가 30 이상인 사람의 전체 정보를 출력하세요.

### 내 풀이 ✅
```python
df.loc[(df['age'] >= 30) & (df['dept'] == '개발')]
```

> AND 조건은 `&`, OR 조건은 `|`. 각 조건은 반드시 `()`로 묶기. Python `and`/`or` 쓰면 에러.

---

## Q5. gender가 'F'이거나 score가 85 이상인 사람의 name, gender, score만 출력하세요.

### 내 풀이 ✅
```python
df.loc[(df['gender'] == 'F') | (df['score'] >= 85)][['name', 'gender', 'score']]
```

> `.loc[조건, 컬럼리스트]` 형태로 한 줄에 쓸 수도 있다.
> ```python
> df.loc[(df['gender'] == 'F') | (df['score'] >= 85), ['name', 'gender', 'score']]
> ```
