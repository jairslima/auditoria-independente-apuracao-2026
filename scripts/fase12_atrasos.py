"""Fase 12: levantamento detalhado de TODOS os atrasos/lacunas (recebimento, cauda, 'Recebida', contingencia SA, 404, carimbos do indice).
Saida: dados/atrasos.json e impressao em tela. Somente leitura dos dados ja coletados."""
import csv, glob, json, os, sys
from collections import Counter, defaultdict
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ

fmt = "%d/%m/%Y %H:%M:%S"
hist, corpo = defaultdict(list), {}
for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    hist[k].append(j["status"])
    if j["status"] == 200:
        corpo[k] = json.loads(j["aux"])
rec = {}
for k, a in corpo.items():
    h = a["hashes"][-1]
    rec[k] = (datetime.strptime(h["dr"] + " " + h["hr"], fmt), a.get("st"), h.get("st"), sorted(x["tp"] for x in h["arq"]))
N = len(rec)
out = {"n_secoes_com_aux": N}
T = lambda hh, mm, ss=0, d=4: datetime(2026, 10, d, hh, mm, ss)

print("=== A. Recebimento (hr do aux.json) por faixa de 5 min, 18:30 a 21:30 ===")
bins = Counter()
for t, *_ in rec.values():
    if T(18, 30) <= t < T(21, 30):
        bins[t.replace(minute=t.minute // 5 * 5, second=0)] += 1
acum = sum(1 for t, *_ in rec.values() if t < T(18, 30))
linhas = []
for b in sorted(bins):
    acum += bins[b]
    linhas.append((b.strftime("%H:%M"), bins[b], acum, round(acum / N * 100, 2)))
    print(f"{b.strftime('%H:%M')}  recebidas={bins[b]:>6,}  acumulado={acum:>7,} ({acum / N * 100:5.2f}%)")
out["bins_5min"] = linhas
ini, fim = T(19, 6, 33), T(20, 8)
dentro = sum(1 for t, *_ in rec.values() if ini < t <= fim)
antes_1h = sum(1 for t, *_ in rec.values() if ini - (fim - ini) < t <= ini)
depois_1h = sum(1 for t, *_ in rec.values() if fim < t <= fim + (fim - ini))
print(f"\nrecebidas DURANTE a pausa do painel (19:06:33-20:08:00): {dentro:,} | na hora anterior: {antes_1h:,} | na hora seguinte: {depois_1h:,}")
out["recebidas_durante_pausa"] = dentro; out["recebidas_hora_anterior"] = antes_1h; out["recebidas_hora_seguinte"] = depois_1h
seg = Counter()
for t, *_ in rec.values():
    if T(19, 6) <= t < T(20, 10):
        seg[t.replace(second=0)] += 1
mx = sorted(seg.items(), key=lambda x: x[1])[:5]
print("minutos mais vazios na janela 19:06-20:10:", [(k.strftime('%H:%M'), v) for k, v in mx])

print("\n=== B. Cauda: recebidas depois de 23:41 (instante em que a CNN diz restarem 22 secoes) ===")
cauda = [(t, k) for k, (t, *_r) in rec.items() if t > T(23, 41)]
cauda.sort()
print("total:", len(cauda), "| depois de 00:00 de 05/10:", sum(1 for t, _ in cauda if t >= T(0, 0, 0, 5)), "| depois de 03:00:", sum(1 for t, _ in cauda if t >= T(3, 0, 0, 5)), "| depois de 06:00:", sum(1 for t, _ in cauda if t >= T(6, 0, 0, 5)))
print("ultimas 5:", [(k, t.strftime('%d %H:%M:%S')) for t, k in cauda[-5:]])
print("por UF (cauda):", Counter(k[0] for _, k in cauda).most_common(8))
print("tipos de arquivo na cauda:", Counter(tuple(rec[k][3]) for _, k in cauda).most_common(4))
out["cauda_2341"] = len(cauda); out["cauda_por_uf"] = Counter(k[0] for _, k in cauda).most_common(10)
out["cauda_ultimas"] = [(list(k), t.strftime("%d %H:%M:%S")) for t, k in cauda[-10:]]

print("\n=== C. Status 'Recebida' no aux.json (no momento da coleta) ===")
recb = [k for k, v in rec.items() if v[2] == "Recebida" or v[1] == "Recebida"]
print("secoes 'Recebida':", len(recb), "| 'Totalizada':", sum(1 for v in rec.values() if v[1] == "Totalizada"))
hs = sorted(rec[k][0] for k in recb)
if hs:
    print("hr dessas secoes: min", hs[0].strftime("%d %H:%M:%S"), "| mediana", hs[len(hs) // 2].strftime("%d %H:%M:%S"), "| max", hs[-1].strftime("%d %H:%M:%S"))
print("por UF:", Counter(k[0] for k in recb).most_common(8))
print("quantas estao na cauda (>23:41):", sum(1 for k in recb if rec[k][0] > T(23, 41)))
out["recebida"] = len(recb)

print("\n=== D. As 31 secoes de contingencia do Sistema de Apuracao (busa) ===")
c = conv()
busa = []
for f in sorted(glob.glob(os.path.join(RAIZ, "dados/busa/*.busa"))):
    nome = os.path.basename(f)[:-5]
    uf, mun, zon, sec = nome.split("-")
    raw = open(f, "rb").read()
    bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(raw))["conteudo"])
    u = bu["urna"]
    busa.append((uf, mun, zon, sec, rec[(uf, mun, zon, sec)][0], str(u.get("motivoUtilizacaoSA"))[:70], bu["cabecalho"]["dataGeracao"]))
for b in sorted(busa, key=lambda x: x[4]):
    print(f"{b[0]} {b[1]}-{b[2]}-{b[3]} recebido {b[4].strftime('%d %H:%M')} | motivo SA: {b[5]} | gerado {b[6]}")
print("por UF:", Counter(b[0] for b in busa), "| hr min/max:", min(b[4] for b in busa).strftime("%d %H:%M"), max(b[4] for b in busa).strftime("%d %H:%M"))
out["busa"] = [[b[0], b[1], b[2], b[3], b[4].strftime("%d %H:%M:%S"), b[5]] for b in busa]

print("\n=== E. Secoes cuja 1a consulta ao TSE deu 404 (68) ===")
c404 = [k for k, h in hist.items() if h[0] == 404]
g = defaultdict(list)
for k in c404:
    g[(k[0], k[1], k[2], len(hist[k]))].append(k)
for key, ks in sorted(g.items()):
    hs = sorted(rec[k][0] for k in ks)
    print(f"{key[0]} {key[1]} z{key[2]} | disponivel na tentativa #{key[3]} | {len(ks)} secoes | recebidas {hs[0].strftime('%H:%M')}..{hs[-1].strftime('%H:%M')}")
out["grupos_404"] = [[list(k[:3]), k[3], len(v)] for k, v in sorted(g.items())]

print("\n=== F. Carimbos 'da/ha' do indice -cs.json (publicacao, NAO chegada) ===")
carimbos = Counter(); tem = 0
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    d = json.load(open(f, encoding="utf-8"))
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" in s:
                    carimbos[(s["da"], s["ha"][:5])] += 1; tem += 1
print("secoes com carimbo:", tem)
print("minutos de carimbo mais frequentes:", [(f"{a} {b}", n) for (a, b), n in carimbos.most_common(8)])
dif = [(k, rec[k][0], None) for k in rec][:0]
atras = 0
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    d = json.load(open(f, encoding="utf-8"))
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                if "da" in s and (uf, m["cd"], z["cd"], s["ns"]) in rec:
                    cs = datetime.strptime(s["da"] + " " + s["ha"], fmt)
                    if (cs - rec[(uf, m["cd"], z["cd"], s["ns"])][0]).total_seconds() > 3600:
                        atras += 1
print("secoes cujo carimbo do indice e >1h posterior ao hr de recebimento:", atras, f"({atras / tem * 100:.1f}%)")
out["carimbo_indice_mais_1h_depois"] = atras
json.dump(out, open(os.path.join(RAIZ, "dados/atrasos.json"), "w"), ensure_ascii=False, indent=1)
