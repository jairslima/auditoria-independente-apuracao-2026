"""Fase 11: teste de controle do metodo em UFs e cargos SORTEADOS (semente fixa 2026), fora do RS.
Sorteia N UFs (exceto rs e zz) e, para cada UF, K cargos entre Governador(3), Senador(5), Dep. Federal(6) e Dep. Estadual(7;
no DF o cargo equivalente e Dep. Distrital, codigo 8). Soma nos BUs (decodificador oficial asn1tools, spec 2026) todos os
votaveis desses cargos e compara com o oficial (6259/dados/<uf>/<uf>-c000X-e006259-u.jws): cada candidato, brancos, nulos e
total de legenda. Grava dados/aleatorio_sorteio.json (o sorteio) e dados/aleatorio_resultado.json (tudo, para auditoria)."""
import base64, glob, json, os, random, sys, urllib.request
from collections import defaultdict
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn ro rr sc sp se to".split()
NOMES = {3: "Governador", 5: "Senador", 6: "Deputado Federal", 7: "Deputado Estadual", 8: "Deputado Distrital"}
N_UF, K_CARGOS, SEED = int(os.environ.get("N_UF", 8)), 2, 2026


def le(caminho):
    c = conv()
    bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
    out = defaultdict(int)
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        if rpe["idEleicao"] != 6259:
            continue
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                for vv in tvc["votosVotaveis"]:
                    t = vv["tipoVoto"]
                    if t == 1:
                        k = (cargo, "cand", str(vv["identificacaoVotavel"]["codigo"]))
                    elif t == 4:
                        k = (cargo, "legenda", "total")
                    else:
                        k = (cargo, {2: "branco", 3: "nulo"}.get(t, f"tipo{t}"), "total")
                    out[k] += vv["quantidadeVotos"]
    return dict(out)


def oficial(uf, cargo):
    u = f"https://resultados.tse.jus.br/oficial/ele2026/6259/dados/{uf}/{uf}-c000{cargo}-e006259-u.jws"
    try:
        t = urllib.request.urlopen(u, timeout=60).read().decode().split(".")[1]
    except Exception:
        return None
    d = json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))
    cands = {}
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            for cd in par["cand"]:
                cands[str(cd["n"])] = (cd.get("nmu") or cd["nm"], par["sg"], int(cd["vap"]))
    v = d["v"]
    return {"cands": cands, "branco": int(v["vb"]), "nulo": int(v["vn"]), "legenda": int(v.get("vl", 0) or 0), "gerado": f"{d['dg']} {d['hg']}",
            "secoes": f"{d['s']['st']}/{d['s']['ts']}"}


if __name__ == "__main__":
    rnd = random.Random(SEED)
    ufs = rnd.sample(UFS, N_UF)
    sorteio = []
    for uf in ufs:
        pool = [3, 5, 6, 8 if uf == "df" else 7]
        sorteio.append({"uf": uf, "cargos": rnd.sample(pool, K_CARGOS)})
    json.dump({"semente": SEED, "ufs_sorteadas": ufs, "sorteio": sorteio}, open(os.path.join(RAIZ, "dados/aleatorio_sorteio.json"), "w"), indent=1)
    print("SORTEIO:", sorteio, flush=True)
    resultado = []
    for s in sorteio:
        uf = s["uf"]
        arqs = sorted(glob.glob(os.path.join(RAIZ, f"dados/bu/{uf}/*.bu")) + glob.glob(os.path.join(RAIZ, f"dados/busa/{uf}-*.busa")))
        print(f"\n### {uf.upper()}: {len(arqs)} BUs ...", flush=True)
        tot = defaultdict(int)
        with ProcessPoolExecutor(2) as ex:
            for r in ex.map(le, arqs, chunksize=100):
                for k, v in r.items():
                    tot[k] += v
        for cargo in s["cargos"]:
            of = oficial(uf, cargo)
            if of is None:
                print(f"  {uf} {NOMES[cargo]}: oficial indisponivel", flush=True)
                continue
            iguais, difs = 0, []
            for n, (nm, sg, vap) in of["cands"].items():
                b = tot.get((cargo, "cand", n), 0)
                if b == vap:
                    iguais += 1
                else:
                    difs.append((n, nm, sg, b, vap, b - vap))
            extras = {k[2]: v for k, v in tot.items() if k[0] == cargo and k[1] == "cand" and k[2] not in of["cands"]}
            outros = {}
            for rotulo in ("branco", "nulo", "legenda"):
                b = tot.get((cargo, rotulo, "total"), 0)
                outros[rotulo] = (b, of[rotulo], b - of[rotulo])
            ok_tudo = (not difs) and all(x[2] == 0 for x in outros.values())
            sample = rnd.sample(sorted(of["cands"].items(), key=lambda x: -x[1][2]), min(5, len(of["cands"])))
            amostra = [(n, nm, sg, tot.get((cargo, "cand", n), 0), vap) for n, (nm, sg, vap) in sample]
            resultado.append({"uf": uf, "cargo": cargo, "nome": NOMES[cargo], "n_cand_oficial": len(of["cands"]), "iguais": iguais, "divergentes": difs,
                              "votaveis_fora_da_lista_oficial": extras, "brancos_nulos_legenda": outros, "zero_a_zero": ok_tudo, "amostra_aleatoria": amostra,
                              "oficial_gerado": of["gerado"], "secoes_oficial": of["secoes"], "n_bus": len(arqs)})
            print(f"  {uf.upper()} {NOMES[cargo]}: {iguais}/{len(of['cands'])} candidatos iguais | brancos {outros['branco'][2]:+d} nulos {outros['nulo'][2]:+d} legenda {outros['legenda'][2]:+d} | ZERO A ZERO: {ok_tudo}", flush=True)
            for a in amostra:
                print(f"      amostra: n={a[0]} {a[1][:24]:24} {a[2]:10} BUs={a[3]:>9,} oficial={a[4]:>9,} {'OK' if a[3]==a[4] else 'DIFERE'}", flush=True)
            for d_ in difs[:8]:
                print(f"      DIVERGE: n={d_[0]} {d_[1][:24]} BUs={d_[3]:,} oficial={d_[4]:,} dif={d_[5]:+,}", flush=True)
    json.dump(resultado, open(os.path.join(RAIZ, "dados/aleatorio_resultado.json"), "w"), ensure_ascii=False, indent=1)
    print("\nRESUMO: pares UF/cargo:", len(resultado), "| zero a zero:", sum(1 for r in resultado if r["zero_a_zero"]), flush=True)
