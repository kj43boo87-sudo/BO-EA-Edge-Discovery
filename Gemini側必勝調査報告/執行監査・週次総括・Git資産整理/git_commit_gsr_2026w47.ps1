# ==============================================================================
# BO・EA Edge Discovery — GSR-2026W47 第3工程 2段階同期（Gドライブミラー ＆ GitHub Push）スクリプト
# ファイル名: git_commit_gsr_2026w47.ps1
# ローカルGit正本ルート: C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery
# Gドライブミラー先:     G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告
# 準拠規約: プログラム資産管理手順.txt（8原則：作業前後SHA256再照合、旧版非破壊保持、.gitロック回避、大容量CSV完全除外）
# ==============================================================================
[CmdletBinding()]
param(
    [string]$LocalRepoRoot = "C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery",
    [string]$GDriveReportRoot = "G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告",
    [switch]$PushToGitHub = $true
)

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host " GSR-2026W47 Stage 3: 1) Local Asset & SHA256 Audit -> 2) GDrive Mirror -> 3) Git Push" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# 0. パス存在確認と 00_Project_Control 等の標準フォルダ確保
if (-not (Test-Path $LocalRepoRoot)) {
    throw "ローカルGitリポジトリが見つかりません: $LocalRepoRoot"
}
if (-not (Test-Path (Join-Path $LocalRepoRoot ".git"))) {
    throw ".git ディレクトリが見つかりません: $LocalRepoRoot\.git"
}
if (-not (Test-Path $GDriveReportRoot)) {
    throw "Google Drive 側の同期先ルートが見つかりません: $GDriveReportRoot"
}

$Stage1Dir = Join-Path $GDriveReportRoot "トレード手法の市場調査＆データ点検"
$Stage2Dir = Join-Path $GDriveReportRoot "機会台帳突合＆IS統計・Plateau検証"
$Stage3Dir = Join-Path $GDriveReportRoot "執行監査・週次総括・Git資産整理"

$ControlDir = Join-Path $LocalRepoRoot "00_Project_Control"
$LocalStage1Dir = Join-Path $LocalRepoRoot "Gemini側必勝調査報告\トレード手法の市場調査＆データ点検"
$LocalStage2Dir = Join-Path $LocalRepoRoot "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証"
$LocalStage3Dir = Join-Path $LocalRepoRoot "Gemini側必勝調査報告\執行監査・週次総括・Git資産整理"

New-Item -ItemType Directory -Force -Path $ControlDir, $LocalStage1Dir, $LocalStage2Dir, $LocalStage3Dir | Out-Null

# 1. Gドライブ上の最新第1〜第3工程成果物をローカルGitリポジトリ（00_Project_Control 等）へ取り込み（大容量CSV除外）
Write-Host "`n[Step 1/5] Syncing verified GSR-2026W47 deliverables into $LocalRepoRoot..." -ForegroundColor Cyan

$DecisionSrc = Join-Path $Stage3Dir "GSR-2026W47_decision.md"
$DecisionDestControl = Join-Path $ControlDir "GSR-2026W47_decision.md"
$DecisionDestStage3  = Join-Path $LocalStage3Dir "GSR-2026W47_decision.md"

if (Test-Path $DecisionSrc) {
    Copy-Item -Path $DecisionSrc -Destination $DecisionDestControl -Force
    Copy-Item -Path $DecisionSrc -Destination $DecisionDestStage3 -Force
    Write-Host "  [Synced] GSR-2026W47_decision.md -> 00_Project_Control\" -ForegroundColor Green
}

# GSR-2026W46_decision.md や QUANT_PYTHON_MASTER_CONTEXT.md、GEMINI_DISCOVERY_TRACE_RULE.md も 00_Project_Control へ集約
$ControlFiles = @(
    (Join-Path $Stage3Dir "GSR-2026W46_decision.md"),
    (Join-Path $Stage3Dir "DECISION_TEMPLATE.md"),
    (Join-Path $GDriveReportRoot "GEMINI_DISCOVERY_TRACE_RULE.md"),
    (Join-Path (Split-Path $GDriveReportRoot -Parent) "QUANT_PYTHON_MASTER_CONTEXT.md")
)
foreach ($cf in $ControlFiles) {
    if (Test-Path $cf) {
        $leaf = Split-Path $cf -Leaf
        Copy-Item -Path $cf -Destination (Join-Path $ControlDir $leaf) -Force
    }
}

# Gドライブの3工程フォルダからローカルリポジトリ内ミラー階層へ軽量資産のみ取り込み（大容量CSV・ZIP除外）
$ExcludeFiles = @(
    "*1.csv",
    "*5.csv",
    "*-M1-No Session.csv",
    "*_TimeSeries.csv",
    "opportunity_ledger.csv",
    "is_2015_2021_opportunity_ledger_*.csv",
    "outcomes.csv",
    "is_outcomes*.csv",
    "*.zip",
    "*.pyc",
    "desktop.ini"
)
$ExcludeDirs = @(".git", "__pycache__", ".venv", "venv")

& robocopy $GDriveReportRoot (Join-Path $LocalRepoRoot "Gemini側必勝調査報告") *.py *.ps1 *.md *.json *.csv /E /XO /XF $ExcludeFiles /XD $ExcludeDirs /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "Robocopy (GDrive -> LocalRepo) failed with exit code $LASTEXITCODE"
}

# スクリプト自身も 00_Project_Control と Stage3 の双方へ配置
$SelfPath = $MyInvocation.MyCommand.Path
if ($SelfPath -and (Test-Path $SelfPath)) {
    Copy-Item -Path $SelfPath -Destination (Join-Path $ControlDir "git_commit_gsr_2026w47.ps1") -Force
    Copy-Item -Path $SelfPath -Destination (Join-Path $LocalStage3Dir "git_commit_gsr_2026w47.ps1") -Force
}

# 2. プログラム資産管理8原則に基づく実ソース・文書のSHA256再計算と照合
Write-Host "`n[Step 2/5] Re-calculating and verifying SHA256 hashes across Local Git Repository..." -ForegroundColor Cyan

$AssetsToVerify = @(
    @{
        Stage = "Control"
        RelPath = "00_Project_Control\GSR-2026W47_decision.md"
        ExpectedSha256 = "bd2a79abf080883828121c896041abdebf73441ebe877e1287269b467787ddd7"
        Role = "GSR-2026W47 最終5ゲート裁定・GSR-TKYFIX-002実験契約（正本）"
        CheckClass = "現行版確認済み"
    },
    @{
        Stage = "Control"
        RelPath = "00_Project_Control\QUANT_PYTHON_MASTER_CONTEXT.md"
        ExpectedSha256 = "89f9c215a02717b1057cd14fa9167b5b8cb7fbc37e60760dbe5f572c2bbb9d13"
        Role = "共通マスターコンテキスト v2.2"
        CheckClass = "現行版確認済み"
    },
    @{
        Stage = "Control"
        RelPath = "00_Project_Control\GEMINI_DISCOVERY_TRACE_RULE.md"
        ExpectedSha256 = "fd70c9e64015404b8c324a03a62135a4b1f3229f5f8100d157d139c25517a4d6"
        Role = "GSR-* 専用TRACE採番規約"
        CheckClass = "現行版確認済み"
    },
    @{
        Stage = "Stage1"
        RelPath = "Gemini側必勝調査報告\トレード手法の市場調査＆データ点検\profile_is_market_structure_gsr_2026w47_v1_0.py"
        ExpectedSha256 = "d3f4ba214a79bb41e38313a1dbd307afff4a303ef836bee3d922ed77619bc5a1"
        Role = "GSR-2026W47 第1工程 Label-Free機会台帳抽出スクリプト (v1.0.2)"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage1"
        RelPath = "Gemini側必勝調査報告\トレード手法の市場調査＆データ点検\output_is_profile_gsr_2026w47_20261110_070227\stage1_to_stage2_handover_manifest_gsr_2026w47.json"
        ExpectedSha256 = "37a8842b0d34471d3adeeafac241279c85ab19fcb099b28f9155128c990b969c"
        Role = "GSR-2026W47 第1→第2工程引き継ぎマニフェストJSON"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\gsr_2026w47_is_plateau_verifier_v1_0.py"
        ExpectedSha256 = "0e888bc1e4926d6d41d7cbd16d46c78d01c4c2b1a2e21a2ad1fe5e08f439fc2f"
        Role = "GSR-2026W47 第2工程 非重複3D格子・1Dマージナル検証スクリプト (v1.0.0)"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\GSR-202611-W3-WED_Stage2_IS_Plateau_Report.md"
        ExpectedSha256 = "1acd59bbe6223985aaa8335dc7b27be7287703a484ce1ae890c9d1240a410118"
        Role = "GSR-2026W47 第2工程 統計・Plateau検証レポート"
        CheckClass = "現行版確認済み"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\GSR-202611-W3-WED-SPARK.md"
        ExpectedSha256 = ""
        Role = "Aegis (Spark) 第2工程独立性能監査レポート"
        CheckClass = "実行確認済み"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\output_gsr_2026w47_is_plateau_20261110_070559\spark_audit_handover_manifest_gsr_2026w47.json"
        ExpectedSha256 = "ad1b5c8b7b4b5ae430774c96f13e10759697de227f77e9e4edcf4fd62dc8e2eb"
        Role = "GSR-2026W47 第2工程 Spark監査引き継ぎマニフェストJSON"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\output_gsr_2026w47_is_plateau_20261110_070559\is_standalone_and_ablation_summary_gsr_2026w47.csv"
        ExpectedSha256 = "ba83b1a2a5e5c6543634d721bf5ab1e68d42e2bd3e0d7ecd3013c1d052ff375d"
        Role = "GSR-2026W47 Standalone & Controlアブレーション集計表 (15行)"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\output_gsr_2026w47_is_plateau_20261110_070559\is_disjoint_3d_grid_gsr_2026w47.csv"
        ExpectedSha256 = "e2ed1b6edd958492541d9deb1e215ea4fec1cd3df26bd26517210e5bbea1926e"
        Role = "GSR-2026W47 非重複(Disjoint) 3D 239セル集計表"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage2"
        RelPath = "Gemini側必勝調査報告\機会台帳突合＆IS統計・Plateau検証\output_gsr_2026w47_is_plateau_20261110_070559\is_non_cumulative_marginals_and_yearly_gsr_2026w47.csv"
        ExpectedSha256 = "0d9038e743d0af17643e1c191528be1bdca678cdfe3001c25d14bc2f85626bfb"
        Role = "GSR-2026W47 1D非累積マージナル＆年次分解表 (108行)"
        CheckClass = "現行版確認済み（実行確認済み）"
    },
    @{
        Stage = "Stage3"
        RelPath = "Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\GSR-2026W47_Executive_Audit_and_Weekly_Summary_2026-11-13.md"
        ExpectedSha256 = "31ad4595f20f3a2c08934646d10e702f2ff44db5ee62342beb875b066a07df27"
        Role = "GSR-2026W47 第3工程 執行監査・週次総括統合報告書"
        CheckClass = "現行版確認済み"
    },
    @{
        Stage = "Stage3"
        RelPath = "Gemini側必勝調査報告\執行監査・週次総括・Git資産整理\GSR-202611-W3-FRI_Stage3_to_Next_Monday_Stage1_Handover.md"
        ExpectedSha256 = "0bb8b57a7ab97aa7b96a56306160c40c6de4c88ef77f4b290186355843c8fd73"
        Role = "次週月曜（第1工程：GSR-2026W48）ループ接続引き継ぎ書"
        CheckClass = "現行版確認済み"
    }
)

$VerifiedRows = @()
foreach ($a in $AssetsToVerify) {
    $full = Join-Path $LocalRepoRoot $a.RelPath
    if (-not (Test-Path $full)) {
        Write-Warning "  [Missing] $($a.RelPath) (skipping)"
        continue
    }
    $hash = (Get-FileHash -Path $full -Algorithm SHA256).Hash.ToLowerInvariant()
    $fInfo = Get-Item -Path $full
    if ($a.ExpectedSha256 -and ($hash -ne $a.ExpectedSha256)) {
        Write-Warning "  [Hash Diff] $($fInfo.Name): expected $($a.ExpectedSha256), actual $hash"
    } else {
        Write-Host "  [Verified] $($fInfo.Name) ($($fInfo.Length) B) SHA256=$($hash.Substring(0,16))..." -ForegroundColor Green
    }
    $VerifiedRows += [PSCustomObject]@{
        Stage        = $a.Stage
        FileName     = $fInfo.Name
        RelPath      = $a.RelPath.Replace('\', '/')
        Bytes        = $fInfo.Length
        LastModified = $fInfo.LastWriteTime.ToString("yyyy-MM-dd HH:mm:ss")
        SHA256       = $hash
        Role         = $a.Role
        CheckClass   = $a.CheckClass
    }
}

# 3. ローカルリポジトリのルート INDEX.md 更新（手編集内容を消さずに非破壊追記）
Write-Host "`n[Step 3/5] Updating root INDEX.md in $LocalRepoRoot..." -ForegroundColor Cyan
$RootIndexPath = Join-Path $LocalRepoRoot "INDEX.md"
$SectionHeader = "## GSR-2026W47 第3工程 最終裁定＆GSR-TKYFIX-002差配登録（2026-11-13 JST）"

$MdRows = $VerifiedRows | ForEach-Object {
    "| `$($_.Stage)` | [`$($_.FileName)`]($($_.RelPath)) | $($_.Role) | `$($_.CheckClass)` | $($_.LastModified) | `$($_.SHA256.Substring(0,16))...` |"
}
$MdTable = ($MdRows -join "`r`n")

$AppendSection = @"

$SectionHeader

- **ローカルGit正本パス**: `C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery`
- **Gドライブミラーパス**: `G:\マイドライブ\AIトレーサビリティ\BO・EA Edge Discovery\Gemini側必勝調査報告`
- **案件ステータス確定**:
  - `GSR-EXHAUST-001`（EURUSD / USDJPY M1）: **`FAIL`（棄却・永久凍結）** — 逆アブレーション（`-2.40%pt`）、$\text{CLB}_{97.5\%} < 0$、摩擦崩壊（TRAP-05）。再検証厳禁。
  - `GSR-SHOCKDECAY-001`（EURUSD / USDJPY M1）: **`FAIL`（棄却・永久凍結）** — 逆アブレーション、$\text{CLB}_{97.5\%} < 0$、摩擦崩壊（TRAP-05）。再検証厳禁。
  - `GSR-TKYFIX-001`（USDJPY M1）: **`HOLD`（保留 ➔ `GSR-TKYFIX-002` IS内追加検証へ移行）** — 値幅中央値 `+0.50 pip`、`+0.3 pip` 勝率 `55.26%`。OOS（2022–2026）未開封ロック維持のもと、実験A（OR条件TRAP-06排除）・実験B（15分変動幅下限分離）・実験C（64分割TRAP-07廃止・非重複粗視化スライス）を実施。

| 階層 | ファイル（リポジトリ相対パス） | 役割・内容 | 4段階確認区分 | 更新日時 | SHA256（先頭16桁） |
| :--- | :--- | :--- | :--- | :--- | :--- |
$MdTable
"@

if (Test-Path $RootIndexPath) {
    $existingIdx = Get-Content -Path $RootIndexPath -Raw -Encoding UTF8
    if ($existingIdx -notmatch [regex]::Escape($SectionHeader)) {
        Add-Content -Path $RootIndexPath -Value $AppendSection -Encoding UTF8
        Write-Host "  [Updated] Appended GSR-2026W47 section to $RootIndexPath" -ForegroundColor Green
    } else {
        Write-Host "  [Skipped] GSR-2026W47 section already present in $RootIndexPath" -ForegroundColor Yellow
    }
} else {
    Set-Content -Path $RootIndexPath -Value ("# BO-EA-Edge-Discovery プログラム資産索引 (INDEX.md)`r`n" + $AppendSection) -Encoding UTF8
    Write-Host "  [Created] $RootIndexPath" -ForegroundColor Green
}

# 4. 処理1（Google Drive正本ミラーコピー：.gitおよび大容量データを厳格除外してGドライブへ同期）
Write-Host "`n[Step 4/5] Stage-1 Sync: Mirroring canonical files from Local Repo to Google Drive (.git & large CSVs excluded)..." -ForegroundColor Cyan

$GDriveControlMirror = Join-Path $GDriveReportRoot "00_Project_Control"
New-Item -ItemType Directory -Force -Path $GDriveControlMirror | Out-Null

# 00_Project_Control を Google Drive 側へミラーコピー（.git・大容量CSV除外）
& robocopy $ControlDir $GDriveControlMirror /E /XO /XF $ExcludeFiles /XD $ExcludeDirs /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "Robocopy (00_Project_Control -> GDrive) failed with exit code $LASTEXITCODE"
}

# ローカルの Gemini側必勝調査報告 配下の更新分を Google Drive 側へ同期（Gドライブ側の既存大容量台帳CSVを消さないよう /MIR ではなく /E /XO を使用）
& robocopy (Join-Path $LocalRepoRoot "Gemini側必勝調査報告") $GDriveReportRoot *.py *.ps1 *.md *.json *.csv /E /XO /XF $ExcludeFiles /XD $ExcludeDirs /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) {
    throw "Robocopy (Local Gemini側必勝調査報告 -> GDrive) failed with exit code $LASTEXITCODE"
}

# ルート INDEX.md と README.md も Gドライブ側の BO・EA Edge Discovery 直下へ控え同期
$GDriveProjectRoot = Split-Path $GDriveReportRoot -Parent
Copy-Item -Path $RootIndexPath -Destination (Join-Path $GDriveProjectRoot "INDEX.md") -Force
if (Test-Path (Join-Path $LocalRepoRoot "README.md")) {
    Copy-Item -Path (Join-Path $LocalRepoRoot "README.md") -Destination (Join-Path $GDriveProjectRoot "README.md") -Force
}
Write-Host "  [OK] Google Drive mirror sync completed without touching .git or large CSVs." -ForegroundColor Green

# 5. 処理2（ローカルGitリポジトリ C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery での .gitignore 検証・Commit・GitHub Push）
Write-Host "`n[Step 5/5] Stage-2 Sync: Staging, committing, and pushing to origin/main from $LocalRepoRoot..." -ForegroundColor Cyan

Push-Location $LocalRepoRoot
try {
    # .gitignore に大容量データ除外規則が含まれていることを保証
    $GitIgnorePath = Join-Path $LocalRepoRoot ".gitignore"
    $RequiredIgnores = @(
        "# Exclude large historical M1 CSVs, opportunity ledgers, full outcomes, and archives",
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
        $curIgnore = Get-Content -Path $GitIgnorePath -Raw -Encoding UTF8
        foreach ($rule in $RequiredIgnores) {
            if ($curIgnore -notmatch [regex]::Escape($rule)) {
                Add-Content -Path $GitIgnorePath -Value $rule -Encoding UTF8
            }
        }
    } else {
        Set-Content -Path $GitIgnorePath -Value ($RequiredIgnores -join "`r`n") -Encoding UTF8
    }

    git add ".gitignore"
    git add "README.md" 2>$null
    git add "INDEX.md"
    git add "00_Project_Control/*"
    git add "Gemini側必勝調査報告/**/*.py" 2>$null
    git add "Gemini側必勝調査報告/**/*.ps1" 2>$null
    git add "Gemini側必勝調査報告/**/*.md" 2>$null
    git add "Gemini側必勝調査報告/**/*.json" 2>$null
    git add "Gemini側必勝調査報告/**/*.csv" 2>$null

    # 安全防壁：500KB超のファイルおよび機会台帳・全行勝敗CSV・生M1データをステージングから強制排除
    $staged = git diff --cached --name-only
    foreach ($sf in $staged) {
        if (Test-Path $sf) {
            $item = Get-Item $sf
            if (($item.Length -gt 512000) -or ($item.Name -like "*opportunity_ledger*.csv") -or ($item.Name -like "*outcomes*.csv") -or ($item.Name -like "*-M1-*") -or ($item.Extension -eq ".zip")) {
                Write-Warning "  [Blocked Oversized/Excluded File] Unstaging $sf ($($item.Length) bytes)"
                git reset HEAD -- $sf | Out-Null
            }
        }
    }

    Write-Host "`n--- Git Status (C:\Users\kj43b\Desktop\BO-EA-Edge-Discovery) ---" -ForegroundColor Green
    git status --short

    $hasStagedChanges = git diff --cached --name-only
    if ($hasStagedChanges) {
        git commit -m "chore(gsr-2026w47): record final 5-gate ruling in 00_Project_Control, freeze EXHAUST/SHOCKDECAY & register GSR-TKYFIX-002 contract"
        Write-Host "  [Committed] Local commit created on branch $(git branch --show-current)." -ForegroundColor Green
    } else {
        Write-Host "  [No new changes] Working tree is already committed." -ForegroundColor Yellow
    }

    if ($PushToGitHub) {
        Write-Host "  [Pushing] Executing 'git push origin main'..." -ForegroundColor Cyan
        git push origin main
        Write-Host "  [Completed] Successfully pushed to origin/main (https://github.com/kj43boo87-sudo/BO-EA-Edge-Discovery.git)." -ForegroundColor Cyan
    }
} finally {
    Pop-Location
}
