$ErrorActionPreference = 'Stop'

$root = Split-Path -Parent $MyInvocation.MyCommand.Path
$registry = Join-Path $root 'registry'

function Clean-Markdown([string]$text) {
    if ([string]::IsNullOrWhiteSpace($text)) { return '' }
    $value = $text.Trim()
    $value = [regex]::Replace($value, '\[([^\]]+)\]\([^\)]+\)', '$1')
    $value = $value -replace '\*\*', ''
    $value = $value -replace '`', ''
    return $value.Trim()
}

function Get-Field([string]$block, [string[]]$labels) {
    foreach ($label in $labels) {
        $match = [regex]::Match($block, '(?m)^' + [regex]::Escape($label) + ':\s*(.+)$')
        if ($match.Success) { return Clean-Markdown $match.Groups[1].Value }
    }
    return ''
}

function Get-Sections([string]$path, [string]$prefix) {
    $content = Get-Content -LiteralPath $path -Raw -Encoding utf8
    $pattern = '(?ms)<a id="(' + $prefix.ToLower() + '-\d{2})"></a>\s*##\s+(' + $prefix + '-\d{2}):\s*(.+?)\r?\n(.*?)(?=<a id="(?:' + $prefix.ToLower() + '-\d{2}|[^\"]+)"></a>|\z)'
    return [regex]::Matches($content, $pattern)
}

function Get-SourceSections([string]$block) {
    $marker = '### Full source record and conditions'
    $index = $block.IndexOf($marker)
    if ($index -lt 0) { return @() }
    $full = $block.Substring($index + $marker.Length)
    $items = @()
    $matches = [regex]::Matches($full, '(?ms)^\*\*([^*]+?):\*\*\s*(.+?)(?=\r?\n\r?\n\*\*|\r?\n\r?\n###|\z)')
    foreach ($match in $matches) {
        $items += [ordered]@{
            label = (Clean-Markdown $match.Groups[1].Value)
            text = (Clean-Markdown (($match.Groups[2].Value -replace '\r?\n', ' ')))
        }
    }
    return $items
}

function Get-TableRow([string]$block, [string]$id) {
    foreach ($line in ($block -split "`r?`n")) {
        if ($line -match ('^\|\s*' + [regex]::Escape($id) + '(?:\s*/[^|]+)?\s*\|')) {
            $cells = @($line.Trim('|').Split('|') | ForEach-Object { Clean-Markdown $_ })
            return $cells
        }
    }
    return @()
}

$details = [ordered]@{}

foreach ($match in (Get-Sections (Join-Path $registry 'decisions-registry.md') 'ADR')) {
    $id = $match.Groups[2].Value
    $block = $match.Groups[4].Value
    $statements = @()
    foreach ($line in ($block -split "`r?`n")) {
        if ($line -match '^\|\s*(ADR-\d+-S\d+)\s*\|\s*([^|]+)\|\s*([^|]+)\|') {
            $statements += [ordered]@{ id = $Matches[1]; status = (Clean-Markdown $Matches[2]); text = (Clean-Markdown $Matches[3]) }
        }
    }
    $details[$id] = [ordered]@{
        kind = 'ADR'
        title = (Clean-Markdown $match.Groups[3].Value)
        context = (Get-Field $block @('Problem / Context'))
        owner = (Get-Field $block @('Decision owner'))
        closure = (Get-Field $block @('Closure condition'))
        accepted = (Get-Field $block @('Accepted decision'))
        proposed = (Get-Field $block @('Proposed options and Open details'))
        consequences = (Get-Field $block @('Consequences'))
        statements = $statements
        sourceSections = @(Get-SourceSections $block)
    }
}

foreach ($match in (Get-Sections (Join-Path $registry 'open-issues-registry.md') 'DL')) {
    $id = $match.Groups[2].Value
    $block = $match.Groups[4].Value
    $sourceRow = @(Get-TableRow $block $id)
    $details[$id] = [ordered]@{
        kind = 'DL'
        title = (Clean-Markdown $match.Groups[3].Value)
        status = (Get-Field $block @('Status'))
        requiredWork = (Get-Field $block @('Required work'))
        conflict = (Get-Field $block @('Exact conflict / missing evidence'))
        effect = (Get-Field $block @('Effect'))
        options = (Get-Field $block @('Existing options'))
        owner = (Get-Field $block @('Decision owner'))
        closure = (Get-Field $block @('Closure criterion'))
        dependencies = (Get-Field $block @('Dependencies'))
        additionalEvidence = (Get-Field $block @('Additional Source Evidence'))
        sourceRow = $sourceRow
    }
}

foreach ($match in (Get-Sections (Join-Path $registry 'acceptance-register.md') 'AT')) {
    $id = $match.Groups[2].Value
    $block = $match.Groups[4].Value
    $sourceRow = @(Get-TableRow $block $id)
    $details[$id] = [ordered]@{
        kind = 'AT'
        title = (Clean-Markdown $match.Groups[3].Value)
        goal = (Get-Field $block @('Goal'))
        status = (Get-Field $block @('Execution status'))
        authority = (Get-Field $block @('Reference contract / authority'))
        gap = (Get-Field $block @('Unapproved mechanism or gap'))
        evidence = (Get-Field $block @('Required evidence and acceptance checks'))
        related = (Get-Field $block @('تصمیم‌ها / مسائل مرتبط','Related decisions / issues'))
        sourceRow = $sourceRow
    }
}

$json = $details | ConvertTo-Json -Depth 8 -Compress
$output = 'window.recordDetails = ' + $json + ';'
Set-Content -LiteralPath (Join-Path $root 'adr-decision-details.js') -Value $output -Encoding utf8
Write-Output "Generated $($details.Count) record details."
