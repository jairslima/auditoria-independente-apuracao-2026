"""Fase 12b: detalhe dos atrasos. (1) cauda >23:41 por municipio/zona + hora de emissao do BU na urna; (2) 'Recebida' por zona;
(3) defasagem entre a emissao do BU na urna e o registro (hr) no TSE, em amostra aleatoria e nos grupos de interesse."""
import glob, json, os, random, sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

fmt = "%d/%m/%Y %H:%M:%S"
rec, st = {}, {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] == 200:
        a = json.loads(j["aux"]); h = a["hashes"][-1]
        k = (j["uf"], j["mun"], j["zona"], j["sec"])
        rec[k] = datetime.strptime(h["dr"] + " " + h["hr"], fmt); st[k] = h.get("st") if a.get("st") == "Totalizada" else a.get("st")
nomes, tam_zona = {}, Counter()
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    d = json.load(open(f, encoding="utf-8"))
    for m in d["abr"][0]["mu"]:
        nomes[(uf, m["cd"])] = m["nm"]
        for z in m["zon"]:
            tam_zona[(uf, m["cd"], z["cd"])] = sum(1 for s in z["sec"] if "da" in s)
C = conv()


def emissao(k):
    p = os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu")
    if not os.path.exists(p):
        return None
    bu = C.decode("EntidadeBoletimUrna", C.decode("EntidadeEnvelopeGenerico", bytearray(open(p, "rb").read()))["conteudo"])
    return datetime.strptime(bu["dataHoraEmissao"], "%Y%m%dT%H%M%S")


def resumo(titulo, ks):
    print(f"\n--- {titulo}: {len(ks)} secoes")
    g = defaultdict(list)
    for k in ks:
        g[(k[0], k[1], k[2])].append(k)
    for z, v in sorted(g.items(), key=lambda x: -len(x[1]))[:8]:
        hs = sorted(rec[k] for k in v)
        em = [e for e in (emissao(k) for k in v[:40]) if e]
        em_s = f"urna emitiu o BU entre {min(em).strftime('%H:%M')} e {max(em).strftime('%H:%M')}" if em else "?"
        print(f"{z[0]} {nomes.get((z[0], z[1]), z[1])[:22]:22} zona {z[2]} | {len(v):>4} de {tam_zona[z]} secoes da zona | registrado {hs[0].strftime('%d %H:%M')}..{hs[-1].strftime('%d %H:%M')} | {em_s}")


L = datetime(2026, 10, 4, 23, 41)
resumo("CAUDA: registro depois de 23:41 de 04/10", [k for k, t in rec.items() if t > L])
resumo("STATUS 'Recebida'", [k for k, s in st.items() if s == "Recebida"])

print("\n--- Defasagem (registro no TSE menos emissao do BU na urna), amostra aleatoria de 3.000 secoes (semente 2026)")
ks = sorted(rec)
random.Random(2026).shuffle(ks)
d = []
for k in ks[:3000]:
    e = emissao(k)
    if e:
        d.append((rec[k] - e).total_seconds() / 60)
d.sort()
q = lambda p: d[int(p * (len(d) - 1))]
print(f"n={len(d)} | mediana {q(.5):.0f} min | p90 {q(.9):.0f} | p99 {q(.99):.0f} | max {d[-1]:.0f} min | >2h: {sum(1 for x in d if x > 120)}")
for nome, ks2 in (("grupo 404 (68)", [k for k in rec if (k[0], k[1], k[2]) in {('mg', '41335', '0316'), ('mg', '41335', '0319'), ('mg', '53716', '0269'), ('mg', '54038', '0279'), ('sp', '63134', '0388')}])):
    dd = sorted((rec[k] - e).total_seconds() / 60 for k in ks2 if (e := emissao(k)))
    print(f"{nome}: n={len(dd)} | mediana {dd[len(dd) // 2]:.0f} min | max {dd[-1]:.0f} min")
