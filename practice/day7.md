# 7일차 — 문자열 처리

## 개념 정리

### 1. `.str` 접근자

```python
df['col'].str.메서드()  # 문자열 Series에는 항상 .str 붙임
```

---

### 2. 대소문자 변환

```python
df['col'].str.lower()   # 전체 소문자
df['col'].str.upper()   # 전체 대문자
df['col'].str.title()   # 첫 글자만 대문자
```

---

### 3. 문자열 길이

```python
df['col'].str.len()     # 각 문자열 길이 (정수 Series 반환)
```

---

### 4. 포함 여부 — `str.contains` ★★★

```python
df[df['col'].str.contains('키워드')]            # 포함된 행 필터
df[df['col'].str.contains('A|B')]              # A 또는 B 포함
df[df['col'].str.contains('키워드', na=False)]  # 결측치 있을 때 NaN→False 처리
```

> 결측치 있는 행은 NaN 반환 → 불리언 필터에 NaN 섞이면 ValueError 발생.
> 습관적으로 `na=False` 붙이는 게 안전.

---

### 5. 문자열 분리 — `str.split`

```python
df['col'].str.split('-').str[0]        # 분리 후 첫 번째 요소
df['col'].str.split('-').str[1]        # 분리 후 두 번째 요소
df['col'].str.split('-', expand=True)  # 분리 결과를 컬럼으로 반환
```

---

### 6. 정규식 추출 — `str.extract`

```python
df['col'].str.extract(r'(\d+)')      # 숫자 추출
df['col'].str.extract(r'([A-Z]+)')   # 대문자 알파벳 추출
```

> 괄호 `()` 안이 추출 대상. 결과는 DataFrame(컬럼 1개).
> 자주 쓰는 패턴: `\d+`(숫자), `\D+`(숫자 아닌 것), `[A-Z]+`(대문자), `[a-z]+`(소문자)

---

### 7. 치환 — `str.replace`

```python
df['col'].str.replace('old', 'new')
df['col'].str.replace(',', '')   # 쉼표 제거
```

---

### 시험 빈출 패턴

```python
# 패턴 1: 특정 문자열 포함 행 필터 후 집계
df[df['email'].str.contains('gmail')]['score'].mean()

# 패턴 2: 구분자 분리 후 새 컬럼 생성
df['domain'] = df['email'].str.split('@').str[1]

# 패턴 3: 문자열 길이 조건 필터
df[df['name'].str.len() >= 3]

# 패턴 4: 정규식으로 알파벳/숫자 추출
df['grade_type'] = df['grade'].str.extract(r'([A-Z]+)')
```

---

## 연습문제

### 데이터 세팅

```python
import pandas as pd

data = {
    'name':     ['김민준', '이서연', '박지호', '최유진', '정승현',
                 '강민서', '윤지원', '장하은', '임도현', '한소율'],
    'email':    ['minjun@gmail.com', 'seoyeon@naver.com', 'jiho@gmail.com',
                 'yujin@kakao.com', 'sh_jung@naver.com', 'minseo@gmail.com',
                 'jiwon@daum.net', 'haeun@kakao.com', 'dohyun@naver.com',
                 'soyul@gmail.com'],
    'phone':    ['010-1234-5678', '010-2345-6789', '010-3456-7890',
                 '010-4567-8901', '010-5678-9012', '010-6789-0123',
                 '010-7890-1234', '010-8901-2345', '010-9012-3456',
                 '010-0123-4567'],
    'grade':    ['A1', 'B2', 'A3', 'C1', 'B1', 'A2', 'C3', 'B3', 'A1', 'C2'],
    'score':    [92, 75, 88, 61, 79, 95, 58, 72, 90, 63],
    'region':   ['서울 강남구', '부산 해운대구', '서울 마포구', '대구 중구', '서울 송파구',
                 '인천 남동구', '부산 사하구', '서울 강북구', '대구 달서구', '인천 계양구']
}
df = pd.DataFrame(data)
```

---

### Q1. email에서 `@` 기준으로 분리하여 도메인만 추출해 `domain` 컬럼으로 추가하라. 도메인별 인원수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['domain'] = df['email'].str.split('@').str[1]
print(df.groupby('domain')['domain'].count())
```

</details>

---

### Q2. email이 `gmail`을 포함하는 사람의 score 평균을 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(round(df[df['email'].str.contains('gmail')]['score'].mean(), 2))
```

</details>

---

### Q3. phone에서 가운데 4자리 숫자만 추출해 `mid_num` 컬럼으로 추가하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['mid_num'] = df['phone'].str.split('-').str[1]
print(df['mid_num'])
```

</details>

---

### Q4. grade에서 알파벳(A/B/C)만 추출해 `grade_type` 컬럼으로 추가하라. grade_type별 score 평균을 내림차순으로 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['grade_type'] = df['grade'].str.extract(r'([A-Z]+)')
print(df.groupby('grade_type')['score'].mean().sort_values(ascending=False))
```

</details>

---

### Q5. region에서 `서울`을 포함하는 행만 필터링하여 score 평균을 소수 둘째 자리까지 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(round(df[df['region'].str.contains('서울')]['score'].mean(), 2))
```

</details>

---

### Q6. name의 글자 수가 3자 이상인 사람의 수를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
print(df[df['name'].str.len() >= 3]['name'].count())
```

</details>

---

### Q7. email을 모두 대문자로 변환한 뒤, `NAVER`를 포함하는 이메일 주소를 출력하라.

<details>
<summary>풀이 보기</summary>

#### 풀이 ✅
```python
df['email'] = df['email'].str.upper()
print(df[df['email'].str.contains('NAVER')]['email'])
```

> 시험 환경은 코드 에디터 — 마지막 줄 자동 출력 없음. `print()` 필수.

</details>
