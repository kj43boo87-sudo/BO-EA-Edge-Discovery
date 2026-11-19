[CmdletBinding()]
param(
    [string]$LocalRepo  = "C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery",
    [string]$GDriveRoot = "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告",
    [string]$CommitMsg  = "GSR-2026W48: Record GSR-TKYFIX-002 IS 5-gate PASS_CANDIDATE, One-Shot OOS contract, weekly audit & INDEX v1.2",
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
    foreach ($line in $output) {
        Write-Host $line
    }
    if ($code -ne 0) {
        throw "git $($GitArgs -join ' ') failed with exit code $code"
    }
}

Write-Host "=== [GSR-2026W48] Pre-flight Check ===" -ForegroundColor Cyan
if (-not (Test-Path -LiteralPath (Join-Path $LocalRepo ".git"))) {
    throw ".git directory not found in $LocalRepo"
}

$localGsrDir = Join-Path $LocalRepo "Gemini側必勝調査報告"
if (-not (Test-Path -LiteralPath $localGsrDir)) {
    New-Item -ItemType Directory -Path $localGsrDir -Force | Out-Null
}

# --- Step 1: Pull W48 lightweight Stage 1-3 files from GDrive -> Local Gemini側必勝調査報告 ---
Write-Host "=== [Step 1/3] Pull Lightweight Assets (GDrive -> Local Repo, Excluding Heavy CSV/ZIP/gdoc) ===" -ForegroundColor Cyan
if (Test-Path -LiteralPath $GDriveRoot) {
    $pullArgs = @(
        $GDriveRoot,
        $localGsrDir,
        "/E", "/XO", "/R:2", "/W:2",
        "/XD", ".git", ".venv", "__pycache__", "raw_data", "downloads",
        "/XF", "*.zip", "*.7z", "*.gdoc", "*.gsheet", "*.gslides", "*M1-No Session*.csv", "*opportunity_ledger*.csv", "*row_level*.csv", "*full_rows*.csv", "*all_trades_raw*.csv"
    )
    if ($DryRun) { $pullArgs += "/L" }
    $prevPref = $ErrorActionPreference; $ErrorActionPreference = "Continue"
    & robocopy @pullArgs | Out-Null
    $rc = $LASTEXITCODE
    $ErrorActionPreference = $prevPref
    if ($rc -ge 8) { throw "Robocopy (Pull) failed with exit code $rc" }
    Write-Host "Pull completed (robocopy exit code: $rc)." -ForegroundColor Green
}

# --- Step 2: Canonical SHA256 Spot Check ---
Write-Host "=== [Step 2/3] Canonical SHA256 Spot Check ===" -ForegroundColor Cyan
$expectedHashes = @{
    "MASTER_DIRECTOR_ROLE_PROMPT_v1.2.md"                    = "0caca9b9759cc28dfad5a50ef3952f2fac9b868d933b68b11d5592b36345dae9"
    "profile_is_market_structure_gsr_2026w48_v1_0.py"        = "2b2c6f7201f23ac1ec0f886468a8727355d423d51a3c07034e60671edf18603d"
    "gsr_2026w48_is_tkyfix002_verifier_v1_0.py"              = "74f079f670a83cd0202ffb2b4e7e0057a1497d81884d248233b4c9f4d85a0669"
    "is_standalone_and_ablation_summary_gsr_2026w48.csv"     = "d548e3daa590ed876d71548b224c084271508acc1b090a98e97d7c869defd7c7"
    "is_non_cumulative_marginals_and_yearly_gsr_2026w48.csv" = "b213a8ee36fad174c3d0496e531777b8c30ce6648164a1d766560d4c7878236d"
    "spark_audit_handover_manifest_gsr_2026w48.json"         = "3b29debe08aa16dd8816ace61150a79b2f99373c21c467e397a18756f78f7746"
    "GSR-2026W48_Stage2_IS_Report.md"                        = "35d0669cc2b605405706ed259ef5cd0c7a059ccabba8745907cb5b09596169e7"
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
        Write-Host "[SKIP] $name not found locally yet (will be synced on non-DryRun)" -ForegroundColor DarkYellow
    }
}

# --- Step 3: Stage 1 Mirror (Local Gemini側必勝調査報告 -> GDrive) & Stage 2 Git Push ---
Write-Host "=== [Step 3/3] Mirror to GDrive & Git Add / Commit / Push ===" -ForegroundColor Cyan
if (Test-Path -LiteralPath $GDriveRoot) {
    $pushArgs = @(
        $localGsrDir,
        $GDriveRoot,
        "/E", "/XO", "/R:2", "/W:2",
        "/XD", ".git", ".venv", "__pycache__", "raw_data", "downloads",
        "/XF", "*.zip", "*.7z", "*.gdoc", "*.gsheet", "*.gslides", "*M1-No Session*.csv", "*opportunity_ledger*.csv", "*row_level*.csv", "*full_rows*.csv", "*all_trades_raw*.csv"
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

    Write-Host "--- git status --short ---" -ForegroundColor Cyan
    Invoke-GitSafe @("status", "--short")

    if ($DryRun) {
        Write-Host "[DryRun] Completed safely. Run without -DryRun to sync and push to origin/main." -ForegroundColor Yellow
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
        Write-Host "Successfully pushed GSR-2026W48 canonical assets to origin/main." -ForegroundColor Green
    }
} finally {
    Pop-Location
}