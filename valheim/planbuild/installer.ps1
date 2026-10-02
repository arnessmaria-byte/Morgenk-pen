# Installerer PlanBuild med avhengigheter i Valheim og legger inn Solnes-tegningene.
# Lim inn hele blokka i PowerShell med Valheim lukket. Endrer ingen eksisterende filer.
& {
  $ErrorActionPreference = 'Stop'
  $ProgressPreference = 'SilentlyContinue'
  [Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12

  $V = "${env:ProgramFiles(x86)}\Steam\steamapps\common\Valheim"
  if (-not (Test-Path "$V\valheim.exe")) { throw "Fant ikke Valheim i $V" }
  if (Get-Process valheim -ErrorAction SilentlyContinue) { throw 'Lukk Valheim først, og lim inn skriptet på nytt.' }
  if ((Test-Path "$V\winhttp.dll") -or (Test-Path "$V\BepInEx")) { throw 'BepInEx ligger der allerede. Stopper uten å endre noe.' }

  $W = "$HOME\valheim-analyse\mods"
  New-Item -ItemType Directory -Force $W | Out-Null
  $pakker = @(
    @{ n = 'denikson/BepInExPack_Valheim/5.4.2351'; h = 'bce631497976a93977ceb08e166712e6c31d15244956f89f17df092a9b62e29f' },
    @{ n = 'ValheimModding/Jotunn/2.30.2';          h = '8aae92da2be0eb6820cd4cf57e2f6c1d6ad0d738d4915966e7c3d7a94e9a9b0f' },
    @{ n = 'ValheimModding/HookGenPatcher/0.0.4';   h = '4f920c9b43d6cd8a808d4f7f6cda5b0fce5930f021e693f2bc034a7c39f6f0e4' },
    @{ n = 'MathiasDecrock/PlanBuild/0.20.0';       h = '79859e5f3989d86e316563a652aa817d5821903fe53ca69b14f89563defaffdd' }
  )
  foreach ($p in $pakker) {
    $navn = $p.n -replace '/', '-'
    $zip = "$W\$navn.zip"
    Invoke-WebRequest "https://thunderstore.io/package/download/$($p.n)/" -OutFile $zip -UseBasicParsing
    if ((Get-FileHash $zip -Algorithm SHA256).Hash -ne $p.h) { throw "Feil sjekksum for $navn. Stopper." }
    Expand-Archive $zip "$W\$navn" -Force
    Write-Host "Lastet ned  $navn"
  }

  $B = "$W\denikson-BepInExPack_Valheim-5.4.2351\BepInExPack_Valheim"
  Copy-Item "$B\winhttp.dll", "$B\doorstop_config.ini", "$B\.doorstop_version" $V
  Copy-Item "$B\BepInEx" $V -Recurse
  New-Item -ItemType Directory -Force "$V\BepInEx\plugins\Jotunn", "$V\BepInEx\patchers", "$V\BepInEx\config\PlanBuild\blueprints" | Out-Null
  Copy-Item "$W\ValheimModding-Jotunn-2.30.2\plugins\*" "$V\BepInEx\plugins\Jotunn"
  Copy-Item "$W\ValheimModding-HookGenPatcher-0.0.4\patchers\BepInEx.MonoMod.HookGenPatcher" "$V\BepInEx\patchers" -Recurse
  Copy-Item "$W\ValheimModding-HookGenPatcher-0.0.4\config\HookGenPatcher.cfg" "$V\BepInEx\config"
  Copy-Item "$W\MathiasDecrock-PlanBuild-0.20.0\plugins\PlanBuild" "$V\BepInEx\plugins" -Recurse
  Write-Host 'Installert  BepInEx, Jotunn, HookGenPatcher og PlanBuild'

  $R = 'https://raw.githubusercontent.com/arnessmaria-byte/Morgenk-pen/claude/valheim-save-analysis-s5y2sa/valheim/planbuild'
  $tegninger = @{
    'Solnes_Kongesalen.blueprint' = 'dd14e3fdf6ac7636d6167e4cea3c453496a4b39108d59d7fa6c2c43c8b6448e3'
    'Solnes_Vestporten.blueprint' = '1d2533a2cf2e0c74ce5c329cd8e856f3f055930e3beac71fb3f3e27101252643'
    'Solnes_Grav22m.blueprint'    = '4d163349d43249dd67d0650082c5fcfaf23e534622d951b67bf221fbe4f753c9'
  }
  foreach ($t in $tegninger.Keys) {
    $f = "$V\BepInEx\config\PlanBuild\blueprints\$t"
    Invoke-WebRequest "$R/$t" -OutFile $f -UseBasicParsing
    if ((Get-FileHash $f -Algorithm SHA256).Hash -ne $tegninger[$t]) { Remove-Item $f; throw "Feil sjekksum for $t" }
    Write-Host "Tegning     $t"
  }
  Write-Host ''
  Write-Host 'Ferdig. Start Valheim fra Steam som vanlig.' -ForegroundColor Green
}
