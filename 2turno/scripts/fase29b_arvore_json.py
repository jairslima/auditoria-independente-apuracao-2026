# -*- coding: utf-8 -*-
"""Fase 29b: monta o JSON da comparacao 1o x 2o turno de Presidente em arvore (Brasil, regiao, UF, municipio) para o artefato do relatorio.
Cada no traz, para o 1o turno, [comparecimento, Lula, Flavio, outros candidatos, brancos, nulos] e, para o 2o, [comparecimento, Lula, Flavio, brancos, nulos].
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/artefato/dados_turnos.json"""
import csv, glob, json, os
from collections import defaultdict
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
T1 = os.path.join(os.path.dirname(RAIZ), "AuditoriaPresidente2026", "dados", "votos_secao.csv")
T2 = os.path.join(RAIZ, "dados", "votos_secao.csv")
OUT = os.path.join(RAIZ, "resultados", "artefato")
os.makedirs(OUT, exist_ok=True)
NOME_UF = {"ac": "Acre", "al": "Alagoas", "am": "Amazonas", "ap": "Amapá", "ba": "Bahia", "ce": "Ceará", "df": "Distrito Federal", "es": "Espírito Santo",
           "go": "Goiás", "ma": "Maranhão", "mg": "Minas Gerais", "ms": "Mato Grosso do Sul", "mt": "Mato Grosso", "pa": "Pará", "pb": "Paraíba",
           "pe": "Pernambuco", "pi": "Piauí", "pr": "Paraná", "rj": "Rio de Janeiro", "rn": "Rio Grande do Norte", "ro": "Rondônia", "rr": "Roraima",
           "rs": "Rio Grande do Sul", "sc": "Santa Catarina", "se": "Sergipe", "sp": "São Paulo", "to": "Tocantins", "zz": "Exterior"}
REGIOES = [("N", "Norte", ["ac", "am", "ap", "pa", "ro", "rr", "to"]), ("NE", "Nordeste", ["al", "ba", "ce", "ma", "pb", "pe", "pi", "rn", "se"]),
           ("CO", "Centro-Oeste", ["df", "go", "ms", "mt"]), ("SE", "Sudeste", ["es", "mg", "rj", "sp"]), ("S", "Sul", ["pr", "rs", "sc"]), ("EX", "Exterior", ["zz"])]
ROT_CAND = {"c13": "Lula", "c22": "Flávio Bolsonaro", "c70": "Augusto Cury", "c14": "Renan Santos", "c55": "Ronaldo Caiado", "c30": "Zema",
            "c80": "Samara Martins", "c16": "Hertz Dias", "c27": "Clariana Zacarkim", "c21": "Edmilson Costa", "c29": "Rui Costa Pimenta", "c35": "Wilson Grassi",
            "c28": "Candidato 28 (nulo técnico)"}

nomes = {}
for f in glob.glob(os.path.join(RAIZ, "dados", "cs", "*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    for m in json.load(open(f, encoding="utf-8"))["abr"][0]["mu"]:
        nomes[(uf, m["cd"])] = m["nm"]

mun1 = defaultdict(lambda: defaultdict(int))
mun2 = defaultdict(lambda: defaultdict(int))
uf_c1 = defaultdict(lambda: defaultdict(int))
for r in csv.DictReader(open(T1, encoding="utf-8")):
    k = (r["uf"], r["mun"])
    cs = {c: int(v) for c, v in r.items() if c.startswith("c")}
    x = mun1[k]
    x["comp"] += int(r["total"]); x["lula"] += cs["c13"]; x["flavio"] += cs["c22"]
    x["outros"] += sum(v for c, v in cs.items() if c not in ("c13", "c22"))
    x["branco"] += int(r["branco"]); x["nulo"] += int(r["nulo"])
    for c, v in cs.items():
        uf_c1[r["uf"]][c] += v
for r in csv.DictReader(open(T2, encoding="utf-8")):
    k = (r["uf"], r["mun"])
    x = mun2[k]
    x["comp"] += int(r["total"]); x["lula"] += int(r["c13"]); x["flavio"] += int(r["c22"]); x["branco"] += int(r["branco"]); x["nulo"] += int(r["nulo"])


def v1(x): return [x["comp"], x["lula"], x["flavio"], x["outros"], x["branco"], x["nulo"]]
def v2(x): return [x["comp"], x["lula"], x["flavio"], x["branco"], x["nulo"]]


ufs, muns = {}, {}
for uf in NOME_UF:
    a, b = defaultdict(int), defaultdict(int)
    lista = []
    for (u, m) in sorted(k for k in mun1 if k[0] == uf):
        for c in a.keys() | mun1[(u, m)].keys():
            a[c] += mun1[(u, m)][c] if c in mun1[(u, m)] else 0
        for c in mun2[(u, m)]:
            b[c] += mun2[(u, m)][c]
        lista.append([m, nomes.get((u, m), m), v1(mun1[(u, m)]), v2(mun2[(u, m)])])
    ufs[uf] = {"nome": NOME_UF[uf], "t1": v1(a), "t2": v2(b), "c1": {ROT_CAND.get(c, c): v for c, v in uf_c1[uf].items()}}
    muns[uf] = lista
curva = []
for r in csv.DictReader(open(os.path.join(os.path.dirname(RAIZ), "AuditoriaPresidente2026", "segundo_turno", "dados_monitor", "curva_oficial.csv"), encoding="utf-8"), delimiter=";"):
    t = datetime.strptime(r["utc_consulta"], "%Y-%m-%dT%H:%M:%SZ") - timedelta(hours=3)
    curva.append([round((t - datetime(2026, 10, 25, 16, 0, 0)).total_seconds() / 60, 1), float(r["pct_secoes"].replace(",", ".")), int(r["secoes_totalizadas"])])
out = {"gerado": datetime.now().strftime("%d/%m/%Y"), "regioes": [{"id": i, "nome": n, "ufs": u} for i, n, u in REGIOES], "ufs": ufs, "mun": muns, "curva": curva,
       "rotulos_c1": ROT_CAND}
json.dump(out, open(os.path.join(OUT, "dados_turnos.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
n = sum(len(v) for v in muns.values())
print("municipios/postos:", n, "| tamanho:", os.path.getsize(os.path.join(OUT, "dados_turnos.json")), "bytes")
