# Pedido ao TSE: suspensão da totalização e bloqueio do recebimento de BUs no 2º turno (25/10/2026)

**Destinatário:** Ouvidoria do TSE (formulário eletrônico ou ouv@tse.jus.br), Lei nº 12.527/2011.
**Situação:** RASCUNHO, NÃO enviado. Aguarda revisão e protocolo pelo Jair. Preencher CPF e data. Não anexei documento pessoal.
**Anexos sugeridos:** `AuditoriaPresidente2026_T2/resultados/fase24_cruza_monitor.csv` (499.207 seções, com hr e primeira vez vista) e o gráfico/tabela da curva oficial (`segundo_turno/dados_monitor/curva_oficial.csv`).

---

**Assunto:** Suspensão da totalização e bloqueio do recebimento de boletins de urna entre 17h06 e 19h no 2º turno de 25/10/2026; registros de recepção, divulgação e campo `hr`.
**Data do protocolo:** [preencher]

**Requerentes**

1. **Jair da Silva Lima**, jornalista profissional registrado no Ministério do Trabalho e Emprego sob o nº 0024314/RS (cartão emitido em 11/09/2026, código de autenticidade 1504531). CPF: [informar no formulário]. E-mail: jairslima@gmail.com.
2. **Folha dos Vales** (folhadosvales.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.
3. **Folha do Litoral Norte** (folhadolitoralnorte.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.

Os requerentes apresentam este pedido em conjunto. Nos termos do art. 10, § 3º, da Lei nº 12.527/2011, não é exigida a motivação do pedido; informa-se, apenas por transparência, que se trata de apuração jornalística de interesse público sobre o processamento do 2º turno de 25/10/2026.
**Fundamento.** Constituição Federal, art. 5º, XIV e XXXIII, e art. 37, § 3º, II; Lei nº 12.527/2011 (Lei de Acesso à Informação), em especial os arts. 7º, 10, 11, 12 e 14; e Resolução-TSE nº 23.435/2015, alterada pela Resolução-TSE nº 23.583/2018.

**Esclarecimento sobre o sigilo do voto.** Este pedido não solicita dados pessoais de eleitores nem qualquer informação que permita identificar votos individuais. Todas as informações pedidas dizem respeito a horários, estados de processamento, registros técnicos e esclarecimentos sobre arquivos já públicos.

**Fatos de que partimos**

1. Segundo a imprensa oficial e as declarações do Presidente do TSE (Agência Brasil, Agência Câmara e Rádio Senado, de 25/10/2026), o ministro Cristiano Zanin, do STF, determinou a prorrogação por até duas horas, até as 19h, do encerramento do recebimento dos votos, a totalização foi suspensa às 17h06 com 1.225 de 499.248 seções apuradas, e o recebimento dos boletins de urna foi temporariamente bloqueado.
2. A coleta que fizemos do repositório público (consulta ao resultado nacional a cada cerca de 2 minutos, de 16h às 23h27) registrou o total parado em 1.225 seções, com geração às 17:06:31, até as 19:02, e novos dados a partir das 19:03:36. Nesse intervalo o índice de seções não recebeu nenhuma seção nova, e nenhuma seção tem, no campo `hr` do repositório, horário entre aproximadamente 17:10 e 19:00. O campo `hr` é o da última tentativa de envio: em 965 seções vimos o arquivo publicado antes do `hr` que consta hoje.
3. 264 seções com `hr` entre 17:07 e 17:08 só apareceram no índice entre 19:11 e 19:12.
4. A soma dos 499.207 BUs confere com o total oficial das 23:27:02, e as assinaturas verificadas até agora são válidas. Este pedido não afirma divergência de votos. Busca documentar o que ocorreu com os boletins entre a geração na urna e a publicação.

**Informações requeridas**

1. **Ato e horários.** Cópia dos ofícios, ordens e mensagens que o TSE recebeu do STF sobre a prorrogação, com data e hora de recebimento, e dos atos internos que determinaram a suspensão da totalização e o **bloqueio do recebimento dos BUs** (horário de início e de fim, quem determinou, quem executou).
2. **Registro técnico do bloqueio.** Os logs do sistema de recepção/totalização (inclusive do Sistema Transportador) do período de 16h às 20h de 25/10/2026, ou relatório que informe: o que exatamente foi bloqueado (recepção, totalização, publicação ou os três), por qual mecanismo e em que equipamentos.
3. **Destino dos BUs gerados entre 17h e 19h.** Para as seções cuja urna emitiu o BU depois do início do bloqueio: onde o arquivo permaneceu (na urna, na rede, em fila ou armazenamento do TSE ou do TRE), se alguma tentativa de transmissão foi rejeitada ou aguardou, quem tinha acesso a esse armazenamento, e a hora em que cada BU foi efetivamente recebido. Pedimos a lista por seção em CSV.
4. **Capacidade e contingência.** O Presidente do TSE declarou não saber "ao certo" se haveria armazenamento. Pedimos o relatório ou nota técnica que avaliou essa capacidade e o plano de contingência aplicado, com data.
5. **O campo `hr`.** A regra do sistema que define o campo `hr` do repositório público (hora de geração, de recebimento ou da última tentativa) e se ela se aplica igualmente a seções recebidas durante e após o bloqueio. Pedimos também os motivos de 965 seções terem hoje `hr` posterior ao primeiro momento em que as vimos publicadas (187 delas com `hr` de 26/10).
6. **Votos depois das 17h.** O número de votos e de seções com voto registrado após as 17h, por UF, segundo os registros do TSE, e o critério usado para separar seções "encerradas às 17h" de seções "mantidas abertas". Há levantamento da imprensa (35.521 votos após as 17h) que o TSE não comentou.
7. **Urnas substituídas.** A relação das seções com urna substituída no 2º turno (o Presidente declarou 0,31%) e a hora da substituição, para as seções que estavam abertas durante a prorrogação.
8. **Publicação.** Se o TSE manteve o painel de resultados parado por decisão ou por limitação técnica, e a hora em que a divulgação voltou ao normal.

Pedimos a resposta em meio digital, em CSV para as listas por seção. Caso parte da informação seja considerada sigilosa, pedimos o fornecimento da parte não sigilosa e a indicação do fundamento legal (art. 7º, § 2º, da Lei nº 12.527/2011). O pedido é cooperativo: queremos esclarecer a cronologia e documentar a transparência do processo, e não apontar falha de ninguém.

Os requerentes se colocam à disposição para encaminhar o relatório da auditoria, as listas completas e os scripts que reproduzem as medições citadas, para que o Tribunal possa conferi-las.

Termos em que pedem deferimento.

[Local e data]

Jair da Silva Lima, por si e pelas publicações Folha dos Vales e Folha do Litoral Norte

---
Fontes dos fatos do item 1 (todas consultadas em 26/10/2026; as páginas do tse.jus.br retornaram erro 403 e não foram lidas):
- Agência Brasil, "Zanin manda ampliar horário de votação até 19h": https://agenciabrasil.ebc.com.br/justica/noticia/2026-10/zanin-manda-ampliar-horario-de-votacao-ate-19h
- Agência Brasil, "TSE diz que contagem dos votos será retomada às 19h": https://agenciabrasil.ebc.com.br/politica/noticia/2026-10/tse-diz-que-contagem-dos-votos-sera-retomada-19h
- Agência Câmara, 25/10/2026: https://www.camara.leg.br/noticias/1313728-presidente-do-tse-afirma-que-a-decisao-de-prorrogar-a-votacao-exigiu-medidas-extraordinarias
- Rádio Senado, 25/10/2026: https://www12.senado.leg.br/radio/1/noticia/2026/10/25/presidente-do-tse-afirma-que-prorrogacao-da-votacao-nao-comprometeu-a-apuracao
