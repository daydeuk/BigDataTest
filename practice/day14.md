# 14일차 — 통계 검정 완전 (Day14+15 압축)

> 치트시트의 코드 패턴을 보지 않고 직접 써보는 것이 목표.  
> 모든 검정은 `from scipy import stats` 사용. p-value 기준: **0.05**

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
    'score2':   np.random.normal(75, 10, n).round(1),   # 대응표본용
    'income':   np.random.normal(5000, 1000, n).round(0),
    'passed':   np.random.randint(0, 2, n)
})
```

---

## Part 1 — t검정

### Q1. 일표본 t검정
`score` 평균이 70과 다른지 검정하라. t통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
stat, p = stats.ttest_1samp(df['score'], popmean=70)
print(round(stat, 3))
print(round(p, 3))
```

</details>

---

### Q2. 대응표본 t검정
`score`와 `score2`의 평균 차이가 있는지 검정하라. t통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
stat, p = stats.ttest_rel(df['score'], df['score2'])
print(round(stat, 3))
print(round(p, 3))
```

</details>

---

### Q3. 독립표본 t검정 (Welch)
`group`이 A인 그룹과 B인 그룹의 `score` 평균이 다른지 Welch t검정하라. t통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
g_a = df[df['group'] == 'A']['score']
g_b = df[df['group'] == 'B']['score']
stat, p = stats.ttest_ind(g_a, g_b, equal_var=False)
print(round(stat, 3))
print(round(p, 3))
```

> Welch t검정: `equal_var=False` 필수

</details>

---

## Part 2 — 분산분석 / 비모수 검정

### Q4. ANOVA (일원분산분석)
`group` A, B, C 세 그룹의 `score` 평균이 다른지 검정하라. F통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
groups = [df[df['group'] == g]['score'] for g in ['A', 'B', 'C']]
stat, p = stats.f_oneway(*groups)
print(round(stat, 3))
print(round(p, 3))
```

> `*groups` — 리스트를 펼쳐서 인자로 전달

</details>

---

### Q5. Kruskal-Wallis
`group` A, B, C 세 그룹의 `income` 분포가 다른지 Kruskal-Wallis 검정하라. 검정통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
groups = [df[df['group'] == g]['income'] for g in ['A', 'B', 'C']]
stat, p = stats.kruskal(*groups)
print(round(stat, 3))
print(round(p, 3))
```

> ANOVA의 비모수 버전. 사용법 동일

</details>

---

### Q6. Mann-Whitney U
`gender`가 M인 그룹과 F인 그룹의 `score` 분포가 다른지 Mann-Whitney U 검정하라. U통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
g_m = df[df['gender'] == 'M']['score']
g_f = df[df['gender'] == 'F']['score']
stat, p = stats.mannwhitneyu(g_m, g_f, alternative='two-sided')
print(round(stat, 3))
print(round(p, 3))
```

> `alternative='two-sided'` 양측검정. 단측은 `'less'` 또는 `'greater'`

</details>

---

### Q7. Levene 등분산 검정
`group` A, B, C 세 그룹의 `score` 분산이 같은지 Levene 검정하라. 검정통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
groups = [df[df['group'] == g]['score'] for g in ['A', 'B', 'C']]
stat, p = stats.levene(*groups)
print(round(stat, 3))
print(round(p, 3))
```

</details>

---

### Q8. Shapiro-Wilk 정규성 검정
`score`의 앞 50개가 정규분포를 따르는지 Shapiro-Wilk 검정하라. 검정통계량과 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
stat, p = stats.shapiro(df['score'].head(50))
print(round(stat, 3))
print(round(p, 3))
```

> Shapiro-Wilk는 소표본(n≤50)에 적합. 문제에서 앞 N개 지정하는 경우 많음

</details>

---

## Part 3 — 상관검정

### Q9. Pearson 상관검정
`score`와 `income`의 선형 상관관계를 Pearson 검정하라. 상관계수와 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
stat, p = stats.pearsonr(df['score'], df['income'])
print(round(stat, 3))
print(round(p, 3))
```

</details>

---

### Q10. Spearman 순위상관검정
`score`와 `income`의 순위 상관관계를 Spearman 검정하라. 상관계수와 p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
stat, p = stats.spearmanr(df['score'], df['income'])
print(round(stat, 3))
print(round(p, 3))
```

</details>

---

## Part 4 — 카이제곱 검정

### Q11. 카이제곱 독립성 검정
`group`과 `passed`의 관계가 독립인지 카이제곱 검정하라. chi2, 자유도, p-value를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
ct = pd.crosstab(df['group'], df['passed'])
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(round(chi2, 3))
print(dof)
print(round(p, 3))
```

> `chi2_contingency` 반환 순서: chi2, p, dof, expected (기대빈도 행렬)

</details>

---

## Part 5 — OLS 회귀

### Q12. OLS 회귀
`score`를 종속변수, `income`을 독립변수로 OLS 회귀를 적합하라. `income`의 계수, p-value, R-squared를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
import statsmodels.formula.api as smf

model = smf.ols('score ~ income', data=df).fit()
print(round(model.params['income'], 3))
print(round(model.pvalues['income'], 3))
print(round(model.rsquared, 3))
```

</details>

---

### Q13. 범주형 포함 OLS
`score`를 종속변수, `income`과 `group`(범주형)을 독립변수로 OLS 회귀를 적합하라. `income`의 계수와 p-value, R-squared를 소수 셋째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
model = smf.ols('score ~ income + C(group)', data=df).fit()
print(round(model.params['income'], 3))
print(round(model.pvalues['income'], 3))
print(round(model.rsquared, 3))
```

> 범주형 변수는 `C(변수명)`으로 감싸기

</details>

---

## 핵심 암기표

| 검정 | 함수 | 언제 |
|------|------|------|
| 일표본 t | `ttest_1samp(col, popmean=N)` | 평균 vs 기준값 |
| 대응표본 t | `ttest_rel(before, after)` | 전후 비교 |
| 독립표본 t | `ttest_ind(g1, g2, equal_var=False)` | 두 그룹 평균 |
| ANOVA | `f_oneway(*groups)` | 3개+ 그룹 평균 |
| Kruskal | `kruskal(*groups)` | ANOVA 비모수 버전 |
| Mann-Whitney | `mannwhitneyu(g1, g2, alternative='two-sided')` | 두 그룹 비모수 |
| Levene | `levene(*groups)` | 등분산 검정 |
| Shapiro | `shapiro(col)` | 정규성 검정 |
| Pearson | `pearsonr(x, y)` | 선형 상관 |
| Spearman | `spearmanr(x, y)` | 순위 상관 |
| 카이제곱 | `chi2_contingency(crosstab)` | 범주 독립성 |
| OLS | `smf.ols('y ~ x', data=df).fit()` | 선형 회귀 |
