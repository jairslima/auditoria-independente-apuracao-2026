"""Fase 19: RDV (registro digital do voto, voto a voto, embaralhado) contra o BU da MESMA secao, todos os cargos das duas eleicoes.
Mapeamento RDV->BU: nominal(2,digitacao N)->candidato N; legenda(1,digitacao P)->legenda do partido P; branco(3,5)->brancos; nulos(4,6,7,8,9)->nulos.
Amostra: as mesmas 20.811 secoes da fase 16 (20.000 sorteadas + 68 que deram 404 + 743 da cauda). Saida: dados/rdv_vs_bu.csv"""
import csv, json, os, sys, time
from collections import Counter
from concurrent.futures import ProcessPoolExecutor
import asn1tools

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv as conv_bu, RAIZ
import fase9_assinaturas as f9

SAIDA = os.path.join(RAIZ, "dados", "rdv_vs_bu.csv")
CAMPOS = ["uf", "mun", "zona", "sec", "grupo", "status", "n_comparacoes", "n_dif", "detalhe", "erro"]
_RDV = None


def rdv_conv():
    global _RDV
    if _RDV is None:
        _RDV = asn1tools.compile_files([os.path.join(RAIZ, "docs_tse", "spec2026", "spec", "rdv.asn1")], codec="ber", numeric_enums=True)
    return _RDV


def norm(x):
    try:
        return str(int(x))
    except Exception:
        return str(x)


def contagem_rdv(raw):
    ent = rdv_conv().decode("EntidadeResultadoRDV", bytearray(raw))
    tipo, eleicoes = ent["rdv"]["eleicoes"]
    out = {}
    for e in eleicoes:
        for vc in e["votosCargos"]:
            cargo = vc["idCargo"][1]
            c = Counter()
            for v in vc["votos"]:
                t = v["tipoVoto"]
                if t == 2:
                    c[("cand", norm(v["digitacao"]))] += 1
                elif t == 1:
                    c[("legenda", norm(str(v["digitacao"])[:2]))] += 1   # numero de candidato inexistente conta para o partido (2 primeiros digitos)
                elif t in (3, 5):
                    c[("branco", "t")] += 1
                else:
                    c[("nulo", "t")] += 1
            out[(e["idEleicao"], cargo)] = c
    return out


def contagem_bu(caminho):
    c = conv_bu()
    bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
    out = {}
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                cnt = Counter()
                for vv in tvc["votosVotaveis"]:
                    t, q = vv["tipoVoto"], vv["quantidadeVotos"]
                    if not q:
                        continue
                    if t == 1:
                        cnt[("cand", norm(vv["identificacaoVotavel"]["codigo"]))] += q
                    elif t == 4:
                        cnt[("legenda", norm(vv["identificacaoVotavel"]["partido"]))] += q
                    elif t == 2:
                        cnt[("branco", "t")] += q
                    elif t == 3:
                        cnt[("nulo", "t")] += q
                out[(rpe["idEleicao"], cargo)] = cnt
    return out


def trabalha(a):
    k, url, grupo = a
    base = {"uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "grupo": grupo, "status": "", "n_comparacoes": "", "n_dif": "", "detalhe": "", "erro": ""}
    try:
        raw = f9.baixa(url)
        if raw is None:
            base["status"] = "sem_rdv"; return base
        r = contagem_rdv(raw)
        b = contagem_bu(os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu"))
        difs, n = [], 0
        for chave in sorted(set(r) | set(b)):
            n += 1
            rc, bc = r.get(chave, Counter()), b.get(chave, Counter())
            if {x: v for x, v in rc.items() if v} != {x: v for x, v in bc.items() if v}:
                dd = {str(x): (rc.get(x, 0), bc.get(x, 0)) for x in set(rc) | set(bc) if rc.get(x, 0) != bc.get(x, 0)}
                difs.append(f"{chave}:{dd}")
        base.update(status="ok" if not difs else "DIVERGE", n_comparacoes=n, n_dif=len(difs), detalhe=" | ".join(difs)[:600])
    except Exception as e:
        base.update(status="erro", erro=repr(e)[:160])
    return base


if __name__ == "__main__":
    ult = {}
    for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        if j["status"] == 200 or (j["uf"], j["mun"], j["zona"], j["sec"]) not in ult:
            ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
    plano = [(r["uf"], r["mun"], r["zona"], r["sec"], r["grupo"]) for r in csv.DictReader(open(os.path.join(RAIZ, "dados/assinaturas_estadual.csv"), encoding="utf-8"))]
    feitos = set()
    if os.path.exists(SAIDA):
        for r in csv.DictReader(open(SAIDA, encoding="utf-8")):
            feitos.add((r["uf"], r["mun"], r["zona"], r["sec"]))
    itens = []
    for uf, mun, zon, sec, grupo in plano:
        k = (uf, mun, zon, sec)
        if k in feitos or k not in ult or ult[k]["status"] != 200:
            continue
        a = json.loads(ult[k]["aux"]); h = a["hashes"][-1]
        rdv = next((x["nm"] for x in h["arq"] if x["tp"] == "rdv"), None)
        if rdv:
            itens.append((k, f"{f9.B}/{uf}/{mun}/{zon}/{sec}/{h['hash']}/{rdv}", grupo))
    print(f"secoes na amostra: {len(plano)} | a fazer: {len(itens)}", flush=True)
    novo = not os.path.exists(SAIDA)
    n = ok = 0
    with ProcessPoolExecutor(int(os.environ.get("PROCS", 4))) as ex, open(SAIDA, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        for r in ex.map(trabalha, itens, chunksize=10):
            w.writerow(r); n += 1; ok += 1 if r["status"] == "ok" else 0
            if n % 1000 == 0:
                f.flush(); print(n, "iguais:", ok, time.strftime("%H:%M:%S"), flush=True)
    print("fim", n, "iguais:", ok, flush=True)
