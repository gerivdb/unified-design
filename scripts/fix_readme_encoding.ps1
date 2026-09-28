$content = Get-Content 'D:\DO\WEB\TOOLS\L0-CANON\unified-design\README.md' -Raw
$tmp = [System.IO.Path]::GetTempFileName()
Set-Content -LiteralPath $tmp -Value $content -Encoding UTF8
Move-Item -LiteralPath $tmp -Destination 'D:\DO\WEB\TOOLS\L0-CANON\unified-design\README.md' -Force
Write-Output "README.md encoding fixed"
