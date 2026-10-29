# -*- coding: utf-8 -*-
"""Fase 21b (2o turno): para cada tipo de mensagem do log da urna, compara a frequencia (fracao das secoes em que a mensagem aparece)
nas secoes atrasadas, nas vistas antes do hr e nas do Sistema de Apuracao contra todas as demais, usando os logs de TODAS as urnas
(contadores gravados pela fase 27). Saida: resultados/fase21b_mensagens.csv e fase21b_resumo.json.
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ck = json.load(open(os.path.join(RAIZ, "resultados", "fase27_msg_contadores.json"), encoding="utf-8"))
tot = ck["tot"]
resto_n = tot.get("resto", 0)
linhas = []
for m, c in ck["msgs"]:
    pr = c.get("resto", 0) / resto_n if resto_n else 0
    for g in ("atrasada", "antes_hr", "sist_apuracao"):
        n = tot.get(g, 0)
        if not n:
            continue
        pg = c.get(g, 0) / n
        if abs(pg - pr) > 0.10:
            linhas.append((abs(pg - pr), g, n, c.get(g, 0), round(pg, 4), c.get("resto", 0), round(pr, 4), m[0], m[1], m[2]))
linhas.sort(reverse=True)
with open(os.path.join(RAIZ, "resultados", "fase21b_mensagens.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["diferenca_abs", "grupo", "secoes_no_grupo", "com_a_mensagem_no_grupo", "fracao_no_grupo", "com_a_mensagem_no_resto", "fracao_no_resto", "modulo", "nivel", "mensagem"])
    w.writerows(linhas)
res = {"secoes_por_grupo": tot, "tipos_de_mensagem": len(ck["msgs"]),
       "diferencas_acima_de_10pp": {g: sum(1 for l in linhas if l[1] == g) for g in ("atrasada", "antes_hr", "sist_apuracao")}}
json.dump(res, open(os.path.join(RAIZ, "resultados", "fase21b_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
for l in [x for x in linhas if x[1] != "sist_apuracao"][:20]:
    print(l)
