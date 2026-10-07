"""Fase 9: verifica, por secao, (a) a assinatura ECDSA/EdDSA do hash final do BU (Presidente, eleicao 6257) com a chave do
certificado de hardware da urna (vota.vsc) e (b) o certificado contra as chaves raiz do TSE (mr_util._CHAVES_RAIZ).
Streaming: baixa o .vsc, verifica e descarta. Ordem ALEATORIA (semente 2026): qualquer prefixo e uma amostra aleatoria.
Retomavel: pula secoes ja presentes em dados/assinaturas_secao.csv.  Entrada: dados/aux.jsonl, dados/cadeia_secao.csv."""
import csv, hashlib, json, os, random, sys, time, urllib.request, urllib.error
from concurrent.futures import ProcessPoolExecutor

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY2026 = os.path.join(RAIZ, "docs_tse", "spec2026", "python")
sys.path.insert(0, PY2026)
from lib import mr_util as m  # noqa: E402
import asn1tools  # noqa: E402

B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
SAIDA = os.path.join(RAIZ, "dados", "assinaturas_secao.csv")
CAMPOS = ["uf", "mun", "zona", "sec", "status", "modelo_hw", "cn_cert", "emissor", "cert_valido", "assin_valida", "n_urna_cn", "erro"]
_CONV = None


def conv():
    global _CONV
    if _CONV is None:
        _CONV = asn1tools.compile_files([os.path.join(RAIZ, "docs_tse", "spec2026", "spec", "assinatura.asn1")], codec="ber", numeric_enums=True)
    return _CONV


def baixa(url):
    for i in range(6):
        try:
            return urllib.request.urlopen(url, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code == 404:
                return None
        except Exception:
            pass
        time.sleep(5 * (2 ** i))
    return None


def trabalha(a):
    k, url, hash_final, assin_hex = a
    base = {"uf": k[0], "mun": k[1], "zona": k[2], "sec": k[3], "status": "", "modelo_hw": "", "cn_cert": "", "emissor": "",
            "cert_valido": "", "assin_valida": "", "n_urna_cn": "", "erro": ""}
    try:
        raw = baixa(url)
        if raw is None:
            base.update(status="sem_vsc")
            return base
        ent = conv().decode("EntidadeAssinaturaEcourna", bytearray(raw))
        modelo = m._modelo(ent["origemAssinaturaHW"]["modeloEquipamento"])
        tipo, cert = ent["assinaturaHW"]["informacaoChave"]
        if tipo != "certificadoDigital":
            base.update(status="sem_certificado", modelo_hw=str(modelo))
            return base
        x509 = m.decode_x509(m.converte_certificado_para_x509(cert, modelo))
        _, _, chave, verif = m.extrai_chave_do_certificado(x509)
        cn = m.common_name(x509["tbsCertificate"]["subject"][1])
        emissor = m.common_name(x509["tbsCertificate"]["issuer"][1])
        try:
            cert_ok = bool(m.valida_certificado(x509, verif))
        except Exception:
            cert_ok = False
        msg = hashlib.sha512(bytes.fromhex(hash_final)).digest()
        try:
            ass_ok = bool(verif.verify(msg, bytes.fromhex(assin_hex), chave))
        except Exception:
            ass_ok = False
        digs = "".join(ch for ch in cn if ch.isdigit())
        base.update(status="ok", modelo_hw=str(modelo), cn_cert=cn, emissor=emissor, cert_valido=int(cert_ok), assin_valida=int(ass_ok),
                    n_urna_cn=int(digs) if digs else "")
    except Exception as e:
        base.update(status="erro", erro=repr(e)[:160])
    return base


if __name__ == "__main__":
    limite = int(sys.argv[1]) if len(sys.argv) > 1 else None
    cad = {}
    for r in csv.DictReader(open(os.path.join(RAIZ, "dados/cadeia_secao.csv"), encoding="utf-8")):
        cad[(r["uf"], r["arquivo"])] = r
    feitos = set()
    if os.path.exists(SAIDA):
        for r in csv.DictReader(open(SAIDA, encoding="utf-8")):
            feitos.add((r["uf"], r["mun"], r["zona"], r["sec"]))
    ult = {}
    for l in open(os.path.join(RAIZ, "dados/aux.jsonl"), encoding="utf-8"):
        j = json.loads(l)
        if j["status"] == 200 or (j["uf"], j["mun"], j["zona"], j["sec"]) not in ult:
            ult[(j["uf"], j["mun"], j["zona"], j["sec"])] = j
    itens = []
    for k, j in ult.items():
        if j["status"] != 200 or k in feitos:
            continue
        h = json.loads(j["aux"])["hashes"][-1]
        vsc = next((x["nm"] for x in h["arq"] if x["tp"] == "vota"), None)
        c = cad.get((k[0], f"{k[1]}-{k[2]}-{k[3]}.bu"))
        if not vsc or not c or not c["hash_final_6257"]:
            continue
        itens.append((k, f"{B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{h['hash']}/{vsc}", c["hash_final_6257"], c["assinatura_6257"]))
    random.Random(2026).shuffle(itens)
    if limite:
        itens = itens[:limite]
    print("a verificar:", len(itens), "| ja feitos:", len(feitos), flush=True)
    novo = not os.path.exists(SAIDA)
    n = ok = 0
    with ProcessPoolExecutor(4) as ex, open(SAIDA, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=CAMPOS)
        if novo:
            w.writeheader()
        for r in ex.map(trabalha, itens, chunksize=20):
            w.writerow(r)
            n += 1
            ok += 1 if (r["status"] == "ok" and r["assin_valida"] == 1 and r["cert_valido"] == 1) else 0
            if n % 2000 == 0:
                f.flush()
                print(n, "ok_completo:", ok, time.strftime("%H:%M:%S"), flush=True)
    print("fim", n, "ok_completo:", ok, flush=True)
