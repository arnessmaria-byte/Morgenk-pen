# Bytter PlanBuild 0.18.8 (ShelledGhost) ut med 0.20.0 (MathiasDecrock), som retter feilen der
# planer på bakken står som «Not enough support». Lim inn med Valheim lukket.
& {
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

  $V = "${env:ProgramFiles(x86)}\Steam\steamapps\common\Valheim"
  $P = "$V\BepInEx\plugins\PlanBuild"
  if (-not (Test-Path "$P\PlanBuild.dll")) { throw "Fant ikke PlanBuild i $P" }
  if (Get-Process valheim -ErrorAction SilentlyContinue) { throw 'Lukk Valheim først, og lim inn skriptet på nytt.' }

  $W = "$HOME\valheim-analyse\mods"
  New-Item -ItemType Directory -Force $W | Out-Null
  $zip = "$W\MathiasDecrock-PlanBuild-0.20.0.zip"
  Invoke-WebRequest 'https://thunderstore.io/package/download/MathiasDecrock/PlanBuild/0.20.0/' -OutFile $zip -UseBasicParsing
  if ((Get-FileHash $zip -Algorithm SHA256).Hash -ne '79859e5f3989d86e316563a652aa817d5821903fe53ca69b14f89563defaffdd') { throw 'Feil sjekksum for PlanBuild 0.20.0. Stopper.' }
  Expand-Archive $zip "$W\MathiasDecrock-PlanBuild-0.20.0" -Force

  $B = "$W\PlanBuild-0.18.8-backup"
  if (Test-Path $B) { Remove-Item $B -Recurse -Force }
  Move-Item $P $B
  Copy-Item "$W\MathiasDecrock-PlanBuild-0.20.0\plugins\PlanBuild" "$V\BepInEx\plugins" -Recurse
  Write-Host 'Oppdatert  PlanBuild 0.18.8 -> 0.20.0 (den gamle ligger i valheim-analyse\mods\PlanBuild-0.18.8-backup)'
  Write-Host ''
  Write-Host 'Ferdig. Start Valheim fra Steam som vanlig.' -ForegroundColor Green
}
