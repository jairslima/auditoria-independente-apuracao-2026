"""Fase 13: urnas substituidas/contingencia/recuperacao e consistencia interna de cada BU.
Por BU (todos os .bu e .busa): tipoUrna, tipoArquivo, tipo de identificacao, historico de correspondencias (urnas anteriores),
qtdEleitoresAptos e qtdComparecimento (Presidente, eleicao 6257), soma dos votos de Presidente. Saida: dados/urnas_tipo.csv."""
import csv, glob, json, os, sys
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import conv, RAIZ


def trabalha(caminho):
    nome = os.path.basename(caminho)
    uf = os.path.basename(os.path.dirname(caminho)) if caminho.endswith(".bu") else nome.split("-")[0]
    try:
        c = conv()
        bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
        u = bu["urna"]
        corr = u["correspondenciaResultado"]
        tipo_id = corr["identificacao"][0]
        hist = bu.get("historicoCorrespondencias") or []
        hist_urnas = []
        for h in hist:
            hist_urnas.append(str(h["carga"]["numeroInternoUrna"]))
        apt = comp = soma = None
        for rpe in bu["resultadosVotacaoPorEleicao"]:
            if rpe["idEleicao"] == 6257:
                apt = rpe["qtdEleitoresAptos"]
                for rv in rpe["resultadosVotacao"]:
                    comp = rv["qtdComparecimento"]
                    soma = sum(vv["quantidadeVotos"] for tvc in rv["totaisVotosCargo"] for vv in tvc["votosVotaveis"])
        return [uf, nome, u["tipoUrna"], u["tipoArquivo"], tipo_id, len(hist), ";".join(hist_urnas), corr["carga"]["numeroInternoUrna"], apt, comp, soma, ""]
    except Exception as e:
        return [uf, nome, "", "", "", "", "", "", "", "", "", repr(e)[:150]]


if __name__ == "__main__":
    arqs = sorted(glob.glob(os.path.join(RAIZ, "dados/bu/*/*.bu")) + glob.glob(os.path.join(RAIZ, "dados/busa/*.busa")))
    print("arquivos:", len(arqs), flush=True)
    n = 0
    with ProcessPoolExecutor(3) as ex, open(os.path.join(RAIZ, "dados/urnas_tipo.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["uf", "arquivo", "tipoUrna", "tipoArquivo", "tipo_identificacao", "n_historico", "urnas_anteriores", "urna_interna", "aptos_6257", "comparecimento_6257", "soma_votos_6257", "erro"])
        for r in ex.map(trabalha, arqs, chunksize=200):
            w.writerow(r)
            n += 1
            if n % 50000 == 0:
                print(n, flush=True)
    print("fim", n, flush=True)
