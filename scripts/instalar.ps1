param([switch]$Demo)
$ErrorActionPreference='Stop'
Set-Location (Split-Path $PSScriptRoot -Parent)
New-Item -ItemType Directory -Force work/tmp | Out-Null
$env:TEMP=(Resolve-Path work/tmp).Path
$env:TMP=$env:TEMP
if(-not(Test-Path .venv/Scripts/python.exe)){
  py -3.14 -m venv .venv
  if($LASTEXITCODE -ne 0){throw 'No se pudo crear el entorno'}
}
$python='.\.venv\Scripts\python.exe'
& $python -m pip install -r requirements.txt
if($LASTEXITCODE -ne 0){throw 'Instalación fallida'}
& $python -m pip check
if($LASTEXITCODE -ne 0){throw 'Dependencias incompatibles'}
& $python scripts/configurar.py
& $python -m alembic upgrade head
if($LASTEXITCODE -ne 0){throw 'Migración fallida'}
& $python -m scripts.preparar
if($Demo){& $python -m scripts.datos_demo}
Write-Host 'Preparación terminada. Para cuenta real: python -m scripts.crear_coordinador; para ejecutar usa el intérprete de .venv.'
