# -*- coding: utf-8 -*-
"""Fase 27: log da urna (log.jez / logsa.jez) de TODAS as secoes, lido em fluxo (o arquivo nao e guardado), so os eventos de 25/10/2026,
horario convertido para Brasilia (AC +2 h; AM, RO, RR, MT, MS +1 h; Fernando de Noronha nao tratado). Retomavel.
Saida: resultados/fase27_logs_todas.csv. Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, io, json, os, re, sys, time, urllib.request, zipfile
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados"
SAIDA = os.path.join(RAIZ, "resultados", "fase27_logs_todas.csv")
CAMPOS = ["uf", "mun", "zona", "sec", "urna_serie", "encerrar_brt", "gera_bu_brt", "gera_log_brt", "ultimo_voto_brt", "votos_total",
          "votos_apos_17h00", "votos_apos_17h06", "votos_apos_19h00", "n_reinicios", "erro"]
OFF = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}
FMT = "%d/%m/%Y %H:%M:%S"
RE_T = re.compile(r"^(25/10/2026 \d\d:\d\d:\d\d)\t(\w+)\t(\d+)\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")
T1700, T1706, T1900 = (datetime(2026, 10, 25, h, m, s) for h, m, s in ((17, 0, 0), (17, 6, 31), (19, 0, 0)))
NT = int(os.environ.get("THREADS", "6"))


def corpo(z, so_externo_da_urna=False):
    """Linhas do log da urna. O zip pode ter 2 arquivos: logd.dat (eventos depois do ultimo reinicio) e um .jez aninhado com o log da midia externa
    (eventos anteriores). Une os dois sem repetir linhas e ordena pela hora. Com so_externo_da_urna=True devolve so o logd.dat (leitura antiga)."""
    nomes = z.namelist()
    principal = z.read("logd.dat" if "logd.dat" in nomes else nomes[0]).decode("latin1").splitlines()
    if so_externo_da_urna:
        return principal
    vistas = set(principal)
    todas = list(principal)
    for n in nomes:
        d = z.read(n)
        if n != "logd.dat" and d[:2] == b"PK":
            z2 = zipfile.ZipFile(io.BytesIO(d))
            for n2 in z2.namelist():
                for linha in z2.read(n2).decode("latin1").splitlines():
                    if linha not in vistas:
                        vistas.add(linha)
                        todas.append(linha)
    todas.sort(key=lambda x: x[:19])
    return todas


def metricas(k, raw):
    z = zipfile.ZipFile(io.BytesIO(raw))
    L = corpo(z)
    off = timedelta(hours=OFF.get(k[0], 0))
    ev = [m for m in (RE_T.match(x) for x in L) if m]

    def t(m):
        return datetime.strptime(m.group(1), FMT) + off

    votos = [t(m) for m in ev if m.group(5).startswith("O voto do eleitor foi computado")]
    enc = [t(m) for m in ev if m.group(5).startswith("Operador selecionou: Encerrar vota")]
    bu = [t(m) for m in ev if "arquivo de resultado [bu.dat] + [In" in m.group(5)]
    lg = [t(m) for m in ev if "arquivo de resultado [log.jez] + [In" in m.group(5) or "arquivo de resultado [logsa.jez] + [In" in m.group(5)]

    def iso(x):
        return x[-1].isoformat() if x else ""

    return {"urna_serie": ev[-1].group(3) if ev else "", "encerrar_brt": iso(enc), "gera_bu_brt": iso(bu), "gera_log_brt": iso(lg),
            "ultimo_voto_brt": max(votos).isoformat() if votos else "", "votos_total": len(votos),
            "votos_apos_17h00": sum(1 for v in votos if v >= T1700), "votos_apos_17h06": sum(1 for v in votos if v >= T1706),
            "votos_apos_19h00": sum(1 for v in votos if v >= T1900),
            "n_reinicios": sum(1 for m in ev if "Início das operações do logd" in m.group(5))}


def norm(s):
    s = re.sub(r"\[[^\]]*\]", "[X]", s)
    return re.sub(r"\d+", "N", s)[:110]


def mensagens(raw, so_externo_da_urna=False):
    """Conjunto de tipos de mensagem (modulo, nivel, texto normalizado) presentes no log do dia, para a fase 21b."""
    z = zipfile.ZipFile(io.BytesIO(raw))
    ev = [m for m in (RE_T.match(x) for x in corpo(z, so_externo_da_urna)) if m]
    return sorted({(e.group(4), e.group(2), norm(e.group(5))) for e in ev})


def trabalha(it):
    k, url, grp = it
    base = {"uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "erro": ""}
    err = ""
    for n in range(4):
        try:
            raw = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "auditoria-independente"}), timeout=60).read()
            base.update(metricas(k, raw))
            base["_grupo"] = grp
            base["_msgs"] = mensagens(raw)
            return base
        except Exception as e:
            err = repr(e)[:120]
            time.sleep(1 + n)
    base["erro"] = err
    return base


CK = os.path.join(RAIZ, "resultados", "fase27_msg_contadores.json")
DEST = os.path.join(RAIZ, "..", "AuditoriaPresidente2026", "pedidos_lai", "anexos", "anexo_TSE_2turno_secoes_destacadas.csv")


def salva_ck(n_linhas, tot, msgs):
    tmp = CK + ".tmp"
    json.dump({"n_linhas": n_linhas, "tot": dict(tot), "msgs": [[list(m), dict(c)] for m, c in msgs.items()]}, open(tmp, "w", encoding="utf-8"), ensure_ascii=False)
    os.replace(tmp, CK)


if __name__ == "__main__":
    from collections import Counter, defaultdict
    # grupos para a fase 21b: atrasada (264), antes_hr (965), sist_apuracao (29, so logsa) e resto
    grupo_dest = {}
    for r in csv.DictReader(open(DEST, encoding="utf-8-sig"), delimiter=";"):
        grupo_dest[(r["uf"], r["mun"], r["zona"], r["sec"])] = "atrasada" if "depois" in r["motivo"] else "antes_hr"
    # retomada: so vale se houver checkpoint; o CSV e cortado no que o checkpoint cobre e as linhas com erro saem para serem refeitas
    tot, msgs, linhas_ok = Counter(), defaultdict(Counter), []
    if os.path.exists(CK) and os.path.exists(SAIDA):
        ck = json.load(open(CK, encoding="utf-8"))
        tot = Counter(ck["tot"])
        for m, c in ck["msgs"]:
            msgs[tuple(m)] = Counter(c)
        todas = list(csv.DictReader(open(SAIDA, encoding="utf-8-sig"), delimiter=";"))[:ck["n_linhas"]]
        linhas_ok = [r for r in todas if not r["erro"]]
    with open(SAIDA, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        w.writeheader()
        w.writerows(linhas_ok)
    feitos = {(r["uf"], r["mun"], r["zona"], r["sec"]) for r in linhas_ok}
    itens = []
    for l in open(os.path.join(RAIZ, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        if j["status"] != 200:
            continue
        k = (j["uf"], j["mun"], j["zona"], j["sec"])
        if k in feitos:
            continue
        h = json.loads(j["aux"])["hashes"][-1]
        arq = next((x for x in h["arq"] if x["tp"] in ("log", "logsa")), None)
        if arq:
            grp = "sist_apuracao" if arq["tp"] == "logsa" else grupo_dest.get(k, "resto")
            itens.append((k, f"{B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{arq['nm']}", grp))
    print("a fazer:", len(itens), "ja feitos:", len(feitos), flush=True)
    n = len(linhas_ok)
    with ThreadPoolExecutor(NT) as ex, open(SAIDA, "a", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS, delimiter=";")
        for i, r in enumerate(ex.map(trabalha, itens), 1):
            g, ms = r.pop("_grupo", None), r.pop("_msgs", None)
            w.writerow(r)
            n += 1
            if g is not None:
                tot[g] += 1
                for m in ms:
                    msgs[m][g] += 1
            if i % 2000 == 0:
                f.flush()
                salva_ck(n, tot, msgs)
                print(i, time.strftime("%H:%M:%S"), flush=True)
    salva_ck(n, tot, msgs)
    print("fim", n, flush=True)
