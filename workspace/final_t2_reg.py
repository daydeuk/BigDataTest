# 2유형 최종 복습 Set 2 — 배달 소요 시간 (회귀 · RMSE) → result_reg.csv
# 문제: retake/2유형_최종복습.md
# 실행: .venv/bin/python workspace/final_t2_reg.py   (프로젝트 폴더에서)
# 채점: .venv/bin/python workspace/grade_t2.py reg
# 시작 시각: __:__   (목표 25분, 핵심 한 장은 덮고 — 막히면 🆘 한 칸)

# 1. 데이터 확인

# 1-1. 데이터 불러오기
import pandas as pd
train = pd.read_csv('retake/data/final_t2/delivery_train.csv')
test = pd.read_csv('retake/data/final_t2/delivery_test.csv')
# 평가지표 : RMSE ROOT MEAN SQUARED ERROR

# 1-2. 데이터 훑어보기
print(train.info())
print(test.info())
print(train.head())
print(test.head())

# 2. 전처리
# 2-1. 데이터 나누기
y = train['delivery_min']
X = train.drop(columns=['order_id', 'delivery_min'])
X_test = test.drop(columns=['order_id'])

# 2-2. 결측치 처리
print(X.isnull().sum())
print(X_test.isnull().sum())
print(X['distance_km'].value_counts()) # median으로 선정
print(X['rider_exp_months'].value_counts()) # mode로 선정
print(X['rush'].value_counts()) # '없음' 가자

m = X['distance_km'].median()
X['distance_km'] = X['distance_km'].fillna(m)
X_test['distance_km'] = X_test['distance_km'].fillna(m)

m2 = X['rider_exp_months'].mode()[0]
X['rider_exp_months'] = X['rider_exp_months'].fillna(m2)
X_test['rider_exp_months'] = X_test['rider_exp_months'].fillna(m2)

X['rush'] = X['rush'].fillna('없음')
X_test['rush'] = X_test['rush'].fillna('없음')

print(X.info())
print(X_test.info())

# 3. 인코딩
# 3-1. 데이터 합치기
all_x = pd.concat([X, X_test])

# 3-2. 인코딩
all_x = pd.get_dummies(all_x, columns=['weather', 'time_slot', 'vehicle', 'rush']) # **** 나는 지금 info()로 object인걸 모두 columns에 넣고 있는데, 만약 데이터는 숫자인데 Dtype만 object인 놈이 있으면 어떻게해? Dtype만 변경하는거 가능하니?

# 3-3. 데이터 나누기
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]

# 4.모델링
# 4-1. train, value 나누기
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42)

# 4-2. 모델 준비(회귀)
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4-3. 예측
# 회귀에서는 proba 말고 predict만
pred = model.predict(X_value)

# 4-4. 평가
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
# *** mean_squared_error라는 이름이 기억 안나면 어떤거를 help 나 dir 써야해?

import numpy as np
print(round(np.sqrt(mean_squared_error(y_value, pred)),3)) # *** 루트를 사용하는 방법이 기억이 안남..
print(round(mean_absolute_error(y_value, pred),3))
print(round(r2_score(y_value, pred),3))

# 5. 제출
# 5-1. 전체 데이터 대상 예측
model.fit(X, y)
pred = model.predict(X_test)

# 5-2. 파일 만들기
pd.DataFrame({'pred':pred}).to_csv('result_reg.csv', index=False)
# 5-3. 확인
df = pd.read_csv('result_reg.csv')
print(df.shape)
print(df.head())