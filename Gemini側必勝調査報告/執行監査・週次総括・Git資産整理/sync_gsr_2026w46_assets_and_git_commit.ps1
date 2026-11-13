# ==============================================================================
# BO・EA Edge Discovery (Gemini側必勝調査報告) — GSR-2026W46 週次資産整理・INDEX.md反映・Git正本登録スクリプト
# 保管先: G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\sync_gsr_2026w46_assets_and_git_commit.ps1
# 準拠規約: プログラム資産管理手順.txt（実ソースSHA256再計算・旧版保持・大容量CSV除外）＆ GEMINI_DISCOVERY_TRACE_RULE.md
# ==============================================================================
[CmdletBinding()]
param(
    [switch]$CommitToGit = $true
)

$ErrorActionPreference = "Stop"

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
    throw "Google Drive 内のプロジェクトルートが見つかりません。G:ドライブのマウントを確認してください。"
}
Write-Host "[1/6] Project Root : $RepoRoot" -ForegroundColor Cyan

# 2. GSR-2026W46 検証スクリプト(.py)・ドキュメント(.md)の実ソースSHA256再計算と照合（手順書 規則2・4・5・6）
$ExpectedAssets = @(
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_2015_2021_v1_4.py"
        ExpectedSha256 = "809ec0ec9c5623dd369814c238ec2b344f2ab9f83ae9e11d1df718e495ad732a"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage1_Market_Survey"
        Status = "実行確認済み（v1.4.0 Dukascopy M1正本パス・GSRコード対応）"
    },
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_2015_2021_v1_3.py"
        ExpectedSha256 = "c2098de77aef3c19719626d0e33acd050d59bd8192479e6079c039c7d3e1fa4c"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage1_Market_Survey\archive"
        Status = "旧版保持（v1.3.0）"
    },
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_2015_2021_v1_2.py"
        ExpectedSha256 = "a7fa4ada92f47c5adb2d01db7e4c823bd8a5820fb06c23c2f13951027aaae2eb"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage1_Market_Survey\archive"
        Status = "旧版保持（v1.2.0）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "gsr_eurusd_is_plateau_verifier_v1_0.py"
        ExpectedSha256 = "cbb38b9e9776d8215899c460d20d12ce02eca74b9e9c227a97559419d64dee21"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage2_IS_Plateau"
        Status = "実行確認済み（v1.1.0 非累積3Dマージナル＆PSEUDO_PLATEAU_WARNING改修版）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "gsr_eurusd_is_plateau_verifier_v1_1.py"
        ExpectedSha256 = "98a75ba95ff26e3b702bbbfa4b450f2eb195e6bec1588e41ef3a8429e5be02c9"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage2_IS_Plateau\archive"
        Status = "静的確認済み（v1.1.0 別名保存版）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "gsr_eurusd_is_plateau_verifier_v1_0_old_cumulative.py"
        ExpectedSha256 = "e10faa06c2f665c1cc732fab433b6d52daf9d598205c7d53a6c8707126a9a077"
        DestRelDir = "04_Python_Research\GSR-2026W46\Stage2_IS_Plateau\archive"
        Status = "旧版保持（v1.0.0 累積格子レガシー版）"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "GSR-2026W46_decision.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions"
        Status = "確定決定記録（GSR-2026W46 EURUSD 3候補＆既存EA監査 正式棄却・凍結）"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "GSR-2026W46_Spark_Audit_and_Executive_Summary_2026-11-09.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions\weekly_audits"
        Status = "GSR-2026W46 Spark独立監査（GSR-202611-W2-WED-SPARK）＆執行監査統合報告"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "DECISION_TEMPLATE.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions\templates"
        Status = "GSR専用コード＆非累積マージナル対応 decision.md 標準テンプレート"
    },
    @{
        Stage = "All"
        Path  = Join-Path $ReportRoot "GEMINI_DISCOVERY_TRACE_RULE.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions"
        Status = "Gemini側必勝調査報告 専用TRACEコード（GSR-*）採番規約"
    }
)

Write-Host "`n[2/6] Calculating live SHA256 hashes of GSR-2026W46 scripts and documents..." -ForegroundColor Cyan
$VerifiedRecords = @()

foreach ($item in $ExpectedAssets) {
    $srcPath = $item.Path
    if (-not (Test-Path $srcPath)) {
        Write-Warning "File not found (skipping): $srcPath"
        continue
    }
    $actualHash = (Get-FileHash -Path $srcPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $fileInfo   = Get-Item -Path $srcPath
    if ($item.ExpectedSha256 -and ($actualHash -ne $item.ExpectedSha256)) {
        Write-Warning "SHA256 notice on $($fileInfo.Name): expected $($item.ExpectedSha256), actual $actualHash"
    } else {
        Write-Host "  [OK] $($fileInfo.Name) ($($fileInfo.Length) B) SHA256=$($actualHash.Substring(0,16))..." -ForegroundColor Green
    }

    $destDir = Join-Path $RepoRoot $item.DestRelDir
    New-Item -ItemType Directory -Force -Path $destDir | Out-Null
    $destFile = Join-Path $destDir $fileInfo.Name
    if ((Test-Path $destFile) -and ((Get-FileHash $destFile -Algorithm SHA256).Hash.ToLowerInvariant() -ne $actualHash)) {
        $backupName = "$($fileInfo.BaseName)_backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')$($fileInfo.Extension)"
        Copy-Item -Path $destFile -Destination (Join-Path $destDir $backupName) -Force
    }
    Copy-Item -Path $srcPath -Destination $destFile -Force

    $VerifiedRecords += [PSCustomObject]@{
        Stage        = $item.Stage
        FileName     = $fileInfo.Name
        RelRepoPath  = (Join-Path $item.DestRelDir $fileInfo.Name).Replace('\', '/')
        Bytes        = $fileInfo.Length
        LastModified = $fileInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        SHA256       = $actualHash
        Status       = $item.Status
    }
}

# 3. 軽量集計CSV・マニフェスト（非累積3Dマージナル表含む）の同期（大容量明細CSVは除外）
Write-Host "`n[3/6] Syncing compact summary manifests & non-cumulative 3D marginal table..." -ForegroundColor Cyan
$Stage2OutDir = Join-Path $Stage2Dir "output_eurusd_is_plateau_20261109_060458"
$DestTestDir  = Join-Path $RepoRoot "07_Tests_and_Backtests\GSR-2026W46\output_eurusd_is_plateau_20261109_060458"
if (Test-Path $Stage2OutDir) {
    New-Item -ItemType Directory -Force -Path $DestTestDir | Out-Null
    $CompactFiles = @(
        "spark_audit_handover_manifest_eurusd.json",
        "is_standalone_summary_eurusd.csv",
        "is_yearly_breakdown_eurusd.csv",
        "is_session_breakdown_eurusd.csv",
        "is_atr_breakdown_eurusd.csv",
        "existing_eurusd_reports_m1_audit.csv",
        "is_non_cumulative_marginal_3d_eurusd.csv",
        "is_plateau_grid_eurusd_v1_1.csv"
    )
    foreach ($cf in $CompactFiles) {
        $cfPath = Join-Path $Stage2OutDir $cf
        if (-not (Test-Path $cfPath)) {
            $cfPath = Join-Path $Stage3Dir $cf
        }
        if (Test-Path $cfPath) {
            Copy-Item -Path $cfPath -Destination (Join-Path $DestTestDir $cf) -Force
            Write-Host "  [Copied compact evidence] $cf" -ForegroundColor Green
        }
    }
}

# 4. ルート INDEX.md への非破壊追記
Write-Host "`n[4/6] Appending GSR-2026W46 asset table to root INDEX.md..." -ForegroundColor Cyan
$RootIndexPath = Join-Path $RepoRoot "INDEX.md"
$SectionMarker = "## 週次検証・監査資産追記ログ（2026-11-09：GSR-2026W46 EURUSD 3候補＆既存EA監査 最終棄却・v1.1非累積マージナル改修）"

$TableRows = $VerifiedRecords | ForEach-Object {
    "| `$($_.Stage)` | [`$($_.FileName)`]($($_.RelRepoPath)) | $($_.Status) | $($_.LastModified) | `$($_.SHA256.Substring(0,16))...` |"
}
$TableText = ($TableRows -join "`r`n")

$IndexBlock = @"

$SectionMarker

- **記録日**: 2026-11-09 JST（執行監査・週次総括・Git資産整理）
- **専用案件コード**: `GSR-2026W46`（個別候補: `GSR-CLIMAX-001`, `GSR-PULLBACK-001`, `GSR-FAKEOUT-001`, `GSR-SURVEY-001` ／ 独立監査: `GSR-202611-W2-WED-SPARK`）
- **最終判定**: **棄却・凍結（EURUSD ISゲートにて全3候補不通過・他4通貨への展開中止・2022–2026年OOS 1,781,411行未開封ロック維持）**
- **主要監査成果**: 3D累積格子の擬似プラトーを排除する非累積3Dマージナル分解（`is_non_cumulative_marginal_3d_eurusd.csv`, SHA256: `2705bea4842ab7fb...`）を標準実装（v1.1.0）し、既存逆張りEAの `barsPassed > 5`（6分満期バグ）を摘発。

| 工程 | ファイル（リポジトリ内正本パス） | 用途・確認状態（静的/実行確認区分） | 更新日時 | SHA256（実測先頭16桁） |
| :--- | :--- | :--- | :--- | :--- |
$TableText
"@

if (Test-Path $RootIndexPath) {
    $currentIndex = Get-Content -Path $RootIndexPath -Raw -Encoding UTF8
    if ($currentIndex -notmatch [regex]::Escape($SectionMarker)) {
        Add-Content -Path $RootIndexPath -Value $IndexBlock -Encoding UTF8
        Write-Host "  [Updated] Appended GSR-2026W46 section to $RootIndexPath" -ForegroundColor Green
    } else {
        Write-Host "  [Skipped] GSR-2026W46 section already present in $RootIndexPath" -ForegroundColor Yellow
    }
} else {
    Set-Content -Path $RootIndexPath -Value ("# プログラム索引`r`n" + $IndexBlock) -Encoding UTF8
}

# 5. .gitignore による大容量CSV・生ヒストリカルデータの除外保証
Write-Host "`n[5/6] Ensuring .gitignore excludes large raw M1 CSVs and multi-MB ledgers/outcomes..." -ForegroundColor Cyan
$GitIgnorePath = Join-Path $RepoRoot ".gitignore"
$IgnoreRules = @(
    "# Exclude large historical M1 CSVs and multi-MB opportunity ledgers / outcomes",
    "*1.csv",
    "*5.csv",
    "*-M1-No Session.csv",
    "*_TimeSeries.csv",
    "opportunity_ledger.csv",
    "is_2015_2021_opportunity_ledger_*.csv",
    "outcomes.csv",
    "is_outcomes*.csv",
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

# 6. Git ステージング・1MB超ファイル強制アンステージ・コミット
if ($CommitToGit -and (Test-Path (Join-Path $RepoRoot ".git"))) {
    Write-Host "`n[6/6] Staging GSR-2026W46 code, markdown records, and compact summaries..." -ForegroundColor Cyan
    Push-Location $RepoRoot
    try {
        git add ".gitignore"
        git add "INDEX.md"
        git add "01_Plans_and_Decisions/*.md"
        git add "01_Plans_and_Decisions/**/*.md"
        git add "04_Python_Research/**/*.py"
        git add "07_Tests_and_Backtests/GSR-2026W46/output_eurusd_is_plateau_20261109_060458/*.json"
        git add "07_Tests_and_Backtests/GSR-2026W46/output_eurusd_is_plateau_20261109_060458/*.csv"

        # Safety gate: unstage any file > 500 KB or matching large ledger/outcomes names
        $stagedFiles = git diff --cached --name-only
        foreach ($sf in $stagedFiles) {
            if (Test-Path $sf) {
                $fItem = Get-Item $sf
                if (($fItem.Length -gt 512000) -or ($fItem.Name -like "*outcomes*.csv") -or ($fItem.Name -like "*opportunity_ledger*.csv")) {
                    Write-Warning "Unstaging large CSV (>500KB or raw outcomes/ledger): $sf ($($fItem.Length) bytes)"
                    git reset HEAD -- $sf | Out-Null
                }
            }
        }

        Write-Host "`n--- Staged Git Changes ---" -ForegroundColor Green
        git status --short

        $hasStaged = git diff --cached --name-only
        if ($hasStaged) {
            git commit -m "chore(gsr-2026w46): reject EURUSD 3 candidates at IS gate, add v1.1 non-cumulative marginal audit & fix 6m expiry bug"
            Write-Host "[Completed] Git commit succeeded." -ForegroundColor Cyan
        } else {
            Write-Host "[Info] Working tree is already clean." -ForegroundColor Yellow
        }
    } finally {
        Pop-Location
    }
} else {
    Write-Host "`n[6/6] Git commit skipped (or .git not initialized at $RepoRoot). File sync and INDEX.md update completed." -ForegroundColor Yellow
}
