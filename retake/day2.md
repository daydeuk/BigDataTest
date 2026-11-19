# 재도전 Day 2 — 1유형 ② groupby · agg · transform · value_counts

> 2026-11-17 (화) · 목표 2시간 · 복습 10분 → 개념 40분 → 연습문제 60분 → 오답 정리 10분
>
> 시작 전: [Day 1 복습](복습_day1.md) 10분

---

## 오늘의 연습용 미니 데이터

개념 예제는 아래 6행짜리 표로 설명한다. 직접 쳐서 결과를 비교해 본다.

```python
import pandas as pd
import numpy as np

t = pd.DataFrame({
    'name':  ['A', 'B', 'C', 'D', 'E', 'F'],
    'team':  ['red', 'blue', 'red', 'blue', 'red', 'green'],
    'score': [80, 90, 70, np.nan, 60, 85],
    'age':   [25, 32, 41, 28, 36, 30],
})
```

```
  name   team  score  age
0    A    red   80.0   25
1    B   blue   90.0   32
2    C    red   70.0   41
3    D   blue    NaN   28     ← score 결측
4    E    red   60.0   36
5    F  green   85.0   30
```

---

## 1. value_counts — "몇 개씩 있나?" ⭐ 가장 쉬운 집계

```python
t['team'].value_counts()                 # 값별 개수 (많은 순으로 자동 정렬)
t['team'].value_counts(normalize=True)   # 값별 비율 (합계 1)
t['team'].nunique()                      # 서로 다른 값이 몇 종류인가 → 3
t['team'].unique()                       # 서로 다른 값 목록 → ['red' 'blue' 'green']
```

```
value_counts()        value_counts(normalize=True)
team                  team
red      3            red      0.500000
blue     2            blue     0.333333
green    1            green    0.166667
```

**결과에서 꺼내는 법**

| 원하는 것 | 코드 | 결과 |
|---|---|---|
| 가장 많은 값의 **이름** | `t['team'].value_counts().index[0]` | `'red'` |
| 가장 많은 값의 **개수** | `t['team'].value_counts().iloc[0]` | `3` |
| 특정 값의 개수 | `t['team'].value_counts()['blue']` | `2` |
| 특정 값의 비율 | `t['team'].value_counts(normalize=True)['red']` | `0.5` |

> `value_counts()`는 **이미 많은 순으로 정렬**돼 있다. 그래서 1등은 `index[0]` / `iloc[0]`로 바로 꺼낸다.
> 왼쪽 글자(`red`, `blue`)가 **이름표(index)**, 오른쪽 숫자가 **값**이다. Day 1의 loc/iloc 그대로 적용된다.

---

## 2. groupby 기본 — "그룹별로 나눠서 계산"

```python
t.groupby('team')['score'].mean()
#        ↑ 이걸로 나누고  ↑ 이 컬럼을  ↑ 이렇게 계산
```

```
team
blue     90.0      ← blue 팀 score: [90, NaN] → NaN은 빼고 평균 = 90
green    85.0
red      70.0      ← red 팀 score: [80, 70, 60] → 평균 70
Name: score, dtype: float64
```

**결과는 Series이고, 이름표(index)가 그룹 이름이다.**

```python
g = t.groupby('team')['score'].mean()    # ← 계산(.mean())까지 끝난 결과를 g에 담는다
```

> ⚠️ `t.groupby('team')['score']`까지는 **나눠만 놓은 묶음**이라 `.loc`, `.iloc`, `.sort_values`가 없다 (AttributeError).
> 반드시 `mean()`·`sum()`·`size()` 같은 계산을 붙인 뒤에 꺼낸다. (사용자 질문에서 나온 함정)

| 원하는 것 | 코드 | 결과 |
|---|---|---|
| 특정 그룹 값 | `g.loc['red']` | `70.0` |
| 가장 큰 그룹 **이름** | `g.idxmax()` | `'blue'` |
| 가장 큰 **값** | `g.max()` | `90.0` |
| 2번째로 큰 값 | `g.sort_values(ascending=False).iloc[1]` | `85.0` |
| 2번째로 큰 그룹 이름 | `g.sort_values(ascending=False).index[1]` | `'green'` |

> ⚠️ **groupby 결과는 값 순서가 아니라 그룹 이름 순서(가나다·ABC)로 정렬된다.** (blue → green → red)
> 그래서 "N번째로 큰 그룹"은 반드시 `sort_values(ascending=False)` 후 `iloc[N-1]`.

자주 쓰는 계산 함수: `mean()` 평균 · `sum()` 합계 · `max()` / `min()` · `median()` 중앙값 · `std()` 표준편차 · `count()` / `size()` 건수(아래 3번) · `nunique()` 고유값 개수

---

## 3. 건수 세기 — size vs count ⭐ 결측치가 있으면 답이 달라진다

```python
t.groupby('team').size()             # 행 수 (결측 포함)
t.groupby('team')['score'].count()   # score가 결측이 아닌 행 수
```

| team | `size()` | `['score'].count()` | 이유 |
|---|---|---|---|
| blue | **2** | **1** | D의 score가 NaN → count에서 빠짐 |
| green | 1 | 1 | |
| red | 3 | 3 | |

> **"주문 건수", "인원 수", "몇 건"** → 행 수를 묻는 것 → `size()` (또는 `value_counts()`)
> `count()`는 **그 컬럼에 값이 있는 행만** 센다. 결측이 있는 컬럼으로 count하면 건수가 줄어든다.
> 지난번 단골 실수: 건수를 구하는데 `sum()`을 씀 → 건수는 `size()` / `count()`

---

## 4. agg — 여러 계산을 한 번에

```python
# 방법 ① 리스트로 — 컬럼 이름이 함수 이름이 된다
t.groupby('team')['score'].agg(['mean', 'max', 'count'])

# 방법 ② 이름=(컬럼, 함수) — 결과 컬럼 이름을 내가 정한다
t.groupby('team').agg(평균=('score', 'mean'), 인원=('name', 'size'))
```

```
① 리스트                          ② 이름 지정
       mean   max  count                 평균  인원
team                              team
blue   90.0  90.0      1          blue   90.0   2
green  85.0  85.0      1          green  85.0   1
red    70.0  80.0      3          red    70.0   3
```

**결과는 DataFrame (행 = 그룹, 열 = 계산)** → Day 1 필터 그대로 쓴다

```python
a = t.groupby('team').agg(평균=('score', 'mean'), 인원=('name', 'size'))

a[a['인원'] >= 2]                              # 인원 2명 이상인 팀만
a[a['인원'] >= 2]['평균'].idxmin()              # 그중 평균이 가장 낮은 팀 이름 → 'red'
a.loc['blue', '평균']                           # blue 팀의 평균 → 90.0
```

> 시험 단골 흐름: **그룹별로 [건수, 평균]을 같이 구한다 → 건수 조건으로 거른다 → 평균이 가장 큰/작은 그룹.**
> `agg`가 기억 안 나면 따로 구해도 된다: `cnt = ...size()`, `avg = ...mean()` → `avg[cnt >= 2]` (이름표가 같으면 이렇게 걸러진다)

---

## 5. transform — 각 행 옆에 "자기 그룹 값" 붙이기 ⭐ 지난번 오답

**"자기 팀 평균보다 나이가 많은 사람"** 같은 문제는 행 하나하나를 자기 그룹 값과 비교해야 한다.

```python
t.groupby('team')['age'].mean()               # 3행 (팀 수만큼) → 6행인 t와 바로 비교 불가 ❌
t.groupby('team')['age'].transform('mean')    # 6행 (원본 행 수 그대로) → 비교 가능 ✅
```

```python
t['team_mean'] = t.groupby('team')['age'].transform('mean')
t[t['age'] > t['team_mean']]
```

```
  name   team  score  age  team_mean            결과 (자기 팀 평균보다 나이 많음)
0    A    red   80.0   25       34.0            1    B   blue   32 > 30
1    B   blue   90.0   32       30.0            2    C    red   41 > 34
2    C    red   70.0   41       34.0            4    E    red   36 > 34
3    D   blue    NaN   28       30.0
4    E    red   60.0   36       34.0
5    F  green   85.0   30       30.0            ← F는 30 = 30이라 '보다 큰'에 안 들어감
```

| | `groupby().mean()` | `groupby().transform('mean')` |
|---|---|---|
| 결과 행 수 | 그룹 수 (3) | 원본 행 수 (6) |
| 쓰는 때 | 그룹별 결과 자체가 답일 때 | **행마다 자기 그룹과 비교**할 때 |

> 문제에 **"자신이 속한 ○○의 평균보다"**, **"그룹 평균 이상인 행"** → transform

---

## 6. 두 컬럼으로 나누기 + reset_index

```python
t2 = t.copy()
t2['grade'] = ['x', 'x', 'y', 'y', 'y', 'x']                # 예제용 컬럼 하나 추가

t2.groupby(['team', 'grade'])['age'].mean()                 # 리스트로 두 컬럼
t2.groupby(['team', 'grade'])['age'].mean().reset_index()   # 이름표를 일반 컬럼으로
```

```
team   grade                       team grade   age
blue   x        32.0          0   blue     x  32.0
       y        28.0          1   blue     y  28.0
green  x        30.0    →     2  green     x  30.0
red    x        25.0          3    red     x  25.0
       y        38.5          4    red     y  38.5
```

> 이름표가 두 겹이라 헷갈리면 `reset_index()`로 평범한 표로 만든 뒤 Day 1 방식(필터·정렬·iloc)으로 푼다.
> `reset_index()` (drop 없이) → 이름표가 **컬럼으로 살아남는다**. `reset_index(drop=True)` → 이름표를 **버린다**. groupby 결과에는 drop 없이 쓴다.

---

## 7. 그룹별 상위 N개 — 정렬 먼저, 그다음 groupby().head(N)

"각 팀에서 나이가 가장 많은 1명"

```python
t.sort_values('age', ascending=False).groupby('team').head(1)
```

```
  name   team  score  age
2    C    red   70.0   41
1    B   blue   90.0   32
5    F  green   85.0   30
```

> 순서가 중요하다: **정렬 → groupby → head(N)**. 정렬 없이 하면 그냥 각 팀의 원래 앞쪽 N개가 나온다 (Day 1 Q6와 같은 실수).
> 결과는 원래 행들이 그대로 남은 DataFrame이라, 이어서 `['score'].mean()` 같은 계산을 붙이면 된다.

---

## 8. 그룹별 최빈값 — mode는 바로 안 된다 (지난번 오답)

```python
t.groupby('team')['score'].mode()                         # ❌ 에러: SeriesGroupBy에 mode 없음
t.groupby('team')['name'].agg(lambda x: x.mode()[0])     # ✅ 그룹별 최빈값 1개
```

> 시험에 자주 나오지는 않는다. 에러가 나면 "아 lambda로 감싸야 했지"만 떠올리면 된다.

---

## 오늘의 함정 요약

| 함정 | 기억할 한 줄 |
|---|---|
| groupby 결과는 이름순 정렬 | N번째 큰 그룹 → `sort_values(ascending=False).iloc[N-1]` |
| 건수인데 `count()` | 결측 있는 컬럼은 줄어든다. 건수 → `size()` |
| 그룹 값과 행 비교 | `transform` 으로 원본 행 수 맞추기 |
| 그룹별 상위 N | **정렬 먼저** → `groupby().head(N)` |
| 그룹 **이름**을 묻는지 **값**을 묻는지 | 이름 → `idxmax()` / `index[0]`, 값 → `max()` / `iloc[0]` |
| "정수로" / "소수 N째 자리" | `int()` / `round(x, N)` — Day 1에서 두 번 빠뜨림 ⚠️ |

---

# 연습문제 (8문제)

## 데이터 세팅

```python
import pandas as pd
df = pd.read_csv('retake/data/day2_orders.csv')
```

온라인 쇼핑몰 주문 40건. 컬럼:

| 컬럼 | 뜻 |
|---|---|
| `order_id` | 주문 번호 |
| `region` | 지역 (서울·경기·부산·대구·광주) |
| `category` | 상품 분류 (식품·의류·가전·도서) |
| `member` | 회원 여부 (`Y` / `N`) |
| `price` | 단가 |
| `qty` | 수량 |
| `rating` | 평점 (1~5, **결측 있음**) |

> 풀이 방법: `workspace/day2.py`에 풀고 "채점해줘"라고 말하기.
> 각 문제는 **원본 df에서 시작**한다. 단, Q4 이후에 쓰는 `amount` 컬럼은 Q4에서 만든 것을 그대로 써도 된다.
> 답에 **이름**과 **값**을 둘 다 묻는 문제가 있다. 문제를 끝까지 읽는다.

---

### Q1. (기본) 주문 건수가 가장 많은 지역(`region`)의 **이름**과 **건수**를 출력하라.

### Q2. (기본) 상품 분류(`category`)별 `price` 평균을 구했을 때, 평균이 가장 높은 분류의 **이름**과 그 평균을 **정수**로 출력하라.

### Q3. (기본) 전체 주문 중 `category`가 '식품'인 주문의 **비율**을 소수 셋째 자리까지 반올림해 출력하라.

### Q4. (응용) `price × qty`로 주문 금액 컬럼 `amount`를 만들어라. 지역별 `amount` 합계를 구했을 때, **2번째로 큰** 지역의 **이름**과 **합계**를 출력하라.

### Q5. (응용) 분류별로 **주문 건수**와 `rating` **평균**을 구하라. 주문 건수가 **10건 이상**인 분류 중 `rating` 평균이 **가장 낮은** 분류의 **이름**을 출력하라.
> 주문 건수 = 그 분류의 주문 행 수 (rating이 비어 있는 주문도 1건이다)

### Q6. (응용) 각 주문의 `price`가 **자신이 속한 지역**의 `price` 평균보다 **큰** 주문은 몇 건인가?

### Q7. (복합) 회원(`member == 'Y'`) 주문만 사용한다. 지역별로 주문 건수와 `rating` 평균을 구하고, **주문 건수가 5건 이상**인 지역 중 `rating` 평균이 **가장 낮은** 지역의 **이름**과 그 평균을 소수 둘째 자리까지 반올림해 출력하라.

### Q8. (복합) Q4의 `amount`를 사용한다. **각 분류에서 `amount`가 큰 순으로 2건씩** 뽑아라 (총 8건). 이 8건의 `amount` 평균을 **정수**로 출력하라.

---

## 채점 결과 — 8 / 8 정답 (Q6 △ → 재풀이 ✅) (2026-11-20)

| # | 내 답 | 정답 | 결과 |
|---|---|---|---|
| Q1 | 서울, 14 | 서울, 14 | ✅ (풀이 중 `qty` 합계 → `value_counts`로 고침) |
| Q2 | 가전, 159514 | 가전, 159514 | ✅ (풀이 중 `int()` 누락 → 고침) |
| Q3 | 0.3 | 0.3 | ✅ |
| Q4 | 경기, 1352900 | 경기, 1352900 | ✅ |
| Q5 | 의류 | 의류 | ✅ (count 컬럼 선택 주의 — 아래) |
| Q6 | 10 | 10 | △ → ✅ `>=` 사용 → 재풀이에서 `>`로 고침 |
| Q7 | 경기, 3.17 | 경기, 3.17 | ✅ |
| Q8 | 326712 | 326712 | ✅ |

### Q1 ✅ — 풀이 과정에서 한 번 틀렸던 것
```python
# 처음 풀이 ❌ — 지역별 "수량 합계"(서울 48). 건수가 아님. 1등 이름만 우연히 같았다
df.groupby('region')['qty'].sum().sort_values(ascending=False).reset_index()

# 최종 ✅
print(df['region'].value_counts().idxmax())   # 서울
print(df['region'].value_counts().max())      # 14
```
> **건수 = 행 수** → `value_counts()` / `size()`. 컬럼 값을 더하는 `sum()`이 아니다.

### Q2 ✅ — 처음엔 △였던 것
```python
# 처음 풀이 △ — Index(['가전'], ...) [159514.28571429] : 목록 통째 + int() 없음
d2 = df.groupby('category')['price'].mean().sort_values(ascending=False).head(1)
print(d2.index, d2.values)

# 최종 ✅
print(df.groupby('category')['price'].mean().idxmax())        # 가전
print(int(df.groupby('category')['price'].mean().max()))      # 159514
```

### Q3 ✅
```python
print(round(df['category'].value_counts(normalize=True)['식품'], 3))   # 0.3
```

### Q4 ✅
```python
df['amount'] = df['price'] * df['qty']
print(df.groupby('region')['amount'].sum().sort_values(ascending=False).index[1])   # 경기
print(df.groupby('region')['amount'].sum().sort_values(ascending=False).iloc[1])    # 1352900
```

### Q5 ✅ — 정답이지만 count 컬럼을 고를 때 주의
```python
q5 = df.groupby('category').agg(qty_count=('qty', 'count'), rating_mean=('rating', 'mean'))
q5 = q5.sort_values('rating_mean', ascending=True).reset_index()
print(q5[q5['qty_count'] >= 10]['category'].iloc[0])   # 의류
```
> `qty`에는 결측이 없어서 `count` = 행 수가 되어 맞았다. **같은 코드를 `('rating', 'count')`로 썼다면 답이 '식품'으로 바뀐다** (도서 10건 중 rating 있는 건 7건).
>
> | 분류 | `size` (주문 건수) | `rating` count |
> |---|---|---|
> | 도서 | **10** | 7 |
> | 의류 | **11** | 9 |
>
> 건수를 셀 땐 **`size`**가 가장 안전하다: `cnt=('order_id', 'size')`

### Q6 △ — 답은 맞았지만 부등호가 다름
```python
# 내 풀이
df['price_mean'] = df.groupby('region')['price'].transform('mean')
print(len(df[df['price'] >= df['price_mean']]))   # 10

# 모범답안 — 문제는 "평균보다 큰" → >
print(len(df[df['price'] > df['price_mean']]))    # 10
```
> 재풀이 ✅ (2026-11-20): `>`로 고침.
>
> 이 데이터는 평균과 똑같은 price가 0건이라 우연히 같았다. **"크다/초과" → `>`, "이상" → `>=`, "작다/미만" → `<`, "이하" → `<=`**

### Q7 ✅
```python
q7 = df[df['member'] == 'Y']
q7 = q7.groupby('region').agg(주문건수=('qty', 'count'), rating평균=('rating', 'mean'))
q7 = q7.sort_values('rating평균', ascending=False)
q7 = q7[q7['주문건수'] >= 5]
print(q7.index[-1])                          # 경기
print(round(q7.iloc[-1]['rating평균'], 2))    # 3.17
```
> 내림차순 정렬 후 `[-1]`(맨 끝)로 최솟값을 꺼냈다. 맞는 방법이다. 오름차순 + `[0]` 또는 `idxmin()`도 같다.

### Q8 ✅
```python
print(int(df.sort_values('amount', ascending=False).groupby('category')['amount'].head(2).mean()))   # 326712
```
> **정렬 → groupby → head(2)** 순서 정확 👍

---

### 개념 공부 중 나온 질문 (실행으로 확인)

| 질문 | 답 |
|---|---|
| `reset_index()` = Series → DataFrame? | 결과는 그렇다. 본래 하는 일은 **이름표(그룹 이름)를 컬럼으로 꺼내는 것** |
| 컬럼이 하나인데 왜 Series? | 왼쪽 team·grade는 컬럼이 아니라 **이름표**. 값은 age 한 줄 |
| groupby 먼저, 정렬 나중이면? | 그룹별 "원래 앞쪽 N개"를 정렬만 한 것 → 틀림. `groupby().sort_values()`는 에러 |
| `agg(lambda x: ...)`의 x는 컬럼 전체? | 아니다. **그룹 하나의 조각**이 그룹 수만큼 한 번씩 들어간다 |
| `value_counts().index[0]` = 최빈값? | 맞다. 단 동점일 때 `mode()`는 가나다순, value_counts는 먼저 나온 순 |
| `iloc[0]` vs `values[0]` | 값 하나는 같다. 여러 개 꺼내면 iloc은 이름표 유지, values는 배열만 |
| `groupby('team')['score'].loc['red']` 에러 | **계산(`.mean()`) 전**이라 표가 아님 → `...mean().loc['red']` |
| `iloc[0, ['region','qty']]` 에러 | iloc은 열도 **번호만**. 이름은 `loc[0, [...]]` 또는 `iloc[0][[...]]` |
| `groupby().head(1)`인데 왜 여러 행? | **그룹마다** 1개. 행 수 = 그룹 수 × N |
| `groupby()['amount'].head(2)` 이름표가 category가 아님 | head는 **고르기** → 원래 행 번호 유지. 집계(sum·mean)만 그룹 이름이 이름표 |

> 참고: 개념 8번에서 red 팀 score [80, 70, 60]은 모두 1번씩이라 `mode()`가 세 값을 다 돌려주고, `[0]`으로 가장 작은 **60**이 나왔다.
