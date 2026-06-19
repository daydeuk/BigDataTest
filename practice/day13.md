# 13일차 — 2유형 풀세트 반복 (3회)

> 전처리 → 인코딩 → split → 모델 → 평가 → CSV 제출 전체 흐름을 처음 보는 데이터로 3회 반복.  
> 개념 설명 없이 바로 풀기. 막히면 `공부계획.md`의 2유형 핵심 템플릿 참고.

---

## Set 1 — 대출 승인 분류

### 데이터 세팅

```python
import pandas as pd
import numpy as np

np.random.seed(10)
n = 300
train = pd.DataFrame({
    'id':              range(1, n+1),
    'age':             np.random.randint(20, 65, n),
    'income':          np.random.randint(2000, 10000, n),
    'credit_score':    np.random.randint(300, 850, n),
    'employment_type': np.random.choice(['정규직', '계약직', '자영업'], n),
    'loan_amount':     np.random.randint(500, 5000, n),
    'approved':        np.random.randint(0, 2, n)
})
test = pd.DataFrame({
    'id':              range(n+1, n+101),
    'age':             np.random.randint(20, 65, 100),
    'income':          np.random.randint(2000, 10000, 100),
    'credit_score':    np.random.randint(300, 850, 100),
    'employment_type': np.random.choice(['정규직', '계약직', '자영업'], 100),
    'loan_amount':     np.random.randint(500, 5000, 100),
})
```

---

### Q1. `employment_type`을 원핫인코딩하고, `approved`를 y로 `train_test_split(test_size=0.2, random_state=42, stratify=y)`하라. `X_train.shape`를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.model_selection import train_test_split

train_enc = pd.get_dummies(train, columns=['employment_type'])
test_enc  = pd.get_dummies(test,  columns=['employment_type'])
train_enc, test_enc = train_enc.align(test_enc, join='left', axis=1, fill_value=0)

X = train_enc.drop(columns=['id', 'approved'])
y = train_enc['approved']
X_test = test_enc.drop(columns=['id', 'approved'], errors='ignore')

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(X_train.shape)
```

</details>

---

### Q2. `RandomForestClassifier(n_estimators=100, random_state=42)`로 학습하고 검증 accuracy를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score

model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_val)
print(round(accuracy_score(y_val, pred), 4))
```

</details>

---

### Q3. 같은 모델로 검증 f1_score(average='macro')를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.metrics import f1_score

print(round(f1_score(y_val, pred, average='macro'), 4))
```

</details>

---

### Q4. 같은 모델로 검증 `roc_auc_score`를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.metrics import roc_auc_score

pred_proba = model.predict_proba(X_val)[:, 1]
print(round(roc_auc_score(y_val, pred_proba), 4))
```

> roc_auc는 `predict()` 아닌 `predict_proba()[:, 1]` 사용

</details>

---

### Q5. 학습된 모델로 `X_test`(제출용 test 데이터)를 예측하고 `pred` 컬럼으로 `result.csv`에 저장하라. 저장 후 불러와서 shape, 컬럼명, 앞 10개 pred 합계를 출력하라.

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

## Set 2 — 직원 이직 분류

### 데이터 세팅

```python
import pandas as pd
import numpy as np

np.random.seed(20)
n = 400
train = pd.DataFrame({
    'id':               range(1, n+1),
    'age':              np.random.randint(22, 55, n),
    'salary':           np.random.randint(2500, 9000, n),
    'years':            np.random.randint(1, 20, n),
    'dept':             np.random.choice(['개발', '영업', '인사', '마케팅'], n),
    'satisfaction':     np.random.randint(1, 6, n),
    'overtime':         np.random.choice(['Yes', 'No'], n),
    'left':             np.random.randint(0, 2, n)
})
test = pd.DataFrame({
    'id':               range(n+1, n+101),
    'age':              np.random.randint(22, 55, 100),
    'salary':           np.random.randint(2500, 9000, 100),
    'years':            np.random.randint(1, 20, 100),
    'dept':             np.random.choice(['개발', '영업', '인사', '마케팅'], 100),
    'satisfaction':     np.random.randint(1, 6, 100),
    'overtime':         np.random.choice(['Yes', 'No'], 100),
})
```

---

### Q1. `dept`, `overtime`을 원핫인코딩하고, `left`를 y로 `train_test_split(test_size=0.2, random_state=42, stratify=y)`하라. `X_train.shape`를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.model_selection import train_test_split

train_enc = pd.get_dummies(train, columns=['dept', 'overtime'])
test_enc  = pd.get_dummies(test,  columns=['dept', 'overtime'])
train_enc, test_enc = train_enc.align(test_enc, join='left', axis=1, fill_value=0)

X = train_enc.drop(columns=['id', 'left'])
y = train_enc['left']
X_test = test_enc.drop(columns=['id', 'left'], errors='ignore')

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(X_train.shape)
```

</details>

---

### Q1-B. (라벨인코딩 버전) `dept`, `overtime`을 `LabelEncoder`로 인코딩하고, `left`를 y로 `train_test_split(test_size=0.2, random_state=42, stratify=y)`하라. `X_train.shape`를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

for col in ['dept', 'overtime']:
    le = LabelEncoder()
    train[col] = le.fit_transform(train[col])   # train: fit + transform
    test[col]  = le.transform(test[col])         # test: transform만

X = train.drop(columns=['id', 'left'])
y = train['left']
X_test = test.drop(columns=['id'])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
print(X_train.shape)
```

> 원핫인코딩과 달리 concat 불필요 — 컬럼 수가 변하지 않음  
> train에만 `fit_transform`, test에는 `transform`만

</details>

---

### Q2. `XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')`로 학습하고 검증 roc_auc_score를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score

model = XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')
model.fit(X_train, y_train)
pred_proba = model.predict_proba(X_val)[:, 1]
print(round(roc_auc_score(y_val, pred_proba), 4))
```

> roc_auc는 `predict_proba()[:, 1]` 사용

</details>

---

### Q3. 같은 모델로 검증 accuracy와 f1_score(average='binary')를 각각 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.metrics import accuracy_score, f1_score

pred = model.predict(X_val)
print(round(accuracy_score(y_val, pred), 4))
print(round(f1_score(y_val, pred, average='binary'), 4))
```

</details>

---

### Q4. test 데이터의 예측값을 `result.csv`로 저장하라. 저장 후 불러와서 shape, 컬럼명, 앞 10개 pred 합계를 출력하라.

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

## Set 3 — 부동산 가격 회귀

### 데이터 세팅

```python
import pandas as pd
import numpy as np

np.random.seed(30)
n = 350
train = pd.DataFrame({
    'id':        range(1, n+1),
    'area':      np.random.randint(40, 200, n),
    'floors':    np.random.randint(1, 30, n),
    'age':       np.random.randint(0, 40, n),
    'location':  np.random.choice(['강남', '강북', '경기'], n),
    'renovated': np.random.choice(['Y', 'N'], n),
    'price':     np.random.randint(10000, 100000, n)
})
test = pd.DataFrame({
    'id':        range(n+1, n+101),
    'area':      np.random.randint(40, 200, 100),
    'floors':    np.random.randint(1, 30, 100),
    'age':       np.random.randint(0, 40, 100),
    'location':  np.random.choice(['강남', '강북', '경기'], 100),
    'renovated': np.random.choice(['Y', 'N'], 100),
})
```

---

### Q1. `location`, `renovated`를 원핫인코딩하고, `price`를 y로 `train_test_split(test_size=0.2, random_state=42)`하라. (stratify 없음) `X_train.shape`를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.model_selection import train_test_split

train_enc = pd.get_dummies(train, columns=['location', 'renovated'])
test_enc  = pd.get_dummies(test,  columns=['location', 'renovated'])
train_enc, test_enc = train_enc.align(test_enc, join='left', axis=1, fill_value=0)

X = train_enc.drop(columns=['id', 'price'])
y = train_enc['price']
X_test = test_enc.drop(columns=['id', 'price'], errors='ignore')

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape)
```

> 회귀는 stratify 없음

</details>

---

### Q1-B. (라벨인코딩 버전) `location`, `renovated`를 `LabelEncoder`로 인코딩하고, `price`를 y로 `train_test_split(test_size=0.2, random_state=42)`하라. (stratify 없음) `X_train.shape`를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split

le = LabelEncoder()
train['location'] = le.fit_transform(train['location'])
test['location']  = le.transform(test['location'])

train['renovated'] = le.fit_transform(train['renovated'])
test['renovated']  = le.transform(test['renovated'])

X = train.drop(columns=['id', 'price'])
y = train['price']
X_test = test.drop(columns=['id'])

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
print(X_train.shape)
```

> 회귀는 stratify 없음

</details>

---

### Q2. `RandomForestRegressor(n_estimators=100, random_state=42)`로 학습하고 검증 RMSE와 MAE를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_val)

print(round(np.sqrt(mean_squared_error(y_val, pred)), 4))
print(round(mean_absolute_error(y_val, pred), 4))
```

</details>

---

### Q3. `LinearRegression`과 `RandomForestRegressor` 두 모델의 RMSE를 비교하고, 더 낮은 모델명과 RMSE를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from sklearn.linear_model import LinearRegression

model_lr = LinearRegression()
model_lr.fit(X_train, y_train)
rmse_lr = np.sqrt(mean_squared_error(y_val, model_lr.predict(X_val)))

model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)
rmse_rf = np.sqrt(mean_squared_error(y_val, model_rf.predict(X_val)))

if rmse_lr <= rmse_rf:
    print('LinearRegression')
    print(round(rmse_lr, 4))
else:
    print('RandomForestRegressor')
    print(round(rmse_rf, 4))
```

</details>

---

### Q4. RMSE가 더 낮은 모델로 test 데이터의 예측값을 `result.csv`로 저장하라. 저장 후 불러와서 shape, 컬럼명, 앞 10개 pred 합계를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
best_model = model_lr if rmse_lr <= rmse_rf else model_rf

result = pd.DataFrame({'pred': best_model.predict(X_test)})
result.to_csv('result.csv', index=False)

check = pd.read_csv('result.csv')
print(check.shape)
print(check.columns.tolist())
print(round(check['pred'].head(10).sum(), 4))
```

</details>
