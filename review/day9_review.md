# Day9 복습 — NumPy + 백분위수 + 복합 필터

> `practice/day9.md` 개념 + Q1~Q8 풀이 후 여기에 오답 기록

## 핵심 체크리스트

- [x] `np.percentile(arr, 90)` vs `df['col'].quantile(0.9)` — 범위 차이 (0~100 vs 0~1)
- [x] `df['col'].std()` 기본값 = ddof=1 (표본표준편차)
- [x] `np.std(arr)` 기본값 = ddof=0 (모표준편차) — 시험에서 혼동 주의
- [x] `.mode()[0]` — `[0]` 안 붙이면 Series 반환
- [x] `transform('median')` — 그룹별 값을 행마다 붙여서 행별 비교 가능
- [x] 복합 필터: 집계 → 임계값 추출 → 필터 → 재집계 패턴

## 오답 기록

| 문제 | 틀린 이유 | 올바른 코드 |
|------|---------|-----------|
| Q1 | `round()` 누락 | `print(round(np.percentile(df['score'], 25), 1))` |
| Q3 | `abs()` 누락 — 차이의 절댓값 | `print(round(abs(mean1 - mean2), 2))` |
| Q7 | `transform` 대신 `groupby().median()` 사용 — 행 수 불일치로 비교 불가 | `df['dept_median'] = df.groupby('dept')['score'].transform('median')` |
| Q8 | `agg` 인자를 문자열로 전달 | `agg(['mean', 'std'])` — 리스트로 전달 |
