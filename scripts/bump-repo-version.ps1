<#
.SYNOPSIS
Bump repo version from source VERSION file and propagate to known targets.

.PARAMETER Bump
One of: major, minor, patch.

.EXAMPLE
powershell -ExecutionPolicy ByPass -File "D:\DO\WEB\TOOLS\L4-TOOLS\DEEP-X\scripts\bump-repo-version.ps1" -Bump patch
#>
[CmdletBinding()]
param(
  [Parameter(Mandatory=$true)][ValidateSet('major','minor','patch')][string]$Bump
)

$ErrorActionPreference = 'Stop'
$repoRoot = Join-Path $PSScriptRoot '..'
$versionFile = Join-Path -Path $repoRoot -ChildPath 'VERSION'
if (-not (Test-Path -LiteralPath $versionFile)) {
  throw "VERSION file not found at $versionFile"
}

$current = (Get-Content -LiteralPath $versionFile -Raw).Trim()
if ($current -notmatch '^\d+\.\d+\.\d+$') {
  throw "Invalid current version format: $current"
}
$parts = $current.Split('.') | ForEach-Object { [int]$_ }
switch ($Bump) {
  'major' { $parts[0]++; $parts[1] = 0; $parts[2] = 0 }
  'minor' { $parts[1]++; $parts[2] = 0 }
  'patch' { $parts[2]++ }
}
$next = ($parts -join '.').ToString()
Write-Output "[bump-repo-version] current=$current next=$next repo=$repoRoot"

Set-Content -LiteralPath $versionFile -Value $next -Encoding UTF8

$candidates = @(
  'chrome\manifest.json',
  'firefox\manifest.json',
  'manifest.json',
  'package.json',
  'src\index.js',
  'README.md'
)

$updated = 0
foreach ($rel in $candidates) {
  $path = Join-Path -Path $repoRoot -ChildPath $rel
  if (-not (Test-Path -LiteralPath $path)) { continue }
  $content = Get-Content -LiteralPath $path -Raw
  $nextContent = $content -replace [regex]::Escape($current), $next
  if ($nextContent -ne $content) {
    Set-Content -LiteralPath $path -Value $nextContent -Encoding UTF8
    Write-Output "[bump-repo-version] updated=$path"
    $updated++
  }
}

if ($updated -eq 0) {
  Write-Output "[bump-repo-version] WARN no file updated"
}

Push-Location -LiteralPath $repoRoot
try {
  if (git rev-parse --is-inside-work-tree 2>$null) {
    git add -A
    git commit -m "chore: bump version to $next"
    git tag -a "v$next" -m "v$next"
    git push origin main
    git push origin "v$next"
    Write-Output "[bump-repo-version] git tag=v$next pushed"
  }
} finally {
  Pop-Location
}
