@echo off
rem Legger verdenene Bossrush og BossrushViking (seed HHcLC5acQt) inn i Valheim.
rem Dobbeltklikk filen. Ingenting annet trengs.
powershell -NoProfile -ExecutionPolicy Bypass -Command ^
  "$d = Join-Path $env:USERPROFILE 'AppData\LocalLow\IronGate\Valheim\worlds_local';" ^
  "$w = @{ 'Bossrush' = 'MQAAACkAAAAIQm9zc3J1c2gKSEhjTEM1YWNRdEzWxBHuRKhkAAAAAAIAAAAAAAAAAAAAAAA='; 'BossrushViking' = 'GQEAACkAAAAOQm9zc3J1c2hWaWtpbmcKSEhjTEM1YWNRdEzWxBHpW8/1/////wIAAAAACgAAAA9wbGF5ZXJkYW1hZ2UgNzAPZW5lbXlkYW1hZ2UgMjAwEmVuZW15c3BlZWRzaXplIDEyMBRlbmVteWxldmVsdXByYXRlIDE0MAxldmVudHJhdGUgNjAFbm9tYXAQZGVhdGhkZWxldGVpdGVtcxBkZWF0aHNraWxsc3Jlc2V0DW5vYm9zc3BvcnRhbHNWcHJlc2V0IGNvbWJhdF92ZXJ5aGFyZDpkZWF0aHBlbmFsdHlfaGFyZGNvcmU6cmVzb3VyY2VzX2RlZmF1bHQ6cmFpZHNfbW9yZTpwb3J0YWxzX2hhcmQAAAAA' };" ^
  "foreach ($n in $w.Keys) { $f = Join-Path $d $n; if (Test-Path $f) { Write-Host ($n + ' finnes allerede, hopper over.'); continue };" ^
  "  New-Item -ItemType Directory -Force -Path $f | Out-Null;" ^
  "  [IO.File]::WriteAllBytes((Join-Path $f '_main.0.fwl2'), [Convert]::FromBase64String($w[$n])); Write-Host ('La inn ' + $n) }"
echo.
echo Ferdig. Start Valheim og velg Bossrush eller BossrushViking.
pause
