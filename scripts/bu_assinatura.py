"""Verifica as assinaturas Ed25519 das tuplas de votos do BU (especificacao oficial do TSE, docs_tse/spec).
Mesma logica de docs_tse/spec/python/bu_assinatura_tuplas.py, usando 'cryptography' em vez de 'ed25519'.
Mensagem assinada = SHA-512 de f"{codigoCargo}{tipoVoto}{qtd}{codigo}{partido}{carga}" (codigo/partido so p/ tipos 1 e 4)."""
import hashlib, os, sys
import asn1tools
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SPEC = os.path.join(RAIZ, "docs_tse", "spec", "spec")
CONV = asn1tools.compile_files([os.path.join(SPEC, os.environ.get("BU_ASN1", "bu.asn1"))], numeric_enums=True)


def verifica_bu(raw: bytes):
    """Retorna dict: chave (hex), carga, n_ok, n_falha, falhas[...], cargos."""
    env = CONV.decode("EntidadeEnvelopeGenerico", bytearray(raw))
    bu = CONV.decode("EntidadeBoletimUrna", env["conteudo"])
    chave = bu["chaveAssinaturaVotosVotavel"]
    vk = Ed25519PublicKey.from_public_bytes(bytes(chave))
    carga = bu["urna"]["correspondenciaResultado"]["carga"]["codigoCarga"]
    ok = falha = 0
    falhas = []
    for rpe in bu["resultadosVotacaoPorEleicao"]:
        for rv in rpe["resultadosVotacao"]:
            for tvc in rv["totaisVotosCargo"]:
                cargo = tvc["codigoCargo"][1]
                for vv in tvc["votosVotaveis"]:
                    tipo, qtd = vv["tipoVoto"], vv["quantidadeVotos"]
                    ident = ""
                    if tipo in (1, 4):
                        i = vv["identificacaoVotavel"]
                        ident = f"{i['codigo']}{i['partido']}"
                    claro = f"{cargo}{tipo}{qtd}{ident}{carga}".encode("iso8859-1")
                    try:
                        vk.verify(bytes(vv["assinatura"]), hashlib.sha512(claro).digest())
                        ok += 1
                    except InvalidSignature:
                        falha += 1
                        falhas.append((cargo, tipo, qtd, ident))
    return {"chave": bytes(chave).hex(), "carga": carga, "n_ok": ok, "n_falha": falha, "falhas": falhas}


if __name__ == "__main__":
    for p in sys.argv[1:]:
        try:
            r = verifica_bu(open(p, "rb").read())
            print(p, "->", r["n_ok"], "ok,", r["n_falha"], "falhas | carga", r["carga"], "| chave", r["chave"][:16] + "...")
        except Exception as e:
            print(p, "-> ERRO", repr(e)[:200])
