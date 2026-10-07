"""Fase 16: verifica, POR AMOSTRAGEM, a assinatura ECDSA/EdDSA do hash final da eleicao ESTADUAL (6259) em cada BU.
Amostra = 20.000 secoes sorteadas (semente 2026) + TODAS as que atrasaram (68 com 404 na 1a coleta + 743 registradas depois de 23h41).
Mesma logica da fase 9 (Presidente): chave do certificado de hardware (vota.vsc), msg = SHA-512 do hash final em bytes. Saida: dados/assinaturas_estadual.csv"""
import csv, hashlib, json, os, random, sys, time
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fase9_assinaturas as f9
from bu_cadeia import conv as conv_bu, RAIZ

m = f9.m
SAIDA = os.path.join(RAIZ, "dados", "assinaturas_estadual.csv")
CAMPOS = ["uf", "mun", "zona", "sec", "grupo", "status", "modelo_hw", "cert_ok", "assin_estadual_valida", "erro"]


def trabalha(a):
    k, url, grupo = a
    base = {"uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "grupo": grupo, "status": "", "modelo_hw": "", "cert_ok": "", "assin_estadual_valida": "", "erro": ""}
    try:
        caminho = os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu")
        c = conv_bu()
        bu = c.decode("EntidadeBoletimUrna", c.decode("EntidadeEnvelopeGenerico", bytearray(open(caminho, "rb").read()))["conteudo"])
        rpe = next(x for x in bu["resultadosVotacaoPorEleicao"] if x["idEleicao"] == 6259)
        hash_final = bytes(rpe["ultimoHashVotosVotavel"]).hex()
        assinatura = bytes(rpe["assinaturaUltimoHashVotosVotavel"])
        raw = f9.baixa(url)
        if raw is None:
            base.update(status="sem_vsc"); return base
        ent = f9.conv().decode("EntidadeAssinaturaEcourna", bytearray(raw))
        modelo = m._modelo(ent["origemAssinaturaHW"]["modeloEquipamento"])
        tipo, cert = ent["assinaturaHW"]["informacaoChave"]
        x509 = m.decode_x509(m.converte_certificado_para_x509(cert, modelo))
        _, _, chave, verif = m.extrai_chave_do_certificado(x509)
        try:
            cert_ok = bool(m.valida_certificado(x509, verif))
        except Exception:
            cert_ok = False
        msg = hashlib.sha512(bytes.fromhex(hash_final)).digest()
        try:
            ok = bool(verif.verify(msg, assinatura, chave))
        except Exception:
            ok = False
        base.update(status="ok", modelo_hw=str(modelo), cert_ok=int(cert_ok), assin_estadual_valida=int(ok))
    except Exception as e:
        base.update(status="erro", erro=repr(e)[:160])
    return base


if __name__ == "__main__":
    ult = {}
    for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        if j["status"] == 200 or (j["uf"], j["mun"], j["zona"], j["sec"]) not in ult:
            ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
    info = {}
    for k, j in ult.items():
        if j["status"] != 200:
            continue
        a = json.loads(j["aux"]); h = a["hashes"][-1]
        vsc = next((x["nm"] for x in h["arq"] if x["tp"] == "vota"), None)
        if vsc and os.path.exists(os.path.join(RAIZ, "dados", "bu", k[0], f"{k[1]}-{k[2]}-{k[3]}.bu")):
            info[k] = (f"{f9.B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{vsc}", datetime.strptime(h["dr"] + " " + h["hr"], "%d/%m/%Y %H:%M:%S"))
    # grupos que atrasaram
    hist = {}
    for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        hist.setdefault((j["uf"], j["mun"], j["zona"], j["sec"]), []).append(j["status"])
    g404 = {k for k, h in hist.items() if h[0] == 404 and k in info}
    cauda = {k for k, (u, t) in info.items() if t > datetime(2026, 10, 4, 23, 41)}
    SEMENTE = int(os.environ.get("SEMENTE", 2026)); AMOSTRA = int(os.environ.get("AMOSTRA", 20000)); GRUPO = os.environ.get("GRUPO", "sorteio")
    rnd = random.Random(SEMENTE)
    feitos = set()
    if os.path.exists(SAIDA):
        for r in csv.DictReader(open(SAIDA, encoding="utf-8")):
            feitos.add((r["uf"], r["mun"], r["zona"], r["sec"]))
    # exterior (zz) nao tem eleicao estadual; secoes ja verificadas ficam fora do novo sorteio
    restantes = sorted(k for k in set(info) - g404 - cauda - feitos if k[0] != "zz")
    sorteio = set(rnd.sample(restantes, min(AMOSTRA, len(restantes))))
    plano = [(k, "atrasou_404") for k in sorted(g404)] + [(k, "cauda_apos_2341") for k in sorted(cauda - g404)] + [(k, GRUPO) for k in sorted(sorteio)]
    itens = [(k, info[k][0], g) for k, g in plano if k not in feitos]
    rnd.shuffle(itens)
    print(f"plano: {len(plano)} secoes (404: {len(g404)}, cauda: {len(cauda - g404)}, sorteio '{GRUPO}': {len(sorteio)}, semente {SEMENTE}) | a fazer: {len(itens)}", flush=True)
    novo = not os.path.exists(SAIDA)
    n = ok = 0
    with ProcessPoolExecutor(int(os.environ.get("PROCS", 6))) as ex, open(SAIDA, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        for r in ex.map(trabalha, itens, chunksize=10):
            w.writerow(r); n += 1
            ok += 1 if (r["status"] == "ok" and r["assin_estadual_valida"] == 1) else 0
            if n % 1000 == 0:
                f.flush(); print(n, "validas:", ok, time.strftime("%H:%M:%S"), flush=True)
    print("fim", n, "validas:", ok, flush=True)
