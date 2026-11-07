"""Score a live benchmark CSV (id;gold;alt;pred;layer;review;hr;llm_error;ms;err).
Usage: python3 scripts/score_live.py test/results/live_*.csv"""
import sys
from collections import defaultdict
POS = {"positive_reply", "interested", "meeting_request"}
for path in sys.argv[1:]:
    rows = [l.split(";") for l in open(path).read().strip().splitlines()]
    n = len(rows); ok = 0; per = defaultdict(lambda: [0, 0, 0])  # tp fp fn
    fpi = []; hr_tp = hr_fn = hr_fp = hr_tn = 0; errs = 0; lat = []
    for r in rows:
        id_, gold, alt, pred, layer, review, hr, llm_err, ms = r[:9]
        alts = [a for a in alt.split("|") if a]
        good = pred == gold or pred in alts
        ok += good
        if good: per[pred][0] += 1
        else: per[pred][1] += 1; per[gold][2] += 1
        if pred in POS and gold not in POS and not any(a in POS for a in alts): fpi.append(id_)
        if hr in ("true", "false"):
            e, g = hr == "true", review == "true"
            hr_tp += e and g; hr_fn += e and not g; hr_fp += (not e) and g; hr_tn += (not e) and not g
        errs += bool(llm_err) or bool(r[9] if len(r) > 9 else "")
        if layer != "rules": lat.append(int(ms))
    f1s = []
    for k, (tp, fp, fn) in per.items():
        if tp + fn == 0: continue
        p = tp / (tp + fp) if tp + fp else 0; rc = tp / (tp + fn)
        f1s.append(2 * p * rc / (p + rc) if p + rc else 0)
    lat.sort()
    print(f"{path}\n  accuracy {ok}/{n} = {ok/n:.1%} | macroF1 {sum(f1s)/len(f1s):.1%} | false-interest {len(fpi)} {fpi}")
    print(f"  human review: tp {hr_tp} fn {hr_fn} fp {hr_fp} tn {hr_tn} | llm errors {errs} | LLM latency ms p50 {lat[len(lat)//2] if lat else '-'} p95 {lat[int(len(lat)*.95)] if lat else '-'}")
    print("  misses:", " ".join(f"{r[0]}:{r[1]}->{r[3]}" for r in rows if not (r[3] == r[1] or r[3] in r[2].split('|'))))
