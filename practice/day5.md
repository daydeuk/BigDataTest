# 5일차 — 그룹/집계 + 출력 패턴

## 개념 정리

### 1. groupby + 기본 집계

```python
df.groupby('category')['sales'].sum()     # 합계
df.groupby('category')['sales'].mean()    # 평균
df.groupby('category')['sales'].count()   # 건수
df.groupby('category')['sales'].max()     # 최댓값
df.groupby('category')['sales'].min()     # 최솟값
df.groupby('category')['sales'].median()  # 중앙값
```

> `groupby` 결과는 Series. 인덱스가 그룹 키이므로 `.reset_index()`로 DataFrame으로 변환 가능.

---

### 2. groupby + agg — 여러 집계 한번에

```python
# 딕셔너리 형태 — 컬럼별 다른 집계
df.groupby('category').agg({'sales': ['sum', 'mean', 'count'], 'quantity': 'sum'})

# 리스트 형태 — 같은 컬럼에 여러 집계
df.groupby('category')['sales'].agg(['sum', 'mean', 'count', 'max'])
```

> 결과 컬럼이 MultiIndex가 될 수 있음 — `columns = ['sum', 'mean', 'count']` 로 재지정하거나 `reset_index()` 후 사용.

---

### 3. value_counts — 빈도 / 비율

```python
df['gender'].value_counts()              # 빈도 (내림차순)
df['gender'].value_counts(normalize=True)  # 비율 (합계 = 1.0)
df['age_group'].value_counts().index[0]   # 최빈값
```

> `normalize=True` 는 각 값의 비율을 반환. 시험 패턴: `round(..., 4)` 습관화.

---

### 4. sort_values — 정렬

```python
df.sort_values('sales', ascending=False)  # 내림차순 (기본은 오름차순)
df.sort_values(['region', 'sales'], ascending=[True, False])  # 다중 정렬
```

---

### 5. N번째 값 출력 패턴 ★★★

```python
# 패턴 A — reset_index + iloc (groupby 결과)
result = df.groupby('region')['sales'].mean().sort_values(ascending=False).reset_index()
print(result.iloc[1]['region'])   # 2번째 region (0-indexed)

# 패턴 B — 전체 DataFrame 정렬 후 iloc
df_sorted = df.sort_values('sales', ascending=False).reset_index(drop=True)
print(df_sorted.iloc[2]['sales'])  # 3번째 sales 값

# 패턴 C — nlargest / nsmallest
df['sales'].nlargest(3).iloc[-1]   # 3번째로 큰 값
```

> 시험에서 "N번째로 높은 값" 문제가 자주 나옴. `iloc[N-1]` (0-indexed) 을 헷갈리지 말 것.

---

### 6. groupby + transform — 그룹 평균과 비교

```python
# 각 행에 자기 그룹의 통계값을 붙여서 비교할 때
df['group_mean'] = df.groupby('gender')['rating'].transform('mean')
filtered = df[df['rating'] >= df['group_mean']]
```

> `transform`은 결과를 원본 DataFrame과 같은 인덱스로 반환 → 조건 필터링에 활용.

---

### 시험 빈출 패턴 정리

```python
# 패턴 1: groupby 후 N번째 항목
result = df.groupby('region')['sales'].sum().sort_values(ascending=False).reset_index()
print(result.iloc[0]['region'])       # 1위 region
print(result.iloc[1]['region'])       # 2위 region

# 패턴 2: 이중 groupby (멀티 인덱스)
result = df.groupby(['region', 'category'])['sales'].sum()
print(result.idxmax())               # 합계 최대인 (region, category) 튜플

# 패턴 3: 조건 필터 후 groupby
df_filtered = df[df['age_group'].isin(['30대', '40대', '50대'])]
result = df_filtered.groupby('category')['quantity'].sum().sort_values(ascending=False)
print(result.index[:2].tolist())      # 상위 2개 category

# 패턴 4: value_counts 비율
print(df['age_group'].value_counts(normalize=True).round(4))
```

---

## 연습문제

### 데이터 세팅

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

### Q1. category별 sales 합계를 내림차순으로 정렬하여 출력하라. 합계가 가장 높은 category 이름을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df.groupby('category')['sales'].sum().sort_values(ascending=False)
print(result)
print(result.index[0])  # 전자제품
```

> `groupby` 결과는 Series — `.index[0]` 으로 첫 번째 인덱스(그룹 키) 접근.

</details>

---

### Q2. region별 sales 평균을 내림차순 정렬하여 출력하라. 소수 셋째 자리까지 반올림하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df.groupby('region')['sales'].mean().sort_values(ascending=False).round(3)
print(result)
# 부산    75750.0
# 대구    61000.0
# 인천    51750.0
# 서울    47750.0
# 광주    26500.0
```

</details>

---

### Q3. gender 컬럼의 빈도를 출력하고, 빈도가 가장 높은 gender를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
vc = df['gender'].value_counts()
print(vc)
print(vc.index[0])  # M
```

> `value_counts()`는 내림차순 정렬 → `.index[0]` 이 최빈값.

</details>

---

### Q4. sales를 내림차순으로 정렬했을 때 3번째로 높은 sales 값을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
# 방법 A — sort_values + reset_index + iloc
df_sorted = df.sort_values('sales', ascending=False).reset_index(drop=True)
print(df_sorted.iloc[2]['sales'])  # 110000

# 방법 B — nlargest
print(df['sales'].nlargest(3).iloc[-1])  # 110000
```

> `iloc[2]`는 0-indexed → 3번째 행. `reset_index(drop=True)` 없으면 원본 인덱스가 유지됨 — 반드시 drop=True.

</details>

---

### Q5. category별 sales의 합계, 평균, 최댓값, 건수를 한번에 구하라. 컬럼명은 sum, mean, max, count로 지정하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df.groupby('category')['sales'].agg(['sum', 'mean', 'max', 'count'])
result.columns = ['sum', 'mean', 'max', 'count']
print(result)
```

> `agg(['sum', 'mean', 'max', 'count'])` 는 리스트를 받아 각 집계 함수를 컬럼으로 반환.
> `agg` 결과의 컬럼명은 함수명 그대로이므로 재지정 불필요하지만, 습관적으로 명시하면 안전.

</details>

---

### Q6. region별 sales 평균을 내림차순 정렬했을 때 2번째 region 이름을 출력하라. (`reset_index` + `iloc` 사용)

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df.groupby('region')['sales'].mean().sort_values(ascending=False).reset_index()
print(result.iloc[1]['region'])  # 대구
```

> `reset_index()` 를 호출해야 iloc로 행을 선택한 뒤 컬럼명으로 값을 꺼낼 수 있다.
> `reset_index()` 없이 `.index[1]` 만 써도 되지만, 두 컬럼 이상 필요할 때는 reset_index가 필수.

</details>

---

### Q7. age_group이 '30대', '40대', '50대'인 행만 남긴 후, category별 quantity 합계를 구하라. 합계 내림차순으로 상위 2개 category 이름을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
target = ['30대', '40대', '50대']
df_filtered = df[df['age_group'].isin(target)]

result = df_filtered.groupby('category')['quantity'].sum().sort_values(ascending=False)
print(result.index[:2].tolist())  # ['전자제품', '생활용품']
```

> `isin(리스트)` 로 여러 값 중 하나를 포함하는 조건. `OR` 조건을 `|` 여러 번 쓰는 것보다 깔끔.
> `.index[:2]` 는 상위 2개의 그룹 키(인덱스)만 슬라이싱.

</details>

---

### Q8. age_group별 비율을 출력하라. 소수 넷째 자리까지 반올림하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df['age_group'].value_counts(normalize=True).round(4)
print(result)
# 30대    0.3
# 20대    0.25
# 40대    0.2
# 50대    0.15
# 10대    0.1
```

> `normalize=True` 는 각 값의 비율(0~1)을 반환. `value_counts()`와 마찬가지로 내림차순 정렬.

</details>

---

### Q9. region × category 두 컬럼을 기준으로 sales 합계를 구하라. 합계가 가장 큰 (region, category) 조합의 region과 category를 각각 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = df.groupby(['region', 'category'])['sales'].sum().reset_index()
result = result.sort_values('sales', ascending=False)
print(result.iloc[0]['region'])    # 부산
print(result.iloc[0]['category'])  # 전자제품

# 방법 B — idxmax (튜플로 반환)
result2 = df.groupby(['region', 'category'])['sales'].sum()
print(result2.idxmax())  # ('부산', '전자제품')
```

> 멀티 키 `groupby`는 결과 인덱스가 MultiIndex → `reset_index()` 후 일반 컬럼처럼 접근 가능.

</details>

---

### Q10. gender별 rating 평균 이상인 행만 남긴 후, category별 sales 중앙값을 내림차순 정렬했을 때 2번째 category를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
# transform으로 각 행에 자기 gender 그룹의 rating 평균을 붙임
df['avg_rating'] = df.groupby('gender')['rating'].transform('mean')
filtered = df[df['rating'] >= df['avg_rating']]

result = filtered.groupby('category')['sales'].median().sort_values(ascending=False).reset_index()
print(result.iloc[1]['category'])  # 스포츠
```

> `transform('mean')` — groupby와 달리 원본 DataFrame과 같은 길이의 Series를 반환하므로 조건 필터에 바로 사용 가능.
> gender별 평균: M ≈ 4.108, F = 4.038 → 각 gender 기준으로 해당 rating 이상인 행만 통과.

</details>
