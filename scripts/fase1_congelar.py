"""Fase 1: congela totais oficiais (presidente) e indices de secoes (-cs.json) de todas as UFs.
Grava cada arquivo bruto + manifesto SHA-256 com carimbo UTC. Auditoria Presidente 2026."""
import hashlib, json, os, sys, time, urllib.request
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial"
MANIFESTO = os.path.join(RAIZ, "dados", "manifesto_fase1.jsonl")


def baixa(url, destino):
    req = urllib.request.Request(url, headers={"User-Agent": "auditoria-presidente-2026/1.0"})
    for t in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                corpo = r.read()
                return r.status, corpo
        except Exception as e:
            err = e
            time.sleep(2 * (t + 1))
    return getattr(err, "code", 0), b""


def registra(url, destino, status, corpo):
    os.makedirs(os.path.dirname(destino), exist_ok=True)
    if corpo:
        open(destino, "wb").write(corpo)
    with open(MANIFESTO, "a", encoding="utf-8") as m:
        m.write(json.dumps({
            "utc": datetime.now(timezone.utc).isoformat(), "url": url, "arquivo": os.path.relpath(destino, RAIZ),
            "status": status, "bytes": len(corpo), "sha256": hashlib.sha256(corpo).hexdigest() if corpo else None,
        }) + "\n")


def main():
    s, cfg = baixa(f"{B}/comum/config/ele-c.json", "")
    registra(f"{B}/comum/config/ele-c.json", os.path.join(RAIZ, "dados/oficial/ele-c.json"), s, cfg)
    d = json.loads(cfg.decode("latin-1") if b"\xef\xbf\xbd" not in cfg else cfg.decode("utf-8"))
    ufs = None
    for p in d["pl"]:
        if p["c"] == "ele2026":
            for e in p["e"]:
                if e["cd"] == "6257":
                    ufs = [a["cd"] for a in e["abr"]]
    ufs = "br ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to zz".split()
    for uf in ufs:
        # total oficial do presidente (cargo 0001)
        u = f"{B}/ele2026/6257/dados/{uf}/{uf}-c0001-e006257-u.jws"
        s, c = baixa(u, "")
        registra(u, os.path.join(RAIZ, f"dados/oficial/{uf}-c0001-e006257-u.jws"), s, c)
        if uf == "br":
            continue
        u = f"{B}/ele2026/arquivo-urna/3220/config/{uf}/{uf}-p003220-cs.json"
        s, c = baixa(u, "")
        registra(u, os.path.join(RAIZ, f"dados/cs/{uf}-p003220-cs.json"), s, c)
        print(uf, s, len(c))


if __name__ == "__main__":
    main()
