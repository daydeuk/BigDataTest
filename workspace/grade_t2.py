# 2유형 최종 복습 — 혼자 채점하는 스크립트 (고치지 말고 실행만)
# 실행: .venv/bin/python workspace/grade_t2.py cls    (Set 1 분류 · AUC)
#       .venv/bin/python workspace/grade_t2.py reg    (Set 2 회귀 · RMSE)
# [1] 제출 형식 → [2] 숨긴 정답으로 점수 → [3] 풀이 코드에서 반복 실수 점검
import os
import re
import sys
import numpy as np
import pandas as pd
from sklearn.metrics import roc_auc_score, mean_squared_error

D = 'retake/data/final_t2'
SETS = {
    'cls': dict(name='Set 1 — 헬스장 회원 이탈 (이진 분류 · ROC-AUC)', result='result_cls.csv',
                src='workspace/final_t2_cls.py', train=f'{D}/gym_train.csv', test=f'{D}/gym_test.csv',
                answer=f'{D}/_answer_cls_do_not_open.csv', target='churn', idc='member_id', n_train=1000, n_val=200),
    'reg': dict(name='Set 2 — 배달 소요 시간 (회귀 · RMSE)', result='result_reg.csv',
                src='workspace/final_t2_reg.py', train=f'{D}/delivery_train.csv', test=f'{D}/delivery_test.csv',
                answer=f'{D}/_answer_reg_do_not_open.csv', target='delivery_min', idc='order_id', n_train=1200, n_val=240),
}
PASS_AUC, PASS_RMSE = 0.83, 7.2

args = sys.argv[1:]
kind = args[0] if args else ''
if kind not in SETS:
    print('사용법: .venv/bin/python workspace/grade_t2.py cls   (또는 reg)')
    raise SystemExit
S = dict(SETS[kind])
for flag in ('--src', '--result'):          # 출제자 검토용 (평소엔 안 씀)
    if flag in args:
        S[flag[2:]] = args[args.index(flag) + 1]

print('=' * 64)
print(f' 2유형 최종 복습 — 자동 채점 · {S["name"]}')
print('=' * 64)

# ---------------------------------------------------------------- [1] 형식
print('\n[1] 제출 형식')
ok = True
p = None
if not os.path.exists(S['result']):
    ok = False
    print(f"  ❌ {S['result']} 가 없다 — 프로젝트 폴더에 이 이름으로 저장했는지 확인")
    src_txt = open(S['src'], encoding='utf-8').read() if os.path.exists(S['src']) else ''
    if re.search(r"to_csv\(\s*['\"]%s['\"]" % re.escape(S['result']), src_txt):
        print(f"     → 풀이 파일에는 to_csv('{S['result']}')가 있다 = 고친 뒤 실행(▷)을 안 한 것. 풀이 파일을 다시 실행하고 채점")
    elif os.path.exists('result.csv'):
        print("     → result.csv 가 보인다. 이번 문제의 파일 이름은 "
              f"{S['result']} (실전 분류 때 만든 result.csv일 수도 있음)")
else:
    r = pd.read_csv(S['result'])
    n_test = len(pd.read_csv(S['test']))
    if os.path.exists(S['src']) and os.path.getmtime(S['src']) > os.path.getmtime(S['result']) + 1:
        print('  ⚠️ 풀이 파일을 결과 파일보다 나중에 고쳤다 → 고친 뒤 다시 실행(▷)했는지 확인 (아래 점수는 옛 결과)')
    if list(r.columns) != ['pred']:
        ok = False
        print(f'  ❌ 컬럼이 {list(r.columns)} — pred 하나여야 한다')
        if any(str(c).startswith('Unnamed') for c in r.columns):
            print('     → index=False 빠짐 (Unnamed: 0 컬럼이 생김)')
        elif 'pred' not in r.columns:
            print("     → pd.DataFrame({'pred': pred}) — 컬럼 이름을 pred로")
    else:
        print('  ✅ 컬럼: pred 하나')
    if len(r) != n_test:
        ok = False
        print(f'  ❌ 행 수 {len(r)} — test 행 수 {n_test}와 다르다')
        if len(r) == S['n_train']:
            print('     → X(train)로 예측함. 5-2는 X_test')
        elif len(r) == S['n_val']:
            print('     → X_val(검증용)로 예측함. 5-2는 X_test')
        elif len(r) < n_test:
            print('     → test 행을 지웠나? (dropna 등) test는 한 행도 지우면 안 된다')
    else:
        print(f'  ✅ 행 수: {len(r)} (= test 행 수)')
    if 'pred' in r.columns:
        p = r['pred']
        if p.isnull().sum() > 0:
            ok = False
            print(f'  ❌ pred에 결측 {p.isnull().sum()}개')
        if not pd.api.types.is_numeric_dtype(p):
            ok = False
            print(f'  ❌ pred가 숫자가 아니다: {list(p.astype(str).unique()[:3])}')
        elif kind == 'cls':
            if set(p.dropna().unique()) <= {0, 1}:
                print('  ⚠️ 값이 0과 1뿐 → predict를 냈다. AUC는 확률 predict_proba(X_test)[:, 1] (점수가 깎인다)')
            elif p.min() < 0 or p.max() > 1:
                ok = False
                print('  ❌ 0~1 밖의 값이 있다 — 확률이 아니다')
            else:
                print(f'  ✅ 값: 0~1 확률 ({p.nunique()}가지)')
        else:
            if p.nunique() == 1:
                print(f'  ⚠️ 400건 예측이 전부 {p.iloc[0]:.2f} 하나 — 모델 예측이 아니라 값 하나로 찍었다')
            else:
                print(f'  ✅ 값: 숫자 (범위 {p.min():.1f} ~ {p.max():.1f}분)')

# ---------------------------------------------------------------- [2] 점수
print('\n[2] 점수 (숨긴 test 정답)')
if not ok or p is None:
    print('  ⛔ 형식이 틀려 실제 시험이면 채점 불가 — [1]부터 고치기')
else:
    ans = pd.read_csv(S['answer'])[S['target']]
    if kind == 'cls':
        sc = roc_auc_score(ans, p)
        print(f'  test ROC-AUC = {sc:.4f}   (통과 기준 {PASS_AUC} 이상, 높을수록 좋음)')
        if sc >= PASS_AUC:
            print('  🎉 통과!')
        elif sc < 0.5:
            print('  ❌ 0.5보다 낮다 = 거꾸로 맞힘 → [:, 0](이탈 안 할 확률)을 냈다. AUC는 [:, 1]')
        elif set(p.unique()) <= {0, 1}:
            print('  ❌ 0/1을 내서 깎였다 → pred = model.predict_proba(X_test)[:, 1]')
        else:
            print('  ❌ 기준 미달 — 결측 · 인코딩 · predict_proba 확인')
        print('  참고: 기본 템플릿 약 0.869 / 0·1(predict)로 내면 0.669 / [:, 0]으로 내면 0.131')
    else:
        sc = np.sqrt(mean_squared_error(ans, p))
        print(f'  test RMSE = {sc:.4f}   (통과 기준 {PASS_RMSE} 이하, 낮을수록 좋음)')
        print('  🎉 통과!' if sc <= PASS_RMSE else '  ❌ 기준 미달 — 결측을 같은 컬럼 값으로 채웠는지 · 인코딩 · Regressor 확인')
        print('  참고: 기본 템플릿 약 6.56 / 결측을 다른 컬럼 값으로 채우면 8.24 / 평균 하나로 찍으면 14.10')

# ---------------------------------------------------------------- [3] 코드 점검
print('\n[3] 코드 점검 — 풀이 파일에서 반복 실수 찾기 (점수와 별개, 주석은 무시)')


def strip_comment(line):
    out, q = [], None
    for ch in line:
        if q:
            out.append(ch)
            if ch == q:
                q = None
        elif ch in '\'"':
            q = ch
            out.append(ch)
        elif ch == '#':
            break
        else:
            out.append(ch)
    return ''.join(out).rstrip()


if not os.path.exists(S['src']):
    print(f"  (풀이 파일 {S['src']} 없음)")
    raise SystemExit
lines = [strip_comment(l) for l in open(S['src'], encoding='utf-8')]
lines = [l for l in lines if l.strip()]
txt = '\n'.join(lines)
if len(lines) < 5:
    print('  (아직 코드가 거의 없다 — 풀고 나서 다시 채점)')
    raise SystemExit
good, warn = [], []

# 2-1 나누기
if re.search(r'X_test\s*=\s*test\s*\.\s*drop', txt):
    good.append('2-1 X_test를 test에서 만듦')
elif re.search(r'X_test\s*=\s*train', txt):
    warn.append('2-1 X_test를 train에서 만듦 → X_test = test.drop(columns=[…])')

# 2-2 결측: 컬럼마다 채웠나
miss = set()
for f in (S['train'], S['test']):
    s = pd.read_csv(f).isnull().sum()
    miss |= set(s[s > 0].index)
miss.discard(S['target'])
whole = any(re.search(r'\b(X|X_test|train|test)\s*\.\s*fillna\(', l) for l in lines)


def handled(col):
    pat = re.compile(r"['\"]%s['\"]" % re.escape(col))
    for i, l in enumerate(lines):
        if pat.search(l) and 'fillna' in l:
            return True
        if pat.search(l) and (l.lstrip().startswith('for ') or re.match(r'\s*\w+\s*=\s*\[', l)):
            if any('fillna' in x for x in lines[i:i + 8]):
                return True
    return whole


for c in sorted(miss):
    if handled(c):
        good.append(f"2-2 '{c}' 결측 채움")
    else:
        warn.append(f"2-2 '{c}' 결측을 채우는 줄을 못 찾았다 (이 PC sklearn 1.6은 그냥 돌아가지만 시험장 버전은 💥 가능)")

# 2-2 결측: 같은 컬럼 · train 기준
var_src = {}
for l in lines:
    m1 = re.search(r"(\w+)\s*=\s*(X_test|X|train|test)\[['\"](\w+)['\"]\]\s*\.\s*(median|mean|mode)\(", l)
    if m1:
        var_src[m1.group(1)] = (m1.group(2), m1.group(3))
    m2 = re.search(r"(X_test|X|train|test)\[['\"](\w+)['\"]\]\s*=\s*(X_test|X|train|test)\[['\"](\w+)['\"]\]"
                   r"\s*\.\s*fillna\((.*)\)", l)
    if not m2:
        continue
    lt, lc, rt, rc, arg = m2.groups()
    if lc != rc:
        warn.append(f"2-2 {lt}['{lc}'] = {rt}['{rc}'].fillna(…) — 왼쪽·오른쪽 컬럼 이름이 다르다")
    a = arg.strip()
    src = var_src.get(a)
    inline = re.search(r"(X_test|X|train|test)\[['\"](\w+)['\"]\]\s*\.\s*(median|mean|mode)\(", a)
    if inline:
        src = (inline.group(1), inline.group(2))
    if src:
        if src[1] != lc:
            warn.append(f"2-2 '{lc}'을 '{src[1]}' 값으로 채움 → m = X['{lc}']…처럼 같은 컬럼에서 구하기 (반복 실수 ⚠️)")
        if src[0] in ('X_test', 'test'):
            warn.append(f"2-2 '{lc}'을 test 값으로 채움 → 채울 값은 train(X)에서 구한다")

# 3-1 인코딩
enc = 'get_dummies(' in txt or 'LabelEncoder' in txt
if enc and 'concat(' in txt:
    good.append('3-1 합쳐서 인코딩')
elif enc:
    warn.append('3-1 concat 없이 인코딩 → test에만 있는 범주 때문에 컬럼이 어긋난다. 합쳐서 → 바꾸고 → iloc으로 나누기')
if re.search(r"get_dummies\(\s*\w+\s*,(?!\s*(?:columns|drop_first|dtype|prefix)\s*=)", txt):
    warn.append("3-1 get_dummies(all_x, […]) — columns= 빠짐 → get_dummies(all_x, columns=[…])")

# 4-1 분할
tts = re.findall(r'train_test_split\((.*?)\)', txt, flags=re.S)
if not tts:
    warn.append('4-1 train_test_split이 없다 — 검증 점수를 못 본다 (제출 점수와는 별개지만 템플릿대로)')
elif kind == 'cls':
    if any(re.search(r'stratify\s*=\s*y\b', t) for t in tts):
        good.append('4-1 stratify=y')
    else:
        warn.append('4-1 분류인데 stratify=y 빠짐 (Day 4 · 실전 분류에 이어 반복 실수 ⚠️)')
else:
    if any('stratify' in t for t in tts):
        warn.append('4-1 회귀에 stratify → 💥 에러 원인. 회귀는 stratify 없음')
    else:
        good.append('4-1 회귀라 stratify 없음')

# 4-2 모델
models = re.findall(r'RandomForest(Classifier|Regressor)\s*\(([^)]*)\)', txt)
want = 'Classifier' if kind == 'cls' else 'Regressor'
if not models:
    warn.append('4-2 RandomForest 모델 줄을 못 찾았다')
else:
    if all(k == want for k, _ in models):
        good.append(f'4-2 RandomForest{want}')
    else:
        warn.append(f'4-2 {"분류" if kind == "cls" else "회귀"}인데 RandomForest{"Regressor" if kind == "cls" else "Classifier"} 사용')
    if all('random_state' in a for _, a in models):
        good.append('4-2 random_state 고정')
    else:
        warn.append('4-2 random_state 빠짐 → 실행할 때마다 점수가 달라진다 (반복 실수)')

# 4-3 · 4-4 · 5-2 지표
if kind == 'cls':
    has1 = re.search(r'predict_proba\([^)]*\)\s*\[\s*:\s*,\s*1\s*\]', txt)
    has0 = re.search(r'predict_proba\([^)]*\)\s*\[\s*:\s*,\s*0\s*\]', txt)
    if has0:
        warn.append('4-3·5-2 predict_proba(…)[:, 0] = 이탈 안 할 확률 → [:, 1]')
    elif has1:
        good.append('4-3·5-2 predict_proba(…)[:, 1]')
    else:
        warn.append('4-3·5-2 AUC인데 predict_proba(…)[:, 1]이 없다')
    if re.search(r'pred\s*=\s*model\.predict\(\s*X_test\s*\)', txt):
        warn.append('5-2 pred = model.predict(X_test) → AUC는 확률 predict_proba(X_test)[:, 1]')
    if 'roc_auc_score(' in txt:
        good.append('4-4 검증 AUC 확인')
    else:
        warn.append('4-4 검증 점수(roc_auc_score)를 안 구했다')
else:
    if 'predict_proba' in txt:
        warn.append('4-3 회귀에는 확률이 없다 → predict')
    if 'squared=False' in txt.replace(' ', ''):
        warn.append('4-4 squared=False → 이 PC(sklearn 1.6) 💥 TypeError. np.sqrt(mean_squared_error(…))')
    elif re.search(r'np\.sqrt\(\s*mean_squared_error', txt) or 'root_mean_squared_error' in txt:
        good.append('4-4 검증 RMSE = np.sqrt(mean_squared_error(…))')
    else:
        warn.append('4-4 검증 RMSE를 안 구했다 → np.sqrt(mean_squared_error(y_val, pred))')

# 5-1 다시 학습 · 5-2 저장
if re.search(r'\.fit\(\s*X\s*,\s*y\s*\)', txt):
    good.append('5-1 fit(X, y) 다시 학습')
else:
    warn.append('5-1 model.fit(X, y) 다시 학습이 없다 → 80%로만 배운 모델로 제출 (점수 조금 손해)')
if re.search(r"to_csv\([^)]*index\s*=\s*False", txt):
    good.append('5-2 index=False')

warn = list(dict.fromkeys(warn))        # X · X_test 두 줄에서 같은 경고가 나오면 한 번만
for g in good:
    print(f'  ✅ {g}')
for w in warn:
    print(f'  ⚠️ {w}')
print('-' * 64)
print(f'  코드 점검: ✅ {len(good)}개 / ⚠️ {len(warn)}개' + ('  — 깔끔!' if not warn else '  — ⚠️ 줄만 고치면 된다'))
