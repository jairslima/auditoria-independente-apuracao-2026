# Como protocolar os pedidos de acesso à informação

Conjunto de seis pedidos, redigidos em nome de Jair da Silva Lima e das publicações Folha dos Vales e Folha do Litoral Norte. **Nada foi enviado.** O protocolo é feito por você, depois de ler cada texto e concordar com ele.

| Ordem | Arquivo | Destinatário | Seções do anexo | O que se pede, em uma linha |
|---|---|---|---:|---|
| 1 | `01_TSE.md` | TSE, Ouvidoria (SIC) | 842 | log de recepção e totalização, relatório do incidente das 19h06 às 20h08, definição de "Recebida"/"Totalizada", critério das urnas substituídas, esquema de assinatura do Sistema de Apuração |
| 2 | `02_TRE-PA.md` | TRE do Pará | 621 | por que 621 seções têm registro só em 05/10 (354 em Belém, zona 97) |
| 3 | `03_TRE-PE.md` | TRE de Pernambuco | 60 | idem (50 em Cabo de Santo Agostinho, zona 15, no mesmo minuto) |
| 4 | `04_TRE-MA.md` | TRE do Maranhão | 45 | idem (Viana e Cajari, zona 20, às 01h56) |
| 5 | `05_TRE-MG.md` | TRE de Minas Gerais | 61 | publicação tardia de arquivos em Betim, Teófilo Otoni e Uberlândia; 2 seções do Sistema de Apuração |
| 6 | `06_TRE-SP.md` | TRE de São Paulo | 12 | publicação tardia em Carapicuíba, zona 388; estado "Recebida" |

Os anexos (listas de seções, com hora de emissão do BU na urna e hora de registro) estão em `anexos/`. Cada pedido cita o seu anexo.

## Antes de enviar (checklist)

1. **Leia os seis textos.** Eles afirmam fatos medidos na auditoria, com números. Se algum número ou frase não for algo que você assinaria, corrija o arquivo `scripts/fase20b_redige_pedidos.py` ou me peça, e eu regenero.
2. **Preencha os campos entre colchetes:** CPF, CNPJ de cada Folha (se houver) e a data do protocolo. Não coloquei nenhum documento pessoal nos textos.
3. **Confirme o canal de cada tribunal.** O TSE recebe pedidos de acesso à informação pela Ouvidoria (formulário eletrônico, `tse.jus.br/servicos-eleitorais/servicos/ouvidoria-tse`, regida pela Res.-TSE 23.435/2015). Cada TRE tem a sua Ouvidoria/SIC no próprio site. Alguns usam o Fala.BR (gov.br), outros formulário próprio: verifique no site de cada um antes.
4. **Quem aparece como solicitante.** Os formulários costumam aceitar uma pessoa física. Registre o pedido em nome de **Jair da Silva Lima**, cole o texto no campo de descrição e anexe o CSV. Os nomes das duas Folhas já estão no corpo do texto.
5. **Anexe o CSV** de cada pedido (`anexos/anexo_TSE_todas_as_secoes.csv` e `anexos/anexo_TRE-xx.csv`). O do TSE pode ser grande para alguns formulários: se não couber, anexe só o do TSE em PDF resumido ou envie por e-mail e cite o protocolo.
6. **Guarde o número do protocolo** de cada um e a data. Eu registro no `PROJECT.md` quando você me passar.

## Prazos (Lei 12.527/2011)

- Resposta em até **20 dias** a contar do protocolo, prorrogáveis por mais **10 dias** com justificativa (art. 11, §§ 1º e 2º).
- Se negarem ou não responderem: **recurso em até 10 dias** (art. 15), dirigido à autoridade superior, pelo mesmo sistema, seguindo o procedimento da Res.-TSE 23.435/2015. Peça sempre o inteiro teor da negativa (art. 14).
- Os pedidos não têm custo; só o de reprodução, se houver (art. 12).

## Ordem sugerida

Enviar o TSE primeiro, e os cinco TREs no mesmo dia. Assim, as respostas se cruzam: o TSE explica o sistema, os TREs explicam as zonas.

## O que fazer quando as respostas chegarem

Entregue os arquivos a mim. Eu cruzo cada resposta com os dados da auditoria, atualizo o `ANEXO_ATRASOS.md` (seções 2, 3, 4 e 6), o `RELATORIO.md` e a página, e marco o que passou de "hipótese" a "esclarecido" ou "ainda em aberto".

## Cuidados com o tom

Os textos pedem esclarecimento e registros. Nenhum acusa ninguém, e todos dizem que a soma dos votos **não** diverge do resultado oficial. Isso é intencional: é o que os dados mostram, e um pedido cooperativo tem mais chance de obter os logs.
