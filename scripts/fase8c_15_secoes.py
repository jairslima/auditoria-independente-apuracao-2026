"""Fase 8c: inclui as 15 secoes (Betim/MG zona 319 e Carapicuiba/SP zona 388) publicadas pelo TSE depois da coleta principal.
Le o BU (parser BER proprio), verifica a cadeia de hashes e acrescenta as linhas em dados/votos_secao.csv e dados/cadeia_secao.csv."""
import csv, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_parser import parse_bu
from bu_cadeia import verifica_cadeia, RAIZ

ja = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8"))}
cab = next(csv.reader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")))
cands = [c for c in cab if c.startswith("c") and c not in ("cand",)]
aux = {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] == 200:
        aux[(j["uf"], j["mun"], j["zona"], j["sec"])] = json.loads(j["aux"])
novas = [tuple(k) for k in json.load(open(os.path.join(RAIZ, "dados/secoes_sem_bu.json"))) if tuple(k) not in ja]
print("secoes a incluir:", len(novas))
lv, lc, tot = [], [], {}
for k in novas:
    caminho = os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu")
    if not os.path.exists(caminho):
        print("  ainda sem BU:", k); continue
    raw = open(caminho, "rb").read()
    r = parse_bu(raw); p = r["pres"]
    h = aux[k]["hashes"][-1]
    v = [p.get(int(c[1:]), 0) for c in cands]
    br, nu = p.get("branco", 0), p.get("nulo", 0)
    lv.append([*k, h["dr"] + " " + h["hr"], hashlib.sha256(raw).hexdigest(), r["ts_bu"][0]] + v + [br, nu, sum(v) + br + nu])
    c = verifica_cadeia(raw)
    f = next(x for x in c["finais"] if x[0] == 6257)
    lc.append([k[0], f"{k[1]}-{k[2]}-{k[3]}.bu", c["n_tuplas"], c["erros_tupla"], c["erros_ordem"], c["erros_final"], f[1], f[2], json.dumps({str(a): b for a, b in p.items()}, sort_keys=True), ""])
    print(" ", k, "tuplas", c["n_tuplas"], "erros(tupla/ordem/final):", c["erros_tupla"], c["erros_ordem"], c["erros_final"], "| Flavio", p.get(22), "Lula", p.get(13))
    for cc, vv in p.items(): tot[cc] = tot.get(cc, 0) + vv
with open(os.path.join(RAIZ, "dados/votos_secao.csv"), "a", newline="", encoding="utf-8") as f: csv.writer(f).writerows(lv)
with open(os.path.join(RAIZ, "dados/cadeia_secao.csv"), "a", newline="", encoding="utf-8") as f: csv.writer(f).writerows(lc)
print("votos nas 15 secoes (Presidente):", {str(k): v for k, v in sorted(tot.items(), key=lambda x: -x[1])[:5]}, "| incluidas:", len(lv))
