"""Resumo da fase 8: erros de decodificacao, cadeia de hashes e concordancia do 2o parser (asn1tools) com o 1o (BER proprio)."""
import csv, json
rows = list(csv.DictReader(open('dados/cadeia_secao.csv', encoding='utf-8')))
print("secoes:", len(rows))
print("erro de decodificacao:", sum(1 for r in rows if r['erro_decodificacao']))
print("secoes com erro de hash de tupla:", sum(1 for r in rows if int(r['err_tupla']) > 0), "| de ordem:", sum(1 for r in rows if int(r['err_ordem']) > 0), "| hash final:", sum(1 for r in rows if int(r['err_final']) > 0))
print("tuplas verificadas:", f"{sum(int(r['n_tuplas']) for r in rows):,}")
for r in [r for r in rows if r['erro_decodificacao']][:5]: print("  ", r['uf'], r['arquivo'], r['erro_decodificacao'])
meu = {}
for r in csv.DictReader(open('dados/votos_secao.csv', encoding='utf-8')):
    meu[(r['uf'], f"{r['mun']}-{r['zona']}-{r['sec']}")] = {k[1:]: int(v) for k, v in r.items() if k.startswith('c') and k != 'cand'} | {'branco': int(r['branco']), 'nulo': int(r['nulo'])}
dif = comp = 0; ex = []
for r in rows:
    if not r['pres_json']: continue
    k = (r['uf'], r['arquivo'].rsplit('.', 1)[0])
    if k not in meu: continue
    comp += 1
    p = {a: b for a, b in json.loads(r['pres_json']).items() if b}
    m = {a: b for a, b in meu[k].items() if b}
    if p != m:
        dif += 1
        if len(ex) < 3: ex.append((k, p, m))
print("2o parser x 1o parser: comparadas", comp, "| divergentes", dif)
for e in ex: print("  ", e)
