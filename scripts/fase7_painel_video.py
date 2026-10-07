"""Fase 7: confronta os 3 estados do painel (TV Senado, 04/10 19:08, 19:20, 20:10) com a reconstrucao pelos BUs.
Percentuais sobre votos validos (candidatos). Prefixo = secoes ordenadas por hr (recebimento do BU)."""
import csv, os
from datetime import datetime
import numpy as np
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rows = list(csv.DictReader(open(os.path.join(RAIZ, "dados/votos_secao.csv"), encoding="utf-8")))
rows.sort(key=lambda r: datetime.strptime(r["hr"], "%d/%m/%Y %H:%M:%S"))
cands = [c for c in rows[0] if c.startswith("c")]
M = np.array([[int(r[c]) for c in cands] for r in rows], dtype=np.int64)
cum = M.cumsum(axis=0)
val = cum.sum(axis=1)
idx = {c: cands.index(c) for c in ("c22", "c13", "c70", "c55")}
pct = {c: cum[:, i] / val * 100 for c, i in idx.items()}
hrs = [r["hr"][11:] for r in rows]
TOT = 499248
estados = {
    "A 19:08 (47,26%)": (0.4726, dict(c22=50.20, c13=41.63, c70=2.96, c55=2.38)),
    "B 19:20 (64,81%)": (0.6481, dict(c22=49.58, c13=42.25, c70=2.97, c55=2.34)),
    "C 20:10 (84,96%)": (0.8496, dict(c22=48.47, c13=43.49, c70=2.94, c55=2.27)),
}
for nome, (frac, alvo) in estados.items():
    n0 = int(round(frac * TOT))
    print(f"\n== {nome}: secoes anunciadas ~{n0:,}")
    print(f"   prefixo hr com {n0:,} secoes (ate {hrs[n0-1]}): " + "  ".join(f"{c}={pct[c][n0-1]:.2f}(painel {alvo[c]})" for c in alvo))
    lo, hi = int(n0 * 0.80), min(len(rows) - 1, int(n0 * 1.20))
    err = sum((pct[c][lo:hi] - alvo[c]) ** 2 for c in alvo)
    b = lo + int(np.argmin(err))
    print(f"   melhor prefixo p/ os 4 percentuais: {b+1:,} secoes (ate {hrs[b]}) erro_rms={np.sqrt(err[b-lo]/4):.3f} pp | " + "  ".join(f"{c}={pct[c][b]:.2f}" for c in alvo))
    print(f"   diferenca de contagem vs anunciada: {b+1-n0:+,} secoes ({(b+1-n0)/TOT*100:+.2f} pp de urnas)")
