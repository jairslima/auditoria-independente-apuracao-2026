"""Fase 8b: reprocessa as secoes que falharam na fase 8 (urna de contingencia) e mescla em dados/cadeia_secao.csv."""
import csv, os, sys
from concurrent.futures import ProcessPoolExecutor
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fase8_cadeia_todos import trabalha, RAIZ
if __name__ == "__main__":
    p = os.path.join(RAIZ, "dados/cadeia_secao.csv")
    rows = list(csv.reader(open(p, encoding="utf-8")))
    cab, dados = rows[0], rows[1:]
    falhas = [i for i, r in enumerate(dados) if r[9]]
    def caminho(r):
        return os.path.join(RAIZ, "dados", "busa" if r[1].endswith(".busa") else os.path.join("bu", r[0]), r[1]) if r[1].endswith(".busa") else os.path.join(RAIZ, "dados", "bu", r[0], r[1])
    arqs = [caminho(dados[i]) for i in falhas]
    print("reprocessando:", len(arqs), flush=True)
    with ProcessPoolExecutor(8) as ex:
        for i, novo in zip(falhas, ex.map(trabalha, arqs, chunksize=50)):
            dados[i] = list(map(str, novo))
    with open(p, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(cab); w.writerows(dados)
    print("restam com erro:", sum(1 for r in dados if r[9]), flush=True)
