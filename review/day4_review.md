# 4일차 복습 — 결측치 처리 + 중복 제거

## 데이터 세팅

```python
import pandas as pd

data = {
    'city':     ['서울', '서울', '부산', '부산', '대구', None, '인천', '인천', '서울', '대구'],
    'category': ['전자', '의류', '전자', '식품', '의류', '전자', '식품', '의류', '전자', None],
    'sales':    [100, 80, 120, 60, 90, 110, 70, 85, 100, 95],
    'count':    [5, 3, None, 4, 6, 2, 3, None, 5, 4],
    'rating':   [4.2, 3.8, 4.5, 3.5, 4.0, 4.1, 3.7, 4.3, 4.2, 3.9]
}
df = pd.DataFrame(data)
```

---

## Q1. 결측치가 있는 컬럼과 개수만 출력하라.

### 내 풀이 ✅
```python
q1 = df.isnull().sum()
print(q1[q1 > 0])
```

> `isnull().sum()` 결과는 Series — 조건 필터로 결측 있는 컬럼만 뽑는다.
> 변수명을 짧게 쓰는 게 관례: `s = df.isnull().sum(); print(s[s > 0])`

---

## Q2. count 결측치를 count 평균으로 채운 뒤, count 전체 합계를 소수 둘째 자리까지 출력하라.

### 내 풀이 ✅
```python
q2 = df['count'].fillna(df['count'].mean())
print(round(q2.sum(), 2))
```

> `fillna(df['col'].mean())` — 평균 대체는 수치형에서 가장 많이 쓰이는 패턴.
> `round()` 빠뜨리지 않는 것이 핵심 (오답노트 항목).

---

## Q3. 완전히 같은 중복 행 개수를 출력하라. (첫 번째 등장 제외)

### 내 풀이 ✅
```python
print(df.duplicated().sum())
```

> `duplicated()` 기본값은 `keep='first'` — 첫 번째 등장은 자동으로 False 처리.
> `.sum()` 하면 "첫 번째 제외한 중복 수"가 나온다.

---

## Q4. 완전히 같은 중복 행을 제거하고(첫 번째 유지), city 결측 행을 제거한 뒤 city별 sales 합계를 내림차순 정렬했을 때 1위 city를 출력하라.

### 내 풀이 ✅
```python
q4 = df.drop_duplicates()
q4 = q4.dropna(subset=['city'])
print(q4.groupby('city')['sales'].sum().sort_values(ascending=False).index[0])
```

> `drop_duplicates()` 기본값이 `keep='first'`라 옵션 생략 가능.
> groupby 결과는 Series — `.index[0]`으로 바로 1위 city 이름 꺼낸다.
