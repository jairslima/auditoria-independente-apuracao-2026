"""Auditoria Independente da Apuração 2026 by Jair Lima.

Fase 30 (25/11/2026): testa, com o arquivo oficial "Detalhe da apuração por seção eleitoral"
(dados abertos do TSE), o horário de recebimento do BU e da 1ª totalização parcial do 2º turno
de Presidente, contra as respostas do TSE de 09/11/2026 (protocolos 83192627165101 e
83236428120806).

Uso: python -I fase30_recebimento_bu_2turno.py <detalhe_votacao_secao_2026.zip> <saida.json>
Fonte: https://cdn.tse.jus.br/estatistica/sead/odsele/detalhe_votacao_secao/detalhe_votacao_secao_2026.zip
Horários em Brasília (conferido: SP, 1º turno, recebimento 04/10 18:37).
"""
import csv
import collections
import datetime as dt
import io
import json
import sys
import zipfile

D = dt.datetime
P = lambda s: D.strptime(s, "%d/%m/%Y %H:%M:%S")
T = lambda h, m, s=0: D(2026, 10, 25, h, m, s)


def cum(lista, limite):
    return sum(1 for x in lista if x <= limite)


def main(zip_path, saida):
    z = zipfile.ZipFile(zip_path)
    t = io.TextIOWrapper(z.open("detalhe_votacao_secao_2026_BR.csv"), encoding="latin-1", newline="")
    r = csv.reader(t, delimiter=";")
    h = next(r)
    ix = {k: i for i, k in enumerate(h)}
    linhas = []
    geracao = set()
    for row in r:
        if row[ix["NR_TURNO"]] != "2":
            continue
        geracao.add((row[ix["DT_GERACAO"]], row[ix["HH_GERACAO"]]))
        linhas.append({
            "rec": P(row[ix["DT_RECEBIMENTO_BU_HOR_TSE"]]),
            "tot": P(row[ix["DT_PRIM_TOT_PARCIAL_HOR_TSE"]]),
            "uf": row[ix["SG_UF"]],
            "origem": row[ix["DS_ORIGEM_VOTO"]],
            "comp": int(row[ix["QT_COMPARECIMENTO"]] or 0),
        })
    rec = sorted(x["rec"] for x in linhas)
    tot = sorted(x["tot"] for x in linhas)
    janela = [x for x in linhas if T(17, 7, 38) <= x["rec"] < T(19, 0)]
    res = {
        "secoes_turno2": len(linhas),
        "geracao_arquivo": sorted(geracao),
        "recebimento_acumulado": {k: cum(rec, v) for k, v in {
            "ate_17:06:31": T(17, 6, 31), "ate_17:07:01": T(17, 7, 1),
            "ate_17:07:59": T(17, 7, 59), "ate_19:00:00": T(19, 0)}.items()},
        "primeira_totalizacao_acumulada": {k: cum(tot, v) for k, v in {
            "ate_17:06:31": T(17, 6, 31), "ate_17:07:01": T(17, 7, 1),
            "ate_17:07:59": T(17, 7, 59), "ate_19:00:00": T(19, 0)}.items()},
        "ultima_totalizacao_antes_das_18h": str(max(x for x in tot if x < T(18, 0))),
        "recebidos_17h07m38_a_19h": len(janela),
        "recebidos_17h07m38_a_19h_por_origem": dict(collections.Counter(x["origem"] for x in janela)),
        "recebidos_17h07m38_a_19h_por_uf": dict(collections.Counter(x["uf"] for x in janela)),
        "recebidos_17h07m38_a_19h_com_comparecimento_zero": sum(1 for x in janela if x["comp"] == 0),
        "recebidos_19h00_a_19h10": sum(1 for x in rec if T(19, 0) <= x < T(19, 10)),
        "recebidos_19h10_a_19h20": sum(1 for x in rec if T(19, 10) <= x < T(19, 20)),
        "ultimo_recebimento": str(rec[-1]),
    }
    with open(saida, "w", encoding="utf-8") as f:
        json.dump(res, f, ensure_ascii=False, indent=1)
    print(json.dumps(res, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
