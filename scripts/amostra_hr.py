"""Calibracao 2: amostra aleatoria (semente fixa) de secoes; le hr/dr do aux.json e estima fracao ate 19:06:33."""
import glob, json, os, random, urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
secs = []
for f in sorted(glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json"))):
    d = json.load(open(f, encoding="utf-8"))
    uf = d["abr"][0]["cd"]
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" in s:
                    secs.append((uf, m["cd"], z["cd"], s["ns"]))
random.seed(2026)
amostra = random.sample(secs, 2000)


def pega(t):
    uf, mu, zo, ns = t
    u = f"{B}/{uf}/{mu}/{zo}/{ns}/p003220-{uf}-m{mu}-z{zo}-s{ns}-aux.json"
    for _ in range(3):
        try:
            return t, json.loads(urllib.request.urlopen(u, timeout=30).read().decode("utf-8"))
        except Exception:
            pass
    return t, None


with ThreadPoolExecutor(16) as ex:
    res = list(ex.map(pega, amostra))
ok = [(t, a) for t, a in res if a]
print("baixadas:", len(ok), "de", len(amostra))
n_hash = [len(a["hashes"]) for t, a in ok]
print("secoes com >1 hash (reenvio):", sum(1 for n in n_hash if n > 1))
hrs = []
for t, a in ok:
    h = a["hashes"][-1]
    hrs.append(datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S"))
lim = datetime(2026, 10, 4, 19, 6, 33)
print("fracao hr <= 19:06:33:", round(sum(1 for h in hrs if h <= lim) / len(hrs), 4), "(painel: 0.6481)")
print("min/max hr:", min(hrs), max(hrs))
