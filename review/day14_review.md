# Day14 복습 — 통계 검정 완전 (Day14+15 압축)

> `practice/day14.md` Q1~Q13 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [ ] p-value < 0.05 → 귀무가설 기각 → 유의한 차이 있음
- [ ] `ttest_1samp(col, popmean=N)` — 일표본
- [ ] `ttest_rel(before, after)` — 대응표본
- [ ] `ttest_ind(g1, g2, equal_var=False)` — 독립표본 Welch
- [ ] `f_oneway(*groups)` — ANOVA
- [ ] `kruskal(*groups)` — Kruskal-Wallis
- [ ] `mannwhitneyu(g1, g2, alternative='two-sided')` — Mann-Whitney
- [ ] `levene(*groups)` — 등분산
- [ ] `shapiro(col)` — 정규성
- [ ] `pearsonr(x, y)` — Pearson 상관
- [ ] `spearmanr(x, y)` — Spearman 상관
- [ ] `chi2_contingency(pd.crosstab(...))` — 카이제곱
- [ ] `smf.ols('y ~ x + C(범주형)', data=df).fit()` — OLS

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| | | |
