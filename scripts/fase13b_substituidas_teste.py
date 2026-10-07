"""Fase 13b: (1) comparecimento das urnas substituidas (tipoUrna 4) e RED (tipoArquivo 2) vs. secoes vizinhas da mesma zona;
(2) eleitores aptos do BU vs. cadastro independente (principal + agregadas)."""
import csv, glob, json, math, os, random
from collections import defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
csv.field_size_limit(10**7)
rows = []
for r in csv.DictReader(open(os.path.join(RAIZ, "dados/urnas_tipo.csv"), encoding="utf-8")):
    if r["erro"] or not r["aptos_6257"] or int(r["aptos_6257"]) == 0:
        continue
    mun, zon, sec = r["arquivo"].rsplit(".", 1)[0].split("-")[-3:]
    rows.append({"uf": r["uf"], "k": (r["uf"], mun, zon, sec), "zona": (r["uf"], mun, zon), "tu": r["tipoUrna"], "ta": r["tipoArquivo"],
                 "apt": int(r["aptos_6257"]), "comp": int(r["comparecimento_6257"] or 0)})
print("secoes com aptos > 0:", len(rows))
por_zona = defaultdict(list)
for r in rows:
    por_zona[r["zona"]].append(r)


def teste(nome, sel):
    difs, pesos = [], []
    for z, lst in por_zona.items():
        alvo = [r for r in lst if sel(r)]
        ref = [r for r in lst if r["tu"] == "1" and r["ta"] == "1"]
        if not alvo or len(ref) < 5:
            continue
        t_ref = sum(r["comp"] for r in ref) / sum(r["apt"] for r in ref)
        for r in alvo:
            difs.append(r["comp"] / r["apt"] - t_ref)
            pesos.append(r["apt"])
    n = len(difs)
    if not n:
        print(nome, "sem dados"); return
    m = sum(difs) / n
    sd = math.sqrt(sum((d - m) ** 2 for d in difs) / max(n - 1, 1))
    se = sd / math.sqrt(n)
    ta = sum(r["comp"] for r in rows if sel(r)) / sum(r["apt"] for r in rows if sel(r))
    print(f"{nome}: n={n:,} | comparecimento medio do grupo {ta * 100:.2f}% | diferenca media vs. seccoes vizinhas da mesma zona: {m * 100:+.2f} pp (erro padrao {se * 100:.2f} pp; IC95% {100 * (m - 1.96 * se):+.2f} a {100 * (m + 1.96 * se):+.2f})")
    return m, se, n


teste("Urna substituida (tipoUrna=4, contingencia que virou secao)", lambda r: r["tu"] == "4")
teste("RED (tipoArquivo=2, dados recuperados da urna original)", lambda r: r["ta"] == "2")
teste("Sistema de Apuracao (tipoArquivo 4 ou 5)", lambda r: r["ta"] in ("4", "5"))
# controle: grupo aleatorio do mesmo tamanho de secoes normais (deve dar ~0)
rnd = random.Random(2026)
normais = [r for r in rows if r["tu"] == "1" and r["ta"] == "1"]
amostra = set(id(r) for r in rnd.sample(normais, 3033))
teste("CONTROLE: 3.033 secoes normais sorteadas (deve dar ~0)", lambda r: id(r) in amostra)

# (2) aptos do BU vs cadastro
cad = {}
with open(os.path.join(RAIZ, "dados/externos/eleitorado_local_votacao_2026_BRASIL.csv"), encoding="latin-1", newline="") as f:
    for c in csv.DictReader(f, delimiter=";"):
        k = (c["SG_UF"].lower(), c["CD_MUNICIPIO"].zfill(5), c["NR_ZONA"].zfill(4), c["NR_SECAO"].zfill(4))
        cad[k] = (c["DS_TIPO_SECAO_AGREGADA"], c["NR_SECAO_PRINCIPAL"].zfill(4) if c["NR_SECAO_PRINCIPAL"] not in ("-1", "") else None, int(c["QT_ELEITOR_ELEICAO_FEDERAL"] or 0))
soma_princ = defaultdict(int)
for k, (tp, pr, q) in cad.items():
    if tp == "Principal":
        soma_princ[k] += q
    elif pr:
        soma_princ[(k[0], k[1], k[2], pr)] += q
iguais = difer = sem = 0
dif_ex = []
for r in rows:
    if r["k"] not in soma_princ:
        sem += 1; continue
    if soma_princ[r["k"]] == r["apt"]:
        iguais += 1
    else:
        difer += 1
        if len(dif_ex) < 8:
            dif_ex.append((r["k"], r["apt"], soma_princ[r["k"]]))
print(f"\naptos do BU x cadastro (principal + agregadas): iguais {iguais:,} | diferentes {difer:,} | sem correspondencia {sem}")
for e in dif_ex: print("   dif:", e)

# detalhe das diferencas de aptos
import collections
ds = []
for r in rows:
    if r["k"] in soma_princ:
        ds.append((r["apt"] - soma_princ[r["k"]], r))
tot_bu = sum(r["apt"] for _, r in ds)
tot_cad = sum(soma_princ[r["k"]] for _, r in ds)
print(f"\nsoma de aptos nos BUs: {tot_bu:,} | soma no cadastro (mesmas secoes): {tot_cad:,} | diferenca liquida: {tot_bu - tot_cad:+,}")
nz = [d for d, _ in ds if d != 0]
print(f"secoes com diferenca: {len(nz):,} | media |dif|: {sum(abs(d) for d in nz) / max(len(nz), 1):.2f} | |dif|<=3: {sum(1 for d in nz if abs(d) <= 3):,} ({sum(1 for d in nz if abs(d) <= 3) / max(len(nz), 1) * 100:.1f}%) | |dif|>10: {sum(1 for d in nz if abs(d) > 10):,}")
print("sinal: BU maior que cadastro:", sum(1 for d in nz if d > 0), "| BU menor:", sum(1 for d in nz if d < 0))
maiores = sorted(ds, key=lambda x: -abs(x[0]))[:6]
for d, r in maiores: print("   maior dif:", r["k"], "BU", r["apt"], "cadastro", soma_princ[r["k"]], "tipoUrna", r["tu"], "tipoArq", r["ta"])
for nome, sel in (("urna substituida", lambda r: r["tu"] == "4"), ("normal", lambda r: r["tu"] == "1" and r["ta"] == "1")):
    g = [d for d, r in ds if sel(r)]
    print(f"   {nome}: {sum(1 for d in g if d != 0) / len(g) * 100:.1f}% das secoes com diferenca de aptos")

# distribuicao (nao so a media) da diferenca de comparecimento: urna substituida x controle
def difs_grupo(sel):
    out = []
    for z, lst in por_zona.items():
        alvo = [r for r in lst if sel(r)]
        ref = [r for r in lst if r["tu"] == "1" and r["ta"] == "1" and not sel(r)]
        if not alvo or len(ref) < 5: continue
        t_ref = sum(r["comp"] for r in ref) / sum(r["apt"] for r in ref)
        out += [(r["comp"] / r["apt"] - t_ref) * 100 for r in alvo]
    return sorted(out)
def pct(v, p): return v[int(p * (len(v) - 1))]
for nome, sel in (("URNA SUBSTITUIDA", lambda r: r["tu"] == "4"), ("CONTROLE (3.033 normais)", lambda r: id(r) in amostra)):
    v = difs_grupo(sel)
    print(f"\n{nome}: n={len(v):,} | percentis da diferenca (pp): p1 {pct(v,.01):+.1f} | p5 {pct(v,.05):+.1f} | p25 {pct(v,.25):+.1f} | mediana {pct(v,.5):+.1f} | p75 {pct(v,.75):+.1f} | p95 {pct(v,.95):+.1f}")
    print(f"   com deficit > 10 pp: {sum(1 for x in v if x < -10):,} ({sum(1 for x in v if x < -10)/len(v)*100:.1f}%) | > 20 pp: {sum(1 for x in v if x < -20):,} | > 40 pp: {sum(1 for x in v if x < -40):,}")
