# Day 6 복습 (3유형) — 문제는 retake/복습_day6.md
# 실행: .venv/bin/python workspace/review_day6.py
# 채점: .venv/bin/python workspace/grade_day6.py   (맨 아래 answer에 답을 넣은 뒤)
# 시작 시각: __:__   (목표 35분, 노트 보지 않기)
import pandas as pd
import numpy as np

df = pd.read_csv('retake/data/day6_review/diet.csv')

# 문제 1 — 검정
# 1-1, 1-2
print(df.info())
print(df.head())

# 1-1. 같은 참가자의 프로그램 전후 체중이 다른지 검증하라.
from scipy import stats
stat, p = stats.ttest_rel(df['weight_before'], df['weight_after'])
print(round(stat, 3), round(p, 3))

# 1-2. 1-1의 결과로 귀무가설을 기각하는가?
if(p<0.05):
    print('기각')
else:
    print('채택')

# 1-3
# 등분산을 가정하지 않는다..
df['diff'] = df['weight_before'] - df['weight_after']
A_df = df[df['program'] == 'A']['diff']
B_df = df[df['program'] == 'B']['diff']
#print(help(stats.ttest_ind))
stat, p = stats.ttest_ind(A_df, B_df, equal_var=False) #등분산을 가정하지 않는다 -> equal_var=False
print(round(p,3))

# 1-4 sex와 success가 관련 있는지 카이제곱 독립성 검정을 하라. 검정통계량
# 카이제곱 독립성 검정..
ct = pd.crosstab(df['sex'], df['success'])
print(ct)
#help(stats.chi2_contingency)
chi2, p, dof, expected = stats.chi2_contingency(ct) # *** 각각 어떤 값을 나타내는지 까먹음
print(round(chi2, 3)) # ***문제에서 원하는 검정통계량은 chi2 일까..?

# 1-5
from scipy import stats
stat, p = stats.ttest_1samp(df['age'], 40)
print(round(p, 3))


# 문제 2 — 회귀
# 2-1 ~ 2-5

# 2-1. weight_after를 weight_before, exercise_hours, calories, age로 예측하는 선형회귀를 적합하라.
# exercise_hours의 회귀계수
import statsmodels.formula.api as smf
# 선형회귀 -> smf.ols
model = smf.ols('weight_after ~ weight_before + exercise_hours + calories + age', data=df).fit()
print(model.summary())
print(round(model.params['exercise_hours'],4))

# 2-2. 2-1 모델에서 유의수준 0.05에서 유의하지 않은 변수의 개수 (절편 제외)
pv = model.pvalues.drop('Intercept')
print(len(pv[pv > 0.05]))

# 2-3. 2-1 모델에서 유의한 변수의 이름을 전부 (절편 제외)
vpv = pv[pv <= 0.05]
print('2-3')
print(vpv.index.tolist()) # *** Series에서 index 빼오는 법 모르겠음. 그리고 가장 위에 1 있는데 왜있는지도 모르겠고, 없애는 방법도 모르겠음 ***

# 2-4. 2-1 모델의 R²
print(round(model.rsquared,3))

# 2-5. weight_before=80, exercise_hours=5, calories=2000, age=40인 참가자의 예측 체중
new = pd.DataFrame({'weight_before':[80], 'exercise_hours':[5], 'calories':[2000], 'age':[40]})
print(new)
pred = model.predict(new)
print(round(pred,2)) # *** 앞에 0이 나오는데, 어떻게 해야하지? pred.iloc[0]을 붙여야하나?

# 2-6
import statsmodels.formula.api as smf
model = smf.logit('success ~ exercise_hours + calories', data=df).fit()
print(model.summary())
print(round(np.exp(model.params['exercise_hours']),3)) # *** 오즈비는 np.exp(계수)

# ---------------------------------------------------------------
# 답 적기 — 코드로 구한 변수를 넣는다 (예: '1-1': round(stat1, 3))
# ---------------------------------------------------------------
answer = {
    '1-1': None,
    '1-2': None,
    '1-3': None,
    '1-4': None,
    '1-5': None,
    '2-1': None,
    '2-2': None,
    '2-3': None,
    '2-4': None,
    '2-5': None,
    '2-6': None,
}