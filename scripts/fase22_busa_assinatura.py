# -*- coding: utf-8 -*-
"""Fase 22: verifica a assinatura das 31 secoes do Sistema de Apuracao (sa.vsc), usando a mesma estrutura
EntidadeAssinaturaEcourna do vota.vsc e as funcoes oficiais do TSE (docs_tse/spec2026/python/lib/mr_util.py).
Para cada secao: (a) certificado de hardware valido contra as chaves raiz do TSE; (b) hash de cada arquivo publicado
(busa.dat, rdv.dat, logsa.jez) igual ao hash assinado; (c) assinatura de hardware de cada arquivo valida;
(d) hash do conteudo auto-assinado (hardware e software) confere.
Autoria: Auditoria Independente da Apuracao 2026 by Jair Lima. Saida: resultados/fase22_busa_assinatura.csv"""
import csv, hashlib, json, os, sys, urllib.request

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(RAIZ, "docs_tse", "spec2026", "python"))
from lib import mr_util as m  # noqa: E402
import asn1tools  # noqa: E402

B = "https://resultados.tse.jus.br/oficial/ele2026/arquivo-urna/3220/dados"
DIR = os.path.join(RAIZ, "dados", "sa")
os.makedirs(DIR, exist_ok=True)
CONV = asn1tools.compile_files([os.path.join(RAIZ, "docs_tse", "spec2026", "spec", "assinatura.asn1")], codec="ber", numeric_enums=True)


def pega(k, hsh, nome):
    dest = os.path.join(DIR, nome)
    if not (os.path.exists(dest) and os.path.getsize(dest) > 0):
        open(dest, "wb").write(urllib.request.urlopen(f"{B}/{k[0]}/{k[1]}/{k[2]}/{k[3]}/{hsh}/{nome}", timeout=90).read())
    return dest


linhas = []
for l in open(os.path.join(RAIZ, "dados", "aux.jsonl"), encoding="utf-8"):
    j = json.loads(l)
    if j["status"] != 200:
        continue
    a = json.loads(j["aux"])
    h = a["hashes"][-1]
    if not any(x["tp"] == "busa" for x in h["arq"]):
        continue
    k = (j["uf"], j["mun"], j["zona"], j["sec"])
    r = {"UF": k[0].upper(), "mun": k[1], "zona": k[2], "secao": k[3], "cert_valido": "", "cn_cert": "", "arquivos_assinados": "",
         "hash_ok": 0, "hash_falha": 0, "assin_ok": 0, "assin_falha": 0, "nao_publicados": "", "auto_hash_hw": "", "auto_hash_sw": "", "erro": ""}
    try:
        vsc = next(x["nm"] for x in h["arq"] if x["tp"] == "sa")
        for x in h["arq"]:
            pega(k, h["hash"], x["nm"])
        raw = open(os.path.join(DIR, vsc), "rb").read()
        ent = CONV.decode("EntidadeAssinaturaEcourna", bytearray(raw))
        modelo = m._modelo(ent["origemAssinaturaHW"]["modeloEquipamento"])
        tipo, cert = ent["assinaturaHW"]["informacaoChave"]
        x509 = m.decode_x509(m.converte_certificado_para_x509(cert, modelo))
        _, _, chave, verif = m.extrai_chave_do_certificado(x509)
        r["cn_cert"] = m.common_name(x509["tbsCertificate"]["subject"][1])
        try:
            r["cert_valido"] = int(bool(m.valida_certificado(x509, verif)))
        except Exception:
            r["cert_valido"] = 0
        for campo, col in (("assinaturaHW", "auto_hash_hw"), ("assinaturaSW", "auto_hash_sw")):
            e = ent[campo]
            r[col] = int(hashlib.sha512(e["conteudoAutoAssinado"]).digest() == e["autoAssinado"]["assinatura"]["hash"])
        cont = CONV.decode("Assinatura", ent["assinaturaHW"]["conteudoAutoAssinado"])
        nomes, falt = [], []
        for arq in cont["arquivosAssinados"]:
            nome = arq["nomeArquivo"]
            nomes.append(nome)
            hsh = arq["assinatura"]["hash"]
            p = os.path.join(DIR, nome)
            if not os.path.exists(p):
                falt.append(nome.split("-", 1)[-1])
            elif hashlib.sha512(open(p, "rb").read()).digest() == hsh:
                r["hash_ok"] += 1
            else:
                r["hash_falha"] += 1
            if verif.verify(hashlib.sha512(hsh).digest(), arq["assinatura"]["assinatura"], chave):
                r["assin_ok"] += 1
            else:
                r["assin_falha"] += 1
        r["arquivos_assinados"] = ",".join(n.split("-", 1)[-1] for n in nomes)
        r["nao_publicados"] = ",".join(falt)
    except Exception as e:
        r["erro"] = repr(e)[:200]
    linhas.append(r)
    print(r["UF"], r["mun"], r["zona"], r["secao"], "cert", r["cert_valido"], "hash", r["hash_ok"], r["hash_falha"], "assin", r["assin_ok"], r["assin_falha"], r["nao_publicados"], r["erro"], flush=True)

out = os.path.join(RAIZ, "resultados", "fase22_busa_assinatura.csv")
w = csv.DictWriter(open(out, "w", newline="", encoding="utf-8-sig"), fieldnames=list(linhas[0]), delimiter=";")
w.writeheader()
w.writerows(linhas)
print("secoes:", len(linhas), "| cert valido:", sum(1 for x in linhas if x["cert_valido"] == 1), "| assin_falha total:", sum(x["assin_falha"] for x in linhas),
      "| hash_falha total:", sum(x["hash_falha"] for x in linhas), "| erros:", sum(1 for x in linhas if x["erro"]))
