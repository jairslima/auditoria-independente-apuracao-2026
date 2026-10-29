# Aviso de hora em hora no Telegram com o andamento da verificacao completa do 2o turno e atualizacao do relatorio.
# Auditoria Independente da Apuracao 2026 by Jair Lima
(Get-Process -Id $PID).PriorityClass = 'Idle'
$T2 = 'C:\Users\jairs\Claude\AuditoriaPresidente2026_T2'
Set-Location "$T2\scripts"
$env:PYTHONUTF8 = '1'
while ($true) {
  Start-Sleep 3600
  $log = Get-Content "$T2\dados\cadeia4.log" -ErrorAction SilentlyContinue
  if ($log -match 'FIM_CADEIA') { break }
  try { python atualiza_relatorio.py | Out-Null } catch {}
  $msg = python progresso.py
  try { python C:\Users\jairs\Scripts\telegram_direto.py "[Claude] Auditoria 2o turno, andamento`n$msg" | Out-Null } catch {}
}
