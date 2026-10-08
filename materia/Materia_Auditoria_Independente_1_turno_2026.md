# Auditoria independente refaz a soma do 1º turno com dados públicos do TSE e não encontra nenhuma diferença em Presidente

*Boletins de urna de 499.207 seções reproduzem o resultado oficial ao voto; trabalho aponta pontos que só o TSE e os TREs podem explicar, e pedidos de informação já foram enviados*

Uma auditoria independente, feita apenas com arquivos públicos do Tribunal Superior Eleitoral (TSE), refez a soma dos votos do 1º turno das eleições de 4 de outubro de 2026 e **não encontrou nenhuma diferença** entre os boletins de urna (BUs) e o resultado oficial para Presidente: nem de um voto. Os 499.207 boletins das seções instaladas somam exatamente os 119.300.788 votos válidos do total oficial: Flávio Bolsonaro (PL) 56.104.503, Lula (PT) 53.879.538, Augusto Cury 3.448.569, Renan Santos 2.675.887, Ronaldo Caiado 2.605.148 e Zema 326.488, além de brancos (2.300.798) e nulos (3.669.003).

O trabalho foi feito pelo jornalista Jair Lima, responsável pela Folha dos Vales e pela Folha do Litoral Norte, com formação em Investigação Forense e Perícia Criminal e em tecnologia da informação. **Não se trata de perícia judicial nem de laudo oficial:** é uma auditoria técnica sem contratação de qualquer parte, e o relatório completo, com os scripts para quem quiser repetir a conta, está disponível.

## O que foi conferido

* **Soma por urna, município e UF.** A soma dos BUs bate com o oficial nos 5.757 municípios e postos no exterior e nas 28 abrangências (27 UFs e exterior), em todos os candidatos, brancos e nulos. A margem entre Flávio e Lula, de 2.224.965 votos, é igual à oficial.
* **Eleição estadual.** Nas 27 UFs, as 108 combinações de UF e cargo (Governador, Senador, Deputado Federal e Estadual) têm 100% dos 18.839 candidatos iguais ao arquivo oficial, e o Governador bate nos 5.571 municípios. No Rio Grande do Sul, por exemplo, Zucco (3.516.048 votos), Juliana Brizola (1.917.374) e Gabriel Souza (510.698) para o governo, e Sanderson, Marcel van Hattem e Manuela d'Ávila no Senado, estão iguais ao voto.
* **Integridade dos boletins.** A cadeia de hashes de 67,86 milhões de linhas de votos fecha em todos os BUs, e a assinatura digital de cada urna e o certificado são válidos nas 499.176 seções com BU de urna. As 31 seções apuradas pelo Sistema de Apuração (29 no exterior e 2 em Minas Gerais) também têm assinatura válida nas 31.
* **Registro voto a voto.** O registro digital do voto (RDV) bate com o BU nas 20.811 seções verificadas, incluindo todas as que atrasaram.
* **Log das urnas.** O registro de eventos de 842 seções que atrasaram ou foram registradas no dia seguinte foi comparado com o de 1.500 seções sorteadas. Nada na urna explica o atraso.

## A pausa do painel

Durante a apuração, o painel do TSE ficou sem atualizar de 19h06 até as 20h08, com cerca de 64,8% das seções, e o presidente do Tribunal atribuiu o fato a congestionamento no sistema de divulgação. A auditoria mostra que **não há salto nem descontinuidade nos números dos boletins**: os três estados do painel exibidos pela TV Senado (antes, durante e depois da pausa) são reproduzidos pelos BUs com erro de até 0,005 ponto percentual. Os registros de chegada dos boletins também pararam por 27,5 minutos e depois vieram em rajada, o que é coerente com um gargalo dentro do TSE, mas os dados públicos não permitem dizer se foi de recepção, de processamento ou só de divulgação.

Sobre a queda do percentual de Flávio ao longo da noite, de 51,3% às 17h58 para 47,03% no final, a análise indica que ela se explica em boa parte pela ordem em que as regiões foram chegando.

## Onde ficam as perguntas em aberto

O relatório lista, sem esconder, os pontos que os dados públicos não explicam:

* **68 seções com arquivos publicados com atraso**, em cinco zonas de Betim, Teófilo Otoni e Uberlândia (MG) e Carapicuíba (SP). Todas foram publicadas até 6 de outubro e a soma fecha com elas.
* **743 seções com registro no dia seguinte**, a maioria no Pará (621), além de Pernambuco, Maranhão, Bahia, Amazonas e Minas. O arquivo oficial do Pará, gerado às 12h51 de 5 de outubro, já tinha o total igual à soma dos BUs incluindo essas seções, o que indica que o horário de registro não é o momento em que os votos entraram no total.
* **7.369 seções com o estado "Recebida"** em vez de "Totalizada" na coleta de 5 de outubro, concentradas em São Paulo, Minas e Pará. O estado coincide exatamente com a presença do arquivo de imagem do boletim, mas o significado do rótulo só o TSE pode dizer.
* **Urnas substituídas:** os BUs mostram 3.033 seções com urna substituta e 50 de recuperação de dados, contra 1.121 substituições divulgadas durante a apuração.

Nenhum desses pontos altera a soma final. Eles afetam a reconstrução da cronologia.

## Limites do trabalho

O boletim de urna é a saída da própria urna. A auditoria mostra que a totalização é consistente com os boletins e que eles não foram alterados depois de assinados, pelos métodos usados, mas **não prova que cada voto foi gravado exatamente como digitado pelo eleitor**. Isso exige o boletim impresso na seção e auditoria presencial. As chaves e a especificação usadas para validar as assinaturas vêm do próprio TSE.

## Pedidos de informação

Em 7 de outubro, o autor e as duas publicações enviaram pedidos de acesso à informação (Lei 12.527/2011) ao TSE e aos tribunais regionais eleitorais do Pará, de Pernambuco, do Maranhão, de Minas Gerais e de São Paulo. Pedem os horários de recebimento e transmissão de cada seção, o relatório técnico da pausa do painel, a definição dos estados "Recebida" e "Totalizada" e a razão de cada atraso. O prazo legal de resposta é de 20 dias, prorrogável por mais 10. O TSE (protocolo 81136107180936) e o TRE de Pernambuco (81151008080724) registraram os pedidos; até a publicação desta reportagem, nenhum dos tribunais havia respondido o mérito. [Atualizar esta frase antes de publicar.]

*Contato do autor: jairslima@gmail.com. Auditoria Independente da Apuração 2026 by Jair Lima.*
