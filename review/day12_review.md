# Day12 복습 — 회귀 모델 완전

> `practice/day12.md` 개념 + Q1~Q8 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [x] `LinearRegression()` — 파라미터 없음
- [x] `RandomForestRegressor(n_estimators=100, random_state=42)`
- [x] `XGBRegressor(n_estimators=100, random_state=42)`
- [x] `RMSE = np.sqrt(mean_squared_error(y_val, pred))`
- [x] `MAE = mean_absolute_error(y_val, pred)`
- [x] 회귀는 `stratify` 없음 — 연속값이라 클래스 비율 개념 없음
- [x] CSV 제출: `result.to_csv('result.csv', index=False)` — index=False 필수

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| Q2 | `predict()`에 X 대신 y 넣음 | `model.predict(X_test)` |
| Q4 | if/else 조건 반전 — 더 낮은 모델 출력해야 하는데 반대 출력 | `if Q4_L <= Q4_R: print('LinearRegression')` |
| Q6 | 컬럼 지정 없이 `.sum()` → Series로 출력됨 | `from_pred['pred'].head(10).sum()` |
| Q6 | `to_csv`에 `index=False` 처음에 누락 | `pred_df.to_csv('result.csv', index=False)` |
| Q8 | "소수 넷째 자리" 명시됐는데 `round` 누락 | `print(round(rmse, 4))` |

## 잘 한 점

- `mean_squared_error`, `mean_absolute_error` 인수 순서 `(y_true, y_pred)` 정확히 인지
- 회귀에서 `stratify` 제외 자연스럽게 기억
- 세 모델 RMSE 비교 시 초기값 설정 후 순차 비교 방식 스스로 구현
