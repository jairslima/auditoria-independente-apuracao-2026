Revisão técnica independente dos arquivos `RELATORIO.md`, `ANEXO_ATRASOS.md` e `PROJECT.md`. Leitura adversária, com a perspectiva favorável no fim.

1. **Alta. Circularidade central subdimensionada no resumo.** `RELATORIO.md`, 2.4 e 7. Toda a validação depende de artefatos do TSE: os BUs, as chaves raiz e a especificação ASN.1 vêm do próprio órgão auditado. A seção 7 admite isso, mas o resumo (2.4, "Nenhum BU lido apresentou sinal de adulteração") omite a ressalva. Correção: "nenhum sinal detectável pelos métodos empregados, cujas chaves e especificação provêm do próprio TSE".

2. **Alta. "Zero a zero" é consistência, não independência.** `RELATORIO.md`, 2.2 e 4. O total oficial é gerado a partir dos mesmos BUs; a igualdade detecta erro de totalização ou transcrição, mas não detectaria uma alteração uniforme aplicada aos dois lados. Correção: declarar isso e reservar a palavra "independente" para RDV, assinatura e cadastro de eleitorado.

3. **Média. "Dois decodificadores independentes" é excessivo.** `RELATORIO.md`, 3.3. São duas implementações em Python da mesma especificação ASN.1 oficial; um erro de interpretação da especificação se duplicaria. O `PROJECT.md` ainda lista um segundo parser (Node/Go) como pendência. Correção: "duas implementações independentes do mesmo formato".

4. **Média. Erro na conta do RDV.** `RELATORIO.md`, 6.1. Com n=20.811 e prevalência de 0,014%, a chance de zero ocorrências é cerca de 5,4%, acima dos 5% declarados. O limiar correto é cerca de 0,0144% (ou "mais de 0,015%"). A frase análoga das assinaturas (0,003%, n=100.761) está correta: cerca de 4,9%.

5. **Média. Desenho amostral misto invalida a leitura populacional.** `RELATORIO.md`, 6 e 6.1. As amostras juntam sorteio (99.950) com grupos escolhidos a dedo (68 que deram 404, 743 da cauda, 50 do exterior). A frase "se mais de X% das seções..." só vale para a parte sorteada; os grupos escolhidos são censo dirigido, não amostra aleatória. Correção: relatar a parte probabilística separada.

6. **Média. "O BU é a soma exata dos votos individuais" generaliza uma amostra.** `RELATORIO.md`, 6.1. Isso foi verificado em 20.811 de cerca de 499.176 seções (4,2%). Correção: acrescentar "na amostra de 20.811 seções".

7. **Média. Soma interna da tabela principal não fecha.** `RELATORIO.md`, 4. As linhas de candidatos somam 119.300.793, mas o texto afirma votos válidos 119.300.788 (diferença de 5). A tabela diz "zero a zero" e esse descompasso não é explicado. Correção: conferir a transcrição de uma linha ou explicar os 5 votos.

8. **Baixa. 40 postos contra 41 seções.** `RELATORIO.md`, 4.2.2 diz "40 postos do exterior sem seção instalada"; 4.3 e `ANEXO_ATRASOS.md`, 7, dizem 41 seções. Correção: explicar a diferença (por exemplo, um posto com duas seções).

9. **Baixa. `PROJECT.md` conflita com o relatório.** `PROJECT.md`, linha 20, usa "17.972 agregadas", enquanto `RELATORIO.md`, 3, e o Anexo 7 usam 17.931 agregadas mais 41 sem dados. Correção: alinhar o número e a derivação.

10. **Média. Hipóteses concorrentes não testadas.** Anexo 2 e 3; `RELATORIO.md`, 4. Para o apagão, a lacuna de 27,5 minutos nos carimbos `hr` e a rajada seguinte são compatíveis tanto com gargalo quanto com pausa para reprocessamento ou reenvio de arquivos; o texto diz "coerente com gargalo" e não testa a alternativa. As 15 seções tardias "carregam exatamente as diferenças" é igualmente compatível com (re)geração dos arquivos para fechar a conta, dado que a assinatura depende das chaves do TSE. Correção: listar cada hipótese e o que a falsificaria.

11. **Média. Lacunas pouco visíveis.** `log.jez` não verificado; RDV só por amostra; 31 BUs do Sistema de Apuração sem assinatura verificada; painel real do TSE não gravado (só TV Senado via OCR); chaves raiz não conferidas fora do pacote do TSE; nenhum BU impresso confrontado. `RELATORIO.md`, 5, 6 e 7. Correção: bloco "não verificado" no topo do relatório.

12. **Baixa. Tom citável fora de contexto.** `RELATORIO.md`, 2.4, 2.5, 6.1 e 7. "Prova", "íntegros", "bate ao voto", "nenhum sinal de adulteração" e "sem descontinuidade" podem ser citados por leigos. A separação provado/não provado existe (6.1, 7) mas fica longe do resumo. Correção: qualificar já nas respostas curtas.

13. **Baixa. Semente 2026 reusada.** Os sorteios de UF/cargo, da amostra de `hr`, de assinatura e de RDV usam a mesma semente 2026, gerando amostras correlacionadas. Correção: semente distinta por sorteio.

**Perito favorável diria:** o relatório é excepcionalmente transparente (o Anexo 11 lista os próprios erros), os três estados do painel batem com erro menor que 0,005 ponto percentual, as assinaturas de 499.176 seções e de 100.761 da amostra estadual são válidas, e os limites (BU como saída da própria urna, chaves do TSE) estão declarados.

**Veredito:** sustenta bem a consistência entre BUs, total oficial, RDV amostral e assinaturas, além da reconstrução dos três estados do painel. Não sustenta, sem qualificação, "nenhum sinal de adulteração" nem a inferência populacional das amostras mistas. A mudança mais importante é reformular as conclusões fortes (2.4 e 6.1) para "detectável pelos métodos empregados, com chaves do TSE" e "na amostra", separando a parte sorteada da dirigida nas frases estatísticas.
