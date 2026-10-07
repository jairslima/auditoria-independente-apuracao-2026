# -*- coding: utf-8 -*-
"""Fase 21c: resume, a partir do logsa.jez, o que aconteceu nas 31 secoes apuradas pelo Sistema de Apuracao (busa).
Autoria: Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase21c_sistema_apuracao.csv"""
import csv, os, re, zipfile, collections
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(RAIZ, "dados", "log")
R = [r for r in csv.DictReader(open(os.path.join(RAIZ, "resultados", "fase21_logs.csv"), encoding="utf-8-sig"), delimiter=";") if "busa" in r["motivo"]]
T = re.compile(r"^(\d\d/\d\d/\d{4} \d\d:\d\d:\d\d)\t\w+\t\d+\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")
out = []
for r in R:
    k = (r["UF"].lower(), r["mun"], r["zona"], r["secao"])
    z = zipfile.ZipFile(os.path.join(LOG, "-".join(k) + ".jez"))
    ev = [T.match(x) for x in z.read(z.namelist()[0]).decode("latin1").splitlines()]
    ev = [(e.group(1), e.group(2), e.group(3)) for e in ev if e]
    def ach(p, mod="SA"):
        return [(t, m) for t, mod_, m in ev if mod_ == mod and re.search(p, m)]
    tipos = sorted({re.sub(r".*\((.*)\).*", r"\1", m) for _, m in ach(r"Tipo de apura")})
    motivo = [m.split(": ", 1)[1] for _, m in ach(r"Motivo da apura")]
    cargos = [re.search(r"\[(.*?)\]", m).group(1) for _, m in ach(r"^In.cio da digita..o de BU para o cargo")]
    ini = ach(r"In.cio dos trabalhos do SA")
    fim = ach(r"arquivo de resultado \[busa\.dat\] \+ \[T")
    canc = len(ach(r"Apura..o cancelada"))
    dig_bu = bool(ach(r"In.cio da digita..o de BU$"))
    out.append({"UF": r["UF"], "mun": r["mun"], "zona": r["zona"], "secao": r["secao"], "tipos_apuracao": " | ".join(tipos),
                "motivo_registrado": " | ".join(motivo), "cargos_digitados": ",".join(cargos), "apuracao_cancelada_vezes": canc,
                "inicio_SA": ini[0][0] if ini else "", "fim_busa": fim[0][0] if fim else "", "emissao_BU_busa_no_repositorio": ""})
w = csv.DictWriter(open(os.path.join(RAIZ, "resultados", "fase21c_sistema_apuracao.csv"), "w", newline="", encoding="utf-8-sig"), fieldnames=list(out[0]), delimiter=";")
w.writeheader(); w.writerows(out)
print(len(out), "secoes")
print(collections.Counter(o["tipos_apuracao"] for o in out))
print(collections.Counter(o["motivo_registrado"] for o in out))
print(collections.Counter(o["cargos_digitados"] for o in out))
print("canceladas:", sum(1 for o in out if o["apuracao_cancelada_vezes"]), "| UF:", collections.Counter(o["UF"] for o in out))
