"""FASE 24 (2026-10-19): correspondência de urnas esperada x efetivada em Pernambuco, para as seções da resposta do TRE-PE.

Entradas (baixadas de cdn.tse.jus.br, ver PROJECT.md): dados/externos/correspondencia_PE/{esperada,efetivada}/
  - csec_1t_PE_041020261259.csv (urna esperada por seção, gerada em 04/10/2026 12:59:37)
  - ceft_1t_PE_051020261049.csv (correspondência efetivada, gerada em 05/10/2026 10:49:30)
Saída: resultados/fase24_correspondencia_pe.json
Conclusão que o script sustenta: urna esperada == urna efetivada nas 60 seções do anexo e nas 127 seções com BU rejeitado;
sem divergência e com origem 'Urna Eletrônica'. Não prova o conteúdo do BU (isso é o hash), só quem gerou o resultado."""
import csv, collections, json, pathlib

RAIZ = pathlib.Path(__file__).resolve().parent.parent
D = RAIZ / "dados/externos/correspondencia_PE"
RESP = RAIZ / "pedidos_lai/respostas/TRE-PE_2026-10-19/_analise/bus_rejeitados_PE.csv"
ANEXO = RAIZ / "pedidos_lai/anexos/anexo_TRE-PE.csv"


def ler(p):
    return list(csv.DictReader(open(p, encoding="latin-1", newline=""), delimiter=";", quotechar='"'))


esp = ler(D / "esperada/csec_1t_PE_041020261259.csv")
eft = ler(D / "efetivada/ceft_1t_PE_051020261049.csv")
E = {(int(r["NR_ZONA"]), int(r["NR_SECAO"])): r for r in esp}
F = {(int(r["NR_ZONA"]), int(r["NR_SECAO"])): r for r in eft}
anexo = [(int(r["zona"]), int(r["secao"])) for r in csv.DictReader(open(ANEXO, encoding="utf-8-sig"), delimiter=";")]
rej = sorted({(int(r["zona"]), int(r["secao"])) for r in csv.DictReader(open(RESP, encoding="utf-8"))})


def resumo(chaves):
    ach = [k for k in chaves if k in F]
    return {
        "secoes": len(chaves), "encontradas": len(ach),
        "urna_esperada_igual_efetivada": sum(1 for k in ach if F[k]["NR_URNA_ESPERADA"] == F[k]["NR_URNA_EFETIVADA"]),
        "tp_divergencia": dict(collections.Counter(F[k]["TP_DIVERGENCIA"] or "(nenhuma)" for k in ach)),
        "origem_do_voto": dict(collections.Counter(F[k]["DS_ORIGEM_VOTO"] for k in ach)),
    }


saida = {
    "gerado_esperada": esp[0]["DT_GERACAO"] + " " + esp[0]["HH_GERACAO"],
    "gerado_efetivada": eft[0]["DT_GERACAO"] + " " + eft[0]["HH_GERACAO"],
    "secoes_PE_esperada": len(E), "secoes_PE_efetivada": len(F),
    "so_em_uma_das_listas": len(set(E) ^ set(F)),
    "esperada_mudou_entre_os_arquivos": sum(1 for k in E if k in F and E[k]["NR_URNA_ESPERADA"] != F[k]["NR_URNA_ESPERADA"]),
    "pe_urna_esperada_diferente_da_efetivada": sum(1 for k in F if F[k]["NR_URNA_ESPERADA"] != F[k]["NR_URNA_EFETIVADA"]),
    "pe_tp_divergencia": dict(collections.Counter(r["TP_DIVERGENCIA"] or "(nenhuma)" for r in eft)),
    "pe_origem_do_voto": dict(collections.Counter(r["DS_ORIGEM_VOTO"] for r in eft)),
    "anexo_60": resumo(anexo),
    "rejeitadas_127": resumo(rej),
}
out = RAIZ / "resultados/fase24_correspondencia_pe.json"
out.write_text(json.dumps(saida, ensure_ascii=False, indent=2), encoding="utf-8")
print(json.dumps(saida, ensure_ascii=False, indent=2))
