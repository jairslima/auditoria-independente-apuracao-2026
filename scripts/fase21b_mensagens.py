# -*- coding: utf-8 -*-
"""Fase 21b: compara a presenca de cada tipo de mensagem do log da urna entre as secoes do anexo LAI e o controle.
Autoria: Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, os, re, zipfile, collections, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(RAIZ, "dados", "log")
R = list(csv.DictReader(open(os.path.join(RAIZ, "resultados", "fase21_logs.csv"), encoding="utf-8-sig"), delimiter=";"))
RE_T = re.compile(r"^(\d\d/\d\d/\d{4} \d\d:\d\d:\d\d)\t(\w+)\t(\d+)\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")

def grupo(r):
    m = r["motivo"]
    if r["grupo"] == "controle": return "controle"
    if "busa" in m: return "sist_apuracao"
    if "404" in m: return "atrasadas68"
    return "dia_seguinte"

def norm(s):
    s = re.sub(r"\[[^\]]*\]", "[X]", s)
    return re.sub(r"\d+", "N", s)[:110]

pres = collections.defaultdict(lambda: collections.Counter()); tot = collections.Counter()
for r in R:
    k = (r["UF"].lower(), r["mun"], r["zona"], r["secao"]); g = grupo(r); tot[g] += 1
    z = zipfile.ZipFile(os.path.join(LOG, "-".join(k) + ".jez"))
    ms = set()
    for x in z.read(z.namelist()[0]).decode("latin1").splitlines():
        e = RE_T.match(x)
        if e: ms.add((e.group(4), e.group(2), norm(e.group(5))))
    for m in ms: pres[m][g] += 1
print(tot)
linhas = []
for m, c in pres.items():
    pc = c["controle"] / tot["controle"]
    for g in ("dia_seguinte", "atrasadas68", "sist_apuracao"):
        pg = c[g] / tot[g]
        if abs(pg - pc) > 0.15:
            linhas.append((abs(pg - pc), g, round(pg, 2), round(pc, 2), m))
for l in sorted([x for x in linhas if x[1]!="sist_apuracao"], reverse=True)[:30]: print(l)
