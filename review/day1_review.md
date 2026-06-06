# 1일차 복습 — Python 최소 문법

## Q1. f-string으로 출력하세요.

`name = "김철수"`, `score = 95` 일 때 `"김철수의 점수는 95점입니다"` 를 f-string으로 출력하세요.

### 내 풀이 ✅
```python
name = "김철수"
score = 95
print(f'{name}의 점수는 {score}점입니다')
```

---

## Q2. 리스트에서 마지막 값과 전체 길이를 출력하세요.

```python
cols = ['gender', 'age', 'dept', 'score', 'name']
```

### 내 풀이 ✅
```python
print(cols[-1])
print(len(cols))
```

---

## Q3. 80점 이상인 값만 출력하세요.

```python
scores = [55, 88, 72, 91, 80, 63, 95]
```

### 내 풀이 ✅
```python
for score in scores:
    if score >= 80:
        print(score)
```

> `>` (초과) vs `>=` (이상) 구분 주의.

---

## Q4. 합계를 반환하는 함수 get_sum을 작성하세요.

### 내 풀이 ✅
```python
def get_sum(numbers):
    total = 0
    for number in numbers:
        total += number
    return total

cols = [10, 20, 30]
total = get_sum(cols)
print(total)
```

> 인덱스를 안 쓸 때는 `enumerate` 불필요. Python은 세미콜론 없어도 됨 (Java 습관 주의).

---

## Q5. enumerate로 순회하며 출력하세요.

```python
cols = ['gender', 'age', 'dept']
```

### 내 풀이 ✅
```python
for i, v in enumerate(cols):
    print(f'{i}번: {v}')
```
