# 재도전 Day 1 — 1유형 ① Pandas 기초 · 필터 · 결측치 · 중복

> 2026-11-15 (일) · 목표 2시간 · 개념 40분 → 연습문제 60분 → 오답 정리 10분

---

## 0. 시험 환경에서 꼭 알아둘 것

| 제약 | 그래서 어떻게 |
|------|------------|
| **자동완성 없음** | 함수 이름을 외워서 쳐야 한다. 오늘 나오는 함수는 전부 손으로 쳐 본다 |
| **한 줄씩 실행 불가** (전체 실행만) | 중간 확인은 `print()`로 한다. 다 풀고 나서 확인용 print는 지워도 되고 둬도 된다 |
| **실행 시간 1분 제한** | 1유형에선 걱정할 일 거의 없음 |
| `help()`, `dir()` 사용 가능 | 함수 이름이 기억 안 나면 `print(dir(pd.DataFrame))` |
| 1유형 답은 **별도 제출 화면에 값만 입력** | 코드 결과로 나온 숫자를 그대로 옮겨 적는다 |

---

## 1. 데이터 불러오기와 훑어보기

```python
import pandas as pd

df = pd.read_csv('retake/data/day1_employees.csv')

print(df.head())      # 앞 5행 (head(10)이면 10행)
print(df.shape)       # (행 수, 열 수) — 괄호 없음! 속성이다
print(df.info())      # 컬럼별 타입 + 결측 아닌 값 개수
print(df.describe())  # 숫자 컬럼 요약 (평균, 표준편차, 사분위수)
print(df.columns)     # 컬럼 이름 목록
```

> **시험 시작 루틴**: 문제를 받으면 `head()`, `shape`, `info()`를 먼저 찍어서 컬럼 이름과 결측치를 확인한다.
> `df.shape`에 괄호를 붙이면(`df.shape()`) 에러가 난다.

---

## 2. 컬럼 선택

```python
df['salary']              # 컬럼 1개 → Series
df[['dept', 'salary']]    # 컬럼 여러 개 → 대괄호 두 겹 → DataFrame
```

> 대괄호 두 겹(`[[ ]]`)을 빼먹는 실수가 많다. 바깥 `[]`는 선택, 안쪽 `[]`는 리스트다.

---

## 3. 조건 필터 ⭐ 1유형의 기본기

```python
# 조건 1개
df[df['age'] >= 30]

# 조건 여러 개: & (그리고), | (또는) — 각 조건을 반드시 괄호로 감싼다
df[(df['dept'] == '개발') & (df['age'] >= 30)]
df[(df['city'] == '서울') | (df['city'] == '부산')]

# 여러 값 중 하나: isin — | 를 여러 번 쓰는 것보다 깔끔
df[df['city'].isin(['서울', '부산'])]

# 반대 조건: ~
df[~df['city'].isin(['서울', '부산'])]
```

> **함정 3가지**
> - Python의 `and` / `or`는 pandas 필터에서 에러가 난다. 반드시 `&` / `|`
> - 조건마다 괄호 필수: `df['a'] > 1 & df['b'] < 2` ❌ → `(df['a'] > 1) & (df['b'] < 2)` ✅
> - 같다는 `==` (등호 두 개)

---

## 4. loc / iloc

```python
df.iloc[0]            # 첫 번째 행 (위치 번호 0)
df.iloc[0:3]          # 첫 번째 ~ 세 번째 행 (위치 번호 0, 1, 2 — 끝 번호 3은 포함 안 됨)
df.iloc[2]['salary']  # 세 번째 행 (위치 번호 2)의 salary

df.loc[df['age'] >= 30, 'salary']   # 조건으로 행 고르고 + 컬럼 고르기
```

| | 기준 | 언제 |
|---|---|---|
| `iloc` | **위치 번호** (0부터: 0, 1, 2...) | "N번째 값" 꺼낼 때 → `iloc[N-1]` |
| `loc` | **이름 / 조건** | 조건 + 컬럼을 한 번에 고를 때 |

### ⭐ loc과 iloc이 다른 결과를 내는 순간 — 정렬·필터 후 (사용자 질문에서 나온 핵심)

행 왼쪽의 숫자는 **이름표(인덱스)**다. 정렬하거나 필터해도 원래 번호를 그대로 들고 다닌다.

```
s = df[['id','age','salary']].head(5).sort_values('salary', ascending=False)

     id  age  salary
2  E002   36  7060.0    ← 맨 위 줄인데 이름표는 2
0  E003   59  6180.0    ← 두 번째 줄인데 이름표는 0
4  E014   30  4690.0
1  E029   52  3970.0
3  E010   23     NaN
```

| | 기준 | 비유 |
|---|---|---|
| `iloc` | **지금 몇 번째 줄인가** (위치) | 줄 선 순서 "앞에서 첫 번째 사람" |
| `loc` | **이름표에 뭐라고 적혀 있나** | "이름표 2번 달고 있는 사람" |

| 코드 | 의미 | 결과 |
|---|---|---|
| `s.iloc[0]` | 맨 위 **첫 번째 줄** | **E002** (salary 1등) ✅ |
| `s.loc[0]` | 이름표가 **0**인 행 | **E003** (salary 2등) ❌ |
| `s.iloc[2]` | 위에서 **세 번째 줄** | E014 |
| `s.loc[2]` | 이름표가 **2**인 행 | E002 |

> "salary 1등"을 물었는데 `loc[0]`을 쓰면 **2등이 답으로 나온다. 에러도 안 난다.**

**`reset_index(drop=True)`** = 이름표를 지금 줄 순서대로 0, 1, 2…로 새로 붙인다 → 그 뒤로는 `loc[0]`과 `iloc[0]`이 같아진다.

```
     id  age  salary
0  E002   36  7060.0    ← 이제 이름표 = 줄 순서
1  E003   59  6180.0
2  E014   30  4690.0
```

> **외우는 법: 숫자는 `iloc`, 조건은 `loc`.**
> 정렬 후 N번째 → `iloc[N-1]` / 조건 + 컬럼으로 고르기·바꾸기 → `loc[조건, '컬럼']`

### ⭐ 값을 바꿀 때는 대괄호 하나에 `[행, 열]` — `loc` 또는 `iloc` (사용자 질문에서 나온 핵심)

진짜 규칙은 "loc만 된다"가 아니라 **대괄호를 두 번 이어 붙이지 않는 것**이다.

```python
df.iloc[2, 5] = 0          # ✅ iloc도 OK — 세 번째 행, 위치 5번 컬럼(salary). 원본 바뀜
df.iloc[2]['salary'] = 0   # ❌ 대괄호 두 번 → 복사본만 바뀜 + 경고
```

> `iloc`은 컬럼도 **번호**로 써야 한다 (`df.columns.get_loc('salary')` → 5). 컬럼 번호를 세다 틀리기 쉬우니,
> 시험에서 값을 바꿀 땐 **컬럼 이름을 쓸 수 있는 `loc[조건, '컬럼']`이 가장 안전**하다.

```python
df.loc[df['age'] >= 30, 'salary']      # 꺼내 보기 — 아래와 결과 같음
df[df['age'] >= 30]['salary']          # 꺼내 보기 — 위와 결과 같음

df.loc[df['age'] >= 30, 'salary'] = 0  # ✅ 원본 df가 바뀜 (그 칸에 직접 써 넣기)
df[df['age'] >= 30]['salary'] = 0      # ❌ 복사본만 바뀌고 원본 그대로 + SettingWithCopyWarning
```

| 코드 모양 | 원본 df |
|---|---|
| `df.loc[조건, '컬럼'] = 값` (대괄호 하나) | ✅ 바뀜 |
| `df.iloc[행번호, 열번호] = 값` (대괄호 하나) | ✅ 바뀜 |
| `a = df.loc[...]` 다음에 `a`를 수정 | ❌ 안 바뀜 (a는 복사본) |
| `df[조건]['컬럼'] = 값` / `df.iloc[2]['컬럼'] = 값` (대괄호 두 번) | ❌ 안 바뀜 + 경고 |

> 경고는 에러가 아니라서 **답이 틀린 줄 모르고 넘어가기 쉽다.** 값을 바꿀 땐 `df.loc[조건, '컬럼'] = 값` 한 줄이 가장 안전.

---

## 5. 정렬과 N번째 값 꺼내기 ⭐ 시험 단골

```python
df.sort_values('salary')                     # 오름차순 (작은 값부터)
df.sort_values('salary', ascending=False)    # 내림차순 (큰 값부터)

# "salary가 3번째로 높은 사람의 age"
s = df.sort_values('salary', ascending=False).reset_index(drop=True)
print(s.iloc[2]['age'])     # 3번째 = 인덱스 2

# 상위 N개
df.sort_values('salary', ascending=False).head(5)
```

> "3번째" → `iloc[2]`. 0부터 세기 때문에 **항상 1을 뺀다.**
> `reset_index(drop=True)`는 정렬 후 인덱스를 0부터 다시 매긴다. `iloc`만 쓸 땐 없어도 되지만 습관처럼 붙이면 `loc`과 헷갈릴 일이 없다.

---

## 6. 결측치

```python
df.isnull().sum()              # 컬럼별 결측치 개수
df.isnull().sum().idxmax()     # 결측치가 가장 많은 컬럼 이름
df['salary'].isnull().sum()    # 특정 컬럼만

df = df.dropna()                     # 결측치가 하나라도 있는 행 삭제
df = df.dropna(subset=['salary'])    # salary가 결측인 행만 삭제

df['salary'] = df['salary'].fillna(df['salary'].mean())     # 평균으로 채우기
df['salary'] = df['salary'].fillna(df['salary'].median())   # 중앙값으로 채우기
df['city'] = df['city'].fillna('없음')                       # 문자로 채우기
```

> **재할당 필수!** `df.dropna()`만 쓰면 원본은 그대로다. `df = df.dropna()`로 다시 담아야 한다.
> (지난번 오답노트 단골)

---

## 7. 중복

```python
df.duplicated().sum()          # 완전히 똑같은 행의 개수 (첫 번째는 빼고 센다)
df = df.drop_duplicates()      # 중복 행 제거 (첫 번째만 남김)
df = df.drop_duplicates(subset=['id'])   # id가 같으면 중복으로 보고 제거
```

---

## 8. 출력 패턴 — 답을 정확하게 내는 법

```python
len(df)                     # 행 개수 (= df.shape[0])
round(x, 2)                 # 소수 둘째 자리까지 반올림 — 괄호 위치 주의!
int(x)                      # 정수로 (소수점 버림)
df['salary'].mean()         # 평균
df['salary'].sum()          # 합계
df['salary'].max()          # 최댓값
df['salary'].min()          # 최솟값
df['salary'].median()       # 중앙값
                            # ↑ 모두 결측치(NaN)는 빼고 계산한다

df['salary'].idxmax()       # 최댓값이 있는 행의 "이름표"(인덱스) — 위치가 아님!
df.loc[df['salary'].idxmax(), 'id']   # → 그래서 꺼낼 땐 iloc이 아니라 loc
```

> **"몇 명/몇 개"를 물으면 숫자 하나만 출력한다.** DataFrame을 통째로 출력하고 행 수를 눈으로 세면 실수한다 → `len()`
> `print(round(x), 2)` ❌ → `print(round(x, 2))` ✅

---

---

# 연습문제 (8문제)

## 데이터 세팅

```python
import pandas as pd
df = pd.read_csv('retake/data/day1_employees.csv')
```

직원 33행 데이터. 컬럼: `id`, `dept`(부서), `gender`, `age`, `city`, `salary`(연봉), `score`(평가 점수)

> 풀이 방법: 채팅에 코드를 붙이거나, `workspace/day1.py`에 저장하고 "채점해줘"라고 말하기.
> 각 문제는 **원본 df에서 새로 시작**한다 (Q4, Q5, Q6, Q7, Q8은 문제에 적힌 대로 중복 제거부터).

---

### Q1. (기본) 데이터의 행 수와 열 수를 각각 출력하라.

### Q2. (기본) 결측치가 가장 많은 컬럼의 **이름**을 출력하라.

### Q3. (기본) 완전히 중복된 행이 몇 개인지 출력하고, 중복을 제거한 뒤의 행 수를 출력하라.

### Q4. (응용) 중복을 제거한 데이터에서, 부서(`dept`)가 '개발'이면서 나이가 30세 이상인 직원은 몇 명인가?

### Q5. (응용) 중복을 제거한 데이터에서, `salary`의 결측치를 `salary`의 **중앙값**으로 채운 뒤 `salary`의 평균을 소수 둘째 자리까지 반올림해 출력하라.

### Q6. (응용) 중복을 제거한 데이터에서, `score`가 결측인 행을 삭제하라. 그다음 `score` 상위 5명의 `salary` 평균을 **정수**로 출력하라.

### Q7. (복합) 중복을 제거한 데이터에서, 도시가 '서울' 또는 '부산'이고 성별이 'F'인 직원 중 `salary`가 가장 높은 직원의 `id`를 출력하라.

### Q8. (복합) 중복 제거 → `salary` 결측 행 삭제 → 나이가 많은 순으로 정렬했을 때, **3번째로 나이가 많은** 직원의 `salary`를 출력하라.

---

## 채점 결과 — 6 / 8 (2026-11-16)

| Q | 결과 | 내 답 | 정답 |
|---|---|---|---|
| 1 | ✅ | 33, 7 | 33, 7 |
| 2 | ✅ | salary | salary |
| 3 | ✅ | 3, 30 | 3, 30 |
| 4 | ✅ | 7 | 7 |
| 5 | ✅ | 4660.33 | 4660.33 |
| 6 | ❌ | 74.0 | **4202** |
| 7 | ✅ | E002 | E002 |
| 8 | ❌ | 6300.0 | **5530.0** |

### Q1 ✅
```python
print(len(df))
print(df.shape[1])
```
> `print(df.shape[0], df.shape[1])`로 한 번에 써도 된다.

### Q2 ✅
```python
print(df.isnull().sum().idxmax())
```

### Q3 ✅
```python
print(df.duplicated().sum())
print(len(df.drop_duplicates()))
```
> 메모: `duplicated()`, `drop_duplicates()` 이름이 잘 생각나지 않았음 → 오답노트에 기록.

### Q4 ✅
```python
df4 = df.drop_duplicates()
print(len(df4[(df4['dept']=='개발') & (df4['age'] >= 30)]))
```
> "loc로는 어떻게?" → 개수만 셀 땐 loc이 필요 없다. 지금 방식이 정답이고 가장 일반적. (`len(df4.loc[조건])`도 결과는 같음)

### Q5 ✅ (경고 있음)
```python
df5 = df.drop_duplicates()
df5['salary'] = df5['salary'].fillna(df5['salary'].median())   # SettingWithCopyWarning
print(round(df5['salary'].mean(), 2))
```
> 답은 맞다. 필터·중복 제거 결과에 값을 바꿀 땐 `df.drop_duplicates().copy()`로 경고를 없앤다.

### Q6 ❌ — 정렬을 안 하고, salary 대신 score 평균을 냄
```python
# 내 풀이
df6 = df.drop_duplicates()
df6 = df6.dropna(subset=['score']).reset_index(drop=True)
print(df6['score'].head(5).mean())      # → 74.0
```
**틀린 곳 3개**
1. "score **상위** 5명"인데 정렬 없이 `head(5)` → 그냥 **맨 앞 5행**을 가져옴
2. 구해야 하는 건 **salary** 평균인데 **score** 평균을 냄
3. **정수**로 출력하라고 했는데 `int()` 없음

```python
# 모범답안
df6 = df.drop_duplicates()
df6 = df6.dropna(subset=['score'])
top5 = df6.sort_values('score', ascending=False).head(5)
print(int(top5['salary'].mean()))       # → 4202
```
> "상위 N개" = **`sort_values(..., ascending=False).head(N)`** 세트. 정렬 없는 head는 상위가 아니다.
> 다 쓰고 나서 **문제를 다시 읽고** "어느 컬럼의 무엇을, 어떤 형식으로"를 체크한다.

### Q7 ✅
```python
df7 = df.drop_duplicates()
print(df7.loc[df7[((df7['city'] == '서울') | (df7['city'] == '부산')) & (df7['gender']== 'F')]['salary'].idxmax(), 'id'])
```
> idxmax(이름표) → loc 짝을 정확히 썼다. 한 줄이 길어서 실수하기 쉬우니 나눠 쓰면 더 안전:
```python
f = df7[df7['city'].isin(['서울', '부산']) & (df7['gender'] == 'F')]
print(f.loc[f['salary'].idxmax(), 'id'])
```

### Q8 ❌ — 정렬 기준 컬럼이 틀림
```python
# 내 풀이
df8 = df.drop_duplicates()
df8 = df8.dropna(subset=['salary'])
df8 = df8.sort_values('salary', ascending=False).reset_index(drop=True)   # ← age로 정렬해야 함
print(df8.loc[2, 'salary'])             # → 6300.0
```
```python
# 모범답안
df8 = df.drop_duplicates()
df8 = df8.dropna(subset=['salary'])
df8 = df8.sort_values('age', ascending=False)
print(df8.iloc[2]['salary'])            # → 5530.0
```
> "**나이**가 많은 순" → `sort_values('age', ...)`. 정렬 기준과 출력 컬럼이 다른 문제는 둘을 헷갈리기 쉽다.
> 중복 제거 → 결측 제거 → 정렬 순서는 정확했다. reset_index 후 `loc[2]`도 맞는 방식이지만, N번째는 `iloc[N-1]`이 더 안전.

---

### 재풀이 (2026-11-16)

| Q | 결과 | 내 답 | 정답 |
|---|---|---|---|
| 6 | △ → ✅ | 4202.0 → 4202 | **4202** |
| 8 | ✅ | 5530.0 | 5530.0 |

```python
# Q6 재풀이 — 정렬 + salary 평균은 고쳤지만 int() 여전히 없음
df6 = df.drop_duplicates().copy()
df6 = df6.dropna(subset=['score']).sort_values('score', ascending=False).reset_index(drop=True)
print(df6['salary'].head(5).mean())     # → 4202.0  (정수 요구 → int() 필요)

# Q8 재풀이 ✅
df8 = df.drop_duplicates().copy()
df8 = df8.dropna(subset=['salary'])
df8 = df8.sort_values('age', ascending=False).reset_index(drop=True)
print(df8.loc[2, 'salary'])             # → 5530.0
```
> Q6: `4202.0`과 `4202`는 시험 답안 칸에서 다르게 채점될 수 있다. "정수로"가 보이면 `int()`를 반사적으로.

> Q6 재재풀이 ✅: `print(int(df6['salary'].head(5).mean()))` → 4202. **Day 1 최종 8/8.**
