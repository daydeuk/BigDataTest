# Day 4 시작 전 10분 복습 — Day 3 오답 · 어려웠던 것

> 셀프 퀴즈는 **`workspace/review_day3.py`에 직접 쳐서** 풀고 "복습 채점해줘".

---

## 1. 내가 틀린 것

| # | 실수 | 기억할 한 줄 |
|---|---|---|
| 1 | True/False 결과를 `.count()`로 셈 → 40 (Q3) — isin `len(조건)`과 **같은 실수** ⚠️ | True/False 세기 → **`.sum()`** 또는 `len(df[조건])` |

| 코드 | 결과 |
|---|---|
| `조건.sum()` | True 개수 ✅ |
| `len(df[조건])` | 걸러진 행 수 ✅ |
| `조건.count()` / `len(조건)` | 전체 칸 수 ❌ |

---

## 2. ⭐ 내가 `**` 표시한 것

### ⭐⭐⭐ True/False: `.sum()` = 개수, `.mean()` = 비율 (복습 R5에서 "진짜 중요")

```python
df['is_weekend'] = df['order_dt'].dt.dayofweek >= 5
df.groupby('city')['is_weekend'].mean()    # 도시별 주말 비율
```
> 자세한 설명·함정·연습문제 → [⭐ 핵심 반복 복습](핵심_반복복습.md)

### ① 대소문자 무시는 `.lower()` 먼저 — 국룰 맞다

```python
df['email'].str.lower().str.contains('gmail')
df['email'].str.lower().str.endswith('@gmail.com')
```
> contains·startswith·endswith **모두 대소문자 구분**. `case=False`는 contains에만 있어서 → `lower()` 하나로 통일

### ② ⭐⭐ split 조각은 `.str[N]` — `[N]`은 에러 없이 틀린다

```
                  ↓ .str[1] = 각 칸의 2번째 (두 번째 "열"을 통으로)
행 0 → [010, 1234, 5678]
행 1 → [010, 9876, 5432]   ← [1] = 1번 행 통째 ❌
```
> **컬럼에서는 쪼갤 때도 `.str`, 꺼낼 때도 `.str`**

---

## 3. 헷갈렸던 개념 한 장

| 개념 | 한 줄 |
|---|---|
| `.dt` 괄호 | 속성(`month`, `hour`, `dayofweek`)은 괄호 없음. **`day_name()`만 괄호** |
| 요일 번호 | 월=0 … 일=6, 주말 `>= 5` |
| `pd.cut` 경계 | 기본 `(a, b]` 오른쪽 포함 = "이하". "미만"이면 `right=False` (`left=` 없음) |
| `pd.cut` 끝 | 0이나 음수가 있으면 `-np.inf`. 다 쓰고 `isnull().sum()`으로 NaN 확인 |
| `pd.cut` 이름 | `bins`, `labels` 복수형. 라벨 수 = 경계 수 − 1 |
| IQR | Q3 − Q1. 이상치 = Q1 − 1.5×IQR 미만 / Q3 + 1.5×IQR 초과 |
| quantile·std | 숫자 컬럼만. 표 전체엔 `numeric_only=True` |
| 그룹별 비율 | 조건을 컬럼으로 → `groupby('g')['is_x'].mean()` |

---

## 4. 셀프 퀴즈 (5문제) — `workspace/review_day3.py`

데이터: `retake/data/day3_delivery.csv`

| # | 문제 |
|---|---|
| R1 | naver 계정(대소문자 구분 없이) 주문은 몇 건인가? |
| R2 | 일요일 주문의 `amount` 평균 (소수 둘째) |
| R3 | `deliver_min`이 **30분 미만**이면 '정시', **30분 이상**이면 '지연' (`pd.cut` 사용, `right` 주의). '지연' 건수 |
| R4 | `amount`의 IQR 방식 이상치 개수 (Q1 − 1.5×IQR 미만 또는 Q3 + 1.5×IQR 초과). 0개여도 정답이다 |
| R5 | 시/도별 **주말 주문 비율**이 가장 높은 시/도 이름과 비율 (소수 셋째) |

<details>
<summary>정답 보기 (py로 다 풀고 열기)</summary>

| # | 정답 | 모범답안 |
|---|---|---|
| R1 | 17 | `df['email'].str.lower().str.contains('naver').sum()` |
| R2 | 27800.0 | (날짜 변환 먼저) `round(df[df['order_dt'].dt.dayofweek == 6]['amount'].mean(), 2)` |
| R3 | 31 | `pd.cut(df['deliver_min'], bins=[0, 30, np.inf], labels=['정시', '지연'], right=False)` → `value_counts()['지연']` — `right=False` 빼면 29 (30분 2건이 '정시'로 감) |
| R4 | 0 | `q1, q3` → `iqr` → `len(df[(df['amount'] < q1 - 1.5*iqr) \| (df['amount'] > q3 + 1.5*iqr)])` |
| R5 | 인천, 0.667 | `df['is_weekend'] = df['order_dt'].dt.dayofweek >= 5` → `df['city'] = ...str.split().str[0]` → `groupby('city')['is_weekend'].mean()` |

</details>

### 셀프 퀴즈 채점 — 3 / 5 + △ 2 (2026-11-22)

| # | 내 출력 | 정답 | 결과 | 메모 |
|---|---|---|---|---|
| R1 | 17 | 17 | ✅ | `lower()` → `endswith('@naver.com')` → `.sum()` — Day 3 Q3 실수 고쳐짐 👍 |
| R2 | `6    27800.0` (Series) | 27800.0 | △ | 값은 맞음. 이미 일요일만 걸렀으니 groupby 필요 없음 → `round(r2['amount'].mean(), 2)` |
| R3 | (출력 없음) | 31 | △ | `pd.cut(..., right=False)` 정확. **마지막에 건수를 안 셈** → `df['grade'].value_counts()['지연']` |
| R4 | 0 | 0 | ✅ | |
| R5 | 인천 0.667 | 인천 0.667 | ✅ | 분자 ÷ 분모 방식. 아래 함정 확인 |

**R5 — 내 방식(분자 ÷ 분모)은 맞다. 단, "0건 그룹"에서 차이가 난다**

```python
# 내 풀이 ✅
r5_2 = df.groupby('city')['dayofweek'].count()                        # 분모: 도시별 전체 주문
r5_1 = df[df['dayofweek'] >= 5].groupby('city')['dayofweek'].count()  # 분자: 도시별 주말 주문
r = r5_1 / r5_2                                                        # 이름표(도시)끼리 맞춰서 나눔

# 다른 방법 — True/False 컬럼의 평균 = 비율
df['is_weekend'] = df['dayofweek'] >= 5
df.groupby('city')['is_weekend'].mean()
```

| 도시 | 분자 | 분모 | 비율 |
|---|---|---|---|
| 경기 | 2 | 7 | 0.286 |
| 부산 | 3 | 9 | 0.333 |
| 서울 | 7 | 18 | 0.389 |
| 인천 | 4 | 6 | **0.667** |

가상 실험 — **인천의 주말 주문이 0건**이었다면:

| 방법 | 인천 | 가장 **낮은** 도시 (`idxmin`) |
|---|---|---|
| 분자 ÷ 분모 | **NaN** (주말 0건이라 분자에 인천이 아예 없음) | 경기 ❌ |
| `is_weekend` 평균 | **0.0** | 인천 ✅ |

> 필터 후 groupby하면 **0건인 그룹은 결과에서 사라진다.** 그래서 나누면 NaN.
> "가장 높은" 문제에선 영향이 없지만, "가장 낮은" 문제에선 답이 틀린다.
> **그룹별 비율은 True/False 컬럼 → `groupby().mean()`이 더 안전하다.**

---

다 봤으면 → Day 4 (2유형 분류)로.
