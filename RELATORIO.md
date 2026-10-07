# Auditoria Independente da Apuração 2026 by Jair Lima

1º turno, 4 de outubro de 2026. Presidente e eleição estadual. Autor: Jair Lima (jairslima@gmail.com).

Data da coleta: 05 e 06/10/2026. Fonte única: dados públicos do TSE (`resultados.tse.jus.br`) e documentação técnica do TSE.
Escopo: Presidente (eleição 6257) e eleição estadual (6259: Governador, Senador, Deputado Federal e Estadual ou Distrital), pleito de arquivos de urna 3220.

## 1. Pergunta

Os dados públicos do TSE permitem refazer, urna a urna, a soma dos votos de Presidente no 1º turno e compará-la com o resultado oficial? Houve alteração de números associada ao "apagão" do painel de apuração (das 19h06min33s até ~20h08, segundo a imprensa: mais de uma hora)?

## 2. Respostas curtas

1. **Sim, os dados bastam.** Os boletins de urna (BU), com a assinatura digital da urna, são públicos por seção.
2. **A soma dos BUs reproduz o oficial ao voto, zero a zero.** Os 499.207 BUs somam exatamente o total oficial em todos os candidatos, nos brancos, nos nulos, nos votos válidos (119.300.788) e nas 28 abrangências (27 UFs e exterior). Uma diferença inicial (Flávio 1.757, Lula 1.746) vinha de 15 seções cujos arquivos o TSE ainda não tinha publicado; elas foram publicadas entre 05 e 06/10 e, incluídas, fecharam a conta exatamente.
3. **O RDV, o registro voto a voto da mesma urna, bate com o BU** em todas as 20.811 seções da amostra (103.855 comparações de cargo por seção), incluindo todas as seções que atrasaram (seção 6.1).
4. **Nenhum BU lido apresentou sinal de adulteração**: a cadeia de hashes das 67,86 milhões de linhas de votos fecha em todos os 499.207 BUs, e as assinaturas ECDSA/EdDSA do hash final de Presidente são **válidas nas 499.176 seções com BU de urna** (ver seção 6).
5. **O apagão não deixa descontinuidade nos números.** Os três estados do painel exibidos pela TV Senado (antes, durante e depois do apagão) são reproduzidos pelos BUs com erro menor que 0,005 ponto percentual.
6. **Flávio Bolsonaro nunca esteve acima de 50% dos votos válidos no estado congelado do painel.** Ele esteve acima de 50% mais cedo na noite (pico de 51,3% às 17h58) porque as primeiras seções a chegar vieram de regiões mais favoráveis a ele. O percentual desceu de forma contínua até 47,03%.

## 3. Dados e método

Todos os caminhos abaixo são sob `https://resultados.tse.jus.br/oficial/ele2026/`.

| Item | Caminho / observação |
|---|---|
| Totais oficiais de Presidente | `6257/dados/<uf>/<uf>-c0001-e006257-u.jws` (JWT, o conteúdo é JSON) |
| Índice de seções por UF | `arquivo-urna/3220/config/<uf>/<uf>-p003220-cs.json` |
| Arquivos por seção | `arquivo-urna/3220/dados/<uf>/<mun>/<zona>/<seção>/p003220-...-aux.json`, que lista `bu.dat`, `rdv.dat`, `log.jez`, `vota.vsc` |

Etapas (scripts em `scripts/`, todos reexecutáveis):

1. **Congelamento** dos totais oficiais e dos índices, com SHA-256 e hora UTC (`fase1_congelar.py`, `dados/manifesto_fase1.jsonl`).
2. **Coleta** dos `aux.json` (499.207 seções instaladas) e dos BUs (499.161 `.bu`, 31 de contingência `.busa` e 15 publicados pelo TSE só em 06/10; total 499.207). O TSE aplica limite de requisições (HTTP 429): usar até 10 conexões.
3. **Leitura dos BUs** por dois decodificadores independentes: um parser BER próprio (`bu_parser.py`) e o decodificador `asn1tools` com a especificação ASN.1 oficial de 2026 (`bu_cadeia.py`). Concordam em 499.161 de 499.161 seções comparadas.
4. **Soma** seção a seção → município → UF → Brasil e **comparação** com o oficial (`fase4_compara.py`).
5. **Integridade criptográfica** (seção 6).
6. **Painel de TV**: transmissão da TV Senado (gravação baixada), leitura por OCR e conferência visual do painel de Presidente, e comparação com os BUs ordenados pela hora de recebimento (`video_ocr.py`, `fase7_painel_video.py`).

Fatos de método que não são óbvios:

- **A hora de chegada de cada BU é o campo `hr` do `aux.json`.** O campo `da/ha` do índice `-cs.json` não é hora de chegada (só 812 seções "chegariam" até 19h06).
- O índice lista 517.179 seções: 499.207 instaladas (com BU, número idêntico às seções instaladas do total oficial), 17.931 agregadas a outra seção (campo `nsp`) e 41 sem dados e sem seção principal, que são as não instaladas (todas no exterior; ver 4.3).
- Em urna de contingência, o hash inicial usa a identificação da seção real (`identificacaoSecao`), e não a da urna (validado em 60 de 60 casos antes de aplicar).

## 4. Soma dos BUs contra o oficial

Total oficial (arquivo gerado em 05/10/2026 12h51): votos válidos 119.300.788.

| Candidato | Soma dos BUs | Oficial | Diferença |
|---|---:|---:|---:|
| Flávio Bolsonaro (22) | 56.104.503 | 56.104.503 | 0 |
| Lula (13) | 53.879.538 | 53.879.538 | 0 |
| Augusto Cury (70) | 3.448.569 | 3.448.569 | 0 |
| Renan Santos (14) | 2.675.887 | 2.675.887 | 0 |
| Ronaldo Caiado (55) | 2.605.148 | 2.605.148 | 0 |
| Zema (30) | 326.488 | 326.488 | 0 |
| Demais (16, 21, 27, 29, 35, 80) | 260.660 | 260.660 | 0 |
| Brancos | 2.300.798 | 2.300.798 | 0 |
| Nulos | 3.669.003 | 3.669.003 | 0 |

- **Primeira rodada (antes das 15 seções):** os BUs estavam abaixo do oficial em Flávio 1.757, Lula 1.746, Cury 161, Renan 149, Caiado 90, Zema 23, demais 6, brancos 105, nulos 162, todas as diferenças concentradas em Betim/MG (zona 319, 3 seções) e Carapicuíba/SP (zona 388, 12 seções), cujos arquivos davam HTTP 404 até 05/10. Em 06/10 os 15 arquivos estavam publicados; baixados e incluídos, as 15 seções carregam exatamente aquelas diferenças (por exemplo Flávio 1.757 e Lula 1.746) e a cadeia de hashes delas fecha sem erro. A imprensa não publicou explicação para o atraso na publicação dos arquivos dessas seções (busca em 06/10).
- **Os lotes de seções que só apareceram depois (histórico do meu download).** Na primeira passada (05/10), 68 seções deram HTTP 404; elas pertencem a 5 zonas eleitorais. Todas tiveram o BU registrado como recebido (campo `hr`) em 04/10 entre 20h07 e 21h15, ou seja, na onda de recebimento logo após a retomada do painel, e todas constam como "Totalizado". O que atrasou foi a **publicação dos arquivos**, não o recebimento.

| Zona | Seções | BU recebido (04/10) | Arquivos disponíveis a partir de |
|---|---:|---|---|
| Betim/MG, zona 316 | 30 | 20h08 a 20h59 | 1ª repetição (05/10) |
| MG, município 53716, zona 269 | 18 | 20h44 a 21h15 | 1ª repetição (05/10) |
| Uberlândia/MG, zona 279 | 5 | 20h52 a 20h55 | 2ª repetição (05/10, noite) |
| Betim/MG, zona 319 | 3 | 20h07 a 20h10 | 3ª repetição (06/10) |
| Carapicuíba/SP, zona 388 | 12 | 20h59 a 21h14 | 3ª repetição (06/10) |

- Atenção a um erro que cometi e corrijo aqui: o horário que o índice `-cs.json` mostra para essas seções (Betim 00h52 de 05/10, Carapicuíba 23h00 de 04/10) **não é horário de chegada**; é o carimbo de publicação do índice. Escrever que elas foram "as últimas a chegar" estava errado.
- Além disso, 12.296 respostas HTTP 429 (limite de requisições) na primeira passada foram do meu cliente, e foram repetidas até concluir; não são falta de arquivo no TSE.
- O candidato nº 28 tem 5.246 votos nos BUs e não consta na lista oficial de candidatos; o TSE contabiliza exatamente 5.246 "nulos técnicos". Bate ao voto, e esses votos ficam fora dos válidos.
- Percentual de Flávio nos válidos: 47,03% (47,0278%); Lula 45,16% (45,1628%). Margem Flávio menos Lula: 2.224.965, igual ao oficial.
- Para vencer no 1º turno, Flávio precisaria de 3.545.892 votos a mais sem alterar o total de válidos.

### 4.1 Teste de controle: Governador e Senador do RS (eleição estadual 6259)

Para validar o método em um caso sem seções faltando, somei nos BUs do RS os votos de Governador e Senador (`fase10_rs_estadual.py`) e comparei com `rs-c0003-e006259-u.jws` e `rs-c0005-e006259-u.jws`. Foram lidos 27.547 BUs, igual às 27.547 seções totalizadas do oficial.

| Cargo | Candidatos comparados | Brancos | Nulos | Resultado |
|---|---:|---:|---:|---|
| Governador | 7 (Zucco 3.516.048; Juliana Brizola 1.917.374; Gabriel Souza 510.698; demais) | 324.123 | 315.858 | diferença 0 em todos |
| Senador | 13 (Sanderson 3.453.316; Marcel van Hattem 3.449.053; Manuela d'Ávila 1.957.697; Pimenta 1.870.301; demais) | 1.089.553 | 837.203 | diferença 0 em todos |

Nenhum votável nos BUs ficou fora da lista oficial. Isso mostra que o método e os decodificadores reproduzem o oficial voto a voto quando todas as seções estão publicadas. Limite: a assinatura do hash final foi verificada para a eleição 6257 (Presidente); para a 6259 a cadeia de hashes foi verificada, mas não a assinatura.

### 4.2 Teste em UFs e cargos sorteados (eleição estadual, fora do RS)

Sorteio com semente fixa 2026 (`scripts/fase11_aleatorio.py`, `dados/aleatorio_sorteio.json`, resultado em `dados/aleatorio_resultado.json`): AM, MT, PE, SP, RO, TO, ES e PI, com 2 cargos aleatórios cada, num total de 16 pares UF/cargo (Governador, Senador, Deputado Federal e Estadual). Em **todos os 16 pares, 100% dos candidatos, brancos e nulos batem ao voto** com o oficial (por exemplo, SP Governador: Tarcísio 14.491.874 e Haddad 8.423.656; PE Governador: Raquel Lyra 2.805.438 e João Campos 2.360.469).

Em 3 pares o **total de votos de legenda** difere (BUs maior que o oficial): PE Deputado Estadual +746, SP Deputado Federal +1.173 e PI Deputado Federal +634. Os três estão explicados **exatamente** por um campo do próprio arquivo oficial: PE +746 é o MOBILIZA com situação "Anulado sub judice" (`tval` = 746); PI +634 é a soma de 456 + 119 + 37 + 22 de quatro partidos nessa situação (MOBILIZA, DEMOCRATA, DC, PCO); e SP Deputado Federal +1.173 são votos de legenda do PCO, partido sem lista no estado, que o TSE contabiliza nos "nulos técnicos" (5.737 votos nominais fora da lista + 1.173 = 6.910, igual ao `vnt` oficial). É classificação do TSE, não voto perdido.

### 4.2.1 Auditoria completa de Minas Gerais e São Paulo (UFs com arquivos publicados com atraso)

Como MG e SP concentraram os arquivos que demoraram a aparecer (56 e 12 seções, ver `ANEXO_ATRASOS.md`), auditei as duas UFs inteiras (`scripts/fase15_mg_sp.py`, `dados/fase15.log`, `dados/mg_sp_resultado.json`): 52.062 BUs de MG (incluindo as 2 do Sistema de Apuração) e 103.656 de SP.

| Nível | MG | SP |
|---|---|---|
| Governador, candidatos iguais ao oficial | 11 de 11 | 5 de 5 |
| Senador | 16 de 16 | 13 de 13 |
| Deputado Federal | 710 de 710 | 1.045 de 1.045 |
| Deputado Estadual | 944 de 944 | 1.346 de 1.346 |
| Brancos e nulos (4 cargos) | iguais | iguais |
| **Municípios, Presidente e Governador (candidatos, brancos, nulos)** | **853 de 853** | **645 de 645** |

- Entre eles estão os municípios das zonas que atrasaram: **Betim, Uberlândia, Teófilo Otoni e Carapicuíba**, todos iguais ao oficial.
- A única diferença é o total de **legenda** do **PCO** (MG +457 federal e +437 estadual; SP +1.173 federal e +1.178 estadual). Em MG Dep. Federal e Estadual e em SP Dep. Estadual o PCO consta como "Anulado sub judice" com `tval` exatamente igual (457, 437 e 1.178); em SP Dep. Federal vale a explicação dos nulos técnicos acima. Todas as diferenças de legenda do teste estão explicadas.
- **Um erro meu, corrigido:** a primeira rodada deste passe não incluiu os 2 BUs do Sistema de Apuração de MG (arquivos `.busa`), e mostrou, por isso, diferenças em 2 municípios (41238 e 50075) e em vários candidatos. Incluídos, tudo bate. A rodada válida é a registrada em `dados/fase15.log`.

### 4.2.2 Conferência município a município, Brasil inteiro (Presidente)

Para cada um dos 5.757 municípios e postos no exterior do índice do TSE (5.571 municípios e 186 postos), somei os BUs e comparei com o arquivo oficial do município (`6257/dados/<uf>/<uf><município>-c0001-e006257-u.jws`) em `scripts/fase17_municipios.py`. **Os 5.757 batem exatamente**, nos 12 candidatos, brancos, nulos e nulos técnicos (nº 28). A soma dos votos válidos dos municípios é 119.300.788, igual ao total nacional. Os 40 postos do exterior sem seção instalada não têm BU e o oficial registra zero para eles. Os dados por município estão em `relatorio_web/municipios.json` e alimentam a consulta da página.

### 4.2.3 Eleição estadual completa, todas as 27 UFs

Em `scripts/fase18_estadual_todas.py` somei os BUs da eleição estadual de cada UF (497.897 BUs; o exterior não tem eleição estadual) e comparei com o arquivo oficial de cada UF e cargo, e o Governador também por município. Resultado:

| Verificação | Resultado |
|---|---|
| Combinações UF × cargo (Governador, Senador, Deputado Federal, Deputado Estadual ou Distrital) | **108 de 108 com 100% dos candidatos, brancos e nulos iguais** |
| Candidatos conferidos um a um | **18.839 de 18.839** |
| Governador por município | **5.571 de 5.571** municípios iguais |
| Diferenças no total de legenda | 9.904 votos de partidos "Anulado sub judice" (campo `tval` do oficial) e 1.912 nos nulos técnicos (PB 304, SE 435, SP 1.173); **nenhuma sem explicação** |

A explicação de cada diferença de legenda é verificada automaticamente: o valor dos BUs tem de ser igual ao `tval` do partido no arquivo oficial ou, para partido sem lista, fechar com o total de nulos técnicos (`vnt`). Os resultados de cada UF estão em `dados/estadual/<uf>.json`.

### 4.3 Cruzamento com o cadastro de eleitorado por seção (fonte independente)

O arquivo `eleitorado_local_votacao_2026.zip` (dados abertos do TSE, 175,8 MB, SHA-256 `f920e5f6...a26e90a`) lista 517.179 seções, **o mesmo conjunto exato do índice de seções do TSE**. As 499.248 seções principais ativas são igual ao total oficial. As únicas 41 que não têm BU são seções **não instaladas no exterior** (1 a 27 eleitores cada, 423 eleitores no total, igual ao `esni` do arquivo oficial). A soma dos eleitores aptos registrada nos BUs (158.745.079) mais esses 423 dá exatamente o total de eleitores do arquivo oficial (158.745.502). Em nenhum dos 499.207 BUs a soma de votos difere do comparecimento que o próprio BU registra. Detalhes no `ANEXO_ATRASOS.md`, seções 7 e 8.

## 5. O apagão do painel

> Os atrasos e lacunas de dados (seções que apareceram depois, status "Recebida", cauda de registros do dia seguinte, Sistema de Apuração) estão documentados em detalhe no **`ANEXO_ATRASOS.md`**. Eles são os pontos mais fracos desta auditoria.

Fontes do horário: O Tempo (matéria publicada durante a pausa, ainda sem retomada às 19h57) informa painel sem atualização desde 19h06min33s, com 323.539 de 499.248 seções (64,81%), Flávio 49,58%, Lula 42,25%. O Jornal de Brasília informa retomada às 20h08, com 84,96% das urnas apuradas: a pausa durou **cerca de 1h02**, não 47 ou 50 minutos. A CNN Brasil registra a explicação do presidente do TSE (congestionamento no sistema de divulgação por fluxo de dados acima do normal), a afirmação de que a intercorrência afetou a divulgação e não a contabilização dos votos, e que às 23h41 restavam 22 das 499.248 seções por totalizar. A divulgação das eleições estaduais continuou normalmente durante a pausa.

Gravação da TV Senado (início 16h19min46s BRT, relógio na tela confere). Estados do painel de Presidente lidos nos quadros:

| Momento | Urnas apuradas | Flávio | Lula | BUs que reproduzem (hora de recebimento) |
|---|---:|---:|---:|---|
| 19h08 a 19h18 | 47,26% | 50,20% | 41,63% | até ~18h43 |
| 19h20 a 19h56 (congelamento) | 64,81% | 49,58% | 42,25% | até ~19h05 |
| 20h10 (após a volta) | 84,96% | 48,47% | 43,49% | até ~19h59 |

- Em cada estado os quatro percentuais (Flávio, Lula, Cury, Caiado) saem dos BUs com erro RMS de até 0,005 ponto percentual. Não há salto entre o estado de 64,81% e o de 84,96%.
- O estado de 47,26% permaneceu na tela da emissora até ~19h18, quando o painel real já mostrava 64,81%: defasagem dos gráficos da emissora. É a explicação mais provável para a impressão de que "a diferença sumiu".
- A queda de Flávio (51,3% às 17h58, 49,58% no congelamento, 47,03% no final) é contínua e se explica em boa parte pela ordem de chegada das regiões. Controlando por UF, o resíduo às 19h06 é de +0,70 ponto percentual; por município, +0,32; ambos decaem a zero até as 21h.
- Os carimbos de registro dos BUs (`hr`) também pararam: nenhum registro entre 19h31m50s e 19h59m22s (27,5 minutos), depois uma rajada, e um ritmo quase constante de ~500 por minuto entre 20h05 e 20h40. Isso é coerente com um gargalo de processamento no TSE, mas não permite separar se a pausa foi de recepção, de processamento ou só de divulgação (ver `ANEXO_ATRASOS.md`, seção 2).
- O que não foi feito: o painel real do TSE (site) não foi gravado; usei o painel exibido pela TV Senado. Não li quadros entre 19h56 e 20h10 (a retomada, às 20h08, é confirmada pela imprensa e pelo estado de 84,96% visto às 20h10).

## 6. Integridade criptográfica dos BUs

Documentação oficial de 2026 (`formato-arquivos-de-bu-rdv-e-assinatura-digital`, baixada da página do TSE em `docs_tse/`). O esquema de 2026 difere do de 2022 (chave Ed25519 por tupla); em 2026:

1. Hash inicial por eleição: SHA-512 de `pleito|eleição|município|zona|seção|código da carga`.
2. Cada linha de votos recebe um hash encadeado: SHA-512 do hash anterior mais ordem, cargo, tipo de voto, quantidade, número e partido.
3. O hash final é assinado com ECDSA (ou EdDSA) pela chave de hardware da urna; o certificado dessa chave está no arquivo `vota.vsc` e se valida contra as chaves raiz do TSE (AC URNA, AC UE2020, AC UE2022).

Resultados:

| Verificação | Resultado |
|---|---|
| Cadeia de hashes (67,86 milhões de linhas de votos, 499.207 BUs) | 0 erros de hash, de ordem ou de hash final |
| **RDV contra BU**, por amostragem (6.1) | 20.811 de 20.811 seções iguais, 103.855 comparações de cargo por seção, **zero diferenças** |
| Assinatura do hash final da eleição **estadual** (6259), por amostragem | **100.761 de 100.761 seções verificadas, assinatura e certificado válidos, zero falhas**: 19.950 sorteadas (semente 2026), 80.000 sorteadas em segunda rodada (semente 2027), as 68 que deram 404 e as 743 da cauda (todas as seções que atrasaram). Cobre as 27 UFs e os quatro modelos de urna. 50 seções sorteadas do exterior ficaram de fora porque o exterior não tem eleição estadual (`scripts/fase16_assinatura_estadual.py`, `dados/assinaturas_estadual.csv`). Se mais de 0,003% das seções tivessem assinatura inválida, a chance de não aparecer nenhuma seria menor que 5% |
| Assinatura ECDSA do hash final de Presidente e certificado da urna | 499.176 de 499.176 seções com BU de urna (UE 2013, 2015, 2020 e 2022): assinatura válida e certificado válido contra a raiz do TSE, **zero falhas**. Cada certificado assina uma única seção (499.176 certificados distintos). O número da urna no nome do certificado é igual ao número interno da urna no BU em 499.162 (99,997%); as 14 diferenças são todas BUs do tipo RED (recuperação de dados), em que o equipamento que assina não é o da urna original, e nelas a assinatura e o certificado também são válidos |

### 6.1 RDV (registro digital do voto) contra o BU

O RDV é o registro, voto a voto e embaralhado para proteger o sigilo, de cada voto digitado na urna. Para as mesmas 20.811 seções da amostra de assinatura estadual (19.950 sorteadas com semente 2026, mais **todas** as 68 que deram 404 e as 743 da cauda, mais 50 do exterior) baixei o `rdv.dat` de cada seção e somei os votos por cargo, nas duas eleições (`scripts/fase19_rdv.py`, `dados/rdv_vs_bu.csv`). Mapeamento do RDV para o BU: voto nominal com número N é o candidato N; branco (incluindo o branco após suspensão) é branco; os cinco tipos de nulo são nulos; voto de legenda é do partido dos dois primeiros dígitos, porque o número de candidato que não existe conta para o partido. Validei o método numa seção antes de rodar a amostra.

Resultado: **20.811 de 20.811 seções com RDV igual ao BU em todos os cargos**, 103.855 comparações de cargo por seção, nenhuma diferença. Se mais de 0,014% das seções tivessem o RDV diferente do BU, a chance de não aparecer nenhuma na amostra seria menor que 5%. O que isso prova: o BU é a soma exata dos votos individuais registrados na própria urna. O que não prova: que cada voto registrado corresponde à intenção do eleitor.

O verificador também foi testado contra os exemplos oficiais do TSE de 2022 (9 de 9 e 7 de 7 assinaturas válidas) e contra uma seção de 2026 pelo script oficial (`bu_assinatura_tuplas.py`: "terminada com sucesso").

## 7. Limites e ressalvas

- **O BU é a saída da própria urna.** Esta auditoria prova que a totalização bate com os BUs e que os BUs estão íntegros e assinados pela urna. Ela **não prova que a urna gravou fielmente o voto digitado pelo eleitor**. Isso exige o BU impresso na seção, o RDV e a auditoria presencial.
- As chaves raiz usadas para validar os certificados vêm do pacote de documentação do próprio TSE. A confiança nelas é externa a esta verificação; a lista de hashes dessas chaves publicada pelo TSE pode ser conferida à parte.
- **Não cobertas pela assinatura:** as 31 seções do Sistema de Apuração (`busa`, outro esquema de assinatura; só a cadeia de hashes foi verificada) e, na eleição estadual 6259, as seções que não entraram na amostra (assinatura verificada por amostragem de 100.761 seções, todas válidas; cadeia de hashes verificada em todas). Os totais da eleição estadual foram conferidos ao voto nas 27 UFs (seção 4.2.3).
- **Pendentes:** o RDV foi verificado só por amostra (6.1) e o `log.jez` não foi verificado; o status "Recebida" (7.369 seções na coleta de 05/10) tem significado desconhecido, embora a soma com elas incluídas bata exatamente; a causa do apagão e a explicação dos registros do dia seguinte (Pará, Pernambuco, Maranhão) não são verificáveis com dados públicos (`ANEXO_ATRASOS.md`).
- Os percentuais reproduzidos do painel usam como denominador a soma de todos os candidatos presentes nos BUs, incluindo o nº 28 (5.246 votos, 0,004% do total). O efeito sobre os percentuais é inferior a 0,005 ponto percentual.
- Não reproduzi o painel real do TSE seção por seção: a ordem de totalização do painel não é a ordem de recebimento dos BUs (diferença de ~2 mil seções no estado de 19h06).

## 8. Como reproduzir

Requisitos: Python 3.14, `asn1tools`, `cryptography`, `pyOpenSSL`, `ecpy` (fixado no commit indicado em `docs_tse/spec2026/python/requirements.txt`), `ffmpeg` e `tesseract` (só para o vídeo).

Ordem dos scripts em `scripts/`: `fase1_congelar.py`, `fase2_aux.py`, `fase2_bu.py`, `fase3_parse.py`, `fase4_compara.py`, `fase5_faltantes_curva.py`, `fase6_composicao.py`, `fase6b_composicao_municipio.py`, `fase8_cadeia_todos.py` (mais `fase8b_contingencia.py` e `fase8c_15_secoes.py`), `fase9_assinaturas.py`, `fase10_rs_estadual.py`, `fase11_aleatorio.py`, `fase12_atrasos.py`, `fase12b_atrasos_detalhe.py`, `fase13_substituidas.py`, `fase13b_substituidas_teste.py`, `fase14_cadastro.py`, `fase15_mg_sp.py`, `fase16_assinatura_estadual.py`, `fase17_municipios.py`, `fase18_estadual_todas.py`, `fase19_rdv.py`, `video_ocr.py`, `fase7_painel_video.py`. Detalhes e decisões em `PROJECT.md`.

Os dados brutos (`dados/`, cerca de 5 GB) e o vídeo não são versionados. Os totais oficiais e índices congelados estão em `dados/oficial/` e `dados/cs/`, com os hashes em `dados/manifesto_fase1.jsonl`.

## 9. Autoria e assinatura

**Jair Lima** (Jair da Silva Lima), 7 de outubro de 2026.

- **Jornalista.** Registro profissional no Ministério do Trabalho e Emprego nº **0024314/RS**, expedido em 11/09/2026. Autenticidade em `sirpweb.mte.gov.br/sirpweb`, código 1504531.
- **Perícia.** Pós-graduado (lato sensu, 360 horas) em **Investigação Forense e Perícia Criminal**, Centro Universitário Leonardo da Vinci (Uniasselvi), curso de 2020, certificado de 05/05/2021, registro nº 79092 (livro D-359, folha 613).
- **Tecnologia da Informação.** Tecnólogo em **Redes de Computadores**, Instituto Federal Catarinense (colação de grau em 2013, diploma de 2014). Pós-graduado em **Governança de TI** (Uniasselvi, 2015) e em **Tecnologias Google for Education** (Universidade LaSalle, 2019). Curso Cisco Networking Academy *CCNA Exploration: Network Fundamentals* (2012).

**Natureza do trabalho.** Auditoria técnica independente, feita sem contratação, nomeação ou pedido de qualquer parte, apenas com arquivos públicos do TSE. Não é perícia judicial nem laudo oficial. A formação em perícia e o registro de jornalista identificam o autor e não substituem o exame por um órgão competente.

Contato: jairslima@gmail.com
