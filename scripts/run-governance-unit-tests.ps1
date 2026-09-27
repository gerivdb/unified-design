<#
.SYNOPSIS
    Run governance unit tests with command resolution.
    Implements Command Resolution Protocol: resolves python/pytest before execution.
.DESCRIPTION
    This script demonstrates the command resolution protocol:
    - Resolves external commands before execution
    - Falls back to common install paths
    - Fails loudly if command not found
#>

param(
    [string[]]$TestPath = "tests",
    [switch]$Verbose
)

$ErrorActionPreference = "Stop"

# Command Resolution Protocol
function Resolve-Command {
    param(
        [string]$CommandName,
        [string[]]$FallbackPaths = @()
    )
    
    # Try Get-Command first
    $cmd = Get-Command $CommandName -ErrorAction SilentlyContinue
    if ($cmd) {
        return $cmd.Source
    }
    
    # Try fallback paths
    foreach ($path in $FallbackPaths) {
        if (Test-Path $path) {
            return $path
        }
    }
    
    throw "Command '$CommandName' not found in PATH or common install paths."
}

# Resolve python
try {
    $pythonPath = Resolve-Command -CommandName "python" -FallbackPaths @(
        Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe",
        Join-Path $env:LOCALAPPDATA "Programs\Python\Python311\python.exe",
        Join-Path $env:PROGRAMFILES "Python312\python.exe",
        Join-Path $env:PROGRAMFILES "Python311\python.exe"
    )
    Write-Host "[CMD-RESOLVE] python -> $pythonPath" -ForegroundColor Green
} catch {
    Write-Error $_.Exception.Message
    exit 1
}

# Resolve pytest (optional, used as module)
$pytestModule = "pytest"
Write-Host "[CMD-RESOLVE] pytest -> module ($pytestModule)" -ForegroundColor Green

# Run tests with resolved python
$args = @("$pytestModule", $TestPath)
if ($Verbose) {
    $args += "-v"
}

Write-Host "[RUN] $pythonPath $($args -join ' ')" -ForegroundColor Cyan
& $pythonPath @args 2>&1
exit $LASTEXITCODE
