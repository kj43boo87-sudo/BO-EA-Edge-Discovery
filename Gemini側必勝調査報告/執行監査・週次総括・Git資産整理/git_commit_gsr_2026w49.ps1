[CmdletBinding()]
param(
    [string]$LocalRepo  = "C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery",
    [string]$GDriveRoot = "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告",
    [string]$CommitMsg  = "GSR-2026W49: Record Track A One-Shot OOS REJECTED, Track B Multi-Fix audit & INDEX v1.2",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

function Invoke-GitSafe {
    param(
        [Parameter(Mandatory = $true)]
        [AllowEmptyString()]
        [string[]]$GitArgs
    )
    $prevPref = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    try {
        $output = & git @GitArgs 2>&1
        $code = $LASTEXITCODE
    } finally {
        $ErrorActionPreference = $prevPref
    }
    foreach ($line in $output) { Write-Host $line }
    if ($code -ne 0) { throw "git $($GitArgs -join ' ') failed with exit code $code" }
}

if (-not (Test-Path -LiteralPath (Join-Path $LocalRepo ".git"))) {
    throw ".git directory not found in $LocalRepo"
}

$localGsrDir = Join-Path $LocalRepo "Gemini側必勝調査報告"
if (-not (Test-Path -LiteralPath $localGsrDir)) {
    New-Item -ItemType Directory -Path $localGsrDir -Force | Out-Null
}

Write-Host "=== [Step 1/3] Pull Lightweight Assets (GDrive -> Local Repo, Excluding Heavy CSV/ZIP/gdoc) ===" -ForegroundColor Cyan
if (Test-Path -LiteralPath $GDriveRoot) {
    $pullArgs = @(
        $GDriveRoot, $localGsrDir, "/E", "/XO", "/R:2", "/W:2",
        "/XD", ".git", ".venv", "__pycache__", "raw_data", "downloads",
        "/XF", "*.zip", "*.7z", "*.gdoc", "*.gsheet", "*.gslides",
               "*M1-No Session*.csv", "*opportunity_ledger*.csv", "*row_level*.csv", "*full_rows*.csv", "*all_trades_raw*.csv"
    )
    if ($DryRun) { $pullArgs += "/L" }
    $prevPref = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    & robocopy @pullArgs | Out-Null
    $rc = $LASTEXITCODE
    $ErrorActionPreference = $prevPref
    if ($rc -ge 8) { throw "Robocopy (Pull) failed with exit code $rc" }
    Write-Host "Pull completed (robocopy exit code: $rc)." -ForegroundColor Green
}

Write-Host "=== [Step 2/3] Canonical SHA256 Spot Check (GSR-2026W49) ===" -ForegroundColor Cyan
$expectedHashes = @{
    "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"                    = "0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9"
    "profile_market_structure_gsr_2026w49_v1_0.py"           = "f4609b51f933c21bbf8db3e2f54095ee728cd6571d805b3df04531c386fb364b"
    "gsr_2026w49_stage2_oos_and_multifix_verifier_v1_0.py"   = "2b9c5017abd9f723536f05bd4f362888642af6b9cc53e0e107a412407a9ca479"
    "spark_audit_handover_manifest_gsr_2026w49.json"         = "e50c86b03a3acd954175101297495378e3e541352a909b1b7d5e3ff87aed5354"
    "oos_tkyfix002_standalone_and_diagnostics_gsr_2026w49.csv" = "1483b04b0f6f5e2c09e6d9aa36b5829534eee6d6385eff560f52acbf294190f1"
    "is_multifix_standalone_and_ablation_gsr_2026w49.csv"    = "63e602fbe2b21321d85adb299299db82b0319ab33262c81efbf564b4e2884a8a"
    "is_multifix_disjoint_slices_and_yearly_gsr_2026w49.csv" = "80cad076b09fb835356f838074307e1295edaf4e95729eb9d80534528f5ab164"
}
foreach ($name in $expectedHashes.Keys) {
    $found = Get-ChildItem -LiteralPath $LocalRepo -Filter $name -Recurse -File -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($null -ne $found) {
        $actual = (Get-FileHash -LiteralPath $found.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
        if ($actual -eq $expectedHashes[$name]) {
            Write-Host "[OK]   $name ($($actual.Substring(0,12))...)" -ForegroundColor Green
        } else {
            Write-Warning "[DIFF] $name expected=$($expectedHashes[$name].Substring(0,12))... actual=$($actual.Substring(0,12))..."
        }
    } else {
        Write-Host "[SKIP] $name not found locally yet" -ForegroundColor DarkYellow
    }
}

Write-Host "=== [Step 3/3] Mirror to GDrive & Git Add / Commit / Push ===" -ForegroundColor Cyan
if (Test-Path -LiteralPath $GDriveRoot) {
    $pushArgs = @(
        $localGsrDir, $GDriveRoot, "/E", "/XO", "/R:2", "/W:2",
        "/XD", ".git", ".venv", "__pycache__", "raw_data", "downloads",
        "/XF", "*.zip", "*.7z", "*.gdoc", "*.gsheet", "*.gslides",
               "*M1-No Session*.csv", "*opportunity_ledger*.csv", "*row_level*.csv", "*full_rows*.csv", "*all_trades_raw*.csv"
    )
    if ($DryRun) { $pushArgs += "/L" }
    $prevPref = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    & robocopy @pushArgs | Out-Null
    $rc2 = $LASTEXITCODE
    $ErrorActionPreference = $prevPref
    if ($rc2 -ge 8) { throw "Robocopy (Mirror) failed with exit code $rc2" }
    Write-Host "GDrive 1-to-1 mirror completed (robocopy exit code: $rc2)." -ForegroundColor Green
}

Push-Location -LiteralPath $LocalRepo
try {
    Invoke-GitSafe @("config", "core.pager", "cat")
    Invoke-GitSafe @("config", "core.quotepath", "false")
    Invoke-GitSafe @("config", "core.autocrlf", "false")
    Invoke-GitSafe @("config", "core.safecrlf", "false")
    Invoke-GitSafe @("status", "--short")

    if ($DryRun) {
        Write-Host "[DryRun] Completed safely." -ForegroundColor Yellow
        return
    }

    Invoke-GitSafe @("add", "-A")
    $stagedHeavy = (& git diff --cached --name-only 2>$null) | Where-Object {
        $_ -match "\.(zip|7z|gdoc|gsheet|gslides)$" -or $_ -match "M1-No Session" -or $_ -match "opportunity_ledger"
    }
    if ($stagedHeavy) {
        Invoke-GitSafe @("reset", "HEAD")
        throw "Blocked commit: heavy/excluded files were staged: $($stagedHeavy -join ', ')"
    }

    $pending = & git status --porcelain
    if ([string]::IsNullOrWhiteSpace(($pending -join ""))) {
        Write-Host "No changes to commit. Working tree clean." -ForegroundColor Green
    } else {
        Invoke-GitSafe @("commit", "-m", $CommitMsg)
        Invoke-GitSafe @("push", "origin", "main")
        Write-Host "Successfully pushed GSR-2026W49 canonical assets to origin/main." -ForegroundColor Green
    }
} finally {
    Pop-Location
}
