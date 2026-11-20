# 재도전 Day 3 — 1유형 ③ 날짜 · 문자열 · 파생 컬럼 · quantile · 표준편차

> 2026-11-20 (금) · 목표 2시간 · 복습 10분 → 개념 40분 → 연습문제 60분 → 오답 정리 10분
>
> 시작 전: [Day 2 복습](복습_day2.md) 10분
>
> 오늘은 **새 함수가 많다.** 전부 외우려 하지 말고, 표의 "시험 단골"만 손으로 두 번씩 쳐 본다.

---

## 오늘의 연습용 미니 데이터

```python
import pandas as pd
import numpy as np

t = pd.DataFrame({
    'name':  ['Kim Minsu', 'lee jihye', 'PARK Sora', 'choi Dan'],
    'dt':    ['2024-03-02 09:30', '2024-03-15 18:05', '2024-04-06 21:40', '2024-05-20 13:00'],
    'join':  ['2024-02-25', '2024-01-10', '2024-04-06', '2024-03-01'],
    'phone': ['010-1234-5678', '010-9876-5432', '011-2222-3333', '010-5555-0000'],
    'score': [55, 72, 90, 30],
})
```

---

## 1. 날짜 ① — `pd.to_datetime` 먼저! ⭐

CSV에서 읽은 날짜는 **그냥 글자(문자열)**다. 글자 상태로는 월·요일을 꺼낼 수 없다.

```python
t['dt'].dt.month
# AttributeError: Can only use .dt accessor with datetimelike values   ← 글자라서 에러

t['dt'] = pd.to_datetime(t['dt'])     # 글자 → 날짜로 변환 (재할당 필수!)
t['join'] = pd.to_datetime(t['join'])
```

> **시험 루틴**: `**df.info()`에서 날짜 컬럼이 `object`면 → `pd.to_datetime` 먼저.
> 변환 후 `info()`를 다시 보면 `datetime64[ns]`로 바뀌어 있다.

---

## 2. 날짜 ② — `.dt.무엇` 으로 꺼내기

```python
x = t['dt']
x.dt.year         # 연
x.dt.month        # 월
x.dt.day          # 일
x.dt.hour         # 시
x.dt.dayofweek    # 요일 번호 (월=0 … 일=6)
x.dt.day_name()   # 요일 이름 ('Monday' …) — 이것만 괄호 있음!
```

실제 결과:

```
                   dt  year  month  day  hour  dayofweek  day_name()
0 2024-03-02 09:30:00  2024      3    2     9          5    Saturday
1 2024-03-15 18:05:00  2024      3   15    18          4      Friday
2 2024-04-06 21:40:00  2024      4    6    21          5    Saturday
3 2024-05-20 13:00:00  2024      5   20    13          0      Monday
```

| 문제 표현 | 코드 |
|---|---|
| "3월 주문" | `df[df['dt'].dt.month == 3]` |
| "주말 주문" | `df[df['dt'].dt.dayofweek >= 5]` (토=5, 일=6) |
| "저녁 6시~9시대" | `df[(df['dt'].dt.hour >= 18) & (df['dt'].dt.hour <= 21)]` |
| "월별 건수" | `df['dt'].dt.month.value_counts()` (Day 2 그대로) |
| "2024-04-01 이후" | `df[df['dt'] >= '2024-04-01']` (글자와 바로 비교 가능) |

> ⚠️ **요일 번호는 월요일=0**이다. 일요일=0이 아니다. 헷갈리면 `day_name()`으로 이름을 보고 확인한다.
> ⚠️ `day_name()`만 괄호가 있고, `year`·`month`·`hour`·`dayofweek`는 괄호가 없다.

---

## 3. 날짜 ③ — 두 날짜의 차이 (며칠 지났나)

```python
diff = t['dt'] - t['join']     # 날짜끼리 빼면 '기간'이 된다
diff.dt.days                   # 기간 → 일수(정수)
```

```
diff                       diff.dt.days
0    6 days 09:30:00       6
1   65 days 18:05:00       65
2    0 days 21:40:00       0      ← 같은 날 가입·주문 = 0일
3   80 days 13:00:00       80
```

> `.dt.days`는 시간 부분을 **버린다** (6일 9시간 → 6).
> "가입 후 30일 이내" → `diff.dt.days <= 30` (이내 = 포함 → `<=`)

---

## 4. 문자열 — `.str.무엇` ⭐ 시험 단골

숫자에 `.dt`가 있듯이, 글자 컬럼에는 `.str`을 붙인다.

```python
s = t['name']
s.str.lower()              # 소문자로
s.str.upper()              # 대문자로
s.str.len()                # 글자 수
s.str[:3]                  # 앞 3글자 (슬라이싱)
s.str.contains('kim')      # 'kim'이 들어 있나 → True/False
s.str.startswith('010')    # ~로 시작하나
s.str.endswith('.com')     # ~로 끝나나
s.str.replace('-', '')     # 바꾸기
s.str.split('-')           # 쪼개기 → 목록
s.str.split('-').str[1]    # 쪼갠 것 중 2번째 조각
```

**대소문자 함정** — 실제 결과:

```
        name    contains('kim')   lower().str.contains('kim')
0  Kim Minsu    False ❌           True ✅
1  lee jihye    False              False
2  PARK Sora    False              False
3   choi Dan    False              False
```

> `contains`는 **대소문자를 구분**한다. 'Kim'은 'kim'이 아니다.
> 문제에 "대소문자 구분 없이"가 있으면 → **`.str.lower()` 먼저**, 그다음 `.str.contains()`

**split 결과 꺼내기** — 실제 결과:

```
phone              split('-')            split('-').str[1]
010-1234-5678      [010, 1234, 5678]     1234
011-2222-3333      [011, 2222, 3333]     2222
```

> 쪼개면 칸마다 **목록**이 들어간다. 목록에서 N번째 조각은 **`.str[N-1]`** (여기서도 0부터)
> 주소 "서울 강남구 …"의 시/도 → `df['address'].str.split().str[0]` (괄호 비우면 **띄어쓰기**로 쪼갠다)

### ⭐⭐ `.str[1]` vs `[1]` — 에러 없이 틀린다 (사용자 질문에서 나온 핵심)

```
                  ↓ .str[1] = 각 칸 안에서 2번째 (세로로 쭉)
행 0 → [010, 1234, 5678]
행 1 → [010, 9876, 5432]   ← [1] = 1번 행을 통째로 (가로 한 줄)
행 2 → [011, 2222, 3333]
행 3 → [010, 5555, 0000]
```

| 코드 | 실제 결과 | 뜻 |
|---|---|---|
| `s.str.split('-')[1]` | `['010', '9876', '5432']` ❌ | **1번 행** 통째 (에러 안 남!) |
| `s.str.split('-').str[1]` | `['1234', '9876', '2222', '5555']` ✅ | **모든 행**의 2번째 조각 |

| 대상 | 쪼개기 | 조각 꺼내기 |
|---|---|---|
| 글자 하나 `'010-1234'` | `'010-1234'.split('-')` | `[1]` |
| 컬럼 전체 `s` | `s.str.split('-')` | **`.str[1]`** |

> **기억법: 컬럼에서는 쪼갤 때도 `.str`, 꺼낼 때도 `.str`.**
> 파이썬 글자 하나에는 `[1]`이 맞아서 더 헷갈린다. 컬럼(값 여러 개)이면 "칸마다 해 줘" = `.str`

**필터에 쓰기** — 결과가 True/False라서 Day 1 필터 그대로

```python
len(df[df['email'].str.contains('gmail')])          # gmail 포함 행 수
df['email'].str.contains('gmail').sum()             # 같은 답 (Day 1 isin과 같은 원리)
```

---

## 5. 파생 컬럼 ① — `np.where` (조건에 따라 2가지 값) ⭐

```python
t['pass'] = np.where(t['score'] >= 60, '합격', '불합격')
#                    ↑ 조건            ↑ True일 때 ↑ False일 때
```

```
   score  pass
0     55  불합격
1     72  합격
2     90  합격
3     30  불합격
```

> 엑셀의 `IF(조건, 참, 거짓)`과 같다. `import numpy as np` 잊지 않기.
> 새 컬럼이 생기면 바로 Day 2처럼 `value_counts()`, `groupby('pass')` 할 수 있다.

---

## 6. 파생 컬럼 ② — `pd.cut` (숫자를 구간으로) — 경계값 주의 ⚠️

```python
t['grade'] = pd.cut(t['score'], bins=[0, 40, 70, 100], labels=['C', 'B', 'A'])
```

`bins=[0, 40, 70, 100]` → 구간 3개: `(0, 40]` `(40, 70]` `(70, 100]`

| 구간 | 뜻 | 라벨 |
|---|---|---|
| `(0, 40]` | 0 **초과** 40 **이하** | C |
| `(40, 70]` | 40 초과 70 이하 | B |
| `(70, 100]` | 70 초과 100 이하 | A |

**경계값이 어디로 가나** — 실제 결과:

| 값 | 기본 (`right=True`) | `right=False` |
|---|---|---|
| 40 | **C** (40 이하) | B (40 이상 70 미만) |
| 70 | **B** (70 이하) | A |

> 기본은 **오른쪽 끝 포함**(`]`). 문제가 "40 이하 / 40 초과 70 이하"면 기본 그대로.
> 문제가 "40 미만 / 40 이상 70 미만"이면 `right=False`.
> 끝이 없는 구간("60분 초과")은 `np.inf` (무한대): `bins=[0, 30, 60, np.inf]`
> 지난번 실수: pd.cut 컬럼으로 groupby하면 경고 → `groupby('grade', observed=True)`

---

## 7. quantile(사분위수) · 표준편차

```python
sc = t['score']           # [55, 72, 90, 30]
sc.quantile(0.25)         # 48.75  — 1사분위수 (Q1, 하위 25%)
sc.quantile(0.5)          # 63.5   — 중앙값 (= sc.median())
sc.quantile(0.75)         # 76.5   — 3사분위수 (Q3, 상위 25%)
sc.std()                  # 25.539… — 표준편차
sc.describe()             # 위 값들을 한 번에 (25% / 50% / 75% / std)
```

**IQR과 이상치** — 시험 단골

```python
q1 = df['col'].quantile(0.25)
q3 = df['col'].quantile(0.75)
iqr = q3 - q1
outlier = df[(df['col'] < q1 - 1.5 * iqr) | (df['col'] > q3 + 1.5 * iqr)]
```

> "상위 25% 이상" → `df[df['col'] >= df['col'].quantile(0.75)]`
> 백분위수 "90번째 백분위수" → `quantile(0.9)` (0~1 사이 소수로 쓴다. `quantile(90)` ❌)
> 표준편차: pandas `std()`는 기본이 표본표준편차(`ddof=1`)다. 문제에 특별한 말이 없으면 그대로 쓴다.

---

## 오늘의 함정 요약

| 함정 | 기억할 한 줄 |
|---|---|
| 글자 날짜에 `.dt` | 에러 → `pd.to_datetime` 먼저 (재할당) |
| 요일 번호 | 월=0 … 일=6, 주말은 `>= 5` |
| `day_name` 괄호 | `day_name()`만 괄호, 나머지는 괄호 없음 |
| `contains` 대소문자 | "대소문자 무시" → `.str.lower().str.contains()` |
| split 조각 | N번째 조각 → `.str[N-1]` |
| `pd.cut` 경계 | 기본은 오른쪽 포함 `(a, b]`. "미만"이면 `right=False` |
| "이내" / "초과" | 이내·이하 `<=`, 초과 `>` (Day 2 Q6) |
| quantile 숫자 | 0~1 소수: `quantile(0.75)` |

---

# 연습문제 (8문제)

## 데이터 세팅

```python
import pandas as pd
import numpy as np
df = pd.read_csv('retake/data/day3_delivery.csv')
```

배달 주문 40건. 컬럼:

| 컬럼 | 뜻 |
|---|---|
| `order_id` | 주문 번호 |
| `order_dt` | 주문 일시 (`2024-05-17 17:15` 형태의 **글자**) |
| `signup_date` | 고객 가입일 (**글자**) |
| `email` | 고객 이메일 (일부는 대문자) |
| `address` | 주소 (`서울 송파구 243번길` 형태) |
| `amount` | 주문 금액 |
| `deliver_min` | 배달 걸린 시간 (분) |

> 풀이 방법: `workspace/day3.py`에 풀고 "채점해줘".
> 각 문제는 원본에서 시작하되, **날짜 변환(`pd.to_datetime`)과 Q5·Q6에서 만든 컬럼은 이어서 써도 된다.**

---

### Q1. (기본) 주문이 가장 많은 **월**과 그 **건수**를 출력하라.

### Q2. (기본) 주말(토요일·일요일)에 들어온 주문은 몇 건인가?

### Q3. (기본) 이메일이 gmail 계정인 주문은 몇 건인가? (**대소문자 구분 없이** 센다)

### Q4. (응용) `address`의 첫 단어가 시/도다. 주문이 가장 많은 **시/도 이름**을 출력하라.

### Q5. (응용) 가입일부터 주문일까지 지난 일수를 구하라. **30일 이내(30일 포함)**면 '신규', 아니면 '기존'으로 `type` 컬럼을 만들어라. '신규' 주문의 `amount` 평균을 소수 둘째 자리까지 출력하라.

### Q6. (응용) `deliver_min`을 구간으로 나눠 `speed` 컬럼을 만들어라.
- **30분 이하** → '빠름'
- **30분 초과 60분 이하** → '보통'
- **60분 초과** → '느림'

'빠름' 주문은 몇 건인가?

### Q7. (응용) `amount`의 1사분위수, 3사분위수, IQR(3사분위수 − 1사분위수)을 차례로 출력하라.

### Q8. (복합) 주문 시각이 **18시~21시대**(18시 0분 ~ 21시 59분)인 주문만 사용한다. 시/도별 `amount` **표준편차**를 구했을 때, 표준편차가 가장 큰 **시/도 이름**과 그 값을 소수 둘째 자리까지 출력하라.

---

## 채점 결과 — 7 / 8 → Q3 재풀이 ✅ (2026-11-21)

| # | 내 답 | 정답 | 결과 |
|---|---|---|---|
| Q1 | 5, 16 | 5월, 16 | ✅ |
| Q2 | 16 | 16 | ✅ |
| Q3 | **40** | **13** | ❌ → 재풀이 ✅ `.count()` → True·False 모두 셈 |
| Q4 | 서울 | 서울 | ✅ |
| Q5 | 26400.0 | 26400.0 | ✅ `<=30` 경계 정확 |
| Q6 | 11 | 11 | ✅ 경계값(30·60) 정확 |
| Q7 | 14875.0 37375.0 22500.0 | 같음 | ✅ |
| Q8 | 인천, 20193.23 | 인천, 20193.23 | ✅ |

### Q1 ✅
```python
df['order_dt'] = pd.to_datetime(df['order_dt'])
df['order_month'] = df['order_dt'].dt.month
print(df.value_counts('order_month').index[0])   # 5
print(df.value_counts('order_month').iloc[0])    # 16
```
> `df.value_counts('컬럼')`도 된다. 더 흔한 모양은 `df['order_month'].value_counts()`

### Q2 ✅
```python
df['dayofweek'] = df['order_dt'].dt.dayofweek
q2 = df[(df['dayofweek'] == 5) | (df['dayofweek'] == 6)]
print(len(q2))   # 16
```
> 더 짧게: `len(df[df['dayofweek'] >= 5])` 또는 `isin([5, 6])`

### Q3 ❌ — `.count()`는 True·False를 **다** 센다 (isin 복습 I1과 같은 실수 ⚠️)
```python
# 내 풀이 — 40
df['lower_eamil'] = df['email'].str.lower()
print(df['lower_eamil'].str.endswith('@gmail.com').count())

# 모범답안 — 13
print(df['email'].str.lower().str.endswith('@gmail.com').sum())
print(len(df[df['email'].str.lower().str.endswith('@gmail.com')]))   # 같은 답
```

| 코드 | 결과 | 세는 것 |
|---|---|---|
| `조건.count()` | 40 ❌ | **결측이 아닌 칸** 수 → True·False 모두 |
| `조건.sum()` | 13 ✅ | True 개수 |
| `len(df[조건])` | 13 ✅ | 걸러진 행 수 |

> `lower()` 먼저 한 것은 정확했다 (안 하면 11). **True/False 결과를 셀 땐 `.sum()` 또는 `len(df[ ])`** — `count()`·`len(조건)`은 전체 행 수가 나온다.
> 내 `**` 질문 "대소문자 무시는 `.lower()` 먼저가 국룰?" → **맞다.** contains·startswith·endswith 모두 같은 방법으로 통일

### Q4 ✅
```python
df['city'] = df['address'].str.split(' ').str[0]
print(df['city'].value_counts().idxmax())   # 서울
```

### Q5 ✅
```python
df['signup_date'] = pd.to_datetime(df['signup_date'])
df['diff'] = (df['order_dt'] - df['signup_date']).dt.days
df['type'] = np.where(df['diff'] <= 30, '신규', '기존')
print(round(df.groupby('type')['amount'].mean().loc['신규'], 2))   # 26400.0
```
> `< 30`이었다면 27076.92 — 30일인 주문이 2건 있었다. "이내 = 포함" 정확 👍

### Q6 ✅
```python
df['speed'] = pd.cut(df['deliver_min'], bins=[0, 30, 60, np.inf], labels=['빠름', '보통', '느림'])
print(df['speed'].value_counts().loc['빠름'])   # 11
```
> `right=False`였다면 9 — 30분 주문 2건이 '보통'으로 넘어간다. 기본 `(a, b]` 그대로 정확 👍

### Q7 ✅
```python
q1 = df['amount'].quantile(0.25)
q3 = df['amount'].quantile(0.75)
print(q1, q3, q3 - q1)   # 14875.0 37375.0 22500.0
```

### Q8 ✅
```python
df['order_hour'] = df['order_dt'].dt.hour
q8 = df[(df['order_hour'] >= 18) & (df['order_hour'] <= 21)]
print(q8.groupby('city')['amount'].std().sort_values(ascending=False).index[0])          # 인천
print(round(q8.groupby('city')['amount'].std().sort_values(ascending=False).iloc[0], 2))  # 20193.23
```
> 필터 결과를 `q8`에 담고 계산 — Day 2 복습에서 정한 "변수로 빼기" 습관 그대로 👍

---

### 개념 공부 중 나온 질문 (실행으로 확인)

| 질문 | 답 |
|---|---|
| `dayofweek()`도 괄호? | 없다. `.dt` 뒤엔 **`day_name()`만 괄호**. 붙이면 `'Series' object is not callable` |
| minute·second는 없나? | 있다 (`minute`, `second`, `quarter`, `date`…). 시험 빈도가 낮아 생략했던 것 |
| `split('-')[1]` 해도 되나? | ⭐⭐ 안 된다. 에러 없이 **1번 행 통째**. 조각은 `.str[1]` (= 두 번째 열을 통으로) |
| `iloc`은 열도 번호? | 그렇다. 행 번호 + 열 이름은 `iloc[0]['col']` |
| `iloc[0]['region', 'qty']`? | 안 된다 → `iloc[0][['region', 'qty']]` (여러 개는 대괄호 두 겹) |
| groupby에 조건 바로? | 안 된다 → 조건을 컬럼으로 만들고 `groupby('g')['is_x'].mean()` = 그룹별 비율 |
| `bins`·`labels` 이름 고정? | 철자 고정 (복수형). 라벨 수 = 경계 수 − 1. 데이터가 경계 밖이면 조용히 NaN |
| `right`가 경계 위치 결정? | 그렇다. "이하" → 기본, "미만" → `right=False`. `left=`는 없다 |
| 음의 무한대 필요? | **0이 있으면** 필요 — `(0, 30]`은 0을 못 담는다 → `-np.inf` 또는 `include_lowest=True` |
| quantile·std는 숫자만? | 그렇다. 글자면 `could not convert string to float`. 표 전체엔 `numeric_only=True` |
| IQR? | Q3 − Q1 = 가운데 50%의 폭. 이상치 = Q1 − 1.5×IQR 미만 / Q3 + 1.5×IQR 초과 |
| startswith·endswith는 대소문자 무시? | 아니다. **셋 다 구분**. `case=False`는 contains만 → `lower()` 먼저로 통일 |
| value_counts로 평균? | 안 된다. 세기만. 다른 컬럼 평균은 `groupby` |
