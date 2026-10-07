"""Fase 17: soma dos BUs x arquivo oficial POR MUNICIPIO (Presidente, eleicao 6257) para os 5.757 municipios/postos.
Baixa dados/<uf>/<uf><mun>-c0001-e006257-u.jws (cache em dados/oficial_mun/), compara e gera relatorio_web/municipios.json."""
import base64, csv, glob, json, os, sys, time, urllib.request, urllib.error
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/6257/dados"
CACHE = os.path.join(RAIZ, "dados", "oficial_mun")
os.makedirs(CACHE, exist_ok=True)
CANDS = [13, 22, 70, 14, 55, 30, 80, 16, 27, 21, 29, 35]          # ordem de exibicao: Lula, Flavio, Cury, Renan, Caiado, Zema, ...
# 1) soma dos BUs por (uf, mun)
bu = defaultdict(lambda: defaultdict(int))
for r in csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")):
    k = (r["uf"], r["mun"])
    bu[k]["secoes"] += 1
    for c in CANDS + [28]:
        bu[k][f"c{c}"] += int(r[f"c{c}"])
    bu[k]["branco"] += int(r["branco"]); bu[k]["nulo"] += int(r["nulo"])
# 2) nomes
nomes = {}
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    for m in json.load(open(f, encoding="utf-8"))["abr"][0]["mu"]:
        nomes[(uf, m["cd"])] = m["nm"]
print("municipios:", len(nomes), "| com BUs:", len(bu), flush=True)


def baixa(k):
    uf, mun = k
    p = os.path.join(CACHE, f"{uf}{mun}.jws")
    if os.path.exists(p) and os.path.getsize(p) > 500:
        return k, open(p, "rb").read().decode()
    url = f"{B}/{uf}/{uf}{mun}-c0001-e006257-u.jws"
    for i in range(6):
        try:
            t = urllib.request.urlopen(url, timeout=60).read().decode()
            open(p, "wb").write(t.encode())
            return k, t
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return k, None
        except Exception:
            pass
        time.sleep(3 * (2 ** i))
    return k, None


saida, bons, ruins = [], 0, []
with ThreadPoolExecutor(8) as ex:
    for i, (k, t) in enumerate(ex.map(baixa, sorted(nomes))):
        b = bu.get(k, {})
        if t is None:
            saida.append({"uf": k[0], "m": k[1], "n": nomes[k], "s": b.get("secoes", 0), "ok": None}); ruins.append(k); continue
        d = json.loads(base64.urlsafe_b64decode(t.split(".")[1] + "=" * (-len(t.split(".")[1]) % 4)))
        of = {int(c["n"]): int(c["vap"]) for a in d["carg"][0]["agr"] for p in a["par"] for c in p["cand"]}
        v = d["v"]
        bu_l = [b.get(f"c{c}", 0) for c in CANDS]
        of_l = [of.get(c, 0) for c in CANDS]
        extras = {"vb": int(v["vb"]), "vn": int(v["vn"]), "vnt": int(v.get("vnt", 0) or 0)}
        igual = (bu_l == of_l and b.get("branco", 0) == extras["vb"] and b.get("nulo", 0) == extras["vn"] and b.get("c28", 0) == extras["vnt"])
        bons += igual
        if not igual:
            ruins.append(k)
        saida.append({"uf": k[0], "m": k[1], "n": nomes[k], "s": b.get("secoes", 0), "ok": bool(igual),
                      "bu": bu_l + [b.get("branco", 0), b.get("nulo", 0), b.get("c28", 0)],
                      "of": of_l + [extras["vb"], extras["vn"], extras["vnt"]]})
        if i % 1000 == 0:
            print(i, flush=True)
print(f"iguais ao oficial: {bons} de {len(saida)} | nao iguais ou indisponiveis: {len(ruins)} {ruins[:10]}", flush=True)
out = {"candidatos": CANDS, "rotulos": ["Lula", "Flávio Bolsonaro", "Augusto Cury", "Renan Santos", "Ronaldo Caiado", "Zema", "Samara Martins", "Hertz Dias", "Clariana Zacarkim", "Edmilson Costa", "Rui Costa Pimenta", "Wilson Grassi"],
       "numeros": CANDS, "gerado": time.strftime("%d/%m/%Y"), "n_ok": bons, "n_total": len(saida), "dados": saida}
json.dump(out, open(os.path.join(RAIZ, "relatorio_web", "municipios.json"), "w", encoding="utf-8"), ensure_ascii=False, separators=(",", ":"))
print("tamanho json:", os.path.getsize(os.path.join(RAIZ, "relatorio_web", "municipios.json")), "bytes", flush=True)
