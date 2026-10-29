# Complemento ao pedido ao TSE do 2º turno (26/10/2026): duas coletas do repositório

**Destinatário:** Ouvidoria do TSE (ouv@tse.jus.br), no mesmo fio do pedido de 26/10/2026 (mensagem Gmail `1a179e2fabe13ed7`).
**Situação:** ENVIADO em 27/10/2026 (mensagem Gmail `1a180148191792cf`, no fio `1a179e2fabe13ed7`), após aprovação do Jair.
**Anexo:** nenhum. A lista das 8.753 seções (`AuditoriaPresidente2026_T2/resultados/fase26_aux_mudancas.csv`) é oferecida no texto e enviada se o Tribunal pedir.

---

Prezados,

Complemento o pedido que enviei em 26/10/2026 sobre o 2º turno com um fato novo, medido em duas coletas completas do repositório público de arquivos de urna (499.207 seções em cada uma).

**Fatos**

1. As coletas foram feitas em 26/10/2026, de manhã e início da tarde, e em 27/10/2026, das 11h10 às 15h12, ambas por consulta ao arquivo de cada seção (<code>aux.json</code>).
2. **O hash do BU é idêntico nas duas coletas, nas 499.207 seções.** Nenhum BU publicado mudou.
3. O estado e a lista de arquivos de 8.753 seções (1,75%) mudaram entre as duas coletas, 6.604 delas em São Paulo, 757 na Bahia, 624 no Pará, 322 em Pernambuco e 191 no Maranhão.
4. Em 7.017 seções o estado passou de "Recebida" para "Totalizada": o arquivo <code>imgbu</code> deixou de constar e, em 7.010 delas, o campo de data e hora (<code>hr</code>) voltou a um horário anterior.
5. Em 1.736 seções o estado passou de "Totalizada" para "Recebida": o arquivo <code>imgbu</code> passou a constar e o <code>hr</code> passou a um horário posterior (em uma delas, o arquivo de log também passou a constar).

**Pedidos complementares**

1. A regra do sistema que faz o estado ("Recebida" e "Totalizada"), o campo <code>hr</code> e a presença do arquivo <code>imgbu</code> mudarem sem que o hash do BU mude. O que significa a presença do <code>imgbu</code> e em que situações ele entra e sai.
2. Para as 8.753 seções (a lista por seção será enviada em CSV assim que o Tribunal indicar o canal ou o formato), o histórico de eventos de recebimento e processamento de pacotes entre 25/10 e 27/10/2026, com data e hora: recebimentos, reenvios, rejeições e mudanças de estado.
3. A confirmação de que, nessas seções, o BU usado na totalização é o que corresponde ao hash publicado, que permaneceu o mesmo nas duas coletas.
4. Se o repositório público altera, depois da totalização, outros campos ou arquivos de uma seção além dos citados, e se essas alterações são registradas em log.

Peço a resposta em meio digital, em CSV para as listas por seção. Caso parte da informação seja considerada sigilosa, peço o fornecimento da parte não sigilosa e a indicação do fundamento legal (art. 7º, § 2º, da Lei nº 12.527/2011).

Os requerentes se colocam à disposição para encaminhar as coletas e os scripts que reproduzem as medições.

Termos em que pedem deferimento.

Três Coroas/RS, 27 de outubro de 2026

Jair da Silva Lima, por si e pelas publicações Folha dos Vales e Folha do Litoral Norte
Jornalista profissional (MTE 0024314/RS)
