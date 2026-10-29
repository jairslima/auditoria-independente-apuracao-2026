# Cadeia da verificacao completa do 2o turno (sem amostragem), em prioridade Idle.
# Auditoria Independente da Apuracao 2026 by Jair Lima
(Get-Process -Id $PID).PriorityClass = 'Idle'
$T2 = 'C:\Users\jairs\Claude\AuditoriaPresidente2026_T2'
Set-Location "$T2\scripts"
$env:PYTHONUTF8 = '1'
function Log($m) { "$m $(Get-Date)" | Add-Content "$T2\dados\cadeia4.log" -Encoding utf8 }
function Avisa($m) { try { python C:\Users\jairs\Scripts\telegram_direto.py "[Claude] Auditoria 2o turno`n$m" | Out-Null } catch { Log "falha no aviso: $_" } }
function Relatorio($abrir) { try { if ($abrir) { python atualiza_relatorio.py --abrir | Out-Null } else { python atualiza_relatorio.py | Out-Null } } catch { Log "falha ao atualizar relatorio: $_" } }
function Etapa($nome, $script) {
  Log "inicio $nome"
  python $script *> "$T2\dados\$nome.log"
  $cod = $LASTEXITCODE
  Log "fim $nome codigo $cod"
  return $cod
}
function Fim($nome, $cod) {
  $res = if ($cod -eq 0) { 'concluída' } else { "TERMINOU COM ERRO (código $cod), ver dados\$nome.log" }
  Relatorio $true
  Avisa "Etapa $nome $res.`n$(python progresso.py)"
}

Log 'inicio cadeia4'
# 1) segunda copia do aux.json (27/10) e comparacao com a de 26/10 manha
$c = Etapa 'fase2_aux_24h' 'fase2_aux_24h.py'
if ($c -eq 0) { $c = Etapa 'fase26_compara_aux' 'fase26_compara_aux.py' }
Fim 'fase26_compara_aux' $c
# 2) municipios (Presidente)
$c = Etapa 'fase17_municipios' 'fase17_municipios.py'
Fim 'fase17_municipios' $c
# 3) RDV completo e logs de todas as urnas, em paralelo (2 + 6 conexoes, abaixo do limite do TSE)
python prepara_plano_rdv.py *> "$T2\dados\prepara_plano_rdv.log"
$env:PROCS = '2'; $env:THREADS = '6'
Log 'inicio fase19_rdv'; Log 'inicio fase27_logs_todas'
$p1 = Start-Process python -ArgumentList 'fase19_rdv.py' -NoNewWindow -PassThru -RedirectStandardOutput "$T2\dados\fase19_rdv.log" -RedirectStandardError "$T2\dados\fase19_rdv.err"
$p2 = Start-Process python -ArgumentList 'fase27_logs_todas.py' -NoNewWindow -PassThru -RedirectStandardOutput "$T2\dados\fase27_logs_todas.log" -RedirectStandardError "$T2\dados\fase27_logs_todas.err"
$fim1 = $false; $fim2 = $false
while (-not ($fim1 -and $fim2)) {
  Start-Sleep 30
  if (-not $fim1 -and $p1.HasExited) { $fim1 = $true; Log "fim fase19_rdv codigo $($p1.ExitCode)"; Fim 'fase19_rdv' $p1.ExitCode }
  if (-not $fim2 -and $p2.HasExited) { $fim2 = $true; Log "fim fase27_logs_todas codigo $($p2.ExitCode)"; Fim 'fase27_logs_todas' $p2.ExitCode }
}
# 4) numero da urna no log x certificado
$c = Etapa 'fase28_urna_certificado' 'fase28_urna_certificado.py'
Fim 'fase28_urna_certificado' $c
Log 'FIM_CADEIA'
Avisa "Todas as etapas terminaram. Falta a revisão final do texto do relatório (RELATORIO_2TURNO.md), que faço quando você voltar.`n$(python progresso.py)"
