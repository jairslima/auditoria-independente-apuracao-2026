(Get-Process -Id $PID).PriorityClass = 'Idle'
$env:PYTHONUTF8='1'
Set-Location 'C:\Users\jairs\Claude\AuditoriaPresidente2026_T2\scripts'
python fase29c_transferencias.py *> 'C:\Users\jairs\Claude\AuditoriaPresidente2026_T2\dados\fase29c.log'
