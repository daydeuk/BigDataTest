# 7일차 복습 — 문자열 처리

## 데이터 세팅

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

## Q1. email에서 `@` 기준으로 분리하여 도메인만 추출해 `domain` 컬럼으로 추가하라. 도메인별 인원수를 출력하라.

### 내 풀이 ✅
```python
df['domain'] = df['email'].str.split('@').str[1]
print(df.groupby('domain')['domain'].count())
```

> `str.split('@').str[1]` — `@` 기준 분리 후 두 번째 요소(인덱스 1)가 도메인.

---

## Q2. email이 `gmail`을 포함하는 사람의 score 평균을 소수 둘째 자리까지 출력하라.

### 내 풀이 ✅
```python
print(round(df[df['email'].str.contains('gmail')]['score'].mean(), 2))
```

---

## Q3. phone에서 가운데 4자리 숫자만 추출해 `mid_num` 컬럼으로 추가하라.

### 내 풀이 ✅
```python
df['mid_num'] = df['phone'].str.split('-').str[1]
print(df['mid_num'])
```

> `010-1234-5678` → split('-') → ['010', '1234', '5678'] → str[1] = '1234'

---

## Q4. grade에서 알파벳(A/B/C)만 추출해 `grade_type` 컬럼으로 추가하라. grade_type별 score 평균을 내림차순으로 출력하라.

### 내 풀이 ✅
```python
df['grade_type'] = df['grade'].str.extract(r'([A-Z]+)')
print(df.groupby('grade_type')['score'].mean().sort_values(ascending=False))
```

> `str.extract(r'([A-Z]+)')` — 대문자 알파벳 1개 이상 추출. 괄호 안이 추출 대상.

---

## Q5. region에서 `서울`을 포함하는 행만 필터링하여 score 평균을 소수 둘째 자리까지 출력하라.

### 내 풀이 ✅
```python
print(round(df[df['region'].str.contains('서울')]['score'].mean(), 2))
```

---

## Q6. name의 글자 수가 3자 이상인 사람의 수를 출력하라.

### 내 풀이 ✅
```python
print(df[df['name'].str.len() >= 3]['name'].count())
```

> `str.len()` — 각 문자열 길이를 정수 Series로 반환.

---

## Q7. email을 모두 대문자로 변환한 뒤, `NAVER`를 포함하는 이메일 주소를 출력하라.

### 내 풀이 ✅
```python
df['email'] = df['email'].str.upper()
print(df[df['email'].str.contains('NAVER')]['email'])
```

> 시험 환경은 코드 에디터 — 마지막 줄 자동 출력 없음. `print()` 필수.
