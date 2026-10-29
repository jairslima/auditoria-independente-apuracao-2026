"""Fase 2c: baixa o busa.dat das secoes sem BU (Sistema de Apuracao). Auditoria Independente da Apuracao 2026 by Jair Lima."""
import json, os, urllib.request
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados"
os.makedirs(os.path.join(RAIZ, "dados", "busa"), exist_ok=True)
ult = {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l); ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
ok = 0
for k, j in ult.items():
    h = json.loads(j["aux"])["hashes"][-1]
    if any(x["tp"] == "bu" for x in h["arq"]):
        continue
    nome = next((x["nm"] for x in h["arq"] if x["tp"] == "busa"), None)
    if not nome:
        print("SEM busa:", k); continue
    u = f"{B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{nome}"
    d = os.path.join(RAIZ, "dados", "busa", f"{k[0]}-{k[1]}-{k[2]}-{k[3]}.busa")
    try:
        c = urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "auditoria-presidente-2026/1.0"}), timeout=60).read()
        open(d, "wb").write(c); ok += 1
    except Exception as e:
        print("FALHA", k, e)
print("busa baixados:", ok)
