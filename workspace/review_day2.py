# Day 2 복습 셀프 퀴즈 — 문제는 retake/복습_day2.md "3. 1분 셀프 퀴즈"
# 실행: .venv/bin/python workspace/review_day2.py   (프로젝트 폴더에서)
# 한 번 풀었던 퀴즈 (3/5). Q3, Q4를 직접 쳐서 다시 풀어 본다.
import pandas as pd

df = pd.read_csv('retake/data/day2_orders.csv')

# Q1. 지역별 주문 건수 중 2번째로 많은 지역 이름
print('--- Q1 ---')

# Q2. 분류별 rating 평균이 가장 낮은 분류 이름
print('--- Q2 ---')

# Q3. 각 주문의 qty가 자기 분류의 qty 평균 이상인 주문 수   ← 재풀이 (transform)
print('--- Q3 ---')

# Q4. 서울 주문 중 가전의 비율 (소수 셋째)   ← 재풀이 (변수로 빼기)
print('--- Q4 ---')

# Q5. 지역별 최빈 분류(category)
print('--- Q5 ---')
