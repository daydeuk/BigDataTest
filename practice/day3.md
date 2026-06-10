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

## Q1. 2번째 행(인덱스 1)의 name과 score 값을 .loc로 각각 출력하세요.

<details>
<summary>풀이 보기</summary>

### 내 풀이 ✅
```python
print(df.loc[1, 'name'])
print(df.loc[1, 'score'])
```

</details>

---

## Q2. .iloc로 마지막 행 전체를 출력하세요.

<details>
<summary>풀이 보기</summary>

### 내 풀이 ✅
```python
print(df.iloc[-1])
```

> `-1`은 마지막 위치. `.loc[-1]`은 라벨 -1이 없으면 에러 — 마지막 행은 `iloc[-1]` 이 안전.

</details>

---

## Q3. age가 30 이상인 사람의 name과 age만 출력하세요.

<details>
<summary>풀이 보기</summary>

### 내 풀이 ✅
```python
print(df[df['age'] >= 30][['name', 'age']])

# .loc로 한 번에 (더 간결)
print(df.loc[df['age'] >= 30, ['name', 'age']])
```

> `df.loc[조건, ['컬럼']]` 으로 필터링 + 컬럼 선택을 한 줄에 가능.

</details>

---

## Q4. gender가 'M' 이고 score가 70 이상인 사람의 전체 정보를 출력하세요.

<details>
<summary>풀이 보기</summary>

### 내 풀이 ✅
```python
q4 = df[(df['gender'] == 'M') & (df['score'] >= 70)]
print(q4)
```

> AND 조건은 `&`, OR 조건은 `|`. 각 조건은 반드시 `()`로 묶기. Python `and`/`or` 쓰면 에러.

</details>

---

## Q5. dept가 '개발' 이거나 age가 25 이하인 사람의 name, dept, age 컬럼만 출력하세요.

<details>
<summary>풀이 보기</summary>

### 내 풀이 ✅
```python
print(df.loc[(df['dept'] == '개발') | (df['age'] <= 25)][['name', 'dept', 'age']])
```

</details>
