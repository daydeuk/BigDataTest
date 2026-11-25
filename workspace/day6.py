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


# Q2. 2-2 대응: after, before 순서 → 통계량 (소수 셋째), 기각/채택


# Q3. 2-3 독립: A반 vs B반 after (등분산) → 통계량, p-value (소수 셋째), 기각/채택


# Q4. 3 카이제곱: group × passed → 통계량, p-value (소수 셋째), 자유도, 기각/채택


# Q5. 4 선형회귀: after ~ before + hours + sleep (세 변수) → hours 계수 (소수 넷째)


# Q6. 유의하지 않은 변수 개수 / R² (소수 셋째) / before=70, hours=5, sleep=6 예측 (소수 둘째)


# Q7. 5 로지스틱: passed ~ hours + sleep → hours 오즈비 (소수 셋째)


# Q8. hours, sleep 중 유의한 변수 이름 (0.05)

