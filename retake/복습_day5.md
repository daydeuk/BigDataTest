# Day 6 시작 전 복습 — Day 5 (2유형 회귀 + 라벨 인코딩) 오답 · 핵심

> 복습 과제는 **`workspace/review_day5.py`에 템플릿을 보지 않고 처음부터** 친다. 목표 15분. 다 치면 "복습 채점해줘".

---

## 1. 내가 틀린 것 (모두 고쳐서 5/5)

| # | 실수 | 기억할 한 줄 |
|---|---|---|
| Q4 | 라벨 버전 RMSE에 원핫의 `pred`를 넣음 → 두 버전 점수가 똑같이 나옴 | 결과가 이상하면 **그 줄의 변수 이름**부터. 버전 꼬리표(`_lb`)는 **모든 줄에** |
| Q2 | `pd.get_dummies(all_x, cols)` — `columns=` 빠짐 → 두 번째 자리는 **prefix** (이번엔 운) | **`pd.get_dummies(all_x, columns=cols)`** — 옵션은 항상 `이름=값` |
| Q1 | "서로 다른 값의 개수"를 `value_counts()` 표로 | **`nunique()`** = 종류 수 한 숫자 |
| 구현 | `RandomForestRegressor()` — `random_state` 빠짐 → 실행마다 RMSE가 다름 | **분할에도 모델에도 `random_state=42`** |

---

## 2. ⭐ 분류 vs 회귀 — 다른 곳은 4군데

| 조각 | 분류 | 회귀 |
|---|---|---|
| 1-2 판단 | 정답 `nunique()`가 몇 개 | 정답 `nunique()`가 **수백 개** |
| 4-1 분할 | `stratify=y` | **빼기** (넣으면 에러) |
| 4-2 모델 | `RandomForestClassifier` | **`RandomForestRegressor`** |
| 4-3 예측 | `predict` / `predict_proba()[:, 1]` | **`predict`만** |
| 4-4 점수 | AUC·F1·accuracy (높을수록) | **`np.sqrt(mean_squared_error(y, pred))`** · MAE (낮을수록) · R² |
| 5-2 제출 | 지표 따라 확률 또는 0/1 | `predict` 그대로 |

> `mean_squared_error(..., squared=False)` → 최신 sklearn **에러**. `np.sqrt(...)`로
> RMSE가 좋은지 판단: **평균만 찍었을 때(≈ 정답의 표준편차)** 보다 확실히 작으면 정상

---

## 3. ⭐ 인코딩 — 원핫 vs 라벨

```python
all_x = pd.concat([X, X_test])                     # 합치기 (같음)

all_x = pd.get_dummies(all_x, columns=cols)        # A. 원핫 — 한 줄 (기본)
# 또는
for c in cols:                                     # B. 라벨 — 컬럼마다
    le = LabelEncoder()                            #    새 le (for문 안!)
    all_x[c] = le.fit_transform(all_x[c])          #    합친 표의 컬럼 하나씩

X = all_x.iloc[:len(X)]                            # 다시 나누기 (같음)
X_test = all_x.iloc[len(X):]
```

| 라벨 인코딩 함정 | 에러 | 합쳐서 하면 |
|---|---|---|
| train에서만 fit → test에 처음 보는 값 | `unseen labels: 'BMW'` | ✅ 해결 |
| `le` 하나로 여러 컬럼 돌려쓰기 | 사전 덮어씀 → `unseen labels` | ✅ for문 안에서 새 `le` |
| 표 전체에 `fit_transform(X)` | `y should be a 1d array` | ✅ 컬럼 하나씩 |

> 점수 차이 거의 없음 (RMSE 342.81 vs 343.82). **기본은 원핫**, 문제가 "라벨 인코딩"이라 할 때만 라벨

---

## 4. 헷갈렸던 이름 정리

| 이름 | 정체 |
|---|---|
| `X` | train 전체의 문제 (2-2 결측은 **여기서** 값을 구함) |
| `X_train` | 그중 80% — **학습용** |
| `X_value` | 그중 20% — **val**idation(검증)용. 학습에 안 씀 |
| `X_test` | test 파일 — 제출용 |
| `nunique()` / `value_counts()` / `unique()` | 종류 수 한 숫자 / 값별 개수 표 / 종류 목록 |

---

## 5. 복습 과제 — `workspace/review_day5.py`

**같은 중고차 데이터, 인코딩과 지표만 바꾼 버전**이다.

> **문제**: `car_train.csv`로 학습해 `car_test.csv` 차량의 가격을 예측하라.
> 평가지표는 **MAE**이다. 범주형 컬럼은 **LabelEncoder**로 인코딩하라.
> 전처리는 Day 5 Q2와 같다 (mileage·engine_cc train 중앙값, fuel '없음').
> 검증 MAE(소수 둘째)를 출력하고, 예측 가격을 `pred` 컬럼 하나짜리 `result.csv`로 제출하라.

체크 포인트:
1. 회귀 → `stratify` 없음, `Regressor`, `predict`
2. 라벨 인코딩 → **합쳐서, for문 안에서 새 `le`**
3. MAE → `mean_absolute_error(정답, 예측)`
4. `result.csv`는 (200, 1)

<details>
<summary>기준 (다 풀고 열기)</summary>

| 항목 | 기준 |
|---|---|
| 검증 MAE | 261.65 (`test_size=0.2, random_state=42`, 모델 `n_estimators=100, random_state=42`) |
| 제출 파일 | (200, 1) |
| test MAE | **350 이하 통과** (기본 템플릿 280.83, 평균만 찍으면 1080.02) |

</details>

---

다 했으면 → Day 6 (3유형)으로.
