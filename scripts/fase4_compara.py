"""Fase 4: soma dos BUs vs. total oficial (BR e UFs) + calibracao do painel congelado 19:06:33."""
import base64, csv, json, os
from collections import defaultdict
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def jws(p):
    t = open(p, "rb").read().decode().split(".")[1]
    return json.loads(base64.urlsafe_b64decode(t + "=" * (-len(t) % 4)))


def oficial(uf):
    d = jws(os.path.join(RAIZ, f"dados/oficial/{uf}-c0001-e006257-u.jws"))
    out = {}
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            for c in par["cand"]:
                out[int(c["n"])] = int(c["vap"])
    # outras formas (federacao)
    for fed in d["carg"][0].get("fed", []):
        pass
    return out, d


rows = list(csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")))
cands = [c for c in rows[0].keys() if c.startswith("c")]
tot = defaultdict(lambda: defaultdict(int))
for r in rows:
    for c in cands:
        tot[r["uf"]][int(c[1:])] += int(r[c])
        tot["br"][int(c[1:])] += int(r[c])
    tot[r["uf"]]["branco"] += int(r["branco"]); tot["br"]["branco"] += int(r["branco"])
    tot[r["uf"]]["nulo"] += int(r["nulo"]); tot["br"]["nulo"] += int(r["nulo"])

print("=== BRASIL: soma dos BUs x oficial (candidatos) ===")
of, d = oficial("br")
print("oficial gerado em", d["dg"], d["hg"])
tudo_ok = True
for c in sorted(of):
    a = tot["br"].get(c, 0)
    print(f"cand {c:>3}: BUs={a:>11,} oficial={of[c]:>11,} dif={a - of[c]:>+9,}")
    tudo_ok &= a == of[c]
print("BR candidatos batem integralmente:", tudo_ok)

print("\n=== por UF (candidatos): dif total absoluta ===")
for uf in sorted(k for k in tot if k != "br"):
    try:
        o, _ = oficial(uf)
    except Exception as e:
        print(uf, "sem oficial", e); continue
    dif = {c: tot[uf].get(c, 0) - o[c] for c in o if tot[uf].get(c, 0) != o[c]}
    print(uf, "OK" if not dif else f"DIVERGE {dif}")

print("\n=== calibracao painel 19:06:33 (323.539 secoes; Flavio 37.566.895; Lula 32.007.853) ===")
pts = sorted(((datetime.strptime(r["hr"], "%d/%m/%Y %H:%M:%S"), r) for r in rows), key=lambda x: x[0])
ac = defaultdict(int)
melhor = None
for i, (t, r) in enumerate(pts, 1):
    for c in cands:
        ac[c] += int(r[c])
    if i == 323539:
        print(f"na secao #323539 (hr={t}): Flavio(c22)={ac['c22']:,} Lula(c13)={ac['c13']:,}")
    if ac["c22"] >= 37566895 and melhor is None:
        melhor = (i, t, dict(ac))
print("primeira secao em que Flavio >= 37.566.895:", melhor[0] if melhor else None, melhor[1] if melhor else None)
if melhor:
    print("  Lula nesse ponto:", melhor[2]["c13"])
