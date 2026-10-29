# Auditoria Independente da Apuração 2026 by Jair Lima: relatório do 2º turno (25/10/2026)

Versão de 28/10/2026. A versão para leitura, com a comparação entre os turnos em níveis (Brasil, região, estado e município), é o artefato: https://claude.ai/artifact/VYSyE8NrQjZowXKzyHsXDs. Dados e scripts: `AuditoriaPresidente2026_T2/` (scripts e resultados) e `AuditoriaPresidente2026/segundo_turno/dados_monitor/` (coleta ao vivo). Todas as verificações foram feitas nas 499.207 seções, sem amostragem.

## 1. Resultado em uma página

| Verificação | Resultado |
|---|---|
| Soma dos 499.207 boletins de urna (BU) contra o total oficial (gerado 25/10 às 23:27:02) | **Diferença zero**, no Brasil, nas 27 UFs e no exterior. Candidato 13: 64.256.232; candidato 22: 59.826.041 |
| Soma por município e posto | **5.757 de 5.757 iguais** ao oficial (5.571 municípios e 186 postos no exterior; 40 postos sem seção instalada valem zero) |
| Cadeia de hashes das tuplas de cada BU | **0 erros** (tupla, ordem e hash final) em 499.207 BUs |
| Assinatura digital (certificado e assinatura do hash final) | **499.178 de 499.178 válidas**, mais **29 de 29** do Sistema de Apuração, sem nenhuma falha |
| RDV (registro digital do voto) contra o BU da mesma seção | **499.206 de 499.206 iguais**, 539.816 comparações de cargo por seção, 0 divergências. Uma seção (CE zona 21 seção 136) não tem RDV publicado |
| Número da urna no log × no certificado | **499.177 iguais, 0 diferentes** (29 do Sistema de Apuração sem certificado de urna; 1 sem log) |
| Estabilidade do repositório (coletas de 26/10 e 27/10) | Nenhum hash de BU mudou nas 499.207 seções; o estado mudou em 8.753 |
| Divulgação oficial | **Parada por cerca de 1h54min** (17:08 a 19:02), em decorrência da liminar do STF que prorrogou a votação |
| Votos computados depois das 17h, nos logs de 499.206 seções | **34.810** em 30.086 seções (imprensa: 35.521); depois das 19h: 13 |

Totais oficiais finais: votos válidos 124.082.273; brancos 1.430.496; nulos 2.723.305. Candidato 13 (Lula) com 51,79% e candidato 22 (Flávio Bolsonaro) com 48,21% dos válidos.

**Leitura honesta:** os números dos BUs, as assinaturas e o RDV são consistentes entre si e com o total oficial. Isso é consistência, não prova de ausência de adulteração. O BU é saída da própria urna.

## 2. Comparação entre o 1º e o 2º turno

As 499.207 seções são as mesmas nos dois turnos. Do 1º para o 2º turno:

| | 1º turno | 2º turno | Diferença |
|---|---|---|---|
| Comparecimento | 125.275.835 | 128.236.074 | +2.960.239 |
| Lula (13) | 53.879.538 | 64.256.232 | +10.376.694 |
| Flávio Bolsonaro (22) | 56.104.503 | 59.826.041 | +3.721.538 |
| Brancos e nulos | 5.969.801 | 4.153.801 | −1.816.000 |
| Os outros 10 candidatos e os nulos técnicos (5.246) | 9.321.993 | não disputaram | |

Os dois candidatos ganharam votos. O ganho conjunto (14.098.232) é igual, sem resto, à soma de 9.321.993 votos dos outros candidatos do 1º turno, 1.816.000 votos a menos em brancos e nulos e 2.960.239 de aumento no comparecimento. A identidade vale em todas as seções, municípios, estados e no país (testada nos 5.717 municípios e postos). A identidade é aritmética: vale em toda seção cujo BU soma corretamente, e testá-la só confirma que os dados são internamente consistentes (0 violações nas 499.207 seções). Ela mede o tamanho de cada parcela, não o comportamento dos eleitores, e não diz quem trocou de candidato: o voto é secreto.

A estimativa de transferência por regressão ecológica (499.201 seções, aptos pelo cadastro de eleitores) é um indício estatístico. Sustenta que quem votou em Lula ou em Flávio no 1º turno ficou quase todo do mesmo lado (101% e 100% no país; o 101% é impossível e mostra o limite do método), e que os eleitores de Cury foram mais para o Lula (58% contra 29% no país; nos 23 estados em que os eleitores de Cury somam mais de 20 mil, o Lula fica à frente em todos, de 43% a 83% contra 21% a 45%). Não sustenta as estimativas de brancos e nulos e de abstenção (a de brancos e nulos para o Lula varia de 39% a 91% entre os 23 estados com mais de 20 mil eleitores desse grupo; vários coeficientes saem fora de 0% a 100%). O artefato traz a matriz por nível, com intervalos e a faixa entre estados.

## 3. Método (o mesmo do 1º turno, com as constantes do 2º)

Eleição de Presidente 6258, pleito de urnas 3221. Coleta do índice e do `aux.json` de cada seção (duas vezes), download dos BUs, decodificação do formato 2026 em ASN.1, soma por seção e comparação com o total oficial e com o arquivo oficial de cada município, verificação da cadeia de hashes, verificação das assinaturas contra as chaves raiz do TSE, comparação do RDV com o BU, leitura dos logs das urnas e comparação seção a seção com o 1º turno.

## 4. A suspensão da totalização e do recebimento (17h06 a 19h)

### 4.1 O que o TSE e o STF informaram (fontes públicas de 25/10/2026)

- O ministro Cristiano Zanin, do STF, determinou "prorrogação por até duas horas, até às 19h, horário de Brasília, do encerramento do recebimento dos votos em todas as seções do Brasil", cabendo ao TSE dar cumprimento. Pedido da campanha de Lula (falta de transporte), com pedido semelhante da campanha de Flávio Bolsonaro em 17 municípios. Depois, esclareceu que valia para as seções ainda abertas. O fato chegou ao STF às 16:23:49 (Agência Brasil) ou 16h32 (TV Senado); a Agência Câmara fala em cerca de 15h30.
- "A contagem dos votos foi suspensa às 17h06, com 1.225 das 499.248 seções apuradas", com retomada anunciada para as 19h.
- O Presidente do TSE declarou que a prorrogação exigiu "o bloqueio temporário do recebimento dos boletins de urna", que isso "gerou uma contenção extraordinária nos boletins de urna", que "não sabíamos, ao certo, se teríamos armazenamento" e que a prorrogação "não comprometeu a apuração". Informou 0,31% de urnas substituídas.
- Levantamento da imprensa com logs das urnas: 35.521 votos para Presidente depois das 17h.

Fontes: Agência Brasil (`agenciabrasil.ebc.com.br/justica/noticia/2026-10/zanin-manda-ampliar-horario-de-votacao-ate-19h` e `.../politica/noticia/2026-10/tse-diz-que-contagem-dos-votos-sera-retomada-19h`), Agência Câmara (`camara.leg.br/noticias/1313728-...`), Rádio Senado (`www12.senado.leg.br/radio/1/noticia/2026/10/25/...`), Gazeta do Povo. As páginas do `tse.jus.br` retornaram erro 403 e não foram lidas.

### 4.2 O que a coleta própria mostra

- A curva oficial para em **1.225 seções (0,25%)**, geração às 17:06:31, em todas as 153 consultas de 20:07:57Z a 22:00:12Z (17:08 a 19:00 de Brasília), sem intervalo maior que 2 minutos entre consultas, então a ausência de mudança não é falha de coleta. Às 19:02:13 apareceu um arquivo gerado às 17:07:01 com 1.456 seções; o gerado às 19:03:36 (1.909 seções) foi visto às 19:04:53 e o gerado às 19:05:16 (7.560 seções, 1,51%), às 19:06:12.
- Nenhuma seção tem, no campo `hr` do repositório, horário entre ~17:10 e 19:00 (faixa de 17h: 1.895; de 17h10 a 18h50: **zero**; a partir de 19h: 6.124 na primeira faixa). O índice também não ganhou nenhuma seção nova de 20:20Z a 22:10Z. Isso é compatível com o **bloqueio do recebimento** declarado pelo TSE. O padrão também seria compatível com recebimento oculto, e os dados não distinguem os dois (ver 4.4).
- 264 seções com `hr` de 17:07 e 17:08 só apareceram no índice às 19:11 e 19:12 (atraso de 7.397 a 7.523 s).
- O tempo normal entre o `hr` e a primeira vez que o monitor viu a seção é de mediana 403 s (p90 568 s, p99 708 s).
- 965 seções foram vistas publicadas antes do `hr` que consta hoje; em 187 delas (PE 124, PA 51, AM 12) o `hr` atual é de 26/10 de manhã.
- No 1º turno, o conjunto de dados abertos "Detalhe da apuração por seção eleitoral" do TSE trouxe o horário de recebimento de cada BU e mostrou que o horário de 05/10 de quase todas as seções do anexo era de reenvio, e que o recebimento real foi em 04/10. O arquivo baixado em 29/10 traz só o 1º turno. Quando o do 2º turno for publicado, ele permite testar a afirmação do bloqueio: se o horário de recebimento de algum BU estiver entre 17h06 e 19h, o TSE recebeu durante o bloqueio; se todos forem de 19h em diante, o bloqueio se confirma pela fonte oficial.

### 4.3 O que os logs de todas as urnas mostram (499.206 de 499.207 seções)

- BU gerado antes de 17:06:31: 390.455 (78,2%); entre 17:06:31 e 19:00: 101.863 (20,4%); depois das 19:00: 6.859 (1,4%). As 29 seções do Sistema de Apuração não geram BU na urna.
- Votos computados depois das 17h (Brasília): 34.810 em 30.086 seções; depois das 17h06: 4.870 em 3.347; depois das 19h: 13 em 12. A imprensa informa 35.521; a diferença de 711 não foi explicada. Parte dos votos depois das 17h é de eleitores que já estavam na fila às 17h, que a lei já permitia votar sem prorrogação; os logs não separam as duas origens.
- Os eventos "voto computado" dos logs somam 128.235.225, 99,9993% do comparecimento (128.236.074). Os 849 votos sem evento se explicam: 831 nas 27 seções do Sistema de Apuração (BU digitado, sem voto registrado na urna), 54 em seis seções com 1 a 36 votos a menos no log, 268 na seção sem log publicado (SP zona 395 seção 298), menos 304 de uma seção (ES zona 9 seção 85) em que o zip do log traz também o log de outra urna, com 304 votos. Para chegar a esse resultado foi preciso ler os dois arquivos do zip do log de 1.462 seções, o log da mídia externa e o logd.dat, porque a urna foi trocada ou reiniciada durante a votação. Os números de votos depois das 17h vêm desses eventos e não mudaram com a leitura completa.
- **Trocas de urna nos logs:** em 1.432 seções (0,287%) o log do dia traz duas ou três urnas diferentes. Em 1.417 delas mais de uma urna registrou votos (a primeira registrou parte e a substituta o resto); em 15, uma segunda urna só gerou o resultado. Nas 1.435 seções em que os votos estavam divididos, a urna que gerou o `bu.dat` é a do certificado em todas (1.435 de 1.435), e a soma dos votos das urnas confere com o comparecimento do BU em 1.428; as sete exceções são seis seções com 1 a 36 votos a menos no log e a seção do ES. O presidente do TSE informou 0,31% de urnas substituídas (cerca de 1.548); os logs mostram 0,287% (1.432). A diferença pode ser de trocas antes do primeiro voto, que não dividem os votos entre urnas; isso não foi procurado.
- A diferença entre o `hr` do TSE e a geração do BU na urna tem mediana de 2h27 a 3h51 em todas as UFs, sem UF fora do padrão (exterior fora desta comparação, por causa dos fusos).
- Sensibilidade ao fuso: se o fuso do Acre estivesse errado em 1 hora, a fração de BUs gerados entre 17h06 e 19h iria de 20,4% a 20,8%; se o dos estados de UTC-4 (AM, RO, RR, MT e MS) estivesse errado em 1 hora, iria de 19,2% a 25,1%. A conversão usada se confirma pelo atraso mediano desses estados, que fica na faixa dos demais (AC 2h51, AM 2h41, RO 3h03, RR 3h18, MT 3h00, MS 2h50, contra 2h27 a 3h51 no país); um erro de 1 hora os deslocaria para fora da faixa. Sem o exterior, a fração é de 20,3%.
- BU gerado depois das 19h está concentrado em RJ (3.043), SP (1.697), BA (980), PE (704) e PB (312), 6.736 dos 6.859.
- Comparação das mensagens do log entre as seções atrasadas e as demais: diferenças acima de 10 pontos percentuais em 9 tipos de mensagem nas 264 atrasadas (configuração da urna) e em 53 nas 965 vistas antes do `hr` (habilitação do eleitor, bateria interna ausente, conferência de dado digitado), nenhuma de erro de geração do BU, de transmissão ou de leitura de mídia; compatíveis com a composição do grupo (73% do exterior). Não verifiquei essa explicação seção por seção.
- Sistema de Apuração (29 seções do exterior): 22 combinam apuração eletrônica e digitação de BU do exterior, 7 foram só digitação, 27 tiveram a apuração cancelada e refeita ao menos uma vez; apenas Presidente.

### 4.4 O que continua sem resposta

- O monitor e os logs não distinguem "o TSE bloqueou o recebimento" de "o TSE recebeu e guardou sem publicar". O `hr` público é o horário da última tentativa de envio. O log da urna não registra transmissão.
- Entre as coletas de 26/10 e 27/10, nenhum hash de BU mudou; o estado e o arquivo `imgbu` mudaram em 8.753 seções (6.604 em SP): 7.017 passaram de "Recebida" para "Totalizada" e 1.736 de "Totalizada" para "Recebida". É compatível com o estado seguindo o último pacote recebido, inclusive reenvios.
- Onde os BUs gerados entre 17h06 e 19h ficaram retidos (na urna, em fila ou em armazenamento do TSE ou do TRE), quem tinha acesso e o registro do bloqueio e do desbloqueio: só o TSE responde. Pedido de acesso à informação enviado ao TSE em 26/10/2026 às 20:24 UTC, com complemento em 27/10/2026; prazo de 20 dias (15/11/2026) e de 30 dias (25/11/2026); aguardando protocolo e resposta.

## 5. O que NÃO está verificado

- Duas seções ficaram fora de parte das conferências por falta de arquivo publicado: CE zona 21 seção 136 (sem RDV) e SP zona 395 seção 298 (sem log). Em ES zona 9 seção 85, o zip do log traz também o log de outra urna (304 votos), a esclarecer com o tribunal.
- A diferença de 711 votos entre os logs (34.810) e o número da imprensa (35.521) não foi explicada.
- Os fusos de Fernando de Noronha e do exterior não foram tratados nas análises de log.
- A estimativa de transferência de votos entre os turnos é um indício estatístico; seus coeficientes de brancos, nulos e abstenção não são confiáveis.
- Nada neste relatório prova que cada voto foi gravado fielmente: os testes mostram consistência entre arquivos que a própria urna produz. O voto é secreto, e a comparação entre turnos descreve variações por seção, não decisões de eleitores.

## 6. Assinatura

Auditoria feita por Jair da Silva Lima, jornalista profissional (MTE 0024314/RS), pós-graduado em Investigação Forense e Perícia Criminal, formação em TI (IFC Redes, Governança de TI, Google for Education, curso Cisco CCNA Exploration). Não é perito registrado, e este relatório não é perícia judicial.
