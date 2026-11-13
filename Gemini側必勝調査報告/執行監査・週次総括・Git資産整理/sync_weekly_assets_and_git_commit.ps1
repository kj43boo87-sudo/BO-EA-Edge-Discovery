# ==============================================================================
# BO・EA Edge Discovery — 週次プログラム資産整理・INDEX.md反映・Git正本登録スクリプト
# 保管先: G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\sync_weekly_assets_and_git_commit.ps1
# 準拠規約: プログラム資産管理手順.txt（実ソースSHA256再計算・旧版保持・大容量CSV除外）
# ==============================================================================
[CmdletBinding()]
param(
    [switch]$CommitToGit = $true
)

$ErrorActionPreference = "Stop"

# 1. 3工程フォルダとGit正本リポジトリルートの特定
$ReportRoot = "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告"
$Stage1Dir  = Join-Path $ReportRoot "トレード手法の市場調査＆データ点検"
$Stage2Dir  = Join-Path $ReportRoot "機会台帳突合＆IS統計・Plateau検証"
$Stage3Dir  = Join-Path $ReportRoot "執行監査・週次総括・Git資産整理"

$CandidateRepoRoots = @(
    "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Codex\BO-EA-Edge-Discovery",
    "G:\マイドライブ\AIトレーサビリティ\Codex\BO-EA-Edge-Discovery",
    "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery"
)
$RepoRoot = $CandidateRepoRoots | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $RepoRoot) {
    throw "Google Drive 内のプロジェクトルートが見つかりません。G:ドライブの同期状態を確認してください。"
}
Write-Host "[1/6] Project Root     : $RepoRoot" -ForegroundColor Cyan
Write-Host "      Stage 1 Folder   : $Stage1Dir"
Write-Host "      Stage 2 Folder   : $Stage2Dir"
Write-Host "      Stage 3 Folder   : $Stage3Dir"

# 2. 今週の検証スクリプト(.py)・ドキュメント(.md)の実ソースSHA256再計算と照合（手順書 規則2・6）
$ExpectedAssets = @(
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_2015_2021_v1_2.py"
        ExpectedSha256 = "a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb"
        DestRelDir = "04_Python_Research\Stage1_Market_Survey"
        Status = "静的確認済み（v1.2.0 引数なし自動探索対応）"
    },
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_2015_2021.py"
        ExpectedSha256 = "e37a9e62626d76ae90b7013de9842bcca007906cabad4b7e5afe0ca08d0111ce"
        DestRelDir = "04_Python_Research\Stage1_Market_Survey\archive"
        Status = "旧版保持（v1.1.0）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "bo_eur_005_is_plateau_verifier.py"
        ExpectedSha256 = "7c125ea7c02db45a2e2af779f9dc7af530639cf900a3109296667207689703a9"
        DestRelDir = "04_Python_Research\BO-EUR-005"
        Status = "実行確認済み（v2.4 正規SHA256統一版）"
    },
    @{
        Stage = "Stage2/3"
        Path  = Join-Path $Stage3Dir "BO-EUR-005_decision.md"
        FallbackPath = Join-Path $Stage2Dir "BO-EUR-005_decision.md"
        ExpectedSha256 = "2d0e2e05b8dcd86c2993b2e0fea0f8c8505d609e654a5110ce49e7882c255109"
        DestRelDir = "01_Plans_and_Decisions"
        Status = "確定決定記録（ISゲート棄却・凍結）"
    },
    @{
        Stage = "Stage2/3"
        Path  = Join-Path $Stage3Dir "BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md"
        FallbackPath = Join-Path $Stage2Dir "BO-EUR-005_Spark_Audit_and_Handover_Log_2026-11-05.md"
        ExpectedSha256 = "6c663ad984c4f68f998a8a8ad0881f8787d082c7f321b2dc54bfe765a5a24fad"
        DestRelDir = "01_Plans_and_Decisions"
        Status = "Spark独立監査・執行監査統合ログ"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "DECISION_TEMPLATE.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions\templates"
        Status = "公式TRACE・decision.md標準テンプレート"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "WEEKLY_EXECUTIVE_AUDIT_AND_HANDOVER_20261106.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions\weekly_audits"
        Status = "2026-11-06 週次総括・最終5ゲート監査報告"
    }
)

Write-Host "`n[2/6] Verifying live SHA256 hashes of scripts (.py) and documents (.md)..." -ForegroundColor Cyan
$VerifiedRecords = @()

foreach ($item in $ExpectedAssets) {
    $srcPath = $item.Path
    if ((-not (Test-Path $srcPath)) -and $item.FallbackPath -and (Test-Path $item.FallbackPath)) {
        $srcPath = $item.FallbackPath
    }
    if (-not (Test-Path $srcPath)) {
        Write-Warning "File not found yet (skipping): $($item.Path)"
        continue
    }
    $actualHash = (Get-FileHash -Path $srcPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $fileInfo   = Get-Item -Path $srcPath
    $hashMatch  = if ($item.ExpectedSha256) { $actualHash -eq $item.ExpectedSha256 } else { $true }

    if (-not $hashMatch) {
        Write-Warning "SHA256 mismatch on $($fileInfo.Name): expected $($item.ExpectedSha256), got $actualHash"
    } else {
        Write-Host "  [OK] $($fileInfo.Name) ($($fileInfo.Length) bytes) SHA256=$($actualHash.Substring(0,16))..." -ForegroundColor Green
    }

    # Copy to canonical repository subfolder (preserving existing files if different)
    $destDir = Join-Path $RepoRoot $item.DestRelDir
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    $destFile = Join-Path $destDir $fileInfo.Name
    if ((Test-Path $destFile) -and ((Get-FileHash $destFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $actualHash)) {
        $backupName = "$($fileInfo.BaseName)_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')$($fileInfo.Extension)"
        Copy-Item -Path $destFile -Destination (Join-Path $destDir $backupName) -Force
        Write-Host "  [Preserved old version] -> $backupName" -ForegroundColor Yellow
    }
    Copy-Item -Path $srcPath -Destination $destFile -Force

    $VerifiedRecords += [PSCustomObject]@{
        Stage        = $item.Stage
        FileName     = $fileInfo.Name
        RelRepoPath  = (Join-Path $item.DestRelDir $fileInfo.Name).Replace('\', '/')
        SourcePath   = $srcPath.Replace('\', '/')
        Bytes        = $fileInfo.Length
        LastModified = $fileInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        SHA256       = $actualHash
        Status       = $item.Status
    }
}

# 3. 小容量の集計証跡（マニフェストJSON・サマリーCSVのみ）をコピーし、大容量CSVは除外
Write-Host "`n[3/6] Copying compact summary manifests (excluding large raw/outcomes/grid CSVs)..." -ForegroundColor Cyan
$Stage2OutDir = Join-Path $Stage2Dir "output_is_plateau_20261104_173018"
$DestTestDir  = Join-Path $RepoRoot "07_Tests_and_Backtests\BO-EUR-005\output_is_plateau_20261104_173018"
if (Test-Path $Stage2OutDir) {
    New-Item -ItemType Directory -Force -Path $DestTestDir | Out-Null
    $CompactFiles = @(
        "spark_audit_handover_manifest.json",
        "is_standalone_summary.csv",
        "is_paired_summary.csv",
        "is_yearly_breakdown.csv"
    )
    foreach ($cf in $CompactFiles) {
        $cfPath = Join-Path $Stage2OutDir $cf
        if (Test-Path $cfPath) {
            Copy-Item -Path $cfPath -Destination (Join-Path $DestTestDir $cf) -Force
            Write-Host "  [Copied summary] $cf" -ForegroundColor Green
        }
    }
}

# 4. ルート INDEX.md への非破壊追記（手編集内容を消さず、重複追記を防止）
Write-Host "`n[4/6] Updating root INDEX.md with verified SHA256 entries..." -ForegroundColor Cyan
$RootIndexPath = Join-Path $RepoRoot "INDEX.md"
$SectionMarker = "## 週次検証・監査資産追記ログ（2026-11-06：BO-EUR-005最終棄却＆3工程パイプライン整備）"

$TableRows = $VerifiedRecords | ForEach-Object {
    "| `$($_.Stage)` | [`$($_.FileName)`]($($_.RelRepoPath)) | $($_.Status) | $($_.LastModified) | `$($_.SHA256.Substring(0,16))...` |"
}
$TableText = ($TableRows -join "`r`n")

$IndexBlock = @"

$SectionMarker

- **記録日**: 2026-11-06 JST（執行監査・週次総括・Git資産整理）
- **対象案件**: `BO-EUR-005`（ISゲートにて正式棄却・凍結 / `VIEWED_EVAL` 2022–2026年 748件未開封維持）および次週新規調査3案（`Proposal A / B / C`）
- **3工程保管ルート**: `G:/マイドライブ/AIトレーサビリティ/BO・EA Edge Discovery/Gemini側必勝調査報告/`

| 工程 | ファイル（リポジトリ内正本パス） | 用途・確認状態（静的/実行確認区分） | 更新日時 | SHA256（実測先頭16桁） |
| :--- | :--- | :--- | :--- | :--- |
$TableText
"@

if (Test-Path $RootIndexPath) {
    $currentIndex = Get-Content -Path $RootIndexPath -Raw -Encoding UTF8
    if ($currentIndex -notmatch [regex]::Escape($SectionMarker)) {
        Add-Content -Path $RootIndexPath -Value $IndexBlock -Encoding UTF8
        Write-Host "  [Updated] Appended 2026-11-06 asset table to $RootIndexPath" -ForegroundColor Green
    } else {
        Write-Host "  [Skipped] 2026-11-06 section already exists in $RootIndexPath" -ForegroundColor Yellow
    }
} else {
    Set-Content -Path $RootIndexPath -Value ("# プログラム索引`r`n" + $IndexBlock) -Encoding UTF8
    Write-Host "  [Created] $RootIndexPath" -ForegroundColor Green
}

# 5. .gitignore の整備（大容量CSV・ヒストリカルデータ・ZIPの誤コミット防止）
Write-Host "`n[5/6] Ensuring .gitignore excludes large CSVs and raw tick/bar archives..." -ForegroundColor Cyan
$GitIgnorePath = Join-Path $RepoRoot ".gitignore"
$IgnoreRules = @(
    "# Exclude large historical price CSVs and multi-MB intermediate tables",
    "*1.csv",
    "*5.csv",
    "*_TimeSeries.csv",
    "opportunity_ledger.csv",
    "outcomes.csv",
    "is_outcomes.csv",
    "is_plateau_grid.csv",
    "is_2015_2021_opportunity_ledger*.csv",
    "*.zip",
    "__pycache__/",
    "*.pyc"
)
if (Test-Path $GitIgnorePath) {
    $existingIgnore = Get-Content -Path $GitIgnorePath -Raw -Encoding UTF8
    foreach ($rule in $IgnoreRules) {
        if ($existingIgnore -notmatch [regex]::Escape($rule)) {
            Add-Content -Path $GitIgnorePath -Value $rule -Encoding UTF8
        }
    }
} else {
    Set-Content -Path $GitIgnorePath -Value ($IgnoreRules -join "`r`n") -Encoding UTF8
}

# 6. Git ステージング・大容量ファイル除外検査・コミット
if ($CommitToGit -and (Test-Path (Join-Path $RepoRoot ".git"))) {
    Write-Host "`n[6/6] Staging verified .py, .md, .ps1, and compact manifests in Git..." -ForegroundColor Cyan
    Push-Location $RepoRoot
    try {
        git add ".gitignore"
        git add "INDEX.md"
        git add "01_Plans_and_Decisions/*.md"
        git add "01_Plans_and_Decisions/**/*.md"
        git add "04_Python_Research/**/*.py"
        git add "07_Tests_and_Backtests/BO-EUR-005/output_is_plateau_20261104_173018/spark_audit_handover_manifest.json"
        git add "07_Tests_and_Backtests/BO-EUR-005/output_is_plateau_20261104_173018/is_standalone_summary.csv"
        git add "07_Tests_and_Backtests/BO-EUR-005/output_is_plateau_20261104_173018/is_paired_summary.csv"
        git add "07_Tests_and_Backtests/BO-EUR-005/output_is_plateau_20261104_173018/is_yearly_breakdown.csv"

        # Safety gate: unstage any file > 1 MB or any large CSV
        $stagedFiles = git diff --cached --name-only
        foreach ($sf in $stagedFiles) {
            if (Test-Path $sf) {
                $sz = (Get-Item $sf).Length
                if ($sz -gt 1048576) {
                    Write-Warning "Unstaging oversized file (>1MB): $sf ($sz bytes)"
                    git reset HEAD -- $sf | Out-Null
                }
            }
        }

        Write-Host "`n--- Staged Git Changes ---" -ForegroundColor Green
        git status --short

        $hasStaged = git diff --cached --name-only
        if ($hasStaged) {
            git commit -m "chore(bo-eur-005): record IS gate rejection, weekly audit & stage 1-3 scripts (2026-11-06)"
            Write-Host "[Completed] Git commit succeeded." -ForegroundColor Cyan
        } else {
            Write-Host "[Info] Working tree is already clean and up to date." -ForegroundColor Yellow
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "`n[6/6] Git commit skipped (or .git not initialized at $RepoRoot). File sync and INDEX.md update completed." -ForegroundColor Yellow
}
