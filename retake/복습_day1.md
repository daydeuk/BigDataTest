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
