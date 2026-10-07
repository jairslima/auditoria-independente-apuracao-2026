"""Fase 5: (a) quais secoes instaladas ficaram sem BU e por que; (b) curva acumulada de Flavio/Lula por hora de chegada."""
import csv, json, os, glob
from collections import Counter, defaultdict
from datetime import datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")))
tem = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in rows}
faltam = []
for f in sorted(glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json"))):
    d = json.load(open(f, encoding="utf-8")); uf = d["abr"][0]["cd"]
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" in s and (uf, m["cd"], z["cd"], s["ns"]) not in tem:
                    faltam.append((uf, m["cd"], z["cd"], s["ns"]))
print("instaladas sem BU:", len(faltam), dict(Counter(k[0] for k in faltam)))
aux = {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l); aux[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
motivos = Counter()
for k in faltam:
    j = aux.get(k)
    if not j or j["status"] != 200:
        motivos[f"aux HTTP {j['status'] if j else 'ausente'}"] += 1
    else:
        a = json.loads(j["aux"]); h = a["hashes"][-1]
        motivos[f"aux ok st={a.get('st')}/{h.get('st')} arqs={sorted(x['tp'] for x in h['arq'])}"] += 1
for m, n in motivos.most_common(): print(n, m)
json.dump(faltam, open(os.path.join(RAIZ, "dados/secoes_sem_bu.json"), "w"))

pts = sorted(((datetime.strptime(r["hr"], "%d/%m/%Y %H:%M:%S"), r) for r in rows), key=lambda x: x[0])
f = l = v = 0; maxp = (0, None)
marcos = {}
for i, (t, r) in enumerate(pts, 1):
    f += int(r["c22"]); l += int(r["c13"]); v += sum(int(r[c]) for c in r if c.startswith("c"))
    p = f / v * 100
    if i > 20000 and p > maxp[0]: maxp = (p, t, i)
    h = t.replace(minute=t.minute // 15 * 15, second=0)
    marcos[h] = (i, f, l, v)
print("\nmaximo de Flavio % dos validos (apos 20 mil secoes):", round(maxp[0], 3), maxp[1], "secao", maxp[2])
print("\nhora(15min) | secoes | Flavio % | Lula % | margem Flavio-Lula")
for h, (i, f, l, v) in sorted(marcos.items()):
    if h.day == 4 and 17 <= h.hour <= 23 or h.day == 5 and h.hour < 3:
        print(h.strftime("%d %H:%M"), f"{i:>7,}", f"{f/v*100:6.2f}", f"{l/v*100:6.2f}", f"{f-l:>12,}")
print("\nFINAL (BUs):", i, f"Flavio {f/v*100:.3f}%  Lula {l/v*100:.3f}%  validos {v:,}")
