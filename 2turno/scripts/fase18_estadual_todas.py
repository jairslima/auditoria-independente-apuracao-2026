"""Fase 18: eleicao ESTADUAL (6259) completa: Governador(3), Senador(5), Dep.Federal(6), Dep.Estadual(7; DF: Distrital 8) em TODAS as 27 UFs,
mais Governador POR MUNICIPIO no pais inteiro. Uma UF por vez (retomavel: dados/estadual/<uf>.json).
Diferencas de legenda sao classificadas automaticamente: 'explicada' se bate com tval de partido 'Anulado sub judice' ou com os nulos tecnicos (vnt)."""
import glob, json, os, sys, time
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import RAIZ
from fase15_mg_sp import le, jws, B

UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn ro rr sc sp se to".split()
NOMES = {3: "Governador", 5: "Senador", 6: "Deputado Federal", 7: "Deputado Estadual", 8: "Deputado Distrital"}
PROCS = int(os.environ.get("PROCS", 4))
PASTA = os.path.join(RAIZ, "dados", "estadual")
os.makedirs(PASTA, exist_ok=True)


def oficial(d):
    cands, partidos = {}, {}
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            partidos[str(par["n"])] = {"tvtl": int(par.get("tvtl") or 0), "tval": int(par.get("tval") or 0), "dvt": par.get("dvt")}
            for cd in par["cand"]:
                cands[str(cd["n"])] = int(cd["vap"])
    v = d["v"]
    return cands, partidos, {"branco": int(v["vb"]), "nulo": int(v["vn"]), "legenda": int(v.get("vl", 0) or 0), "vnt": int(v.get("vnt", 0) or 0)}


def compara_cargo(uf, cargo, tot):
    d = jws(f"{B}/6259/dados/{uf}/{uf}-c000{cargo}-e006259-u.jws")
    if d is None:
        return {"cargo": NOMES[cargo], "erro": "oficial indisponivel"}
    cands, partidos, o = oficial(d)
    dif_c = [(n, tot.get((cargo, "cand", n), 0), v) for n, v in cands.items() if tot.get((cargo, "cand", n), 0) != v]
    bn = {k: (tot.get((cargo, k, "total"), 0), o[k]) for k in ("branco", "nulo") if tot.get((cargo, k, "total"), 0) != o[k]}
    extras_nom = sum(v for (c, k, n), v in tot.items() if c == cargo and k == "cand" and n not in cands)
    # legenda por partido: BU x (tvtl). Explicacao: tval do partido (anulado sub judice) ou partido sem lista (vai para nulos tecnicos)
    leg_bu = {p: v for (c, k, p), v in tot.items() if c == cargo and k == "legenda" and p != "total"}
    sem_expl, expl_tval, so_bu = {}, {}, 0
    for p in set(leg_bu) | set(partidos):
        b, of = leg_bu.get(p, 0), partidos.get(p, {"tvtl": 0, "tval": 0})
        if b == of["tvtl"]:
            continue
        if p in partidos and b == of["tval"]:
            expl_tval[p] = b
        elif p not in partidos:
            so_bu += b
        else:
            sem_expl[p] = (b, of["tvtl"], of["tval"])
    nulos_tec_ok = (extras_nom + so_bu == o["vnt"])
    return {"cargo": NOMES[cargo], "candidatos": len(cands), "candidatos_divergentes": dif_c, "brancos_nulos_divergentes": bn,
            "legenda_explicada_tval": expl_tval, "legenda_so_nos_BUs_para_nulos_tecnicos": so_bu, "legenda_sem_explicacao": sem_expl,
            "nulos_tecnicos": {"oficial": o["vnt"], "bu_nominais_fora_da_lista": extras_nom, "bu_legenda_partido_sem_lista": so_bu, "bate": nulos_tec_ok},
            "zero_a_zero_candidatos_brancos_nulos": (not dif_c) and (not bn)}


def gov_municipal(uf, m, mt):
    d = jws(f"{B}/6259/dados/{uf}/{uf}{m}-c0003-e006259-u.jws")
    if d is None:
        return m, "indisponivel"
    cands, _, o = oficial(d)
    dif = [(n, mt.get((6259, 3, "cand", n), 0), v) for n, v in cands.items() if mt.get((6259, 3, "cand", n), 0) != v]
    dbn = {k: (mt.get((6259, 3, k, "total"), 0), o[k]) for k in ("branco", "nulo") if mt.get((6259, 3, k, "total"), 0) != o[k]}
    return m, ("igual" if not dif and not dbn else {"cand": dif, "bn": dbn})


if __name__ == "__main__":
    alvo = sys.argv[1:] or UFS
    for uf in alvo:
        saida = os.path.join(PASTA, f"{uf}.json")
        if os.path.exists(saida):
            print(f"{uf.upper()}: ja feito, pulando", flush=True); continue
        arqs = sorted(glob.glob(os.path.join(RAIZ, f"dados/bu/{uf}/*.bu")) + glob.glob(os.path.join(RAIZ, f"dados/busa/{uf}-*.busa")))
        t0 = time.time()
        tot, mt = defaultdict(int), defaultdict(lambda: defaultdict(int))
        with ProcessPoolExecutor(PROCS) as ex:
            for mun, ut, mu in ex.map(le, arqs, chunksize=100):
                for k, v in ut.items():
                    tot[k] += v
                for k, v in mu.items():
                    mt[mun][k] += v
        res = {"uf": uf, "n_bus": len(arqs), "cargos": []}
        for cargo in (3, 5, 6, 8 if uf == "df" else 7):
            res["cargos"].append(compara_cargo(uf, cargo, tot))
        with ThreadPoolExecutor(5) as ex:
            gm = dict(ex.map(lambda m: gov_municipal(uf, m, mt[m]), sorted(mt)))
        res["gov_municipios"] = {"total": len(gm), "iguais": sum(1 for v in gm.values() if v == "igual"), "nao_iguais": {m: v for m, v in gm.items() if v != "igual"}}
        json.dump(res, open(saida, "w", encoding="utf-8"), ensure_ascii=False)
        linhas = []
        for c in res["cargos"]:
            if "erro" in c:
                linhas.append(f"{c['cargo']}: {c['erro']}"); continue
            linhas.append(f"{c['cargo']}: {c['candidatos'] - len(c['candidatos_divergentes'])}/{c['candidatos']} cand" + ("" if c["zero_a_zero_candidatos_brancos_nulos"] else " DIVERGE")
                          + (f" | legenda tval {sum(c['legenda_explicada_tval'].values())}" if c["legenda_explicada_tval"] else "")
                          + (f" | legenda->nulos tec {c['legenda_so_nos_BUs_para_nulos_tecnicos']}" if c["legenda_so_nos_BUs_para_nulos_tecnicos"] else "")
                          + (f" | SEM EXPLICACAO {c['legenda_sem_explicacao']}" if c["legenda_sem_explicacao"] else ""))
        print(f"{uf.upper()} ({len(arqs)} BUs, {time.time() - t0:.0f}s) | Gov municipios {res['gov_municipios']['iguais']}/{res['gov_municipios']['total']} | " + " | ".join(linhas), flush=True)
    print("FIM", flush=True)
