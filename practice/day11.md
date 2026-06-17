# 11일차 — 분류 모델 완전

## 개념 정리

### 1. 분류 모델 종류 ★★★

| 모델 | import | 특징 |
|---|---|---|
| `RandomForestClassifier` | `sklearn.ensemble` | 트리 여러 개 앙상블, 안정적 |
| `XGBClassifier` | `xgboost` | 부스팅, 성능 좋음, 시험 단골 |
| `LogisticRegression` | `sklearn.linear_model` | 선형, 빠름 |
| `DecisionTreeClassifier` | `sklearn.tree` | 단순 트리 |

> 시험에서 **RandomForest, XGBoost** 가 가장 많이 출제됨

---

### 2. 분류 모델 기본 패턴 ★★★

```python
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier

# RandomForest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_val)

# XGBoost
model = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
model.fit(X_train, y_train)
pred = model.predict(X_val)
```

> `eval_metric='logloss'` — XGBoost 분류 시 경고 방지용. 없어도 동작하지만 습관적으로 추가

---

### 3. 분류 평가지표 ★★★

```python
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# accuracy — 전체 중 맞춘 비율
print(round(accuracy_score(y_val, pred), 4))

# f1_score — precision과 recall의 조화평균
print(round(f1_score(y_val, pred, average='macro'), 4))
# average 옵션: 'binary'(이진), 'macro'(클래스 평균), 'weighted'(가중 평균)

# roc_auc — 확률값(predict_proba) 기준 평가
pred_proba = model.predict_proba(X_val)[:, 1]   # 양성 클래스 확률
print(round(roc_auc_score(y_val, pred_proba), 4))
```

> **핵심 구분**
> - `predict()` → 0/1 예측값 → accuracy, f1에 사용
> - `predict_proba()[:, 1]` → 확률값 → roc_auc에 사용

---

### 4. CSV 제출 패턴 ★★★

```python
# test 데이터 예측 후 제출
result = pd.DataFrame({'pred': model.predict(X_test)})
result.to_csv('result.csv', index=False)

# 확인
result_check = pd.read_csv('result.csv')
print(result_check.shape)
print(result_check.columns.tolist())
print(result_check['pred'].head(10).sum())
```

> **주의사항**
> - `index=False` 필수 — 없으면 `Unnamed: 0` 컬럼 생겨서 오답 처리
> - 컬럼명은 문제에서 지정한 이름으로

---

### 5. 전체 흐름 요약 (분류)

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

# 1. 데이터 로드
train = pd.read_csv('data/train.csv')
test  = pd.read_csv('data/test.csv')

# 2. 전처리 (인코딩)
train = pd.get_dummies(train, columns=['col1', 'col2'])
test  = pd.get_dummies(test,  columns=['col1', 'col2'])
train, test = train.align(test, join='left', axis=1, fill_value=0)

# 3. X, y 분리
X = train.drop(columns=['id', 'target'])
y = train['target']
X_test = test.drop(columns=['id'])

# 4. split
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 5. 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)

# 6. 평가
pred = model.predict(X_val)
print(round(accuracy_score(y_val, pred), 4))
print(round(f1_score(y_val, pred, average='macro'), 4))

# 7. CSV 제출
result = pd.DataFrame({'pred': model.predict(X_test)})
result.to_csv('result.csv', index=False)
```

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

np.random.seed(42)
n = 200
data = {
    'id':       range(1, n+1),
    'age':      np.random.randint(20, 60, n),
    'income':   np.random.randint(2000, 8000, n),
    'score':    np.random.randint(40, 100, n),
    'region':   np.random.choice(['서울', '경기', '부산'], n),
    'channel':  np.random.choice(['online', 'offline'], n),
    'churn':    np.random.choice([0, 1], n, p=[0.6, 0.4])
}
df = pd.DataFrame(data)
```

---

### Q1. region과 channel을 원핫인코딩하고, churn을 y로 train_test_split(test_size=0.2, random_state=42, stratify=y)하라. X_train shape를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df_enc = pd.get_dummies(df, columns=['region', 'channel'])

X = df_enc.drop(columns=['id', 'churn'])
y = df_enc['churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)
print(X_train.shape)
```

</details>

---

### Q2. RandomForestClassifier(n_estimators=100, random_state=42)로 학습하고 검증 accuracy를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

pred = model.predict(X_test)
print(round(accuracy_score(y_test, pred), 4))
```

</details>

---

### Q3. 위 모델의 검증 f1_score(average='macro')를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(round(f1_score(y_test, pred, average='macro'), 4))
```

</details>

---

### Q4. 위 모델의 검증 roc_auc_score를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
pred_proba = model.predict_proba(X_test)[:, 1]
print(round(roc_auc_score(y_test, pred_proba), 4))
```

> `predict_proba()[:, 1]` — 전체 확률 행렬에서 양성(1) 클래스 확률만 추출

</details>

---

### Q5. XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')로 학습하고 검증 accuracy를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from xgboost import XGBClassifier

model_xgb = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
model_xgb.fit(X_train, y_train)

pred_xgb = model_xgb.predict(X_test)
print(round(accuracy_score(y_test, pred_xgb), 4))
```

</details>

---

### Q6. RandomForest와 XGBoost 두 모델의 accuracy를 비교하고, 더 높은 모델명과 점수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
acc_rf  = accuracy_score(y_test, pred)
acc_xgb = accuracy_score(y_test, pred_xgb)

if acc_rf >= acc_xgb:
    print('RandomForest')
    print(round(acc_rf, 4))
else:
    print('XGBoost')
    print(round(acc_xgb, 4))
```

</details>

---

### Q7. RandomForest 모델로 X_test 예측 결과를 result.csv로 저장하라. 저장 후 불러와서 shape, 컬럼명, 앞 10개 pred 합계를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = pd.DataFrame({'pred': model.predict(X_test)})
result.to_csv('result.csv', index=False)

check = pd.read_csv('result.csv')
print(check.shape)
print(check.columns.tolist())
print(check['pred'].head(10).sum())
```

</details>

---

### Q8. accuracy, f1(macro), roc_auc 세 가지 평가지표를 한꺼번에 출력하라. (RandomForest 모델 기준, 소수 셋째 자리)

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
pred       = model.predict(X_test)
pred_proba = model.predict_proba(X_test)[:, 1]

print(round(accuracy_score(y_test, pred), 3))
print(round(f1_score(y_test, pred, average='macro'), 3))
print(round(roc_auc_score(y_test, pred_proba), 3))
```

</details>
