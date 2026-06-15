# Day10 복습 — Sklearn 전처리 + 데이터 합치기

> `practice/day10.md` 개념 + Q1~Q8 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [ ] `get_dummies(df, columns=['col'])` — 원핫인코딩, 원본 컬럼 자동 제거
- [ ] `LabelEncoder().fit_transform()` → `le.classes_` 로 매핑 확인
- [ ] `train_test_split(..., stratify=y)` — 분류 문제에서 클래스 비율 유지
- [ ] 스케일링: train은 `fit_transform`, test는 `transform`만 (fit 금지)
- [ ] `StandardScaler` vs `MinMaxScaler` — 정규화(평균0 표준편차1) vs 0~1 압축
- [ ] `pd.merge(df1, df2, on='key', how='left')` — left join
- [ ] `pd.concat([df1, df2], axis=0)` — 행 방향 / `axis=1` — 열 방향

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| | | |
