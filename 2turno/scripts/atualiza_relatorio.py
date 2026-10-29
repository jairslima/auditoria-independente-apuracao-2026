# -*- coding: utf-8 -*-
"""Atualiza a secao 'Andamento da verificacao completa' do RELATORIO_2TURNO.md com os numeros atuais de cada etapa, gera o HTML e,
com --abrir, mostra o relatorio na tela. Auditoria Independente da Apuracao 2026 by Jair Lima."""
import csv, json, os, sys, time
from collections import Counter
from datetime import datetime

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REL = os.path.join(os.path.dirname(RAIZ), "AuditoriaPresidente2026", "RELATORIO_2TURNO.md")
HTML = os.path.join(RAIZ, "resultados", "RELATORIO_2TURNO.html")
INI, FIM = "<!-- ANDAMENTO:INICIO -->", "<!-- ANDAMENTO:FIM -->"
R = lambda *p: os.path.join(RAIZ, *p)
n = lambda x: f"{x:,}".replace(",", ".")


def linhas_arq(p):
    if not os.path.exists(p):
        return 0
    with open(p, "rb") as f:
        return sum(1 for _ in f)


def jload(p):
    return json.load(open(p, encoding="utf-8")) if os.path.exists(p) else None


def estagios():
    st = {}
    p = R("dados", "cadeia4.log")
    if os.path.exists(p):
        for l in open(p, encoding="utf-8", errors="replace"):
            partes = l.split()
            if len(partes) >= 2 and partes[0] in ("inicio", "fim"):
                st[partes[1]] = "concluída" if partes[0] == "fim" else "em andamento"
                if partes[0] == "fim" and "codigo" in partes and partes[partes.index("codigo") + 1] != "0":
                    st[partes[1]] = "terminou com erro"
    return st


def bloco():
    st = estagios()
    s = [INI, "## 6. Andamento da verificação completa (sem amostragem)", "",
         f"Atualizado automaticamente em {datetime.now():%d/%m/%Y %H:%M}. Esta seção substitui, etapa por etapa, as partes por amostra das seções 3.3 e 4.", "",
         "| Etapa | Estado | Resultado até agora |", "|---|---|---|"]
    # 1 aux 24h
    r26 = jload(R("resultados", "fase26_resumo.json"))
    n24 = linhas_arq(R("dados", "aux_24h.jsonl"))
    if r26:
        res = (f"{n(r26['secoes_coleta_dia27'])} seções comparadas com a coleta de 26/10 manhã. Mudanças: {n(r26['secoes_com_alguma_mudanca'])} seções "
               f"(hash do BU mudou: {n(r26['hash_mudou'])}; estado mudou: {n(r26['estado_mudou'])}; data/hora mudou: {n(r26['dr_hr_mudou'])}).")
    else:
        res = f"{n(n24)} de 499.207 seções coletadas."
    s.append(f"| 1. Segunda cópia do aux.json (27/10) e comparação com a de 26/10 | {st.get('fase2_aux_24h', 'pendente') if not r26 else 'concluída'} | {res} |")
    # 5 municipios
    mj = jload(R("relatorio_web", "municipios.json"))
    res = f"{n(mj['n_ok'])} de {n(mj['n_total'])} municípios e postos iguais ao oficial." if mj else "–"
    s.append(f"| 2. Conferência município a município (Presidente) | {st.get('fase17_municipios', 'pendente')} | {res} |")
    # 2 rdv
    p = R("dados", "rdv_vs_bu.csv")
    if os.path.exists(p):
        c = Counter(r["status"] for r in csv.DictReader(open(p, encoding="utf-8")))
        tot = sum(c.values())
        res = f"{n(tot)} de 499.207 seções comparadas: {n(c.get('ok', 0))} iguais, {n(c.get('DIVERGE', 0))} divergentes, {n(c.get('erro', 0))} com erro, {n(c.get('sem_rdv', 0))} sem RDV."
    else:
        res = "–"
    s.append(f"| 3. RDV contra o BU em todas as seções | {st.get('fase19_rdv', 'pendente')} | {res} |")
    # 3 logs
    p = R("resultados", "fase27_logs_todas.csv")
    if os.path.exists(p):
        rows = list(csv.DictReader(open(p, encoding="utf-8-sig"), delimiter=";"))
        ok = [r for r in rows if not r["erro"]]
        v17 = sum(int(r["votos_apos_17h00"] or 0) for r in ok)
        v1706 = sum(int(r["votos_apos_17h06"] or 0) for r in ok)
        v19 = sum(int(r["votos_apos_19h00"] or 0) for r in ok)
        com = sum(1 for r in ok if int(r["votos_apos_17h00"] or 0) > 0)
        a = b = c2 = 0
        for r in ok:
            if r["gera_bu_brt"]:
                t = datetime.fromisoformat(r["gera_bu_brt"])
                if t < datetime(2026, 10, 25, 17, 6, 31): a += 1
                elif t < datetime(2026, 10, 25, 19, 0, 0): b += 1
                else: c2 += 1
        res = (f"{n(len(ok))} de 499.207 logs lidos ({n(len(rows) - len(ok))} com erro). Votos computados depois das 17h00: **{n(v17)}** em {n(com)} seções "
               f"(depois das 17h06: {n(v1706)}; depois das 19h00: {n(v19)}). BU gerado antes de 17h06: {n(a)}; entre 17h06 e 19h00: {n(b)}; depois das 19h00: {n(c2)}.")
    else:
        res = "–"
    s.append(f"| 4. Logs de todas as urnas (votos depois das 17h e hora de geração do BU) | {st.get('fase27_logs_todas', 'pendente')} | {res} |")
    # 4 urna x certificado
    r28 = jload(R("resultados", "fase28_resumo.json"))
    res = (f"{n(r28['iguais'])} seções com o número da urna igual ao do certificado; {n(r28['diferentes'])} diferentes; "
           f"{n(r28['sem_certificado'])} sem certificado; {n(r28['sem_log'])} sem log.") if r28 else "–"
    s.append(f"| 5. Número da urna no log × certificado | {st.get('fase28_urna_certificado', 'pendente')} | {res} |")
    s += ["", "Os números desta seção vêm direto dos arquivos em `AuditoriaPresidente2026_T2/resultados/` e `dados/`.", FIM]
    return "\n".join(s)


def main():
    t = open(REL, encoding="utf-8").read()
    b = bloco()
    if INI in t and FIM in t:
        t = t[:t.index(INI)] + b + t[t.index(FIM) + len(FIM):]
    else:
        t = t.rstrip() + "\n\n" + b + "\n"
    open(REL, "w", encoding="utf-8").write(t)
    try:
        import markdown
        corpo = markdown.markdown(t, extensions=["tables"])
    except Exception:
        corpo = "<pre>" + t.replace("<", "&lt;") + "</pre>"
    css = ("body{font-family:Segoe UI,Arial,sans-serif;max-width:980px;margin:24px auto;padding:0 16px;line-height:1.5;color:#1b1b1b;background:#fff}"
           "table{border-collapse:collapse;width:100%;margin:12px 0}th,td{border:1px solid #bbb;padding:6px 8px;text-align:left;vertical-align:top}"
           "th{background:#eee}code{background:#f2f2f2;padding:1px 4px}h1,h2,h3{line-height:1.25}")
    os.makedirs(os.path.dirname(HTML), exist_ok=True)
    open(HTML, "w", encoding="utf-8").write(f"<!doctype html><html lang='pt-BR'><head><meta charset='utf-8'><title>Relatório do 2º turno</title><style>{css}</style></head><body>{corpo}</body></html>")
    print("relatório atualizado:", REL)
    if "--abrir" in sys.argv:
        os.startfile(HTML)


if __name__ == "__main__":
    main()
