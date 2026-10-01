# Henter siste versjon av Solnes-tegningene til PlanBuild og overskriver de gamle.
& {
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12
  $D = "${env:ProgramFiles(x86)}\Steam\steamapps\common\Valheim\BepInEx\config\PlanBuild\blueprints"
  if (-not (Test-Path $D)) { throw "Fant ikke $D. Kjør installer.ps1 først." }
  $R = 'https://raw.githubusercontent.com/arnessmaria-byte/Morgenk-pen/claude/valheim-save-analysis-s5y2sa/valheim/planbuild'
  $tegninger = @{
    'Solnes_Kongesalen.blueprint' = 'dd14e3fdf6ac7636d6167e4cea3c453496a4b39108d59d7fa6c2c43c8b6448e3'
    'Solnes_Vestporten.blueprint' = '1d2533a2cf2e0c74ce5c329cd8e856f3f055930e3beac71fb3f3e27101252643'
    'Solnes_Grav22m.blueprint'    = '4d163349d43249dd67d0650082c5fcfaf23e534622d951b67bf221fbe4f753c9'
  }
  foreach ($t in $tegninger.Keys) {
    $tmp = "$env:TEMP\$t"
    Invoke-WebRequest "$R/$t" -OutFile $tmp -UseBasicParsing
    if ((Get-FileHash $tmp -Algorithm SHA256).Hash -ne $tegninger[$t]) { Remove-Item $tmp; throw "Feil sjekksum for $t" }
    Move-Item $tmp "$D\$t" -Force
    Write-Host "Oppdatert  $t"
  }
  Write-Host ''
  Write-Host 'Ferdig. Start Valheim på nytt for å laste de nye tegningene.' -ForegroundColor Green
}
