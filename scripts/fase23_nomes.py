# -*- coding: utf-8 -*-
"""Fase 23: tabela nominal da eleicao estadual (6259): para cada UF, Governador (3 mais votados) e Senador (mais votados/eleitos),
com os votos do arquivo oficial e o resultado da conferencia contra a soma dos BUs (fase 18: dados/estadual/<uf>.json).
Autoria: Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase23_candidatos_por_uf.csv e .md"""
import csv, json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import RAIZ
from fase15_mg_sp import jws, B

UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn ro rr sc sp se to".split()


def cands(d):
    out = []
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            for c in par["cand"]:
                out.append({"nome": c.get("nmu") or c["nm"], "n": c["n"], "partido": par["sg"], "votos": int(c["vap"]), "pct": c["pvap"], "situacao": c["st"]})
    return sorted(out, key=lambda x: -x["votos"])


linhas = []
for uf in UFS:
    conf = json.load(open(os.path.join(RAIZ, "dados", "estadual", f"{uf}.json"), encoding="latin1"))
    ok = {c["cargo"]: c.get("zero_a_zero_candidatos_brancos_nulos") for c in conf["cargos"]}
    for cargo, cod, n in (("Governador", 3, 3), ("Senador", 5, 3)):
        d = jws(f"{B}/6259/dados/{uf}/{uf}-c000{cod}-e006259-u.jws")
        if d is None:
            continue
        for i, c in enumerate(cands(d)[:n], 1):
            linhas.append({"UF": uf.upper(), "cargo": cargo, "posicao": i, "candidato": c["nome"], "numero": c["n"], "partido": c["partido"],
                           "votos_oficial": c["votos"], "percentual": c["pct"], "situacao": c["situacao"],
                           "soma_BUs_igual_ao_oficial_em_todos_os_candidatos_da_UF_neste_cargo": "sim" if ok.get(cargo) else "NAO"})
    print(uf, flush=True)

with open(os.path.join(RAIZ, "resultados", "fase23_candidatos_por_uf.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";")
    w.writeheader()
    w.writerows(linhas)

with open(os.path.join(RAIZ, "resultados", "fase23_candidatos_por_uf.md"), "w", encoding="utf-8") as f:
    for cargo in ("Governador", "Senador"):
        f.write(f"\n**{cargo} (três mais votados por UF; votos do arquivo oficial; soma dos BUs igual em todos os candidatos da UF: {'sim' if all(l['soma_BUs_igual_ao_oficial_em_todos_os_candidatos_da_UF_neste_cargo']=='sim' for l in linhas if l['cargo']==cargo) else 'NAO em alguma UF'})**\n\n")
        f.write("| UF | 1º | 2º | 3º |\n|---|---|---|---|\n")
        for uf in UFS:
            ls = [l for l in linhas if l["UF"] == uf.upper() and l["cargo"] == cargo]
            cel = " | ".join(f"{l['candidato']} ({l['partido']}) {l['votos_oficial']:,}".replace(",", ".") for l in ls)
            f.write(f"| {uf.upper()} | {cel} |\n")
print("linhas:", len(linhas))
