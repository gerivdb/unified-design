#!/usr/bin/env pwsh
# pre-push-ethics-check.ps1 — Validation éthique transversale avant push
# IntentHash: 0xPRE_PUSH_ETHICS_CHECK_20260920
# Référence: PRD-MOC-ETHIQUE-TRANSVERSALE-HOOKS-2026-09-20

$ErrorActionPreference = 'Stop'

function Get-GitRepoRoot {
    return (git rev-parse --show-toplevel).Trim()
}

function Invoke-WazaaPathology {
    param(
        [string]$Message,
        [string]$Severity = 'blocking'
    )
    
    $wazaaScript = Join-Path $RepoRoot 'scripts\governance_wazaa_subscriber.py'
    if (-not (Test-Path $wazaaScript)) {
        Write-Host '[ETHICS] WAZAA subscriber not found, skipping pathology event'
        return
    }
    
    $timestamp = (Get-Date).ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ')
    $bodyJson = '{"topic":"pathology","severity":"' + $Severity + '","message":"' + $Message + '","repo":"' + $RepoRoot + '","timestamp_utc":"' + $timestamp + '"}'
    
    try {
        python $wazaaScript --send-pathology $bodyJson 2>&1 | Out-Null
        Write-Host ('[ETHICS] WAZAA pathology event sent: ' + $Message)
    } catch {
        Write-Host ('[ETHICS] WARNING: Failed to send WAZAA pathology event: ' + $_.Exception.Message)
    }
}

function Test-PrivateField {
    param([string]$Path)
    
    if (-not (Test-Path $Path)) {
        return $true
    }
    
    try {
        $content = Get-Content $Path -Raw
        if ($content -notmatch 'entity_type:\s*REPO') {
            return $true
        }
        
        $lines = Get-Content $Path
        $inRepoBlock = $false
        $hasEntityType = $false
        $hasPrivate = $false
        
        foreach ($line in $lines) {
            if ($line -match '^\s*entity_type:\s*REPO') {
                $hasEntityType = $true
                $inRepoBlock = $true
            }
            elseif ($inRepoBlock -and $line -match '^\s*private:') {
                $hasPrivate = $true
                $inRepoBlock = $false
            }
            elseif ($inRepoBlock -and $line -match '^\s*\w+:\s*\w+') {
                # Nouveau champ, continuer dans le bloc
            }
            elseif ($inRepoBlock -and $line -match '^-') {
                # Nouvelle entrée YAML
                $inRepoBlock = $false
                if ($hasEntityType -and -not $hasPrivate) {
                    Write-Host ('[ETHICS] FAIL: ' + $Path + ' — missing private field in REPO entry')
                    Invoke-WazaaPathology -Message ('Missing private field in ' + $Path) -Severity 'blocking'
                    return $false
                }
                $hasEntityType = $false
                $hasPrivate = $false
            }
        }
        
        # Vérifier la dernière entrée
        if ($hasEntityType -and -not $hasPrivate) {
            Write-Host ('[ETHICS] FAIL: ' + $Path + ' — missing private field in REPO entry')
            Invoke-WazaaPathology -Message ('Missing private field in ' + $Path) -Severity 'blocking'
            return $false
        }
        
        return $true
    } catch {
        Write-Host ('[ETHICS] ERROR parsing ' + $Path + ' : ' + $_.Exception.Message)
        return $false
    }
}

$RepoRoot = Get-GitRepoRoot

# Fichiers SOT à vérifier
$sotFiles = @(
    'known_repositories.yaml',
    'AGENT_RAM.yaml',
    'BRIDGES.yaml'
)

$allOk = $true
foreach ($file in $sotFiles) {
    $fullPath = Join-Path $RepoRoot $file
    if (-not (Test-PrivateField -Path $fullPath)) {
        $allOk = $false
    }
}

if (-not $allOk) {
    Write-Host '[ETHICS] BLOCKED: Ethical validation failed — fix before push'
    exit 1
}

Write-Host '[ETHICS] OK: Ethical validation passed'
exit 0
