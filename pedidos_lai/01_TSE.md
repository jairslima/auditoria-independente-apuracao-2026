# Pedido de acesso à informação ao Tribunal Superior Eleitoral

**Destinatário:** Ouvidoria / Serviço de Informação ao Cidadão (SIC) do Tribunal Superior Eleitoral, por meio do formulário eletrônico da Ouvidoria.
**Assunto:** Registros de recepção, totalização e divulgação do 1º turno de 04/10/2026; incidente na divulgação do resultado de Presidente; estados "Recebida" e "Totalizada".
**Data do protocolo:** [preencher]

**Requerentes**

1. **Jair da Silva Lima**, jornalista profissional registrado no Ministério do Trabalho e Emprego sob o nº 0024314/RS (cartão emitido em 11/09/2026, código de autenticidade 1504531). CPF: [informar no formulário]. E-mail: jairslima@gmail.com.
2. **Folha dos Vales** (folhadosvales.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.
3. **Folha do Litoral Norte** (folhadolitoralnorte.com.br), publicação jornalística da qual o primeiro requerente é responsável. CNPJ: [informar, se houver]. E-mail: afolhadosvales@gmail.com.

Os requerentes apresentam este pedido em conjunto. Nos termos do art. 10, § 3º, da Lei nº 12.527/2011, não é exigida a motivação do pedido; informa-se, apenas por transparência, que se trata de apuração jornalística de interesse público sobre o processamento do 1º turno de 04/10/2026.

**Fundamento.** Constituição Federal, art. 5º, XIV e XXXIII, e art. 37, § 3º, II; Lei nº 12.527/2011 (Lei de Acesso à Informação), em especial os arts. 7º, 10, 11, 12 e 14; e Resolução-TSE nº 23.435/2015, alterada pela Resolução-TSE nº 23.583/2018.

**Contexto.** Uma auditoria independente do 1º turno (*Auditoria Independente da Apuração 2026 by Jair Lima*), feita exclusivamente com arquivos públicos do TSE (boletins de urna, registro digital do voto, arquivos de assinatura e arquivos de resultado de `resultados.tse.jus.br`), reproduziu a soma de votos de Presidente (499.207 seções) e da eleição estadual e **não encontrou diferença em relação ao resultado oficial**. Ao fazê-la, porém, identificou pontos de processamento que os dados públicos não permitem explicar. Todos os horários abaixo são de Brasília e todos os números foram medidos nos arquivos públicos coletados em 05 e 06/10/2026.

**Fatos observados nos arquivos públicos**

1. **Pausa na divulgação de Presidente.** Segundo a imprensa, o painel de Presidente ficou sem atualização de 19h06min33s até as 20h08, em 64,81% das seções, e o presidente do Tribunal atribuiu o fato a congestionamento no sistema de divulgação. Nos arquivos públicos, o campo `hr` (hora de registro da seção) mostra 110.864 seções registradas nesse período, mas **nenhum registro entre 19h31m50s e 19h59m22s (27,5 minutos)**, seguido de rajada e de ritmo quase constante de cerca de 500 por minuto entre 20h05 e 20h40.
2. **Arquivos publicados com atraso por zona.** Na primeira coleta (05/10), 68 seções de cinco zonas eleitorais (Betim/MG zonas 316 e 319, Teófilo Otoni/MG zona 269, Uberlândia/MG zona 279 e Carapicuíba/SP zona 388) retornavam "arquivo não encontrado". Todas constavam com BU registrado em 04/10 entre 20h07 e 21h15 e foram publicadas entre 05/10 e 06/10 (a última leva, 15 seções, só em 06/10).
3. **Registros no dia seguinte.** 743 seções têm registro (`hr`) depois das 23h41 de 04/10, até as 15h24 de 05/10 (Pará 621, Pernambuco 60, Maranhão 45, Bahia 7, Amazonas 7, Minas Gerais 3). O arquivo oficial de resultado de Presidente do Pará, gerado às 12h51m45s de 05/10 com 20.827 de 20.827 seções totalizadas, tem total **igual** à soma dos boletins incluindo as seções do Pará registradas depois dessa hora. Logo, para essas seções, o campo `hr` não parece indicar o momento em que os votos entraram no total.
4. **Estados "Recebida" e "Totalizada".** Na coleta de 05/10, 491.838 seções apareciam como "Totalizada" e 7.369 como "Recebida" nos arquivos de seção (`aux.json`), concentradas em poucas zonas (SP 5.125, MG 1.729, PA 506), embora o resultado oficial já contasse 100% das seções.
5. **Índice de seções.** Os campos `da`/`ha` do índice por UF (`...-cs.json`) são, em 99,3% das seções, mais de uma hora posteriores ao `hr`, e 69.438 seções compartilham o mesmo minuto (05/10 às 00h52).
6. **Urnas substituídas.** Os BUs trazem 3.033 seções com urna de contingência que passou a ser de seção (tipo de urna 4) e 50 de recuperação de dados (RED), contra 1.121 substituições divulgadas durante a apuração. O campo opcional de histórico de correspondências está vazio em todos os BUs.
7. **Sistema de Apuração.** 31 seções (29 no exterior, 2 em MG) têm BU gerado pelo Sistema de Apuração (`.busa`) e arquivo de assinatura `.vscsa`, cujo esquema de verificação não consta da documentação pública de formato de BU/RDV/assinatura de 2026.

**Pedidos**

1. O **registro de eventos** (log) dos sistemas de recepção, totalização e divulgação de resultados de 04/10/2026, entre 17h e 23h59, e de 05/10/2026 até 12h51, ao menos de forma agregada por intervalo de 5 minutos: quantidade de BUs recebidos, totalizados e publicados, e os intervalos de indisponibilidade ou lentidão.
2. O **relatório técnico do incidente** na divulgação do resultado de Presidente entre 19h06 e 20h08: hora de início, de detecção e de normalização, causa, componentes envolvidos, providências adotadas e se algum arquivo de resultado foi regenerado ou republicado, com a respectiva cronologia.
3. Para **cada seção do Anexo TSE** (842 seções, lista em anexo): a hora de recebimento do BU, de totalização e de publicação dos arquivos, e o motivo de qualquer diferença entre elas.
4. A **definição oficial e a regra de atribuição** dos estados "Recebida" e "Totalizada", do campo `hr` e dos campos `da`/`ha`, e a explicação para os fatos 3, 4 e 5 acima.
5. Para as 68 seções do fato 2: o **motivo da publicação tardia** por zona e o **resumo criptográfico (hash) de cada arquivo no momento do recebimento**, para conferência de integridade.
6. O **critério** de contagem de urnas substituídas, a explicação da diferença entre as 3.033 seções de urna substituta mais 50 RED e as 1.121 substituições divulgadas, e a razão de o histórico de correspondências não constar dos BUs.
7. A **especificação do esquema de assinatura** do arquivo `.vscsa` e as chaves públicas (ou listas de hash das chaves públicas) das Eleições 2026, para permitir a verificação independente dos 31 BUs do Sistema de Apuração.

**Forma de entrega.** Em meio digital, de preferência em arquivo estruturado (CSV ou planilha) para as listas por seção e em PDF para relatórios, enviados ao e-mail dos requerentes ou anexados ao sistema. Caso parte da informação seja considerada sigilosa, solicita-se o acesso à parte não sigilosa, com ocultação apenas do trecho protegido (art. 7º, § 2º), e o inteiro teor da decisão de negativa (art. 14).

**Esclarecimento sobre o sigilo do voto.** Este pedido não solicita dados pessoais de eleitores nem qualquer informação que permita identificar votos individuais. Todas as informações pedidas dizem respeito a horários, estados de processamento, registros técnicos e esclarecimentos sobre arquivos já públicos, por seção eleitoral ou de forma agregada.

Os requerentes se colocam à disposição para encaminhar o relatório da auditoria, as listas completas e os scripts que reproduzem as medições citadas, para que o Tribunal possa conferi-las.

**Anexos:** `anexos/anexo_TSE_todas_as_secoes.csv` (842 seções: as 68 de publicação tardia, as 743 registradas depois de 23h41 e as 31 do Sistema de Apuração, com hora de emissão do BU na urna e hora de registro) e `anexos/resumo_zonas_recebida.csv` (zonas com estado "Recebida").

Termos em que pedem deferimento.

[Local e data]

Jair da Silva Lima, por si e pelas publicações Folha dos Vales e Folha do Litoral Norte
