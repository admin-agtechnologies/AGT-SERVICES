param(
    [string]$RootPath = ".",
    [ValidateSet("summary","full")]
    [string]$Mode = "full"
)

$OutputDir = "_scan_output"
$MaxFileSizeKB = 300

$root = Resolve-Path $RootPath
$outDir = Join-Path $root $OutputDir

if (!(Test-Path $outDir)) {
    New-Item -ItemType Directory -Path $outDir | Out-Null
}

$outFile = Join-Path $outDir "context.md"

Write-Host "Scanning project..."

# ---------- FILE FILTER ----------
function IsValidFile($file) {
    $ext = $file.Extension.ToLower()

    $allowed = @(
        ".py",".js",".ts",".json",".yml",".yaml",
        ".md",".txt",".toml",".env",".sql",".conf"
    )

    return $allowed -contains $ext -or
           $file.Name -match "docker|requirements|package|readme|env"
}

# ---------- EXCLUDED ----------
function IsExcluded($path) {
    $p = $path.ToLower()

    return $p -match "node_modules|\.git|\.venv|__pycache__|dist|build"
}

# ---------- TREE ----------
$tree = ""
Get-ChildItem $root -Recurse | ForEach-Object {
    if (-not (IsExcluded $_.FullName)) {
        $rel = $_.FullName.Replace($root, "")
        $tree += "$rel`n"
    }
}

# ---------- FILES ----------
$files = @()

Get-ChildItem $root -Recurse -File | ForEach-Object {
    if (!(IsExcluded $_.FullName) -and (IsValidFile $_)) {
        $files += $_
    }
}

# ---------- BUILD ----------
$content = "# AGT CONTEXT`n`n"

$content += "## PROJECT TREE`n"
$content += "```text`n$tree`n```n`n"

$content += "## FILES`n"

foreach ($f in $files) {
    $size = [math]::Round($f.Length / 1KB,2)
    $content += "- $($f.FullName) ($size KB)`n"
}

$content += "`n## CODE CONTEXT`n`n"

if ($Mode -eq "full") {
    foreach ($f in $files) {
        $size = $f.Length / 1KB

        if ($size -lt $MaxFileSizeKB) {
            $content += "===== FILE START: $($f.FullName) =====`n"

            try {
                $data = Get-Content $f.FullName -Raw
                $content += "```n$data`n```n"
            } catch {
                $content += "[UNREADABLE]`n"
            }

            $content += "===== FILE END =====`n`n"
        }
    }
}

$content += "## SUMMARY`n"
$content += "- Total files: $($files.Count)`n"

Set-Content -Path $outFile -Value $content -Encoding UTF8

Write-Host "Done."
Write-Host "Output: $outFile"