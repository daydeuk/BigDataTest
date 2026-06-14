# 6일차 복습 — 날짜/시간 처리

## 데이터 세팅

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
    'region':   ['서울','부산','서울','대구','인천','서울','부산','광주',
                 '서울','대구','인천','부산','서울','광주','대구','인천',
                 '서울','부산','서울','대구'],
    'category': ['한식','중식','피자','한식','치킨','피자','한식','중식',
                 '치킨','피자','한식','치킨','피자','한식','중식','피자',
                 '한식','치킨','피자','한식'],
    'amount':   [18000,22000,15000,25000,19000,32000,21000,17000,
                 23000,16000,31000,14000,29000,12000,24000,27000,
                 20000,26000,18000,33000],
    'delivery_time': [25,35,30,20,40,28,45,22,
                      32,38,27,34,42,19,36,31,
                      29,44,26,33]
}
df = pd.DataFrame(data)
df['order_datetime'] = pd.to_datetime(df['order_datetime'])
```

---

## Q1. order_datetime을 datetime 타입으로 변환한 후, 월별 주문 건수를 출력하라.

### 내 풀이 ✅
```python
df['month'] = df['order_datetime'].dt.month
print(df.groupby('month')['month'].count())
```

> 건수는 행 수 — 특정 컬럼 합계가 아님. `groupby().size()` 또는 `value_counts().sort_index()`도 동일.

---

## Q2. 3월 주문만 필터링하여 amount 평균을 소수 셋째 자리까지 출력하라.

### 내 풀이 ✅
```python
print(round(df[df['month'] == 3]['amount'].mean(), 3))
```

> Q1에서 만든 `month` 컬럼 재활용 가능.

---

## Q3. 주문 시각이 18시 이상인 저녁 주문 건수를 출력하라.

### 내 풀이 ✅
```python
df['hour'] = df['order_datetime'].dt.hour
print(df[df['hour'] >= 18].shape[0])
```

> 건수 출력 시 반드시 `.shape[0]` 또는 `len()` 추가. DataFrame 그대로 출력하면 오답.

---

## Q4. 요일(day_name) 컬럼을 추가한 후, 요일별 amount 합계를 내림차순으로 출력하라. 합계가 가장 높은 요일을 출력하라.

### 내 풀이 ✅
```python
df['day_name'] = df['order_datetime'].dt.day_name()
result = df.groupby('day_name')['amount'].sum().sort_values(ascending=False)
print(result)
print(result.index[0])
```

> `day_name()`은 영어 문자열 반환 ('Monday', 'Saturday' 등).

---

## Q5. dayofweek을 이용해 주말(토·일)과 평일로 구분하고, 각 그룹의 amount 평균을 소수 셋째 자리까지 출력하라.

### 내 풀이 ✅
```python
df['is_weekend'] = df['order_datetime'].dt.dayofweek >= 5
print(round(df.groupby('is_weekend')['amount'].mean(), 3))
```

> `dayofweek`: 0=월 ~ 4=금, 5=토, 6=일. `>= 5`가 주말.

---

## Q6. 3월이면서 주문 시각이 18시 이상인 주문의 건수와 amount 합계를 출력하라.

### 내 풀이 ✅
```python
cond = (df['order_datetime'].dt.month == 3) & (df['order_datetime'].dt.hour >= 18)
filtered = df[cond]
print(len(filtered))
print(filtered['amount'].sum())
```

> 복합 조건은 각 조건을 `()`로 감싸고 `&`로 연결.

---

## Q7. 월별 amount 합계와 건수를 구하라. 합계가 가장 높은 달의 건수를 출력하라.

### 내 풀이 ✅
```python
q7 = df.groupby('month')['amount'].agg(['sum', 'count'])
index = q7['sum'].sort_values(ascending=False).index[0]
print(q7.loc[index, 'count'])
```

> `idxmax()`로 더 간단하게 가능: `top_month = q7['sum'].idxmax()`
> `agg(['sum', 'count'])` — 합계와 건수 한번에 구하는 패턴.

---

## Q8. 2024-01-01 기준으로 각 주문의 경과일(elapsed_days)을 계산하여 컬럼으로 추가하라. 경과일이 100일 이상인 주문 건수를 출력하라.

### 내 풀이 ✅
```python
base = pd.Timestamp('2024-01-01')
df['elapsed_days'] = (df['order_datetime'] - base).dt.days
print(df[df['elapsed_days'] >= 100].shape[0])
```

> `(datetime - base)` 결과는 timedelta → `.dt.days`로 정수(일수) 추출.
> `base = '2024-01-01'` 문자열도 동일하게 동작.
