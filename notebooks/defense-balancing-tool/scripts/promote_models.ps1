param(
  [Parameter(Mandatory=$true)]
  [string]$Tag
)

$ErrorActionPreference = "Stop"

function Copy-Required([string]$src, [string]$dst) {
  if (-not (Test-Path $src)) {
    throw "[promote] missing: $src"
  }
  Copy-Item $src $dst -Force
}

Copy-Required "models\rf_full_$Tag.joblib"    "models\rf_full_current.joblib"
Copy-Required "models\rf_full_$Tag.json"      "models\rf_full_current.json"

Copy-Required "models\rf_no_perk_$Tag.joblib" "models\rf_no_perk_current.joblib"
Copy-Required "models\rf_no_perk_$Tag.json"   "models\rf_no_perk_current.json"

Copy-Required "models\rf_no_adv_$Tag.joblib"  "models\rf_no_adv_current.joblib"
Copy-Required "models\rf_no_adv_$Tag.json"    "models\rf_no_adv_current.json"

Set-Content "models\current_tag.txt" $Tag -Encoding UTF8

Write-Host "[OK] promoted -> current (tag=$Tag)"
