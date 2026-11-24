# 재도전 Day 5 풀이 — 2유형 회귀 + 라벨 인코딩 (문제는 retake/day5.md)
# 실행: .venv/bin/python workspace/day5.py   (프로젝트 폴더에서)
# 5단계 (번호 = 단계-조각, Day 4와 같음) — 분류와 다른 곳: stratify 없음 · Regressor · predict만 · RMSE
#   1 탐색: 1-1 불러오기 · 1-2 훑어보기 (분류/회귀 판단)
#   2 전처리①: 2-1 나누기 · 2-2 결측
#   3 전처리②: 3-1 인코딩 (A 원핫 / B 라벨)
#   4 모델링: 4-1 분할 · 4-2 학습 · 4-3 예측 · 4-4 점수
#   5 제출: 5-1 다시 학습 · 5-2 저장 · 5-3 확인
# Day 4 풀이를 복사하지 말고 처음부터 친다. import부터!

# Q1. 1-1 불러오기 (retake/data/day5/car_train.csv, car_test.csv) · 1-2 훑어보기 → 분류? 회귀?
# 1. 탐색
# 1-1. 데이터 불러오기
import pandas as pd
train = pd.read_csv('retake/data/day5/car_train.csv')
test  = pd.read_csv('retake/data/day5/car_test.csv')

# 1-2. 데이터 훑어보기
print(train.info())
print(test.info())
print(train.head())
print(test.head())
print(train['price'].unique()) # price가 정답이라는걸 알았으니 nunique()로 회귀 / 분류 문제를 나눈다. (숫자 많으니 회귀 문제)


# Q2. 2-1 나누기 · 2-2 결측 (mileage, engine_cc: train 중앙값 / fuel: '없음')
# 2. 전처리 1번.
# 2-1. X, y 나누기
y = train['price']
X = train.drop(columns=['car_id', 'price'])
X_test = test.drop(columns=['car_id'])

# 2-2. 결측치 커버
# fuel - object / mileage - float / engine_cc - float
s = X.isnull().sum()
print(s[s>0])
print(X['fuel'].value_counts())
print(X['mileage'].value_counts())
print(X['engine_cc'].value_counts())

# (1) fuel 같은 경우에는 '없음'으로 처리하는게 좋아보임. (*** 분류 일때는 '없음'하는게 나을지, mode()[0]하는게 나을지 모르겠음)
X['fuel'] = X['fuel'].fillna('없음')
X_test['fuel'] = X_test['fuel'].fillna('없음')

# (2) mileage 같은 경우는 중앙값이 결측치로 유리해보임.
m = X['mileage'].median()
X['mileage'] = X['mileage'].fillna(m)
X_test['mileage'] = X_test['mileage'].fillna(m) # *** 내 기억상 X_test의 결측치로도 X_train의 중앙값 사용이 유리.

# (3) engine_cc의 경우는 최빈값이 결측치 처리에 유리해보임.
m = X['engine_cc'].mode()[0]
X['engine_cc'] = X['engine_cc'].fillna(m)
X_test['engine_cc'] = X_test['engine_cc'].fillna(m)

# Q2-A. 3-1 인코딩 — 원핫 (합쳐서 get_dummies → iloc) → X, X_test shape
# 3. 인코딩
# 3-1. 데이터 합치기
print(X.shape, X_test.shape) # 열 개수 맞는지 확인
all_x = pd.concat([X, X_test])

# 3-2. 인코딩 (원핫인코딩)
print(X.info()) # object 컬럼 확인
all_x = pd.get_dummies(all_x, columns=['brand', 'fuel', 'transmission', 'accident'])

# Q2-B. 3-1 인코딩 — 라벨 (합쳐서 컬럼마다 LabelEncoder → iloc) → X_lb, X_test_lb shape
# from sklearn.preprocessing import LabelEncoder
# cols = ['brand', 'fuel', 'transmission', 'accident']
# for c in cols:
#     le = LabelEncoder() # 컬럼마다 새로 만든다
#     all_x[c] = le.fit_transform(all_x[c]) # 합친 표에서 바로 fit_transform

# 3-3. 데이터 다시 분할
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]

# Q3. (원핫) 4-1 분할 (stratify 없음) · 4-2 RandomForestRegressor · 4-3 predict · 4-4 RMSE, MAE (소수 둘째)
# 4. 모델링
# 4-1 분할
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42) # stratify=y 는 회귀

# 4-2 모델링
from sklearn.ensemble import RandomForestRegressor # 회귀니까 Regressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4-3 예측
# *** predict로 하는 X_value는 어떤 값들이지..?
pred = model.predict(X_value) # 회귀는 predict_proba 사용 X


# 4-4 평가
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
rmse = np.sqrt(mean_squared_error(y_value, pred))
mae = mean_absolute_error(y_value, pred)
r2score = r2_score(y_value,pred)

# *** rmse랑 mae는 실행할때마다 조금씩 다른 값이 나오는데 이유가 뭘까?
print(round(rmse,2)) # *** 낮을수록 좋다는데 어느 정도가 좋은걸까?
print(round(mae,2)) # *** 낮을수록 좋다는데 어느 정도가 좋은걸까?
print(round(r2score,2)) #1과 가까우면 좋음 #0.94

# Q4. (라벨) 같은 방법으로 검증 RMSE → 원핫과 차이 주석


# Q5. 5-1 다시 학습 (원핫, X, y) · 5-2 저장 (X_test, predict, result.csv) · 5-3 확인
# 5. 제출
# 5-1 전체 데이터 학습 및 예측
model.fit(X, y)
pred = model.predict(X_test)
# 5-2
pd.DataFrame({'pred':pred}).to_csv('result.csv', index=False)
df = pd.read_csv('result.csv')
print(df)
print(df.shape)


# 문제 풀이
# Q1. (탐색) train·test의 행·열 수, train의 결측 컬럼과 개수, price의 평균(정수)과 서로 다른 값의 개수를 출력하고, 분류인지 회귀인지 주석으로 적어라.
print(train.shape)
print(test.shape)
s = train.isnull().sum()
print(s[s>0])
m = int(train['price'].mean())
print(m)
p = train['price']
print(p.nunique()) #회귀임

# Q2. (전처리) 아래처럼 전처리하라.
# y = price / X = train에서 car_id, price 제외 / X_test = test에서 car_id 제외
# mileage, engine_cc 결측 → train 중앙값 / fuel 결측 → '없음'
# A. brand, fuel, transmission, accident를 합쳐서 원핫 인코딩 → X, X_test shape 출력
# B. (따로 한 번 더) 같은 컬럼을 LabelEncoder로 인코딩한 버전도 만들어 shape 출력 — 변수 이름은 X_lb, X_test_lb처럼 구분
y = train['price']
X = train.drop(columns=['car_id', 'price'])
X_test = test.drop(columns=['car_id'])

m = X['mileage'].median()
X['mileage'] = X['mileage'].fillna(m)
X_test['mileage'] = X_test['mileage'].fillna(m)

m = X['engine_cc'].median()
X['engine_cc'] = X['engine_cc'].fillna(m)
X_test['engine_cc'] = X_test['engine_cc'].fillna(m)

X['fuel'] = X['fuel'].fillna('없음')
X_test['fuel'] = X_test['fuel'].fillna('없음')

cols = ['brand', 'fuel', 'transmission', 'accident']

# 데이터 합치기
all_x = pd.concat([X, X_test])
# 1. 원핫 인코딩
onehot_x = pd.get_dummies(all_x, columns=cols)

X = onehot_x.iloc[:len(X)]
X_test = onehot_x.iloc[len(X):]

# 2. 라벨 인코딩
from sklearn.preprocessing import LabelEncoder
for c in cols:
    le = LabelEncoder()
    all_x[c] = le.fit_transform(all_x[c])

X_lb = all_x.iloc[:len(X)]
X_test_lb = all_x.iloc[len(X):]

print(X.shape, X_test.shape)
print(X_lb.shape, X_test_lb.shape)

# Q3. (모델 · 원핫 버전) train_test_split(test_size=0.2, random_state=42)로 나누고
# RandomForestRegressor(n_estimators=100, random_state=42)로 학습하라. 검증 RMSE와 MAE를 소수 둘째 자리까지 출력하라.
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2 , random_state=42)

from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_value)

from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np
rmse = np.sqrt(mean_squared_error(y_value, pred))
mae = mean_absolute_error(y_value, pred)

print(round(rmse,2))
print(round(mae,2))

#Q4. (비교 · 라벨 버전) Q2-B의 라벨 인코딩 데이터로 Q3과 똑같이 하고 검증 RMSE를 출력하라. 원핫과 차이를 주석으로 적어라.
X_lb_train, X_lb_value, y_lb_train, y_lb_value = train_test_split(X_lb, y, test_size=0.2, random_state=42)
model_lb = RandomForestRegressor(n_estimators=100, random_state=42)
model_lb.fit(X_lb_train, y_lb_train)
pred_lb = model_lb.predict(X_lb_value)
rmse_lb = np.sqrt(mean_squared_error(y_lb_value, pred_lb))
mae_lb = mean_absolute_error(y_lb_value, pred_lb)
print(round(rmse_lb,2))
print(round(mae_lb,2))
# 값이 똑같은데..?


#Q5. (제출) 원핫 버전 모델을 train 전체로 다시 학습한 뒤 test 차량의 가격을 예측해 pred 컬럼 하나짜리 result.csv로 저장하라. 다시 불러와 shape과 앞 5행을 출력하라.
#채점: Q5는 숨겨진 test 정답으로 RMSE 400 이하면 통과 (기본 템플릿 약 342, 평균만 찍으면 약 1382).
model.fit(X, y)
pred = model.predict(X_test)

pd.DataFrame({'pred': pred}).to_csv('result.csv', index=False)
df = pd.read_csv('result.csv')
print(df.shape)
print(df.head())