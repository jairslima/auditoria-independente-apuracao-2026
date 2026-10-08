# Auditoria independente refaz a soma de 499 mil urnas do 1º turno e o resultado de Presidente bate com o do TSE, voto a voto

*Trabalho feito só com arquivos públicos confere assinaturas, municípios e eleição estadual; também mostra a pausa do painel em números e lista o que só o TSE e os TREs podem explicar, com pedidos de informação já protocolados*

Quem acompanhou a apuração do 1º turno, na noite de 4 de outubro, viu o painel do Tribunal Superior Eleitoral (TSE) parar por mais de uma hora e ficou com a pergunta que sempre volta: dá para conferir se a conta fecha? Uma auditoria independente, feita por um jornalista com arquivos públicos do próprio TSE, refez a soma urna por urna e respondeu: dá, e fecha. Os boletins de urna (BUs) das 499.207 seções instaladas somam exatamente os 119.300.788 votos válidos do resultado oficial de Presidente. Não há diferença de um único voto, em nenhum candidato, nos brancos ou nos nulos.

O trabalho vai além de dizer que a conta fechou. Ele mede a pausa do painel, mostra que 15 seções que demoraram a aparecer eram exatamente a diferença que faltava na primeira soma, verifica as assinaturas digitais das urnas e aponta, sem esconder, os pontos que os dados públicos não explicam. Para esses, o autor já protocolou pedidos de acesso à informação no TSE e nos tribunais regionais. A auditoria **não encontrou fraude**: encontrou consistência e perguntas.

O autor é Jair Lima, jornalista responsável pela Folha dos Vales e pela Folha do Litoral Norte, com pós graduação em Investigação Forense e Perícia Criminal e formação em tecnologia da informação. É uma auditoria técnica, sem contratação nem pedido de qualquer parte. **Não é perícia judicial nem laudo oficial.**

## Em números

* **499.207** seções instaladas com boletim de urna lido, mais 41 não instaladas no exterior (423 eleitores).
* **0** votos de diferença entre a soma dos boletins e o total oficial de Presidente.
* **5.757 de 5.757** municípios e postos no exterior iguais ao arquivo oficial, mais as 27 UFs e o exterior.
* **108 de 108** combinações de UF e cargo da eleição estadual iguais (18.839 candidatos conferidos um a um).
* **499.176 de 499.176** assinaturas digitais de urna válidas em Presidente, mais as 31 do Sistema de Apuração.
* **27,5 minutos** sem nenhum registro de boletim durante a pausa do painel.

## Como uma pessoa refaz a conta de 499 mil urnas

Ao fim da votação, cada urna eletrônica emite o boletim de urna: um arquivo com os votos daquela seção e uma assinatura digital gerada pela própria máquina. O TSE publica esses arquivos, um por seção, para qualquer pessoa. Entre 5 e 7 de outubro, o autor baixou os de todo o país, leu os arquivos com dois programas independentes que seguem a especificação oficial do TSE e somou os votos seção por seção, município por município e estado por estado. Depois comparou cada soma com os arquivos de resultado do TSE.

Cada boletim carrega uma proteção em cadeia: cada linha de votos é amarrada à anterior por uma impressão digital (hash), e a última é assinada pela urna. A auditoria refez essa cadeia em 67,86 milhões de linhas, nos 499.207 boletins, sem erro, e verificou a assinatura e o certificado de cada urna contra as chaves raiz do TSE. O registro digital do voto, que guarda cada voto embaralhado dentro da mesma urna, também foi comparado com o boletim em 20.811 seções (cerca de 4% do total), com as mesmas somas.

## O que bateu

| Candidato | Soma dos boletins | Resultado oficial |
|---|---:|---:|
| Flávio Bolsonaro (22) | 56.104.503 | 56.104.503 |
| Lula (13) | 53.879.538 | 53.879.538 |
| Augusto Cury (70) | 3.448.569 | 3.448.569 |
| Renan Santos (14) | 2.675.887 | 2.675.887 |
| Ronaldo Caiado (55) | 2.605.148 | 2.605.148 |
| Zema (30) | 326.488 | 326.488 |
| Demais candidatos | 260.655 | 260.655 |
| Brancos | 2.300.798 | 2.300.798 |
| Nulos | 3.669.003 | 3.669.003 |

Flávio Bolsonaro terminou com 47,03% dos votos válidos e Lula com 45,16%, uma margem de 2.224.965 votos, igual nos boletins e no oficial. Para vencer no 1º turno, Flávio precisaria de 3.545.892 votos a mais.

A igualdade vale em todos os níveis testados. Na eleição estadual, Governador, Senador, Deputado Federal e Deputado Estadual ou Distrital fecham nas 27 UFs, e o Governador bate nos 5.571 municípios. No Rio Grande do Sul, por exemplo, os 3.516.048 votos de Zucco, os 1.917.374 de Juliana Brizola e os 510.698 de Gabriel Souza para o governo, e os votos de Sanderson, Marcel van Hattem e Manuela d'Ávila para o Senado, saem dos boletins idênticos ao arquivo oficial. Em São Paulo, Tarcísio (14.491.874) e Haddad (8.423.656); em Minas, Cleitinho Azevedo (6.321.590) e Patrus Ananias (3.006.088); em Pernambuco, Raquel Lyra (2.805.438) e João Campos (2.360.469).

As únicas diferenças encontradas na eleição estadual são de votos de legenda, e todas têm explicação exata em campos do próprio arquivo oficial: partidos com situação "anulado sub judice" e votos que o TSE classifica como nulos técnicos. Nenhuma ficou sem explicação.

### A conta que só fechou quando as últimas 15 seções apareceram

Na primeira soma, a auditoria ficou abaixo do oficial em Flávio 1.757 votos e em Lula 1.746. A diferença estava concentrada em 15 seções, 3 de Betim (MG) e 12 de Carapicuíba (SP), cujos arquivos o TSE ainda não tinha publicado. Quando eles apareceram, entre 5 e 6 de outubro, a soma fechou ao voto. Ou seja: a lacuna era exatamente o que faltava no download, e não uma divergência de resultado.

## A pausa do painel, em números

O painel do TSE ficou sem atualizar de 19h06min33s até as 20h08, com 64,81% das seções, cerca de 1h02. O presidente do Tribunal atribuiu o problema a congestionamento no sistema de divulgação. A auditoria não confirma nem refuta a causa, mas mede o que os dados mostram.

**Os números dos boletins não dão salto.** Os três estados do painel exibidos pela TV Senado, antes, durante e depois da pausa (47,26%, 64,81% e 84,96% das urnas apuradas), são reproduzidos pelos boletins com erro de no máximo 0,005 ponto percentual. Nada se encaixa de forma abrupta entre um estado e outro.

**Os carimbos de registro também pararam.** Cada seção tem um carimbo de quando seus arquivos foram registrados no repositório do TSE. Entre 19h31min50s e 19h59min22s, nenhum registro: 27,5 minutos de silêncio. Depois veio uma rajada e um ritmo quase constante de cerca de 500 seções por minuto, entre 20h05 e 20h40. É coerente com um gargalo dentro do TSE, mas os dados públicos não dizem se a pausa foi de recepção, de processamento ou só de divulgação.

**A queda de Flávio tem explicação geográfica.** Ele chegou a 51,3% dos votos válidos às 17h58 e terminou com 47,03%. Nunca esteve acima de 50% no estado congelado do painel. A queda se explica em boa parte pela ordem em que as regiões foram chegando: controlando por município, a diferença remanescente cai de 0,70 ponto percentual às 19h06 para zero até as 21h.

## O que os dados públicos não explicam

O relatório lista, ponto por ponto, o que continua em aberto. Nenhum deles altera a soma final; todos afetam a reconstrução do que aconteceu e quando.

**1. Arquivos que apareceram depois (68 seções).** Na primeira coleta, em 5 de outubro, 68 seções de cinco zonas (Betim, Teófilo Otoni e Uberlândia, em Minas; Carapicuíba, em São Paulo) davam "arquivo não encontrado". Os boletins delas tinham sido registrados na noite da eleição, entre 20h07 e 21h15, e todas constavam como totalizadas: o que demorou foi a publicação dos arquivos. Foram publicados até 6 de outubro.

**2. Registros no dia seguinte (743 seções).** Seções com registro depois das 23h41 de 4 de outubro, até as 15h24 do dia 5: Pará 621, Pernambuco 60, Maranhão 45, Bahia 7, Amazonas 7 e Minas 3. A maior parte vem de zonas inteiras, como Belém, zona 97 (354 de 354 seções, entre 13h41 e 14h19). O que chama a atenção é que o arquivo oficial do Pará, gerado às 12h51 de 5 de outubro, já tinha o total igual à soma dos boletins, incluindo essas seções. Logo, o carimbo de registro delas não é o momento em que os votos entraram no total: o campo serve de referência de ordem para a maioria, mas não de horário de chegada para essa cauda.

**3. O rótulo "Recebida" (7.369 seções).** Na coleta de 5 de outubro, 491.838 seções constavam "Totalizada" e 7.369 "Recebida", concentradas em São Paulo (5.125), Minas (1.729) e Pará (506). O oficial já contava 100% das seções, então o rótulo não indica voto fora do total. O achado novo: o estado "Recebida" coincide exatamente com a presença do arquivo de imagem do boletim. As 7.369 têm a imagem publicada, e nenhuma das 491.838 "Totalizada" tem. É uma correlação; o significado do rótulo só o TSE pode dizer.

**4. Sistema de Apuração (31 seções, 1.348 votos).** São 29 seções no exterior e 2 em Minas cujos boletins não vieram direto da urna, e sim do Sistema de Apuração, que registra o resultado por digitação. A auditoria verificou a assinatura dos 31, que é válida, e leu o registro de eventos (log) dessas máquinas: no exterior, aparece a digitação de um boletim do exterior, só para Presidente, em cerca de 1 a 3 minutos por seção; em Minas, a digitação do boletim mais cédulas, com o motivo "urna encerrada com eleitores na fila", nas duas.

**5. Urnas substituídas.** Os boletins mostram 3.033 seções com urna de contingência que passou a ser da seção e 50 de recuperação de dados, contra 1.121 substituições divulgadas durante a apuração. Todos os boletins são consistentes, e o comparecimento dessas seções ficou 0,65 ponto percentual abaixo do das vizinhas, sem nenhuma com perda grande. O boletim não registra qual urna substituiu qual.

### Olhando dentro da urna

Para ver se algo na urna explicava os atrasos, o autor leu o registro de eventos de 811 seções atrasadas ou registradas no dia seguinte e o comparou com o de 1.500 seções sorteadas como controle. A urna gera o boletim na mesma hora típica nos três grupos (mediana 17h07 no controle, 17h16 nas 743, 17h13 nas 68), e os alertas e erros aparecem em proporção parecida. Não há nada na urna que explique o atraso. O único sinal pequeno: erro de leitura da mídia de resultado em 1,1% das 743, contra 0,3% do controle, concentrado em poucas zonas. O log não registra a transmissão (a mídia é lida na zona), por isso não responde ao horário de recebimento.

## O que esta auditoria não prova

O boletim de urna é a saída da própria urna. A auditoria mostra que a totalização é consistente com os boletins e que eles não foram alterados depois de assinados, pelos métodos usados. Ela **não prova que a urna gravou fielmente o voto digitado pelo eleitor**: isso exige o boletim impresso na seção e auditoria presencial. As chaves e a especificação usadas para validar as assinaturas vêm do próprio TSE. O registro voto a voto foi conferido por amostra (20.811 seções) e a assinatura da eleição estadual também (100.761 seções), embora a cadeia de hashes tenha sido verificada em todos os boletins.

## O que foi perguntado ao TSE e aos TREs

Em 7 de outubro, o autor e as duas publicações enviaram pedidos de acesso à informação (Lei 12.527/2011) ao TSE e aos tribunais regionais eleitorais do Pará, de Pernambuco, do Maranhão, de Minas Gerais e de São Paulo. Pedem os horários de recebimento, totalização e publicação de cada uma das 842 seções do anexo, o relatório técnico da pausa do painel, a definição dos estados "Recebida" e "Totalizada", o critério de contagem das urnas substituídas e a razão de cada atraso. O TSE registrou o pedido sob o protocolo 81136107180936 e o TRE de Pernambuco, sob o 81151008080724; os demais tribunais ainda não haviam informado protocolo. O prazo legal de resposta é de 20 dias, prorrogável por mais 10. As respostas serão cruzadas com o relatório e publicadas.

## Confira você mesmo

A página com o resumo e a consulta por município e por candidato está em **www.folhadosvales.com.br/auditoria-2026**. O relatório completo, o anexo de atrasos, os scripts para repetir a conta e os pedidos de informação estarão no repositório **github.com/jairslima/auditoria-independente-apuracao-2026**. A auditoria foi concluída em 7 de outubro de 2026 e continua aberta à conferência. Um kit para repetir o trabalho no 2º turno, com registro próprio de horário de chegada de cada seção, já está pronto.

**Jair Lima**, jornalista, registro profissional 0024314/RS, responsável pela Folha dos Vales e pela Folha do Litoral Norte. Contato: jairslima@gmail.com.
