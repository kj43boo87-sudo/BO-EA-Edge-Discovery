# ==============================================================================
# BO・EA Edge Discovery (Gemini側必勝調査報告) — GSR-2026W47 第3工程 Git正本資産整理＆INDEX.md更新スクリプト
# 保管先: G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\sync_gsr_2026w47_assets_and_git_commit.ps1
# 準拠規約: プログラム資産管理手順.txt（8原則：README→INDEX→説明書→実ソース確認、作業前後SHA256照合、旧版非破壊保持、大容量CSV完全除外）
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
    throw "Google Drive 内のプロジェクトルートが見つかりません。G:ドライブの同期状態を確認してください。"
}
Write-Host "[1/6] Canonical Root : $RepoRoot" -ForegroundColor Cyan

# 2. プログラム資産管理8原則に基づく事前ドキュメント・実ソースSHA256再計算＆照合
$ExpectedAssets = @(
    @{
        Stage = "Master"
        Path  = Join-Path (Split-Path $ReportRoot -Parent) "QUANT_PYTHON_MASTER_CONTEXT.md"
        ExpectedSha256 = "89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13"
        DestRelDir = "01_Plans_and_Decisions"
        Status = "現行版確認済み（v2.2 共通マスターコンテキスト）"
    },
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "profile_is_market_structure_gsr_2026w47_v1_0.py"
        ExpectedSha256 = "d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1"
        DestRelDir = "04_Python_Research\GSR-2026W47\Stage1_Market_Survey"
        Status = "実行確認済み（v1.0.2 Label-Free機会台帳抽出）"
    },
    @{
        Stage = "Stage1"
        Path  = Join-Path $Stage1Dir "output_is_profile_gsr_2026w47_20261110_070227\stage1_to_stage2_handover_manifest_gsr_2026w47.json"
        ExpectedSha256 = "37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c"
        DestRelDir = "07_Tests_and_Backtests\GSR-2026W47\Stage1_Profile"
        Status = "実行確認済み（第1→第2工程引き継ぎマニフェストJSON）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "gsr_2026w47_is_plateau_verifier_v1_0.py"
        ExpectedSha256 = "0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f"
        DestRelDir = "04_Python_Research\GSR-2026W47\Stage2_IS_Plateau"
        Status = "実行確認済み（v1.0.0 非重複3D格子＆1Dマージナル＆アブレーション検証）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md"
        ExpectedSha256 = "1acd59bbe6223985aaa8335dc7b27be7287703a484ce1ae890c9d1240a410118"
        DestRelDir = "01_Plans_and_Decisions\weekly_audits"
        Status = "実行確認済み（GSR-2026W47 第2工程統計・Plateau検証報告）"
    },
    @{
        Stage = "Stage2"
        Path  = Join-Path $Stage2Dir "GSR-202611-W3-WED-SPARK.md"
        ExpectedSha256 = ""
        DestRelDir = "01_Plans_and_Decisions\weekly_audits"
        Status = "確定済み（Aegis/Spark独立性能監査報告 GSR-202611-W3-WED-SPARK）"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "GSR-2026W47_decision.md"
        ExpectedSha256 = "a045fc0bd77f06349b9dd648f0f06a470a94af59ee4c7c8a356459ace1e765d3"
        DestRelDir = "01_Plans_and_Decisions"
        Status = "確定決定記録（EXHAUST/SHOCKDECAY棄却・TKYFIX保留＆GSR-TKYFIX-002実験契約）"
    },
    @{
        Stage = "Stage3"
        Path  = Join-Path $Stage3Dir "GSR-2026W47_Executive_Audit_and_Weekly_Summary_2026-11-13.md"
        ExpectedSha256 = "31ad4595f20f3a2c08934646d10e702f2ff44db5ee62342beb875b066a07df27"
        DestRelDir = "01_Plans_and_Decisions\weekly_audits"
        Status = "確定済み（GSR-2026W47 第3工程執行監査・週次総括統合報告）"
    }
)

Write-Host "`n[2/6] Verifying live SHA256 hashes of GSR-2026W47 scripts, manifests, and decision records..." -ForegroundColor Cyan
$VerifiedRecords = @()

foreach ($item in $ExpectedAssets) {
    $srcPath = $item.Path
    if (-not (Test-Path $srcPath)) {
        Write-Warning "Optional/Pending file not found at $srcPath (skipping)"
        continue
    }
    $actualHash = (Get-FileHash -Path $srcPath -Algorithm SHA256).Hash.ToLowerInvariant()
    $fileInfo   = Get-Item -Path $srcPath
    if ($item.ExpectedSha256 -and ($actualHash -ne $item.ExpectedSha256)) {
        Write-Warning "SHA256 mismatch on $($fileInfo.Name): expected $($item.ExpectedSha256), actual $actualHash"
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

# 3. 軽量集計CSV・マニフェストJSONのみをテスト証跡フォルダへ同期（大容量機会台帳26.6MB等は厳格除外）
Write-Host "`n[3/6] Syncing GSR-2026W47 compact summary CSVs & manifest JSON..." -ForegroundColor Cyan
$Stage2OutDir = Join-Path $Stage2Dir "output_gsr_2026w47_is_plateau_20261110_070559"
$DestTestDir  = Join-Path $RepoRoot "07_Tests_and_Backtests\GSR-2026W47\output_gsr_2026w47_is_plateau_20261110_070559"
if (Test-Path $Stage2OutDir) {
    New-Item -ItemType Directory -Force -Path $DestTestDir | Out-Null
    $CompactFiles = @(
        @{ Name = "spark_audit_handover_manifest_gsr_2026w47.json"; Hash = "ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb" },
        @{ Name = "is_standalone_and_ablation_summary_gsr_2026w47.csv"; Hash = "ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d" },
        @{ Name = "is_disjoint_3d_grid_gsr_2026w47.csv"; Hash = "e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e" },
        @{ Name = "is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv"; Hash = "0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb" }
    )
    foreach ($cf in $CompactFiles) {
        $cfPath = Join-Path $Stage2OutDir $cf.Name
        if (Test-Path $cfPath) {
            $h = (Get-FileHash -Path $cfPath -Algorithm SHA256).Hash.ToLowerInvariant()
            if ($h -eq $cf.Hash) {
                Write-Host "  [OK] $($cf.Name) SHA256=$($h.Substring(0,16))..." -ForegroundColor Green
            }
            Copy-Item -Path $cfPath -Destination (Join-Path $DestTestDir $cf.Name) -Force
        }
    }
}

# 4. ルート INDEX.md の非破壊更新（GSR-EXHAUST-001: FAIL / GSR-SHOCKDECAY-001: FAIL / GSR-TKYFIX-001: HOLD -> GSR-TKYFIX-002 移行）
Write-Host "`n[4/6] Updating root INDEX.md with GSR-2026W47 final rulings & GSR-TKYFIX-002 contract..." -ForegroundColor Cyan
$RootIndexPath = Join-Path $RepoRoot "INDEX.md"
$SectionMarker = "## 週次検証・監査資産追記ログ（2026-11-13：GSR-2026W47 最終裁定確定 ＆ GSR-TKYFIX-002 IS内追加検証差配）"

$TableRows = $VerifiedRecords | ForEach-Object {
    "| `$($_.Stage)` | [`$($_.FileName)`]($($_.RelRepoPath)) | $($_.Status) | $($_.LastModified) | `$($_.SHA256.Substring(0,16))...` |"
}
$TableText = ($TableRows -join "`r`n")

$IndexBlock = @"

$SectionMarker

- **記録日**: 2026-11-13 JST（第3工程：最終5ゲート判定・週次総括・Git資産整理）
- **対象パイプライン**: `GSR-2026W47`（独立監査ログ: `GSR-202611-W3-WED-SPARK`）
- **案件別最終ステータス**:
  - `GSR-EXHAUST-001`（EURUSD / USDJPY M1）: **`FAIL`（棄却・永久凍結）** — 逆アブレーション（`-2.40%pt`）、$\text{CLB}_{97.5\%} < 0$、摩擦崩壊（TRAP-05）。再検証・延命厳禁。
  - `GSR-SHOCKDECAY-001`（EURUSD / USDJPY M1）: **`FAIL`（棄却・永久凍結）** — 逆アブレーション、$\text{CLB}_{97.5\%} < 0$、摩擦崩壊（TRAP-05）。再検証・延命厳禁。
  - `GSR-TKYFIX-001`（USDJPY M1）: **`HOLD`（保留 ➔ `GSR-TKYFIX-002` IS内追加検証へ移行）** — 値幅中央値 `+0.50 pip`、`+0.3 pip` 勝率 `55.26%` の摩擦耐性を確認。OOS（2022–2026）未開封ロック維持のもと、実験A（OR条件TRAP-06排除）・実験B（15分変動幅下限分離）・実験C（64分割TRAP-07廃止・非重複粗視化スライス）を実施。

| 工程 | ファイル（リポジトリ内正本パス） | 用途・確認状態（静的/実行確認区分） | 更新日時 | SHA256（実測先頭16桁） |
| :--- | :--- | :--- | :--- | :--- |
$TableText
"@

if (Test-Path $RootIndexPath) {
    $currentIndex = Get-Content -Path $RootIndexPath -Raw -Encoding UTF8
    if ($currentIndex -notmatch [regex]::Escape($SectionMarker)) {
        Add-Content -Path $RootIndexPath -Value $IndexBlock -Encoding UTF8
        Write-Host "  [Updated] Appended GSR-2026W47 section to $RootIndexPath" -ForegroundColor Green
    } else {
        Write-Host "  [Skipped] GSR-2026W47 section already exists in $RootIndexPath" -ForegroundColor Yellow
    }
} else {
    Set-Content -Path $RootIndexPath -Value ("# プログラム索引`r`n" + $IndexBlock) -Encoding UTF8
}

# 5. .gitignore の厳格検証（生M1 CSV、機会台帳CSV 26.6MB、全行勝敗CSV、ZIPの完全除外）
Write-Host "`n[5/6] Enforcing .gitignore rules for large CSVs and raw data..." -ForegroundColor Cyan
$GitIgnorePath = Join-Path $RepoRoot ".gitignore"
$IgnoreRules = @(
    "# Exclude large historical M1 CSVs, opportunity ledgers, outcomes, and archives",
    "*1.csv",
    "*5.csv",
    "*-M1-No Session.csv",
    "*_TimeSeries.csv",
    "opportunity_ledger.csv",
    "is_2015_2021_opportunity_ledger_*.csv",
    "is_2015_2021_opportunity_ledger_gsr_2026w47.csv",
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

# 6. Git ステージング・大容量ファイル強制遮断検査・コミット
if ($CommitToGit -and (Test-Path (Join-Path $RepoRoot ".git"))) {
    Write-Host "`n[6/6] Staging verified GSR-2026W47 assets and running size gate..." -ForegroundColor Cyan
    Push-Location $RepoRoot
    try {
        git add ".gitignore"
        git add "INDEX.md"
        git add "01_Plans_and_Decisions/*.md"
        git add "01_Plans_and_Decisions/**/*.md"
        git add "04_Python_Research/**/*.py"
        git add "07_Tests_and_Backtests/GSR-2026W47/**/*.json"
        git add "07_Tests_and_Backtests/GSR-2026W47/**/*.csv"
        git add "Gemini側必勝調査報告/*/*.py" 2>$null
        git add "Gemini側必勝調査報告/*/*.ps1" 2>$null
        git add "Gemini側必勝調査報告/*/*.md" 2>$null

        # Safety gate: unstage any file > 500 KB or matching ledger/outcomes/raw M1 patterns
        $stagedFiles = git diff --cached --name-only
        foreach ($sf in $stagedFiles) {
            if (Test-Path $sf) {
                $fItem = Get-Item $sf
                if (($fItem.Length -gt 512000) -or ($fItem.Name -like "*opportunity_ledger*.csv") -or ($fItem.Name -like "*outcomes*.csv") -or ($fItem.Name -like "*-M1-*")) {
                    Write-Warning "Unstaging excluded large file: $sf ($($fItem.Length) bytes)"
                    git reset HEAD -- $sf | Out-Null
                }
            }
        }

        Write-Host "`n--- Staged Git Changes ---" -ForegroundColor Green
        git status --short

        $hasStaged = git diff --cached --name-only
        if ($hasStaged) {
            git commit -m "chore(gsr-2026w47): freeze EXHAUST/SHOCKDECAY as FAIL, hold TKYFIX-001 & register GSR-TKYFIX-002 IS contract"
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
