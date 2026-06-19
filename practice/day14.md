# 14+15일차 — 3유형 핵심 패턴 5개

> 이것만 보고 끝낸다. p-value < 0.05 → 유의한 차이 있음.

---

## 데이터 세팅

```python
import pandas as pd
import numpy as np
from scipy import stats

np.random.seed(42)
n = 200

df = pd.DataFrame({
    'id':       range(1, n+1),
    'group':    np.random.choice(['A', 'B', 'C'], n),
    'gender':   np.random.choice(['M', 'F'], n),
    'score':    np.random.normal(72, 10, n).round(1),
    'score2':   np.random.normal(75, 10, n).round(1),
    'income':   np.random.normal(5000, 1000, n).round(0),
    'passed':   np.random.randint(0, 2, n)
})
```

---

## 공통 출력 패턴

```python
print(round(stat, 3))
print(round(p, 3))
```

---

## Q1. 일표본 t검정 — "평균이 기준값과 다른가?"

```python
stat, p = stats.ttest_1samp(df['score'], 70)
print(round(stat, 3))
print(round(p, 3))
```

---

## Q2. 대응표본 t검정 — "전후 차이가 있는가?"

```python
stat, p = stats.ttest_rel(df['score'], df['score2'])
print(round(stat, 3))
print(round(p, 3))
```

---

## Q3. 독립표본 t검정 (Welch) — "두 그룹 평균이 다른가?"

```python
g_a = df[df['group'] == 'A']['score']
g_b = df[df['group'] == 'B']['score']
stat, p = stats.ttest_ind(g_a, g_b, equal_var=False)  # Welch
print(round(stat, 3))
print(round(p, 3))
```

> `equal_var=True` → 합동분산 t검정 (분산 같을 때)

---

## Q4. ANOVA — "3개+ 그룹 평균이 다른가?"

```python
g_a = df[df['group'] == 'A']['score']
g_b = df[df['group'] == 'B']['score']
g_c = df[df['group'] == 'C']['score']
stat, p = stats.f_oneway(g_a, g_b, g_c)
print(round(stat, 3))
print(round(p, 3))
```

---

## Q5. 카이제곱 — "두 범주형 변수가 관련 있는가?"

```python
ct = pd.crosstab(df['group'], df['passed'])
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(round(chi2, 3))
print(round(p, 3))
print(dof)
```

> 반환 순서: chi2 → p → dof → expected  
> 기대빈도 최솟값 요구 시: `print(round(expected.min(), 3))`

---

## + F검정 — "두 그룹의 분산이 다른가?"

```python
var1, var2 = g_a.var(), g_b.var()
F = var1/var2 if var1 >= var2 else var2/var1
df1, df2 = len(g_a)-1, len(g_b)-1
p_f = 2 * min(stats.f.cdf(F, df1, df2), stats.f.sf(F, df1, df2))
print(round(F, 3))
print(round(p_f, 3))
```
