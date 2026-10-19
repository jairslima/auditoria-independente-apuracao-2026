# Resposta do TRE-PE ao pedido LAI (protocolo 81151008080724)

**Situação:** e-mail "Resposta de Protocolo" recebido em 19/10/2026 às 14h04 (Brasília), id Gmail `1a1551f739bf1bba`, remetente naoresponda-sac-tre-pe@tse.jus.br, com 2 anexos verificados pelo Gmail. Pesquisa de satisfação enviada junto (id `1a1551ee679a5a60`), com a solicitação "concluída em 19/10/2026, às 14:04".

**Anexos (ainda NÃO analisados; precisam ser baixados do Gmail e guardados em `pedidos_lai/respostas/TRE-PE_2026-10-19/`, pasta no `.gitignore`):**
1. Planilha "Auditoria de Arquivos Recebidos PE" (nº 3532972): para cada uma das 60 seções do anexo, horário de geração do arquivo na urna, de leitura/recebimento pela Justiça Eleitoral, de transmissão e de recebimento no TSE.
2. "Relação de BUs rejeitados pelo Sistema de Totalização" (nº 3532994): os 129 registros de "Erro por retransmissão de uma seção já recebida" (não só as 60).

## O que o tribunal afirma (a STIC do TRE-PE respondendo)

| Item do pedido | Resposta do tribunal | Como tratar |
|---|---|---|
| 1. Horários por seção | Planilha anexa. Todos os resultados foram gerados pelas urnas das próprias seções. Em nenhuma das 60 foi preciso recuperar resultados nem usar o Sistema de Apuração. Envio inicial em 04/10/2026 por pontos de transmissão com o JE Connect (VPN). Em todas as 60 houve **retransmissão "equivocada" em 05/10** pelo Transportador Web, nos cartórios. | Conferir a planilha contra `aux.json`/`hr` e contra a lista dos 129 rejeitados. |
| 2. Motivo e operação | A mídia de resultado também grava arquivos de biometria (`.wsqmes`, `.wsqman`, `.wsqbio`), pesados. O art. 242 da Res.-TSE 23.751/2026 faculta enviá-los em até 3 dias. As zonas deveriam reler as mídias no dia seguinte e selecionar só a biometria, mas **enviaram o conteúdo inteiro** (BU, RDV, LOG e biometria). O sistema rejeitou os BUs por retransmissão, com data e hora idênticas às do levantamento. Não há ata nem relatório de ocorrência. | Mesma explicação que o TRE-MA deu para as 01h56. Confirma que o campo `hr` público guarda a última tentativa, não a chegada. |
| 3. Substituição de urna | Em nenhuma das 60 houve substituição. | Cruzar com o levantamento de urnas substituídas (ANEXO seção 8). |
| 4. Hash do BU na urna e no TSE | O TRE-PE **não guarda cópia dos BUs** (ficam sob guarda dos juízos eleitorais) e não acessa o repositório do TSE; não consegue calcular hashes. Indica pedir ao TSE as cópias dos BUs usados e dos rejeitados. Diz que a integridade é verificada na recepção pelo TSE e que a correspondência urna preparada x urna efetiva pode ser conferida em dois ZIPs públicos (abaixo). | Item 4 **não foi atendido pelo TRE-PE**: segue só com o TSE (pedido nº 81136107180936, prazo 27/10). |
| 5. 50 seções da zona 15 (Cabo de Santo Agostinho) às 10h49 de 05/10 | Explicação do item 2: a zona leu todas as mídias e transmitiu tudo de uma vez, o que gera o mesmo horário de rejeição. | Coerente com o minuto único. |

Outros dados informados: totalização de Governador e de Senador em PE em **04/10/2026 22:54:57** (horário local), comandada pelo TRE-PE (a de Presidente é comandada pelo TSE); o TRE-PE só faz a logística de transmissão; dúvidas sobre os arquivos retransmitidos e rejeitados no app Resultados devem ir à Ouvidoria do TSE.

## Leitura crítica (não aceitar sem conferir)

- A frase de que a rejeição "é uma prova de que o conteúdo era idêntico" **não se sustenta como prova**: a rejeição por "seção já recebida" é uma regra do sistema para a seção, e o texto não diz que o sistema compara conteúdo. Só a comparação de hashes mostra identidade. O próprio tribunal reconhece que não pode calculá-los e remete ao TSE.
- A explicação (biometria enviada junto com o resto, por erro de operação nas zonas) é plausível e consistente com o TRE-MA, mas é **declaração do tribunal**, sem ata. Verificável pela planilha: se as 60 rejeições estão no mesmo dia, em poucos minutos por zona, e se há 129 no total.
- O que o dado público já mostrava e agora tem explicação oficial: o horário `hr` das 60 seções é o das retransmissões rejeitadas, não o da chegada do BU original (04/10). A chegada original, segundo o tribunal, foi a noite de 04/10. A planilha 3532972 deve trazer esse horário original: **é o dado que falta** para fechar o caso de PE.
- Ficam sem resposta: hash do BU (item 4) e a relação de PE entre o horário de recebimento do TSE e o `hr` público.

## Próximos passos

1. **Baixar os 2 anexos** do Gmail (o mais simples é "baixar todos os anexos", que gera um ZIP, como no TRE-MA) e guardar em `pedidos_lai/respostas/TRE-PE_2026-10-19/`; avisar para eu analisar.
2. Comparar a planilha 3532972 com `resultados/` e `dados/aux.json` das 60 seções, e a lista de 129 rejeitados com as 842 seções do anexo LAI.
3. Baixar (precisa de autorização do Jair) os dois ZIPs públicos de correspondência:
   - `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/correspesp/CESP_1t_PE_041020261259.zip` (urna esperada)
   - `https://cdn.tse.jus.br/estatistica/sead/eleicoes/eleicoes2026/correspefet/CEFT_1t_PE_051020261049.zip` (urna efetiva)
   e conferir as 60 seções de PE (mais as da lista dos 129).
4. Cobrar do TSE os BUs recebidos e os rejeitados das 60 seções (conferir em `pedidos_lai/01_TSE.md` se o pedido ao TSE já cobre; se não cobrir, fazer novo pedido citando esta resposta do TRE-PE) para a comparação de hashes.
5. Atualizar RELATORIO (seção 7.2), ANEXO e a página, como foi feito para o TRE-MA; revisar a frase dos protocolos da matéria da Folha dos Vales.
6. Responder à pesquisa de satisfação do TRE-PE é opcional (decisão do Jair).
