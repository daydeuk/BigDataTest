# Day11 복습 — 분류 모델 완전

> 2026-06-18 완료

## 핵심 체크리스트

- [x] `RandomForestClassifier(n_estimators=100, random_state=42)` — 기본 패턴
- [x] `XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')`
- [x] `accuracy_score(y_val, pred)` — predict() 결과 사용
- [x] `f1_score(y_val, pred, average='macro')` — average 옵션 주의
- [x] `roc_auc_score(y_val, pred_proba)` — predict_proba()[:, 1] 사용
- [x] CSV 제출: `result.to_csv('result.csv', index=False)` — index=False 필수

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| Q1 | 인코딩 후 원본 df 사용 | `X = df_enc.drop(columns=['id', 'churn'])` |
| Q3 | f1_score에 average='macro' 누락 | `f1_score(y_test, pred, average='macro')` |
| Q4 | predict_proba에 [:, 1] 누락 | `model.predict_proba(X_test)[:, 1]` |
| Q5 | `x_test` 소문자 오타 | `X_test` 대문자 |
| Q7 | `pd.DataFrame(pred, index=False)` | index=False는 to_csv에서 사용 |
| Q7 | `pd.DataFrame('result.csv')` | `pd.read_csv('result.csv')` |
| Q7 | `columns.tolist` 괄호 누락 | `columns.tolist()` |
| Q8 | round() 누락 | `round(accuracy_score(...), 3)` |
