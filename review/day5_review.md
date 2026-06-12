# 5일차 복습 — 그룹/집계 + 출력 패턴

## 데이터 세팅

```python
import pandas as pd

data = {
    'region':    ['서울', '서울', '부산', '부산', '대구', '대구', '인천', '인천', '광주', '광주',
                  '서울', '부산', '대구', '인천', '광주', '서울', '부산', '대구', '인천', '광주'],
    'category':  ['전자제품', '의류', '식품', '전자제품', '생활용품', '의류', '스포츠', '전자제품', '식품', '의류',
                  '스포츠', '생활용품', '전자제품', '의류', '스포츠', '식품', '전자제품', '의류', '생활용품', '스포츠'],
    'gender':    ['M', 'M', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'M',
                  'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F', 'M', 'F'],
    'age_group': ['30대', '20대', '40대', '30대', '50대', '20대', '10대', '30대', '40대', '20대',
                  '30대', '40대', '20대', '50대', '30대', '10대', '20대', '30대', '40대', '50대'],
    'sales':     [85000, 32000, 15000, 120000, 45000, 28000,  9000, 95000, 22000, 41000,
                  67000, 38000, 110000, 55000, 18000,  7000, 130000, 61000, 48000, 25000],
    'quantity':  [5, 3, 2, 8, 4, 2, 1, 6, 3, 4,
                  5, 3, 7, 5, 2, 1, 9, 4, 4, 2],
    'rating':    [4.2, 3.8, 4.0, 4.5, 3.5, 4.1, 3.9, 4.3, 3.7, 4.4,
                  4.6, 3.6, 4.8, 4.0, 3.8, 3.5, 4.7, 4.2, 3.9, 4.1]
}
df = pd.DataFrame(data)
```

---

## Q1. category별 sales 합계를 내림차순으로 정렬하여 출력하라. 합계가 가장 높은 category 이름을 출력하라.

### 내 풀이 ✅
```python
Q1 = df.groupby('category')['sales'].sum().sort_values(ascending=False)
print(Q1)
print(Q1.index[0])
```

> groupby 결과는 Series — 값만 필요하면 reset_index 없이 `.index[0]`으로 바로 꺼낸다.

---

## Q2. region별 sales 평균을 내림차순 정렬하여 출력하라. 소수 셋째 자리까지 반올림하라.

### 내 풀이 ✅
```python
Q2 = df.groupby('region')['sales'].mean().sort_values(ascending=False)
print(round(Q2, 3))
```

> `round(Series, n)` 과 `Series.round(n)` 둘 다 된다.

---

## Q3. gender 컬럼의 빈도를 출력하고, 빈도가 가장 높은 gender를 출력하라.

### 내 풀이 ✅
```python
Q3 = df.value_counts('gender')
print(Q3)
print(Q3.index[0])
```

> `df.value_counts('gender')` 와 `df['gender'].value_counts()` 둘 다 된다.
> `value_counts()`는 내림차순 정렬 → `.index[0]`이 최빈값.

---

## Q4. sales를 내림차순으로 정렬했을 때 3번째로 높은 sales 값을 출력하라.

### 내 풀이 ✅
```python
print(df['sales'].sort_values(ascending=False).reset_index(drop=True).iloc[2])
```

> Series에서는 `reset_index` 없이 `iloc`만 써도 된다.
> ```python
> print(df['sales'].sort_values(ascending=False).iloc[2])  # 더 간단
> ```
> DataFrame 정렬 후 N번째 행을 꺼낼 때는 `reset_index(drop=True)` 필요.

---

## Q5. category별 sales의 합계, 평균, 최댓값, 건수를 한번에 구하라. 컬럼명은 sum, mean, max, count로 지정하라.

### 내 풀이 ✅
```python
Q5 = df.groupby('category')['sales'].agg(['sum', 'mean', 'max', 'count'])
print(Q5)
```

> `agg(['sum', 'mean', 'max', 'count'])` 결과 컬럼명은 함수명 그대로 — 재지정 불필요.
> 컬럼명을 바꿀 때만: `result.columns = ['합계', '평균', '최대', '건수']`

---

## Q6. region별 sales 평균을 내림차순 정렬했을 때 2번째 region 이름을 출력하라.

### 내 풀이 ✅
```python
Q6 = df.groupby('region')['sales'].mean().sort_values(ascending=False).reset_index()
print(Q6.loc[1, 'region'])
```

> region **이름**을 꺼내야 하니 `reset_index()` (drop 없이) — region이 컬럼으로 내려온다.
> `drop=True` 쓰면 region이 사라지므로 주의.

---

## Q7. age_group이 '30대', '40대', '50대'인 행만 남긴 후, category별 quantity 합계를 구하라. 합계 내림차순으로 상위 2개 category 이름을 출력하라.

### 내 풀이 ✅
```python
Q7 = df[df['age_group'].isin(['30대', '40대', '50대'])]
print(Q7.groupby('category')['quantity'].sum().nlargest(2).index.tolist())
```

> `isin(리스트)` — OR 조건 여러 개를 깔끔하게 표현.
> `.index.tolist()` 또는 `list(.index)` 로 리스트 형태로 출력.

---

## Q8. age_group별 비율을 출력하라. 소수 넷째 자리까지 반올림하라.

### 내 풀이 ✅
```python
print(round(df.value_counts('age_group', normalize=True), 4))
```

> `normalize=True` → 비율(0~1) 반환. `value_counts()` 기본은 빈도(횟수).

---

## Q9. region × category 두 컬럼을 기준으로 sales 합계를 구하라. 합계가 가장 큰 (region, category) 조합의 region과 category를 각각 출력하라.

### 내 풀이 ✅
```python
result = df.groupby(['region', 'category'])['sales'].sum()
print(result.nlargest(1).index.tolist())

# 또는 idxmax로 각각 출력
idx = result.idxmax()
print(idx[0])  # region
print(idx[1])  # category
```

> 멀티 키 groupby는 `groupby(['col1', 'col2'])` — 리스트로 넣는다.
> `idxmax()` → 최댓값의 인덱스를 튜플로 반환.

---

## Q10. gender별 rating 평균 이상인 행만 남긴 후, category별 sales 중앙값을 내림차순 정렬했을 때 2번째 category를 출력하라.

### 내 풀이 ✅
```python
df[df['rating'] >= df.groupby('gender')['rating'].transform('mean')] \
  .groupby('category')['sales'].median() \
  .nlargest(2).index[1]
```

> `transform('mean')` — groupby 평균을 원본과 같은 길이(행별)로 반환 → 조건 필터에 사용 가능.
> `groupby().mean()`은 그룹당 1행 — 인덱스가 달라서 df['rating']과 직접 비교 불가.
