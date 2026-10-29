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

## TRE-PA (621 seções de Belém e outras)

- Resposta recebida com três arquivos SEI (processo 0011165-96.2026.6.14.8000: resposta, ocorrências e despacho) e, em e-mail separado, o **log do Transportador** do Pará (zip de 2,8 MB, `arquivoPleito3220UFPATransportador_log`).
- O texto do e-mail não traz fatos novos. O tribunal informa que parte dos dados foi enviada por e-mail separado por causa do volume e que, se as respostas das unidades técnicas não estiverem claras ou tiverem omissões, cabe **recurso** para pedir complemento.
- **Pendente:** baixar os quatro arquivos e analisá-los (os 354 de Belém zona 97 com registro de 05/10, e os demais do Pará). O prazo para recurso é de 10 dias a partir da resposta (27/10), ou seja, até 06/11/2026.
