# 실전 분류 복습 — 문제는 retake/실전_분류.md
# 실행: .venv/bin/python workspace/final_cls.py   (프로젝트 폴더에서)
# 채점: .venv/bin/python workspace/grade_cls.py
# 시작 시각: __:__   (목표 25분, 노트 보지 않기)

# 1 데이터 확인
import pandas as pd
train = pd.read_csv('retake/data/final_cls/member_train.csv')
test = pd.read_csv('retake/data/final_cls/member_test.csv')

print(train.info()) # 정답은 grade
print(test.info())
print(train.isnull().sum()) # age / avg_basket / coupon_use
print(test.isnull().sum())
print(train.head())
print(train.head())
print(train['grade'].value_counts()) # value가 3개 -> 분류로 판별

# 2. 전처리
# 2-1. X,y 분리
y = train['grade']
X = train.drop(columns=['member_id', 'grade']) # ID, 정답 제거
X_test = test.drop(columns=['member_id']) # ID제거
print(X.shape, X_test.shape)

# 2-2. 결측치 처리
print(X['age'].value_counts()) # 값을 보니 평균이 적절해보임
print(X['avg_basket'].value_counts()) # 값의 개수를 보니 중앙값이 유리해보임
print(X['coupon_use'].value_counts()) # Y 657개, N512개.. *** '없음'으로 해야할까..? 아니면 개수가 많은 Y로 해야할까?

m = X['age'].mean()
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)

m = X['avg_basket'].mode()[0]
X['avg_basket'] = X['avg_basket'].fillna(m)
X_test['avg_basket'] = X_test['avg_basket'].fillna(m)

X['coupon_use'] = X['coupon_use'].fillna('없음')
X_test['coupon_use'] = X_test['coupon_use'].fillna('없음')

# 3. 인코딩
# 3-1 X, X_test 병합
all_x = pd.concat([X, X_test])
# 3-2. 인코딩 (원핫 or 라벨)
# (1) 원핫 인코딩
#all_x = pd.get_dummies(all_x, columns=['gender', 'region', 'coupon_use', 'app_user'])

# (2) 라벨 인코딩
from sklearn.preprocessing import LabelEncoder
cols = ['gender', 'region', 'coupon_use', 'app_user']
for c in cols:
    le = LabelEncoder() # 매번 새로 생성
    all_x[c] = le.fit_transform(all_x[c])

# 3-3. X, X_test 분할
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]



# 4. 모델링
# 4-1. 테스트 데이터 선정
from sklearn.model_selection import train_test_split
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y) # 분할이니까 무조건 stratify=y

# 4-2. 모델 학습. 분류 => RandomForestClassifier
from sklearn.ensemble import RandomForestClassifier
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 4-3 예측
pred = model.predict(X_value)
# proba = model.predict_proba(X_value)[:,1] # ***다중 분류는 proba 사용 X
print(pred)

# 4-4 평가
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score
#print(round(roc_auc_score(y_value, proba),2)) # ***다중 분류는 proba 사용 X
print(round(f1_score(y_value, pred, average='macro'), 2)) # *** 0.67이면 괜찮은 값이었나? 0.5~0-75로 기억하는데 맞나
print(round(accuracy_score(y_value, pred),2))

# 5. 평가 및 제출
# 평가 데이터 평가
model.fit(X, y)
pred = model.predict(X_test)
# proba = model.predict_proba(X_test)[:, 1] # ***다중 분류는 proba 사용 X

# 형식에 맞춘 파일 생성
pd.DataFrame({'pred':pred}).to_csv('result.csv', index=False) # f1_score를 위해 제출해야하기 때문에 pred 제출!!!
result = pd.read_csv('result.csv')
print(result.shape)
print(result.head())