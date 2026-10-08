# Auditoria Independente da Apuração 2026 by Jair Lima

Auditoria externa e independente do 1º turno das eleições de 4 de outubro de 2026, feita apenas com arquivos públicos do TSE (boletins de urna, registro digital do voto, arquivos de assinatura e arquivos de resultado de `resultados.tse.jus.br`).

**Resultado principal:** a soma dos 499.207 boletins de urna reproduz o resultado oficial de Presidente sem nenhuma diferença (119.300.788 votos válidos), em todos os candidatos, brancos e nulos, nas 27 UFs, no exterior e nos 5.757 municípios e postos. Na eleição estadual, 108 de 108 combinações de UF e cargo conferem. As assinaturas digitais das urnas são válidas em todas as seções de Presidente. O relatório também documenta, sem esconder, os pontos que os dados públicos não explicam (pausa do painel, arquivos publicados com atraso, estado "Recebida", registros do dia seguinte).

## Onde ler

- **Página navegável (consulta por município e por candidato):** https://www.folhadosvales.com.br/auditoria-2026
- **Relatório completo:** [`RELATORIO.md`](RELATORIO.md)
- **Atrasos e lacunas de dados (os pontos mais fracos):** [`ANEXO_ATRASOS.md`](ANEXO_ATRASOS.md)
- **Pedidos de acesso à informação enviados ao TSE e aos TREs:** [`pedidos_lai/`](pedidos_lai) (CPF mascarado)
- **Continuidade técnica do projeto:** [`PROJECT.md`](PROJECT.md)

## Como reproduzir

Requisitos: Python 3.14, `asn1tools`, `cryptography`, `pyOpenSSL`, `ecpy`; `ffmpeg` e `tesseract` só para o vídeo do painel. Os scripts estão em [`scripts/`](scripts), em ordem de fase (`fase1_congelar.py` até `fase23_nomes.py`). O TSE limita as conexões (HTTP 429 acima de cerca de 10 simultâneas). Os dados brutos (cerca de 7 GB) não são versionados; os totais oficiais e os índices congelados estão em `dados/oficial/` e `dados/cs/`, com hashes em `dados/manifesto_fase1.jsonl`. A especificação oficial usada é a do pacote de documentação do próprio TSE (`docs_tse/`).

O kit para repetir o trabalho no 2º turno está em [`segundo_turno/`](segundo_turno).

## Limites

O boletim de urna é a saída da própria urna. Esta auditoria mostra que a totalização é consistente com os boletins e que eles não foram alterados depois de assinados, pelos métodos empregados. Ela **não prova** que a urna gravou fielmente o voto digitado pelo eleitor: isso exige o boletim impresso na seção e auditoria presencial. A especificação e as chaves raiz usadas para validar as assinaturas vêm do próprio TSE. **Não é perícia judicial nem laudo oficial.**

## Autoria

**Jair Lima** (Jair da Silva Lima): jornalista (MTE 0024314/RS), pós graduado em Investigação Forense e Perícia Criminal e em Governança de TI, tecnólogo em Redes de Computadores. Contato: jairslima@gmail.com.

Licença: MIT (ver [`LICENSE`](LICENSE)).
