# -*- coding: utf-8 -*-
"""Monitor de chegada para o 2o turno (Auditoria Independente da Apuracao 2026 by Jair Lima).

Objetivo: registrar o RELOGIO PROPRIO da auditoria, que no 1o turno faltou. No 1o turno so dava para usar o campo `hr` do aux.json
(carimbo de registro no repositorio do TSE), que nao e hora de chegada confiavel. Aqui registramos, para cada secao, o instante UTC em que
NOS vimos a secao publicada pela primeira vez, e, a cada ciclo, o resultado oficial nacional (hora de geracao dg/hg, % de secoes
totalizadas, votos). Isso permite desenhar a curva de apuracao e detectar pausas do painel em tempo real, com carimbo independente.

Uso (deixar rodando na noite da eleicao, ex.: a partir das 16h de Brasilia):
    python monitor_chegada.py                      # descobre sozinho o pleito do 2o turno no config do TSE
    PLEITO=3221 ELEICAO=6258 python monitor_chegada.py   # ou informando

Saidas em segundo_turno/dados_monitor/:
    curva_oficial.csv      uma linha por ciclo: utc, dg, hg, secoes_totalizadas, pct, votos dos candidatos (arquivo nacional)
    primeira_vez.csv       uma linha por secao nova: utc_primeira_vez, uf, mun, zona, secao, da, ha (carimbo do indice)
    snapshots/             copia bruta (gz) do arquivo nacional sempre que dg/hg muda, com SHA-256 no manifesto.jsonl
    ciclos.log             erros e HTTP 429 (limite de requisicoes: o TSE bloqueia acima de ~10 conexoes simultaneas)
Parar com Ctrl+C. Retomavel: ao reiniciar, le primeira_vez.csv e nao repete secoes ja registradas.
Baixo impacto: 1 pedido nacional por ciclo + 27 indices por UF a cada INDICE_A_CADA segundos, sequencial (nunca em paralelo)."""
import base64, csv, gzip, hashlib, json, os, sys, time, urllib.error, urllib.request
from datetime import datetime, timezone

RAIZ = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(RAIZ, "dados_monitor")
SNAP = os.path.join(SAIDA, "snapshots")
os.makedirs(SNAP, exist_ok=True)
B = "https://resultados.tse.jus.br/oficial"
ELEICAO = os.environ.get("ELEICAO", "6258")          # Presidente, 2o turno (cdt2 de 6257)
PLEITO = os.environ.get("PLEITO", "")                # codigo do pleito de urnas do 2o turno; vazio = descobrir
CICLO = int(os.environ.get("CICLO", "60"))           # segundos entre consultas ao arquivo nacional
INDICE_A_CADA = int(os.environ.get("INDICE_A_CADA", "180"))  # segundos entre varreduras dos 27 indices por UF
UFS = "ac al ap am ba ce df es go ma mt ms mg pa pb pr pe pi rj rn rs ro rr sc sp se to zz".split()
UA = {"User-Agent": "auditoria-independente-2026/1.0 (jairslima@gmail.com)"}


def agora():
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def log(msg):
    with open(os.path.join(SAIDA, "ciclos.log"), "a", encoding="utf-8") as f:
        f.write(f"{agora()} {msg}\n")


def pega(url):
    try:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        if e.code == 429:
            log(f"429 {url}")
            time.sleep(30)
        return e.code, b""
    except Exception as e:
        log(f"ERRO {url} {e!r}")
        return 0, b""


def descobre_pleito():
    s, c = pega(f"{B}/comum/config/ele-c.json")
    if s != 200:
        return ""
    d = json.loads(c.decode("utf-8", "replace"))
    for p in d["pl"]:
        for e in p["e"]:
            if e["cd"] == ELEICAO:
                return p["cd"]
    return ""


def texto(c):
    c = c.lstrip(b"\xef\xbb\xbf")
    try:
        return c.decode("utf-8")
    except UnicodeDecodeError:
        return c.decode("latin-1")


def decodifica_jws(c):
    """Arquivos .jws do TSE: JWT cujo meio (base64url) e o JSON do resultado."""
    p = c.decode().split(".")[1]
    return json.loads(base64.urlsafe_b64decode(p + "=" * (-len(p) % 4)))


def ciclo_nacional(vistos_dg):
    url = f"{B}/ele2026/{ELEICAO}/dados/br/br-c0001-e00{ELEICAO}-u.jws"
    s, c = pega(url)
    if s != 200 or not c:
        log(f"nacional HTTP {s} {url}")
        return
    d = decodifica_jws(c)
    cand = {}
    for agr in d["carg"][0]["agr"]:
        for par in agr["par"]:
            for cd in par["cand"]:
                cand[f"{cd.get('nmu') or cd['nm']} ({cd['n']})"] = int(cd["vap"])
    novo = not os.path.exists(os.path.join(SAIDA, "curva_oficial.csv"))
    with open(os.path.join(SAIDA, "curva_oficial.csv"), "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if novo:
            w.writerow(["utc_consulta", "dg", "hg", "secoes_totalizadas", "pct_secoes", "votos_validos", "brancos", "nulos"] + sorted(cand))
        w.writerow([agora(), d.get("dg"), d.get("hg"), d["s"]["st"], d["s"]["pst"], d["v"].get("vv"), d["v"].get("vb"), d["v"].get("vn")] + [cand[k] for k in sorted(cand)])
    chave = (d.get("dg"), d.get("hg"))
    if chave not in vistos_dg:
        vistos_dg.add(chave)
        nome = f"br_{(d.get('dg') or '').replace('/', '')}_{(d.get('hg') or '').replace(':', '')}.jws.gz"
        gz = gzip.compress(c)
        open(os.path.join(SNAP, nome), "wb").write(gz)
        with open(os.path.join(SAIDA, "manifesto.jsonl"), "a", encoding="utf-8") as m:
            m.write(json.dumps({"utc": agora(), "arquivo": nome, "sha256_bruto": hashlib.sha256(c).hexdigest(), "dg": d.get("dg"), "hg": d.get("hg"), "st": d["s"]["st"]}) + "\n")
    print(f"{agora()} dg/hg {d.get('dg')} {d.get('hg')} | secoes {d['s']['st']} ({d['s']['pst']}%)", flush=True)


def varre_indices(pleito, ja):
    novos = 0
    caminho = os.path.join(SAIDA, "primeira_vez.csv")
    existe = os.path.exists(caminho)
    with open(caminho, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        if not existe:
            w.writerow(["utc_primeira_vez", "uf", "mun", "zona", "secao", "da", "ha"])
        for uf in UFS:
            s, c = pega(f"{B}/ele2026/arquivo-urna/{pleito}/config/{uf}/{uf}-p00{pleito}-cs.json")
            if s != 200 or not c:
                continue
            d = json.loads(texto(c))
            agr = d["abr"][0]
            t = agora()
            for m in agr["mu"]:
                for z in m["zon"]:
                    for sec in z["sec"]:
                        if "da" in sec:
                            k = (uf, m["cd"], z["cd"], sec["ns"])
                            if k not in ja:
                                ja.add(k)
                                w.writerow([t, uf, m["cd"], z["cd"], sec["ns"], sec["da"], sec.get("ha", "")])
                                novos += 1
            time.sleep(0.5)
    return novos


def main():
    pleito = PLEITO or descobre_pleito()
    ja = set()
    cam = os.path.join(SAIDA, "primeira_vez.csv")
    if os.path.exists(cam):
        for r in csv.DictReader(open(cam, encoding="utf-8"), delimiter=";"):
            ja.add((r["uf"], r["mun"], r["zona"], r["secao"]))
    vistos_dg = set()
    print(f"Eleicao {ELEICAO}, pleito de urnas {pleito or '(ainda nao publicado)'}; {len(ja)} secoes ja registradas. Ctrl+C para parar.", flush=True)
    ultimo_indice = 0
    while True:
        try:
            if not pleito:
                pleito = descobre_pleito()
                if pleito:
                    print(f"{agora()} pleito do 2o turno publicado: {pleito}", flush=True)
            ciclo_nacional(vistos_dg)
            if pleito and time.time() - ultimo_indice >= INDICE_A_CADA:
                n = varre_indices(pleito, ja)
                ultimo_indice = time.time()
                print(f"{agora()} indices: {n} secoes novas (total visto {len(ja)})", flush=True)
        except KeyboardInterrupt:
            print("Parado pelo usuario.")
            return
        except Exception as e:
            log(f"excecao no ciclo: {e!r}")
        time.sleep(CICLO)


if __name__ == "__main__":
    main()
