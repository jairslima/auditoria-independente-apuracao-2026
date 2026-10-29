"""Fase 14: cruza o cadastro de eleitorado por secao (TSE, dados abertos, fonte independente) com o indice de secoes (-cs.json) e com os BUs.
Responde: (1) todas as secoes do cadastro estao no indice? (2) quais as 41 'nao instaladas'? (3) o eleitorado do cadastro bate com o oficial?"""
import csv, glob, json, os, sys
from collections import Counter, defaultdict

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSV = os.path.join(RAIZ, "dados/externos/eleitorado_local_votacao_2026_BRASIL.csv")
csv.field_size_limit(10**7)

cad = {}                      # (uf, mun, zona, sec) -> dict
linhas = 0
vistos_dup = Counter()
with open(CSV, encoding="latin-1", newline="") as f:
    for r in csv.DictReader(f, delimiter=";"):
        linhas += 1
        k = (r["SG_UF"].lower(), r["CD_MUNICIPIO"].zfill(5), r["NR_ZONA"].zfill(4), r["NR_SECAO"].zfill(4))
        vistos_dup[k] += 1
        cad[k] = {"agr": r["DS_TIPO_SECAO_AGREGADA"], "cd_agr": r["CD_TIPO_SECAO_AGREGADA"], "princ": r["NR_SECAO_PRINCIPAL"],
                  "situ": r["DS_SITU_SECAO"], "situ_zona": r["DS_SITU_ZONA"], "situ_local": r["DS_SITU_LOCAL_VOTACAO"],
                  "eleit_sec": int(r["QT_ELEITOR_SECAO"] or 0), "eleit_fed": int(r["QT_ELEITOR_ELEICAO_FEDERAL"] or 0),
                  "eleicao": r["DS_ELEICAO"], "mun": r["NM_MUNICIPIO"], "local": r["NM_LOCAL_VOTACAO"]}
print("linhas no cadastro:", linhas, "| secoes distintas (UF,mun,zona,secao):", len(cad), "| chaves repetidas:", sum(1 for v in vistos_dup.values() if v > 1))
print("tipo de secao:", Counter(v["agr"] for v in cad.values()))
print("situacao da secao:", Counter(v["situ"] for v in cad.values()))
print("situacao da zona:", Counter(v["situ_zona"] for v in cad.values()), "| situacao do local:", Counter(v["situ_local"] for v in cad.values()))
print("eleicao(es) no arquivo:", Counter(v["eleicao"] for v in cad.values()))

# indice do TSE (-cs.json): instaladas (com da/ha) e agregadas (com nsp)
inst, agr = set(), set()
for f in glob.glob(os.path.join(RAIZ, "dados/cs/*-cs.json")):
    uf = os.path.basename(f).split("-")[0]
    d = json.load(open(f, encoding="utf-8"))
    for m in d["abr"][0]["mu"]:
        for z in m["zon"]:
            for s in z["sec"]:
                k = (uf, m["cd"], z["cd"], s["ns"])
                (inst if "da" in s else agr).add(k)
print("\nindice TSE: instaladas", len(inst), "| agregadas", len(agr), "| total", len(inst | agr))

so_cad = set(cad) - (inst | agr)
so_ind = (inst | agr) - set(cad)
print("secoes no CADASTRO e NAO no indice:", len(so_cad), "| no INDICE e NAO no cadastro:", len(so_ind))
print("  cadastro-sem-indice por UF:", Counter(k[0] for k in so_cad).most_common(8))
print("  cadastro-sem-indice por tipo/situacao:", Counter((cad[k]["agr"], cad[k]["situ"]) for k in so_cad).most_common(8))
print("  indice-sem-cadastro por UF:", Counter(k[0] for k in so_ind).most_common(8))
# cadastro: instaladas na visao do cadastro = principais ativas
princ_ativas = {k for k, v in cad.items() if v["agr"] == "Principal" and v["situ"] == "ATIVO"}
print("\ncadastro: principais ativas", len(princ_ativas), "| em instaladas do indice", len(princ_ativas & inst), "| principais ativas fora de 'instaladas':", len(princ_ativas - inst))
fora = princ_ativas - inst
print("  esas por UF:", Counter(k[0] for k in fora).most_common(10))
for k in sorted(fora)[:15]:
    print("   ", k, cad[k]["mun"], "|", cad[k]["local"][:40], "| eleitores", cad[k]["eleit_fed"], "| no indice como", "agregada" if k in agr else "ausente")
print("instaladas do indice fora das 'principais ativas' do cadastro:", len(inst - princ_ativas))
print("agregadas do indice que o cadastro marca como agregada:", sum(1 for k in agr if k in cad and cad[k]["agr"] != "Principal"), "de", len(agr))

# eleitorado
tot_fed = sum(v["eleit_fed"] for v in cad.values())
print("\neleitorado (QT_ELEITOR_ELEICAO_FEDERAL somado, todas as linhas distintas):", f"{tot_fed:,}", "| oficial 'te' = 158.745.502")
tot_p = sum(cad[k]["eleit_fed"] for k in princ_ativas)
print("  so principais ativas:", f"{tot_p:,}", "| so secoes instaladas do indice:", f"{sum(cad[k]['eleit_fed'] for k in inst if k in cad):,}")
json.dump({"linhas": linhas, "cad": len(cad), "indice_inst": len(inst), "indice_agr": len(agr), "so_cadastro": sorted(map(list, so_cad)),
           "so_indice": sorted(map(list, so_ind)), "principais_ativas_fora_instaladas": sorted(map(list, fora))},
          open(os.path.join(RAIZ, "dados/cadastro_cruzamento.json"), "w"), ensure_ascii=False)
