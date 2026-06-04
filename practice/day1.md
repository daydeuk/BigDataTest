# 1일차 연습문제 — Python 최소 문법

## Q1. f-string으로 출력하세요.

### 내 풀이 ✅
```python
name = "홍길동"
age = 28
print(f"{name}의 나이는 {age}세입니다")
```

---

## Q2. 리스트에서 마지막 값과 길이를 출력하세요.

### 내 풀이 ✅
```python
cols = ['age', 'income', 'score', 'gender']
print(cols[-1])
print(len(cols))
```

---

## Q3. 70점 이상 90점 미만인 값만 출력하세요.

### 내 풀이 ✅
```python
scores = [55, 72, 88, 91, 69, 100, 85]
for score in scores:
    if 90 > score and score >= 70:
        print(score)
```

> Python은 `&&` 대신 `and` 사용. 연결 비교(`70 <= score < 90`)도 가능.

---

## Q4. 평균을 반환하는 함수를 완성하세요.

### 내 풀이 ✅
```python
def get_mean(numbers):
    total = 0
    for number in numbers:
        total += number
    return total / len(numbers)

print(get_mean([10, 20, 30, 40]))  # 25.0
```

> - `sum` 은 Python 내장함수와 이름 충돌 → `total` 사용 권장
> - 세미콜론(`;`) 은 Python에서 불필요

---

## Q5. 인덱스 번호와 컬럼명을 출력하세요.

### 내 풀이 ✅
```python
cols = ['age', 'income', 'score']

# case1 — 카운터 변수 사용
num = 0
for col in cols:
    print(f"{num}번: {col}")
    num += 1

# case2 — enumerate 사용 (더 간결)
for i, col in enumerate(cols):
    print(f"{i}번: {col}")
```

> `enumerate` 는 인덱스 + 값을 동시에 꺼내줘서 카운터 변수 불필요
