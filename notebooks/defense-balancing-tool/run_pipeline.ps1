[CmdletBinding(PositionalBinding=$false)]
param(
  [Parameter(ValueFromRemainingArguments = $true)]
  [object[]] $RemainingArgs
)

$root = $PSScriptRoot
$target = Join-Path $root "scripts\run_pipeline.ps1"

if (-not (Test-Path $target)) {
  Write-Error "Target script not found: $target"
  exit 1
}

Push-Location $root
try {
  & $target @RemainingArgs
} finally {
  Pop-Location
}
