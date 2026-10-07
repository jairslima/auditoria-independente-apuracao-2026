# Anexo A: atrasos e lacunas de dados (os pontos mais fracos da auditoria)

Parte de Auditoria Independente da Apuração 2026 by Jair Lima. Contato: jairslima@gmail.com.

Este anexo documenta, com os dados e a evidência de cada item, tudo o que atrasou, faltou ou ficou ambíguo. Foi escrito para que um revisor externo consiga julgar **quanto** cada ponto enfraquece as conclusões do `RELATORIO.md`. Dados brutos em `dados/`, scripts em `scripts/` (fase12, fase12b, fase13, fase14). Coleta principal em 05/10/2026 (tarde e noite) e 06/10/2026.

## 0. Resumo executivo

| # | Ponto | Seções | Votos em jogo (estimativa: seções × ~240; só o item 4 e o 6 são medidos) | Resolvido? | Efeito sobre as conclusões |
|---|---|---:|---:|---|---|
| 1 | Pausa do painel (apagão) | todas | n/a | descrito, causa só pela versão do TSE | nenhum sobre a soma; relevante para a reconstrução do painel |
| 2 | Seções cujos arquivos davam 404 na 1ª coleta | 68 | ~15 mil | sim, todas publicadas até 06/10 | nenhum: soma fecha ao voto com elas |
| 3 | Status "Recebida" no `aux.json` | 7.369 | ~2 milhões | sim para a soma; **significado do rótulo desconhecido** | nenhum sobre a soma |
| 4 | Seções do Sistema de Apuração (contingência, `busa`) | 31 | 1.348 | incluídas na soma; **assinatura não verificada** | pequeno: 1.348 votos sem verificação de assinatura |
| 5 | Cauda: registro depois de 23h41 | 743 | ~0,17 milhão | soma fecha; **o horário `hr` dessas seções não é horário de totalização** | enfraquece o uso de `hr` como ordem de chegada |
| 6 | Seções sem BU por não instaladas (exterior) | 41 | até 423 eleitores | explicado pelo cadastro | nenhum para o 1º turno |
| 7 | Urnas substituídas (3.033 de contingência, 50 RED) | 3.083 | n/d | BUs íntegros e consistentes; ligação urna original/substituta indisponível | nenhum para o resultado; ver seção 8 |

## 1. Quatro relógios diferentes (não confundir)

| Relógio | Onde está | O que significa | Evidência |
|---|---|---|---|
| Emissão do BU na urna | `dataHoraEmissao` dentro do BU | quando a urna emitiu o boletim, ao fim da votação | valores de 17h01 a ~20h41 de 04/10 nos exemplos examinados |
| Registro `hr` | `aux.json`, campo `hr` do hash | carimbo de registro do conjunto de arquivos da seção no repositório de divulgação | mediana 91 min depois da emissão (p90 164, p99 239, máximo 1.244 min), amostra aleatória de 3.000 seções (semente 2026) |
| Carimbo do índice | `-cs.json`, campos `da/ha` | carimbo de publicação do índice; **não é hora de chegada** | 99,3% das seções têm carimbo mais de 1 h depois do `hr`; mais frequentes: 05/10 00h52 (69.438 seções), 04/10 22h59 (40.750), 23h01 (36.249) |
| Geração do arquivo oficial | `dg/hg` no `.jws` | momento em que o TSE gerou o arquivo de resultado | Brasil 05/10 12h51m47s; PA 12h51m45s; PE 12h51m44s (dados de 12h51m05s) |

Consequência: **só o `hr` serve como proxy de ordem de chegada, e mesmo ele falha em parte da cauda (seção 6).**

## 2. A pausa do painel (apagão)

**Linha do tempo (imprensa):**
- O Tempo (publicada durante a pausa): painel parado desde **19h06min33s**, em 323.539 de 499.248 seções (64,81%); Flávio 49,58%, Lula 42,25%.
- Jornal de Brasília: parado até 19h06 (64,81%); **retomada às 20h08**, com 84,96%; a divulgação das eleições estaduais continuou normalmente. Duração: **cerca de 1h02**, não 47 ou 50 minutos como saiu durante a pausa.
- CNN Brasil: o presidente do TSE atribuiu o problema a "congestionamento no sistema de divulgação" por fluxo de dados acima do normal, afirmando que afetou a divulgação, não a contabilização; às 23h41 restavam 22 das 499.248 seções por totalizar.

**Vídeo da TV Senado (leitura própria dos quadros):** 64,81% de 19h20 a 19h56; 84,96% às 20h10. Os três estados do painel (47,26%, 64,81%, 84,96%) são reproduzidos pelos BUs com erro RMS de até 0,005 ponto percentual (`RELATORIO.md`, seção 5).

**O que o `hr` mostra durante a pausa (seção A de `fase12_atrasos.py`):**

| Faixa de 5 min | Registradas |
|---|---:|
| 18h30 a 19h15 (cada faixa) | ~22 a 26 mil (ritmo normal, com buracos curtos: 18h50 teve 6.562) |
| 19h20 | 12.481 |
| 19h25 | 8.392 |
| 19h30 | 2.834 |
| 19h35 a 19h50 | **0 (nenhum registro)** |
| 19h55 | 4.900 |
| 20h00 | 15.454 |
| 20h05 a 20h40 (cada faixa) | ~2.400 a 3.000, quase constante |
| 20h45, 20h50, 20h55 | 7.043, 9.415, 9.279 |
| 21h00 em diante | decai (2.219, 931, 772...) |

- **Maior intervalo sem nenhum registro na noite: 27,5 min, de 19h31m50s a 19h59m22s.** Outros: 16,3 min (23h54 a 00h11), 7,8 min (18h01 a 18h08).
- Durante a pausa do painel (19h06m33s a 20h08m00s) foram registradas 110.864 seções (257.937 na hora anterior e 47.667 na hora seguinte).
- Entre 20h05 e 20h40 o ritmo foi quase constante: 35 minutos com registro, entre 407 e 584 por minuto (mediana 504). Esse padrão regular é compatível com uma fila sendo drenada a taxa fixa; **é uma inferência, não um fato**.
- O painel de 20h10 (84,96% = ~424 mil seções) corresponde aos BUs com `hr` até ~19h59m30s. Ou seja, o painel ficava ~10 minutos atrás do registro.

**O que isso diz e o que não diz:**
- Diz: os próprios carimbos de registro dos BUs também pararam por 27,5 minutos e depois descarregaram em rajada. Isso é coerente com um gargalo de processamento dentro do TSE, e as urnas emitiram os boletins muito antes (17h a ~20h41).
- **Não diz** se a pausa foi de recepção das urnas, de processamento ou só de divulgação. A explicação do TSE (congestionamento de divulgação) **não é confirmada nem refutada** pelos dados públicos. Para separar, seriam necessários os logs de recepção do TSE, que não são públicos.

### 2.1 Hipóteses concorrentes sobre a pausa, e o que cada uma exigiria

Os dados públicos são compatíveis com mais de uma explicação. Nenhuma foi confirmada ou descartada.

| Hipótese | Compatível com os dados? | O que a falsificaria (e que dado precisaria) |
|---|---|---|
| Gargalo de processamento no TSE, com fila drenada a taxa fixa (explicação oficial: congestionamento na divulgação) | Sim: 27,5 min sem registros, rajada, depois ~500 por minuto | Log de recepção mostrando BUs chegando durante a pausa e sendo gravados depois, ou, ao contrário, BUs não chegando |
| Pausa deliberada ou técnica para reprocessamento ou reenvio de arquivos | Sim: o padrão no `hr` é igual | Registro de operação (changelog, ordem de serviço) do TSE; e comparação do hash dos arquivos antes e depois, que só o TSE tem |
| Falha de recepção das urnas (rede ou transmissão) na janela | Parcial: as urnas emitiram os BUs entre 17h e ~20h41, bem antes | Log de transmissão por seção |
| Pausa só de divulgação (o dado já estava totalizado) | Parcial: a divulgação estadual continuou; a presidencial parou | Hora de totalização de cada seção no banco do TSE |

O que os dados descartam, sem depender de hipótese: não houve alteração nos números do painel entre os três estados lidos, que são reproduzidos pelos BUs com erro de até 0,005 ponto percentual.

## 3. Seções cujos arquivos davam 404 na primeira coleta (68)

Primeira coleta em 05/10, à tarde e à noite (terminou às 19h06). Das 499.207 seções, 12.364 não responderam 200: 12.296 por HTTP 429 (limite de requisições **do meu cliente**, repetidas até concluir) e **68 por HTTP 404** (arquivo não existia no servidor).

| Zona | Seções | BU recebido (`hr`, 04/10) | Disponível a partir de |
|---|---:|---|---|
| Betim/MG, zona 316 | 30 | 20h08 a 20h59 | 1ª repetição (05/10) |
| MG, município 53716, zona 269 | 18 | 20h44 a 21h15 | 1ª repetição (05/10) |
| Uberlândia/MG, zona 279 | 5 | 20h52 a 20h55 | 3ª consulta (entre 05/10 e 06/10) |
| Betim/MG, zona 319 | 3 | 20h07 a 20h10 | 3ª repetição (06/10) |
| Carapicuíba/SP, zona 388 | 12 | 20h59 a 21h14 | 3ª repetição (06/10) |

- Todas foram registradas na onda logo após a retomada do painel e constam como "Totalizado". O que atrasou foi a **publicação dos arquivos**.
- Os BUs das 15 últimas (3 + 12) carregam exatamente as diferenças que existiam no total (Flávio 1.757, Lula 1.746, Cury 161, Renan 149, 162 nulos); a cadeia de hashes delas fecha. Com elas, o Brasil bate zero a zero.
**Hipóteses sobre as 15 seções que fecharam a diferença.** (a) Os arquivos foram publicados com atraso por um problema de processamento por zona (minha leitura, compatível com os lotes por zona). (b) Os arquivos foram gerados ou regerados depois, para fechar a conta, hipótese levantada na revisão crítica e compatível com os dados públicos. Contra (b): cada BU carrega a assinatura ECDSA do hardware da urna, e as 15 foram verificadas (assinatura e certificado válidos, número da urna igual ao do certificado); regerar um BU assinado exigiria a chave privada da urna. O BU delas foi emitido às 17h02 a 17h29 e registrado entre 20h07 e 21h14, como todas as outras do lote. Nenhuma das duas hipóteses pode ser descartada só com dados públicos: a prova seria o hash dos arquivos no momento do recebimento, que só o TSE tem.

- Não encontrei **nenhuma matéria da imprensa** sobre o atraso desses arquivos (duas buscas em 06/10).
- Não sei **por que** cada lote atrasou. Os lotes são por zona eleitoral, o que sugere processamento por zona (TRE ou sistema de divulgação), mas isso é hipótese.

## 4. Status "Recebida" (7.369 seções)

Na coleta de 05/10 (~19h), 491.838 seções constavam "Totalizada" e **7.369 "Recebida"**. Por UF: SP 5.125, MG 1.729, PA 506, PE 8, AM 1. Elas foram registradas (`hr`) de 04/10 17h43 a 05/10 15h24 (mediana 19h07).

Concentração por zona (seções "Recebida" de quantas da zona):

| Zona | "Recebida" | Da zona |
|---|---:|---:|
| Betim/MG, zona 316 | 529 | 559 |
| São Paulo, zona 397 | 518 | 518 |
| Betim/MG, zona 319 | 446 | 449 |
| Uberlândia/MG, zona 279 | 437 | 442 |
| Campinas, zona 378 | 424 | 424 |
| Campinas, zona 379 | 415 | 415 |
| Carapicuíba, zona 303 | 414 | 414 |
| Carapicuíba, zona 388 | 414 | 426 |

- **As zonas com arquivos 404 (seção 3) são as mesmas em que quase todas as seções estavam "Recebida".** Isso sugere um estado por zona, e que as seções 404 eram as últimas da zona a serem publicadas.
- **O rótulo não indica falta de voto no total.** O arquivo oficial de 05/10 12h51 já tinha 100% das seções totalizadas e a soma dos BUs, com essas 7.369 incluídas, bate exatamente. Logo "Recebida" às 19h de 05/10 não quer dizer "ainda fora do total".
- **Significado exato do rótulo: desconhecido.** Documentação do TSE que baixei não o define.

## 5. Seções do Sistema de Apuração (31)

- 29 no exterior (zz) e 2 em MG. As 29 do exterior são `apuracaoTotalmenteManual` (cédulas contadas manualmente, motivo 99); as 2 de MG são `apuracaoMistaBUAE` (mista, motivo 5).
- Registradas (`hr`) entre 20h00 e 22h29; 15 delas com carimbo de 20h00 a 20h01 (lote). BUs gerados pelo Sistema de Apuração entre 17h37 e 22h25.
- Votos de Presidente nessas 31: **1.348** (Flávio 552, Lula 624, brancos 21, nulos 40). Incluídos na soma, que fecha.
- **Limite:** são BUs gerados pelo Sistema de Apuração, com outro tipo de assinatura (`vscsa`). Sua assinatura **não foi verificada**; a cadeia de hashes foi. Nas 29 do exterior a contagem é manual (cédulas), e eu não tenho como conferi-la contra nenhuma urna.

## 6. A cauda: registro depois das 23h41 (743 seções)

- 743 seções com `hr` depois de 23h41 de 04/10; 735 depois da meia-noite; 681 depois das 03h; a última às **15h24m50s de 05/10**.
- Por UF: PA 621, PE 60, MA 45, BA 7, AM 7, MG 3.
- Maiores grupos (registro em 05/10): Belém/PA zona 97 (**354 de 354 seções da zona**, 13h41 a 14h19); Capanema/PA zona 25 (101 de 203, 12h40 a 13h23); Oeiras do Pará zona 45 (61 de 91); Cabo de Santo Agostinho/PE zona 15 (50, todas às 10h49); Gurupá/PA zona 26 (40, 11h05 a 15h24); Viana/MA zona 20 (34, todas às 01h56); Afuá/PA zona 16 (24); Juruti/PA zona 105 (23). As urnas emitiram os BUs normalmente (17h01 a 20h41).
- Tipos de arquivo: 515 delas têm o arquivo extra `imgbu` (imagem do boletim impresso), as outras 228 não.

**A contradição que enfraquece o `hr`:** o arquivo oficial do Pará foi gerado às **12h51m45s de 05/10**, com 20.827 de 20.827 seções totalizadas, e o total dele é **igual à soma dos BUs incluindo** as seções do Pará registradas depois disso (candidato 22: 2.163.957 nos dois; sem as 514 seções registradas depois de 12h51, seriam 2.111.749). Logo, para essas seções, **o `hr` não é o momento em que os votos entraram no total**. Hipótese não provada: o carimbo é de um novo registro do conjunto de arquivos (por exemplo, quando se acrescentou o `imgbu`).

Também **não se concilia** com a CNN (22 seções por totalizar às 23h41): meus 743 registros depois dessa hora não podem ser seções ainda fora do total.

Efeito: **o `hr` serve como ordem de totalização para a maioria das seções** (os três estados do painel batem), mas **não é confiável como horário de chegada para ~700 seções da cauda**. Isso não afeta a soma final, apenas a reconstrução cronológica.

## 7. Seções sem BU: as 41 não instaladas (exterior)

O cadastro de eleitorado por seção (dados abertos do TSE, `eleitorado_local_votacao_2026.zip`, 175,8 MB, fonte independente dos BUs) tem **517.179 seções distintas, o mesmo conjunto exato do índice** (zero faltando em qualquer lado). Dessas, 499.248 são "Principal" (= total oficial) e 17.931 "Agregada" (17.972 no índice; a diferença são as 41 abaixo).

- As **41 seções principais ativas sem BU** estão todas no exterior (zz), com 1 a 27 eleitores cada (Bridgetown, Chuy, Dacca, Harare, Kinshasa, Colombo, Sarajevo e outras), **423 eleitores no total**, igual aos 423 do campo "eleitores em seções não instaladas" (`esni`) do arquivo oficial.
- No índice do TSE elas aparecem **sem dados e sem seção principal** (não são agregadas a outra seção). Não sei por que não foram instaladas.
- Eleitorado: o cadastro soma 158.745.492 (principais ativas); o oficial informa 158.745.502 (diferença de 10, 0,000006%; o cadastro é de 06/10 06h29, o oficial é de 05/10 12h51).
- **Impacto no 1º turno: no máximo 423 votos**, contra uma margem de 3,5 milhões de votos até os 50%.

## 8. Urnas substituídas: quantas, e se os votos delas chegaram

Imprensa: 1.121 urnas substituídas (0,2%), sem votação manual (Exame e Jornal de Brasília, citando o TSE), número divulgado durante a apuração. Nos BUs (levantamento `fase13_substituidas.py`, 499.207 BUs, zero erros de leitura):

| Campo do BU | Valor | Seções |
|---|---|---:|
| Tipo de urna | 1, urna de seção | 496.143 |
| | 4, contingência que passou a ser de seção (**urna substituta**) | **3.033** (0,61%) |
| | 3, contingência (são as do Sistema de Apuração) | 31 |
| Tipo de arquivo | 1, urna de votação | 499.126 |
| | 2, **RED** (dados recuperados da urna original) | 50 |
| | 5 ou 4, Sistema de Apuração | 29 + 2 |
| Histórico de correspondências | preenchido | 0 |

O número final de substituições (3.033, ou 0,61%) é maior que o citado durante a apuração (1.121). Não sei se a diferença é de momento da contagem ou de critério. **Nenhum BU traz o histórico de qual urna substituiu qual** (campo opcional da especificação, vazio em todos), então **não consigo ligar a urna original à substituta pelos dados públicos**.

**Testes feitos (`fase13b_substituidas_teste.py`):**

1. **Consistência interna:** em **nenhum dos 499.207 BUs** a soma dos votos de Presidente difere do comparecimento que o BU registra, e em nenhum o comparecimento supera os eleitores aptos.
2. **Comparecimento das urnas substituídas contra as seções vizinhas da mesma zona** (se os votos da urna original se perdessem, o comparecimento da substituta cairia muito):

| Grupo | n | Comparecimento | Diferença para os vizinhos | Seções com déficit > 20 pp |
|---|---:|---:|---|---:|
| Urna substituída (tipo 4) | 3.033 | 77,39% | −0,65 pp (IC95% −0,81 a −0,49) | 1 |
| Controle: 3.033 seções normais sorteadas | 3.028 | 79,01% | +0,15 pp | 2 |
| RED (tipo 2) | 50 | 78,29% | −0,48 pp (IC95% −1,89 a +0,92) | n/d |

   - Percentis da diferença nas substituídas: p1 −11,9 pp, p5 −8,3, mediana −0,5, p95 +6,3 (controle: −11,3, −7,0, +0,5, +6,5). **Há um deslocamento pequeno e estatisticamente significativo** (em torno de 0,8 pp contra o controle, cerca de 2 eleitores por seção).
   - **Nenhuma seção com perda grande:** 1 seção com déficit maior que 20 pp (controle: 2) e nenhuma acima de 40 pp. Se os votos das urnas originais tivessem sido perdidos sistematicamente, apareceriam muitas seções com déficits de dezenas de pontos.
   - **Interpretação (hipótese, não provada):** o pequeno deslocamento é compatível com eleitores que desistem ou se atrasam por causa da troca de urna. Não tem como separar de perda de alguns votos.
3. **Eleitores aptos do BU contra o cadastro independente** (principal mais agregadas): iguais em 470.664 das 499.207 seções (94,3%); nas 28.543 restantes a diferença média é de 1,34 eleitor, 97,1% com diferença de até 3, com sinais para os dois lados (12.745 acima, 15.798 abaixo) e proporção igual nas urnas substituídas (6,1%) e nas normais (5,7%). A soma dos aptos dos BUs (158.745.079) mais os 423 das seções não instaladas dá **158.745.502, exatamente o total de eleitores do arquivo oficial**. As diferenças pequenas são compatíveis com atualizações do cadastro entre a carga das urnas (setembro) e a geração do arquivo (06/10).

**O que isto não prova:** que nenhum voto foi perdido numa urna que falhou. Prova que nenhum BU está internamente inconsistente, que não há seções com perda de grande escala, e que o total de eleitores fecha. Para ver perda pequena seria preciso comparar com o registro de comparecimento (`jufa`) e com o BU impresso.

## 9. O que cada conclusão depende destes atrasos

| Conclusão | Depende dos atrasos? |
|---|---|
| Soma dos BUs = total oficial, zero a zero | **Não.** Fecha com todas as 499.207 seções, e todos os atrasos foram resolvidos ou delimitados. |
| Cadeia de hashes e assinaturas íntegras | **Não**, exceto as 31 do Sistema de Apuração (assinatura não verificada). As 15 seções publicadas em 06/10 foram verificadas depois (assinatura e certificado válidos). A assinatura da eleição estadual foi verificada em **todas as seções que atrasaram** (68 + 743, todas válidas) e em 99.950 sorteadas em duas rodadas (100.761 seções no total, todas válidas). |
| Os 3 estados do painel de TV = BUs | **Sim**, usa o `hr` como ordem. Validado em 3 pontos; pode falhar para a cauda. |
| "Sem descontinuidade no apagão" | **Sim, em parte.** Vale para a ordem por `hr`; o 'buraco' de 27,5 min nos registros e a rajada seguinte limitam o que se pode afirmar sobre a recepção real. |
| Causa do apagão | **Não verificável** com dados públicos. |

## 10. Como fechar o que está em aberto

1. Pedir ao TSE o log de recepção e totalização por seção do dia 04/10 (hora de chegada real) e a definição dos status "Recebida/Totalizada".
2. Pedir ao TRE-PA e ao TRE-PE/MA a explicação para os registros de 05/10 (Belém zona 97 etc.).
3. Conferir assinatura das 31 do Sistema de Apuração com a especificação do `vscsa`.
4. Conferir `qtdEleitoresAptos` de cada BU contra o cadastro (principal mais agregadas) e a soma de votos contra o comparecimento (levantamento da fase 13).
5. Conferir o `log.jez` das seções do atraso (Betim 316 e 319, Uberlândia 279, Carapicuíba 388, Belém 97). **O RDV delas já foi conferido: as 68 que deram 404 e as 743 da cauda têm o RDV igual ao BU em todos os cargos** (`RELATORIO.md`, 6.1).

## 11. Correções que fiz durante o trabalho (transparência)

1. Eu havia tratado o `da/ha` do índice como hora de chegada: **errado**; é carimbo de publicação.
2. Eu havia escrito que as 15 seções finais "foram das últimas a chegar" (Betim 00h52, Carapicuíba 23h00): **errado**; foram registradas às 20h07 a 21h14, e esses horários são do índice.
3. Eu havia descrito a pausa do painel como 47 a 50 minutos: **errado**; ~1h02 (retomada às 20h08, segundo o Jornal de Brasília e conferido no vídeo às 20h10).
4. Eu havia dito que as 41 seções sem BU eram "agregadas": **errado**; são não instaladas.
5. Uma rodada da fase 8 saiu com erro meu (ordenação de chaves de tipos mistos) e eu a descartei e refiz inteira; os números do relatório vêm da rodada corrigida.
6. Três de 16 pares UF/cargo do teste aleatório (PE Dep. Estadual, SP Dep. Federal, PI Dep. Federal) tinham diferença no total de **legenda**. Todas explicadas exatamente com campos do arquivo oficial: partidos "Anulado sub judice" (PE +746; PI +634) e, em SP Dep. Federal (+1.173), votos de legenda do PCO nos nulos técnicos (5.737 + 1.173 = 6.910). Eu havia deixado o caso de SP em aberto e o fechei na auditoria completa de MG e SP (`RELATORIO.md`, 4.2.1).
7. Na auditoria de MG e SP, a primeira rodada deixou de fora os 2 BUs do Sistema de Apuração de MG e apontou divergências inexistentes; refeita com eles, bate ao voto. Além disso, lancei por engano a segunda rodada enquanto a primeira ainda gravava o mesmo log; o log final é da rodada corrigida e completa.

Contato: jairslima@gmail.com
