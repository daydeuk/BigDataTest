# ANOVA 연습 — 문제는 retake/복습_day6.md 맨 아래 "ANOVA 연습"
# 실행: .venv/bin/python workspace/review_anova.py
import pandas as pd
from scipy import stats

# A1. Day 2 주문 — region(5곳)별 qty 평균 → F, p (소수 셋째), 기각/채택
o = pd.read_csv('retake/data/day2_orders.csv')
print('--- A1 ---')
print(o.info())
print(o.head())
from scipy import stats
#print(o['region'].value_counts())
g1 = o[o['region']=='서울']['qty']
g2 = o[o['region']=='경기']['qty']
g3 = o[o['region']=='대구']['qty']
g4 = o[o['region']=='부산']['qty']
g5 = o[o['region']=='광주']['qty']
stat, p = stats.f_oneway(g1,g2,g3,g4,g5)
print(round(stat,3),round(p,3))
if(p < 0.05):
    print('기각')
else:
    print('채택')
# A2. Day 3 배달 — address 첫 단어(시/도 4곳)별 deliver_min 평균 → F, p, 기각/채택
d = pd.read_csv('retake/data/day3_delivery.csv')
print('--- A2 ---')
print(d.info())
print(d.head())
d['address'] = d['address'].str.split(' ').str[0]
print(d['address'].value_counts())
g1 = d.loc[d['address']=='서울']['deliver_min']
g2 = d.loc[d['address']=='부산']['deliver_min']
g3 = d.loc[d['address']=='경기']['deliver_min']
g4 = d.loc[d['address']=='인천']['deliver_min']
from scipy import stats
stat, p = stats.f_oneway(g1,g2,g3,g4)
print(round(stat,3),round(p,3))
if(p < 0.05):
    print('기각')
else:
    print('채택')
# A3. Day 5 중고차 — brand(5개)별 price 평균 → F, 기각/채택
c = pd.read_csv('retake/data/day5/car_train.csv')
print('--- A3 ---')

# A4. Day 5 중고차 — BMW 제외 4개 brand별 price 평균 → F, 기각/채택
print('--- A4 ---')
print(c.info())
print(c.head())
print(c['brand'].value_counts())
# 제외는 그냥 g에 포함 안하면 끝이네..?
g1 = c.loc[c['brand']=='현대']['price']
g2 = c.loc[c['brand']=='기아']['price']
g3 = c.loc[c['brand']=='쉐보레']['price']
g4 = c.loc[c['brand']=='르노']['price']

# *** 근데 price 별 평균이라니까 .groupby().mean() 이런거 쓰고 싶은데,
# price 목록만 있어도 stats.f_oneway가 다 평균으로 가공해서 처리하는거지?

from scipy import stats
stat, p = stats.f_oneway(g1,g2,g3,g4)
print(round(stat, 3), round(p, 3))
# **** 항상 헷갈린다. p<=0.05 인지 p<0.05인지
if(p < 0.05):
    print('기각')
else:
    print("채택")