"""Fase 3: parseia todos os BUs (presidente) -> dados/votos_secao.csv  (uf,mun,zona,sec,hr,hash_bu,<cands>,branco,nulo,total)."""
import csv, hashlib, json, os, sys
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_parser import parse_bu

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def trabalha(a):
    k, hr, caminho = a
    raw = open(caminho, "rb").read()
    try:
        r = parse_bu(raw)
        return k, hr, hashlib.sha256(raw).hexdigest(), r["pres"], r["ts_bu"], None
    except Exception as e:
        return k, hr, hashlib.sha256(raw).hexdigest(), None, None, repr(e)


if __name__ == "__main__":
    itens = []
    ult = {}
    for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        if j["status"] == 200 or (j["uf"], j["mun"], j["zona"], j["sec"]) not in ult:
            ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
    for j in ult.values():
        if j["status"] != 200:
            continue
        a = json.loads(j["aux"])
        h = a["hashes"][-1]
        k = (j["uf"], j["mun"], j["zona"], j["sec"])
        c = os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu")
        cb = os.path.join(RAIZ, "dados", "busa", f"{k[0]}-{k[1]}-{k[2]}-{k[3]}.busa")
        if os.path.exists(c):
            itens.append((k, h["dr"] + " " + h["hr"], c))
        elif os.path.exists(cb):
            itens.append((k, h["dr"] + " " + h["hr"], cb))  # contingencia (Sistema de Apuracao)
    print("BUs a parsear:", len(itens), flush=True)
    linhas, erros = [], []
    with ProcessPoolExecutor(8) as ex:
        for i, (k, hr, sha, pres, ts, err) in enumerate(ex.map(trabalha, itens, chunksize=500)):
            if err or pres is None:
                erros.append((k, err or "sem pres"))
                continue
            linhas.append((k, hr, sha, pres, ts))
            if i % 100000 == 0:
                print(i, flush=True)
    cands = sorted({c for *_, p, _ in linhas for c in p if isinstance(c, int)})
    with open(os.path.join(RAIZ, "dados/votos_secao.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["uf", "mun", "zona", "sec", "hr", "sha256_bu", "ts_bu"] + [f"c{c}" for c in cands] + ["branco", "nulo", "total"])
        for k, hr, sha, p, ts in linhas:
            v = [p.get(c, 0) for c in cands]
            br, nu = p.get("branco", 0), p.get("nulo", 0)
            w.writerow([*k, hr, sha, ts[0] if ts else ""] + v + [br, nu, sum(v) + br + nu])
    json.dump([[list(k), e] for k, e in erros], open(os.path.join(RAIZ, "dados/parse_erros.json"), "w"), ensure_ascii=False)
    print("ok:", len(linhas), "| erros:", len(erros), "| candidatos:", cands, flush=True)
