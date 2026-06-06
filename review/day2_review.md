# 2일차 복습 — Pandas 기초 1

## 데이터 세팅

```python
import pandas as pd

data = {
    'name':   ['Alice', 'Bob', 'Charlie', 'Dave', 'Eve', 'Frank'],
    'age':    [25, 30, None, 22, 35, 28],
    'score':  [88.5, 72.0, 91.0, None, 65.5, 80.0],
    'gender': ['F', 'M', 'M', 'M', 'F', 'M'],
    'dept':   ['영업', '개발', '개발', '영업', '인사', '인사']
}
df = pd.DataFrame(data)
df.to_csv('MyData.csv', index=False)
df = pd.read_csv('MyData.csv')
```

---

## Q1. 행 수와 열 수를 각각 출력하세요.

### 내 풀이 ✅
```python
print(df.shape[0])
print(df.shape[1])
```

---

## Q2. 전체 컬럼 자료형 출력 + score 컬럼 자료형만 따로 출력하세요.

### 내 풀이 ✅
```python
print(df.dtypes)
print(df['score'].dtype)
```

> `df.dtypes` (DataFrame) vs `df['score'].dtype` (Series) — s 유무 차이.
> `for data in df.dtypes` 로 iterate 하면 컬럼명 없이 dtype 값만 나옴 — 사용 금지.

---

## Q3. 결측치가 있는 컬럼과 그 개수만 출력하세요.

### 내 풀이 ✅
```python
missValue = df.isnull().sum()
print(missValue[missValue > 0])
```

> `df.isnull().sum()` 의 반환값은 **Series**. 조건 필터링으로 결측치 있는 컬럼만 출력 가능.

---

## Q4. 기초 통계를 문자열 컬럼까지 포함해서 출력하세요.

### 내 풀이 ✅
```python
print(df.describe(include='all'))
```

> Colab은 마지막 줄 자동 출력이지만 **시험 환경은 코드 에디터** — `print()` 필수.

---

## Q5. result.csv로 저장 후 다시 불러와서 첫 3행 출력하세요.

### 내 풀이 ✅
```python
df.to_csv('result.csv', index=False)
df = pd.read_csv('result.csv')
print(df.head(3))
```

> `index=False` 빠뜨리면 행 번호 컬럼이 생겨 감점. 반드시 습관화.
