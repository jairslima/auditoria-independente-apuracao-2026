# -*- coding: utf-8 -*-
"""Fase 27d: inclui a secao RJ zona 144 secao 7 (log publicado na coleta de 27/10) e recalcula todos os numeros do relatorio que dependem dos logs.
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os, statistics, sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fase27_logs_todas as f27

R = f27.RAIZ
SAIDA = f27.SAIDA
linhas = list(csv.DictReader(open(SAIDA, encoding="utf-8-sig"), delimiter=";"))
chaves = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in linhas}
# 1) secoes sem log na coleta de 26/10 que passaram a ter na de 27/10
novas = []
for l in open(os.path.join(R, "dados", "aux_24h.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if j["status"] != 200 or k in chaves:
        continue
    h = json.loads(j["aux"])["hashes"][-1]
    arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
    if arq:
        novas.append((k, f"{f27.B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{arq['nm']}", "resto"))
print("secoes com log novo na coleta de 27/10:", [n[0] for n in novas])
for it in novas:
    r = f27.trabalha(it)
    r.pop("_grupo", None); r.pop("_msgs", None)
    linhas.append(r)
with open(SAIDA, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=f27.CAMPOS, delimiter=";")
    w.writeheader(); w.writerows(linhas)

# 2) numeros finais
comp = {}
for r in csv.DictReader(open(os.path.join(R, "dados", "votos_secao.csv"), encoding="utf-8")):
    comp[(r["uf"], r["mun"], r["zona"], r["sec"])] = int(r["total"])
hr = {}
for l in open(os.path.join(R, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] == 200:
        h = json.loads(j["aux"])["hashes"][-1]
        hr[(j["uf"], j["mun"], j["zona"], j["sec"])] = datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S")
A, B = datetime(2026, 10, 25, 17, 6, 31), datetime(2026, 10, 25, 19, 0, 0)
v = lambda r, c: int(r[c] or 0)
tot_ev = sum(v(r, "votos_total") for r in linhas)
print("secoes com log:", len(linhas), "| eventos de voto:", tot_ev, "| comparecimento (BU) dessas secoes:", sum(comp[(r['uf'], r['mun'], r['zona'], r['sec'])] for r in linhas))
print("comparecimento total:", sum(comp.values()), "| eventos / comparecimento: %.4f%%" % (tot_ev / sum(comp.values()) * 100), "| votos sem evento:", sum(comp.values()) - tot_ev)
res = Counter()
for r in linhas:
    d = comp[(r["uf"], r["mun"], r["zona"], r["sec"])] - v(r, "votos_total")
    res["igual" if d == 0 else "log abaixo do BU" if d > 0 else "log acima do BU"] += 1
print("secoes por diferenca (BU - eventos):", dict(res))
sem_ev = [(r["uf"], r["mun"], r["zona"], r["sec"], comp[(r["uf"], r["mun"], r["zona"], r["sec"])] - v(r, "votos_total")) for r in linhas if comp[(r["uf"], r["mun"], r["zona"], r["sec"])] != v(r, "votos_total")]
print("secoes com diferenca != 0:", len(sem_ev), "| soma:", sum(x[4] for x in sem_ev), "| UFs:", Counter(x[0] for x in sem_ev).most_common(4))
print("maiores diferencas restantes:", sorted(sem_ev, key=lambda x: -abs(x[4]))[:6])
v17, v1706, v19 = (sum(v(r, c) for r in linhas) for c in ("votos_apos_17h00", "votos_apos_17h06", "votos_apos_19h00"))
s17, s1706, s19 = (sum(1 for r in linhas if v(r, c) > 0) for c in ("votos_apos_17h00", "votos_apos_17h06", "votos_apos_19h00"))
print(f"votos apos 17h00: {v17} em {s17} secoes | apos 17h06: {v1706} em {s1706} | apos 19h00: {v19} em {s19}")
a = b = c = sem = 0
uf = defaultdict(lambda: [0, 0, 0, 0, 0])
for r in linhas:
    u = r["uf"]; uf[u][0] += 1; uf[u][1] += v(r, "votos_apos_17h00"); uf[u][2] += 1 if v(r, "votos_apos_17h00") > 0 else 0
    if not r["gera_bu_brt"]:
        sem += 1; continue
    t = datetime.fromisoformat(r["gera_bu_brt"])
    if t < A: a += 1
    elif t < B: b += 1; uf[u][3] += 1
    else: c += 1; uf[u][4] += 1
n = a + b + c
print(f"BU gerado antes de 17h06: {a} ({a / n * 100:.1f}%) | 17h06 a 19h: {b} ({b / n * 100:.1f}%) | depois das 19h: {c} ({c / n * 100:.1f}%) | sem gera_bu: {sem}")
enc = [datetime.fromisoformat(r["encerrar_brt"]) for r in linhas if r["encerrar_brt"]]
print("Encerrar votacao depois das 19h:", sum(1 for t in enc if t >= B), "de", len(enc), "| depois de 17h06:", sum(1 for t in enc if t >= A))
d = defaultdict(list)
for r in linhas:
    k = (r["uf"], r["mun"], r["zona"], r["sec"])
    if r["gera_bu_brt"] and k in hr and r["uf"] != "zz":
        d[r["uf"]].append((hr[k] - datetime.fromisoformat(r["gera_bu_brt"])).total_seconds() / 60)
med = {u: statistics.median(q) for u, q in d.items()}
menor, maior = min(med, key=med.get), max(med, key=med.get)
fmt = lambda m: "%dh%02d" % divmod(int(round(m)), 60)
print("mediana hr - gera_bu: menor", menor, fmt(med[menor]), "| maior", maior, fmt(med[maior]), "| AC", fmt(med["ac"]), "AM", fmt(med["am"]), "RO", fmt(med["ro"]), "RR", fmt(med["rr"]), "MT", fmt(med["mt"]), "MS", fmt(med["ms"]))
# sensibilidade de fuso
def conta(da, du):
    j = 0; tot = 0
    for r in linhas:
        if not r["gera_bu_brt"]: continue
        t = datetime.fromisoformat(r["gera_bu_brt"])
        if r["uf"] == "ac": t += timedelta(hours=da)
        elif r["uf"] in ("am", "ro", "rr", "mt", "ms"): t += timedelta(hours=du)
        tot += 1
        if A <= t < B: j += 1
    return j / tot * 100
print("sensibilidade (%% na janela): base %.2f | AC-1 %.2f | AC+1 %.2f | UTC4-1 %.2f | UTC4+1 %.2f" % (conta(0, 0), conta(-1, 0), conta(1, 0), conta(0, -1), conta(0, 1)))
sem_ex = [r for r in linhas if r["uf"] != "zz" and r["gera_bu_brt"]]
jj = sum(1 for r in sem_ex if A <= datetime.fromisoformat(r["gera_bu_brt"]) < B)
print("sem o exterior: %.2f%% na janela" % (jj / len(sem_ex) * 100))
print("TABELA_UF", json.dumps({u: uf[u] for u in sorted(uf)}))
print("TOTAL_UF", [sum(x[i] for x in uf.values()) for i in range(5)])
