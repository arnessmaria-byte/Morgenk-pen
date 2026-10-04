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
    'Solnes_Stabburet.blueprint'  = '3a6e0bff79df83668d1116f7f52ab03a6d6dfde8de88d1dab1a3eb6423285233'
    'Solnes_Mjodstua.blueprint'   = '6f0703f0b6081dd748c6c3ee460f16df264824a209a4ba8a6521eef0601b4f16'
    'Solnes_Tingstua.blueprint'   = 'ae194c261b54ac5126faea55c93c388bbb26a82389cfc63943564d61356b6116'
    'Solnes_Lysthuset.blueprint'  = '63f538e6e326d100e58622e67737c7e4246ef0667a764ee89ffb51eeac2ea0e0'
    'Solnes_Akerbed.blueprint'   = '4cb838d4319c8b10532badc824025e315de05c8a7c3df16c9fb98522172a140f'
    'Solnes_Bigarden.blueprint'  = '042b68777f6f5288ba14395410cec60f1574f83bfdb41ba40229520ae108b47a'
    'Solnes_Folden.blueprint'    = 'bc211279481924a41cf1766200f96b880e8bc3f66efcd2135a19ac1f91ce7c8b'
    'Solnes_Kongebordet.blueprint' = '00a341b7735d7eda7da7f446a4a8abd3b9c14893afdc4fd3bcaa25aa04006689'
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
