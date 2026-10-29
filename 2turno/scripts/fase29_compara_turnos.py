# -*- coding: utf-8 -*-
"""Fase 29: compara o 1o e o 2o turno de Presidente SECAO A SECAO (mesma uf, municipio, zona e secao), a partir dos BUs dos dois turnos.
Mostra de onde vieram os votos a mais de cada candidato: variacao de comparecimento, de brancos e nulos, e a variacao de cada candidato por UF.
O voto e secreto: o BU nao permite saber quem mudou de voto, so quanto mudou em cada secao. A transferencia entre candidatos e estimada por
regressao ecologica (fase 29b), que e um indicio estatistico, nao prova de como cada eleitor votou.
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase29_*.csv e fase29_resumo.json"""
import csv, json, os
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T1 = os.path.join(os.path.dirname(RAIZ), "AuditoriaPresidente2026", "dados", "votos_secao.csv")
T2 = os.path.join(RAIZ, "dados", "votos_secao.csv")
OUT = os.path.join(RAIZ, "resultados")
NOMES = {"c13": "Lula", "c22": "Flávio Bolsonaro"}


def le(p):
    d = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        d[(r["uf"], r["mun"], r["zona"], r["sec"])] = {k: int(v) for k, v in r.items() if k not in ("uf", "mun", "zona", "sec", "hr", "sha256_bu", "ts_bu")}
    return d


a, b = le(T1), le(T2)
cands1 = [k for k in next(iter(a.values())) if k.startswith("c")]
comuns = sorted(set(a) & set(b))
print("secoes 1o turno:", len(a), "| 2o turno:", len(b), "| nas duas:", len(comuns), "| so no 1o:", len(set(a) - set(b)), "| so no 2o:", len(set(b) - set(a)), flush=True)


def soma(d, keys, campo):
    return sum(d[k].get(campo, 0) for k in keys)


nac = {"secoes_nas_duas": len(comuns), "secoes_so_1o_turno": len(set(a) - set(b)), "secoes_so_2o_turno": len(set(b) - set(a))}
for rot, d, ks in (("1o_turno_todas", a, list(a)), ("2o_turno_todas", b, list(b)), ("1o_turno_secoes_comuns", a, comuns), ("2o_turno_secoes_comuns", b, comuns)):
    nac[rot] = {"comparecimento": soma(d, ks, "total"), "brancos": soma(d, ks, "branco"), "nulos": soma(d, ks, "nulo"),
                **{c: soma(d, ks, c) for c in (cands1 if d is a else ["c13", "c22"])}}
json.dump(nac, open(os.path.join(OUT, "fase29_resumo.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(json.dumps(nac, ensure_ascii=False, indent=1), flush=True)

# por UF: variacao nas secoes comuns
uf = defaultdict(lambda: defaultdict(int))
for k in comuns:
    u = k[0]
    for campo in ("total", "branco", "nulo"):
        uf[u]["1_" + campo] += a[k][campo]
        uf[u]["2_" + campo] += b[k][campo]
    for c in ("c13", "c22"):
        uf[u]["1_" + c] += a[k].get(c, 0)
        uf[u]["2_" + c] += b[k][c]
    uf[u]["1_outros"] += sum(a[k].get(c, 0) for c in cands1 if c not in ("c13", "c22"))
with open(os.path.join(OUT, "fase29_por_uf.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["uf", "comparecimento_1o", "comparecimento_2o", "dif_comparecimento", "lula_1o", "lula_2o", "dif_lula", "flavio_1o", "flavio_2o", "dif_flavio",
                "outros_candidatos_1o", "brancos_1o", "brancos_2o", "nulos_1o", "nulos_2o"])
    for u in sorted(uf):
        x = uf[u]
        w.writerow([u, x["1_total"], x["2_total"], x["2_total"] - x["1_total"], x["1_c13"], x["2_c13"], x["2_c13"] - x["1_c13"], x["1_c22"], x["2_c22"],
                    x["2_c22"] - x["1_c22"], x["1_outros"], x["1_branco"], x["2_branco"], x["1_nulo"], x["2_nulo"]])

# secao a secao: variacoes
with open(os.path.join(OUT, "fase29_secoes.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["uf", "mun", "zona", "sec", "comp_1o", "comp_2o", "dif_comp", "lula_1o", "lula_2o", "dif_lula", "flavio_1o", "flavio_2o", "dif_flavio",
                "outros_1o", "brancos_nulos_1o", "brancos_nulos_2o"])
    for k in comuns:
        x, y = a[k], b[k]
        outros = sum(x.get(c, 0) for c in cands1 if c not in ("c13", "c22"))
        w.writerow([*k, x["total"], y["total"], y["total"] - x["total"], x["c13"], y["c13"], y["c13"] - x["c13"], x["c22"], y["c22"], y["c22"] - x["c22"],
                    outros, x["branco"] + x["nulo"], y["branco"] + y["nulo"]])
print("fim", flush=True)
