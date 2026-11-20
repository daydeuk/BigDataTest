# Day 3 복습 셀프 퀴즈 — 문제는 retake/복습_day3.md "4. 셀프 퀴즈"
# 실행: .venv/bin/python workspace/review_day3.py   (프로젝트 폴더에서)
import pandas as pd
import numpy as np

df = pd.read_csv('retake/data/day3_delivery.csv')

# R1. naver 계정(대소문자 구분 없이) 주문 수
print('--- R1 ---')

# R2. 일요일 주문의 amount 평균 (소수 둘째)
print('--- R2 ---')

# R3. deliver_min 30분 미만 '정시' / 30분 이상 '지연' (pd.cut, right 주의) → '지연' 건수
print('--- R3 ---')

# R4. amount의 IQR 방식 이상치 개수
print('--- R4 ---')

# R5. 시/도별 주말 주문 비율이 가장 높은 시/도 이름과 비율 (소수 셋째)
print('--- R5 ---')
