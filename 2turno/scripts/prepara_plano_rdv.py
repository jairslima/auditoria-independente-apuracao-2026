# -*- coding: utf-8 -*-
"""Amplia o plano do RDV (dados/assinaturas_estadual.csv) para as 499.207 secoes. Mantem as ja planejadas. Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
p = os.path.join(RAIZ, "dados", "assinaturas_estadual.csv")
tem = set()
linhas = []
for r in csv.DictReader(open(p, encoding="utf-8")):
    tem.add((r["uf"], r["mun"], r["zona"], r["sec"]))
    linhas.append([r["uf"], r["mun"], r["zona"], r["sec"], r["grupo"]])
novas = 0
for l in open(os.path.join(RAIZ, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if j["status"] == 200 and k not in tem:
        linhas.append([*k, "completa"])
        tem.add(k)
        novas += 1
with open(p, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["uf", "mun", "zona", "sec", "grupo"])
    w.writerows(linhas)
print("plano do RDV:", len(linhas), "secoes (", novas, "novas )")
