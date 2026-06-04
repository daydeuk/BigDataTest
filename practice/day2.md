# 2일차 연습문제 — Pandas 기초 1

## 데이터 세팅

```python
import pandas as pd

data = {
    'name':   ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank'],
    'age':    [25, 30, None, 22, 35, 28],
    'score':  [88.5, 72.0, 91.0, None, 65.5, 80.0],
    'gender': ['F', 'M', 'M', 'M', 'F', 'M'],
    'pass':   [True, True, True, False, True, True]
}
df = pd.DataFrame(data)
```

---

## Q1. 데이터의 행 수와 열 수를 각각 출력하세요.

### 내 풀이 ✅
```python
print(df.shape[0])
print(df.shape[1])
```

---

## Q2. 각 컬럼의 자료형을 출력하되, age 컬럼의 자료형만 따로 한 번 더 출력하세요.

### 내 풀이 (수정 후) ✅
```python
for da in df:
    if da == 'age':
        print(da, df[da].dtype)
    print(da, df[da].dtype)
```

### 모범답안
```python
print(df.dtypes)          # 전체 컬럼 자료형
print(df['age'].dtype)    # age만 따로
```

> `for da in df` 에서 `da` 는 컬럼명(문자열)이므로 `da.dtype` 은 불가.
> `df[da].dtype` 으로 Series로 꺼낸 뒤 접근해야 함.

---

## Q3. 결측치가 있는 컬럼과 그 개수를 확인하세요.

### 내 풀이 ✅
```python
# info()로 확인 → age 1개 / score 1개

print(df.isnull().sum())          # 전체 출력

result = df.isnull().sum()
print(result[result > 0])         # 결측치 있는 컬럼만
```

---

## Q4. score 리스트에서 80점 이상인 값만 출력하세요.

### 내 풀이 ✅
```python
scores = [88.5, 72.0, 91.0, 65.5, 80.0]

for score in scores:
    if score >= 80:
        print(score)
```

---

## Q5. df를 result.csv로 저장하고 다시 불러와서 첫 3행을 출력하세요.

### 내 풀이 ✅
```python
df.to_csv('result.csv', index=False)
df = pd.read_csv('result.csv')
df.head(3)
```
