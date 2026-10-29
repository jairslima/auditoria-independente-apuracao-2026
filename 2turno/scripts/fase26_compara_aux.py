# -*- coding: utf-8 -*-
"""Fase 26: compara duas coletas do aux.json (26/10 manha x 27/10, ~24 h depois): status, ultimo hash, lista de arquivos, dr/hr.
Qualquer secao cujo hash do BU, estado ou horario mudou entre as duas coletas aparece em resultados/fase26_aux_mudancas.csv.
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
D = os.path.join(RAIZ, "dados")


def carrega(nome):
    r = {}
    for l in open(os.path.join(D, nome), encoding="utf-8"):
        j = json.loads(l)
        k = (j["uf"], j["mun"], j["zona"], j["sec"])
        if j["status"] != 200:
            if k not in r:
                r[k] = ("HTTP%s" % j["status"], "", "", "", ())
            continue
        a = json.loads(j["aux"])
        h = a["hashes"][-1]
        r[k] = (a.get("st", ""), h["hash"], h["dr"] + " " + h["hr"], h.get("st", ""), tuple(sorted(x["nm"] for x in h["arq"])))
    return r


A, B = carrega("aux_manha_26-10.jsonl"), carrega("aux_24h.jsonl")
mud = []
for k in sorted(set(A) | set(B)):
    a, b = A.get(k), B.get(k)
    if a == b:
        continue
    tipo = []
    if a is None or b is None:
        tipo.append("so_em_uma_coleta")
    else:
        if a[1] != b[1]:
            tipo.append("hash_mudou")
        if a[0] != b[0] or a[3] != b[3]:
            tipo.append("estado_mudou")
        if a[2] != b[2]:
            tipo.append("dr_hr_mudou")
        if a[4] != b[4]:
            tipo.append("arquivos_mudaram")
    mud.append((k, "+".join(tipo), a, b))
with open(os.path.join(RAIZ, "resultados", "fase26_aux_mudancas.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["uf", "mun", "zona", "sec", "tipo", "manha_26_estado", "manha_26_hash", "manha_26_dr_hr", "dia_27_estado", "dia_27_hash", "dia_27_dr_hr"])
    for k, t, a, b in mud:
        w.writerow([*k, t, a[0] if a else "", a[1] if a else "", a[2] if a else "", b[0] if b else "", b[1] if b else "", b[2] if b else ""])
c = Counter(t for _, t, _, _ in mud)
res = {"secoes_coleta_manha": len(A), "secoes_coleta_dia27": len(B), "secoes_com_alguma_mudanca": len(mud),
       "hash_mudou": sum(1 for _, t, _, _ in mud if "hash_mudou" in t),
       "estado_mudou": sum(1 for _, t, _, _ in mud if "estado_mudou" in t),
       "dr_hr_mudou": sum(1 for _, t, _, _ in mud if "dr_hr_mudou" in t),
       "so_em_uma_coleta": sum(1 for _, t, _, _ in mud if "so_em_uma_coleta" in t), "por_tipo": dict(c)}
json.dump(res, open(os.path.join(RAIZ, "resultados", "fase26_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False))
