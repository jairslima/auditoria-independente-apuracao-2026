"""Fase 6b (nivel municipio): o desvio do % de Flavio ao longo do tempo e explicado so pela composicao entre UFs (que UF chegou antes)?
Compara % observado acumulado em T com % esperado se cada UF votasse seu % final (so a mistura de UFs muda)."""
import csv, os
from collections import defaultdict
from datetime import datetime
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")))
cands = [c for c in rows[0] if c.startswith("c")]
for r in rows:
    r["_t"] = datetime.strptime(r["hr"], "%d/%m/%Y %H:%M:%S"); r["_v"] = sum(int(r[c]) for c in cands)
fin = defaultdict(lambda: [0, 0, 0])
for r in rows:
    a = fin[(r["uf"], r["mun"])]; a[0] += int(r["c22"]); a[1] += int(r["c13"]); a[2] += r["_v"]
for T in ["18:00", "18:30", "19:00", "19:06", "19:30", "20:00", "21:00"]:
    lim = datetime.strptime("04/10/2026 " + T + ":59", "%d/%m/%Y %H:%M:%S")
    obs = defaultdict(lambda: [0, 0, 0])
    for r in rows:
        if r["_t"] <= lim:
            a = obs[(r["uf"], r["mun"])]; a[0] += int(r["c22"]); a[1] += int(r["c13"]); a[2] += r["_v"]
    V = sum(a[2] for a in obs.values())
    pf_obs = sum(a[0] for a in obs.values()) / V * 100
    pf_esp = sum(a[2] * fin[u][0] / fin[u][2] for u, a in obs.items()) / V * 100
    pl_obs = sum(a[1] for a in obs.values()) / V * 100
    pl_esp = sum(a[2] * fin[u][1] / fin[u][2] for u, a in obs.items()) / V * 100
    print(f"ate {T}: Flavio obs {pf_obs:.2f}% | esperado so por mistura de UFs {pf_esp:.2f}% | resid {pf_obs-pf_esp:+.2f} pp || Lula obs {pl_obs:.2f}% esp {pl_esp:.2f}% resid {pl_obs-pl_esp:+.2f} pp")
