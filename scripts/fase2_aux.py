"""Fase 2a: baixa o aux.json de TODAS as secoes instaladas. Retomavel (pula o que ja esta no jsonl).
Saida: dados/aux.jsonl (uma linha por secao: uf, mun, zona, secao, status http, corpo json bruto)."""
import glob, json, os, sys, time, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
SAIDA = os.path.join(RAIZ, "dados", "aux.jsonl")

feitos = set()
if os.path.exists(SAIDA):
    for l in open(SAIDA, encoding="utf-8"):
        try:
            j = json.loads(l)
            if j["status"] == 200:
                feitos.add((j["uf"], j["mun"], j["zona"], j["sec"]))
        except Exception:
            pass

secs = []
for f in sorted(glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json"))):
    d = json.load(open(f, encoding="utf-8"))
    uf = d["abr"][0]["cd"]
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" in s and (uf, m["cd"], z["cd"], s["ns"]) not in feitos:
                    secs.append((uf, m["cd"], z["cd"], s["ns"]))
print("a baixar:", len(secs), "| ja feitos:", len(feitos), flush=True)


def pega(t):
    uf, mu, zo, ns = t
    u = f"{B}/{uf}/{mu}/{zo}/{ns}/p003220-{uf}-m{mu}-z{zo}-s{ns}-aux.json"
    st, corpo = 0, None
    for i in range(5):
        try:
            r = urllib.request.urlopen(u, timeout=30)
            return t, r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            st = e.code
            if e.code == 404:
                return t, 404, None
        except Exception:
            st = -1
        time.sleep(5 * (2 ** i))
    return t, st, None


n = 0
with open(SAIDA, "a", encoding="utf-8") as out, ThreadPoolExecutor(10) as ex:
    for t, st, corpo in ex.map(pega, secs):
        out.write(json.dumps({"uf": t[0], "mun": t[1], "zona": t[2], "sec": t[3], "status": st, "aux": corpo}, ensure_ascii=False) + "\n")
        n += 1
        if n % 5000 == 0:
            out.flush()
            print(n, time.strftime("%H:%M:%S"), flush=True)
print("fim", n, flush=True)
