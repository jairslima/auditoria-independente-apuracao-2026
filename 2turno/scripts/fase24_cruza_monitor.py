"""Fase 24: cruza o relogio proprio do monitor (primeira vez que vimos cada secao no indice) com o hr do aux.json.
Atraso = utc_primeira_vez - (dr hr do aux, BRT=UTC-3). So vale para secoes com hr depois do inicio do monitor.
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase24_cruza_monitor.csv e resumo no stdout."""
import csv, json, os, statistics
from datetime import datetime, timedelta
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MON = os.path.join(RAIZ, "..", "AuditoriaPresidente2026", "segundo_turno", "dados_monitor", "primeira_vez.csv")
ini_mon = datetime(2026, 10, 25, 19, 0, 0)  # primeira consulta do monitor, UTC
pv = {}
for r in csv.reader(open(MON, encoding="utf-8", newline=""), delimiter=";"):
    if len(r) >= 5 and r[0] != "utc_primeira_vez":
        pv[(r[1], r[2], r[3], r[4])] = datetime.strptime(r[0], "%Y-%m-%dT%H:%M:%SZ")
linhas = []
for l in open(os.path.join(RAIZ, "dados", "aux.jsonl"), encoding="utf-8"):
    j = json.loads(l); k = (j["uf"], j["mun"], j["zona"], j["sec"])
    h = json.loads(j["aux"])["hashes"][-1]
    t_hr = datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S") + timedelta(hours=3)  # BRT -> UTC
    vis = pv.get(k)
    linhas.append((k, t_hr, vis))
sem_vis = [x for x in linhas if x[2] is None]
com = [x for x in linhas if x[2] is not None and x[1] >= ini_mon]
atr = [(x[2] - x[1]).total_seconds() for x in com]
os.makedirs(os.path.join(RAIZ, "resultados"), exist_ok=True)
with open(os.path.join(RAIZ, "resultados", "fase24_cruza_monitor.csv"), "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter=";"); w.writerow(["uf", "mun", "zona", "sec", "hr_utc", "primeira_vez_utc", "atraso_s"])
    for (k, t, v), a in zip(com, atr):
        w.writerow([*k, t.isoformat(), v.isoformat(), int(a)])
print("secoes no aux:", len(linhas), "| vistas pelo monitor:", len(linhas) - len(sem_vis), "| nunca vistas:", len(sem_vis))
print("com hr depois do inicio do monitor (19:00Z):", len(com))
if atr:
    q = statistics.quantiles(atr, n=100)
    print(f"atraso s: min {min(atr):.0f} mediana {statistics.median(atr):.0f} p90 {q[89]:.0f} p99 {q[98]:.0f} max {max(atr):.0f}")
    for lim in (300, 900, 3600, 7200):
        print(f"  > {lim}s: {sum(1 for a in atr if a > lim)}")
    neg = [a for a in atr if a < -60]
    print("  vistas ANTES do hr (>60s adiantado):", len(neg))
