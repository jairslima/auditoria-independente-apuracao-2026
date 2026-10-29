# -*- coding: utf-8 -*-
"""Fase 28: numero da urna no log (serie) x numero da urna no certificado de hardware, em TODAS as secoes.
Entradas: resultados/fase27_logs_todas.csv e dados/assinaturas_secao.csv. Saida: resultados/fase28_urna_certificado.csv e fase28_resumo.json.
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
cert = {(r["uf"], r["mun"], r["zona"], r["sec"]): r["n_urna_cn"]
        for r in csv.DictReader(open(os.path.join(RAIZ, "dados", "assinaturas_secao.csv"), encoding="utf-8"))}
iguais = dif = sem_cert = sem_log = 0
difs = []
logs = {(r["uf"], r["mun"], r["zona"], r["sec"]): r for r in csv.DictReader(open(os.path.join(RAIZ, "resultados", "fase27_logs_todas.csv"), encoding="utf-8-sig"), delimiter=";")}
# todas as secoes com BU (as 499.207), para contar tambem as que nao tem log publicado
secoes = [(r["uf"], r["mun"], r["zona"], r["sec"]) for r in csv.DictReader(open(os.path.join(RAIZ, "dados", "votos_secao.csv"), encoding="utf-8"))]
for k in secoes:
    r = logs.get(k, {"urna_serie": ""})
    c = cert.get(k, "")
    if not r["urna_serie"]:
        sem_log += 1
        continue
    if not c:
        sem_cert += 1
        continue
    if int(r["urna_serie"]) == int(c):
        iguais += 1
    else:
        dif += 1
        difs.append((*k, r["urna_serie"], c))
with open(os.path.join(RAIZ, "resultados", "fase28_urna_certificado.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["uf", "mun", "zona", "sec", "urna_no_log", "urna_no_certificado"])
    w.writerows(difs)
res = {"iguais": iguais, "diferentes": dif, "sem_certificado": sem_cert, "sem_log": sem_log}
json.dump(res, open(os.path.join(RAIZ, "resultados", "fase28_resumo.json"), "w"), indent=1)
print(res)
