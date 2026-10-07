"""Fase 8: cadeia de hashes das tuplas em TODOS os BUs + segundo parser (asn1tools/spec oficial 2026) para os votos de Presidente.
Saida: dados/cadeia_secao.csv (uma linha por secao) e dados/cadeia_resumo.json."""
import csv, glob, json, os, sys
from concurrent.futures import ProcessPoolExecutor

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bu_cadeia import verifica_cadeia

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def trabalha(caminho):
    nome = os.path.basename(caminho)
    uf = os.path.basename(os.path.dirname(caminho))
    try:
        r = verifica_cadeia(open(caminho, "rb").read())
        pres = {}
        for rpe in r["bu"]["resultadosVotacaoPorEleicao"]:
            if rpe["idEleicao"] != 6257:
                continue
            for rv in rpe["resultadosVotacao"]:
                for tvc in rv["totaisVotosCargo"]:
                    for vv in tvc["votosVotaveis"]:
                        t = vv["tipoVoto"]
                        k = vv["identificacaoVotavel"]["codigo"] if t == 1 else {2: "branco", 3: "nulo"}.get(t, f"tipo{t}")
                        pres[k] = pres.get(k, 0) + vv["quantidadeVotos"]
        f6257 = next((f for f in r["finais"] if f[0] == 6257), (None, "", ""))
        return (uf, nome, r["n_tuplas"], r["erros_tupla"], r["erros_ordem"], r["erros_final"], f6257[1], f6257[2], json.dumps({str(a): b for a, b in pres.items()}, sort_keys=True), "")
    except Exception as e:
        return (uf, nome, 0, 0, 0, 0, "", "", "", repr(e)[:200])


if __name__ == "__main__":
    arqs = sorted(glob.glob(os.path.join(RAIZ, "dados/bu/*/*.bu")) + glob.glob(os.path.join(RAIZ, "dados/busa/*.busa")))
    print("arquivos:", len(arqs), flush=True)
    n = 0
    with ProcessPoolExecutor(8) as ex, open(os.path.join(RAIZ, "dados/cadeia_secao.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["uf", "arquivo", "n_tuplas", "err_tupla", "err_ordem", "err_final", "hash_final_6257", "assinatura_6257", "pres_json", "erro_decodificacao"])
        for row in ex.map(trabalha, arqs, chunksize=200):
            w.writerow(row)
            n += 1
            if n % 50000 == 0:
                print(n, flush=True)
    print("fim", n, flush=True)
