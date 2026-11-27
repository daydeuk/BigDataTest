# Day 6 복습 — 3유형 (처음 보는 데이터로 혼자 풀고 혼자 채점)

> 시험 전날(11/27). 어제 Day 6을 **처음 보는 데이터**로 다시 한다.
> 목표 **35분**. 노트를 보지 말고 먼저 쳐 보고, 막히면 아래 **"🆘 막히면 열기"** 를 한 칸만.
> 답은 `workspace/review_day6.py` **맨 아래 `answer = {...}`** 에 적고, 채점기로 혼자 채점한다.

---

## 🔑 시작 전 30초 — 이것만 떠올리고 시작

```python
from scipy import stats                    # 검정
import statsmodels.formula.api as smf      # 회귀
# p < 0.05 → 귀무가설 기각 (= 유의하다)
# model.params / model.pvalues / model.rsquared / model.predict(DataFrame)
# 오즈비 = np.exp(계수)   /   이름 전부 = .index.tolist()
```

---

## 📄 데이터

```python
df = pd.read_csv('retake/data/day6_review/diet.csv')
```

다이어트 프로그램 참가자 100명.

| 컬럼 | 뜻 |
|---|---|
| `member_id` | 참가자 번호 |
| `program` | 프로그램 (A / B) |
| `sex` | 성별 (M / F) |
| `age` | 나이 |
| `exercise_hours` | 주간 운동 시간 |
| `calories` | 하루 섭취 칼로리 |
| `weight_before` | 프로그램 전 체중 |
| `weight_after` | 프로그램 후 체중 |
| `success` | 목표 달성 여부 (1 = 달성, 0 = 실패) |

> ⚠️ `retake/data/day6_review/_answer_do_not_open.json`은 채점기가 쓰는 정답. **열지 말 것.**

---

## 문제 1 — 검정 (유의수준 0.05)

| 소문항 | 문제 | 답 형식 |
|---|---|---|
| **1-1** | 같은 참가자의 프로그램 **전후 체중**이 다른지 검정하라 (`weight_before`, `weight_after` 순서). **검정통계량** | 소수 셋째 |
| **1-2** | 1-1의 결과로 귀무가설을 기각하는가? | `'기각'` 또는 `'채택'` |
| **1-3** | 감량(`weight_before − weight_after`)을 새 컬럼으로 만들고, 프로그램 A와 B의 감량 평균이 다른지 검정하라. **등분산을 가정하지 않는다.** **p-value** | 소수 셋째 |
| **1-4** | `sex`와 `success`가 관련 있는지 **카이제곱 독립성 검정**을 하라. **검정통계량** | 소수 셋째 |
| **1-5** | 참가자 나이(`age`)의 평균이 **40세**와 다른지 검정하라. **p-value** | 소수 셋째 |

## 문제 2 — 회귀

| 소문항 | 문제 | 답 형식 |
|---|---|---|
| **2-1** | `weight_after`를 `weight_before`, `exercise_hours`, `calories`, `age`로 예측하는 **선형회귀**를 적합하라. `exercise_hours`의 **회귀계수** | 소수 넷째 |
| **2-2** | 2-1 모델에서 유의수준 0.05에서 **유의하지 않은 변수의 개수** (절편 제외) | 정수 |
| **2-3** | 2-1 모델에서 **유의한 변수의 이름을 전부** (절편 제외) | 목록 `[...]` |
| **2-4** | 2-1 모델의 **R²** | 소수 셋째 |
| **2-5** | `weight_before=80, exercise_hours=5, calories=2000, age=40`인 참가자의 **예측 체중** | 소수 둘째 |
| **2-6** | `success`를 `exercise_hours`, `calories`로 예측하는 **로지스틱 회귀**를 적합하라. `exercise_hours`의 **오즈비** | 소수 셋째 |

---

## ✅ 답 적기 & 채점

`workspace/review_day6.py` 맨 아래 `answer`에 **코드로 구한 값**을 넣는다 (손으로 적지 말고 변수로).

```python
answer = {
    '1-1': round(stat1, 3),
    '1-2': '기각',
    ...
}
```

```bash
.venv/bin/python workspace/grade_day6.py
```

> 채점기는 소문항마다 ✅/❌와 힌트(자릿수, tolist, 기각 방향)를 알려 준다. **9개 이상이면 준비 완료.**

---

## 🆘 막히면 열기 (한 칸씩만)

<details>
<summary>1-1, 1-2 — 같은 사람 전후</summary>

"같은 참가자의 전후" → **대응** → `ttest_rel`
```python
stat1, p1 = stats.ttest_rel(df['weight_before'], df['weight_after'])
```
p가 0.05보다 작으면 `'기각'`
</details>

<details>
<summary>1-3 — 새 컬럼 + 두 그룹 + 등분산 X</summary>

```python
df['loss'] = df['weight_before'] - df['weight_after']     # Day 2·3 파생 컬럼
a = df[df['program'] == 'A']['loss']
b = df[df['program'] == 'B']['loss']
stat3, p3 = stats.ttest_ind(a, b, equal_var=False)        # 등분산 가정 X → equal_var=False
```
</details>

<details>
<summary>1-4 — 카이제곱</summary>

```python
ct = pd.crosstab(df['sex'], df['success'])
chi2, p4, dof, expected = stats.chi2_contingency(ct)      # 결과 4개
```
</details>

<details>
<summary>1-5 — 기준값과 비교</summary>

"평균이 40과 다른가" → **일표본** → `stats.ttest_1samp(df['age'], 40)`
</details>

<details>
<summary>2-1 ~ 2-5 — 선형회귀</summary>

```python
model = smf.ols('weight_after ~ weight_before + exercise_hours + calories + age', data=df).fit()
model.params['exercise_hours']                    # 2-1
pv = model.pvalues.drop('Intercept')              # 절편 빼기
(pv >= 0.05).sum()                                # 2-2
pv[pv < 0.05].index.tolist()                      # 2-3 ⭐ 전부
model.rsquared                                    # 2-4
new = pd.DataFrame({'weight_before': [80], 'exercise_hours': [5], 'calories': [2000], 'age': [40]})
model.predict(new)[0]                             # 2-5
```
⚠️ `pv`를 `df`라고 이름 짓지 않기 (원래 데이터가 사라짐)
</details>

<details>
<summary>2-6 — 로지스틱 + 오즈비</summary>

```python
model2 = smf.logit('success ~ exercise_hours + calories', data=df).fit()   # model2 새 이름
np.exp(model2.params['exercise_hours'])
```
</details>

---

## 📝 기록

| 날짜 | 걸린 시간 | 연 힌트 | 점수 |
|---|---|---|---|
| 11/27 | — | 1-1 순서 질문 | **8 / 11 → 재풀이 11 / 11** (출력 기준, `answer` 미입력) |

### 11/27 채점 — 8 / 11

| 소문항 | 내 출력 | 정답 | 결과 | 원인 · 근거 |
|---|---|---|---|---|
| 1-1 | **−17.452** | **17.452** | ❌ | `ttest_rel(after, before)` — 문제는 **before, after 순서**. 대응 검정은 순서를 바꾸면 **부호만** 반대 (p는 같음) |
| 1-2 | 기각 | 기각 | ✅ | p = 5.7e-32 < 0.05 |
| 1-3 | 0.767 | 0.767 | ✅ | 파생 컬럼 + `equal_var=False` 정확 👍 |
| 1-4 | 0.085 | 0.085 | ✅ | 검정통계량 = `chi2` (질문 답: 맞다) |
| 1-5 | 0.005 | 0.005 | ✅ | |
| 2-1 | −0.4211 | −0.4211 | ✅ | `.fit()`을 한 줄에 붙여 해결 👍 |
| 2-2 | 1 | 1 | ✅ (운) | 절편 안 뺌 — 절편 p = 0.0176이라 안 세어졌을 뿐. `>`가 아니라 `>=` |
| 2-3 | `Index(['Intercept', 'weight_before', 'exercise_hours', 'calories'])` | `['weight_before', 'exercise_hours', 'calories']` | ❌ | ① **절편 포함** (`drop('Intercept')` 안 함) ② Index 객체 그대로 → **`.tolist()`** |
| 2-4 | 0.967 | 0.967 | ✅ | |
| 2-5 | `0    75.898` | **75.9** | ❌ | **자릿수**: 문제는 **소수 둘째** → `round(…, 2)`. (`[0]`은 시험 채점과 무관 — 화면 `0  75.9`를 보고 75.9를 적으면 정답. 연습 채점기·깔끔한 출력용으로만 `pred[0]`) |
| 2-6 | 1.375 | 1.375 | ✅ | 오즈비 = `np.exp(계수)` 👍 (단, 선형 `model`을 덮어씀 → `model2`) |

**`**` 질문 답**

| 질문 | 답 |
|---|---|
| Series에서 index 빼오는 법? | `s.index` → Index 객체 / **`s.index.tolist()`** → 목록 `[…]` (답 칸·채점기는 목록) |
| 맨 위의 "1"은 왜 있나? | 2-3 출력이 아니라 **바로 위 2-2의 `print(len(...))` 결과 1**. 출력이 붙어서 보인 것 → `print('2-3', …)`처럼 라벨을 붙이면 헷갈리지 않음 |
| 2-3 맨 앞의 Intercept는? | 절편의 p-value(0.0176)도 0.05보다 작아서 같이 걸러짐 → **`pv = model.pvalues.drop('Intercept')`** 를 먼저 |
| predict 앞의 0은? | Series의 **이름표**(0번 행). 값만 → `pred[0]` 또는 `pred.iloc[0]` (둘 다 75.9) |
| 카이제곱 4개 값? | `chi2` 검정통계량 / `p` / `dof` 자유도 / `expected` 기대빈도 |

### 재채점 — 11 / 11 ✅ (출력 기준)

| 고친 것 | 출력 |
|---|---|
| 1-1 `ttest_rel(weight_before, weight_after)` | **17.452** ✅ |
| 2-2 `pv = model.pvalues.drop('Intercept')` (두 번 drop → KeyError도 해결) | 1 ✅ |
| 2-3 절편 제외 + `.index.tolist()` | `['weight_before', 'exercise_hours', 'calories']` ✅ |
| 2-5 `round(pred, 2)` | 75.9 ✅ |

> 이번에 나온 질문: `ttest_rel` 순서는 정해진 게 없다(문제 순서 그대로) / 절댓값은 문제가 "절댓값"이라 할 때만 (1유형 "차이"는 abs 의심) / 절편 = 출발점(x=0일 때 y), `smf`가 항상 붙임 → "변수"를 셀 땐 뺀다 / Series에서 Intercept는 **행**이라 `drop('Intercept')` (`drop(columns=…)`는 에러 없이 무시됨) / `index[:]`도 틀린 건 아님, `tolist()`가 깔끔

**패턴 점검 (점수 외)**

| 습관 | 지금 | 고치면 |
|---|---|---|
| 결과 변수 이름 | `stat, p`를 1-1·1-3·1-5에서 재사용 → 마지막 값만 남음 | `stat1, p1` / `stat3, p3` / `stat5, p5` |
| 모델 이름 | 2-6에서 `model = smf.logit(...)` → 선형 모델 사라짐 | `model2` |
| answer 칸 | 비어 있음 → 채점기 0점 | 변수로 채우기 (시험장의 "답 칸 옮겨 적기" 연습) |
| import | `stats`, `smf`를 두 번씩 | 맨 위 한 번 (있어도 에러는 아님) |

---

## ➕ ANOVA 연습 (4문제) — `workspace/review_anova.py`

> 3그룹 이상 평균 비교 → `stats.f_oneway(g1, g2, g3, …)`. 그룹은 Day 1 필터로 하나씩.
> 모든 값은 소수 셋째 자리, 판단은 유의수준 0.05.

| # | 데이터 | 문제 | 답 |
|---|---|---|---|
| A1 | Day 2 `retake/data/day2_orders.csv` | 지역(`region`, 5곳)별 `qty` 평균이 다른가? | F 통계량, p-value, 기각/채택 |
| A2 | Day 3 `retake/data/day3_delivery.csv` | `address`의 첫 단어(시/도, 4곳)별 `deliver_min` 평균이 다른가? | F 통계량, p-value, 기각/채택 |
| A3 | Day 5 `retake/data/day5/car_train.csv` | 브랜드(`brand`, 5개)별 `price` 평균이 다른가? | F 통계량, 기각/채택 |
| A4 | Day 5 같은 데이터 | **BMW를 제외한** 4개 브랜드별 `price` 평균이 다른가? | F 통계량, 기각/채택 |

<details>
<summary>막히면 열기</summary>

```python
g1 = df[df['region'] == '경기']['qty']
g2 = df[df['region'] == '광주']['qty']
# … 그룹 수만큼
stat, p = stats.f_oneway(g1, g2, g3, g4, g5)
```
- A2: 먼저 `df['city'] = df['address'].str.split().str[0]` (Day 3)
- A4: BMW만 빼고 4개 그룹으로 `f_oneway`
- (빠른 방법) `groups = [df[df['brand'] == b]['price'] for b in df['brand'].unique()]` → `stats.f_oneway(*groups)` — `*`는 목록을 풀어서 하나씩 넣어 준다
</details>

### ANOVA 채점 (11/27) — A1 ✅ · A2 ✅ · A4 ✅ (A3 미풀이)

| # | 최종 출력 | 정답 | 과정에서 고친 것 |
|---|---|---|---|
| A1 | 0.861 / 0.497 / 채택 | 같음 | 처음엔 판단만 출력 → `print(round(stat, 3), round(p, 3))` 추가 |
| A2 | 0.685 / 0.567 / 채택 | 같음 | `stats.one_way` → **`stats.f_oneway`** (AttributeError), round 추가 |
| A4 | 14.363 / 0.0 / 기각 | 같음 | **if 아래 기각/채택이 거꾸로** (`p < 0.05: '채택'`) → 고침 — Day 6 Q1과 같은 실수 반복 ⚠️ |

> 질문: groupby().mean() 필요? → 아니다. `f_oneway`·`ttest_ind`는 **원래 값 목록**을 받아 안에서 평균·흩어짐을 계산 (평균만 넣으면 검정 불가) / `<` vs `<=` → 기준은 `p < 0.05` 기각, 딱 0.05는 사실상 안 나와 결과 같음
> 습관: `stat, p = …` 다음 줄은 **`print(round(stat, 3), round(p, 3))`** 세트 → 그다음 if문
> `has no attribute '…'` = 그런 이름 없음 → `dir(stats)`로 확인
> 원래 컬럼(`address`)을 덮어쓰지 말고 새 컬럼(`city`)으로
