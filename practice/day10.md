# 10일차 — Sklearn 전처리 + 데이터 합치기

## Import 모음 ★★★ (전처리 순서 기준)

```python
import pandas as pd
import numpy as np

# 1. 결측치 처리
from sklearn.impute import SimpleImputer

# 2. 인코딩 (get_dummies는 pandas 내장 — import 불필요)
from sklearn.preprocessing import LabelEncoder

# 3. X, y 분리 — import 불필요

# 4. 분할
from sklearn.model_selection import train_test_split

# 5. 스케일링
from sklearn.preprocessing import StandardScaler, MinMaxScaler
```

> `StandardScaler`와 `MinMaxScaler`는 같은 경로 — 한 줄로 같이 import 가능

---

## 전처리 순서 흐름 ★★★ (암기 필수)

```
1. 결측치 처리      fillna / SimpleImputer          ← split 전
2. 인코딩           get_dummies / LabelEncoder       ← split 전
3. X, y 분리        X = df.drop('target') / y = df['target']
4. train_test_split test_size, random_state, stratify(분류만)
5. 스케일링         fit_transform(train) / transform(test)  ← split 후
```

### 왜 이 순서인가?

| 단계 | split 전/후 | 이유 |
|---|---|---|
| 결측치 처리 | **전** | 전체 데이터 기준 중앙값/평균 계산이 더 정확 |
| 인코딩 | **전** | 문자→숫자 변환은 누수 없음. train/test 컬럼 구조 통일 |
| 스케일링 | **후** | train 기준으로만 fit — test 정보가 train에 새어들면 데이터 누수 |

### 스케일링 — split 필요 여부 구분

| 상황 | split | 이유 |
|---|---|---|
| 문제에서 "train 기준 fit" 명시 | O | train/test 분리 후 적용 |
| 문제에서 그냥 변환만 요구 | X | 전체 df에 바로 적용 |

```python
# split 필요한 경우 (Q5 패턴)
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)   # fit_transform 금지!

# split 불필요한 경우 (Q8 패턴)
scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[['col1', 'col2']])
scaled_df = pd.DataFrame(scaled, columns=['col1', 'col2'])
```

> **핵심**: 문제에 split 언급 있으면 split 후, 없으면 전체 df에 바로 적용

---

## 개념 정리

### 1. 원핫인코딩 — `pd.get_dummies` ★★★

```python
# 기본 사용
df_encoded = pd.get_dummies(df, columns=['region', 'channel'])

# 결과: region_A, region_B, channel_online, channel_offline ... 컬럼 추가
# 원본 컬럼(region, channel)은 사라짐

# 컬럼 수 확인
print(df_encoded.shape[1])

# 특정 prefix 컬럼만 추출
region_cols = [c for c in df_encoded.columns if c.startswith('region_')]
print(region_cols)
```

> `get_dummies`는 object/category 타입 자동 인코딩. 수치형은 건드리지 않음.

---

### 2. 라벨인코딩 — `LabelEncoder` ★★★

```python
from sklearn.preprocessing import LabelEncoder

le = LabelEncoder()
df['membership_enc'] = le.fit_transform(df['membership'])

# 클래스 목록 (알파벳순 정렬)
print(le.classes_)      # → ['bronze', 'gold', 'silver', 'vip']

# 앞 N개 값 확인
print(df['membership_enc'].head(20).sum())
```

> `classes_` — 인코딩된 숫자와 원래 값의 매핑. 0부터 알파벳순으로 부여.

---

### 3. y (종속변수) — 분류 vs 회귀 ★★★

y가 무슨 값이냐에 따라 문제 유형이 결정돼요.

| y 값 | 문제 유형 | 예시 | 평가지표 |
|---|---|---|---|
| 0/1, 범주 | **분류** | churn, subscribe, grade | accuracy, f1, roc_auc |
| 연속 숫자 | **회귀** | salary, price, delivery_time | RMSE, MAE |

```python
# 분류 — y가 0/1
y = df['churn']          # 0 또는 1
# stratify=y 사용 가능

# 회귀 — y가 연속값
y = df['salary']         # 3000, 4500, 7200 ...
# stratify 사용 불가
```

> 문제에서 항상 어떤 컬럼을 y로 쓸지 명시해줌 — 그 값을 보고 분류/회귀 판단

---

### 4. train_test_split ★★★

```python
from sklearn.model_selection import train_test_split

X = df.drop('target', axis=1)
y = df['target']

# 기본 분할
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# stratify: 클래스 비율 유지
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# shape 확인
print(X_train.shape)
print(X_test.shape)

# 타겟 비율 확인
print(y_train.mean())
print(y_test.mean())
```

> `stratify=y` — 분류 문제에서 클래스 불균형이 있을 때 필수. 없으면 우연히 train/test 비율이 달라질 수 있음.

---

### 4. 스케일링 — `StandardScaler`, `MinMaxScaler` ★★

```python
from sklearn.preprocessing import StandardScaler, MinMaxScaler

# StandardScaler: 평균 0, 표준편차 1
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)   # fit + transform
X_test_scaled  = scaler.transform(X_test)         # transform만 (fit 금지!)

# MinMaxScaler: 0~1 범위로 압축
scaler = MinMaxScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)
```

> **핵심**: `fit`은 train에만. test에는 `transform`만.  
> test에 `fit_transform` 쓰면 데이터 누수(leakage) — 실전에서 오답 처리.

---

### 5. 결측치 대체 — `SimpleImputer` ★★

```python
from sklearn.impute import SimpleImputer

# 중앙값으로 대체
imp = SimpleImputer(strategy='median')
X_train_imp = imp.fit_transform(X_train)
X_test_imp  = imp.transform(X_test)

# strategy 옵션
# 'mean'     — 평균
# 'median'   — 중앙값
# 'most_frequent' — 최빈값 (범주형에 사용)
# 'constant' — 고정값 (fill_value 파라미터 함께 사용)
```

> pandas `fillna`와 달리 sklearn 파이프라인에 연결 가능. 시험에서는 `fillna`도 정답.

---

### 6. merge / concat ★★

```python
# merge — 키 기준으로 합치기 (SQL JOIN)
result = pd.merge(df1, df2, on='id', how='left')
# how: 'inner'(기본), 'left', 'right', 'outer'

# concat — 행/열 방향으로 붙이기
result = pd.concat([df1, df2], axis=0)   # 행 방향 (위아래)
result = pd.concat([df1, df2], axis=1)   # 열 방향 (좌우)

# index 초기화
result = pd.concat([df1, df2], axis=0).reset_index(drop=True)
```

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer

data = {
    'id':         list(range(1, 21)),
    'age':        [25, 32, None, 45, 28, 52, 31, None, 41, 38,
                   24, 33, 47, 29, 36, 55, 22, 48, 37, None],
    'income':     [3000, 4500, 3800, None, 2800, 6100, 4200, 3600, None, 4100,
                   3100, 4700, 5500, 3900, 4300, 7200, 2500, 5800, 4000, 3400],
    'region':     ['서울', '경기', '서울', '부산', '경기', '서울', '부산', '경기',
                   '서울', '부산', '경기', '서울', '부산', '서울', '경기',
                   '부산', '서울', '경기', '부산', '서울'],
    'membership': ['silver', 'gold', 'bronze', 'vip', 'bronze', 'vip', 'gold',
                   'silver', 'gold', 'bronze', 'silver', 'vip', 'gold', 'bronze',
                   'silver', 'vip', 'bronze', 'gold', 'silver', 'bronze'],
    'channel':    ['online', 'offline', 'online', 'offline', 'online', 'offline',
                   'online', 'online', 'offline', 'online', 'offline', 'online',
                   'offline', 'online', 'offline', 'online', 'offline', 'online',
                   'offline', 'online'],
    'churn':      [0, 0, 1, 0, 1, 0, 0, 1, 0, 1,
                   1, 0, 0, 1, 0, 0, 1, 0, 1, 1]
}
df = pd.DataFrame(data)
```

---

### Q1. region과 channel을 원핫인코딩하라. 인코딩 후 전체 컬럼 수와 'region_'으로 시작하는 컬럼 리스트를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df_enc = pd.get_dummies(df, columns=['region', 'channel'])
print(df_enc.shape[1])
print([c for c in df_enc.columns if c.startswith('region_')])
```

</details>

---

### Q2. membership을 LabelEncoder로 변환하라. classes_ 리스트와 앞 10개 인코딩 값의 합을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
le = LabelEncoder()
df['membership_enc'] = le.fit_transform(df['membership'])
print(list(le.classes_))
print(df['membership_enc'].head(10).sum())
```

</details>

---

### Q3. churn을 종속변수로 test_size=0.25, random_state=42, stratify 적용해 분할하라. train/test shape과 각 churn 평균을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
X = df.drop('churn', axis=1)
y = df['churn']

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

print(X_train.shape)
print(X_test.shape)
print(round(y_train.mean(), 4))
print(round(y_test.mean(), 4))
```

</details>

---

### Q4. age와 income의 결측치를 각 컬럼의 중앙값으로 채워라. 처리 전 결측치 수와 처리 후 income 평균을 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(df[['age', 'income']].isnull().sum().sum())

df['age'] = df['age'].fillna(df['age'].median())
df['income'] = df['income'].fillna(df['income'].median())

print(round(df['income'].mean(), 2))
```

</details>

---

### Q5. age와 income을 StandardScaler로 스케일링하라. (train 기준 fit, test는 transform만) train의 age 평균과 표준편차를 소수 넷째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
# 결측치 먼저 처리
df['age'] = df['age'].fillna(df['age'].median())
df['income'] = df['income'].fillna(df['income'].median())

X = df[['age', 'income']]
y = df['churn']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled  = scaler.transform(X_test)

import pandas as pd
X_train_df = pd.DataFrame(X_train_scaled, columns=['age', 'income'])
print(round(X_train_df['age'].mean(), 4))
print(round(X_train_df['age'].std(), 4))
```

> StandardScaler 적용 후 train의 평균 ≈ 0, 표준편차 ≈ 1.

</details>

---

### Q6. 아래 두 데이터를 id 기준 left join으로 합쳐라. 합친 후 전체 행 수와 score 결측치 수를 출력하라.

```python
df_score = pd.DataFrame({
    'id':    [1, 3, 5, 7, 9, 11, 13, 15],
    'score': [88, 72, 95, 61, 83, 77, 90, 55]
})
```

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
result = pd.merge(df, df_score, on='id', how='left')
print(result.shape[0])
print(result['score'].isnull().sum())
```

</details>

---

### Q7. region별 membership 최빈값으로 이루어진 Series를 만들고, df와 concat(axis=1)으로 붙여라. 새 컬럼명은 'region_top_membership'으로 하고 앞 5행을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
region_mode = df.groupby('region')['membership'].transform(lambda x: x.mode()[0])
df['region_top_membership'] = region_mode
print(df[['region', 'membership', 'region_top_membership']].head())
```

> `concat` 대신 직접 컬럼으로 붙이는 게 더 간결. concat은 별도 Series를 붙일 때 사용.

</details>

---

### Q8. MinMaxScaler로 age와 income을 0~1 범위로 변환하라. 변환 후 income의 최솟값과 최댓값을 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['age'] = df['age'].fillna(df['age'].median())
df['income'] = df['income'].fillna(df['income'].median())

scaler = MinMaxScaler()
scaled = scaler.fit_transform(df[['age', 'income']])
scaled_df = pd.DataFrame(scaled, columns=['age', 'income'])

print(round(scaled_df['income'].min(), 4))
print(round(scaled_df['income'].max(), 4))
```

> MinMaxScaler 적용 후 최솟값 = 0.0, 최댓값 = 1.0.

</details>
