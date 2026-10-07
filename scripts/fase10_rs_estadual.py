"""Fase 10: soma, nos BUs do RS, os votos da eleicao estadual (6259) para Governador (cargo 3) e Senador (cargo 5)
e compara com o oficial (dados/oficial/rs-c0003|c0005-e006259-u.jws). Decodificador asn1tools + spec oficial 2026."""
import base64, glob, json, os, sys
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

CARGOS = {3: "Governador", 5: "Senador"}


def le(caminho):
    c = conv()
    bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
    out = {3: defaultdict(int), 5: defaultdict(int)}
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        if rpe["idEleicao"] != 6259:
            continue
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                if cargo not in out:
                    continue
                for vv in tvc["votosVotaveis"]:
                    t = vv["tipoVoto"]
                    k = str(vv["identificacaoVotavel"]["codigo"]) if t == 1 else {2: "branco", 3: "nulo"}.get(t, f"tipo{t}")
                    out[cargo][k] += vv["quantidadeVotos"]
    return {c: dict(v) for c, v in out.items()}


def jws(p):
    t = open(p, "rb").read().decode().split(".")[1]
    return json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))


if __name__ == "__main__":
    arqs = sorted(glob.glob(os.path.join(RAIZ, "dados/bu/rs/*.bu")) + glob.glob(os.path.join(RAIZ, "dados/busa/rs-*.busa")))
    print("BUs do RS:", len(arqs), flush=True)
    tot = {3: defaultdict(int), 5: defaultdict(int)}
    with ProcessPoolExecutor(2) as ex:
        for r in ex.map(le, arqs, chunksize=100):
            for c, d in r.items():
                for k, v in d.items():
                    tot[c][k] += v
    res = {}
    for c, nome in CARGOS.items():
        d = jws(os.path.join(RAIZ, f"dados/oficial/rs-c000{c}-e006259-u.jws"))
        of = {}
        for agr in d["carg"][0]["agr"]:
            for par in agr["par"]:
                for cd in par["cand"]:
                    of[str(cd["n"])] = (cd.get("nmu") or cd["nm"], par["sg"], int(cd["vap"]))
        linhas = []
        print(f"\n=== {nome} (RS) : soma dos BUs x oficial ===")
        tudo = True
        for k, (nm, sg, vap) in sorted(of.items(), key=lambda x: -x[1][2]):
            b = tot[c].get(k, 0)
            linhas.append((k, nm, sg, b, vap, b - vap))
            tudo &= (b == vap)
            print(f"{k:>4} {nm[:22]:22} {sg:6} BUs={b:>10,} oficial={vap:>10,} dif={b - vap:>+7,}")
        for k, chave in (("branco", "vb"), ("nulo", "vn")):
            b, o = tot[c].get(k, 0), int(d["v"][chave])
            tudo &= (b == o)
            print(f"{k:>11}        BUs={b:>10,} oficial={o:>10,} dif={b - o:>+7,}")
        extra = set(tot[c]) - set(of) - {"branco", "nulo"}
        print("votaveis nos BUs fora da lista oficial:", {k: tot[c][k] for k in extra} or "nenhum")
        print(">>> ZERO A ZERO em todos os candidatos, brancos e nulos:", tudo)
        res[nome] = {"zero_a_zero": tudo, "linhas": linhas}
    json.dump(res, open(os.path.join(RAIZ, "dados/rs_estadual_comparacao.json"), "w"), ensure_ascii=False, indent=1)
