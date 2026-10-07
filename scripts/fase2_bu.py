"""Fase 2b: baixa bu.dat de todas as secoes, em ordem de hr (chegada). Retomavel: pula arquivo ja existente.
Saida: dados/bu/<uf>/<mun>-<zona>-<sec>.bu  e  dados/bu_falhas.jsonl"""
import json, os, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
FALHAS = os.path.join(RAIZ, "dados", "bu_falhas.jsonl")

ult = {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j

itens = []
for k, j in ult.items():
    if j["status"] != 200:
        continue
    a = json.loads(j["aux"])
    h = a["hashes"][-1]
    nome = next((x["nm"] for x in h["arq"] if x["tp"] == "bu"), None)
    if not nome:
        continue
    t = datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S")
    itens.append((t, k, h["hash"], nome))
itens.sort()


def destino(k):
    uf, mu, zo, ns = k
    return os.path.join(RAIZ, "dados", "bu", uf, f"{mu}-{zo}-{ns}.bu")


pend = [i for i in itens if not os.path.exists(destino(i[1]))]
print("total:", len(itens), "| pendentes:", len(pend), flush=True)


def pega(i):
    _, k, hsh, nome = i
    uf, mu, zo, ns = k
    u = f"{B}/{uf}/{mu}/{zo}/{ns}/{hsh}/{nome}"
    st = 0
    for n in range(5):
        try:
            r = urllib.request.urlopen(u, timeout=40)
            return k, 200, r.read()
        except urllib.error.HTTPError as e:
            st = e.code
        except Exception:
            st = -1
        time.sleep(5 * (2 ** n))
    return k, st, None


n = ok = 0
with open(FALHAS, "a", encoding="utf-8") as fl, ThreadPoolExecutor(10) as ex:
    for k, st, corpo in ex.map(pega, pend):
        n += 1
        if st == 200:
            d = destino(k)
            os.makedirs(os.path.dirname(d), exist_ok=True)
            open(d, "wb").write(corpo)
            ok += 1
        else:
            fl.write(json.dumps({"chave": k, "status": st}) + "\n")
            fl.flush()
        if n % 5000 == 0:
            print(n, ok, time.strftime("%H:%M:%S"), flush=True)
print("fim", n, ok, flush=True)
