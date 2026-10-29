"""Fase 20: gera os anexos dos pedidos de acesso a informacao (LAI): listas de secoes por tribunal, com hora de emissao do BU na urna e hora de registro (hr).
Saida: pedidos_lai/anexos/*.csv (UTF-8 com BOM, separador ;) e pedidos_lai/anexos/resumo_zonas_recebida.csv"""
import csv, glob, json, os, sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

SAIDA = os.path.join(RAIZ, "pedidos_lai", "anexos")
os.makedirs(SAIDA, exist_ok=True)
fmt = "%d/%m/%Y %H:%M:%S"

nomes = {}
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    for m in json.load(open(f, encoding="utf-8"))["abr"][0]["mu"]:
        nomes[(uf, m["cd"])] = m["nm"]

hist, aux = defaultdict(list), {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    hist[k].append(j["status"])
    if j["status"] == 200:
        aux[k] = json.loads(j["aux"])
info = {}
for k, a in aux.items():
    h = a["hashes"][-1]
    info[k] = {"hr": datetime.strptime(h["dr"] + " " + h["hr"], fmt), "st_aux": a.get("st"), "st_hash": h.get("st"), "arq": ",".join(sorted(x["tp"] for x in h["arq"]))}

C = conv()


def emissao(k):
    for p in (os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu"), os.path.join(RAIZ, "dados", "busa", f"{k[0]}-{k[1]}-{k[2]}-{k[3]}.busa")):
        if os.path.exists(p):
            bu = C.decode("EntidadeBoletimUrna", C.decode("EntidadeEnvelopeGenerico", bytearray(open(p, "rb").read()))["conteudo"])
            e = bu["dataHoraEmissao"]
            return f"{e[6:8]}/{e[4:6]}/{e[0:4]} {e[9:11]}:{e[11:13]}:{e[13:15]}", bu["urna"]["tipoUrna"], bu["urna"]["tipoArquivo"]
    return "", "", ""


g404 = {k for k, h in hist.items() if h[0] == 404}
cauda = {k for k, v in info.items() if v["hr"] > datetime(2026, 10, 4, 23, 41)}
sa = {tuple(os.path.basename(f)[:-5].split("-")) for f in glob.glob(os.path.join(RAIZ, "dados/busa/*.busa"))}
recebida = {k for k, v in info.items() if v["st_aux"] == "Recebida" or v["st_hash"] == "Recebida"}

grupos = {k: [] for k in g404 | cauda | sa}
for k in g404: grupos[k].append("1a consulta HTTP 404 (arquivos publicados depois)")
for k in cauda: grupos[k].append("registro depois de 23h41 de 04/10")
for k in sa: grupos[k].append("BU do Sistema de Apuracao (busa)")


def escreve(nome, chaves):
    linhas = []
    for k in sorted(chaves, key=lambda x: (x[0], x[1], x[2], x[3])):
        em, tu, ta = emissao(k)
        v = info.get(k, {})
        linhas.append([k[0].upper(), k[1], nomes.get((k[0], k[1]), ""), k[2], k[3], em, v["hr"].strftime(fmt) if v else "", v.get("st_aux", ""), v.get("arq", ""), "; ".join(grupos.get(k, []))])
    p = os.path.join(SAIDA, nome)
    with open(p, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["UF", "cod_municipio", "municipio", "zona", "secao", "emissao_do_BU_na_urna", "registro_hr_no_repositorio_TSE", "status_no_aux", "arquivos_da_secao", "motivo_da_inclusao"])
        w.writerows(linhas)
    return len(linhas), p


resumo = {}
for uf, nome in (("pa", "TRE-PA"), ("pe", "TRE-PE"), ("ma", "TRE-MA"), ("mg", "TRE-MG"), ("sp", "TRE-SP")):
    n, _ = escreve(f"anexo_{nome}.csv", [k for k in grupos if k[0] == uf])
    resumo[nome] = n
# TSE: todas as secoes de interesse
n, _ = escreve("anexo_TSE_todas_as_secoes.csv", list(grupos))
resumo["TSE (todas)"] = n
print("secoes por anexo:", resumo)
print("grupos: 404 =", len(g404), "| cauda =", len(cauda), "| SA =", len(sa), "| uniao =", len(grupos), "| 'Recebida' =", len(recebida))
# zonas com 'Recebida'
z = Counter((k[0], k[1], k[2]) for k in recebida)
tam = Counter((k[0], k[1], k[2]) for k in info)
with open(os.path.join(SAIDA, "resumo_zonas_recebida.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.writer(f, delimiter=";")
    w.writerow(["UF", "cod_municipio", "municipio", "zona", "secoes_com_status_Recebida_na_coleta_de_05_10", "secoes_da_zona_com_BU"])
    for (uf, mu, zo), n in sorted(z.items(), key=lambda x: -x[1]):
        w.writerow([uf.upper(), mu, nomes.get((uf, mu), ""), zo, n, tam[(uf, mu, zo)]])
print("zonas com Recebida:", len(z), "| por UF:", dict(Counter(k[0] for k in recebida)))
# cauda por UF e por zona (para o texto)
for uf in ("pa", "pe", "ma", "mg"):
    ks = [k for k in cauda if k[0] == uf]
    zz = Counter((k[1], k[2]) for k in ks).most_common(4)
    hrs = sorted(info[k]["hr"] for k in ks)
    print(uf.upper(), "cauda", len(ks), "| registro", hrs[0].strftime("%d/%m %H:%M"), "a", hrs[-1].strftime("%d/%m %H:%M"), "| zonas:", [(nomes.get((uf, m), m), z_, n) for (m, z_), n in zz])
