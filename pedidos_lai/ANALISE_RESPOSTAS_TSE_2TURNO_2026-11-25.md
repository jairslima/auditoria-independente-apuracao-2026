# Análise das respostas do TSE ao 2º turno (protocolos 83192627165101 e 83236428120806)

Data da análise: 25/11/2026. Respostas recebidas em 09/11/2026 (18:01 e 18:06), registradas só em 25/11. Texto integral em `respostas/TSE_2026-11-09/`. Script: `scripts/fase30_recebimento_bu_2turno.py`; saída: `AuditoriaPresidente2026_T2/resultados/fase30_recebimento_bu.json`.

Fonte do teste: arquivo oficial "Detalhe da apuração por seção eleitoral" (`detalhe_votacao_secao_2026.zip`, dados abertos do TSE, Last-Modified 26/10/2026 15:35 GMT, geração interna 26/10/2026 09:49:06), que traz os dois turnos. A nota anterior de que o arquivo baixado em 29/10 trazia só o 1º turno não vale para este arquivo; a cópia usada antes era provavelmente antiga e não foi conferida de novo.

## 1. O que o TSE respondeu, item a item, contra os dados

| Tema | O que o TSE disse | O que os dados mostram | Situação |
|---|---|---|---|
| 1.870 seções entre 17h e 17h07 | "totalizados e divulgados" | Arquivo oficial: 1.870 BUs de urna com recebimento e 1ª totalização parcial até 17:07:37 (1.225 até 17:06:31, 1.479 até 17:07:01). O número 1.870 CONFERE. | Confirmado |
| "Divulgados" | idem | Curva pública congelada em 1.225 (17:06:31); 1.456 só apareceram às 19:02; 1.909 às 19:03. Os 645 entre 1.225 e 1.870 foram totalizados em até 66 s mas só ficaram públicos depois das 19h. | Parte "divulgados" NÃO confere com o que o público viu |
| Suspensão às 17h07 | cumprimento de decisão judicial, sem falha técnica | O último BU de urna totalizado é de 17:07:37; depois disso, nenhuma 1ª totalização até 19:02:54. Compatível. | Compatível |
| Recebimento 17h a 19h | BUs "armazenados em fila", "não houve interrupção no recebimento" | No arquivo oficial NENHUM BU de urna tem recebimento entre 17:07:38 e 19:00. Só 39 registros do exterior (zona ZZ, origem "Totalização", comparecimento 0), entre 17:10:19 e 18:56:40, com 1ª totalização às 19:02:54. Depois das 19h: 6.220 recebimentos em 19:00 a 19:10 e 4.509 em 19:10 a 19:20. | Ver 2 |
| Soma até as 19h | | 1.870 + 39 = 1.909, igual ao arquivo público gerado às 19:03:36 (1.909 seções). | Confirma que o que o público viu às 19h03 é o que o arquivo oficial registra |
| Campo `hr` | último recebimento (retransmissão ou totalização final), não o primeiro | Coerente com as duas coletas: 7.017 seções de "Recebida" para "Totalizada" e 1.736 de "Totalizada" para "Recebida", nenhum hash mudou. As 965 seções (187 com `hr` de 26/10) explicadas por retransmissão ou totalização final. | Explicação aceita como compatível; não verificada seção por seção |
| Item 3 do complemento | o hash com st="Totalizado" é o do BU usado | Hash nunca mudou entre as coletas (0 de 499.207). | Compatível |
| Votos após 17h | "cerca de 34 mil" | Nossos logs: 34.810 em 30.086 seções. A imprensa citou 35.521. "Cerca de 34 mil" está perto do nosso número e longe do da imprensa. | A diferença de 711 para a imprensa segue sem explicação; o TSE não a explica |
| Urnas substituídas | 1.947 de 499.178 (0,39%), com 1 no exterior | Logs: 1.432 seções (0,287%) com 2 ou 3 urnas. Em 25/10 o presidente do TSE falou em 0,31%. | Três números diferentes (0,287%, 0,31%, 0,39%); ver 3 |
| Logs | só Entidades Fiscalizadoras, por ofício à Presidência (arts. 46 e seguintes e 6º da Res.-TSE 23.673/2021) | | Pedido de log por LAI não atendido; ver 4 |

## 2. A tensão principal: "sem interrupção no recebimento" contra o campo de recebimento

Duas afirmações do TSE não cabem juntas com o arquivo oficial:

1. 25/10, presidente do TSE: a prorrogação exigiu "o bloqueio temporário do recebimento dos boletins de urna".
2. 09/11, Ouvidoria: "não houve interrupção no recebimento dos arquivos"; os BUs de 17h a 19h ficaram em fila.
3. A própria resposta define `dr`/`hr` como "data e hora de recebimento". O arquivo oficial "Detalhe da apuração por seção" traz o recebimento de cada BU, e nenhum BU de urna tem recebimento entre 17:07:38 e 19:00. Os logs das urnas mostram 101.863 BUs gerados entre 17:06:31 e 19:00, a maioria deles com recebimento oficial só depois das 19h.

Só há duas leituras, e os dados não escolhem entre elas: (a) o recebimento foi bloqueado até as 19h, como disse o presidente do TSE, e então "fila" significa fila nas urnas ou nos TREs; ou (b) o recebimento ocorreu em fila, e o campo oficial registra o momento em que o BU saiu da fila e foi processado, e não o recebimento. Na leitura (b), o campo não serve como prova de bloqueio, e a resposta "o `hr` é o horário de recebimento" teria de ser corrigida. Pergunta fechada que decide: o campo `DT_RECEBIMENTO_BU_HOR_TSE` é o horário em que o arquivo chegou ao TSE ou o horário em que saiu da fila para processamento?

Nada disto prova adulteração: os hashes não mudaram e as assinaturas fecham (ver relatório). É uma inconsistência de descrição do processo.

## 3. Urnas substituídas: 1.947 contra 1.432

- O TSE agora diz 1.947 (0,39%) de 499.178 "urnas com logs processados". Em 25/10 disse 0,31% (cerca de 1.548). Nossos logs mostram 1.432 seções (0,287%).
- 499.178 é o mesmo número de assinaturas de BU de urna que verificamos, então a base é a mesma.
- Os 515 a mais que nos logs (1.947 menos 1.432) cabem na hipótese já registrada no relatório: trocas antes do primeiro voto não dividem votos entre urnas, e nós só contamos urnas com registro no log do dia. Não foi procurado e continua não verificado.
- O que o TSE não explica é por que o percentual subiu de 0,31% para 0,39% em duas semanas.

## 4. Pedido de logs

A resposta ao item 2 muda a via: log só por ofício de Entidade Fiscalizadora (art. 6º da Resolução 23.673/2021) à Presidência do TSE. Não é uma via aberta a este projeto. Prazo de recurso da LAI (em regra 10 dias da ciência, ou seja, até cerca de 19/11/2026) já passou; a Ouvidoria também não tratou o item como negativa formal. Decisão do Jair: se vale pedir a algum partido ou entidade fiscalizadora que faça o ofício. Não decidido.

## 5. O que muda no relatório do 2º turno

- 4.2: o teste anunciado ("se o horário de recebimento de algum BU estiver entre 17h06 e 19h...") foi feito. Resultado: nenhum BU de urna entre 17:07:38 e 19:00; 39 registros do exterior (origem "Totalização"). Isso é compatível com o bloqueio declarado em 25/10 e incompatível com "sem interrupção no recebimento", a não ser que o campo registre a saída da fila (seção 2).
- 4.4: o pedido de acesso à informação foi respondido em 09/11 (dentro do prazo de 15/11).

## 6. Pendências

1. Decidir se haverá réplica ao TSE com a pergunta fechada da seção 2 e a diferença 1.870 "divulgados" contra 1.225 públicos. Nada enviado.
2. Ler a matéria do TSE sobre "cerca de 34 mil votos" (as páginas do tse.jus.br retornaram 403 antes; não lida).
3. Comparar o `hr` do aux.json com o recebimento do arquivo oficial nas 965 seções (explicação de retransmissão), como foi feito para o TRE-PA no 1º turno.
4. Republicar relatório e página do 2º turno, push (rodar `audit-vulnerabilidades.py` antes) e matéria da Folha: aguardam o Jair.
