# Resposta do TRE-PE ao pedido LAI (protocolo 81151008080724)

**Situação:** e-mail "Resposta de Protocolo" recebido em 19/10/2026 às 14h04 (Brasília), id Gmail `1a1551f739bf1bba`, remetente naoresponda-sac-tre-pe@tse.jus.br, resposta da STIC do TRE-PE ("SAC JE 811510"). Pesquisa de satisfação enviada junto (id `1a1551ee679a5a60`), com a solicitação "concluída em 19/10/2026, às 14:04".

**Anexos (analisados em 19/10/2026; guardados em `pedidos_lai/respostas/TRE-PE_2026-10-19/`, pasta no `.gitignore`):**
1. `Auditoria_de_Arquivos_Recebidos__Demanda_811510_Ouve_.pdf` (nº 3532972): 36 páginas, planilha larga cortada em 3 blocos de colunas. Reconstruída em `_analise/auditoria_arquivos_recebidos_PE.csv`: 605 linhas (arquivos de pacote), 60 seções, alinhamento conferido (0 linhas desalinhadas entre máquina de origem e sistema do pacote).
2. `Consulta_de_BUs_rejeitados_3220_PE.pdf` (nº 3532994): 3 páginas, **129 registros** (confere com o número informado), todos com a mensagem "Erro por retransmissão de uma seção já recebida". Em `_analise/bus_rejeitados_PE.csv`.
3. Script do cruzamento: `_analise/cruza_tre_pe.py` (saída `_analise/cruza_pe_60_secoes.csv`).

## Resultados do cruzamento (60 seções do anexo x planilha x lista de 129)

| Fato | Resultado |
|---|---|
| Pacotes por seção | **2 em todas as 60**: o 1º vindo da urna pelo JE Connect (máquina `127.0.1.1`) em 04/10, o 2º pelo **Transportador Web** (retransmissão). Cada pacote traz `bu.dat`, `hash.dat`, `vota.vsc`, `rdv.dat` e `log.jez` (um pacote aparece com os 5 arquivos listados em duplicidade). |
| Chegada do BU original ao TSE | Em **60 de 60** o 1º recebimento no TSE foi em 04/10, **antes das 22:54:57**, hora da totalização de Governador e Senador em PE informada pelo tribunal. Da geração na urna ao 1º recebimento: 38 a 126 min (mediana 67). |
| Geração na urna (planilha) x emissão do BU (anexo) | A planilha é 47 a 225 s mais tarde (mediana 65 s); nunca iguais. São grandezas diferentes (geração do pacote x emissão do BU); anotar para não comparar como se fossem a mesma. |
| Rejeições do anexo | As **60 seções têm rejeição** na lista (uma delas tem 2). |
| Lotes de rejeição | Os 129 registros foram gravados em **apenas 2 minutos**: **05/10 10:49 (52 registros)** e **06/10 12:58 (77 registros)**. |
| Municípios das 129 | Cabo de Santo Agostinho 52, Carnaubeira da Penha 31, Toritama 28, Miranda 9, Paulista 7, Limoeiro 1, Recife 1. |
| O que o `hr` público mostra nas 60 | **51** (50 de Cabo de Santo Agostinho, zona 15, e 1 de Limoeiro, zona 24) tiveram a rejeição no lote de **05/10 10:49** e `hr` = hora da rejeição. **9** (1 de Cabo, zona 121; 7 de Paulista, zona 114; 1 do Recife, zona 3) tiveram a rejeição só no lote de **06/10 12:58**, e o `hr` delas é a hora do recebimento do 2º pacote no TSE (12h30 a 14h40 de 05/10). Os dois grupos não se sobrepõem (51 + 9 = 60). |
| As outras 67 seções rejeitadas (fora do anexo) | Carnaubeira da Penha, Toritama, Miranda etc. (todas no lote de 06/10 12:58) foram rejeitadas igualmente, mas o `hr` público delas **continuou o do envio original** (04/10, por exemplo 20h49 em Carnaubeira da Penha). Por isso não entraram no anexo. |

## O que o tribunal afirma e o que os dados mostram

1. **Explicação geral (retransmissão por engano com biometria, BU rejeitado):** bate com os dados. Todas as 60 seções têm um 2º pacote completo pelo Transportador Web e uma rejeição por retransmissão. Nenhuma foi recuperada nem passou pelo Sistema de Apuração (conferido: o status delas no `aux` é "Totalizada" e nenhuma das 60 está entre as 31 seções do Sistema de Apuração, que são 2 de MG e 29 do exterior).
2. **O BU original chegou antes da totalização:** confirmado pela planilha do próprio tribunal (60 de 60). Isso encerra, para PE, a dúvida sobre "BU que só chegou no dia seguinte": o registro de 05/10 é de uma retransmissão.
3. **Item 5 (50 seções às 10h49) — a explicação do tribunal é só parcial.** Ele diz que a zona leu todas as mídias e transmitiu tudo de uma vez. A planilha confirma que a zona 15 transmitiu o 2º pacote numa janela curta, **das 09h57 às 10h04 de 05/10 (8 minutos diferentes)**, mas as rejeições dessas seções foram gravadas **todas às 10h49:32-34**, cerca de **45 a 52 minutos depois**. Para o conjunto das 60, o intervalo entre o recebimento do 2º pacote e a rejeição vai de 45 min a 24 h (mediana 48 min), porque o TSE grava as rejeições em **2 lotes** (05/10 10h49 e 06/10 12h58). O "mesmo minuto" vem, portanto, do **processamento em lote das rejeições no TSE**, e não do horário da ação da zona.
4. **O `hr` público não é critério confiável nem uniforme.** Para as 60 do anexo ele virou o horário da rejeição (51, lote das 10h49) ou o do recebimento do 2º pacote (9, lote de 06/10). Para as outras 67 rejeitadas (todas no lote de 06/10 12h58), não mudou. O tribunal não explica por que o repositório atualiza o `hr` em umas e não em outras, e essa pergunta só o TSE responde.
5. **Item 4 (hash do BU) segue sem resposta:** o TRE-PE não guarda BUs e remete ao TSE. A frase de que a rejeição "prova que o conteúdo era idêntico" **não é prova**: a regra é rejeitar a retransmissão de seção já recebida; só a comparação de hashes mostra identidade. Nada nos anexos traz hash.
6. **Sem ata nem relatório** sobre a operação (o tribunal diz que não é exigido).

Dados informados: totalização de Governador e de Senador em PE em 04/10/2026 22:54:57 (horário local), comandada pelo TRE-PE; a de Presidente é do TSE. O TRE-PE faz só a logística e manda o restante para a Ouvidoria do TSE.

## Para o relatório (RELATORIO 7.2 / ANEXO / página)

- PE passa a ter explicação documentada para as 60 seções: BU original recebido em 04/10 antes de 22:54:57 (60/60); registro de 05/10 = retransmissão rejeitada ou recebida pelo Transportador Web; **sem troca de urna** (declaração do tribunal).
- Redação cuidadosa: "o `hr` público de 60 seções de PE corresponde à rejeição em lote (51) ou ao recebimento (9) de uma retransmissão, e não à chegada do BU original", e "o tribunal não explica por que 67 outras seções com a mesma rejeição mantêm o `hr` original".
- Manter a ressalva: o hash do BU ainda não foi confrontado; depende do TSE.

## Pendências

1. **Pedir ao TSE** (novo pedido ou complemento ao 81136107180936, que vence em 27/10): (a) cópia dos BUs originais e dos retransmitidos das 129 seções, ou os hashes de recebimento; (b) por que o `hr` do repositório foi atualizado em 60 seções e não em 67 outras com a mesma rejeição; (c) o que roda às 10h49 de 05/10 e às 12h58 de 06/10 (lotes de rejeição). Os dois ZIPs de correspondência indicados pelo tribunal (precisam de autorização do Jair para baixar): `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/correspesp/CESP_1t_PE_041020261259.zip` e `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/correspefet/CEFT_1t_PE_051020261049.zip`.
2. Repetir a mesma análise (SISTOT, rejeições por retransmissão, 2 lotes) nos demais tribunais, e conferir se o TRE-MA também teve lotes de rejeição.
3. Atualizar RELATORIO, ANEXO e a página com o resultado de PE; revisar a frase dos protocolos da matéria da Folha dos Vales.
4. Responder à pesquisa de satisfação do TRE-PE é opcional (decisão do Jair).
