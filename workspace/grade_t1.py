# 1유형 최종 복습 — 혼자 채점하는 스크립트 (고치지 말고 실행만)
# 실행: .venv/bin/python workspace/grade_t1.py   (프로젝트 폴더에서)
# workspace/final_t1.py 맨 아래 answer = {...} 에 적은 답을 정답과 비교하고,
# 틀렸으면 "자주 하는 실수" 중 어느 것인지 원인까지 알려 준다.
import io
import sys
import json
import runpy
import contextlib

SOLUTION = sys.argv[1] if len(sys.argv) > 1 else 'workspace/final_t1.py'

DATA = json.load(open('retake/data/final_t1/_answer_do_not_open.json', encoding='utf-8'))
KEY, TRAP = DATA['answer'], DATA['trap']
HINT = {  # 함정에 안 걸렸는데 틀렸을 때 보여 줄 기본 힌트
    'A1': 'raw.duplicated().sum() / len(raw.drop_duplicates())',
    'A2': 's = df.isnull().sum() → s[s > 0].index.tolist()',
    'A3': "df['menu'].nunique()",
    'A4': "df['store'].str.contains('서울').sum()",
    'A5': "sort_values('amount', ascending=False).head(5)['price'].mean() → int()",
    'A6': "sort_values(…).iloc[2]['order_id']",
    'A7': "d7 = df.copy() → d7.loc[d7['size'] == 'L', 'price'] = d7.loc[…, 'price'] - 500",
    'A8': "fillna('N') → (d8['coupon'] == 'Y').mean()",
    'B1': "groupby('store')['amount'].sum().sort_values(ascending=False) → index[1] / iloc[1]",
    'B2': "str.lower().str.endswith('@gmail.com').sum()",
    'B3': "pd.to_datetime → .dt.month.value_counts() → index[0] / iloc[0]",
    'B4': ".dt.dayofweek >= 5",
    'B5': "groupby('store')['price'].transform('mean')",
    'B6': "pd.cut(amount, bins=[0, 10000, 30000, np.inf], labels=['소', '중', '대'])",
    'B7': "q1, q3 → iqr → (x < q1 - 1.5*iqr) | (x > q3 + 1.5*iqr)",
    'C1': "fillna(groupby('category')['rating'].transform('mean')) → groupby('store').mean() → idxmax",
    'C2': "is_vip 컬럼 → groupby('city')['is_vip'].mean() → idxmin / min",
    'C3': "2024년 3월 필터 → 정렬 → head(10)['qty'].mean() → int()",
    'C4': "abs(커피 평균 − 디저트 평균) → int()",
    'C5': "groupby('store')['amount'].std() → idxmax / max",
}


def same(mine, right):
    if isinstance(right, list):
        return isinstance(mine, (list, tuple)) and sorted(map(str, mine)) == sorted(right)
    if isinstance(right, str):
        return str(mine).strip() == right
    try:
        return abs(float(mine) - float(right)) < 1e-9
    except (TypeError, ValueError):
        return False


ORD = ['', '첫째', '둘째', '셋째', '넷째']


def round_reason(mine, right):
    """함정 목록에 없을 때: 반올림을 안 했거나 자릿수를 다르게 했는지 진단."""
    if isinstance(right, (list, str)) or isinstance(mine, (list, tuple, str)):
        return None
    try:
        m, r = float(mine), float(right)
    except (TypeError, ValueError):
        return None
    if r.is_integer():
        return None  # 정수 답은 함정 목록(int / round)이 진단
    d = len(repr(r).split('.')[1])  # 정답의 소수 자릿수
    if abs(m - r) < 0.5 * 10 ** -d:
        return f'반올림 안 함 → "소수 {ORD[d]}" = round(x, {d})'
    for k in range(d):
        if abs(m - round(m, k)) < 1e-9 and abs(m - r) <= 0.5 * 10 ** -k + 0.5 * 10 ** -d:
            return f'자릿수 틀림: 소수 {k}자리로 반올림함 → 문제는 "소수 {ORD[d]}" = round(x, {d})'
    return None


with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path(SOLUTION)
ans = g.get('answer', {})

print('=' * 64)
print(' 1유형 최종 복습 — 자동 채점')
print('=' * 64)
score = {'A': [0, 0], 'B': [0, 0], 'C': [0, 0]}
for k, right in KEY.items():
    sec = k[0]
    score[sec][1] += 1
    mine = ans.get(k, None)
    if mine is None:
        print(f' ⬜ {k:<5} (답 없음)')
        continue
    if same(mine, right):
        score[sec][0] += 1
        print(f' ✅ {k:<5} {mine!s}')
        continue
    reason = next((h for v, h in TRAP.get(k, []) if same(mine, v)), None) or round_reason(mine, right)
    print(f' ❌ {k:<5} 내 답: {mine!s:<24} → {reason or "힌트: " + HINT[k.split("-")[0]]}')

print('-' * 64)
total = sum(s[0] for s in score.values())
for sec, name in [('A', '기초 체력'), ('B', '집계·날짜·문자열'), ('C', '실전형 복합')]:
    print(f' Set {sec} {name:<10} {score[sec][0]} / {score[sec][1]}')
print(f' 합계 {total} / {len(KEY)}')
print(' 🎉 1유형 준비 완료!' if total == len(KEY) else ' ❌ 표시된 칸만 retake/1유형_최종복습.md의 힌트를 보고 다시')
