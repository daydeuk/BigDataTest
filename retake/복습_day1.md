# Day 2 시작 전 10분 복습 — Day 1 오답 · 핵심

> Day 2를 시작하기 전에 이 파일부터 본다. **답을 보기 전에 머릿속으로(또는 직접 쳐서) 먼저 떠올려 본다.**

---

## 1. 내가 틀린 것 3가지

| # | 실수 | 기억할 한 줄 |
|---|---|---|
| 1 | "상위 5명"인데 **정렬 없이** `head(5)` (Q6) | 상위 N개 = **`sort_values(..., ascending=False).head(N)`** |
| 2 | salary를 구해야 하는데 **score** 평균, 정렬도 **age** 대신 **salary** (Q6, Q8) | 다 풀면 문제 다시 읽기: **어느 컬럼의 / 무엇을 / 어떤 형식으로** |
| 3 | "정수로"인데 `int()` 빠뜨림 — **두 번 연속** ⚠️ (Q6) | **"정수" → `int()`**, **"소수 N째 자리" → `round(x, N)`** |

---

## 2. 핵심 개념 5개

### ① 숫자(순서)는 `iloc`, 조건과 이름은 `loc`
```python
s = df.sort_values('salary', ascending=False)
s.iloc[0]        # ✅ 맨 위 줄 = salary 1등
s.loc[0]         # ❌ 이름표가 0인 행 = 1등이 아닐 수 있음 (에러 없이 틀림)
```
> 정렬·필터·중복 제거·결측 제거를 하면 **이름표가 섞이거나 빈다.** N번째 → `iloc[N-1]`

### ② `idxmax()`는 이름표를 준다 → `loc`으로 꺼낸다
```python
df.loc[df['salary'].idxmax(), 'id']
```

### ③ 값을 바꿀 땐 대괄호 하나에 `[행, 열]`
```python
df.loc[df['age'] >= 30, 'salary'] = 0   # ✅ 원본 바뀜
df[df['age'] >= 30]['salary'] = 0       # ❌ 원본 그대로 + 경고
```

### ④ 필터·중복 제거 결과에 값을 바꿀 땐 `.copy()`
```python
d = df.drop_duplicates().copy()
d['salary'] = d['salary'].fillna(d['salary'].median())
```

### ⑤ 철자 주의: `duplicated()` / `drop_duplicates()`
```python
df.duplicated().sum()     # 중복 행 개수
df = df.drop_duplicates() # 중복 제거 (재할당 필수!)
```

### ⑥ ⭐ 중요 — `isin`: "이 중에 하나라도 해당하면" (복습 때 생소했던 것)

**한 줄 뜻**: 컬럼 값이 **목록 안에 들어 있으면 True**, 없으면 False.

```python
df['city'].isin(['서울', '부산'])          # 각 행: city가 서울 또는 부산이면 True
df[df['city'].isin(['서울', '부산'])]      # True인 행만 남기기 (필터)
df[~df['city'].isin(['서울', '부산'])]     # ~ 를 붙이면 반대: 서울도 부산도 아닌 행
```

실제 결과 (Day 1 데이터 앞 10행):

```
  city   isin  ~isin
0   서울   True  False
1   대구  False   True
2   서울   True  False
3   부산   True  False
...
7   인천  False   True
8  NaN  False   True     ← 결측도 "목록에 없음" → ~isin에서는 True로 잡힌다!
```

**`|` 를 여러 번 쓰는 것과 결과가 같다** (둘 다 19명)

| 방법 | 코드 | 비고 |
|---|---|---|
| `\|` 여러 번 | `df[(df['city'] == '서울') \| (df['city'] == '부산')]` | 값이 많아지면 길어지고 괄호 실수 |
| `isin` ✅ | `df[df['city'].isin(['서울', '부산'])]` | 값이 3개, 4개여도 목록에 추가만 |

**다른 조건과 같이 쓸 때** — isin 덩어리도 하나의 조건이다

```python
df[df['city'].isin(['서울', '부산']) & (df['age'] >= 30)]
#  ↑ isin은 괄호 없어도 됨            ↑ 비교(>=)는 괄호 필수
```

> **함정 3가지**
> 1. **대괄호(목록) 필수**: `isin('서울')` → `TypeError: only list-like objects are allowed`. 값이 하나여도 `isin(['서울'])` (값 하나면 그냥 `== '서울'`이 편하다)
> 2. **`~isin`은 결측(NaN)도 포함**한다. "서울·부산이 아닌 도시"인데 도시가 비어 있는 사람은 빼야 하면 `& df['city'].notna()` 추가
> 3. `in`(파이썬)과 헷갈리지 말기: `df['city'] in ['서울']` ❌ → pandas 컬럼은 `.isin([...])`

#### isin 연습문제 (6문제) — `workspace/day1_isin.py`에 풀기

Day 1 데이터(`retake/data/day1_employees.csv`)를 쓴다.

| # | 문제 |
|---|---|
| I1 | (기본) 원본에서 `city`가 서울·부산·대구 중 하나인 직원 수 |
| I2 | (기본) 원본에서 `dept`가 '개발'도 '영업'도 **아닌** 직원 수 |
| I3 | (함정) 원본에서 `city`가 서울도 부산도 **아닌** 직원 수. 단, **도시가 비어 있는 직원은 제외** |
| I4 | (응용) 중복 제거 후, `city`가 서울 또는 부산이면서 나이 30세 이상인 직원의 `salary` 평균 (소수 둘째 자리) |
| I5 | (응용) 중복 제거 후, `id`가 E003, E007, E012인 직원의 `salary` 합계를 **정수**로 |
| I6 | (복합) 중복 제거 후, `dept`가 '개발' 또는 '인사'이고 성별이 'F'인 직원 중 `score`가 가장 높은 직원의 `id` |

<details>
<summary>정답 보기 (다 풀고 열기)</summary>

| # | 정답 | 모범답안 |
|---|---|---|
| I1 | 24 | `len(df[df['city'].isin(['서울', '부산', '대구'])])` |
| I2 | 18 | `len(df[~df['dept'].isin(['개발', '영업'])])` |
| I3 | 12 | `len(df[~df['city'].isin(['서울', '부산']) & df['city'].notna()])` — notna 빼면 **14** (결측 2명 포함) |
| I4 | 5196.67 | `round(d[d['city'].isin(['서울', '부산']) & (d['age'] >= 30)]['salary'].mean(), 2)` |
| I5 | 9540 | `int(d[d['id'].isin(['E003', 'E007', 'E012'])]['salary'].sum())` — E007은 salary가 NaN이라 합계에서 빠진다 |
| I6 | E008 | `d[d['dept'].isin(['개발', '인사']) & (d['gender'] == 'F')].sort_values('score', ascending=False).iloc[0]['id']` |

(`d = df.drop_duplicates()`)
</details>

#### isin 채점 결과 — 3 / 6 (2026-11-17)

| # | 내 답 | 정답 | 결과 | 원인 |
|---|---|---|---|---|
| I1 | 33 | 24 | ❌ | `len(df['city'].isin(...))` — `df[ ]` 껍데기 없음 → 전체 행 수 |
| I2 | 33 | 18 | ❌ | 같은 원인 + 목록에 '개발' 대신 **'서울'** 오타 |
| I3 | 12 | 12 | ✅ | `dropna` + `!=` 두 개로 풂 (isin 안 썼지만 정답. 결측을 먼저 뺀 게 좋았다) |
| I4 | 5196.67 | 5196.67 | ✅ | |
| I5 | 9540 | 9540 | ✅ | `int()` 챙김 👍 |
| I6 | E003 | E008 | ❌ | 정렬 후 `loc[0]` → 이름표 0 = 3등 (Day 1 개념 ① **반복 ⚠️**) |

**⭐ 오늘의 핵심: `isin(...)` 자체는 "필터"가 아니라 True/False 목록이다**

| 코드 | 결과 | 뜻 |
|---|---|---|
| `df['city'].isin([...])` | 33칸 True/False | 조건표만 만든 것 |
| `len(df['city'].isin([...]))` | **33** ❌ | 조건표의 칸 수 = 전체 행 수 |
| `df[df['city'].isin([...])]` | 24행 DataFrame | `df[ ]`로 감싸야 **걸러진다** |
| `len(df[df['city'].isin([...])])` | **24** ✅ | 걸러진 행 수 |
| `df['city'].isin([...]).sum()` | **24** ✅ | True=1, False=0으로 더함 |

**I6 정렬 결과 (이름표가 따라다님)**

```
      id  score
26  E008   96.0   ← iloc[0] ✅ (맨 위 줄)
8   E030   88.0
0   E003   85.0   ← loc[0]  ❌ (이름표가 0)
```

#### 재풀이 — 6 / 6 ✅ (2026-11-17)

```python
# I1 ✅ 24 — True 개수를 sum
print(df['city'].isin(['서울', '부산', '대구']).sum())

# I2 ✅ 18 — '서울' → '개발'로 고치고 df[ ]로 감쌈
print(len(df[~df['dept'].isin(['개발', '영업'])]))

# I6 ✅ E008 — reset_index(drop=True) 후 loc[0]
df = df[(df['dept'].isin(['개발', '인사'])) & (df['gender'] == 'F')].sort_values('score', ascending=False).reset_index(drop=True)
print(df.loc[0, 'id'])
```

**재풀이 과정에서 나온 질문 (실행으로 확인)**

| 질문 | 답 |
|---|---|
| 정렬 후 `loc[0]['id']`로 써도 틀려? | 틀린다 (E003). 행은 앞의 `loc[0]`에서 이미 정해짐. `iloc[0]` 또는 `reset_index(drop=True)` 후 `loc[0]` |
| `~...isin(...).sum()` 했더니 **-16**? | `.sum()`이 먼저 실행돼 15 → `~15` = -16. **`(~조건).sum()`** 처럼 괄호로 감싸야 18 |
| `len`으로 했는데 33? | `df[ ]` 껍데기가 없었음. `len(~조건)` → 33, `len(df[~조건])` → 18 |

> 헷갈리면 **`len(df[조건])` 하나만** 쓴다. Day 1 필터 모양 그대로라 괄호 실수가 적다.

---

## 3. 1분 셀프 퀴즈

머릿속으로 코드를 떠올린 다음 펼쳐서 확인한다.

<details>
<summary>Q1. salary가 2번째로 높은 사람의 id는?</summary>

```python
df.sort_values('salary', ascending=False).iloc[1]['id']
```
2번째 → `iloc[1]` (1을 뺀다)
</details>

<details>
<summary>Q2. city 결측치를 '없음'으로 채우기 (원본에 반영)</summary>

```python
df['city'] = df['city'].fillna('없음')
```
재할당(`df['city'] =`)을 빼먹으면 원본 그대로
</details>

<details>
<summary>Q3. 30세 미만인 사람의 score를 0으로 바꾸기</summary>

```python
df.loc[df['age'] < 30, 'score'] = 0
```
대괄호 하나에 `[조건, '컬럼']`
</details>

<details>
<summary>Q4. score 상위 3명의 salary 합계를 정수로</summary>

```python
int(df.sort_values('score', ascending=False).head(3)['salary'].sum())
```
상위 N개 = 정렬 + head / "정수" → `int()`
</details>

<details>
<summary>Q5. 부서가 '영업' 또는 '인사'인 사람 수</summary>

```python
len(df[df['dept'].isin(['영업', '인사'])])
```
</details>

---

다 봤으면 → [Day 2 — groupby · 집계](day2.md)로.
