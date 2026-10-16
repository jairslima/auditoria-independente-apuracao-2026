# Análise da resposta do TRE-MA (Protocolo 81179908112145), recebida em 16/10/2026

Resposta do TRE-MA (COUSE) enviada em 15/10/2026 17h22 e entregue pela Ouvidoria em 16/10/2026 08h19. Arquivos originais em `respostas/TRE-MA_2026-10-16/` (pasta ignorada pelo git: contém identificadores de operadores e e-mails de servidores). Esta análise não reproduz dados pessoais.

## O que o tribunal respondeu

1. As planilhas SISTOT (Cajari e Viana) mostram geração do arquivo na urna, leitura da mídia, forma de transmissão e recebimento no TSE; as planilhas de "BUs rejeitados por retransmissão" mostram os reenvios.
2. A retransmissão equivocada pela Junta gerou os registros das 01h56; houve problema de logística no recolhimento de seis urnas e mídias de Cajari, com atraso significativo na chegada à Junta (20ª ZE, sede em Viana).
3. Segundo o BI do TSE do 1º turno, houve substituição da urna da 87ª seção de Viana (fora das 45 seções do pedido).
4. A assinatura do BU é gerada pelo hardware da urna e os arquivos e assinaturas estão no portal resultados.tse.jus.br (sem registro de hash do envio e da retransmissão).
5. Seis seções de Cajari foram transmitidas da sede da Junta em Viana; ao receber as mídias, o servidor do cartório também retransmitiu BUs de várias seções, rejeitados pelo TSE.

## O que os dados anexos confirmam (cruzamento com a lista das 45 seções)

- **39 das 45 seções** (34 de Viana + 5 de Cajari: 134, 136, 171, 219, 237) foram **recebidas pela primeira vez entre 17h57 e 20h56 de 04/10** e tiveram **novo envio entre 01h55:58 e 01h56:57 de 05/10, rejeitado** ("Erro por retransmissão de uma seção já recebida"). Primeiro envio e reenvio saíram da mesma máquina da Junta.
- **6 seções de Cajari** (138, 140, 141, 142, 155, 184): um único pacote cada. Arquivos gerados na urna entre 17h04 e 17h19 de 04/10 (a 142 às 22h00), **mídia lida entre 01h54 e 01h55 de 05/10**, transmissão em 8 segundos (01h56:01 a 01h56:09) e recebimento às 01h56. A ata da Junta registra falha de internet para a coleta nessas seis seções e transmissão na sede, o que concorda com a lista.
- Outras 8 seções de Cajari (130, 131, 148, 154, 176, 186, 208, 225) também tiveram a mídia lida depois das 21h de 04/10, mas foram recebidas antes das 23h41 e por isso não aparecem entre as 45.
- Cajari seção 213: rejeição por retransmissão às **18h47 de 04/10**, fora das 45 (não explicada).
- **Consequência para a auditoria:** o campo `hr` do repositório público (01h56 para as 45 seções) corresponde à **última tentativa de envio** nas 39 seções com retransmissão, não ao primeiro recebimento (17h57 a 20h56). Isso confirma que `hr` não serve como horário de chegada, e que o "atraso" das 39 era artefato do reenvio. Para as 6 seções de Cajari o 01h56 é, de fato, o primeiro e único recebimento.

## Lacunas (levadas à réplica, enviada em 16/10/2026)

- Onde estavam as seis urnas/mídias entre ~17h e 01h54 e quem as recolheu; documento de recebimento das mídias.
- A ata é de Cajari e não trata da retransmissão; falta relatório de ocorrência ou declaração do servidor sobre o reenvio de 39 seções.
- Rejeição da seção 213 às 18h47.
- Substituição de urna: a resposta cita a seção 87 de Viana (fora das 45); falta confirmar expressamente que nenhuma das 45 teve urna ou mídia substituída.
- Integridade: sem registro do hash do envio original e do rejeitado.
- Confirmar que o `hr` público reflete a última tentativa.

## Observações de método

- A ata (PDF digitalizado, 2 páginas, uma por eleição) foi lida por OCR (`Ata_..._texto_OCR.txt`); conferir contra o PDF antes de citar trechos.
- Scripts do cruzamento: `respostas/TRE-MA_2026-10-16/_analise/`.
