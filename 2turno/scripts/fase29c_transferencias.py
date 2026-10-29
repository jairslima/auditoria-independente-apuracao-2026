# -*- coding: utf-8 -*-
"""Fase 29c: estimativa de transferencia de votos do 1o para o 2o turno por regressao ecologica (Goodman), seção a seção.
Unidade: cada secao com BU nos dois turnos (499.207). Variaveis, como fracao dos eleitores aptos da secao:
  1o turno (9 categorias): Lula, Flavio, Cury, Renan Santos, Caiado, Zema, outros candidatos, brancos+nulos, abstencao.
  2o turno (4 destinos): Lula, Flavio, brancos+nulos, abstencao.
Para cada destino: y = soma_c beta_c * x_c (sem intercepto, pois as categorias somam 1), minimos quadrados ponderados pelo numero de aptos.
beta_c e a fracao dos eleitores da categoria c do 1o turno que o modelo atribui a cada destino. Intervalos: bootstrap por municipio (300 sorteios).
LIMITE: e um indicio estatistico. Pressupoe que eleitores da mesma categoria se comportam do mesmo jeito em todas as secoes do grupo; isso falha quando
o perfil da secao muda tanto a categoria quanto o destino (falacia ecologica). Os intervalos nao cobrem esse erro de modelo. Nao e prova de como cada eleitor votou.
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/artefato/transferencias.json e resultados/fase29c_transferencias.csv"""
import csv, json, os
from collections import defaultdict
import numpy as np

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE1 = os.path.join(os.path.dirname(RAIZ), "AuditoriaPresidente2026", "dados")
T1, T2 = os.path.join(BASE1, "votos_secao.csv"), os.path.join(RAIZ, "dados", "votos_secao.csv")
CAD = os.path.join(BASE1, "externos", "eleitorado_local_votacao_2026_BRASIL.csv")
OUT = os.path.join(RAIZ, "resultados")
CAT = ["Lula (13)", "Flávio Bolsonaro (22)", "Augusto Cury (70)", "Renan Santos (14)", "Ronaldo Caiado (55)", "Zema (30)", "Outros candidatos", "Brancos e nulos", "Abstenção"]
DEST = ["Lula (13)", "Flávio Bolsonaro (22)", "Brancos e nulos", "Abstenção"]
REG = {"N": ["ac", "am", "ap", "pa", "ro", "rr", "to"], "NE": ["al", "ba", "ce", "ma", "pb", "pe", "pi", "rn", "se"], "CO": ["df", "go", "ms", "mt"],
       "SE": ["es", "mg", "rj", "sp"], "S": ["pr", "rs", "sc"], "EX": ["zz"]}
NOME_REG = {"N": "Norte", "NE": "Nordeste", "CO": "Centro-Oeste", "SE": "Sudeste", "S": "Sul", "EX": "Exterior"}
B = 300
rng = np.random.default_rng(2026)

# 1) aptos por secao com BU (principal + agregadas), eleicao federal
apt = defaultdict(int)
with open(CAD, encoding="latin-1", newline="") as f:
    rd = csv.reader(f, delimiter=";")
    h = next(rd)
    h = [x.strip('"') for x in h]
    iU, iM, iZ, iS, iP, iQ, iT = (h.index(c) for c in ("SG_UF", "CD_MUNICIPIO", "NR_ZONA", "NR_SECAO", "NR_SECAO_PRINCIPAL", "QT_ELEITOR_ELEICAO_FEDERAL", "NR_TURNO"))
    for r in rd:
        # o arquivo traz uma linha por secao e por turno (identicas); a linha da secao principal ja inclui as agregadas
        if r[iT].strip('"') != "1" or r[iP].strip() not in ("-1", ""):
            continue
        apt[(r[iU].lower(), r[iM].zfill(5), r[iZ].zfill(4), r[iS].zfill(4))] += int(r[iQ])


def le(p):
    d = {}
    for r in csv.DictReader(open(p, encoding="utf-8")):
        d[(r["uf"], r["mun"], r["zona"], r["sec"])] = r
    return d


a, b = le(T1), le(T2)
chaves = sorted(set(a) & set(b))
tot_apt = sum(apt.get(k, 0) for k in chaves)
print("secoes:", len(chaves), "| aptos somados nas secoes com BU:", tot_apt, "(referencia do 1o turno: 158.745.079)", flush=True)
pequenos = [c for c in a[chaves[0]] if c.startswith("c") and c not in ("c13", "c22", "c70", "c14", "c55", "c30")]
mx = defaultdict(list)
for k in chaves:
    ap = apt.get(k, 0)
    x, y = a[k], b[k]
    comp1, comp2 = int(x["total"]), int(y["total"])
    if ap <= 0 or comp1 > ap or comp2 > ap:
        continue
    cats = [int(x["c13"]), int(x["c22"]), int(x["c70"]), int(x["c14"]), int(x["c55"]), int(x["c30"]), sum(int(x[c]) for c in pequenos),
            int(x["branco"]) + int(x["nulo"]), ap - comp1]
    dst = [int(y["c13"]), int(y["c22"]), int(y["branco"]) + int(y["nulo"]), ap - comp2]
    mx[(k[0], k[1])].append([ap] + cats + dst)
print("secoes usadas na regressao:", sum(len(v) for v in mx.values()), flush=True)

# 2) estatisticas suficientes por municipio
mun_ids, A, Bm, SY, SYY, SW, TC = [], [], [], [], [], [], []
for key, rows in mx.items():
    M = np.array(rows, dtype=float)
    w = M[:, 0]
    X = M[:, 1:10] / w[:, None]
    Y = M[:, 10:14] / w[:, None]
    mun_ids.append(key)
    A.append((X * w[:, None]).T @ X)
    Bm.append((X * w[:, None]).T @ Y)
    SY.append((Y * w[:, None]).sum(0))
    SYY.append((Y * Y * w[:, None]).sum(0))
    SW.append(w.sum())
    TC.append(M[:, 1:10].sum(0))
A, Bm, SY, SYY, SW, TC = (np.array(v) for v in (A, Bm, SY, SYY, SW, TC))
ufs_m = np.array([k[0] for k in mun_ids])


def ajusta(idx):
    beta = np.linalg.lstsq(A[idx].sum(0), Bm[idx].sum(0), rcond=None)[0]
    return beta


def grupo(sel):
    idx = np.where(sel)[0]
    if len(idx) < 3:
        return None
    beta = ajusta(idx)
    bs = np.empty((B, 9, 4))
    for i in range(B):
        bs[i] = ajusta(rng.choice(idx, size=len(idx), replace=True))
    lo, hi = np.percentile(bs, 2.5, axis=0), np.percentile(bs, 97.5, axis=0)
    sw, sy, syy = SW[idx].sum(), SY[idx].sum(0), SYY[idx].sum(0)
    ssr = syy - 2 * np.einsum("cd,cd->d", beta, Bm[idx].sum(0)) + np.einsum("cd,ce,ed->d", beta, A[idx].sum(0), beta)
    sst = syy - sy * sy / sw
    r2 = 1 - ssr / sst
    T = TC[idx].sum(0)
    return {"municipios": int(len(idx)), "secoes": int(sum(len(mx[mun_ids[i]]) for i in idx)), "T1": T.round().astype(int).tolist(),
            "beta": beta.round(4).tolist(), "lo": lo.round(4).tolist(), "hi": hi.round(4).tolist(), "r2": r2.round(3).tolist(),
            "votos": (beta * T[:, None]).round().astype(int).tolist()}


res = {"categorias": CAT, "destinos": DEST, "aviso": "Indício estatístico por regressão ecológica; não prova como cada eleitor votou.", "bootstrap": B, "semente": 2026}
res["nac"] = grupo(np.ones(len(mun_ids), dtype=bool))
res["regioes"] = {r: dict(nome=NOME_REG[r], **g) for r, ufl in REG.items() if (g := grupo(np.isin(ufs_m, ufl))) is not None}
res["ufs"] = {u: g for u in sorted(set(ufs_m)) if (g := grupo(ufs_m == u)) is not None}
os.makedirs(os.path.join(OUT, "artefato"), exist_ok=True)
json.dump(res, open(os.path.join(OUT, "artefato", "transferencias.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
with open(os.path.join(OUT, "fase29c_transferencias.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["nivel", "grupo", "categoria_1o_turno", "destino_2o_turno", "fracao_estimada", "ic95_inferior", "ic95_superior", "votos_implicados", "eleitores_da_categoria_1o_turno", "r2_do_destino"])
    def linhas(nivel, nome, g):
        for c in range(9):
            for d in range(4):
                w.writerow([nivel, nome, CAT[c], DEST[d], g["beta"][c][d], g["lo"][c][d], g["hi"][c][d], g["votos"][c][d], g["T1"][c], g["r2"][d]])
    linhas("Brasil", "Brasil", res["nac"])
    for r, g in res["regioes"].items(): linhas("Região", g["nome"], g)
    for u, g in res["ufs"].items(): linhas("UF", u.upper(), g)
n = res["nac"]
print("R2 (Lula2, Flavio2, BN2, Abst2):", n["r2"])
print("Brasil, fracao de cada categoria do 1o turno que vai a cada destino (Lula2, Flavio2, BN2, Abst2):")
for c in range(9):
    print(f"  {CAT[c]:24s}", n["beta"][c], "IC95%", n["lo"][c], n["hi"][c])
print("votos implicados:")
for c in range(9):
    print(f"  {CAT[c]:24s}", n["votos"][c], "total da categoria:", n["T1"][c])
print("soma por destino (deve ser igual ao 2o turno):", [sum(n["votos"][c][d] for c in range(9)) for d in range(4)])
