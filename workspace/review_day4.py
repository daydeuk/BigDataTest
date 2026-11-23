# Day 4 복습 — 2유형 분류를 템플릿 안 보고 처음부터 (문제는 retake/복습_day4.md 4번)
# 실행: .venv/bin/python workspace/review_day4.py   (프로젝트 폴더에서)
# 평가지표: macro F1 → 제출은 0/1 (predict)
# 목표 15분. import부터!

# 1-1 불러오기  (retake/data/day4/churn_train.csv, churn_test.csv)
import pandas as pd
train = pd.read_csv('retake/data/day4/churn_train.csv')
test = pd.read_csv('retake/data/day4/churn_test.csv')

# 1-2 훑어보기
print(train.info())
print(test.info())
print(train.isnull().sum())
print(test.isnull().sum())
print(train.head())
print(test.head())
# churn --> 정답 -> 0/1 (분류 문제)

# 2-1 나누기
y = train['churn']
X = train.drop(columns=['customer_id', 'churn'])
X_test = test.drop(columns=['customer_id'])
print(X.shape, X_test.shape)

# 2-2 결측
print(X.isnull().sum())
print(X_test.isnull().sum())
# 결측치는 중앙값/최빈값 으로 채우기
# age는 최빈값으로 해보기
m = X['age'].mode()[0]
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)

#total_spend 중앙값으로 해보기
m2 = X['total_spend'].median()
X.loc[X['total_spend'].isnull(), 'total_spend'] = m2
X_test.loc[X_test['total_spend'].isnull(), 'total_spend'] = m2

# payment는 '없음' 으로 해보기 *** 실제 데이터인 계좌이체, 카드 둘 중 하나로 처리하면 어떻게 될지 궁금하다 *** 
X['payment'] = X['payment'].fillna('없음')
X_test['payment'] = X_test['payment'].fillna('없음')

#print(X.info())
#print(X['payment'].value_counts())    # '없음'이 보이고 41.0이 없어야 함
#print(X['total_spend'].describe())    # 최솟값이 41 같은 이상한 값이 아닌지

# 3-1 인코딩
# 0, 1 이니까 원 핫 인코딩
# 때의 따라 LabelEncoder()를 사용해야 할 수 있다고 했음 *** 정확한 정보인지는 확인 필요 ***

# 우선 데이터 2개 이어 붙이기
all_x = pd.concat([X, X_test])
# Object 인것들을 숫자형으로 변경해야함.
all_x = pd.get_dummies(all_x, columns=['gender', 'region', 'contract', 'payment'])

print(all_x.shape)
# 데이터 다시 나누기 (train / test)
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]
print(X.shape, X_test.shape)


# 4-1 분할
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2 ,random_state=42, stratify=y)


# 4-2 학습
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4-3 예측
pred = model.predict(X_value)
proba = model.predict_proba(X_value)[:,1]

# 4-4 점수 (macro F1, 소수 넷째)
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
print(roc_auc_score(y_value, proba))
print(f1_score(y_value, pred, average='macro'))
print(accuracy_score(y_value, pred))

# 5-1 다시 학습 *** 다시 학습은 train 전체로 ****
model.fit(X, y)
pred = model.predict(X_test)
proba = model.predict_proba(X_test)[:,1]

#print('pred',pred)
#print('proba',proba)
# 5-2 저장 (result.csv, pred 컬럼, 0/1)
pd.DataFrame({'pred':pred}).to_csv('result.csv', index=False)

# 5-3 확인
df = pd.read_csv('result.csv')
print(df.shape)
print(df.head())