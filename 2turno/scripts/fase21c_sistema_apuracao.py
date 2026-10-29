# -*- coding: utf-8 -*-
"""Fase 21c (2o turno): baixa o logsa.jez das secoes sem BU normal (apuradas pelo Sistema de Apuracao, so busa) e resume o que aconteceu:
tipo de apuracao, motivo registrado, cargos digitados, cancelamentos, inicio e fim.
Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase21c_sistema_apuracao.csv"""
import collections, csv, json, os, re, urllib.request, zipfile

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3221/dados"
LOG = os.path.join(RAIZ, "dados", "log")
os.makedirs(LOG, exist_ok=True)
T = re.compile(r"^(\d\d/\d\d/\d{4} \d\d:\d\d:\d\d)\t\w+\t\d+\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")

secoes = []
for l in open(os.path.join(RAIZ, "dados", "aux_manha_26-10.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] != 200:
        continue
    h = json.loads(j["aux"])["hashes"][-1]
    if any(x["tp"] == "bu" for x in h["arq"]):
        continue
    nm = next((x["nm"] for x in h["arq"] if x["tp"] == "logsa"), None)
    if nm:
        secoes.append(((j["uf"], j["mun"], j["zona"], j["sec"]), f"{B}/{j['uf']}/{j['mun']}/{j['zona']}/{j['sec']}/{h['hash']}/{nm}"))
out = []
for k, url in secoes:
    dest = os.path.join(LOG, "-".join(k) + ".jez")
    if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
        open(dest, "wb").write(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "auditoria-independente"}), timeout=60).read())
    z = zipfile.ZipFile(dest)
    ev = [T.match(x) for x in z.read(z.namelist()[0]).decode("latin1").splitlines()]
    ev = [(e.group(1), e.group(2), e.group(3)) for e in ev if e]

    def ach(p, mod="SA"):
        return [(t, m) for t, mod_, m in ev if mod_ == mod and re.search(p, m)]

    tipos = sorted({re.sub(r".*\((.*)\).*", r"\1", m) for _, m in ach(r"Tipo de apura")})
    motivo = [m.split(": ", 1)[1] for _, m in ach(r"Motivo da apura") if ": " in m]
    cargos = [re.search(r"\[(.*?)\]", m).group(1) for _, m in ach(r"^In.cio da digita..o de BU para o cargo") if re.search(r"\[(.*?)\]", m)]
    ini = ach(r"In.cio dos trabalhos do SA")
    fim = ach(r"arquivo de resultado \[busa\.dat\] \+ \[T")
    out.append({"UF": k[0].upper(), "mun": k[1], "zona": k[2], "secao": k[3], "tipos_apuracao": " | ".join(tipos),
                "motivo_registrado": " | ".join(motivo), "cargos_digitados": ",".join(cargos),
                "apuracao_cancelada_vezes": len(ach(r"Apura..o cancelada")),
                "inicio_SA": ini[0][0] if ini else "", "fim_busa": fim[0][0] if fim else ""})
if out:
    with open(os.path.join(RAIZ, "resultados", "fase21c_sistema_apuracao.csv"), "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0]), delimiter=";")
        w.writeheader()
        w.writerows(out)
print(len(out), "secoes")
print(collections.Counter(o["tipos_apuracao"] for o in out))
print(collections.Counter(o["motivo_registrado"] for o in out))
print(collections.Counter(o["cargos_digitados"] for o in out))
print("canceladas:", sum(1 for o in out if o["apuracao_cancelada_vezes"]), "| UF:", collections.Counter(o["UF"] for o in out))
