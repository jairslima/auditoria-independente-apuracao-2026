"""Fase 15: auditoria de MG e SP (UFs com arquivos publicados com atraso).
(1) Nivel UF: Governador(3), Senador(5), Dep.Federal(6), Dep.Estadual(7): cada candidato, brancos, nulos, legenda total e legenda POR PARTIDO.
(2) Nivel MUNICIPIO: TODOS os municipios de MG e SP, Presidente (6257) e Governador (6259): candidatos, brancos, nulos.
Soma nos BUs (asn1tools + spec oficial 2026) e compara com os .jws oficiais (UF e municipio). Saida: dados/mg_sp_resultado.json e impressao."""
import base64, glob, json, os, sys, time, urllib.request
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

B = "https://resultados.tse.jus.br/oficial/ele2026"
NOMES = {1: "Presidente", 3: "Governador", 5: "Senador", 6: "Deputado Federal", 7: "Deputado Estadual"}


def le(caminho):
    c = conv()
    partes = os.path.basename(caminho).rsplit(".", 1)[0].split("-")
    mun = partes[-3]
    bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
    uf_tot, mun_tot = defaultdict(int), defaultdict(int)
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        ele = rpe["idEleicao"]
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                for vv in tvc["votosVotaveis"]:
                    t, q = vv["tipoVoto"], vv["quantidadeVotos"]
                    if t == 1:
                        k = (cargo, "cand", str(vv["identificacaoVotavel"]["codigo"]))
                    elif t == 4:
                        k = (cargo, "legenda", str(vv["identificacaoVotavel"]["partido"]))
                        uf_tot[(cargo, "legenda", "total")] += q
                    else:
                        k = (cargo, {2: "branco", 3: "nulo"}.get(t, f"tipo{t}"), "total")
                    uf_tot[k] += q
                    if (ele, cargo) in ((6257, 1), (6259, 3)):
                        mun_tot[(ele, cargo) + k[1:]] += q
    return mun, dict(uf_tot), dict(mun_tot)


def jws(url):
    for _ in range(4):
        try:
            t = urllib.request.urlopen(url, timeout=60).read().decode().split(".")[1]
            return json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))
        except Exception:
            time.sleep(2)
    return None


def oficial_cargo(d):
    cands, leg_part = {}, {}
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            leg_part[str(par["n"])] = int(par.get("tvtl") or 0)
            for cd in par["cand"]:
                cands[str(cd["n"])] = int(cd["vap"])
    v = d["v"]
    return cands, {"branco": int(v["vb"]), "nulo": int(v["vn"]), "legenda": int(v.get("vl", 0) or 0)}, leg_part, int(v.get("vnt", 0) or 0)


if __name__ == "__main__":
    out = {}
    for uf in ("mg", "sp"):
        arqs = sorted(glob.glob(os.path.join(RAIZ, f"dados/bu/{uf}/*.bu")) + glob.glob(os.path.join(RAIZ, f"dados/busa/{uf}-*.busa")))
        print(f"\n##### {uf.upper()}: {len(arqs)} BUs", flush=True)
        tot = defaultdict(int)
        mt = defaultdict(lambda: defaultdict(int))
        t0 = time.time()
        with ProcessPoolExecutor(5) as ex:
            for i, (mun, ut, mu) in enumerate(ex.map(le, arqs, chunksize=100)):
                for k, v in ut.items():
                    tot[k] += v
                for k, v in mu.items():
                    mt[mun][k] += v
                if i % 20000 == 0:
                    print("  ", i, f"{time.time() - t0:.0f}s", flush=True)
        res = {"uf": {}, "municipios": {}}
        # --- nivel UF
        for cargo in (3, 5, 6, 7):
            d = jws(f"{B}/6259/dados/{uf}/{uf}-c000{cargo}-e006259-u.jws")
            cands, outros, leg_part, vnt = oficial_cargo(d)
            difs = [(n, tot.get((cargo, "cand", n), 0), vap) for n, vap in cands.items() if tot.get((cargo, "cand", n), 0) != vap]
            dout = {k: (tot.get((cargo, k, "total"), 0), o) for k, o in outros.items() if tot.get((cargo, k, "total"), 0) != o}
            dleg = {p: (tot.get((cargo, "legenda", p), 0), o) for p, o in leg_part.items() if tot.get((cargo, "legenda", p), 0) != o}
            bu_so = {p: v for (c2, k2, p), v in tot.items() if c2 == cargo and k2 == "legenda" and p != "total" and p not in leg_part and v}
            extras_nom = {n: v for (c2, k2, n), v in tot.items() if c2 == cargo and k2 == "cand" and n not in cands and v}
            exc_leg = {p: tot.get((cargo, "legenda", p), 0) - leg_part.get(p, 0) for p in set(p for (c2, k2, p) in tot if c2 == cargo and k2 == "legenda" and p != "total")}
            exc_leg = {p: x for p, x in exc_leg.items() if x > 0}
            ntec = sum(extras_nom.values()) + sum(exc_leg.values())
            print(f"     nulos tecnicos: oficial vnt={vnt:,} | BUs: nominais fora da lista {sum(extras_nom.values()):,} + legenda a mais {sum(exc_leg.values()):,} ({exc_leg or '-'}) = {ntec:,} -> {'BATE' if ntec == vnt else 'NAO BATE'}", flush=True)
            res["uf"][NOMES[cargo]] = {"vnt_oficial": vnt, "nominais_fora_da_lista": extras_nom, "legenda_a_mais": exc_leg, "nulos_tecnicos_batem": ntec == vnt,"candidatos": len(cands), "candidatos_divergentes": difs, "brancos_nulos_legenda_divergentes": dout,
                                       "legenda_por_partido_divergente": dleg, "legenda_so_nos_BUs": bu_so}
            print(f"  {uf.upper()} {NOMES[cargo]}: {len(cands) - len(difs)}/{len(cands)} candidatos iguais | brancos/nulos/legenda divergentes: {dout or 'nenhum'} | legenda por partido divergente: {dleg or 'nenhum'} | legenda so nos BUs: {bu_so or 'nenhuma'}", flush=True)
        # --- nivel municipio (todos)
        muns = sorted(mt)
        def comp(m):
            r = {}
            for ele, cargo, cod in ((6257, 1, "c0001"), (6259, 3, "c0003")):
                d = jws(f"{B}/{ele}/dados/{uf}/{uf}{m}-{cod}-e00{ele}-u.jws")
                if d is None:
                    r[NOMES[cargo]] = "oficial indisponivel"; continue
                cands, outros, _, _ = oficial_cargo(d)
                dif = [(n, mt[m].get((ele, cargo, "cand", n), 0), vap) for n, vap in cands.items() if mt[m].get((ele, cargo, "cand", n), 0) != vap]
                dout = {k: (mt[m].get((ele, cargo, k, "total"), 0), o) for k, o in outros.items() if k != "legenda" and mt[m].get((ele, cargo, k, "total"), 0) != o}
                r[NOMES[cargo]] = {"n": len(cands), "dif": dif, "outros": dout}
            return m, r
        with ThreadPoolExecutor(8) as ex:
            for m, r in ex.map(comp, muns):
                res["municipios"][m] = r
        for cargo in ("Presidente", "Governador"):
            ok = sum(1 for r in res["municipios"].values() if isinstance(r[cargo], dict) and not r[cargo]["dif"] and not r[cargo]["outros"])
            bad = [m for m, r in res["municipios"].items() if not isinstance(r[cargo], dict) or r[cargo]["dif"] or r[cargo]["outros"]]
            print(f"  {uf.upper()} municipios {cargo}: {ok}/{len(muns)} iguais ao oficial (candidatos, brancos, nulos) | divergentes: {bad[:10] or 'nenhum'}", flush=True)
        out[uf] = res
    json.dump(out, open(os.path.join(RAIZ, "dados/mg_sp_resultado.json"), "w"), ensure_ascii=False, indent=1)
    print("\nFIM", flush=True)
