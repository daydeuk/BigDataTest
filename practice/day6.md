# 6일차 — 날짜/시간 처리

## 개념 정리

### 1. pd.to_datetime() — 문자열 → datetime 변환

```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])

# 포맷이 특수한 경우 format 지정
df['date'] = pd.to_datetime(df['date'], format='%Y/%m/%d')
df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
```

> 변환 후에야 `.dt` 접근자 사용 가능. 변환 없이 `.dt.year` 하면 에러.

---

### 2. dt 접근자 — 날짜/시간 요소 추출

```python
df['year']   = df['dt'].dt.year    # 연도 (int)
df['month']  = df['dt'].dt.month   # 월 1~12 (int)
df['day']    = df['dt'].dt.day     # 일 1~31 (int)
df['hour']   = df['dt'].dt.hour    # 시 0~23 (int)
df['minute'] = df['dt'].dt.minute  # 분 0~59 (int)
```

---

### 3. 요일 추출 — day_name() vs dayofweek ★★★

```python
df['day_name']   = df['dt'].dt.day_name()   # 'Monday', 'Sunday' 등 영어 문자열
df['dayofweek']  = df['dt'].dt.dayofweek    # 0=Monday, 1=Tuesday, ..., 6=Sunday
```

> **시험 주의**: `dayofweek`는 **월요일이 0, 일요일이 6** — 헷갈리기 쉬움.
> 주말 필터: `df['dt'].dt.dayofweek >= 5` (토=5, 일=6)
> 평일 필터: `df['dt'].dt.dayofweek < 5`

---

### 4. 날짜 필터링 패턴

```python
# 특정 월 필터
df[df['dt'].dt.month == 3]

# 특정 연도 + 월
df[(df['dt'].dt.year == 2024) & (df['dt'].dt.month == 5)]

# 특정 시간대 (18시 이상 = 저녁)
df[df['dt'].dt.hour >= 18]

# 요일 이름으로 필터
df[df['dt'].dt.day_name() == 'Sunday']

# dayofweek으로 필터
df[df['dt'].dt.dayofweek == 6]   # 일요일만
df[df['dt'].dt.dayofweek >= 5]   # 주말 (토, 일)
```

---

### 5. 날짜 차이 계산

```python
# 특정 기준일과의 차이 (일수)
base = pd.Timestamp('2024-01-01')
df['elapsed_days'] = (df['dt'] - base).dt.days

# 두 datetime 컬럼의 차이
df['diff_hours'] = (df['end_dt'] - df['start_dt']).dt.total_seconds() / 3600
```

> `(datetime - datetime)`의 결과는 `timedelta` → `.dt.days` 또는 `.dt.total_seconds()`로 숫자 추출.

---

### 시험 빈출 패턴 정리

```python
# 패턴 1: datetime 변환 후 month 컬럼 추가 → groupby
df['dt'] = pd.to_datetime(df['dt'])
df['month'] = df['dt'].dt.month
df.groupby('month')['value'].sum()

# 패턴 2: 요일 컬럼 추가 → groupby
df['day_name'] = df['dt'].dt.day_name()
df.groupby('day_name')['value'].mean()

# 패턴 3: 특정 조건 복합 (월 + 시간대)
df[(df['dt'].dt.month == 3) & (df['dt'].dt.hour >= 18)]

# 패턴 4: 주말/평일 구분 컬럼 추가
df['is_weekend'] = df['dt'].dt.dayofweek >= 5
df.groupby('is_weekend')['amount'].mean()
```

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd

data = {
    'order_datetime': [
        '2024-01-05 11:30', '2024-01-14 19:45', '2024-01-22 13:00',
        '2024-02-07 20:15', '2024-02-14 12:30', '2024-02-17 18:00',
        '2024-02-25 21:30', '2024-03-04 14:45', '2024-03-09 09:00',
        '2024-03-15 20:00', '2024-03-20 18:30', '2024-03-28 12:00',
        '2024-04-03 19:00', '2024-04-10 10:30', '2024-04-13 21:00',
        '2024-04-21 15:30', '2024-05-06 12:00', '2024-05-11 20:30',
        '2024-05-19 18:00', '2024-05-25 22:00',
    ],
    'region':   ['서울', '부산', '서울', '대구', '인천', '서울', '부산', '광주',
                 '서울', '대구', '인천', '부산', '서울', '광주', '대구', '인천',
                 '서울', '부산', '서울', '대구'],
    'category': ['한식', '중식', '피자', '한식', '치킨', '피자', '한식', '중식',
                 '치킨', '피자', '한식', '치킨', '피자', '한식', '중식', '피자',
                 '한식', '치킨', '피자', '한식'],
    'amount':   [18000, 22000, 15000, 25000, 19000, 32000, 21000, 17000,
                 23000, 16000, 31000, 14000, 29000, 12000, 24000, 27000,
                 20000, 26000, 18000, 33000],
    'delivery_time': [25, 35, 30, 20, 40, 28, 45, 22,
                      32, 38, 27, 34, 42, 19, 36, 31,
                      29, 44, 26, 33]
}
df = pd.DataFrame(data)
```

---

### Q1. order_datetime을 datetime 타입으로 변환한 후, 월별 주문 건수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
result = df['order_datetime'].dt.month.value_counts().sort_index()
print(result)
# 1    3
# 2    4
# 3    5
# 4    4
# 5    4
```

> `value_counts()` 는 빈도 내림차순 정렬 → `.sort_index()`로 월 순서대로 정렬.
> 또는 `df.groupby(df['order_datetime'].dt.month).size()` 도 동일 결과.

</details>

---

### Q2. 3월 주문만 필터링하여 amount 평균을 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
march = df[df['order_datetime'].dt.month == 3]
print(round(march['amount'].mean(), 3))  # 20200.0
```

> 3월 rows: 17000, 23000, 16000, 31000, 14000 → 합계 101000 / 5 = 20200.0

</details>

---

### Q3. 주문 시각이 18시 이상인 저녁 주문 건수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
evening = df[df['order_datetime'].dt.hour >= 18]
print(len(evening))  # 11
```

> `dt.hour`는 0~23 정수. `>= 18` 이면 18:00, 19:xx, 20:xx, 21:xx, 22:xx 모두 포함.

</details>

---

### Q4. 요일(day_name) 컬럼을 추가한 후, 요일별 amount 합계를 내림차순으로 출력하라. 합계가 가장 높은 요일을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
df['day_name'] = df['order_datetime'].dt.day_name()
result = df.groupby('day_name')['amount'].sum().sort_values(ascending=False)
print(result)
print(result.index[0])  # Saturday
```

> 요일별 합계: Saturday=138000, Sunday=88000, Wednesday=116000, Monday=52000, Friday=34000, Thursday=14000
> 최대: Saturday

</details>

---

### Q5. dayofweek을 이용해 주말(토·일)과 평일로 구분하고, 각 그룹의 amount 평균을 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
df['is_weekend'] = df['order_datetime'].dt.dayofweek >= 5

result = df.groupby('is_weekend')['amount'].mean().round(3)
print(result)
# is_weekend
# False    19636.364   (평일)
# True     25111.111   (주말)
```

> `dayofweek >= 5` → True: 주말(토=5, 일=6) / False: 평일(월=0 ~ 금=4)

</details>

---

### Q6. 3월이면서 주문 시각이 18시 이상인 주문의 건수와 amount 합계를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
cond = (df['order_datetime'].dt.month == 3) & (df['order_datetime'].dt.hour >= 18)
filtered = df[cond]
print(len(filtered))           # 2
print(filtered['amount'].sum()) # 47000
```

> 해당 row: 2024-03-15 20:00 (16000), 2024-03-20 18:30 (31000)

</details>

---

### Q7. 월별 amount 합계와 건수를 구하라. 합계가 가장 높은 달의 건수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
df['month'] = df['order_datetime'].dt.month

result = df.groupby('month')['amount'].agg(['sum', 'count'])
top_month = result['sum'].idxmax()
print(result.loc[top_month, 'count'])  # 5
```

> 월별 합계: 1월=55000, 2월=97000, 3월=101000, 4월=92000, 5월=97000
> 최대 달: 3월 → 건수 = 5

</details>

---

### Q8. 2024-01-01 기준으로 각 주문의 경과일(elapsed_days)을 계산하여 컬럼으로 추가하라. 경과일이 100일 이상인 주문 건수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
base = pd.Timestamp('2024-01-01')
df['elapsed_days'] = (df['order_datetime'] - base).dt.days
print(len(df[df['elapsed_days'] >= 100]))  # 7
```

> `(datetime - datetime)` → timedelta → `.dt.days`로 정수 변환.
> 2024-04-10이 기준일로부터 정확히 100일 (2024는 윤년: 1월31 + 2월29 + 3월31 + 4월1~10 = 100).
> 100일 이상: 4월10일, 4월13일, 4월21일, 5월6일, 5월11일, 5월19일, 5월25일 = 7건.

</details>
