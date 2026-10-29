# Respostas recebidas em 27/10/2026: TRE-SP (zona 388, Carapicuíba) e TRE-PA

Origem: e-mails automáticos "Resposta de Protocolo" de `naoresponda-sac-tre-sp@tse.jus.br` (27/10 às 15:37 UTC, Gmail `1a17e0295eeb0343`) e `naoresponda-sac-tre-pa@tse.jus.br` (27/10 às 13:56 UTC, `1a17da6cad6dd946`), mais o e-mail da Ouvidoria do TRE-PA de 27/10 às 14:08 UTC (`1a17db143196a762`). Os anexos não podem ser baixados pelo conector do Gmail e **não foram lidos**.

## TRE-SP, zona 388 (12 seções de Carapicuíba)

Fatos informados (texto do e-mail):
1. Foi feito **RED** (recuperação de dados da urna) em 11 das 12 seções, porque os mesários não encerraram as urnas. A seção 254 foi encerrada normalmente com a mídia original.
2. Horários do RED informados: seção 147 às 20h20; 148 às 20h59; 155 às 20h43; 181 às 20h50; 299 às 21h12; 300 às 20h50; 360 às 20h37; 371 às 20h50; 413 às 20h36; 419 às 20h54; 554 às 20h32.
3. O boletim publicado não traz a marca de RED porque o log da urna só tem os registros até a gravação na mídia interna, antes da cópia para a Mídia de Resultado; o RED foi usado só para regerar os resultados em nova mídia. O uso pode ser visto pelo VPP na urna ou no log depois do 2º turno.
4. As urnas chegam ao cartório depois das mídias (escolas distantes, quatro caminhões), e o RED das 12 urnas demora mais. O cartório diz ser procedimento normal em todas as eleições.
5. O "código de correspondência" de 6 dígitos **não é** um resumo criptográfico: é a associação entre a seção e a urna preparada para ela (Res.-TSE 23.673/2021). Os resumos SHA-512 dos arquivos estão no arquivo `-vota.vsc` publicado pelo TSE, e o BU (`-bu.dat`) confere com o resumo ali registrado (exemplo dado: seção 147).
6. Não houve substituição de urna nem de cartão de memória nas 12 seções.
7. Anexos: atas da mesa receptora das seções e a planilha de correspondência (`ZE_388 - recorte seções`, a mesma de 19/10).

Cruzamento com os dados do 1º turno (feito em 29/10/2026, `votos_secao.csv`):

| Seção | RED informado | `hr` do TSE (04/10) | `hr` menos RED |
|---|---|---|---|
| 147 | 20:20 | 20:59:04 | 39 min |
| 148 | 20:59 | 21:04:25 | 5 min |
| 155 | 20:43 | 21:04:27 | 21 min |
| 181 | 20:50 | 21:04:27 | 14 min |
| 299 | 21:12 | 21:14:06 | 2 min |
| 300 | 20:50 | 21:00:07 | 10 min |
| 360 | 20:37 | 20:59:04 | 22 min |
| 371 | 20:50 | 21:04:28 | 14 min |
| 413 | 20:36 | 21:00:07 | 24 min |
| 419 | 20:54 | 21:04:29 | 10 min |
| 554 | 20:32 | 20:59:04 | 27 min |

Nas 11 seções, o `hr` do TSE vem de 2 a 39 minutos depois do horário do RED informado, o que é coerente com a explicação do cartório. A seção 254, sem RED, tem `hr` de 21:00:08. O campo `ts_bu` do BU publicado traz 17:07 a 17:43, cerca de três horas antes do RED; isso não contradiz o cartório (o RED regera o resultado a partir da mídia interna gravada no encerramento), mas não é verificável sem o log da urna.

O que muda no relatório do 1º turno (ANEXO, seção de Carapicuíba): a hipótese de atraso por processamento da zona passa a ter explicação do tribunal (RED por urnas não encerradas pelos mesários), parcialmente conferida pelos horários. Falta ver as atas anexas.

## TRE-PA, análise dos anexos (feita em 29/10/2026)

Arquivos em `pedidos_lai/respostas/TRE-PA_2026-10-27/` (fora do git): Informação nº 30/2026 (SVE), Despacho nº 3186741 (STI), relatório de ocorrências do SISTOT e logs do Transportador (2.343 logs de estação, 13,9 MB).

- **Resposta do tribunal (Informação nº 30/2026, processo SEI 0011165-96.2026.6.14.8000).** Os horários de recebimento constam do relatório "Detalhe da apuração por seção eleitoral" dos dados abertos do TSE (exemplo: Afuá seção 07, recebida em 04/10 às 18:27:55). O último BU recebido da 97ª zona (Belém) chegou em 04/10 às 20:00:07, e a totalização final foi às 20:09:30. Os dados do pedido ("registro_hr_no_repositorio_TSE") "não são confirmados" por esse relatório. Os itens 5 e 6 foram devolvidos para esclarecimento, e o despacho pede que a ouvidoria procure o requerente sobre os itens 2, 5 e 6.
- **Conferência no arquivo do TSE** (`detalhe_votacao_secao_2026.zip`, 234 MB, atualizado em 26/10; só 1º turno): as 621 seções do Pará foram recebidas em 04/10; as 354 de Belém, entre 17:11:07 e 20:00:07, com primeira totalização parcial entre 17:20:27 e 20:09:30. O tribunal está certo. Tabela por seção do anexo: `resultados/detalhe_recebimento_anexo_tse.csv`.
- **Logs do Transportador.** As 354 seções da zona 97 foram lidas e enviadas de novo em 05/10 (13:41 a 14:19), com diferença mediana de 0,3 minuto para o `hr` público de cada seção (todas dentro de 5 minutos). Das 621, 361 aparecem com pacote enviado nesses logs; as outras 260 (Capanema zona 25, Oeiras do Pará zona 45, Gurupá zona 26 e outras) não aparecem, o que sugere outro meio de transmissão (os logs do Sistema JEC, citados na resposta, não vieram no arquivo).
- **Relatório de ocorrências.** 101 seções do estado: 95 trocas de urna (0,46% das 20.827) e 6 BUs gerados por RED em urna de seção. Só 3 das 621 seções do anexo estão nele e nenhuma por RED: a troca de urna não explica os horários de 05/10.
- **Conclusão.** O campo `hr` público é o da última tentativa de envio, como já mostravam o Maranhão e Pernambuco. Para as seções do anexo com horário no arquivo do TSE (813 de 842; as 29 do exterior não têm linha), 798 foram recebidas em 04/10; 15 chegaram depois (13 em 05/10 entre 00:11 e 01:56, e 2 do Amazonas que o arquivo mostra em 25/10, provavelmente sobrescritas pelo 2º turno).
- **Pendente.** Rascunho de resposta ao tribunal (esclarecimento dos itens 2, 5 e 6, com pedido do motivo do reenvio da zona 97, das rejeições e dos logs do Sistema JEC) criado no Gmail, não enviado. Prazo de recurso: 06/11/2026.
