# -*- coding: utf-8 -*-
"""Prepara uma copia da auditoria para o 2o turno (Auditoria Independente da Apuracao 2026 by Jair Lima).

Cria uma pasta irma (por padrao ..\\AuditoriaPresidente2026_T2) com os scripts das fases copiados e com os codigos do 1o turno trocados
pelos do 2o turno, para que cada script grave seus dados em dados/ dessa nova raiz, sem misturar com o 1o turno.
Trocas: pleito de urnas 3220 -> PLEITO ; Presidente 6257 -> 6258 ; estadual 6259 -> 6260 (so se houver 2o turno estadual).
Junta (junction) docs_tse do 1o turno para nao copiar de novo, e grava um LEIAME com o que conferir a mao.

Uso:  python preparar_2turno.py --pleito 3221 [--destino C:\\caminho] [--estadual]
O pleito do 2o turno aparece em https://resultados.tse.jus.br/oficial/comum/config/ele-c.json (entrada ele2026 cuja lista de eleicoes contem 6258).
"""
import argparse, os, re, shutil, subprocess, sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pleito", required=True, help="codigo do pleito de urnas do 2o turno (ex.: 3221)")
    ap.add_argument("--destino", default=RAIZ + "_T2")
    ap.add_argument("--presidente", default="6258")
    ap.add_argument("--estadual", action="store_true", help="trocar tambem 6259 -> 6260 (governadores com 2o turno)")
    a = ap.parse_args()
    ssrc, sdst = os.path.join(RAIZ, "scripts"), os.path.join(a.destino, "scripts")
    os.makedirs(sdst, exist_ok=True)
    alertas = []
    for nome in sorted(os.listdir(ssrc)):
        if not nome.endswith(".py"):
            continue
        t = open(os.path.join(ssrc, nome), encoding="utf-8").read()
        o = t
        t = t.replace("3220", a.pleito).replace("6257", a.presidente)
        if a.estadual:
            t = t.replace("6259", "6260")
        # numeros do 1o turno que precisam de conferencia manual
        for padrao in (r"499[.]?207", r"499[.]?248", r"119[.]?300[.]?788", r"27[.]?547"):
            if re.search(padrao, t):
                alertas.append(f"{nome}: contem constante do 1o turno ({padrao})")
        if t != o or True:
            open(os.path.join(sdst, nome), "w", encoding="utf-8").write(t)
    for pasta in ("docs_tse",):
        origem, destino = os.path.join(RAIZ, pasta), os.path.join(a.destino, pasta)
        if os.path.isdir(origem) and not os.path.exists(destino):
            subprocess.run(["cmd", "/c", "mklink", "/J", os.path.normpath(destino), os.path.normpath(origem)], check=False, capture_output=True)
    os.makedirs(os.path.join(a.destino, "dados"), exist_ok=True)
    os.makedirs(os.path.join(a.destino, "resultados"), exist_ok=True)
    with open(os.path.join(a.destino, "LEIAME_T2.md"), "w", encoding="utf-8") as f:
        f.write(f"""# 2o turno: copia preparada em lote

Pleito de urnas: {a.pleito}. Presidente: {a.presidente}. Estadual trocado: {'sim (6260)' if a.estadual else 'nao'}.
Os scripts em `scripts/` sao os do 1o turno com os codigos trocados. Rode na ordem do `RUNBOOK_2TURNO.md` (pasta segundo_turno do projeto original).

## Conferir a mao antes de confiar nos resultados
Constantes do 1o turno ainda presentes nos scripts (podem ser validacoes que vao falhar de proposito ou precisam ser trocadas):
""" + "\n".join(f"- {x}" for x in alertas) + """

Lembretes: a semente dos sorteios (2026, 2027) pode ser mantida, mas registre no relatorio. O 2o turno tem so 2 candidatos a Presidente:
as tabelas do relatorio e a pagina precisam de adaptacao (`relatorio_web/`).
""")
    print("Copia criada em", a.destino)
    print("Constantes do 1o turno a conferir:", len(alertas))
    for x in alertas[:20]:
        print(" -", x)


if __name__ == "__main__":
    main()
