# 재도전 Day 5 — 2유형 ② 회귀 + 라벨 인코딩 vs 원핫 인코딩

> 2026-11-25 (수) · 목표 2시간 · 복습 10분 → 개념 40분 → 풀세트 60분 → 정리 10분
>
> 시작 전: [Day 4 복습](복습_day4.md) 5번 "⭐ 어려웠던 것" 3분
>
> **오늘은 새로 배울 게 적다.** Day 4의 5단계 템플릿(1-1 ~ 5-3) 그대로 가고, **분류와 다른 곳**만 바꾼다.
> 사용자 요청: **라벨 인코딩(LabelEncoder)** 도 원핫 인코딩과 함께 배운다 (3-1).

---

## 🪜 진행 순서 (번호 = 단계-조각, Day 4와 같음)

| 단계 | 조각 | 분류(Day 4)와 다른 곳 | 풀 문제 |
|---|---|---|---|
| **1 탐색** | 1-1 불러오기 · 1-2 훑어보기 | **정답 컬럼을 보고 분류/회귀 판단** | Q1 |
| **2 전처리 ①** | 2-1 나누기 · 2-2 결측 | 같음 | Q2 앞 |
| **3 전처리 ②** | 3-1 인코딩 **A 원핫 / B 라벨** | ⭐ 라벨 인코딩 새로 배움 | Q2 뒤 |
| **4 모델링** | 4-1 분할 · 4-2 학습 · 4-3 예측 · 4-4 점수 | **stratify 없음 · Regressor · predict만 · RMSE** | Q3, Q4 |
| **5 제출** | 5-1 다시 학습 · 5-2 저장 · 5-3 확인 | **predict로 제출** (proba 없음) | Q5 |

---

## 0. 분류 vs 회귀 — 다른 곳은 4군데뿐 ⭐⭐⭐

| | 분류 (Day 4) | **회귀 (오늘)** |
|---|---|---|
| 정답 | 0/1처럼 **몇 종류** (이탈 여부) | **값이 제각각인 숫자** (가격) |
| 4-1 분할 | `stratify=y` | **없음** (넣으면 에러) |
| 4-2 모델 | `RandomForestClassifier` | **`RandomForestRegressor`** |
| 4-3 예측 | `predict` / `predict_proba` | **`predict`만** (확률이 없다) |
| 4-4 점수 | ROC-AUC, F1, accuracy (**높을수록** 좋음) | **RMSE**, MAE, R² (**RMSE·MAE는 낮을수록** 좋음) |
| 5-2 제출 | 지표에 따라 확률 또는 0/1 | **`predict` 그대로** (예측 가격) |

나머지(불러오기·나누기·결측·인코딩·다시 학습·확인)는 **글자 하나 안 바뀐다.**

---

## 1-2. 분류인지 회귀인지 판단하기

```python
print(train['price'].nunique())    # 서로 다른 값의 개수
print(train['price'].head())
```

| 보이는 것 | 판단 |
|---|---|
| 2~10개쯤 (0/1, A/B/C) | 분류 |
| **수백 개** (3020, 2890, 4150 …) | **회귀** |

> 문제 문장으로도 알 수 있다: "**가격을 예측**", "판매량", "점수" → 회귀 / "**여부**", "등급", "종류" → 분류
> 평가지표로도 알 수 있다: **RMSE·MAE·R² → 회귀** / AUC·F1·accuracy → 분류

---

## 3-1. 인코딩 — A 원핫 vs B 라벨 ⭐ (사용자 요청)

글자 컬럼을 숫자로 바꾸는 방법 두 가지. **둘 다 "합쳐서 → 바꾸고 → iloc으로 다시 나누기"** 는 같다.

### 결과 모양 비교 (실행 결과)

`brand = ['현대', '기아', 'BMW', '현대']`

```
A. 원핫 (get_dummies)                  B. 라벨 (LabelEncoder)
   brand_BMW  brand_기아  brand_현대        brand
       0          0          1               2
       0          1          0               1
       1          0          0               0
       0          0          1               2
→ 컬럼이 값 종류만큼 늘어남                → 컬럼 1개 그대로, 값이 0, 1, 2…
                                          (번호는 가나다·ABC 순: BMW=0, 기아=1, 현대=2)
```

### 코드 비교

```python
all_x = pd.concat([X, X_test])
cols = ['brand', 'fuel', 'transmission', 'accident']

# A. 원핫 — 한 줄
all_x = pd.get_dummies(all_x, columns=cols)

# B. 라벨 — 컬럼마다 반복
from sklearn.preprocessing import LabelEncoder
for c in cols:
    le = LabelEncoder()                       # 컬럼마다 새로 만든다
    all_x[c] = le.fit_transform(all_x[c])     # 합친 표에서 바로 fit_transform

X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]
```

> `for c in cols:` — 목록의 컬럼을 하나씩 `c`에 넣어 아래 두 줄을 반복한다 (4번 반복)
> **합친 표(all_x)에서 하면** 지난번 오답 2개를 저절로 피한다 ↓

### 라벨 인코딩 함정 (지난번 오답노트 + 실행 확인)

| 함정 | 결과 | 합쳐서 하면? |
|---|---|---|
| train에서만 fit → test에 처음 보는 값 | `ValueError: y contains previously unseen labels` | ✅ 합친 표에 모든 값이 있어 안전 |
| 같은 `le`로 여러 컬럼을 fit·transform 순서 섞기 | 엉뚱한 기준으로 변환 / 에러 | ✅ for문에서 컬럼마다 새 `le` |
| `le.fit_transform(all_x)` — 표 전체에 | 에러 (컬럼 하나씩만 가능) | ✅ `all_x[c]` 컬럼 하나씩 |

### 언제 뭘 쓰나 (이번 데이터로 비교)

| | 원핫 (get_dummies) | 라벨 (LabelEncoder) |
|---|---|---|
| 컬럼 수 | 8 → **18** | 8 → **8** |
| 검증 RMSE | 342.81 | 343.82 |
| test RMSE | 342.18 | 344.76 |
| 코드 | 한 줄 | for문 |
| 쓰는 때 | **기본 (추천)** | 문제가 "라벨 인코딩"이라 할 때 · 값 종류가 아주 많을 때(원핫이면 컬럼 수백 개) |

> 랜덤포레스트는 둘 다 잘 된다 (차이 1~2). **문제가 지정하지 않으면 원핫으로 통일**, 라벨은 "지정받았을 때 쓸 줄 아는" 정도면 충분

---

## 4. 모델링 — 분류와 다른 곳

### 4-1 분할 — `stratify` 빼기

```python
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42)
```

> 회귀에 `stratify=y`를 넣으면 `ValueError: The least populated class in y has only 1 member` (Day 4에서 확인)

### 4-2 학습 — `Regressor`

```python
from sklearn.ensemble import RandomForestRegressor
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

### 4-3 예측 — `predict`만

```python
pred = model.predict(X_value)      # 예측 가격 (예: 3021.4, 2875.0 …)
```

> 회귀에는 `predict_proba`가 없다 (확률이라는 개념이 없음)

### 4-4 점수 — RMSE (낮을수록 좋음)

```python
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

rmse = np.sqrt(mean_squared_error(y_value, pred))    # ⭐ RMSE = MSE에 루트
print(round(rmse, 2))
print(round(mean_absolute_error(y_value, pred), 2))  # MAE
print(round(r2_score(y_value, pred), 4))             # R² (1에 가까울수록 좋음)
```

| 지표 | 뜻 | 좋은 쪽 |
|---|---|---|
| **RMSE** | 예측이 평균적으로 **얼마나 빗나갔나** (단위 = 가격 단위, 만원) | **낮을수록** |
| MAE | 빗나간 크기의 평균 (큰 실수에 덜 민감) | 낮을수록 |
| R² | 가격의 들쭉날쭉함을 몇 % 설명하나 | 1에 가까울수록 |

> ⚠️ `mean_squared_error(..., squared=False)`는 **최신 sklearn(1.6)에서 에러** (`unexpected keyword argument 'squared'`). 버전에 상관없이 되는 **`np.sqrt(mean_squared_error(...))`** 로 외운다
> 정답 먼저: `mean_squared_error(y_value, pred)`
> 망가졌는지 확인: **평균만 찍었을 때 RMSE**(≈ 가격의 표준편차, 이번엔 약 1300)보다 **확실히 작으면** 정상

---

## 5. 제출 — `predict` 그대로

```python
model.fit(X, y)                                                 # 5-1
pred = model.predict(X_test)                                    # 5-2 — X_test!
pd.DataFrame({'pred': pred}).to_csv('result.csv', index=False)
r = pd.read_csv('result.csv')                                   # 5-3
print(r.shape)        # (200, 1) — test 행 수
print(r.head())       # 가격처럼 보이는 숫자
```

---

## 오늘의 함정 요약

| 함정 | 기억할 한 줄 |
|---|---|
| 회귀에 `stratify=y` | 에러 → 빼기 |
| `Classifier`를 그대로 | **`Regressor`** |
| 회귀에 `predict_proba` | 없다 → `predict` |
| `squared=False` | 최신 버전 에러 → **`np.sqrt(mean_squared_error(...))`** |
| RMSE가 클수록 좋다? | **낮을수록** 좋다 |
| 라벨 인코딩을 train에서만 | 처음 보는 값 에러 → **합친 표에서, 컬럼마다 새 `le`** |

---

# 풀세트 — 중고차 가격 예측

## 데이터 세팅

```python
train = pd.read_csv('retake/data/day5/car_train.csv')   # 800행, 정답 price 있음
test  = pd.read_csv('retake/data/day5/car_test.csv')    # 200행, 정답 없음
```

| 컬럼 | 뜻 |
|---|---|
| `car_id` | 차량 번호 (**모델에 넣지 않는다**) |
| `brand` | 제조사 (현대·기아·쉐보레·르노·BMW) |
| `fuel` | 연료 (결측 있음) |
| `transmission` | 변속기 (자동/수동) |
| `year` | 연식 |
| `mileage` | 주행거리 km (결측 있음) |
| `engine_cc` | 배기량 (결측 있음) |
| `accident` | 사고 이력 (Y/N) |
| `owners` | 소유자 수 |
| **`price`** | **판매 가격 (만원) — train에만 있음** |

> `retake/data/day5/_answer_do_not_open.csv`는 채점용. **열지 말 것.**
> 풀이는 `workspace/day5.py`. Day 4 풀이를 복사하지 말고 **처음부터** 친다 (다른 곳 4군데를 손으로 익히기 위해).

---

### Q1. (탐색) 다음을 각각 출력하고, **분류인지 회귀인지** 주석으로 적어라.
1. train·test의 행·열 수
2. train의 결측 컬럼과 개수
3. `price`의 평균 (정수)
4. `price`가 **몇 종류의 값**을 갖는지 (서로 다른 값의 개수)

> (11/25 문장 수정 — 처음 문장 "평균과 서로 다른 값의 개수"가 "평균과 다른 값"으로 읽혀 애매했다)

### Q2. (전처리) 아래처럼 전처리하라.
1. `y` = `price` / `X` = train에서 `car_id`, `price` 제외 / `X_test` = test에서 `car_id` 제외
2. `mileage`, `engine_cc` 결측 → **train 중앙값** / `fuel` 결측 → `'없음'`
3. **A.** `brand`, `fuel`, `transmission`, `accident`를 합쳐서 **원핫 인코딩** → `X`, `X_test` shape 출력
4. **B.** (따로 한 번 더) 같은 컬럼을 **LabelEncoder**로 인코딩한 버전도 만들어 shape 출력 — 변수 이름은 `X_lb`, `X_test_lb`처럼 구분

### Q3. (모델 · 원핫 버전) `train_test_split(test_size=0.2, random_state=42)`로 나누고 `RandomForestRegressor(n_estimators=100, random_state=42)`로 학습하라. 검증 **RMSE**와 **MAE**를 소수 둘째 자리까지 출력하라.

### Q4. (비교 · 라벨 버전) Q2-B의 라벨 인코딩 데이터로 Q3과 똑같이 하고 검증 **RMSE**를 출력하라. 원핫과 차이를 주석으로 적어라.

### Q5. (제출) 원핫 버전 모델을 **train 전체로 다시 학습**한 뒤 test 차량의 가격을 예측해 `pred` 컬럼 하나짜리 `result.csv`로 저장하라. 다시 불러와 shape과 앞 5행을 출력하라.

> 채점: Q5는 숨겨진 test 정답으로 **RMSE 400 이하면 통과** (기본 템플릿 약 342, 평균만 찍으면 약 1382).

---

## 채점 결과 — ✅ 2 · △ 2 · ❌ 1 → 재풀이 5 / 5 ✅ / 제출 통과 (test RMSE 342.18) (2026-11-25)

| # | 내 출력 | 정답 | 결과 | 메모 |
|---|---|---|---|---|
| Q1 | (800, 10) (200, 9) / fuel 22·mileage 43·engine_cc 28 / 3093 / `value_counts()` 표 (Length: 393) / "회귀임" | … / **393** | △ | 문제 문장이 애매했음 ("평균과 다른 값"으로 읽힘 — 출제 쪽 잘못). 어느 해석이든 출력은 **숫자 하나**여야 → `nunique()` |
| Q2 | (800, 18) (200, 18) / (800, 8) (200, 8) | 같음 | △ | 값은 맞지만 `pd.get_dummies(all_x, cols)` — **위치 인자 함정** (아래) |
| Q3 | 342.81 / 258.85 | 342.81 / 258.85 | ✅ | |
| Q4 | 342.81 / 258.85 ("값이 똑같은데..?") | **343.82** | ❌ | RMSE 계산에 라벨 모델의 `pred_lb` 대신 **원핫의 `pred`** 를 넣음 |
| Q5 | `result.csv` (200, 1) | test RMSE ≤ 400 | ✅ **342.18** | `head()` 출력은 빠짐 (문제 요구사항) |

### Q1 △ — "서로 다른 값의 개수"는 `nunique()` 한 숫자

```python
# 내 풀이 — 393개짜리 value_counts 표가 출력되고, 개수는 맨 아래 Length: 393으로만 보임
p = train['price']
print(p[p != m].value_counts())     # p != m 필터는 의미 없음 (평균 3093인 차는 0대)

# 모범답안
print(train['price'].nunique())     # 393
```

> 1유형식 값 문제였다면 "393"을 직접 찍어야 한다. `value_counts()` = 값별 개수 표 / **`nunique()` = 종류 수 한 숫자** / `unique()` = 종류 목록

### Q2 △ — `pd.get_dummies(all_x, cols)` : 두 번째 자리는 `columns`가 아니라 `prefix` ⚠️

```python
pd.get_dummies(all_x, cols)               # 내 풀이 — cols가 prefix(새 컬럼 이름 앞머리)로 들어감
pd.get_dummies(all_x, columns=cols)       # ✅ 모범답안
```

`pd.get_dummies`의 순서: `(data, prefix=None, prefix_sep='_', ..., columns=None, ...)` — **`columns`는 이름을 붙여야** 한다.

이번엔 **우연히** 같은 결과가 나왔다 (실행 확인):

| 상황 | 결과 |
|---|---|
| 이번 데이터 (글자 컬럼이 딱 4개, 목록 순서와 같음) | `columns=`와 결과 같음 → 운 |
| 목록 순서가 다르면 `['fuel', 'brand', …]` | 브랜드 컬럼이 **`fuel_현대`**, 연료가 **`brand_LPG`** 로 이름이 뒤바뀜 (에러 없음!) |
| 글자 컬럼이 5개인데 목록이 4개면 | `ValueError: Length of 'prefix' (4) did not match` |

> `columns=` 없이 쓰면 pandas가 **글자 컬럼을 전부 알아서** 인코딩하고, 넘긴 목록은 이름표로만 쓴다
> **옵션은 이름=값으로**: `columns=`, `test_size=`, `random_state=`, `average=` — 이름 없이 쓰는 건 맨 앞 데이터(`X`, `y`)뿐

👍 좋았던 점: 원핫 결과를 **`onehot_x`라는 새 변수**에 담아서 `all_x`(원본 합친 표)를 라벨 인코딩에 그대로 재사용 — 두 버전이 서로 안 섞이게 한 설계가 좋다.

### Q3 ✅

```python
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
pred = model.predict(X_value)
print(round(np.sqrt(mean_squared_error(y_value, pred)), 2))   # 342.81
print(round(mean_absolute_error(y_value, pred), 2))           # 258.85
```

### Q4 ❌ — 예측 변수를 잘못 넣음 → "값이 똑같은데..?"의 원인

```python
pred_lb = model_lb.predict(X_lb_value)
rmse_lb = np.sqrt(mean_squared_error(y_lb_value, pred))      # ❌ pred = 원핫 모델의 예측
rmse_lb = np.sqrt(mean_squared_error(y_lb_value, pred_lb))   # ✅ 343.82
```

> 값이 똑같았던 건 라벨·원핫이 같아서가 아니라 **같은 예측을 두 번 채점**했기 때문. 고치면 원핫 342.81 vs 라벨 343.82 (차이 1, 둘 다 OK)
> `y_lb_value`는 `y_value`와 같은 행 (같은 `random_state=42`)이라 정답 쪽은 문제없었다
> **"이상하다"고 느낀 감각이 정확했다** 👍 — 결과가 의심스러우면 그 줄에 넣은 **변수 이름**부터 확인

### Q5 ✅ — 제출 통과 (test RMSE 342.18)

```python
model.fit(X, y)
pred = model.predict(X_test)
pd.DataFrame({'pred': pred}).to_csv('result.csv', index=False)
df = pd.read_csv('result.csv')
print(df.shape)     # (200, 1)
print(df.head())    # ← 문제에서 요구 (빠짐)
```

### 재풀이 — 5 / 5 ✅

| # | 고친 것 | 출력 |
|---|---|---|
| Q1 | `print(p[p != m].nunique())` — 숫자 하나로 | 393 ✅ (`p != m`은 없어도 같은 값) |
| Q2 | `onehot_x = pd.get_dummies(all_x, columns=cols)` | (800, 18) ✅ |
| Q4 | `mean_squared_error(y_lb_value, pred_lb)` | 343.82 ✅ (원핫 342.81과 차이 1) |
| Q5 | `print(df.head())` 추가 | ✅ |
| 회귀 구현 | `RandomForestRegressor(n_estimators=100, random_state=42)` | 매번 같은 값 ✅ |

> 질문: "`pd.get_dummies(all_x, columns=[...])`로 외웠는데 운이 좋았던 거야?" → **외운 모양은 정확**. 운이 좋았던 건 Q2에서 `columns=` 없이 `cols`만 넘긴 줄. `columns=cols`처럼 변수로 넘기는 건 완전히 같다

### 위쪽 "회귀 구현"에서 나온 질문 (실행으로 확인)

| 질문 | 답 |
|---|---|
| RMSE·MAE가 실행마다 다른 이유 | 모델에 `random_state`가 없어서 (332.94 / 342.46 / 42면 항상 343.31). **분할에도 모델에도 `random_state=42`** |
| RMSE는 어느 정도가 좋은가 | 절대 기준 없음. **평균만 찍었을 때(≈1387)보다 확실히 작으면** 정상. 단위는 정답과 같음(만원) |
| `X_value`는? | **val**idation(검증)의 줄임 — 학습에 안 쓰고 숨겨 둔 20% (160대)의 문제. 정답은 `y_value` |
| 20%가 학습 데이터? | 아니다. 80%(`X_train`)가 학습, 20%(`X_value`)는 **검증**. 5-1에서 100% 다시 학습 |
| X_test 결측도 train 값으로? | 그렇다. 2-2 시점엔 분할 전이라 **`X`(train 전체)** 의 값 |
| 결측 '없음' vs 최빈값 | 점수 차이 거의 없음 (Day 4 비교). 문제가 정하면 그대로 |
| LabelEncoder 강제 출제? | 실제 2유형은 방법 자유(결과만 채점)라 가능성 낮음. 모의문제·교재엔 있음 → 쓸 줄만 알면 충분 |
| 라벨 인코딩 함정 | ① test에만 있는 값 → unseen 에러 ② `le` 하나 돌려쓰기 → 사전 덮어씀 ③ 표 전체에 → 1d 에러 → **합쳐서, 컬럼마다 새 `le`** 로 셋 다 해결
