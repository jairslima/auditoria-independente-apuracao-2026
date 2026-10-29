# -*- coding: utf-8 -*-
"""Fase 20b: gera os pedidos de acesso a informacao (LAI) em pedidos_lai/*.md a partir de texto fixo e dos numeros medidos na auditoria.
Autor do projeto: Jair Lima (Auditoria Independente da Apuracao 2026 by Jair Lima)."""
import os

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(RAIZ, "pedidos_lai")
os.makedirs(OUT, exist_ok=True)

REQ = """**Requerentes**

1. **Jair da Silva Lima**, jornalista profissional registrado no Ministério do Trabalho e Emprego sob o nº 0024314/RS (cartão emitido em 11/09/2026, código de autenticidade 1504531). CPF: [informar no formulário]. E-mail: jairslima@gmail.com.
2. **Folha dos Vales** (folhadosvales.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.
3. **Folha do Litoral Norte** (folhadolitoralnorte.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.

Os requerentes apresentam este pedido em conjunto. Nos termos do art. 10, § 3º, da Lei nº 12.527/2011, não é exigida a motivação do pedido; informa-se, apenas por transparência, que se trata de apuração jornalística de interesse público sobre o processamento do 1º turno de 04/10/2026.
"""

BASE_LEGAL = ("**Fundamento.** Constituição Federal, art. 5º, XIV e XXXIII, e art. 37, § 3º, II; Lei nº 12.527/2011 (Lei de Acesso à Informação), "
              "em especial os arts. 7º, 10, 11, 12 e 14; e Resolução-TSE nº 23.435/2015, alterada pela Resolução-TSE nº 23.583/2018.")

FORMA = """**Forma de entrega.** Em meio digital, de preferência em arquivo estruturado (CSV ou planilha) para as listas por seção e em PDF para relatórios, enviados ao e-mail dos requerentes ou anexados ao sistema. Caso parte da informação seja considerada sigilosa, solicita-se o acesso à parte não sigilosa, com ocultação apenas do trecho protegido (art. 7º, § 2º), e o inteiro teor da decisão de negativa (art. 14).

**Esclarecimento sobre o sigilo do voto.** Este pedido não solicita dados pessoais de eleitores nem qualquer informação que permita identificar votos individuais. Todas as informações pedidas dizem respeito a horários, estados de processamento, registros técnicos e esclarecimentos sobre arquivos já públicos, por seção eleitoral ou de forma agregada.
"""

FECHO = ("Os requerentes se colocam à disposição para encaminhar o relatório da auditoria, as listas completas e os scripts que reproduzem as medições citadas, "
         "para que o Tribunal possa conferi-las.")

CONTEXTO = ("**Contexto.** Uma auditoria independente do 1º turno (*Auditoria Independente da Apuração 2026 by Jair Lima*), feita exclusivamente com arquivos públicos do TSE "
            "(boletins de urna, registro digital do voto, arquivos de assinatura e arquivos de resultado de `resultados.tse.jus.br`), reproduziu a soma de votos de Presidente "
            "(499.207 seções) e da eleição estadual e **não encontrou diferença em relação ao resultado oficial**. Ao fazê-la, porém, identificou pontos de processamento que "
            "os dados públicos não permitem explicar. Todos os horários abaixo são de Brasília e todos os números foram medidos nos arquivos públicos coletados em 05 e 06/10/2026.")

ASSINA = "Termos em que pedem deferimento.\n\n[Local e data]\n\nJair da Silva Lima, por si e pelas publicações Folha dos Vales e Folha do Litoral Norte\n"

tse = f"""# Pedido de acesso à informação ao Tribunal Superior Eleitoral

**Destinatário:** Ouvidoria / Serviço de Informação ao Cidadão (SIC) do Tribunal Superior Eleitoral, por meio do formulário eletrônico da Ouvidoria.
**Assunto:** Registros de recepção, totalização e divulgação do 1º turno de 04/10/2026; incidente na divulgação do resultado de Presidente; estados "Recebida" e "Totalizada".
**Data do protocolo:** [preencher]

{REQ}
{BASE_LEGAL}

{CONTEXTO}

**Fatos observados nos arquivos públicos**

1. **Pausa na divulgação de Presidente.** Segundo a imprensa, o painel de Presidente ficou sem atualização de 19h06min33s até as 20h08, em 64,81% das seções, e o presidente do Tribunal atribuiu o fato a congestionamento no sistema de divulgação. Nos arquivos públicos, o campo `hr` (hora de registro da seção) mostra 110.864 seções registradas nesse período, mas **nenhum registro entre 19h31m50s e 19h59m22s (27,5 minutos)**, seguido de rajada e de ritmo quase constante de cerca de 500 por minuto entre 20h05 e 20h40.
2. **Arquivos publicados com atraso por zona.** Na primeira coleta (05/10), 68 seções de cinco zonas eleitorais (Betim/MG zonas 316 e 319, Teófilo Otoni/MG zona 269, Uberlândia/MG zona 279 e Carapicuíba/SP zona 388) retornavam "arquivo não encontrado". Todas constavam com BU registrado em 04/10 entre 20h07 e 21h15 e foram publicadas entre 05/10 e 06/10 (a última leva, 15 seções, só em 06/10).
3. **Registros no dia seguinte.** 743 seções têm registro (`hr`) depois das 23h41 de 04/10, até as 15h24 de 05/10 (Pará 621, Pernambuco 60, Maranhão 45, Bahia 7, Amazonas 7, Minas Gerais 3). O arquivo oficial de resultado de Presidente do Pará, gerado às 12h51m45s de 05/10 com 20.827 de 20.827 seções totalizadas, tem total **igual** à soma dos boletins incluindo as seções do Pará registradas depois dessa hora. Logo, para essas seções, o campo `hr` não parece indicar o momento em que os votos entraram no total.
4. **Estados "Recebida" e "Totalizada".** Na coleta de 05/10, 491.838 seções apareciam como "Totalizada" e 7.369 como "Recebida" nos arquivos de seção (`aux.json`), concentradas em poucas zonas (SP 5.125, MG 1.729, PA 506), embora o resultado oficial já contasse 100% das seções.
5. **Índice de seções.** Os campos `da`/`ha` do índice por UF (`...-cs.json`) são, em 99,3% das seções, mais de uma hora posteriores ao `hr`, e 69.438 seções compartilham o mesmo minuto (05/10 às 00h52).
6. **Urnas substituídas.** Os BUs trazem 3.033 seções com urna de contingência que passou a ser de seção (tipo de urna 4) e 50 de recuperação de dados (RED), contra 1.121 substituições divulgadas durante a apuração. O campo opcional de histórico de correspondências está vazio em todos os BUs.
7. **Sistema de Apuração.** 31 seções (29 no exterior, 2 em MG) têm BU gerado pelo Sistema de Apuração (`.busa`) e arquivo de assinatura `.vscsa`, cujo esquema de verificação não consta da documentação pública de formato de BU/RDV/assinatura de 2026.

**Pedidos**

1. O **registro de eventos** (log) dos sistemas de recepção, totalização e divulgação de resultados de 04/10/2026, entre 17h e 23h59, e de 05/10/2026 até 12h51, ao menos de forma agregada por intervalo de 5 minutos: quantidade de BUs recebidos, totalizados e publicados, e os intervalos de indisponibilidade ou lentidão.
2. O **relatório técnico do incidente** na divulgação do resultado de Presidente entre 19h06 e 20h08: hora de início, de detecção e de normalização, causa, componentes envolvidos, providências adotadas e se algum arquivo de resultado foi regenerado ou republicado, com a respectiva cronologia.
3. Para **cada seção do Anexo TSE** (842 seções, lista em anexo): a hora de recebimento do BU, de totalização e de publicação dos arquivos, e o motivo de qualquer diferença entre elas.
4. A **definição oficial e a regra de atribuição** dos estados "Recebida" e "Totalizada", do campo `hr` e dos campos `da`/`ha`, e a explicação para os fatos 3, 4 e 5 acima.
5. Para as 68 seções do fato 2: o **motivo da publicação tardia** por zona e o **resumo criptográfico (hash) de cada arquivo no momento do recebimento**, para conferência de integridade.
6. O **critério** de contagem de urnas substituídas, a explicação da diferença entre as 3.033 seções de urna substituta mais 50 RED e as 1.121 substituições divulgadas, e a razão de o histórico de correspondências não constar dos BUs.
7. A **especificação do esquema de assinatura** do arquivo `.vscsa` e as chaves públicas (ou listas de hash das chaves públicas) das Eleições 2026, para permitir a verificação independente dos 31 BUs do Sistema de Apuração.

{FORMA}
{FECHO}

**Anexos:** `anexos/anexo_TSE_todas_as_secoes.csv` (842 seções: as 68 de publicação tardia, as 743 registradas depois de 23h41 e as 31 do Sistema de Apuração, com hora de emissão do BU na urna e hora de registro) e `anexos/resumo_zonas_recebida.csv` (zonas com estado "Recebida").

{ASSINA}"""
open(os.path.join(OUT, "01_TSE.md"), "w", encoding="utf-8").write(tse)


def tre(sigla, tribunal, n_secoes, fatos, extra, arquivo, assunto):
    return f"""# Pedido de acesso à informação ao {tribunal}

**Destinatário:** Ouvidoria / Serviço de Informação ao Cidadão (SIC) do {tribunal}.
**Assunto:** {assunto}
**Data do protocolo:** [preencher]

{REQ}
{BASE_LEGAL} No âmbito do Tribunal, aplicam-se também as normas internas de acesso à informação da Justiça Eleitoral.

{CONTEXTO}

**Fatos observados nos arquivos públicos, referentes à jurisdição do {sigla}**

{fatos}

**Pedidos**

1. Para **cada uma das {n_secoes} seções do Anexo {sigla}** (lista em anexo): a hora em que o BU foi recebido na Zona Eleitoral ou no Tribunal, a hora em que foi transmitido ao TSE e a hora de qualquer retransmissão ou novo envio, com a indicação do meio (leitura da mídia de resultado na zona, transmissão pela rede, recuperação de dados ou apuração pelo Sistema de Apuração).
2. A **explicação do motivo** pelo qual os arquivos dessas seções constam com registro nos horários indicados no anexo, e a identificação da operação realizada (reenvio, reprocessamento, inclusão de arquivos, correção de cadastro ou outra), com a **ata ou o relatório de ocorrência** da zona ou do Tribunal, se existir.
3. A informação de **se houve substituição de urna ou de cartão de memória** nessas seções e, havendo, a identificação da urna original e da substituta.
4. A **confirmação**, com o respectivo registro, de que os BUs dessas seções transmitidos ao TSE são os mesmos gerados na urna (resumo criptográfico do arquivo no envio e no recebimento).
{extra}
{FORMA}
{FECHO}

**Anexo:** `anexos/{arquivo}`.

{ASSINA}"""


pa = tre("TRE-PA", "Tribunal Regional Eleitoral do Pará (TRE-PA)", 621,
"""1. **621 seções do Pará** têm o registro dos arquivos (`hr`) depois das 23h41 de 04/10, entre 04/10 às 23h54 e 05/10 às 15h24. Concentram-se em: Belém, zona 97 (354 de 354 seções da zona, registradas em 05/10 entre 13h41 e 14h19), Capanema, zona 25 (101 de 203, 12h40 a 13h23), Oeiras do Pará, zona 45 (61 de 91, 13h29 a 14h44) e Gurupá, zona 26 (40 de 89, 11h05 a 15h24).
2. Os BUs dessas seções foram emitidos nas urnas entre 17h01 e 22h30 de 04/10.
3. O arquivo oficial de Presidente do Pará, gerado às 12h51m45s de 05/10, já registrava 20.827 de 20.827 seções totalizadas, e o total dele é igual à soma dos BUs, **incluindo** as seções do Pará registradas depois dessa hora.
4. Na coleta de 05/10, 506 seções do Pará constavam com o estado "Recebida", e não "Totalizada".""",
"""5. A **explicação** para o fato 3: como o total oficial de Presidente do Pará gerado às 12h51 já incluía as seções registradas depois dessa hora, e o que o registro posterior representa.
6. A razão pela qual **todas as 354 seções da zona 97 (Belém)** têm registro no mesmo intervalo de 38 minutos em 05/10.
""", "anexo_TRE-PA.csv", "Registros de 621 seções do Pará no dia seguinte à votação (05/10/2026); estado \"Recebida\" de 506 seções.")

pe = tre("TRE-PE", "Tribunal Regional Eleitoral de Pernambuco (TRE-PE)", 60,
"""1. **60 seções de Pernambuco** têm registro (`hr`) depois das 23h41 de 04/10, todas em 05/10 entre 10h49 e 14h40. A maior parte está no município de Cabo de Santo Agostinho, zona 15 (50 de 208 seções da zona, todas registradas às 10h49), seguida de Paulista, zona 114 (7).
2. Os BUs das seções de Cabo de Santo Agostinho foram emitidos nas urnas entre 17h03 e 18h41 de 04/10.
3. O arquivo oficial de Presidente de Pernambuco, gerado às 12h51m44s de 05/10, já registrava 21.418 de 21.418 seções totalizadas.""",
"""5. A razão pela qual **50 seções de Cabo de Santo Agostinho (zona 15) têm registro no mesmo minuto**, às 10h49 de 05/10.
""", "anexo_TRE-PE.csv", "Registros de 60 seções de Pernambuco no dia seguinte à votação (05/10/2026).")

ma = tre("TRE-MA", "Tribunal Regional Eleitoral do Maranhão (TRE-MA)", 45,
"""1. **45 seções do Maranhão** têm registro (`hr`) depois das 23h41 de 04/10, todas em 05/10 às 01h56: 34 em Viana, zona 20 (de 151 seções da zona) e 11 em Cajari, zona 20.
2. Os BUs das seções de Viana foram emitidos nas urnas entre 17h01 e 18h36 de 04/10.
3. O arquivo oficial de Presidente do Maranhão, gerado às 12h51m45s de 05/10, já registrava 18.093 de 18.093 seções totalizadas.""",
"""5. A razão pela qual **as 45 seções (Viana e Cajari, zona 20) têm registro no mesmo minuto**, às 01h56 de 05/10, e se houve transmissão a partir da zona nessa hora.
""", "anexo_TRE-MA.csv", "Registros de 45 seções do Maranhão no dia seguinte à votação (05/10/2026).")

mg = tre("TRE-MG", "Tribunal Regional Eleitoral de Minas Gerais (TRE-MG)", 61,
"""1. **56 seções de Minas Gerais** em quatro zonas tiveram os arquivos publicados com atraso (na primeira coleta de 05/10, retornavam "arquivo não encontrado"): Betim, zona 316 (30 seções, BU registrado em 04/10 entre 20h08 e 20h59), Teófilo Otoni, zona 269 (18 seções, 20h44 a 21h15), Uberlândia, zona 279 (5 seções, 20h52 a 20h55) e Betim, zona 319 (3 seções, 20h07 a 20h10). As de Betim zona 316 e de Teófilo Otoni ficaram disponíveis em 05/10, as de Uberlândia na terceira consulta, entre 05/10 e 06/10, e as de Betim zona 319 só em 06/10.
2. As mesmas zonas concentram o estado "Recebida" (na coleta de 05/10, Betim zona 316: 529 de 559 seções; Betim zona 319: 446 de 449; Uberlândia zona 279: 437 de 442), num total de 1.729 seções de Minas nesse estado.
3. **3 seções** de Minas (2 em São João das Missões, zona 166, e 1 em Ataléia, zona 270) têm registro depois das 23h41 de 04/10.
4. **2 seções** de Minas (município 41238, zona 39, seção 168, e município 50075, zona 47, seção 41) têm BU gerado pelo Sistema de Apuração (apuração mista com BU impresso e cédulas), com registro às 22h15 e 22h29.""",
"""5. A razão do **atraso por zona** na publicação dos arquivos das quatro zonas do fato 1 e o significado, para a Zona e o Tribunal, do estado "Recebida" nas zonas do fato 2.
6. O **motivo do uso do Sistema de Apuração** nas 2 seções do fato 4 e a descrição do procedimento (mídia, BU impresso, cédulas).
""", "anexo_TRE-MG.csv", "Publicação tardia de arquivos de 56 seções (Betim, Teófilo Otoni e Uberlândia) e de outras 5 seções de Minas Gerais.")

sp = tre("TRE-SP", "Tribunal Regional Eleitoral de São Paulo (TRE-SP)", 12,
"""1. **12 seções de Carapicuíba, zona 388** (de 426 da zona) tiveram os arquivos publicados com atraso: na primeira coleta e na segunda, ambas em 05/10, retornavam "arquivo não encontrado", e só ficaram disponíveis em 06/10. O BU de cada uma foi registrado em 04/10 entre 20h59 e 21h14, e emitido na urna entre 17h07 e 17h43.
2. Na coleta de 05/10, 5.125 seções de São Paulo constavam como "Recebida" (por exemplo, São Paulo zona 397: 518 de 518 seções; Campinas zonas 378 e 379: 424 e 415; Carapicuíba zonas 303 e 388: 414 e 414).""",
"""5. A razão do **atraso na publicação** dos arquivos das 12 seções da zona 388 de Carapicuíba, em comparação com as demais seções da mesma zona, e o significado, para a Zona e o Tribunal, do estado "Recebida" nas zonas do fato 2.
""", "anexo_TRE-SP.csv", "Publicação tardia de arquivos de 12 seções de Carapicuíba (zona 388) e estado \"Recebida\" em seções de São Paulo.")

for nome, texto in (("02_TRE-PA.md", pa), ("03_TRE-PE.md", pe), ("04_TRE-MA.md", ma), ("05_TRE-MG.md", mg), ("06_TRE-SP.md", sp)):
    open(os.path.join(OUT, nome), "w", encoding="utf-8").write(texto)
print("pedidos gerados:", sorted(f for f in os.listdir(OUT) if f.endswith(".md")))
