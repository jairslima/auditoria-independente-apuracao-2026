(Get-Process -Id $PID).PriorityClass = 'Idle'
$env:PYTHONUTF8='1'; $env:PROCS='2'; $env:THREADS='6'
$T2='C:\Users\jairs\Claude\AuditoriaPresidente2026_T2'; Set-Location "$T2\scripts"
function Log($m) { "$m $(Get-Date)" | Add-Content "$T2\dados\cadeia6.log" -Encoding utf8 }
foreach ($f in 'fase27b_reprocessa_logs','fase19_rdv','fase28_urna_certificado','fase21b_mensagens','atualiza_relatorio') {
  Log "inicio $f"; python "$f.py" *> "$T2\dados\$f.b.log"; Log "fim $f codigo $LASTEXITCODE"
}
Log 'FIM_CADEIA6'
python C:\Users\jairs\Scripts\telegram_direto.py "[Claude] Auditoria 2o turno`nReprocessamento dos logs com 2 arquivos e do RDV das 29 secoes do exterior terminou. Falta publicar a pagina com os numeros completos."
