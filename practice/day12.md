# 12일차 — 회귀 모델 완전

## 개념 정리

### 1. 회귀 모델 종류 ★★★

| 모델 | import | 특징 |
|---|---|---|
| `LinearRegression` | `sklearn.linear_model` | 단순 선형, 빠름 |
| `RandomForestRegressor` | `sklearn.ensemble` | 트리 앙상블, 안정적 |
| `XGBRegressor` | `xgboost` | 부스팅, 성능 좋음 |

> 분류에서 `Classifier` → 회귀에서 `Regressor` 로 바뀌는 것만 기억

---

### 2. 회귀 모델 기본 패턴 ★★★

```python
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from xgboost import XGBRegressor

# LinearRegression
model = LinearRegression()
model.fit(X_train, y_train)
pred = model.predict(X_val)

# RandomForest
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_val)

# XGBoost
model = XGBRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_val)
```

> 회귀는 `stratify` 없음 — 연속값이라 클래스 비율 개념이 없음

---

### 3. 회귀 평가지표 ★★★

```python
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error

# RMSE — 예측 오차의 제곱 평균의 루트 (단위 동일, 이상치 민감)
rmse = np.sqrt(mean_squared_error(y_val, pred))
print(round(rmse, 4))

# MAE — 예측 오차의 절댓값 평균 (이상치 덜 민감)
mae = mean_absolute_error(y_val, pred)
print(round(mae, 4))
```

> **분류 vs 회귀 평가지표 구분**
> | 분류 | 회귀 |
> |---|---|
> | accuracy, f1, roc_auc | RMSE, MAE |
> | `predict()` 사용 | `predict()` 사용 |
> | `predict_proba()` (roc_auc만) | 없음 |

---

### 4. RMSE vs MAE

| | RMSE | MAE |
|---|---|---|
| 공식 | √(오차² 평균) | 오차 절댓값 평균 |
| 이상치 영향 | 크다 (제곱이라) | 작다 |
| 단위 | 원래 단위와 동일 | 원래 단위와 동일 |
| 시험 출제 | ★★★ | ★★ |

---

### 5. CSV 제출 패턴 (회귀)

```python
result = pd.DataFrame({'pred': model.predict(X_test)})
result.to_csv('result.csv', index=False)

check = pd.read_csv('result.csv')
print(check.shape)
print(check.columns.tolist())
print(check['pred'].head(10).sum())
```

> 분류와 동일한 패턴. `index=False` 필수.

---

### 6. 전체 흐름 요약 (회귀)

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

# 1. 데이터 로드
train = pd.read_csv('data/train.csv')
test  = pd.read_csv('data/test.csv')

# 2. 전처리
train = pd.get_dummies(train, columns=['col1', 'col2'])
test  = pd.get_dummies(test,  columns=['col1', 'col2'])
train, test = train.align(test, join='left', axis=1, fill_value=0)

# 3. X, y 분리
X = train.drop(columns=['id', 'target'])
y = train['target']
X_test = test.drop(columns=['id'])

# 4. split — 회귀는 stratify 없음
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42)

# 5. 학습
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)

# 6. 평가
pred = model.predict(X_val)
rmse = np.sqrt(mean_squared_error(y_val, pred))
mae  = mean_absolute_error(y_val, pred)
print(round(rmse, 4))
print(round(mae, 4))

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
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error

np.random.seed(42)
n = 200
data = {
    'id':           range(1, n+1),
    'age':          np.random.randint(20, 60, n),
    'experience':   np.random.randint(0, 30, n),
    'score':        np.random.randint(40, 100, n),
    'dept':         np.random.choice(['개발', '영업', '기획'], n),
    'grade':        np.random.choice(['A', 'B', 'C'], n),
    'salary':       np.random.randint(3000, 9000, n)
}
df = pd.DataFrame(data)
```

---

### Q1. dept와 grade를 원핫인코딩하고, salary를 y로 train_test_split(test_size=0.2, random_state=42)하라. X_train shape를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df_enc = pd.get_dummies(df, columns=['dept', 'grade'])

X = df_enc.drop(columns=['id', 'salary'])
y = df_enc['salary']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)
print(X_train.shape)
```

> 회귀는 `stratify` 없음

</details>

---

### Q2. LinearRegression으로 학습하고 검증 RMSE를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
model_lr = LinearRegression()
model_lr.fit(X_train, y_train)

pred_lr = model_lr.predict(X_test)
rmse_lr = np.sqrt(mean_squared_error(y_test, pred_lr))
print(round(rmse_lr, 4))
```

</details>

---

### Q3. RandomForestRegressor(n_estimators=100, random_state=42)로 학습하고 검증 RMSE를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
model_rf = RandomForestRegressor(n_estimators=100, random_state=42)
model_rf.fit(X_train, y_train)

pred_rf = model_rf.predict(X_test)
rmse_rf = np.sqrt(mean_squared_error(y_test, pred_rf))
print(round(rmse_rf, 4))
```

</details>

---

### Q4. LinearRegression과 RandomForest 두 모델의 RMSE를 비교하고, 더 낮은 모델명과 RMSE를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
if rmse_lr <= rmse_rf:
    print('LinearRegression')
    print(round(rmse_lr, 4))
else:
    print('RandomForestRegressor')
    print(round(rmse_rf, 4))
```

</details>

---

### Q5. XGBRegressor(n_estimators=100, random_state=42)로 학습하고 검증 RMSE와 MAE를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
from xgboost import XGBRegressor

model_xgb = XGBRegressor(n_estimators=100, random_state=42)
model_xgb.fit(X_train, y_train)

pred_xgb = model_xgb.predict(X_test)
rmse_xgb = np.sqrt(mean_squared_error(y_test, pred_xgb))
mae_xgb  = mean_absolute_error(y_test, pred_xgb)
print(round(rmse_xgb, 4))
print(round(mae_xgb, 4))
```

</details>

---

### Q6. RandomForest 모델로 X_test 예측 결과를 result.csv로 저장하라. 저장 후 불러와서 shape, 컬럼명, 앞 10개 pred 합계를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = pd.DataFrame({'pred': model_rf.predict(X_test)})
result.to_csv('result.csv', index=False)

check = pd.read_csv('result.csv')
print(check.shape)
print(check.columns.tolist())
print(round(check['pred'].head(10).sum(), 4))
```

</details>

---

### Q7. LinearRegression, RandomForest, XGBoost 세 모델의 RMSE를 비교하고, 가장 낮은 모델명과 RMSE를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
scores = {
    'LinearRegression':      rmse_lr,
    'RandomForestRegressor': rmse_rf,
    'XGBRegressor':          rmse_xgb
}
best = min(scores, key=scores.get)
print(best)
print(round(scores[best], 4))
```

</details>

---

### Q8. RandomForest 모델로 검증 RMSE와 MAE를 함께 출력하라. (소수 넷째 자리)

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
pred_rf = model_rf.predict(X_test)
rmse = np.sqrt(mean_squared_error(y_test, pred_rf))
mae  = mean_absolute_error(y_test, pred_rf)
print(round(rmse, 4))
print(round(mae, 4))
```

</details>
