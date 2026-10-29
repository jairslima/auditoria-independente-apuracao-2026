"""Dump generico de BER para explorar a estrutura do BU."""
import sys

def tlv(b, i):
    t = b[i]; i += 1
    cls, cons, tag = t >> 6, (t >> 5) & 1, t & 0x1F
    if tag == 0x1F:
        tag = 0
        while True:
            x = b[i]; i += 1
            tag = (tag << 7) | (x & 0x7F)
            if not x & 0x80: break
    l = b[i]; i += 1
    if l & 0x80:
        n = l & 0x7F
        l = int.from_bytes(b[i:i+n], "big"); i += n
    return cls, cons, tag, i, l

def dump(b, i, fim, nivel, maxn=60):
    k = 0
    while i < fim and k < maxn:
        cls, cons, tag, ini, l = tlv(b, i)
        v = b[ini:ini+l]
        pref = "  " * nivel + f"[{cls}:{tag}]"
        if cons:
            print(pref, f"seq len={l}")
            dump(b, ini, ini + l, nivel + 1)
        else:
            try:
                s = v.decode("ascii")
                ok = s.isprintable() and len(s) > 0
            except Exception:
                ok = False
            print(pref, f"len={l}", repr(v.decode("ascii")) if ok else int.from_bytes(v, "big") if l <= 8 else v[:20].hex())
        i = ini + l; k += 1

b = open(sys.argv[1], "rb").read()
print("bytes:", len(b))
dump(b, 0, len(b), 0)
