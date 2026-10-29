# -*- coding: utf-8 -*-
"""Uma linha com o andamento de cada etapa da verificacao completa do 2o turno (usada no aviso de hora em hora).
Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, os
from collections import Counter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def linhas(p):
    if not os.path.exists(p):
        return 0
    with open(p, "rb") as f:
        return max(0, sum(1 for _ in f) - (1 if p.endswith(".csv") else 0))


def ultima(p):
    if not os.path.exists(p):
        return "–"
    t = [l.strip() for l in open(p, encoding="utf-8", errors="replace") if l.strip()]
    return t[-1] if t else "–"


aux = linhas(os.path.join(RAIZ, "dados", "aux_24h.jsonl"))
rdv = os.path.join(RAIZ, "dados", "rdv_vs_bu.csv")
c = Counter(r["status"] for r in csv.DictReader(open(rdv, encoding="utf-8"))) if os.path.exists(rdv) else Counter()
logs = linhas(os.path.join(RAIZ, "resultados", "fase27_logs_todas.csv"))
print(f"aux 27/10: {aux:,} de 499.207 | RDV: {sum(c.values()):,} de 499.207 (divergentes {c.get('DIVERGE', 0)}, erros {c.get('erro', 0)}) | "
      f"logs: {logs:,} de 499.207 | etapa: {ultima(os.path.join(RAIZ, 'dados', 'cadeia4.log'))}".replace(",", "."))
