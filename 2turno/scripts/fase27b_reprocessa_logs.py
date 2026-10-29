# -*- coding: utf-8 -*-
"""Fase 27b: reprocessa os logs que a fase 27 leu sem eventos de 25/10 (zip com 2 arquivos: o log da midia externa e logd.dat) e confere as secoes sem log.
Atualiza as linhas em resultados/fase27_logs_todas.csv e soma os tipos de mensagem aos contadores (fase27_msg_contadores.json).
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os, sys, time
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fase27_logs_todas as f27

RAIZ = f27.RAIZ
SAIDA, CK = f27.SAIDA, f27.CK
linhas = list(csv.DictReader(open(SAIDA, encoding="utf-8-sig"), delimiter=";"))
vazios = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in linhas if not r["urna_serie"]}
grupo_dest = {}
for r in csv.DictReader(open(f27.DEST, encoding="utf-8-sig"), delimiter=";"):
    grupo_dest[(r["uf"], r["mun"], r["zona"], r["sec"])] = "atrasada" if "depois" in r["motivo"] else "antes_hr"
feitos = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in linhas}
itens, sem_arquivo = [], []
for l in open(os.path.join(RAIZ, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] != 200:
        continue
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if k not in vazios and k in feitos:
        continue
    h = json.loads(j["aux"])["hashes"][-1]
    arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
    if arq is None:
        sem_arquivo.append((k, [x["tp"] for x in h["arq"]], h.get("st")))
        continue
    grp = "sist_apuracao" if arq["tp"] == "logsa" else grupo_dest.get(k, "resto")
    itens.append((k, f"{f27.B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{arq['nm']}", grp))
print("a reprocessar:", len(itens), "| secoes sem arquivo de log no repositorio:", sem_arquivo, flush=True)

ck = json.load(open(CK, encoding="utf-8"))
msgs = {tuple(m): dict(c) for m, c in ck["msgs"]}
novos = {}
with ThreadPoolExecutor(f27.NT) as ex:
    for i, r in enumerate(ex.map(f27.trabalha, itens), 1):
        g, ms = r.pop("_grupo", None), r.pop("_msgs", None)
        k = (r["uf"], r["mun"], r["zona"], r["sec"])
        novos[k] = r
        if g is not None:
            for m in ms:
                msgs.setdefault(tuple(m), {})
                msgs[tuple(m)][g] = msgs[tuple(m)].get(g, 0) + 1
        if i % 2000 == 0:
            print(i, time.strftime("%H:%M:%S"), flush=True)
saida = []
for r in linhas:
    k = (r["uf"], r["mun"], r["zona"], r["sec"])
    saida.append(novos.pop(k, r) if k in vazios else r)
saida.extend(novos.values())   # secoes que ainda nao estavam na tabela
with open(SAIDA, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=f27.CAMPOS, delimiter=";")
    w.writeheader()
    w.writerows(saida)
tot = dict(ck["tot"])
json.dump({"n_linhas": len(saida), "tot": tot, "msgs": [[list(m), c] for m, c in msgs.items()]}, open(CK, "w", encoding="utf-8"), ensure_ascii=False)
ainda = sum(1 for r in saida if not r["urna_serie"])
print("fim | linhas:", len(saida), "| ainda sem eventos de 25/10:", ainda, "| com erro:", sum(1 for r in saida if r["erro"]), flush=True)

