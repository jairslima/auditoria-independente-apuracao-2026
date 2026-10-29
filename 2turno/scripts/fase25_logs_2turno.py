# -*- coding: utf-8 -*-
"""Fase 25: logs das urnas do 2o turno (25/10/2026) lidos so nos eventos do dia: hora do encerramento, da geracao do BU e de cada voto
computado, convertidas para o horario de Brasilia, cruzadas com o hr do aux.json. Auditoria Independente da Apuracao 2026 by Jair Lima.
Saida: resultados/fase25_logs_2turno.csv e resumo no stdout. O relogio da urna e o local da UF; o deslocamento por UF e conferido
empiricamente comparando gera_bu com o hr do TSE (mediana por UF)."""
import csv, json, os, re, statistics, zipfile
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG = os.path.join(RAIZ, "dados", "log")
# horas a SOMAR ao relogio local da urna para chegar a Brasilia (AC -2h, AM/RO/RR/MT/MS -1h). Noronha (PE) ignorado.
OFF = {"ac": 2, "am": 1, "ro": 1, "rr": 1, "mt": 1, "ms": 1}
FMT = "%d/%m/%Y %H:%M:%S"
RE_T = re.compile(r"^(25/10/2026 \d\d:\d\d:\d\d)\t(\w+)\t(\d+)\t(\w+)\t(.*?)(?:\t[0-9A-F]{16})?$")
CORTE = datetime(2026, 10, 25, 17, 0, 0)
SUSP = datetime(2026, 10, 25, 17, 6, 31)
RETOMA = datetime(2026, 10, 25, 19, 0, 0)

grupo = {}
for r in csv.DictReader(open(os.path.join(RAIZ, "resultados", "fase21_logs.csv"), encoding="utf-8-sig"), delimiter=";"):
    grupo[(r["UF"].lower(), r["mun"], r["zona"], r["secao"])] = r["grupo"]

hr_aux = {}
for l in open(os.path.join(RAIZ, "dados", "aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    if k in grupo and j["status"] == 200:
        h = json.loads(j["aux"])["hashes"][-1]
        hr_aux[k] = datetime.strptime(h["dr"] + " " + h["hr"], FMT)

linhas = []
for k, g in grupo.items():
    p = os.path.join(LOG, "-".join(k) + ".jez")
    try:
        z = zipfile.ZipFile(p)
        L = z.read(z.namelist()[0]).decode("latin1").splitlines()
    except Exception:
        continue
    off = timedelta(hours=OFF.get(k[0], 0))
    ev = [m for m in (RE_T.match(x) for x in L) if m]
    def t(m): return datetime.strptime(m.group(1), FMT) + off
    votos = [t(m) for m in ev if m.group(5).startswith("O voto do eleitor foi computado")]
    enc = [t(m) for m in ev if m.group(5).startswith("Operador selecionou: Encerrar vota")]
    bu = [t(m) for m in ev if "arquivo de resultado [bu.dat] + [In" in m.group(5)]
    linhas.append({
        "uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "grupo": g,
        "encerrar_brt": enc[-1].isoformat() if enc else "", "gera_bu_brt": bu[-1].isoformat() if bu else "",
        "hr_tse_brt": hr_aux[k].isoformat() if k in hr_aux else "",
        "ultimo_voto_brt": max(votos).isoformat() if votos else "", "votos_total": len(votos),
        "votos_apos_17h_brt": sum(1 for v in votos if v >= CORTE),
    })
os.makedirs(os.path.join(RAIZ, "resultados"), exist_ok=True)
with open(os.path.join(RAIZ, "resultados", "fase25_logs_2turno.csv"), "w", newline="", encoding="utf-8-sig") as f:
    w = csv.DictWriter(f, fieldnames=list(linhas[0]), delimiter=";"); w.writeheader(); w.writerows(linhas)

def D(s): return datetime.fromisoformat(s) if s else None
print("secoes lidas:", len(linhas))
# 1) validacao do deslocamento: hr_tse - gera_bu por UF (controle)
por_uf = {}
for r in linhas:
    if r["grupo"] == "controle" and r["gera_bu_brt"] and r["hr_tse_brt"]:
        por_uf.setdefault(r["uf"], []).append((D(r["hr_tse_brt"]) - D(r["gera_bu_brt"])).total_seconds() / 60)
print("mediana (hr_tse - gera_bu) em minutos, por UF (controle); UF com |valor|>60 indicam relogio/offset diferente:")
print({u: round(statistics.median(v)) for u, v in sorted(por_uf.items()) if len(v) >= 5})
# 2) controle: distribuicao
ctl = [r for r in linhas if r["grupo"] == "controle"]
bu_ok = [r for r in ctl if r["gera_bu_brt"]]
def n(c): return sum(1 for r in bu_ok if c(D(r["gera_bu_brt"])))
print(f"controle com BU no log de 25/10: {len(bu_ok)} de {len(ctl)}")
print("  BU gerado antes de 17:06:31:", n(lambda t: t < SUSP), "| entre 17:06:31 e 19:00:", n(lambda t: SUSP <= t < RETOMA), "| depois das 19:00:", n(lambda t: t >= RETOMA))
# 3) votos apos 17h: estimativa populacional pelo controle (amostra aleatoria simples)
v = [r["votos_apos_17h_brt"] for r in ctl]
if v:
    m = statistics.mean(v); sd = statistics.pstdev(v); N = 499207
    ep = sd / len(v) ** 0.5
    print(f"votos apos 17h (hora de Brasilia) por secao no controle: media {m:.4f}; secoes com algum voto apos 17h: {sum(1 for x in v if x > 0)} de {len(v)}")
    print(f"  estimativa para as {N} secoes: {m*N:,.0f} (IC95% aprox. {max(0,(m-1.96*ep))*N:,.0f} a {(m+1.96*ep)*N:,.0f})")
# 4) destacadas (264 atrasadas + 965 vistas antes do hr)
an = [r for r in linhas if r["grupo"] == "anexo"]
bu_an = [r for r in an if r["gera_bu_brt"]]
def n2(c): return sum(1 for r in bu_an if c(D(r["gera_bu_brt"])))
print(f"destacadas com BU no log de 25/10: {len(bu_an)} de {len(an)}")
print("  BU antes de 17:06:31:", n2(lambda t: t < SUSP), "| 17:06:31 a 19:00:", n2(lambda t: SUSP <= t < RETOMA), "| depois das 19:00:", n2(lambda t: t >= RETOMA))
