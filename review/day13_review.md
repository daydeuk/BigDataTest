# Day13 복습 — 2유형 풀세트 반복

> `practice/day13.md` Set1~3 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [x] 분류는 `stratify=y` / 회귀는 `stratify` 없음
- [x] 원핫인코딩: `pd.concat([train.drop(target), test])` → `get_dummies` → `iloc`으로 분리
- [x] 라벨인코딩: 컬럼별로 `fit_transform(train)` → `transform(test)` 쌍으로 묶기
- [x] roc_auc는 `predict_proba()[:, 1]` 사용 (predict 아님)
- [x] f1_score 이진 분류: `average='binary'` / 다중 분류: `average='macro'`
- [x] `to_csv('result.csv', index=False)` — index=False 필수
- [x] 회귀 RMSE: `np.sqrt(mean_squared_error(y_val, pred))`
- [x] RMSE/MAE 낮을수록 좋음 / accuracy·f1·roc_auc 높을수록 좋음
- [x] `X_test = test.drop(...)` — train 아닌 test에서 만들기
- [x] `round(값, 4)` — 괄호 안에 같이 넣기

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| Set1 Q1 | `stratify=y`를 `get_dummies`에 넣음 | `train_test_split(..., stratify=y)` |
| Set1 Q1 | `pd.concat()` 리스트 `[...]` 누락 | `pd.concat([train.drop(...), test])` |
| Set1 Q1 | `random_state=42` 누락 | `train_test_split(..., random_state=42)` |
| Set1 Q3 | `f1_score` `average='macro'` 누락 | `f1_score(y_val, pred, average='macro')` |
| Set1 Q4 | `predict_proba()[:, 1]` `[:, 1]` 누락 ⚠️ 반복 | `model.predict_proba(X_val)[:, 1]` |
| Set1 Q4 | `sklearn.metricsw` 오타 | `sklearn.metrics` |
| Set2 Q1-B | LabelEncoder 컬럼 순서 혼동 → '영업' unseen label 에러 | fit_transform→transform 쌍으로 묶기 |
| Set2 Q1-B | `X_test = train.drop(...)` 반복 오타 | `X_test = test.drop(...)` |
| Set3 Q1 | `y_test` → `y_train` 변수명 혼동 | `X_train, X_val, y_train, y_val` |
| Set3 Q2 | `print(round(RMSE), 4)` 괄호 위치 | `print(round(RMSE, 4))` |
| Set3 Q4 | RMSE 비교 결과 무시, LinearRegression 하드코딩 | `if RMSE_Linear <= RMSE_Random:` 분기 |
