# 9일차 — NumPy + 백분위수 + 복합 필터 패턴

## 개념 정리

### 1. NumPy 통계 함수 ★★

```python
import numpy as np

arr = [10, 20, 30, 40, 50]

np.mean(arr)      # 평균 → 30.0
np.median(arr)    # 중앙값 → 30.0
np.std(arr)       # 표준편차 (ddof=0, 모표준편차)
np.var(arr)       # 분산 (ddof=0)
np.sum(arr)       # 합계
np.min(arr)       # 최솟값
np.max(arr)       # 최댓값
```

> **pandas vs numpy 표준편차 기본값 차이**
> - `df['col'].std()` → `ddof=1` (표본표준편차, 시험 기본값)
> - `np.std(arr)` → `ddof=0` (모표준편차)
> - 시험에서 "표준편차"만 언급하면 pandas `.std()` (ddof=1) 사용

```python
# 명시적으로 ddof 지정
np.std(arr, ddof=1)    # 표본표준편차
np.std(arr, ddof=0)    # 모표준편차 (기본값)

df['col'].std(ddof=1)  # 표본표준편차 (기본값)
df['col'].std(ddof=0)  # 모표준편차
```

---

### 2. 백분위수 — `np.percentile` vs `quantile` ★★★

```python
# np.percentile — 0~100 범위
np.percentile(df['score'], 25)   # 25백분위수 (Q1)
np.percentile(df['score'], 75)   # 75백분위수 (Q3)
np.percentile(df['score'], 90)   # 90백분위수

# pandas quantile — 0~1 범위
df['score'].quantile(0.25)       # 25백분위수 (Q1)
df['score'].quantile(0.75)       # 75백분위수 (Q3)
df['score'].quantile(0.90)       # 90백분위수
```

> 둘 다 결과 동일. 시험에서 "90백분위수" → `quantile(0.9)` 또는 `np.percentile(arr, 90)` 둘 다 OK.

---

### 3. 백분위수 기반 필터 ★★★

```python
# 패턴 1: 백분위수 이하/이상 필터 → 집계
q25 = df['score'].quantile(0.25)
print(df[df['score'] <= q25]['salary'].mean())

# 패턴 2: 백분위수 범위 (IQR)
q10 = df['price'].quantile(0.10)
q90 = df['price'].quantile(0.90)
print(round(q90 - q10, 3))      # 90p - 10p 범위

# 패턴 3: 그룹별 백분위수 이상 필터 → 집계
p90 = df.groupby('group')['value'].quantile(0.9)
# p90은 그룹별 임계값 → transform으로 행별로 붙여서 필터
df['p90'] = df.groupby('group')['value'].transform(lambda x: x.quantile(0.9))
print(df[df['value'] >= df['p90']].groupby('group')['value'].mean())
```

---

### 4. 복합 필터 패턴 (이중 필터) ★★★

시험 빈출: 조건1로 필터 → 집계값 계산 → 그 값으로 다시 필터

```python
# 패턴: "평균 이상인 행만 뽑아서" → 추가 집계
mean_val = df['distance'].mean()
filtered = df[df['distance'] >= mean_val]
print(filtered['time'].std())

# 패턴: 그룹별 집계 → 조건 충족 그룹만 → 추가 집계
group_mean = df.groupby('dept')['salary'].mean()
valid_depts = group_mean[group_mean >= 5000].index
print(df[df['dept'].isin(valid_depts)]['score'].mean())
```

---

### 5. 최빈값 활용 패턴

```python
# 최빈값 추출
mode_val = df['col'].mode()[0]    # .mode()는 Series 반환 → [0]으로 값 추출

# 최빈값으로 필터
print(df[df['col'] == mode_val]['target'].mean())
```

> `.mode()[0]` — 최빈값이 여러 개면 첫 번째 반환. `[0]` 빠뜨리면 Series가 나와서 비교 불가.

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd
import numpy as np

data = {
    'name':      ['김민준', '이서연', '박지호', '최유진', '정승현',
                  '강민서', '윤지원', '장하은', '임도현', '한소율',
                  '오지훈', '신예린', '백준서', '류하람', '문지수'],
    'age':       [22, 35, 28, 45, 19, 52, 31, 27, 41, 38, 24, 33, 47, 29, 36],
    'gender':    ['M', 'F', 'M', 'F', 'M', 'F', 'F', 'M', 'M', 'F',
                  'M', 'F', 'M', 'F', 'F'],
    'score':     [88, 72, 95, 61, 45, 83, 77, 90, 55, 68, 92, 74, 58, 81, 66],
    'salary':    [3200, 4500, 3800, 5200, 2800, 6100, 4200, 3600, 4800, 4100,
                  3100, 4700, 5500, 3900, 4300],
    'distance':  [12.3, 8.7, 15.1, 5.4, 20.2, 9.8, 11.6, 7.3, 18.5, 13.2,
                  6.1, 14.8, 10.5, 16.7, 8.2],
    'dept':      ['개발', '마케팅', '개발', '인사', '개발', '마케팅', '인사',
                  '개발', '마케팅', '인사', '개발', '마케팅', '인사', '개발', '인사'],
    'smoker':    [0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0]
}
df = pd.DataFrame(data)
```

---

### Q1. score의 25백분위수와 75백분위수를 각각 소수 첫째 자리까지 출력하라. (`np.percentile`과 `quantile` 두 가지 방법으로 모두 작성하라.)

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
# np.percentile 방식
print(round(np.percentile(df['score'], 25), 1))
print(round(np.percentile(df['score'], 75), 1))

# pandas quantile 방식
print(round(df['score'].quantile(0.25), 1))
print(round(df['score'].quantile(0.75), 1))
```

> 결과 동일. 시험에서는 둘 다 사용 가능.

</details>

---

### Q2. distance가 전체 평균 이상인 직원들의 표본표준편차를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
mean_dist = df['distance'].mean()
filtered = df[df['distance'] >= mean_dist]
print(round(filtered['distance'].std(), 3))
```

> `std()` 기본값은 ddof=1 (표본표준편차). 시험에서 "표준편차"는 기본값 사용.

</details>

---

### Q3. smoker=1인 직원과 smoker=0인 직원 각각에서 salary의 90백분위수 이상인 직원의 salary 평균을 구하고, 그 차이의 절댓값을 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
smoker1 = df[df['smoker'] == 1]
smoker0 = df[df['smoker'] == 0]

p90_1 = smoker1['salary'].quantile(0.9)
p90_0 = smoker0['salary'].quantile(0.9)

mean1 = smoker1[smoker1['salary'] >= p90_1]['salary'].mean()
mean0 = smoker0[smoker0['salary'] >= p90_0]['salary'].mean()

print(round(abs(mean1 - mean0), 2))
```

</details>

---

### Q4. score의 최빈값을 구하고, score가 최빈값인 직원들의 salary 평균을 소수 둘째 자리까지 출력하라. 최빈값도 함께 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
mode_score = df['score'].mode()[0]
print(mode_score)
print(round(df[df['score'] == mode_score]['salary'].mean(), 2))
```

> `.mode()[0]` — 최빈값이 여러 개일 수 있으므로 `[0]`으로 첫 번째 값 추출.
> 이 데이터에서는 모든 score가 유일값이므로 최빈값이 여러 개 → 가장 작은 값 반환.

</details>

---

### Q5. dept별 salary의 분산을 구하고, 분산이 가장 큰 부서 이름과 그 분산 값을 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
dept_var = df.groupby('dept')['salary'].var()
print(dept_var.idxmax())
print(round(dept_var.max(), 2))
```

> `var()` 기본값도 ddof=1 (표본분산).

</details>

---

### Q6. salary의 90백분위수와 10백분위수의 차이(범위)를 소수 둘째 자리까지 출력하라. 이 범위보다 높은 salary를 가진 직원 수도 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
q10 = df['salary'].quantile(0.10)
q90 = df['salary'].quantile(0.90)
sal_range = q90 - q10

print(round(sal_range, 2))
print((df['salary'] > sal_range).sum())
```

</details>

---

### Q7. dept별로 score의 중앙값을 구하고, 자신의 dept 중앙값 이상인 직원들의 salary 평균을 dept별로 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['dept_score_median'] = df.groupby('dept')['score'].transform('median')
above = df[df['score'] >= df['dept_score_median']]
print(above.groupby('dept')['salary'].mean().round(2))
```

> `transform('median')` — 그룹별 집계 결과를 원래 df 행 수에 맞게 펼쳐서 붙임.
> 이후 행별 비교 `df['score'] >= df['dept_score_median']` 가능.

</details>

---

### Q8. distance 기준으로 상위 30% (70백분위수 이상)에 해당하는 직원을 'long', 나머지를 'short'로 구분하는 `travel_type` 컬럼을 추가하라. travel_type별 score 평균과 표준편차를 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
p70 = df['distance'].quantile(0.7)
df['travel_type'] = np.where(df['distance'] >= p70, 'long', 'short')
result = df.groupby('travel_type')['score'].agg(['mean', 'std']).round(2)
print(result)
```

> `np.where` + `quantile` 조합 — 백분위수 기준 조건 분류 패턴.
> `agg(['mean', 'std'])` — 여러 집계를 한 번에.

</details>
