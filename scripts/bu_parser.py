"""Parser independente do boletim de urna (BU, BER) para o cargo Presidente (eleicao 6257).
Sem dependencias externas. Estrutura inferida e VALIDADA contra soma de comparecimento do proprio BU e totais oficiais."""
import json, sys


def tlv(b, i):
    t = b[i]; i += 1
    cls, cons, tag = t >> 6, (t >> 5) & 1, t & 0x1F
    if tag == 0x1F:
        tag = 0
        while True:
            x = b[i]; i += 1
            tag = (tag << 7) | (x & 0x7F)
            if not x & 0x80:
                break
    l = b[i]; i += 1
    if l & 0x80:
        n = l & 0x7F
        l = int.from_bytes(b[i:i + n], "big"); i += n
    return cls, cons, tag, i, l


def filhos(b, ini, fim):
    out = []
    i = ini
    while i < fim:
        cls, cons, tag, vi, l = tlv(b, i)
        out.append((cls, cons, tag, vi, vi + l))
        i = vi + l
    return out


def inteiro(b, f):
    return int.from_bytes(b[f[3]:f[4]], "big")


def texto(b, f):
    return b[f[3]:f[4]].decode("ascii", "replace")


def parse_bu(raw):
    """Retorna dict com votos de presidente. Levanta ValueError se estrutura inesperada."""
    top = filhos(raw, 0, len(raw))
    if len(top) != 1:
        raise ValueError("raiz")
    corpo = filhos(raw, top[0][3], top[0][4])
    # octet string (0:4) com o BU interno
    oct_ = next(f for f in corpo if f[0] == 0 and f[2] == 4)
    ib = raw[oct_[3]:oct_[4]]
    _, _, _, vi, l = tlv(ib, 0)
    nivel = filhos(ib, vi, vi + l)
    ts = [texto(ib, f) for f in nivel if f[0] == 0 and f[2] == 27]
    # sequencia grande com os resultados por eleicao: a ultima [0:16] do nivel
    resultados = max((f for f in nivel if f[0] == 0 and f[1] == 1 and f[2] == 16), key=lambda f: f[4] - f[3])
    res = {"ts_bu": ts, "pres": None}
    for el in filhos(ib, resultados[3], resultados[4]):
        cs = filhos(ib, el[3], el[4])
        if not cs or cs[0][2] != 2:
            continue
        if inteiro(ib, cs[0]) != 6257:
            continue
        # procurar recursivamente as entradas [2:1] tipo, [2:2] qtd
        votos = {}
        comparec = None

        def desce(a, z):
            for f in filhos(ib, a, z):
                if f[1] == 1:
                    sub = filhos(ib, f[3], f[4])
                    if len(sub) >= 2 and sub[0][0] == 2 and sub[0][2] == 1 and sub[1][0] == 2 and sub[1][2] == 2:
                        tipo = inteiro(ib, sub[0]); q = inteiro(ib, sub[1])
                        cand = None
                        for s in sub[2:]:
                            if s[0] == 2 and s[2] == 3:
                                ss = filhos(ib, s[3], s[4])
                                cand = inteiro(ib, ss[0])
                        chave = cand if tipo == 1 else {2: "branco", 3: "nulo"}.get(tipo, f"tipo{tipo}")
                        votos[chave] = votos.get(chave, 0) + q
                    else:
                        desce(f[3], f[4])
        desce(el[3], el[4])
        # comparecimento declarado: inteiro [0:2] logo apos o tipo de bloco no nivel do resultado (256 no exemplo)
        res["pres"] = votos
        res["ele_filhos"] = [(f[0], f[2]) for f in cs[:6]]
    return res


if __name__ == "__main__":
    r = parse_bu(open(sys.argv[1], "rb").read())
    print(json.dumps(r, ensure_ascii=False, indent=1))
    print("soma:", sum(r["pres"].values()))
