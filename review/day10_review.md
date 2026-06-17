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
| Q1 | `column=` 오타 (s 빠짐) | `pd.get_dummies(df, columns=[...])` |
| Q1 | DataFrame에 직접 `startswith` 호출 불가 | `[c for c in df.columns if c.startswith('region_')]` |
| Q2 | `head()` 순서 — 컬럼 선택 먼저 | `df['col'].head(10).sum()` |
| Q4 | `mena()` 오타 | `mean()` |
| Q5 | numpy 배열에 컬럼명 접근 불가 | `pd.DataFrame(scaled, columns=[...])` 변환 후 접근 |
| Q7 | `groupby().mode()` 직접 불가 | `transform(lambda x: x.mode()[0])` |
| Q7 | concat 전 Series 이름 미설정 | `region_mode.name = 'region_top_membership'` |
| Q7 | `result.top(5)` → `head()` | `result.head()` |
| Q8 | 불필요한 train_test_split 추가 | split 언급 없으면 전체 df에 바로 적용 |
| Q8 | 변수명 대문자 `Scaler` | 관행상 소문자 `scaler` |
