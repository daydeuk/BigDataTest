# Day 6 복습 (3유형) — 혼자 채점하는 스크립트 (고치지 말고 실행만)
# 실행: .venv/bin/python workspace/grade_day6.py   (프로젝트 폴더에서)
# workspace/review_day6.py 맨 아래 answer = {...} 에 적은 답을 정답과 비교한다
import io
import json
import runpy
import contextlib

KEY = json.load(open('retake/data/day6_review/_answer_do_not_open.json', encoding='utf-8'))
NAMES = {
    '1-1': '대응 t검정 통계량', '1-2': '대응 t검정 기각/채택', '1-3': 'Welch t검정 p-value',
    '1-4': '카이제곱 통계량', '1-5': '일표본 t검정 p-value',
    '2-1': 'exercise_hours 계수', '2-2': '유의하지 않은 변수 개수', '2-3': '유의한 변수 이름 (전부)',
    '2-4': 'R²', '2-5': '예측값', '2-6': '오즈비',
}

with contextlib.redirect_stdout(io.StringIO()):
    g = runpy.run_path('workspace/review_day6.py')
ans = g.get('answer', {})

print('=' * 56)
print(' Day 6 복습 (3유형) — 자동 채점')
print('=' * 56)
score = 0
for k, right in KEY.items():
    mine = ans.get(k, None)
    if mine is None:
        mark, note = '⬜', '답 없음'
    elif isinstance(right, list):
        ok = isinstance(mine, (list, tuple)) and sorted(map(str, mine)) == sorted(right)
        mark = '✅' if ok else '❌'
        note = '' if ok else (
            '목록 전부 필요 → .index.tolist()' if isinstance(mine, str) else f'정답 {right}')
    elif isinstance(right, str):
        ok = str(mine).strip() == right
        mark = '✅' if ok else '❌'
        note = '' if ok else f'정답 {right} (p < 0.05 → 기각)'
    else:
        try:
            ok = abs(float(mine) - float(right)) < 1e-9
        except (TypeError, ValueError):
            ok = False
        mark = '✅' if ok else '❌'
        note = '' if ok else f'정답 {right} (자릿수·round 확인)'
    score += mark == '✅'
    print(f' {mark} {k}  {NAMES[k]:<22} 내 답: {mine!s:<28} {note}')

print('-' * 56)
print(f' 점수: {score} / {len(KEY)}')
print(' 🎉 3유형 쉬운 소문항 준비 완료!' if score >= 9 else ' ❌ 표시된 소문항만 retake/복습_day6.md 힌트로 다시')
