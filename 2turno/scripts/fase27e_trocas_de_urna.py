# -*- coding: utf-8 -*-
"""Fase 27e: nas secoes em que o log tem dois arquivos com eventos de 25/10 (log da midia externa + logd.dat), mostra quais numeros de serie de urna aparecem,
quantos votos cada urna registrou e se a urna que assinou o BU (certificado) e a ultima do dia. Compara a contagem com o 0,31% de urnas substituidas informado pelo TSE.
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase27e_trocas_de_urna.csv"""
import csv, io, json, os, re, sys, time, urllib.request, zipfile
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fase27_logs_todas as f27

R = f27.RAIZ
ANTES = os.path.join(R, "resultados", "fase27_logs_todas.antes_uniao.csv")
alvo = set()
comp = {}
for r in csv.DictReader(open(os.path.join(R, "dados", "votos_secao.csv"), encoding="utf-8")):
    comp[(r["uf"], r["mun"], r["zona"], r["sec"])] = int(r["total"])
for r in csv.DictReader(open(ANTES, encoding="utf-8-sig"), delimiter=";"):
    k = (r["uf"], r["mun"], r["zona"], r["sec"])
    if comp.get(k, 0) > int(r["votos_total"] or 0):
        alvo.add(k)
cert = {(r["uf"], r["mun"], r["zona"], r["sec"]): r["n_urna_cn"] for r in csv.DictReader(open(os.path.join(R, "dados", "assinaturas_secao.csv"), encoding="utf-8"))}
itens = []
for l in open(os.path.join(R, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if j["status"] != 200 or k not in alvo:
        continue
    h = json.loads(j["aux"])["hashes"][-1]
    arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
    if arq and arq["tp"] == "log":
        itens.append((k, f"{f27.B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{arq['nm']}"))
print("secoes a examinar:", len(itens), flush=True)


def analisa(it):
    k, url = it
    for n in range(4):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "auditoria-independente"}), timeout=60).read()
            z = zipfile.ZipFile(io.BytesIO(raw))
            ev = [m for m in (f27.RE_T.match(x) for x in f27.corpo(z)) if m]
            por = defaultdict(lambda: {"ini": None, "fim": None, "votos": 0})
            for m in ev:
                s = por[m.group(3)]
                t = m.group(1)
                s["ini"] = t if s["ini"] is None or t < s["ini"] else s["ini"]
                s["fim"] = t if s["fim"] is None or t > s["fim"] else s["fim"]
                if m.group(5).startswith("O voto do eleitor foi computado"):
                    s["votos"] += 1
            ordem = sorted(por, key=lambda x: por[x]["ini"])
            bu = [m.group(3) for m in ev if "arquivo de resultado [bu.dat] + [In" in m.group(5)]
            por["_bu"] = bu[-1] if bu else (ev[-1].group(3) if ev else "")
            return k, ordem, por, ""
        except Exception as e:
            err = repr(e)[:100]
            time.sleep(1 + n)
    return k, [], {}, err


saida = []
with ThreadPoolExecutor(f27.NT) as ex:
    for k, ordem, por, err in ex.map(analisa, itens):
        if err:
            print("ERRO", k, err, flush=True)
            continue
        final = por.pop("_bu", "")
        com_voto = [u for u in ordem if por[u]["votos"] > 0]
        tipo = "uma_urna" if len(ordem) == 1 else "votou_em_duas_ou_mais_urnas" if len(com_voto) >= 2 else "outra_urna_so_gerou_o_resultado" if len(com_voto) == 1 else "nenhuma_urna_com_voto"
        saida.append({"uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "n_urnas_no_dia": len(ordem), "urnas_em_ordem": "|".join(ordem),
                      "votos_por_urna": "|".join(str(por[u]["votos"]) for u in ordem), "urna_que_gerou_o_bu": final, "tipo": tipo, "urna_do_certificado": cert.get(k, ""),
                      "gerou_bu_igual_certificado": int(bool(final) and bool(cert.get(k)) and int(final) == int(cert[k])), "comparecimento_bu": comp[k],
                      "votos_somados": sum(por[u]["votos"] for u in ordem)})
with open(os.path.join(R, "resultados", "fase27e_trocas_de_urna.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(saida[0]), delimiter=";")
    w.writeheader(); w.writerows(saida)
c = Counter(s["n_urnas_no_dia"] for s in saida)
print("secoes examinadas:", len(saida), "| por numero de urnas distintas no dia:", dict(c))
dois = [s for s in saida if s["n_urnas_no_dia"] >= 2]
print("com 2 ou mais urnas:", len(dois), "(%.3f%% das 499.207 secoes)" % (len(dois) / 499207 * 100), "| TSE informou 0,31% =", round(0.0031 * 499207))
print("urna que gerou o bu.dat = urna do certificado:", sum(s["gerou_bu_igual_certificado"] for s in saida), "de", len(saida))
print("soma dos votos de todas as urnas = comparecimento do BU:", sum(1 for s in saida if s["votos_somados"] == s["comparecimento_bu"]), "de", len(saida))
print("por tipo:", dict(Counter(s["tipo"] for s in saida)))
print("exemplo:", [(s["uf"], s["sec"], s["urnas_em_ordem"], s["votos_por_urna"], s["comparecimento_bu"]) for s in dois[:3]])
