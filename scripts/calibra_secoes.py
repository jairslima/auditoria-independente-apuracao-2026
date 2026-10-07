"""Teste de calibracao 1: contagem de secoes por hora de chegada (cs.json) vs. painel (323.539 as 19h06min33s)."""
import base64, glob, json, os
from collections import Counter
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jws(p):
    t = open(p, "rb").read().decode().split(".")[1]
    return json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))


chegadas = []
por_uf = Counter()
sem_hora = Counter()
for f in sorted(glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json"))):
    d = json.load(open(f, encoding="utf-8"))
    uf = d["abr"][0]["cd"]
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" not in s:
                    sem_hora[uf] += 1
                    continue
                chegadas.append(datetime.strptime(s["da"] + " " + s["ha"], "%d/%m/%Y %H:%M:%S"))
                por_uf[uf] += 1
print("secoes SEM da/ha (sem BU recebido):", sum(sem_hora.values()), dict(sem_hora))
print("total de secoes COM hora:", len(chegadas), "| UFs:", len(por_uf))
br = jws(os.path.join(RAIZ, "dados/oficial/br-c0001-e006257-u.jws"))
print("oficial BR: gerado", br["dg"], br["hg"], "| secoes totalizadas st/ts:", {k: br.get(k) for k in ("s", "st", "ts", "e", "esae")})
print("chaves do JWS BR:", [k for k in br.keys()][:40])
for hh in ["19:05:00", "19:06:33", "19:06:34", "19:10:00", "19:57:00", "20:00:00", "21:00:00"]:
    lim = datetime.strptime("04/10/2026 " + hh, "%d/%m/%Y %H:%M:%S")
    print(hh, sum(1 for c in chegadas if c <= lim))
print("primeira chegada:", min(chegadas), "| ultima:", max(chegadas))
