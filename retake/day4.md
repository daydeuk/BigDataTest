# 재도전 Day 4 — 2유형 ① 분류 전체 흐름

> 2026-11-22 (일) · 목표 3~4시간 · 복습 10분 → 개념 60분 → 풀세트 90분 → 오답 정리 20분
>
> 시작 전: [Day 3 복습](복습_day3.md) · [⭐ 핵심 반복 복습](핵심_반복복습.md) 3분
>
> **2유형 = 40점, 배점이 가장 크다.** 지난번 35점 → 이번 목표 만점.
> 오늘의 목표는 **"5단계 템플릿을 안 보고 칠 수 있게"** 되는 것이다. 모델 이론은 몰라도 된다.

---

## 🪜 차근차근 진행 순서 (사용자 요청 — 한 번에 통으로 말고 단계별로)

한 단계씩: **설명 읽기 → 그 단계만 쳐서 ▷ 실행 → 출력 확인 → 다음 단계**

> **번호는 하나로 통일**: `단계-조각` (예: 4-1 = 4단계 모델링의 첫 조각 "분할"). 템플릿 주석·설명 제목·진행 메모 모두 이 번호를 쓴다.

| 단계 | 조각 | 하는 일 | 풀 문제 | 확인할 출력 |
|---|---|---|---|---|
| **1 탐색** | 1-1 불러오기 · 1-2 훑어보기 | `read_csv`, `info`, `isnull().sum()`, 정답 비율 | Q1 | shape, 결측, 이탈 비율 |
| **2 전처리 ①** | 2-1 나누기 · 2-2 결측 | `y` / `X` / `X_test`, train 기준으로 채우기 | Q2 앞 | 결측 `0 0` |
| **3 전처리 ②** | 3-1 인코딩 | 합치기 → `get_dummies` → `iloc`으로 다시 나누기 | Q2 뒤 | `X`, `X_test` 열 수 같음 |
| **4 모델링** | 4-1 분할 · 4-2 학습 · 4-3 예측 · 4-4 점수 | `train_test_split`, `fit`, `predict`/`predict_proba`, 지표 | Q3, Q4 | 0~1 사이 점수 |
| **5 제출** | 5-1 다시 학습 · 5-2 저장 · 5-3 확인 | `fit(X, y)`, `to_csv(index=False)`, `read_csv` | Q5 | shape (300, 1) |

---

## 0. 2유형 시험은 이렇게 나온다

| 항목 | 내용 |
|---|---|
| 주는 것 | **train 파일** (정답 컬럼 있음) + **test 파일** (정답 컬럼 없음) |
| 할 일 | train으로 모델을 학습 → test의 정답을 예측 |
| 제출 | 예측값을 **`result.csv`** 로 저장 (컬럼 이름은 문제가 정해 줌, 보통 `pred`) |
| 채점 | 숨겨진 test 정답과 비교한 **평가지표 점수**(ROC-AUC, F1 등)가 기준 이상이면 점수 |
| 제약 | 코드 **실행 1분 제한** · 자동완성 없음 · `help()` 가능 |

> 1유형처럼 "정답 숫자 하나"가 아니다. **제출 파일이 형식대로 만들어졌는지 + 점수가 기준을 넘는지**가 전부다.
> 그래서 **복잡한 모델보다 실수 없는 템플릿**이 중요하다. 랜덤포레스트 하나면 충분하다.

---

## 1. 전체 흐름 — 5단계 템플릿 ⭐⭐⭐ (오늘 외울 것)

```python
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score

# 1-1. 불러오기
train = pd.read_csv('train.csv')
test  = pd.read_csv('test.csv')

# 1-2. 훑어보기 (확인만)
print(train.info())
print(train.isnull().sum())
print(train['target'].value_counts())

# 2-1. 나누기 — y / X / X_test (id·정답 컬럼 빼기)
y = train['target']
X = train.drop(columns=['id', 'target'])
X_test = test.drop(columns=['id'])

# 2-2. 결측 — train 기준 값으로 X, X_test 둘 다
m = X['age'].median()
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)

# 3-1. 인코딩 — 합쳐서 get_dummies → 다시 나누기
all_x = pd.concat([X, X_test])
all_x = pd.get_dummies(all_x, columns=['gender', 'region'])
X = all_x.iloc[:len(X)]
X_test = all_x.iloc[len(X):]

# 4-1. 분할 — 검증용 떼어 내기
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# 4-2. 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)

# 4-3. 예측
pred  = model.predict(X_val)                  # 0/1  → F1, accuracy
proba = model.predict_proba(X_val)[:, 1]      # 확률 → ROC-AUC

# 4-4. 점수 — 정답이 앞, 예측이 뒤
print(roc_auc_score(y_val, proba))

# 5-1. 다시 학습 (선택) — train 전체로
model.fit(X, y)

# 5-2. 저장 — test 예측 → result.csv
pred = model.predict_proba(X_test)[:, 1]
pd.DataFrame({'pred': pred}).to_csv('result.csv', index=False)

# 5-3. 확인
print(pd.read_csv('result.csv').shape)
```

**외우는 법 — 5단계 이름만 먼저**: `탐색 → 전처리①(나누기·결측) → 전처리②(인코딩) → 모델링(분할·학습·예측·점수) → 제출`

---

## 2. 단계별 설명

### 2-1. 나누기 — X, y, X_test

| 변수 | 내용 | 만드는 법 |
|---|---|---|
| `y` | train의 **정답** | `train['target']` |
| `X` | train의 **문제** (정답·id 뺀 나머지) | `train.drop(columns=['id', 'target'])` |
| `X_test` | test의 문제 (id 뺀 나머지) | `test.drop(columns=['id'])` |

> **id는 반드시 뺀다.** 고객 번호는 이탈과 상관없는 숫자라서 모델을 헷갈리게 한다.
> 지난번 오답: 제출용 X를 `train.drop(...)`으로 만듦 → **`X_test`는 `test`에서** 만든다.

### 2-2. 결측 — "train 기준"으로 둘 다

```python
m = X['age'].median()              # ← train(X)의 중앙값
X['age'] = X['age'].fillna(m)
X_test['age'] = X_test['age'].fillna(m)    # ← test도 train 값으로

X['payment'] = X['payment'].fillna('없음')        # 글자 컬럼은 '없음' 같은 새 값으로
X_test['payment'] = X_test['payment'].fillna('없음')
```

> 숫자 → **중앙값**(또는 평균), 글자 → **`'없음'`** (또는 최빈값). Day 1 결측치 그대로.
> test 값으로 test를 채우면 안 되냐? 시험 점수엔 거의 영향 없지만, **"train 기준"이 원칙**이다.
> 로컬 sklearn(1.6)은 랜덤포레스트가 결측을 그냥 받아 주지만, **시험장 버전은 다를 수 있다 → 무조건 채운다.**

### 3-1. 인코딩 — 왜 합쳐서 하나 ⚠️

모델은 글자를 못 읽는다 → 글자 컬럼을 0/1 컬럼으로 바꾼다 (`get_dummies` = 원핫 인코딩).

```
pay        →   pay_카드  pay_현금
카드              True     False
현금              False    True
```

**따로 하면 컬럼이 어긋난다** — 실제 실행:

```python
train쪽 pay: ['카드', '현금', '카드']  →  컬럼 ['x', 'pay_카드', 'pay_현금']
test쪽  pay: ['카드', '계좌']          →  컬럼 ['x', 'pay_계좌', 'pay_카드']   ← 다름!

model.predict(test쪽)
# ValueError: The feature names should match those that were passed during fit.
# Feature names unseen at fit time: - pay_계좌
```

**합쳐서 하면 컬럼이 같아진다**

```python
all_x = pd.concat([X, X_test])                 # 위아래로 붙이기 (train 1000행 + test 300행)
all_x = pd.get_dummies(all_x, columns=[...])  # 한 번에 인코딩
X = all_x.iloc[:len(X)]                        # 앞 1000행 = train
X_test = all_x.iloc[len(X):]                   # 나머지 300행 = test
```

> `iloc[:len(X)]` — Day 1의 **위치 번호** 슬라이싱. concat하면 이름표가 겹치므로(0~999, 0~299) **반드시 iloc**.
> 지난번 오답: `pd.concat(X, X_test)` → **리스트로 감싸야** 한다 `pd.concat([X, X_test])`

### 4-1. 분할 — 검증용 떼어 내기 (내 점수 미리 보기)

test에는 정답이 없어서 점수를 모른다 → train의 20%를 떼어서 **모의 시험**을 본다.

```python
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
```

| 결과 | 뜻 |
|---|---|
| `X_tr`, `y_tr` (80%) | 공부용 |
| `X_val`, `y_val` (20%) | 모의 시험용 |

> **순서 고정: `X_tr, X_val, y_tr, y_val`** (X 둘 → y 둘). 지난번 단골 실수
> `stratify=y` — 분류일 때 정답 비율(이탈 43%)을 공부용·시험용에 똑같이 나눠 준다. **분류는 필수**
> `random_state=42` — 매번 같은 결과가 나오게 고정 (문제에서 주는 값 그대로)

### 4-2 학습 · 4-3 예측 · 4-4 점수 ⭐ predict vs predict_proba

```python
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)                          # 공부 (문제, 정답)

pred  = model.predict(X_val)                   # 0 또는 1
proba = model.predict_proba(X_val)[:, 1]       # 1일 확률 (0~1)
```

| 지표 | 무엇을 넣나 | 코드 |
|---|---|---|
| **ROC-AUC** | **확률** | `roc_auc_score(y_val, proba)` |
| F1 (macro) | 0/1 | `f1_score(y_val, pred, average='macro')` |
| accuracy | 0/1 | `accuracy_score(y_val, pred)` |

> **정답(y_val)이 항상 앞**, 예측이 뒤.
> `predict_proba`는 열이 2개 (0일 확률, 1일 확률) → **`[:, 1]`** 로 "1일 확률"만. 지난번 **반복 실수 ⚠️**
> 문제가 "**확률**을 제출" / 평가지표가 **ROC-AUC** → `predict_proba()[:, 1]`
> 문제가 "**0/1(또는 클래스)**를 제출" / 평가지표가 **F1·accuracy** → `predict()`

**0/1로 내면 손해다** — 이번 데이터에서 실제로 확인:

| 제출 | test ROC-AUC |
|---|---|
| `predict_proba()[:, 1]` (확률) | **0.851** |
| `predict()` (0/1) | 0.756 |

### 5-1 다시 학습 · 5-2 저장 · 5-3 확인

```python
model.fit(X, y)                                # (선택) 검증 끝났으면 train 전체로 다시 학습
pred = model.predict_proba(X_test)[:, 1]       # test 예측
pd.DataFrame({'pred': pred}).to_csv('result.csv', index=False)

r = pd.read_csv('result.csv')                  # 꼭 다시 열어서 확인
print(r.shape)        # (test 행 수, 1) 이어야 함
print(r.head())
```

> **`index=False` 필수** — 없으면 이름표 컬럼(`Unnamed: 0`)이 하나 더 생겨 형식 오류
> 컬럼 이름은 **문제에서 정한 그대로** (`pred`, `target` 등)
> 행 수가 **test 행 수와 같은지** 꼭 확인
> 다시 학습(`fit(X, y)`)은 안 해도 점수는 나온다. 하면 데이터를 20% 더 써서 보통 조금 좋아진다

---

## 오늘의 함정 요약

| 함정 | 기억할 한 줄 |
|---|---|
| id를 안 뺌 | `drop(columns=['id', 'target'])` |
| X_test를 train에서 만듦 | **`X_test = test.drop(...)`** |
| 결측 안 채움 | 숫자 → train 중앙값, 글자 → `'없음'` (X, X_test 둘 다) |
| 인코딩을 따로 함 | **합쳐서** `get_dummies` → `iloc`으로 나누기 |
| `pd.concat(X, X_test)` | 리스트로: `pd.concat([X, X_test])` |
| 분할 순서 | `X_tr, X_val, y_tr, y_val` |
| 분류인데 stratify 없음 | `stratify=y` |
| ROC-AUC에 0/1 | `predict_proba(...)[:, 1]` |
| `index=False` 빠짐 | `to_csv('result.csv', index=False)` |
| 제출 확인 안 함 | `pd.read_csv('result.csv').shape` |

---

# 풀세트 — 고객 이탈 예측

## 데이터 세팅

```python
train = pd.read_csv('retake/data/day4/churn_train.csv')   # 1000행, 정답 churn 있음
test  = pd.read_csv('retake/data/day4/churn_test.csv')    # 300행, 정답 없음
```

| 컬럼 | 뜻 |
|---|---|
| `customer_id` | 고객 번호 (**모델에 넣지 않는다**) |
| `age` | 나이 (결측 있음) |
| `gender` | 성별 M/F |
| `region` | 지역 |
| `contract` | 약정 (월단위 / 1년 / 2년) |
| `tenure` | 가입 개월 수 |
| `monthly_fee` | 월 요금 |
| `total_spend` | 누적 결제액 (결측 있음) |
| `support_calls` | 고객센터 문의 횟수 |
| `payment` | 결제 수단 (결측 있음) |
| **`churn`** | **이탈 여부 (1 = 이탈) — train에만 있음** |

> `retake/data/day4/_answer_do_not_open.csv`는 채점용 test 정답이다. **열지 말 것.**
> 풀이는 `workspace/day4.py`. 위의 5단계 템플릿을 **보지 않고** 먼저 쳐 보고, 막히면 본다.

---

### Q1. (확인) train과 test의 행·열 수, train에서 결측치가 있는 컬럼과 그 개수, train의 이탈 비율(소수 셋째 자리)을 출력하라.

### Q2. (전처리) 다음 순서로 전처리하고, 완성된 `X`와 `X_test`의 shape을 출력하라.
1. `y` = train의 `churn` / `X` = train에서 `customer_id`, `churn` 제외 / `X_test` = test에서 `customer_id` 제외
2. `age`, `total_spend`의 결측치 → **train(X)의 중앙값**으로 X와 X_test 모두 채우기
3. `payment`의 결측치 → `'없음'`
4. `gender`, `region`, `contract`, `payment`를 **X와 X_test를 합쳐서** `get_dummies` → 다시 나누기

### Q3. (모델) `train_test_split(test_size=0.2, random_state=42, stratify=y)`로 나누고, `RandomForestClassifier(n_estimators=100, random_state=42)`로 학습하라. 검증 데이터의 **ROC-AUC**를 소수 넷째 자리까지 출력하라.

### Q4. (평가) 같은 모델로 검증 데이터의 **F1(macro)** 와 **accuracy**를 각각 소수 넷째 자리까지 출력하라.

### Q5. (제출) 모델을 **train 전체(X, y)로 다시 학습**한 뒤, test 고객의 **이탈 확률**을 예측해 `pred` 컬럼 하나짜리 `result.csv`로 저장하라 (`index=False`). 저장한 파일을 다시 불러와 shape과 앞 5행을 출력하라.

> 채점: Q1~Q4는 값 비교, Q5는 **숨겨진 test 정답으로 ROC-AUC**를 계산한다. **0.80 이상이면 통과** (기본 템플릿 그대로면 넘는다).
> `result.csv`는 프로젝트 폴더에 생긴다 (git에는 올라가지 않게 해 두었다).

---

## 📌 진행 메모 — ✅ Day 4 완료 (2026-11-22~24)

| 단계 | 상태 | 메모 |
|---|---|---|
| 1 탐색 (Q1) | ✅ | (1000, 11) / (300, 10), 결측 age 41·total_spend 30·payment 19, 이탈 0.434 |
| 2 전처리 ① 나누기 + 결측 (Q2 앞) | ✅ (고친 뒤) | 처음엔 △ — 아래 "2-2 결측에서 고친 것" |
| 3 인코딩 (Q2 뒤) | ✅ | X (1000, 19) / X_test (300, 19), 컬럼 이름·순서 같음, object 0개 |
| 4 모델링 (Q3, Q4) | ✅ (고친 뒤) | 4-1 stratify 누락, 4-2 predict→fit, 4-4 round 누락 → 모두 고침 |
| 5 제출 (Q5) | ✅ | test ROC-AUC **0.8513** (기준 0.80 통과) |

### 2-2 결측에서 고친 것

```python
# ❌ 처음 — 에러 없이 test 300명 중 290명의 나이가 train 나이로 바뀜
X_test['age'] = X['age'].fillna(m)
# ✅
X_test['age'] = X_test['age'].fillna(m)      # 왼쪽·오른쪽 표 이름이 같아야 한다
```

| 행 | test 원래 age | 잘못된 코드 후 | train age |
|---|---|---|---|
| 0 | 60 | **23** | 23 |
| 1 | 56 | **58** | 58 |

> 출력(`0 0`, shape)만으로는 절대 못 잡는다. **채우는 줄은 `X ← X`, `X_test ← X_test`** 인지 눈으로 확인
> 또 하나: 문제는 **중앙값**인데 `mean()` → `median()`으로 고침 (문제가 정한 방법 그대로)

### 4단계 시작할 때 볼 것

```python
# 4-1. 분할 — X 두 개 → y 두 개
X_tr, X_val, y_tr, y_val = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# 4-2 학습 / 4-3 예측 / 4-4 점수 — 정답이 앞, 예측이 뒤
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_tr, y_tr)
pred  = model.predict(X_val)                  # 0/1  → F1, accuracy
proba = model.predict_proba(X_val)[:, 1]      # 확률 → ROC-AUC
```

---

### 개념 공부 중 나온 질문 (실행으로 확인)

| 질문 | 답 |
|---|---|
| 1유형은 부분 점수가 있나? | **없다.** 10점 × 3문제, 값만 채점 → 0/10/20/30만 가능. 형식 실수 = 10점 손실 |
| 3유형은 소문항 하나 맞히면 5점? | 대체로 15점을 2~3개로 나눔. **배점은 회차마다 다름** (시험지에 표시). 목표 10점 = 쉬운 소문항 2개쯤 |
| 지난번 2유형 5점은 어디서? | 공개 안 됨. 형식은 맞았고(35점) **성능 구간**에서 깎였을 가능성 큼 — 대표 원인: ROC-AUC에 0/1 제출 |
| 모델을 바꿔야 하나? | 거의 아니다. 모델 4개 차이 0.04 vs **0/1 제출 실수 0.10** → RandomForest 하나 + 실수 없는 템플릿 |
| 이 흐름을 부르는 용어? | **탐색(EDA) → 전처리 → 모델링 → 평가·제출**. 전처리 = 결측치 처리 · 인코딩 · (스케일링) · (파생변수) |
| 왜 X, y, X_test를 먼저 나누나? | 파일이 2개(train/test)라서. 먼저 나누면 X와 X_test 컬럼이 같아져 같은 코드로 처리 가능. 안 나누고 합치면 churn 300개 NaN, id까지 인코딩하면 컬럼 1309개 |
| 왜 train 값으로 test를 채우나? | test = 모르는 미래 데이터. 공부할 때 정한 규칙(나이 모르면 44세)을 실전에도 그대로. test 정보를 미리 쓰면 **데이터 누수** |
| `get_dummies`는? | 글자 컬럼 → 값 종류만큼 True/False 컬럼 (**원핫 인코딩**). `pd.get_dummies(표, columns=[...])`, 결과 재할당 |
| 원핫 함수 = get_dummies? | pandas는 `get_dummies`. sklearn `OneHotEncoder`도 같은 일. `LabelEncoder`는 0,1,2로 바꾸는 **다른 방식** → **get_dummies로 통일** |
| `test_size`·`random_state`·`stratify` 기준? | 문제가 정하면 그대로. 없으면 0.2 / 42(아무 숫자, 고정이 핵심) / **분류만** `stratify=y` |
| `n_estimators`·`random_state`? | 나무 수 100(기본값, 10은 낮고 300↑은 시간만 늘어남) / 무작위 고정. `max_depth`는 선택 |

---

## 채점 결과 — 5 / 5 ✅ (test ROC-AUC 0.8513 통과) (2026-11-24)

| # | 내 출력 | 정답 | 결과 | 과정에서 고친 것 |
|---|---|---|---|---|
| Q1 | (1000, 11) (300, 10) / age 41·total_spend 30·payment 19 / 0.434 | 같음 | ✅ | |
| Q2 | X (1000, 19) / X_test (300, 19) | 같음 | ✅ | 2-2 표 섞임 (`X_test['age'] = X['age']…`), mean→median |
| Q3 | 0.8261 | 0.8261 | ✅ | 4-1 `stratify=y` 누락 (그대로면 0.8471), 4-2 `model.predict(X_train, y_train)` → `fit` |
| Q4 | 0.7453 / 0.755 | 같음 | ✅ | 4-4 `round(…, 4)` 누락 |
| Q5 | `result.csv` (300, 1), 0~0.99 확률 | test ROC-AUC ≥ 0.80 | ✅ **0.8513** | |

### 최종 풀이 (4-1 ~ 5-3)

```python
# 4-1 분할
X_train, X_value, y_train, y_value = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
# 4-2 학습
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
# 4-3 예측
pred = model.predict(X_value)
proba = model.predict_proba(X_value)[:, 1]
# 4-4 점수
print(round(roc_auc_score(y_value, proba), 4))                 # 0.8261
print(round(f1_score(y_value, pred, average='macro'), 4))      # 0.7453
print(round(accuracy_score(y_value, pred), 4))                 # 0.755
# 5-1 다시 학습
model.fit(X, y)
# 5-2 저장
proba = model.predict_proba(X_test)[:, 1]
pd.DataFrame({'pred': proba}).to_csv('result.csv', index=False)
# 5-3 확인
result = pd.read_csv('result.csv')
print(result.shape)      # (300, 1)
print(result.head())
```

> `pred = model.predict(X_test)` 줄은 제출에 안 쓰여서 지워도 된다 — 남겨 두면 `pred`를 잘못 저장할 위험

### 4단계 공부 중 나온 질문 (실행으로 확인)

| 질문 | 답 |
|---|---|
| `stratify`가 뭐야? | **층화** — 정답 그룹(유지 566 / 이탈 434)마다 20%씩 따로 뽑아 비율 유지. 없으면 검증 이탈 77명(38.5%), 있으면 87명(43.5%) |
| 회귀에선 왜 안 써? | 정답이 연속 숫자라 그룹이 없음 (월요금 455종, 191종은 1명뿐) → `ValueError: least populated class has only 1 member` |
| `n_estimators`? | 나무 수. 100이 기본값 (10은 낮고 300↑은 시간만) |
| predict·predict_proba 둘 다 `X_value`? | 그렇다. 채점 정답이 `y_value`면 예측도 `X_value` (이름 짝). 제출은 `X_test` |
| `average='macro'` 꼭? | 문제가 정하면 그대로. 빼면 binary(0.6957 ≠ 0.7453), 다중분류는 에러. **"F1이면 macro"** |
| 평가를 꼭 해야 해? | 채점엔 불필요(`result.csv`만 채점). 그래도 **망가졌는지 확인하는 계기판** — 0.5 근처·1.0 근처면 의심 |
| 0.75~0.9를 만들어야 해? | 아니다. 점수는 데이터가 정함. "0.5보다 확실히 높고 1.0은 아님"이면 정상 |
| 점수 함수 인자 순서? | **정답 먼저**. macro F1·accuracy는 뒤집어도 같지만 weighted F1은 달라지고 ROC-AUC는 에러 |
| `fit(X, y)` 다시 학습? | 4-1~4-4는 **모의시험**. 확인 끝났으니 숨긴 200명까지 1000명 전부로 다시 공부 (fit은 처음부터 새로). test 0.848 → 0.851 |
| 왜 test가 300명? | 출제자가 나눈 파일 크기 (1300 → 1000 / 300). 검증 200명은 내가 `test_size`로 뗀 것. **제출 행 수 = test 행 수** |
