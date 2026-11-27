# 2유형 최종 복습 Set 1 — 헬스장 회원 이탈 (이진 분류 · ROC-AUC) → result_cls.csv
# 문제: retake/2유형_최종복습.md
# 실행: .venv/bin/python workspace/final_t2_cls.py   (프로젝트 폴더에서)
# 채점: .venv/bin/python workspace/grade_t2.py cls
# 시작 시각: __:__   (목표 25분, 핵심 한 장은 덮고 — 막히면 🆘 한 칸)

# 1 데이터 준비

# 1-1. 데이터 가져오기
import pandas as pd
train = pd.read_csv('retake/data/final_t2/gym_train.csv')
test = pd.read_csv('retake/data/final_t2/gym_test.csv')

# 1-2. 데이터 훑어보기
print(train.info())
print(test.info())
print(train.head())
print(test.head())

# 2.전처리
# 2-1. 데이터 나누기
y = train['churn']
print(y.value_counts()) # 정답 데이터 개수로 회귀/분류 판단 --> 분류로 확인
X = train.drop(columns=['member_id', 'churn'])
X_test = test.drop(columns=['member_id'])
print(X.shape, X_test.shape)

# 2-2. 결측치 채우기
print(X.isnull().sum()) # age, last_visit_days, locker
print(X_test.isnull().sum()) # age, last_visit_days, locker

print(X['age'].value_counts()) # 개수가 모두 많음 => 최빈값 활용
print(X['last_visit_days'].value_counts()) # 개수가 1개인게 많음 => 중앙값 활용
print(X['locker'].value_counts()) # ⭐️⭐️⭐️ 항상 고민. N이 538개고 Y가 385개니까 개수가 많은 538으로 처리해도 되는지, 아니면 '없음'으로 해야하는지 정확히 확인 필요

m = X['age'].mode()[0]
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)

m2 = X['last_visit_days'].median()
X['last_visit_days'] = X['last_visit_days'].fillna(m2)
X_test['last_visit_days'] = X_test['last_visit_days'].fillna(m2)

X['locker'] = X['locker'].fillna('없음')
X_test['locker'] = X_test['locker'].fillna('없음')

# 3. 인코딩
# 3-1. 데이터 합치기
all_x = pd.concat([X, X_test])

# 3-2. 인코딩
# (1) 원핫인코딩
#help(pd.get_dummies)
#print(X.info())
#all_x = pd.get_dummies(all_x, columns=['gender', 'branch', 'membership', 'locker']) # 수치형이 아닌 값들 넣기
#print(all_x)

# (2) 라벨인코딩
from sklearn.preprocessing import LabelEncoder
cols = ['gender', 'branch', 'membership', 'locker']
for c in cols:
    le = LabelEncoder() # 매번 새로 생성
    all_x[c] = le.fit_transform(all_x[c])
print(all_x)

# 3-3. 데이터 나누기
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]
print(X.shape,X_test.shape)

# 4. 모델링
# 4-1. train / value 나누기
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # 분류니까 stratify=y 필수!!

# 4-2. 모델 준비 및 학습
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# 4-3. 예측
pred = model.predict(X_value)
proba = model.predict_proba(X_value)[:,1]

# 4-4. 평가
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score #*** r2_score는 회귀 평가를 위한 지표였던 것 같음.
# 내 기억상 roc_auc_score는 proba / f1_score와 accuracy_score는 pred 활용
# 내 기억상 이진 분류일때는 roc_auc_score, accuracy_score 사용 / 다중 분류일때는 무조건 f1_score의 'macro'
print(round(roc_auc_score(y_value, proba),3)) # **** roc_auc는 1에 가까워야 좋은 지표였나..?
print(round(f1_score(y_value, pred, average='macro'),3))
print(round(accuracy_score(y_value, pred),3))

# 5. 제출
# 전체 데이터로 예측
model.fit(X,y)
proba = model.predict_proba(X_test)[:,1]
# csv 생성
pd.DataFrame({'pred': proba}).to_csv('result_cls.csv', index=False)

# 제출 전 확인
df = pd.read_csv('result_cls.csv')
print(df.shape)
print(df.head())