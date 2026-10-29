# Fase 24: relógio de chegada do monitor × hr do TSE (2º turno)

Auditoria Independente da Apuração 2026 by Jair Lima. Dados: `AuditoriaPresidente2026/segundo_turno/dados_monitor/` (curva oficial minuto a minuto e primeira vez que cada seção apareceu no índice) e `dados/aux.jsonl` (coletado em 26/10 pela manhã, NÃO na madrugada: a cópia da madrugada não foi feita).

## Fatos observados

1. **Congelamento da divulgação oficial.** O total nacional ficou em 1.225 seções (0,25%), gerado às 17:06:31, de 20:07:57Z a 22:02:13Z (17:08 a 19:02 de Brasília), cerca de 1h54min. O monitor consultou a cada ~2 min nesse intervalo (154 consultas gravadas, maior intervalo 121 s), então a ausência de mudança não é falha de coleta. Às 19:03:36 o arquivo passou a 1.909 seções e às 19:05:16 a 7.560 (1,51%).
2. **Nenhum recebimento (hr) entre 17:10 e 19:00 de Brasília.** Faixa de 20:00Z: 1.895 seções com hr; faixa de 20:10Z a 21:50Z: zero; faixa de 22:00Z: 6.124. O monitor também não viu nenhuma seção nova no índice de 20:20Z a 22:10Z.
3. **264 seções com hr de 17:07 a 17:08 só apareceram no índice às 19:11 a 19:12** (atraso de 7.397 a 7.523 s). É o grupo que ficou esperando o fim do congelamento.
4. **Mediana de 403 s** entre o hr de uma seção e o momento em que o monitor a viu no índice (p90 568 s, p99 708 s). Esse é o atraso normal de publicação.
5. **965 seções foram vistas pelo monitor ANTES do hr que o TSE mostra hoje** (708 do exterior, 124 PE, 53 PA, 47 RS, 16 SP, 12 AM, 5 PR). Em 187 delas (PE 124, PA 51, AM 12) o hr atual é de 26/10 (a partir de 08:34 de Brasília), ou seja, o hr foi reescrito depois de a seção já estar publicada; 255 dessas estão com status "Recebida" e arquivo `imgbu`. Isso confirma, com relógio próprio, o que o TRE-MA mostrou no 1º turno: **o hr público reflete a última tentativa de envio, não a chegada**.

## Dados oficiais sobre o congelamento (pesquisados em 26/10/2026; páginas do tse.jus.br retornaram HTTP 403 e NÃO foram lidas, os dados abaixo vêm de Agência Brasil, Agência Câmara, Rádio Senado e imprensa)

- **Decisão:** o ministro Cristiano Zanin, do STF, concedeu liminar determinando "prorrogação por até duas horas, até às 19h, horário de Brasília, do encerramento do recebimento dos votos em todas as seções do Brasil", cabendo ao TSE "dar cumprimento". Pedido da campanha de Lula (falta de ônibus em Salvador, Feira de Santana e Lauro de Freitas); a campanha de Flávio Bolsonaro também pediu prorrogação em 17 municípios de SP, PR e SC. O fato chegou ao STF às 16:23:49 segundo a Agência Brasil (a TV Senado cita 16h32min49s). Agência Brasil publicou a decisão às 17h07. Número do processo: não encontrado.
- **Alcance:** Zanin esclareceu depois que valia para as seções que ainda estavam abertas; a Agência Câmara registra que "foi aplicada apenas às seções que ainda não haviam encerrado as atividades às 17h". A Agência Brasil informa que a decisão chegou ao TRE-RJ depois das 17h, com a votação já encerrada em muitas seções e o boletim emitido.
- **Efeito na totalização:** "A contagem dos votos foi suspensa às 17h06, com 1.225 das 499.248 seções apuradas" (Agência Brasil, 25/10, 18:48); retomada anunciada para as 19h.
- **Explicação do presidente do TSE, Kassio Nunes Marques** (Agência Câmara 25/10 22:42; Rádio Senado 25/10 22:15): a prorrogação exigiu "o bloqueio temporário do recebimento dos boletins de urna"; "Isso gerou uma contenção extraordinária nos boletins de urna"; "Não sabíamos, ao certo, se teríamos armazenamento"; "demos fluência à totalização, ao recebimento dos pacotes de boletim". Segundo a Agência Câmara, o pedido chegou por volta das 15h30 (diverge dos 16:23:49 da Agência Brasil). Afirmou que a prorrogação "não comprometeu a apuração" e que 0,31% das urnas precisaram ser substituídas.
- **Votos depois das 17h:** levantamento do G1, com logs das urnas, aponta 35.521 votos para presidente registrados após as 17h (30.866 em seções já "Totalizado", 4.655 em seções ainda dependentes de validação), em 497.897 seções analisadas. O TSE confirmou a metodologia à Gazeta do Povo e não comentou os números. Outra contagem (CNN Brasil, dados do TSE) fala em cerca de 34 mil.

## Cruzamento: o que os nossos dados dizem sobre a explicação oficial

- **Coincide:** a curva oficial para em 1.225 seções com geração às 17:06:31, igual ao número e ao horário informados pelo TSE; as novas seções voltam a aparecer a partir de 19:03:36.
- **Coincide:** nenhuma seção tem `hr` entre ~17:10 e 19:00 e o índice não ganhou seções novas nessa janela. Isso é compatível com o **bloqueio do recebimento** declarado pelo TSE. Os nossos dados NÃO sustentam a hipótese de que o TSE "recebeu e guardou sem publicar": o `hr` público é o da última tentativa de envio (TRE-MA, 1º turno; 965 seções vistas antes do `hr` atual neste turno), então ele não consegue provar nem desmentir recebimento escondido. O que os dados mostram é ausência de registro de recebimento; o TSE diz que bloqueou.
- **Não verificável por nós:** se os pacotes de BU das urnas que fecharam às 17h ficaram retidos na urna ou em fila no TSE, e por quanto tempo. A pergunta correta ao TSE (LAI): em que equipamento ficaram os BUs gerados entre 17h e 19h, quem os acessava, e qual o registro (log) do bloqueio e do desbloqueio.
- **A verificar com os logs das urnas (fase 21):** o instante de geração de cada BU gerado em seções que fecharam entre 17h e 19h, e os 35.521 votos após as 17h por seção.

## Verificações que fecharam sem diferença

- Soma dos 499.207 BUs × total oficial (23:27:02 de 25/10): diferença zero para os dois candidatos, no Brasil e nas 27 UFs mais exterior. 29 seções do exterior só têm `busa` (Sistema de Apuração) e foram incluídas.
- Cadeia de hashes das tuplas: 0 erros de tupla, de ordem e de hash final em 499.207 BUs.
- Assinaturas (fase 9): em andamento; as 54.000 primeiras (ordem aleatória) estavam todas com certificado e assinatura válidos.

## O que NÃO se pode concluir

- O monitor não distingue "o TSE não recebeu" de "o TSE recebeu e não publicou" durante o congelamento. Isso só o TSE responde (pedido LAI).
- A cópia do `aux.json` da madrugada não existe; a comparação "Recebida × Totalizada" no tempo ficou perdida.
- Conferência da soma e das assinaturas prova consistência com o que as urnas produziram, não que cada voto foi gravado fielmente.
