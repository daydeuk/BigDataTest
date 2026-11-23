# 재도전 Day 4 풀이 — 2유형 분류 풀세트 (문제는 retake/day4.md)
# 실행: .venv/bin/python workspace/day4.py   (프로젝트 폴더에서)
# 5단계 (번호 = 단계-조각, retake/day4.md와 같음)
#   1 탐색: 1-1 불러오기 · 1-2 훑어보기
#   2 전처리①: 2-1 나누기 · 2-2 결측
#   3 전처리②: 3-1 인코딩
#   4 모델링: 4-1 분할 · 4-2 학습 · 4-3 예측 · 4-4 점수   (Q3, Q4)
#   5 제출: 5-1 다시 학습 · 5-2 저장 · 5-3 확인          (Q5)
# 템플릿을 보지 않고 먼저 쳐 본다. import부터!

# 1 탐색 → 2 전처리① → 3 전처리② → 4 모델링 → 5 제출

# 1-1. 불러오기
# import pandas as pd
#train = pd.read_csv('retake/data/day4/churn_train.csv')
#test  = pd.read_csv('retake/data/day4/churn_test.csv')

# 1-1. 데이터 불러오기
# 1 탐색
# import pandas as pd
# train = pd.read_csv('train.csv')
# test = pd.read_csv('test.csv')

# 1-2. 데이터 훑어보기 (확인용)
# print(train.info())
# print(train.isnull().sum()) # 결측치 개수 확인
# print(train['churn'].value_counts())

# 2-1. 나누기 (X, y, X_test 나누기)
# 2 전처리①
# y = train['churn']
# X = train.drop(columns=['customer_id', 'churn'])
# X_test = test.drop(columns=['customer_id'])

# 2-2. 결측치 채우기 - train 기준 값으로 X, X_test 둘 다
# m = X['age'].median()
# X['age'] = X['age'].fillna(m)
# X_test['age'] = X_test['age'].fillna(m) # test도 train의 값으로 채우기

# X['payment'] = X['payment'].fillna('없음') # 글자 컬럼은 '없음' 같은 새 값으로
# X_test['payment'] = X_test['payment'].fillna('없음')

# 3-1. 인코딩 (3 전처리②) - 왜 합쳐서 하나
# 모델은 글자를 못 읽는다 -> 글자 컬럼을 0/1 컬럼으로 바꾼다. (get_dummies = 원 핫 인코딩)
# pay -> pay_카드 pay_현금
# 카드 ->  True    False
# 현금 ->  False   True

# 따로 하면 컬럼이 어긋난다.
# 그래서 합쳐야한다.
# all_x = pd.concat([X, X_test]) # 위아래로 붙이기 (train 1000행 + test 300행)
# all_x = pd.get_dummies(all_x, columns=['payment']) # 한번에 인코딩
# X = all_x.iloc[:len(X)] # 앞 1000행 = train
# X_test = all_x.iloc[len(X):] # 나머지 300행


# 4-1. 분할(검증용) - 내 점수 미리보기
#test에는 정답이 없어서 점수를 모른다 -> train의 20%를 떼어서 모의 시험을 본다.
# from sklearn.model_selection import train_test_split
# X_tr, X_val, y_tr, y_val = train_test_split(X,y, test_size=0.2, random_state=42, stratify=y)

# 4-2 학습 / 4-3 예측 / 4-4 점수 * predict vs predict_proba
# from sklearn.ensemble import RandomForestClassifier
# model = RandomForestClassifier(n_estimators=100, random_state=42)
# model.fit(X_tr, y_tr) # 공부
# pred = model.predict(X_val) # 0 또는 1
# proba = model.predict_proba(X_val)[:, 1] # 1일 확률 (0~1)
# print(pred)
# print(proba)

# 5. 제출 (5-1 다시 학습 / 5-2 저장 / 5-3 확인)
# model.fit(X, y) # (선택) 검증 끝났으면 train 전체로 다시 학습
# pred = model.predict_proba(X_test)[:, 1]
# pd.DataFrame({'pred': pred}).to_csv('result.csv', index = False)
# r = pd.read_csv('result.csv')
# print(r.shape)
# print(r.head())

# Q1. train·test 행·열 수 / train 결측 컬럼과 개수 / 이탈 비율 (소수 셋째)
import pandas as pd

train = pd.read_csv('retake/data/day4/churn_train.csv')
test = pd.read_csv('retake/data/day4/churn_test.csv')
print(train.shape) # train의 행, 열
print(test.shape) # test의 행, 열
#print(train.info())
print(train.isnull().sum()) # train 결측 컬럼과 개수 *** 어떻게 0보다 큰 녀석들만 보여주지?
print(round(train['churn'].mean(),3))# train의 이탈(churn) 비율
t = train.isnull().sum()
print(t[t>0])
# Q2. 나누기 → 결측(age, total_spend: train 중앙값 / payment: '없음') → 합쳐서 get_dummies → 다시 나누기 → X, X_test shape
# 2-1 나누기
y = train['churn']
X = train.drop(columns=['customer_id', 'churn'])
X_test = test.drop(columns=['customer_id'])
print(X.shape, X_test.shape)

# 2-2 결측치 채우기
# age
m = X['age'].median();
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)

# total_spend
m = X['total_spend'].median()
X['total_spend'] = X['total_spend'].fillna(m)
X_test['total_spend'] = X_test['total_spend'].fillna(m)

# payment
X['payment'] = X['payment'].fillna('없음')
X_test['payment'] = X_test['payment'].fillna('없음')

print(X.isnull().sum().sum(), X_test.isnull().sum().sum())

# 3-1 인코딩
print(X.info())
all_x = pd.concat([X, X_test])
all_x = pd.get_dummies(all_x, columns = ['gender', 'region', 'contract', 'payment'])
#print(all_x)
#print(all_x.info())
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]

print(X.shape)
print(X_test.shape)
# Q3. train_test_split(test_size=0.2, random_state=42, stratify=y) → RandomForestClassifier(n_estimators=100, random_state=42) → 검증 ROC-AUC (소수 넷째)
# 4 모델링
# 4-1 검증용으로 떼어내기
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size = 0.2, random_state = 42, stratify=y)

# 4-2 학습
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4-3 예측 / 4-4 점수
# 4-3 예측
pred = model.predict(X_value)
proba = model.predict_proba(X_value)[:, 1]

# 4-4 점수
# roc_auc_score = 확률 (proba)
# f1_score = 0/1 (pred)
# accuracy_score = 0/1 (pred)

from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
print(round(roc_auc_score(y_value, proba),4))
print(round(f1_score(y_value, pred, average='macro'),4))
print(round(accuracy_score(y_value, pred),4))

# Q4. 같은 모델 → 검증 F1(macro), accuracy (소수 넷째)
# 5-1 다시 학습
model.fit(X,y)
# 5-2 저장
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:,1]
pd.DataFrame({'pred': proba}).to_csv('result.csv', index=False)
# 5-3 확인
result = pd.read_csv('result.csv')
print(result.shape)
print(result.head())

# Q5. train 전체(X, y)로 다시 학습 → test 이탈 확률 → result.csv (pred, index=False) → 다시 불러와 shape, head()

