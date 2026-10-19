# Análise da resposta do TRE-SP (Protocolo 81243408181658), recebida em 19/10/2026

Resposta da Secretaria de Tecnologia da Informação do TRE-SP e do cartório da 388ª Zona Eleitoral (Carapicuíba), recebida em 19/10/2026 às 16h53 (Gmail `1a155baa197de34f`) com a planilha `ZE_388 - recorte seções - 20261013.xls` (12 linhas, uma por seção). Originais em `respostas/TRE-SP_2026-10-19/` (ignorada pelo git). A análise não reproduz dados pessoais.

## O que o tribunal diz

1. A planilha traz, por seção: encerramento da urna, geração, transmissão e recebimento.
2. Encerramento das urnas por volta das 17h30, transmissão na Zona por volta das 21h, via Transportador Desktop, tudo por leitura de mídia de resultado, intervalo médio de 3h30.
3. Substituição de urna: remetida à Zona. O cartório diz que não houve substituição.
4. Os resumos de correspondência esperados são iguais aos efetivados no TSE.
5. "Recebido" é o horário de recebimento no TSE. O atraso: remetido à Zona.
6. Cartório: os mesários não finalizaram as urnas "em sua plenitude"; foi preciso fazer RED no cartório quando as urnas chegaram (4 caminhões, escolas distantes), "procedimento normal".

## Conferência com os dados da auditoria

- **Recebimento da planilha x `hr` público.** As 12 seções batem ao minuto (planilha 20h59 a 21h14; `hr` do aux 20h59:04 a 21h14:06). Para estas seções o `hr` público é o horário real de recebimento no TSE (não é reenvio, como no Maranhão).
- **Transmissão x recebimento.** Transmissão entre 20h52 e 21h14. Em 6 seções (148, 155, 181, 299, 371, 419) o recebimento é praticamente instantâneo; nas outras 6 (147, 254, 300, 360, 413, 554) há 7 a 8 minutos entre transmissão e recebimento.
- **Correspondência.** Nas 12, os 6 últimos dígitos da "Correspondência Esperada" são iguais ao "Resumo da Correspondência Efetivada" (12 de 12). Cuidado: é um código curto de 6 dígitos (a planilha chama de resumo), não o SHA-256 do arquivo do BU. Prova coerência do código de correspondência, não do hash do arquivo. O arquivo listado é `...-imgbu.dat` (imagem do BU).
- **Encerramento e geração.** Encerramento da urna entre 17h06 e 17h41 e geração do arquivo 2 a 9 minutos depois (17h08 a 17h47), ou seja, as urnas encerraram e geraram o resultado cedo; o atraso é entre a geração e a transmissão (de 3h05 a 3h56 pela coluna "Geração até Transmissão", média de cerca de 3h37).

## Ponto que não fecha

- O cartório diz que os mesários não finalizaram as urnas e que foi preciso RED no cartório. Mas (a) a planilha registra encerramento da urna e geração do arquivo às 17h, na hora normal; e (b) no BU público as 12 seções são urna do tipo 1 (urna de votação), sem histórico de urna anterior (`n_historico` 0). Nas urnas RED a auditoria encontrou o tipo 2 (50 casos no país). Logo, o BU não tem a marca de RED. Isto não prova que o cartório está errado (o RED pode ter sido feito antes de gerar o BU ou a marca pode não aparecer nesse tipo de arquivo), mas a explicação e os dados não se encaixam sem uma pergunta de esclarecimento.
- Mesmo assim, a causa do atraso (mídias e urnas chegando tarde ao cartório, transmissão em lote por volta das 21h) é compatível com os horários.
- Itens 3 e 5 do pedido ficaram respondidos só pelo cartório, não pela STI.

## Conclusão para a auditoria

Para as 12 seções de Carapicuíba, o `hr` público (20h59 a 21h14) é o horário real de recebimento, o resultado só foi transmitido às 21h por leitura de mídia na Zona, sem sinal de reenvio. Não altera nenhum total. Fica em aberto a coerência entre "RED" e o tipo 1 do BU.

## Perguntas de esclarecimento possíveis ao TRE-SP

1. Se foi feito RED nessas 12 seções, por que o BU é do tipo urna de votação (tipo 1) e a planilha mostra encerramento e geração às 17h?
2. Qual é o relatório do RED (hora, urna original) e o "código de correspondência" (6 dígitos) tem relação com o hash SHA-256 do BU?
