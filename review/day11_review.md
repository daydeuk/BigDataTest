# Day11 복습 — 분류 모델 완전

> `practice/day11.md` 개념 + Q1~Q8 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [ ] `RandomForestClassifier(n_estimators=100, random_state=42)` — 기본 패턴
- [ ] `XGBClassifier(n_estimators=100, random_state=42, eval_metric='logloss')`
- [ ] `accuracy_score(y_val, pred)` — predict() 결과 사용
- [ ] `f1_score(y_val, pred, average='macro')` — average 옵션 주의
- [ ] `roc_auc_score(y_val, pred_proba)` — predict_proba()[:, 1] 사용
- [ ] CSV 제출: `result.to_csv('result.csv', index=False)` — index=False 필수

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| | | |
