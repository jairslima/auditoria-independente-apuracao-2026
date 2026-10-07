# -*- coding: utf-8 -*-
"""Fase 21: baixa o log.jez (log da urna, zip com logd.dat) das 842 secoes do anexo LAI (68 atrasadas, 743 do dia seguinte,
31 do Sistema de Apuracao: logsa.jez) e de uma amostra de controle, e extrai metricas por secao.
Autoria: Auditoria Independente da Apuracao 2026 by Jair Lima.
Saida: dados/log/<uf>-<mun>-<zona>-<sec>.jez  e  resultados/fase21_logs.csv"""
import csv, io, json, os, random, re, sys, time, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
LOG = os.path.join(RAIZ, "dados", "log")
os.makedirs(LOG, exist_ok=True)
N_CONTROLE = int(os.environ.get("N_CONTROLE", "1500"))

aux = {}
for l in open(os.path.join(RAIZ, "dados", "aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] == 200:
        aux[(j["uf"], j["mun"], j["zona"], j["sec"])] = json.loads(j["aux"])

anexo = {}
for r in csv.DictReader(open(os.path.join(RAIZ, "pedidos_lai", "anexos", "anexo_TSE_todas_as_secoes.csv"), encoding="utf-8-sig"), delimiter=";"):
    anexo[(r["UF"].lower(), r["cod_municipio"], r["zona"], r["secao"])] = r["motivo_da_inclusao"]

chaves = sorted(anexo)
rest = sorted(k for k in aux if k not in anexo)
random.Random(2026).shuffle(rest)
controle = rest[:N_CONTROLE]
itens = [(k, "anexo") for k in chaves] + [(k, "controle") for k in controle]


def alvo(k):
    h = aux[k]["hashes"][-1]
    arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
    return h["hash"], arq["nm"] if arq else None


def baixa(it):
    k, grp = it
    dest = os.path.join(LOG, "-".join(k) + ".jez")
    if os.path.exists(dest) and os.path.getsize(dest) > 0:
        return k, grp, True
    hsh, nm = alvo(k)
    if not nm:
        return k, grp, False
    url = f"{B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{hsh}/{nm}"
    for t in range(4):
        try:
            d = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "auditoria-independente"}), timeout=60).read()
            open(dest, "wb").write(d)
            return k, grp, True
        except Exception:
            time.sleep(1 + t)
    return k, grp, False


def linhas(k):
    dest = os.path.join(LOG, "-".join(k) + ".jez")
    z = zipfile.ZipFile(dest)
    nome = z.namelist()[0]
    return z.read(nome).decode("latin1").splitlines()


RE_T = re.compile(r"^(\d\d/\d\d/\d{4} \d\d:\d\d:\d\d)\t(\w+)\t(\d+)\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")


def metricas(k, grp):
    L = linhas(k)
    ev = [RE_T.match(x) for x in L]
    ev = [e for e in ev if e]
    niveis = {}
    for e in ev:
        niveis[e.group(2)] = niveis.get(e.group(2), 0) + 1
    txt = [e.group(5) for e in ev]
    def acha(p):
        return next((e.group(1) for e in ev if re.search(p, e.group(5))), "")
    return {
        "UF": k[0].upper(), "mun": k[1], "zona": k[2], "secao": k[3], "grupo": grp, "motivo": anexo.get(k, ""),
        "linhas": len(L), "eventos": len(ev),
        "primeiro": ev[0].group(1) if ev else "", "ultimo": ev[-1].group(1) if ev else "",
        "ALERTA": niveis.get("ALERTA", 0), "ERRO": niveis.get("ERRO", 0) + niveis.get("ERROR", 0),
        "urna_serie": ev[0].group(3) if ev else "",
        "gera_bu": acha(r"arquivo de resultado \[bu\.dat\] \+ \[In"),
        "gera_log": acha(r"arquivo de resultado \[log\.jez\] \+ \[In"),
        "encerra_votacao": acha(r"(?i)encerr|fim da vota|vota..o encerrada"),
        "n_reinicios": sum(1 for t in txt if re.search(r"(?i)In.cio das opera..es do logd", t)),
        "n_cartao_ou_media": sum(1 for t in txt if re.search(r"(?i)m.dia de resultado|cart.o de mem", t)),
        "n_contingencia_ou_substituta": sum(1 for t in txt if re.search(r"(?i)conting|substitu|recupera..o de dados|\bRED\b", t)),
    }


if __name__ == "__main__":
    with ThreadPoolExecutor(8) as ex:
        res = list(ex.map(baixa, itens))
    falhas = [(k, g) for k, g, ok in res if not ok]
    print("baixados:", len(res) - len(falhas), "falhas:", len(falhas), falhas[:10], flush=True)
    linhas_csv = []
    for k, g, ok in res:
        if ok:
            try:
                linhas_csv.append(metricas(k, g))
            except Exception as e:
                print("erro", k, e)
    os.makedirs(os.path.join(RAIZ, "resultados"), exist_ok=True)
    saida = os.path.join(RAIZ, "resultados", "fase21_logs.csv")
    with open(saida, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(linhas_csv[0]), delimiter=";")
        w.writeheader()
        w.writerows(linhas_csv)
    print("linhas:", len(linhas_csv), "->", saida)
