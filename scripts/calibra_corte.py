"""Calibracao 3: com todos os aux.json, quantas secoes tem hr <= T e qual T reproduz 323.539 (painel 19:06:33)."""
import json, os, collections
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ult = {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j

hrs, multi, sts = [], 0, collections.Counter()
for k, j in ult.items():
    if j["status"] != 200:
        continue
    a = json.loads(j["aux"])
    sts[a.get("st")] += 1
    if len(a["hashes"]) > 1:
        multi += 1
    h = a["hashes"][-1]
    hrs.append((datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S"), k))
hrs.sort()
print("secoes:", len(hrs), "| status aux:", dict(sts), "| com >1 hash:", multi)
alvo = 323539
lim = datetime(2026, 10, 4, 19, 6, 33)
n_lim = sum(1 for h, _ in hrs if h <= lim)
print("hr <= 19:06:33:", n_lim, "| diferenca p/ painel:", n_lim - alvo)
t_alvo = hrs[alvo - 1][0]
print("a secao #323539 (ordem por hr) tem hr =", t_alvo, "| defasagem vs 19:06:33:", lim - t_alvo)
for m in range(0, 61, 5):
    pass
print("hr extremos:", hrs[0][0], hrs[-1][0])
