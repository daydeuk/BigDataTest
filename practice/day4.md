# 4일차 — 결측치 처리 + 중복 제거

## 개념 정리

### 1. 결측치 확인

```python
df.isnull()              # 각 셀이 결측이면 True
df.isnull().sum()        # 컬럼별 결측치 개수
df.isnull().sum().sum()  # 전체 결측치 개수

# 결측치 있는 컬럼만 출력
s = df.isnull().sum()
print(s[s > 0])
```

> `df.notnull()` 은 반대 — `isnull()` 에 `~` 붙여도 같다: `df[~df['age'].isnull()]`

---

### 2. 결측치 제거 — `dropna()`

```python
df.dropna()                          # 결측치 있는 행 전부 제거
df.dropna(subset=['age'])            # age 컬럼이 결측인 행만 제거
df.dropna(subset=['age', 'score'])   # 둘 중 하나라도 결측이면 제거
df.dropna(axis=1)                    # 결측치 있는 열 제거
```

> `inplace=True` 없으면 원본이 안 바뀜 → `df = df.dropna()` 패턴이 안전

---

### 3. 결측치 대체 — `fillna()`

```python
df['age'].fillna(0)                        # 특정 값으로
df['age'].fillna(df['age'].mean())         # 평균으로
df['age'].fillna(df['age'].median())       # 중앙값으로
df['grade'].fillna(df['grade'].mode()[0])  # 최빈값으로 (범주형)
df['score'].fillna(method='ffill')         # 앞 행 값으로 (forward fill)
df['score'].fillna(method='bfill')         # 뒷 행 값으로 (backward fill)
```

> 수치형 → 평균/중앙값, 범주형(문자) → 최빈값(`mode()[0]`)이 일반적
> `mode()` 는 Series를 반환하므로 `[0]` 으로 첫 번째 값만 꺼내야 함

---

### 4. 중복 확인 — `duplicated()`

```python
df.duplicated()                       # 중복 행이면 True (첫 번째 등장은 False)
df.duplicated().sum()                 # 중복 행 개수

# 특정 컬럼 기준 중복 확인
df.duplicated(subset=['name'])
df.duplicated(subset=['date', 'id'])  # 두 컬럼 조합 기준

# keep 옵션
df.duplicated(keep='first')   # 기본값 — 첫 번째 제외 나머지를 True
df.duplicated(keep='last')    # 마지막 제외 나머지를 True
df.duplicated(keep=False)     # 중복된 행 전부 True
```

---

### 5. 중복 제거 — `drop_duplicates()`

```python
df.drop_duplicates()                       # 완전히 같은 행 제거
df.drop_duplicates(subset=['name'])        # name 기준 중복 제거
df.drop_duplicates(subset=['date', 'id'])  # 두 컬럼 조합 기준

# keep 옵션
df.drop_duplicates(keep='first')  # 기본값 — 첫 번째만 남김
df.drop_duplicates(keep='last')   # 마지막만 남김
df.drop_duplicates(keep=False)    # 중복된 행 전부 제거
```

> **시험 패턴**: "같은 날짜에 중복 기록이 있으면 첫 번째만 사용하라"
> → `df.drop_duplicates(subset=['date'], keep='first')`

---

### 시험 빈출 패턴 정리

```python
# 패턴 1: 결측치 있는 컬럼만 골라서 평균으로 채우기
for col in df.columns:
    if df[col].isnull().sum() > 0:
        df[col] = df[col].fillna(df[col].mean())

# 패턴 2: 특정 컬럼 기준 중복 제거 후 집계
df = df.drop_duplicates(subset=['id', 'date'], keep='first')
result = df.groupby('category')['value'].mean()

# 패턴 3: 결측 행 제외하고 비율 계산 (datamanim Q6, Q95 패턴)
df = df[df['view_count'] != 0]
df['ratio'] = df['comment_count'] / df['view_count']
df = df.dropna(subset=['ratio'])
```

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd

data = {
    'date':   ['2024-01', '2024-01', '2024-02', '2024-02', '2024-03',
               '2024-03', '2024-04', '2024-04', '2024-05', '2024-05'],
    'region': ['서울', '서울', '부산', None, '대구', '서울', '부산', None, '대구', '서울'],
    'sales':  [120, 120, 85, 95, 130, 110, 75, 88, 140, 102],
    'count':  [30, 30, 22, 18, 25, 28, 15, None, 22, 26]
}
df = pd.DataFrame(data)
```

---

### Q1. 데이터 전체 결측치 개수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(df.isnull().sum().sum())  # 3
```

</details>

---

### Q2. 결측치가 있는 컬럼과 각 개수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
s = df.isnull().sum()
print(s[s > 0])
# region    2
# count     1
```

</details>

---

### Q3. region 결측치를 '기타'로 채운 후, region 컬럼의 최빈값을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
f = df['region'].fillna('기타')
print(f.mode()[0])  # 서울
```

</details>

---

### Q4. count 결측치를 count 평균으로 채운 뒤, 전체 count 합계를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
c = df['count'].fillna(df['count'].mean())
print(c.sum())  # 240.0
```

</details>

---

### Q5. region에 결측치가 있는 행을 제거한 후 sales 평균을 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
d = df.dropna(subset=['region'])
print(round(d['sales'].mean(), 3))  # 110.25
```

</details>

---

### Q6. 전체 컬럼 기준으로 완전히 같은 중복 행이 몇 개인지 출력하라. (첫 번째 등장 제외)

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(df.duplicated().sum())  # 1
```

</details>

---

### Q7. 완전히 같은 중복 행을 제거하고(첫 번째 유지), region 결측치를 '기타'로 채워라. region별 sales 평균을 구하고 내림차순 정렬했을 때 첫 번째 region을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df = df.drop_duplicates()
df['region'] = df['region'].fillna('기타')
result = df.groupby('region')['sales'].mean().sort_values(ascending=False)
print(result.index[0])  # 대구
```

</details>

---

### Q8. 완전히 같은 중복 행을 제거하고, region 결측치가 있는 행을 제거하라. region별 sales 합계를 구하고, 합계가 전체 region 평균 이상인 region만 남겨라. sales 합계 내림차순으로 정렬했을 때 첫 번째 region을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df = df.drop_duplicates()
df = df.dropna(subset=['region'])
total = df.groupby('region')['sales'].sum()
result = total[total >= total.mean()].sort_values(ascending=False)
print(result.index[0])  # 서울
```

</details>
