# ⭐ 핵심 반복 복습 — 문제는 retake/핵심_반복복습.md "연습문제"
# 실행: .venv/bin/python workspace/review_core.py   (프로젝트 폴더에서)
# 복습할 때마다 아래 풀이를 지우고 처음부터 다시 쳐 본다.
import pandas as pd
import numpy as np

o = pd.read_csv('retake/data/day2_orders.csv')     # Day 2 주문
d = pd.read_csv('retake/data/day3_delivery.csv')   # Day 3 배달

# C1. (Day 2) 회원 주문 수
print('--- C1 ---')

# C2. (Day 2) 회원 주문 비율 (소수 셋째)
print('--- C2 ---')

# C3. (Day 2) 지역별 '식품' 비율이 가장 낮은 지역 이름과 비율 (소수 셋째)
print('--- C3 ---')

# C4. (Day 3) 시/도별 배달 60분 초과 비율이 가장 높은 시/도 이름과 비율 (소수 셋째)
print('--- C4 ---')

# C5. (Day 3) 18시~21시대 주문 비율 (소수 셋째)
print('--- C5 ---')
