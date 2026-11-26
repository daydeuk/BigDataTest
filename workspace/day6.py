# 재도전 Day 6 풀이 — 3유형 검정 · 회귀 (문제는 retake/day6.md)
# 실행: .venv/bin/python workspace/day6.py   (프로젝트 폴더에서)
#   1 판단: p < 0.05 → 귀무가설 기각
#   2 t검정: 2-1 일표본 · 2-2 대응 · 2-3 독립
#   3 카이제곱: 3-1 교차표 · 3-2 독립성 검정
#   4 선형회귀: 4-1 적합 · 4-2 계수·p-value · 4-3 R² · 4-4 예측
#   5 로지스틱: 5-1 적합 · 5-2 오즈비
import pandas as pd
import numpy as np
# from scipy import stats
# import statsmodels.formula.api as smf

df = pd.read_csv('retake/data/day6_study.csv')

# Q1. 2-1 일표본: after 평균 vs 70 → 통계량, p-value (소수 셋째), 기각/채택
print(df)
print(df.info())
print(df.head())

from scipy import stats
stat, p = stats.ttest_1samp(df['after'], 70)
print(round(stat, 3), round(p,3))
if (p < 0.05):
    print('귀무가설 기각')
else:
    print('귀무가설 채택')

# Q2. 2-2 대응: after, before 순서 → 통계량 (소수 셋째), 기각/채택
from scipy import stats
stat, p = stats.ttest_rel(df['after'], df['before'])
print(round(stat, 3), round(p, 3))


# Q3. 2-3 독립: A반 vs B반 after (등분산) → 통계량, p-value (소수 셋째), 기각/채택
# 독립 비교 indepedent
from scipy import stats
a = df.loc[df['group']=='A', 'after']
b = df.loc[df['group']=='B', 'after']
print(len(a), a.mean())
print(len(b), b.mean())

stat, p = stats.ttest_ind(a, b)
print(round(stat, 3), round(p,3))
if p>=0.05:
    print('채택')
else:
    print('기각')



# Q4. 3 카이제곱: group × passed → 통계량, p-value (소수 셋째), 자유도, 기각/채택
print('-Q4-')
ct = pd.crosstab(df['group'], df['passed'])
chi2, p, dof, expected = stats.chi2_contingency(ct)
print(round(chi2, 3), round(p, 3), dof)
# 통계량(카이제곱), p-value, 자유도, 기대빈도
if(p>=0.05):
    print('채택')
else:
    print('기각')

# Q5. 4 선형회귀: after ~ before + hours + sleep (세 변수) → hours 계수 (소수 넷째)
# import statsmodels.formula.api as smf # 3유형 import

# model = smf.ols('after ~ before + hours + sleep', data=df).fit()
# print(model.summary())
# print(round(model.params['hours'], 4))
# coef 계수

# Q6. 유의하지 않은 변수 개수 / R² (소수 셋째) / before=70, hours=5, sleep=6 예측 (소수 둘째)
import statsmodels.formula.api as smf

# model = smf.ols('after ~ before + hours + sleep', data=df).fit()
# print(model.summary())
# pv = model.pvalues[:]
# print(len(df.loc[df>=0.05]))
# print(round(model.rsquared,3))
# new = pd.DataFrame({'before': [70], 'hours':[5], 'sleep':[6]})
# print(round(model.predict(new)[0],2))


# Q7. 5 로지스틱: passed ~ hours + sleep → hours 오즈비 (소수 셋째)
import statsmodels.formula.api as smf
model2 = smf.logit('passed ~ hours + sleep', data=df).fit()
print(model2.summary())
print(model2.params['hours'])
print(np.exp(model2.params['hours']))

# Q8. hours, sleep 중 유의한 변수 이름 (0.05)
pv = model2.pvalues[:]
print(pv[pv<0.05].index.tolist())