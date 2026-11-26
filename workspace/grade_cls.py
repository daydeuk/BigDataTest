# 실전 분류 복습 — 혼자 채점하는 스크립트 (고치지 말고 실행만)
# 실행: .venv/bin/python workspace/grade_cls.py   (프로젝트 폴더에서, result.csv를 만든 뒤)
import os
import pandas as pd
from sklearn.metrics import f1_score

PASS = 0.60
ANSWER = 'retake/data/final_cls/_answer_do_not_open.csv'
TEST = 'retake/data/final_cls/member_test.csv'

print('=' * 50)
print(' 실전 분류 복습 — 자동 채점')
print('=' * 50)

if not os.path.exists('result.csv'):
    print('❌ result.csv가 없다. 프로젝트 폴더에 result.csv로 저장했는지 확인')
    raise SystemExit

r = pd.read_csv('result.csv')
n_test = len(pd.read_csv(TEST))
ok = True

# 1. 형식
print('\n[1] 제출 형식')
if list(r.columns) != ['pred']:
    ok = False
    print(f'  ❌ 컬럼이 {list(r.columns)} — pred 하나여야 한다')
    if any(c.startswith('Unnamed') for c in r.columns):
        print('     → index=False 빠짐 (Unnamed: 0 컬럼이 생김)')
else:
    print('  ✅ 컬럼: pred 하나')

if len(r) != n_test:
    ok = False
    print(f'  ❌ 행 수 {len(r)} — test 행 수 {n_test}와 다르다')
    if len(r) == 1200:
        print('     → X(train)로 예측함. 5-2는 X_test')
    elif len(r) == 240:
        print('     → X_val(검증)으로 예측함. 5-2는 X_test')
else:
    print(f'  ✅ 행 수: {len(r)} (= test 행 수)')

if 'pred' in r.columns:
    if r['pred'].isnull().sum() > 0:
        ok = False
        print(f'  ❌ pred에 결측 {r["pred"].isnull().sum()}개')
    vals = set(r['pred'].dropna().astype(str).unique())
    labels = {'Bronze', 'Silver', 'Gold'}
    if not vals <= labels:
        ok = False
        print(f'  ❌ pred 값이 {sorted(vals)[:5]} … — Bronze / Silver / Gold 글자여야 한다')
        if pd.api.types.is_float_dtype(r['pred']):
            print('     → 확률(predict_proba)을 낸 것 같다. macro F1은 predict()로')
    else:
        print(f'  ✅ 값: {sorted(vals)}')

# 2. 점수
print('\n[2] 점수 (숨겨진 test 정답, macro F1)')
if not ok:
    print('  ⛔ 형식이 틀려 실제 시험이면 채점 불가 — 위부터 고치기')
    raise SystemExit

ans = pd.read_csv(ANSWER)['grade']
score = f1_score(ans, r['pred'].astype(str), average='macro')
print(f'  test macro F1 = {score:.4f}  (통과 기준 {PASS})')
print('  🎉 통과!' if score >= PASS else '  ❌ 기준 미달 — 전처리(결측·인코딩)·predict 확인')
print('\n  참고: 기본 템플릿 약 0.664 / 전부 Bronze로 찍으면 0.212')
