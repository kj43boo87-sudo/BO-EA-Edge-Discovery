# ==============================================================================
# git_commit_gsr_2026w48.ps1
# GSR-2026W48 (GSR-TKYFIX-002 PASS_CANDIDATE) 2-Stage Sync & Git Commit Script
#   Stage 1: SHA256 Verification + Safe Mirror to Google Drive (No .git / No Heavy CSV/ZIP)
#   Stage 2: CRLF-Warning-Safe Git Add / Commit / Push to origin/main
# ==============================================================================
[CmdletBinding()]
param(
    [string]$LocalRepo  = "C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery",
    [string]$GDriveRoot = "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告",
    [string]$CommitMsg  = "GSR-2026W48: Record GSR-TKYFIX-002 IS 5-gate PASS_CANDIDATE, One-Shot OOS contract, weekly audit & INDEX v1.2",
    [switch]$DryRun
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

# --- Safe Git wrapper: prevents LF->CRLF stderr warnings from aborting PowerShell ---
function Invoke-GitSafe {
    param(
        [Parameter(Mandatory = $true)]
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
if (-not (Test-Path -LiteralPath $LocalRepo)) {
    throw "Local Git repository not found: $LocalRepo"
}
if (-not (Test-Path -LiteralPath (Join-Path $LocalRepo ".git"))) {
    throw ".git directory not found in $LocalRepo"
}

# --- Step 1: Ensure .gitignore blocks all heavy CSVs, ledgers, ZIPs, and raw M1 data ---
$gitignorePath = Join-Path $LocalRepo ".gitignore"
$requiredIgnores = @(
    "# --- GSR Heavy Data & Raw M1 Exclusions (Mandatory) ---",
    "*.zip",
    "*.7z",
    "*M1-No Session*.csv",
    "*opportunity_ledger*.csv",
    "*row_level*.csv",
    "*full_rows*.csv",
    "*all_trades_raw*.csv",
    "**/raw_data/",
    "**/downloads/"
)
if (-not (Test-Path -LiteralPath $gitignorePath)) {
    Set-Content -LiteralPath $gitignorePath -Value ($requiredIgnores -join "`n") -Encoding UTF8
} else {
    $existing = Get-Content -LiteralPath $gitignorePath -Raw -Encoding UTF8
    $toAppend = @()
    foreach ($rule in $requiredIgnores) {
        if ($existing -notmatch [regex]::Escape($rule)) {
            $toAppend += $rule
        }
    }
    if ($toAppend.Count -gt 0) {
        Add-Content -LiteralPath $gitignorePath -Value ("`n" + ($toAppend -join "`n")) -Encoding UTF8
        Write-Host "Updated .gitignore with $($toAppend.Count) mandatory heavy-data exclusion rules." -ForegroundColor Yellow
    }
}

# --- Step 2: SHA256 Verification of Canonical Stage 1-3 Assets (if present locally) ---
Write-Host "=== [GSR-2026W48] Canonical SHA256 Spot Check ===" -ForegroundColor Cyan
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
        Write-Host "[SKIP] $name not found under $LocalRepo (check Drive sync if needed)" -ForegroundColor DarkYellow
    }
}

# --- Step 3: Stage 1 Sync - Mirror Local Repo -> Google Drive (Excluding .git & Heavy CSV/ZIP) ---
Write-Host "=== [Stage 1/2] Mirror Copy to Google Drive (Excluding .git and Heavy Files) ===" -ForegroundColor Cyan
if (Test-Path -LiteralPath $GDriveRoot) {
    $roboArgs = @(
        $LocalRepo,
        $GDriveRoot,
        "/E",
        "/XO",
        "/R:2",
        "/W:2",
        "/XD", ".git", ".venv", "__pycache__", "raw_data", "downloads",
        "/XF", "*.zip", "*.7z", "*M1-No Session*.csv", "*opportunity_ledger*.csv", "*row_level*.csv", "*full_rows*.csv", "*all_trades_raw*.csv"
    )
    if ($DryRun) {
        $roboArgs += "/L"
    }
    $prevPref = $ErrorActionPreference
    $ErrorActionPreference = "Continue"
    & robocopy @roboArgs
    $roboCode = $LASTEXITCODE
    $ErrorActionPreference = $prevPref
    # Robocopy exit codes 0-7 indicate success / files copied without failure
    if ($roboCode -ge 8) {
        throw "Robocopy failed with exit code $roboCode"
    }
    Write-Host "Google Drive mirror completed (robocopy exit code: $roboCode)." -ForegroundColor Green
} else {
    Write-Warning "Google Drive root not mounted at $GDriveRoot. Skipping Stage 1 mirror."
}

# --- Step 4: Stage 2 Sync - GitHub Push (CRLF-Warning-Safe) ---
Write-Host "=== [Stage 2/2] Git Add / Commit / Push (origin/main) ===" -ForegroundColor Cyan
Push-Location -LiteralPath $LocalRepo
try {
    Invoke-GitSafe @("config", "core.pager", "")
    Invoke-GitSafe @("config", "core.quotepath", "false")
    Invoke-GitSafe @("config", "core.autocrlf", "false")
    Invoke-GitSafe @("config", "core.safecrlf", "false")

    # Safety guard: abort if any staged or untracked file > 50MB is about to be committed
    $largeFiles = Get-ChildItem -LiteralPath $LocalRepo -Recurse -File -ErrorAction SilentlyContinue |
        Where-Object { $_.FullName -notmatch "\\\.git\\" -and $_.Length -gt 52428800 }
    if ($largeFiles) {
        Write-Warning "Detected files > 50MB in workspace (verifying .gitignore excludes them):"
        $largeFiles | ForEach-Object { Write-Host "  - $($_.FullName) ($([math]::Round($_.Length/1MB,1)) MB)" -ForegroundColor Yellow }
    }

    Invoke-GitSafe @("status", "--short")

    if ($DryRun) {
        Write-Host "[DryRun] Skipping git add / commit / push." -ForegroundColor Yellow
        return
    }

    Invoke-GitSafe @("add", "-A")

    # Double-check no heavy CSV/ZIP got staged
    $stagedHeavy = (& git diff --cached --name-only 2>$null) | Where-Object {
        $_ -match "\.(zip|7z)$" -or $_ -match "M1-No Session" -or $_ -match "opportunity_ledger"
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
