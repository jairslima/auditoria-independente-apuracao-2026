"""Verifica a CADEIA DE HASHES das tuplas do BU de 2026 (especificacao oficial do TSE, docs_tse/spec2026).
hash0 = SHA512("pleito|eleicao|mun|zona|sec|codCarga") ; hash_i = SHA512(f"{hash_{i-1}}|{ordem}|{cargo}|{tipo}|{qtd}[|{codigo}|{partido}]").
Compara cada hash e o hash final (ultimoHashVotosVotavel) com o gravado no BU. A assinatura ECDSA do hash final e tratada a parte."""
import hashlib, os
import asn1tools

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ASN1 = os.path.join(RAIZ, "docs_tse", "spec2026", "spec", "bu.asn1")
_CONV = None


def conv():
    global _CONV
    if _CONV is None:
        _CONV = asn1tools.compile_files([ASN1], codec="ber", numeric_enums=True)
    return _CONV


def verifica_cadeia(raw: bytes) -> dict:
    c = conv()
    env = c.decode("EntidadeEnvelopeGenerico", bytearray(raw))
    bu = c.decode("EntidadeBoletimUrna", env["conteudo"])
    corr = bu["urna"]["correspondenciaResultado"]
    tipo_id, mzs = corr["identificacao"]
    if tipo_id == "identificacaoContingencia":
        # urna de contingencia: a identificacao da urna nao tem secao; vale a secao real do BU (validado em 60/60 casos)
        mzs = bu["identificacaoSecao"]
    mun, zon, sec = mzs["municipioZona"]["municipio"], mzs["municipioZona"]["zona"], mzs["secao"]
    cod_carga = corr["carga"]["codigoCarga"]
    id_pleito = bu["cabecalho"]["idEleitoral"][1]
    erros_tupla = erros_ordem = erros_final = n_tuplas = 0
    finais = []
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        h = hashlib.sha512(f"{id_pleito:05}|{rpe['idEleicao']:05}|{mun:05}|{zon:04}|{sec:04}|{cod_carga:24}".encode("iso8859-1")).digest().hex().upper()
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                ordem = 0
                for vv in tvc["votosVotaveis"]:
                    ordem += 1
                    n_tuplas += 1
                    if "identificacaoVotavel" in vv:
                        i = vv["identificacaoVotavel"]
                        txt = f"{h}|{ordem}|{cargo}|{vv['tipoVoto']}|{vv['quantidadeVotos']}|{i['codigo']}|{i['partido']}"
                    else:
                        txt = f"{h}|{ordem}|{cargo}|{vv['tipoVoto']}|{vv['quantidadeVotos']}"
                    h = hashlib.sha512(txt.encode("iso8859-1")).digest().hex().upper()
                    if h != bytes(vv["hash"]).hex().upper():
                        erros_tupla += 1
                    if ordem != vv["ordemGeracaoHash"]:
                        erros_ordem += 1
        if h != bytes(rpe["ultimoHashVotosVotavel"]).hex().upper():
            erros_final += 1
        finais.append((rpe["idEleicao"], h, bytes(rpe["assinaturaUltimoHashVotosVotavel"]).hex()))
    return {"n_tuplas": n_tuplas, "erros_tupla": erros_tupla, "erros_ordem": erros_ordem, "erros_final": erros_final,
            "finais": finais, "bu": bu}


if __name__ == "__main__":
    import sys
    for p in sys.argv[1:]:
        try:
            r = verifica_cadeia(open(p, "rb").read())
            print(p, "->", {k: v for k, v in r.items() if k not in ("bu", "finais")}, "| eleicoes:", [f[0] for f in r["finais"]])
        except Exception as e:
            print(p, "-> ERRO", repr(e)[:300])
