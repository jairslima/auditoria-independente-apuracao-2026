# Roteiro do 2º turno (Auditoria Independente da Apuração 2026 by Jair Lima)

Objetivo: repetir a auditoria do 1º turno com o que faltou lá, principalmente um **relógio próprio de chegada** das seções, e com a coleta feita enquanto a apuração acontece. Data prevista do 2º turno: 25/10/2026 (confirmar no calendário do TSE).

## O que o 1º turno ensinou (e o 2º turno corrige)

| Lacuna no 1º turno | O que fazer no 2º turno |
|---|---|
| Só havia o `hr` do `aux.json`, que não é hora de chegada confiável para ~743 seções | Rodar `monitor_chegada.py` a noite toda: grava o instante UTC em que NÓS vimos cada seção publicada e a curva do resultado oficial a cada minuto |
| Pausa do painel só reconstruída depois, por vídeo e por `hr` | A curva oficial (`curva_oficial.csv`) mostra pausas em tempo real, com `dg/hg` (geração do arquivo) e o instante da consulta |
| Arquivos de seções que davam 404 e só apareciam depois, descobertos por acaso | O monitor registra o primeiro instante em que o índice mostra cada seção; depois, re-tentar os 404 por 48 h |
| Coleta tardia (05/10 à tarde), com o estado "Recebida" já misturado | Coletar `aux.json` duas vezes: logo após o fim da apuração (madrugada) e 24 h depois, e guardar as duas |
| Pedidos LAI feitos só depois | Já há modelo pronto em `pedidos_lai/`; reaproveitar e mirar nos TREs que atrasaram |

## Passo a passo

### Antes (a partir de 20/10)
1. Descobrir o código do pleito de urnas do 2º turno: `https://resultados.tse.jus.br/oficial/comum/config/ele-c.json`, entrada `ele2026` cuja lista de eleições contém `6258` (Presidente) e, se houver, `6260` (Governador). Provavelmente só aparece perto da eleição.
2. Criar a cópia de scripts: `python segundo_turno\preparar_2turno.py --pleito <código> [--estadual]`. Gera `..\AuditoriaPresidente2026_T2\` com os scripts trocados e um `LEIAME_T2.md` com as constantes do 1º turno a conferir.
3. Testar o monitor por 2 minutos com os dados do 1º turno: `ELEICAO=6257 PLEITO=3220 CICLO=10 python segundo_turno\monitor_chegada.py` (apagar `dados_monitor` depois).

### No dia (a partir das 16h de Brasília, antes de fechar as urnas às 17h)
4. `python segundo_turno\monitor_chegada.py` (deixar aberto; Ctrl+C para parar; retomável). Vai imprimir uma linha por minuto com `dg/hg` e % de seções, e uma linha a cada 3 min com as seções novas.
5. Não rodar nada em paralelo contra o TSE: acima de ~10 conexões vem HTTP 429. O monitor é sequencial e leve.
6. Guardar as notícias do dia (print e link) sobre qualquer pausa ou instabilidade, com horário.

### Depois (madrugada e dia seguinte), na cópia `_T2`, nesta ordem
7. `fase1_congelar.py` (totais oficiais e índices, com SHA-256) e logo `fase2_aux.py` (aux.json). **Guardar uma cópia de `dados/aux.jsonl` como `aux_madrugada.jsonl`** e repetir `fase2_aux.py` 24 h depois sobrescrevendo, para ver as seções que mudam de "Recebida" para "Totalizada".
8. `fase2_bu.py` (BUs), `fase3_parse.py`, `fase4_compara.py` (soma contra o oficial).
9. `fase8_cadeia_todos.py` e `fase9_assinaturas.py` (cadeia de hashes e assinaturas). `fase22_busa_assinatura.py` para as seções do Sistema de Apuração.
10. `fase19_rdv.py` (RDV contra BU, amostra) e `fase21_logs.py` (log das urnas das seções atrasadas, com controle).
11. Cruzar `primeira_vez.csv` do monitor com `hr` do `aux.json`: a diferença `utc_primeira_vez - hr` por seção é o atraso de publicação real. É a tabela que o 1º turno não tinha.
12. Se houver Governador no 2º turno, rodar `fase18_estadual_todas.py` só nas UFs com 2º turno.

### O que adaptar no relatório
- Só 2 candidatos a Presidente: tabelas e página (`relatorio_web/`) precisam de nova versão. O combo de candidatos lê `municipios.json` (12 candidatos); regenerar com `fase17_municipios.py` na cópia.
- Mudar títulos para "2º turno" e as datas. Manter a assinatura (jornalista, perícia, TI) e o aviso de que não é perícia judicial.
- Registrar a semente dos sorteios (2026/2027) ou usar novas, dizendo qual.

## Arquivos do monitor
`segundo_turno/dados_monitor/curva_oficial.csv`, `primeira_vez.csv`, `snapshots/`, `manifesto.jsonl`, `ciclos.log` (ignorados pelo git; o resultado final entra em `resultados/`).
