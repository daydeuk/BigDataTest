# Day 3 시작 전 10분 복습 — Day 2 오답 · 어려웠던 것

> 답을 보기 전에 머릿속으로(또는 직접 쳐서) 먼저 떠올려 본다.

---

## 1. 내가 틀린 것 · 헷갈린 것

| # | 실수 | 기억할 한 줄 |
|---|---|---|
| 1 | "주문 **건수**"인데 `qty`를 **sum** (Q1) — 지난번에도 한 실수 ⚠️ | 건수 = 행 수 → `value_counts()` / `size()` |
| 2 | `print(d2.index, d2.values)` + `int()` 누락 (Q2) — **3번째** ⚠️ | 값 하나 → `index[0]` / `iloc[0]`, "정수" → `int()` |
| 3 | "평균보다 **큰**"인데 `>=` (Q6) | 크다 `>` · 이상 `>=` · 작다 `<` · 이하 `<=` |
| 4 | `groupby('team')['score'].loc['red']` → 에러 | groupby 뒤엔 **계산(`.mean()`)부터** |
| 5 | `iloc[0, ['region', 'qty']]` → 에러 | iloc은 열도 **번호만** → `loc[0, [...]]` |

---

## 2. ⭐ 내가 `**` 표시한 어려웠던 것 3개

### ① 그룹별 최빈값 (Day 2 개념 8 — "중요 까먹기 쉬움")

```python
df.groupby('team')['fruit'].mode()                       # ❌ AttributeError
df.groupby('team')['fruit'].agg(lambda x: x.mode()[0])  # ✅
```

외우는 순서 3단계:
1. x.mode()[0] : 최빈값
2. lambda x: x.mode()[0]
3. .agg(lambda x: x.mode()[0])

| 단계 | 코드 | 뜻 |
|---|---|---|
| 1 | `x.mode()[0]` | Series 하나의 최빈값 (mode는 목록으로 나오니 `[0]`) |
| 2 | `lambda x: x.mode()[0]` | "x를 받아서 x.mode()[0]을 돌려줘" |
| 3 | `.agg(lambda x: x.mode()[0])` | 그룹 **조각마다** x로 넣어서 실행 |

> lambda가 기억 안 나면: `lambda x: x.value_counts().index[0]`도 같은 답 (동점만 아니면)

---

### ② 비율 구하기 (Day 2 Q3 — "어려움")

"전체 중 '식품'의 **비율**" = 식품 건수 ÷ 전체 건수. **모두 0.3**으로 같다 (실행 확인).

| 방법 | 코드 | 생각하는 순서 |
|---|---|---|
| A | `df['category'].value_counts(normalize=True)['식품']` | normalize=True → 개수 대신 비율표 → '식품' 꺼내기 |
| B ⭐ | `len(df[df['category'] == '식품']) / len(df)` | **식품 행 수 ÷ 전체 행 수** (Day 1 필터 그대로) |
| C | `(df['category'] == '식품').mean()` | True=1, False=0의 평균 = True 비율 |

> **B가 가장 직관적이다.** normalize가 기억 안 나면 B로 푼다. 마지막에 `round(..., 3)` 잊지 않기.
>
> 응용: "회원 중 식품 비율" → 분모가 **회원 수**로 바뀐다
> ```python
> m = df[df['member'] == 'Y']
> len(m[m['category'] == '식품']) / len(m)    # 0.375 (회원 24명 중 9명)
> ```
> 비율 문제는 **"무엇 중에서?"(분모)**를 먼저 확인한다.

---

### ③ 필터를 loc로 쓰기 (Day 1 Q4 — "loc로는 어떻게 풀어야할지 모르겠음")

`df[조건]`과 `df.loc[조건]`은 **같은 결과**다. loc 대괄호의 **행 자리**에 조건을 넣으면 된다.

```python
d = df.drop_duplicates()
cond = (d['dept'] == '개발') & (d['age'] >= 30)

len(d[cond])                 # 7 — Day 1 방식
len(d.loc[cond])             # 7 — loc 방식 (행 자리에 조건)
d.loc[cond, 'id'].count()    # 7 — 행엔 조건, 열엔 컬럼 이름
cond.sum()                   # 7 — True 개수
```

| 모양 | 뜻 |
|---|---|
| `d.loc[조건]` | 조건에 맞는 행 전체 |
| `d.loc[조건, '컬럼']` | 조건에 맞는 행의 **그 컬럼만** |
| `d.loc[조건, ['컬럼1', '컬럼2']]` | 여러 컬럼 |

> 언제 loc를 쓰나: **조건 + 특정 컬럼**을 한 번에 고를 때 (`d.loc[cond, 'salary'].mean()`), 그리고 **값을 바꿀 때** (`d.loc[cond, 'salary'] = 0`).
> 개수만 셀 때는 `len(d[cond])`로 충분하다.

---

### ④ ⭐ 필터 결과는 일단 변수에 담는다 (셀프 퀴즈 Q4에서 나온 습관)

```python
s = df[df['region'] == '서울']                     # ① 필터 결과를 변수에
print(len(s))                                       # ② 중간 확인 → 14
round(len(s[s['category'] == '가전']) / len(s), 3)  # ③ 분자도 s, 분모도 s → 0.214
```

| 왜 | 설명 |
|---|---|
| 같은 표를 두 번 쓴다 | 비율 = 분자·분모 모두 "서울 주문". 변수 없으면 긴 필터를 두 번 쳐야 하고 오타 위험 2배 |
| 안쪽 조건도 같은 표여야 한다 | `s[df['category'] == '가전']` ❌ 바깥은 서울만(14행), 안쪽은 전체(40행) → 섞임 |
| 중간 확인 | 시험장은 한 줄씩 실행이 안 된다 → 변수에 담아 `print(len(s))` |

| 상황 | 변수로 빼기 |
|---|---|
| 같은 필터 결과를 **두 번 이상** 씀 | ✅ 꼭 |
| 필터 → 정렬 → 꺼내기, **단계 3개 이상** | ✅ 추천 |
| `len(df[조건])` 한 번에 끝남 | 한 줄도 OK |

> 오타 방지: 괄호·따옴표는 **열면 바로 닫고** 안을 채운다. `df[df'region' == '서울]` ❌ → `df[df['region'] == '서울']` ✅

---

## 3. 1분 셀프 퀴즈

<details>
<summary>Q1. 지역별 주문 건수 중 2번째로 많은 지역 이름</summary>
A. df['region'].value_counts().index[1]
```python
df['region'].value_counts().index[1]
```
value_counts는 이미 많은 순 → 2번째 = `index[1]`
</details>

<details>
<summary>Q2. 분류별 rating 평균이 가장 낮은 분류 이름</summary>
A. df.groupby('category')['rating'].mean().sort_values(ascending=False).index[-1]

```python
df.groupby('category')['rating'].mean().idxmin()
```
</details>

<details>
<summary>Q3. 각 주문의 qty가 자기 분류의 qty 평균 이상인 주문 수</summary>

A. df['qty_mean'] = df.groupby('category')['qty'].transform('mean');
len(df[df['qty'] >= df['qty_mean']])


```python
df['qm'] = df.groupby('category')['qty'].transform('mean')
len(df[df['qty'] >= df['qm']])
```
"이상" → `>=`
</details>

<details>
<summary>Q4. 서울 주문 중 가전의 비율 (소수 셋째)</summary>
s = df[df['region'] == '서울']
A. round(s['category'].value_counts(normalize=True)['가전'],3)


```python
s = df[df['region'] == '서울']
round(len(s[s['category'] == '가전']) / len(s), 3)
```
분모 = 서울 주문 수
</details>

<details>
<summary>Q5. 지역별 최빈 분류(category)</summary>
A. df.groupby('region')['category'].agg(lambda x:x.mode()[0])






```python
df.groupby('region')['category'].agg(lambda x: x.mode()[0])
```
</details>

### 셀프 퀴즈 채점 — 3 / 5 → 재풀이 5 / 5 ✅ (2026-11-20)

| # | 내 답 | 결과 | 원인 |
|---|---|---|---|
| Q1 | `value_counts().index[1]` → 경기 | ✅ | |
| Q2 | `...mean().sort_values(ascending=False).index[-1]` → 의류 | ✅ | 내림차순의 맨 끝 = 최솟값. `idxmin()`이 더 짧다 |
| Q3 | `df.groupby('order')['qty'].mean()` | ❌ | ① 그룹 기준이 `'category'`가 아님 (KeyError) ② **`mean()` → 4행**이라 40행과 비교 불가 → `transform('mean')` ③ `'qty_mean` 따옴표 안 닫힘 |
| Q4 | `df[...].values_counts(normalize=True)[df['category']=='가전']` | ❌ | ① `values_counts` 오타 (`value_counts`) ② 컬럼(`['category']`) 선택 없이 표 전체에 씀 ③ 비율표에서 꺼낼 땐 조건이 아니라 **이름** `['가전']` ④ `round(…, 3)` 없음 |
| Q5 | `agg(lambda x: x.mode()[0])` | ✅ | 어려웠던 것 ① 성공 👍 |

**Q3 — transform 을 또 놓침 (지난번 Day 9에도 같은 실수 ⚠️)**

```python
df['qm'] = df.groupby('category')['qty'].transform('mean')   # 40행 — 각 행 옆에 자기 분류 평균
len(df[df['qty'] >= df['qm']])                                # 18
```

> "**자기** ○○의 평균과 비교" → `transform`. `mean()`은 그룹 수만큼(4행)만 나온다.

**Q4 — 내 아이디어(normalize)를 살려서 고치면**

```python
s = df[df['region'] == '서울']                                   # ① 서울만
round(s['category'].value_counts(normalize=True)['가전'], 3)     # ② category 비율표 → '가전' → 0.214
round(len(s[s['category'] == '가전']) / len(s), 3)              # 방법 B — 같은 답 0.214
```

> 한 줄에 다 넣으려다 꼬였다. **필터 결과를 변수(`s`)에 담고 → 다음 줄에서 계산**하면 실수가 줄어든다.

**md에 적은 재풀이 (2026-11-20) — 실행해 보니 아직 둘 다 에러**

| # | 재풀이 | 실행 결과 | 남은 실수 |
|---|---|---|---|
| Q3 | `df.groupby('order')['qty'].transform('mean')` | 💥 KeyError: 'order' | transform ✅ 고침. **그룹 기준** `'order'` → `'category'` (고치면 18 ✅) |
| Q4 | `s = df[df['region'] == '서울]` / `s['cateogry']...` | 💥 SyntaxError, KeyError: 'cateogry' | 변수로 빼기 ✅ 고침. **`'서울` 따옴표**, **`cateogry` 철자** (고치면 0.214 ✅) |

**오타 수정 후 재채점 — 5 / 5 ✅** (md 답을 그대로 실행: Q1 경기, Q2 의류, Q3 18, Q4 0.214, Q5 ✅)

> 생각(transform, 변수로 빼기)은 다 맞게 고쳤다. 남은 건 **오타 3개**였다 — md에선 안 보이고 실행하면 바로 보인다 → 그래서 복습도 `workspace/review_day2.py`로 푼다.

---

다 봤으면 → Day 3으로.
