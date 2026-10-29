# -*- coding: utf-8 -*-
"""Fase 27c: refaz a leitura dos logs das secoes em que os eventos 'voto computado' ficaram abaixo do comparecimento do BU. Nessas secoes o zip tem 2 arquivos
(log da midia externa, aninhado, e logd.dat) porque a urna reiniciou durante a votacao; a fase 27 leu so um deles. Une os dois, recalcula as metricas da secao e soma
aos contadores de mensagens (fase 21b) so os tipos de mensagem que antes nao apareciam. Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os, sys
from concurrent.futures import ThreadPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fase27_logs_todas as f27

RAIZ, SAIDA, CK = f27.RAIZ, f27.SAIDA, f27.CK
comp = {}
for r in csv.DictReader(open(os.path.join(RAIZ, "dados", "votos_secao.csv"), encoding="utf-8")):
    comp[(r["uf"], r["mun"], r["zona"], r["sec"])] = int(r["total"])
linhas = list(csv.DictReader(open(SAIDA, encoding="utf-8-sig"), delimiter=";"))
alvo = {}
for r in linhas:
    k = (r["uf"], r["mun"], r["zona"], r["sec"])
    if comp.get(k, 0) > int(r["votos_total"] or 0):
        alvo[k] = r
grupo_dest = {}
for r in csv.DictReader(open(f27.DEST, encoding="utf-8-sig"), delimiter=";"):
    grupo_dest[(r["uf"], r["mun"], r["zona"], r["sec"])] = "atrasada" if "depois" in r["motivo"] else "antes_hr"
itens = []
for l in open(os.path.join(RAIZ, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if j["status"] != 200 or k not in alvo:
        continue
    h = json.loads(j["aux"])["hashes"][-1]
    arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
    if arq:
        itens.append((k, f"{f27.B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{arq['nm']}", "sist_apuracao" if arq["tp"] == "logsa" else grupo_dest.get(k, "resto")))
print("secoes a refazer:", len(itens), flush=True)


def trabalha(it):
    k, url, grp = it
    import urllib.request, time
    for n in range(4):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "auditoria-independente"}), timeout=60).read()
            m = f27.metricas(k, raw)
            novos = set(f27.mensagens(raw)) - set(f27.mensagens(raw, so_externo_da_urna=True))
            return k, grp, m, novos, ""
        except Exception as e:
            err = repr(e)[:100]
            time.sleep(1 + n)
    return k, grp, None, set(), err


ck = json.load(open(CK, encoding="utf-8"))
msgs = {tuple(m): dict(c) for m, c in ck["msgs"]}
antes = sum(int(r["votos_total"] or 0) for r in alvo.values())
erros = 0
atualizados = {}
with ThreadPoolExecutor(f27.NT) as ex:
    for k, grp, m, novos, err in ex.map(trabalha, itens):
        if m is None:
            erros += 1
            print("ERRO", k, err, flush=True)
            continue
        atualizados[k] = m
        for msg in novos:
            msgs.setdefault(tuple(msg), {})
            msgs[tuple(msg)][grp] = msgs[tuple(msg)].get(grp, 0) + 1
saida = []
for r in linhas:
    k = (r["uf"], r["mun"], r["zona"], r["sec"])
    if k in atualizados:
        r = {**r, **{c: atualizados[k][c] for c in atualizados[k]}}
    saida.append(r)
with open(SAIDA, "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=f27.CAMPOS, delimiter=";")
    w.writeheader()
    w.writerows(saida)
json.dump({"n_linhas": len(saida), "tot": ck["tot"], "msgs": [[list(m), c] for m, c in msgs.items()]}, open(CK, "w", encoding="utf-8"), ensure_ascii=False)
depois = sum(int(atualizados[k]["votos_total"]) for k in atualizados)
print(f"fim | refeitas: {len(atualizados)} | erros: {erros} | votos nos logs dessas secoes: {antes} -> {depois} (BU: {sum(comp[k] for k in atualizados)})", flush=True)
