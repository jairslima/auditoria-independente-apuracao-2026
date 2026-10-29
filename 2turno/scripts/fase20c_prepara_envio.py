# -*- coding: utf-8 -*-
"""Fase 20c: gera as copias de ENVIO dos pedidos LAI (texto simples, com a lista de secoes no proprio corpo) em pedidos_lai/_envio/ (ignorada pelo git).
O CPF e lido de pedidos_lai/_envio/cpf.txt (fora do git) para nunca entrar no repositorio."""
import csv, os, re

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PED = os.path.join(RAIZ, "pedidos_lai")
ENV = os.path.join(PED, "_envio")
os.makedirs(ENV, exist_ok=True)
CPF = open(os.path.join(ENV, "cpf.txt"), encoding="utf-8").read().strip()
LOCAL_DATA = "Três Coroas/RS, 7 de outubro de 2026"
NL = chr(10)

PEDIDOS = [
    ("01_TSE.md", "anexo_TSE_todas_as_secoes.csv", "TSE", "ouv@tse.jus.br"),
    ("02_TRE-PA.md", "anexo_TRE-PA.csv", "TRE-PA", "ouvidoria@tre-pa.jus.br"),
    ("03_TRE-PE.md", "anexo_TRE-PE.csv", "TRE-PE", "ouvidoria@tre-pe.jus.br"),
    ("04_TRE-MA.md", "anexo_TRE-MA.csv", "TRE-MA", "ouvidoria@tre-ma.jus.br"),
    ("05_TRE-MG.md", "anexo_TRE-MG.csv", "TRE-MG", "ouvidoria@tre-mg.jus.br"),
    ("06_TRE-SP.md", "anexo_TRE-SP.csv", "TRE-SP", "seac@tre-sp.jus.br"),
]
ASSUNTOS = {
    "TSE": "Pedido de acesso à informação (Lei 12.527/2011): registros de recepção, totalização e divulgação do 1º turno de 04/10/2026",
    "TRE-PA": "Pedido de acesso à informação (Lei 12.527/2011): registros de 621 seções do Pará no dia seguinte à votação (05/10/2026)",
    "TRE-PE": "Pedido de acesso à informação (Lei 12.527/2011): registros de 60 seções de Pernambuco no dia seguinte à votação (05/10/2026)",
    "TRE-MA": "Pedido de acesso à informação (Lei 12.527/2011): registros de 45 seções do Maranhão no dia seguinte à votação (05/10/2026)",
    "TRE-MG": "Pedido de acesso à informação (Lei 12.527/2011): publicação tardia de arquivos de seções de Minas Gerais (1º turno 2026)",
    "TRE-SP": "Pedido de acesso à informação (Lei 12.527/2011): publicação tardia de arquivos de 12 seções de Carapicuíba (1º turno 2026)",
}
MOTIVOS = {
    "1a consulta HTTP 404 (arquivos publicados depois)": "ARQ-TARDIO",
    "registro depois de 23h41 de 04/10": "REG-DIA-SEG",
    "BU do Sistema de Apuracao (busa)": "SIST-APURACAO",
}
FRASE_ANEXO = ("Anexo: lista de seções ao final desta mensagem (colunas: UF | município | zona | seção | emissão do BU na urna | "
               "registro hr | motivo). Planilha CSV completa disponível mediante solicitação.")
LEGENDA = ("Horários de Brasília. Motivos: ARQ-TARDIO = arquivos publicados com atraso (a 1ª consulta retornou não encontrado); "
           "REG-DIA-SEG = registro depois das 23h41 de 04/10; SIST-APURACAO = BU gerado pelo Sistema de Apuração.")
COBERTOS = ("PA", "PE", "MA", "MG")


def ler_csv(nome):
    return list(csv.DictReader(open(os.path.join(PED, "anexos", nome), encoding="utf-8-sig"), delimiter=";"))


def curto(x):
    return (x[:5] + x[10:]) if x else ""


def linha(r):
    m = "+".join(MOTIVOS.get(t.strip(), t.strip()) for t in r["motivo_da_inclusao"].split(";"))
    return f'{r["UF"]} | {r["municipio"]} | {r["zona"]} | {r["secao"]} | {curto(r["emissao_do_BU_na_urna"])[:11]} | {curto(r["registro_hr_no_repositorio_TSE"])} | {m}'


def anexo_texto(csvname, sigla):
    rows = ler_csv(csvname)
    if sigla != "TSE":
        return f"ANEXO ({len(rows)} seções). {LEGENDA}" + NL + NL + NL.join(linha(r) for r in rows) + NL
    unicas = [r for r in rows if "registro depois" not in r["motivo_da_inclusao"] or r["UF"] not in COBERTOS]
    dia_seg = [r for r in rows if "registro depois" in r["motivo_da_inclusao"] and r["UF"] in COBERTOS]
    t = (f"ANEXO 1 ({len(unicas)} seções listadas uma a uma: as 68 de publicação tardia, as 31 do Sistema de Apuração e as 14 de AM e BA "
         f"registradas no dia seguinte). {LEGENDA}" + NL + NL)
    t += NL.join(linha(r) for r in unicas) + NL
    grupos = {}
    for r in dia_seg:
        grupos.setdefault((r["UF"], r["municipio"], r["zona"]), []).append(r["registro_hr_no_repositorio_TSE"])
    t += (NL + f"ANEXO 2 ({len(dia_seg)} seções de PA, PE, MA e MG registradas depois das 23h41 de 04/10, resumidas por zona; a lista seção a seção "
          "consta dos pedidos enviados aos respectivos TREs). Colunas: UF | município | zona | quantidade | primeiro registro | último registro" + NL + NL)
    for (uf, mun, zona), v in sorted(grupos.items(), key=lambda x: (-len(x[1]), x[0])):
        v.sort(key=lambda x: (x[6:10], x[3:5], x[0:2], x[11:]))
        t += f"{uf} | {mun} | {zona} | {len(v)} | {curto(v[0])} | {curto(v[-1])}" + NL
    z = ler_csv("resumo_zonas_recebida.csv")
    t += (NL + f"ANEXO 3: zonas com seções no estado Recebida na coleta de 05/10 ({len(z)} zonas). "
          "Colunas: UF | município | zona | seções em Recebida | seções da zona com BU" + NL + NL)
    t += NL.join(f'{r["UF"]} | {r["municipio"]} | {r["zona"]} | {r["secoes_com_status_Recebida_na_coleta_de_05_10"]} | {r["secoes_da_zona_com_BU"]}' for r in z) + NL
    return t


def para_texto(md):
    t = md
    t = re.sub(r"^# (.+)$", lambda m: m.group(1).upper(), t, flags=re.M)
    t = t.replace("**", "").replace("`", "")
    t = re.sub(r"(?<!\w)\*(?!\s)([^*\n]+)\*(?!\w)", r"\1", t)
    t = t.replace("CPF: [informar no formulário].", f"CPF: {CPF}.")
    t = re.sub(r" CNPJ: \[informar, se houver\]\.", "", t)
    t = t.replace("Data do protocolo: [preencher]", f"Data do pedido: {LOCAL_DATA}")
    t = t.replace("[Local e data]", LOCAL_DATA)
    t = t.replace("por meio do formulário eletrônico da Ouvidoria", "por e-mail")
    t = t.replace("(842 seções, lista em anexo)", "(842 seções: 113 listadas uma a uma no anexo abaixo; as 729 de PA, PE, MA e MG resumidas por zona e listadas uma a uma nos pedidos enviados aos respectivos TREs)")
    t = re.sub(r"Anexos?:\s*anexos/[^\n]+", FRASE_ANEXO, t)
    return t.strip() + NL


for md, csvname, sigla, email in PEDIDOS:
    corpo = para_texto(open(os.path.join(PED, md), encoding="utf-8").read())
    pre = ("Solicito o registro deste pedido no Serviço de Informação ao Cidadão e o envio do número de protocolo para acompanhamento, "
           "para este e-mail (jairslima@gmail.com)." + NL + NL)
    corpo = pre + corpo.rstrip() + NL + NL + anexo_texto(csvname, sigla)
    # versao para envio com planilha CSV anexa (sem a lista no corpo)
    prosa = para_texto(open(os.path.join(PED, md), encoding="utf-8").read())
    prosa = prosa.replace(FRASE_ANEXO, "Anexo: planilha CSV anexa a esta mensagem, com a lista de seções (colunas: UF, código do município, município, zona, seção, emissão do BU na urna, registro hr no repositório do TSE, estado no aux.json, arquivos da seção e motivo da inclusão). Horários de Brasília.")
    prosa = prosa.replace("(lista em anexo)", "(planilha anexa)").replace("(842 seções: 113 listadas uma a uma no anexo abaixo; as 729 de PA, PE, MA e MG resumidas por zona e listadas uma a uma nos pedidos enviados aos respectivos TREs)", "(842 seções, planilha anexa)")
    open(os.path.join(ENV, f"{sigla}_corpo_anexo.txt"), "w", encoding="utf-8").write(pre + prosa)
    pend = re.findall(r"\[[^\]]+\]", corpo)
    open(os.path.join(ENV, f"{sigla}_corpo.txt"), "w", encoding="utf-8").write(corpo)
    open(os.path.join(ENV, f"{sigla}_assunto.txt"), "w", encoding="utf-8").write(ASSUNTOS[sigla])
    print(f"{sigla:7} -> {email:28} | corpo {len(corpo):>6} car. | linhas {corpo.count(NL):>4} | pendencias entre colchetes: {pend}")
print("CPF presente nos corpos:", all(CPF in open(os.path.join(ENV, f"{s}_corpo.txt"), encoding="utf-8").read() for _, _, s, _ in PEDIDOS))
print("'anexos/' residual:", sum(open(os.path.join(ENV, f"{s}_corpo.txt"), encoding="utf-8").read().count("anexos/") for _, _, s, _ in PEDIDOS))
