"""Auditoria Independente da Apuração 2026 by Jair Lima.
Fase 25: cruza a série do Painel de Evolução da Totalização do TSE (seções totalizadas a cada 5 min)
com o carimbo `hr` dos BUs (aux.jsonl, primeiro hash com dr/hr). Saída: resultados/fase25_painel_vs_hr.csv e .md
"""
import json, re, sys
from datetime import datetime
from pathlib import Path
R = Path(__file__).resolve().parent.parent
txt = (R/'dados/externos/painel_evolucao_1turno_resumo_geral.txt').read_text(encoding='utf-8')
pan = []
for tok in re.findall(r'\b(\d{6}):(\d+):(\d+)\b', txt):
    dh, s, n = tok
    pan.append((datetime(2026,10,int(dh[:2]),int(dh[2:4]),int(dh[4:])), int(s), int(n)))
hrs = []
for line in open(R/'dados/aux.jsonl', encoding='utf-8'):
    try: o = json.loads(line)
    except Exception: continue
    a = o.get('aux')
    if not a: continue
    try: j = json.loads(a)
    except Exception:
        m = re.search(r'"dr"\s*:\s*"([^"]+)"\s*,\s*"hr"\s*:\s*"([^"]+)"', a)
        if not m: continue
        hrs.append(datetime.strptime(m.group(1)+' '+m.group(2), '%d/%m/%Y %H:%M:%S')); continue
    for h in j.get('hashes', []):
        if h.get('dr') and h.get('hr'):
            hrs.append(datetime.strptime(h['dr']+' '+h['hr'], '%d/%m/%Y %H:%M:%S')); break
hrs.sort()
import bisect
rows = []
for t, s, n in pan:
    c = bisect.bisect_right(hrs, t)
    rows.append((t, s, c, c - s))
out = ['hora,painel_secoes,bu_hr_acumulado,diferenca(bu-painel),painel_delta5min,bu_delta5min']
prev = None
for t, s, c, d in rows:
    ps, pc = (prev[1], prev[2]) if prev else (0, 0)
    out.append(f'{t:%d %H:%M},{s},{c},{d},{s-ps},{c-pc}')
    prev = (t, s, c)
(R/'resultados/fase25_painel_vs_hr.csv').write_text('\n'.join(out), encoding='utf-8')
print('BUs com hr:', len(hrs))
print('\n'.join(out[20:62]))
# maiores intervalos sem BU e sem painel
gaps = sorted(((b-a).total_seconds(), a, b) for a, b in zip(hrs, hrs[1:]))[-5:]
print('maiores intervalos sem hr de BU:', [(int(g), f'{a:%d %H:%M:%S}', f'{b:%d %H:%M:%S}') for g, a, b in gaps])
