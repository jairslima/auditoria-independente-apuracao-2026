# Complemento ao pedido ao TSE (protocolo 81136107180936) com fatos novos de Pernambuco

**Destinatário:** Ouvidoria do TSE (ouv@tse.jus.br), no mesmo fio do pedido de 07/10/2026 (mensagem Gmail `1a1182cc8a9005f1`).
**Assunto:** Complemento ao protocolo 81136107180936: BUs recebidos e rejeitados de 129 seções de Pernambuco.
**Anexo:** `pedidos_lai/anexos/anexo_TSE_complemento_PE_129_rejeitados.csv` (129 registros, extraídos da relação do sistema de totalização que o TRE-PE nos forneceu).
**Situação:** rascunho no Gmail de jairslima@gmail.com, NÃO enviado (aguarda revisão do Jair). Prazo do pedido original: 27/10/2026 (20 dias) e 06/11/2026 (30 dias).

---

Prezados,

Complemento o pedido registrado sob o protocolo 81136107180936 (07/10/2026) com fatos novos, obtidos na resposta do TRE-PE ao protocolo 81151008080724, que me remeteu ao TSE para o que não pôde informar. Os requerentes são os mesmos: Jair da Silva Lima, jornalista profissional registrado no MTE sob o nº 0024314/RS, por si e pela Folha dos Vales e pela Folha do Litoral Norte.

**Fatos informados pelo TRE-PE e conferidos nos documentos que ele enviou**

1. Das 60 seções de Pernambuco do Anexo TSE com registro no dia 05/10/2026, todas tiveram o arquivo de resultado gerado pela urna da própria seção, recebido no TSE em 04/10/2026 (entre 38 e 126 minutos após a geração) e antes das 22h54min57s, horário local informado para a totalização de Governador e Senador. Em todas houve um segundo pacote, transmitido pelo Sistema Transportador Web nos cartórios, em 05/10/2026.
2. A relação "Consulta de BUs rejeitados" do sistema de totalização (em anexo) traz 129 rejeições em Pernambuco, todas com a mensagem "Erro por retransmissão de uma seção já recebida", gravadas em apenas dois minutos: 52 em 05/10/2026 às 10h49 e 77 em 06/10/2026 às 12h58.
3. O campo `hr` publicado no repositório de arquivos de urna passou a indicar o horário da rejeição (51 seções, lote de 10h49) ou o do recebimento do segundo pacote (9 seções, lote de 06/10) nas 60 seções do pedido. Outras 67 seções rejeitadas no mesmo lote de 06/10 mantiveram o `hr` do envio original de 04/10.
4. O TRE-PE informa que não guarda cópia dos BUs, não acessa o repositório do TSE e, por isso, não pode calcular hashes, e que cabe ao TSE informar sobre os arquivos retransmitidos e rejeitados.
5. Os arquivos públicos de correspondência de urnas (CESP de 04/10 e CEFT de 05/10) mostram, para as 129 seções, urna esperada igual à urna efetivada, sem divergência e com origem "Urna Eletrônica". O arquivo CEFT foi gerado em 05/10/2026 às 10h49min30s, o mesmo minuto do primeiro lote de rejeições.

**Pedidos complementares**

1. Para as 129 seções do anexo: **cópia dos arquivos de BU (`bu.dat`) e do `hash.dat`** recebidos em 04/10/2026 e dos retransmitidos e rejeitados em 05 e 06/10/2026, ou, se a cópia não for possível, o **resumo criptográfico (SHA-256 ou SHA-512) de cada arquivo recebido e de cada arquivo rejeitado**, com a data e a hora do recebimento. Este item amplia o item 5 do pedido original, que tratava apenas das 68 seções de publicação tardia.
2. A **regra** do sistema de totalização que define o campo `hr` do repositório público: por que ele passou a indicar o horário da retransmissão em 60 seções e permaneceu no horário do envio original em 67 outras seções com a mesma rejeição. Este item complementa o item 4 do pedido original.
3. A **rotina que registra as rejeições em lote** em 05/10/2026 às 10h49 e em 06/10/2026 às 12h58: o que a executa, com que periodicidade e se há relação com a geração do arquivo de correspondência efetivada às 10h49min30s de 05/10.
4. Se o sistema, ao rejeitar uma transmissão por "retransmissão de uma seção já recebida", **compara o conteúdo (hash)** do arquivo retransmitido com o do arquivo já recebido, ou se rejeita pela simples existência da seção, sem comparar o conteúdo.
5. A **confirmação** de que, nas 129 seções, o BU utilizado na totalização é o recebido em 04/10/2026, com a data e a hora do recebimento de cada um.

Peço que a resposta seja enviada em meio digital, preferencialmente em CSV para as listas por seção. Caso parte da informação seja considerada sigilosa, peço o fornecimento da parte não sigilosa e a indicação do fundamento legal (art. 7º, § 2º, da Lei nº 12.527/2011).

Atenciosamente,
Jair da Silva Lima
Jornalista profissional (MTE 0024314/RS)
Folha dos Vales e Folha do Litoral Norte
afolhadosvales@gmail.com
