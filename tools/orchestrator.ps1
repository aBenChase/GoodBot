# Serial orchestrator (v0 skeleton). Runs ONE queued task at a time under a
# turn-lease, then auto-commits that agent's changes with an Agent trailer.
# DRY-RUN by default -- pass -Execute to actually launch agents and commit.
#
# Queue: queue/pending/*.json (oldest first). Task shape:
#   { "agent":"claude|openai", "title":"...", "prompt":"...", "worktree":"../gb-claude" }
# Launch commands come from tools/orchestrator.config.json (see the .example).
[CmdletBinding()]
param(
  [switch]$Execute,
  [int]$LeaseMinutes = 30
)
$ErrorActionPreference = 'Stop'
$repo = (git rev-parse --show-toplevel).Trim()
Set-Location $repo
$lock = 'shared/TURN.lock'
$cfgPath = 'tools/orchestrator.config.json'
$cfg = if (Test-Path $cfgPath) { Get-Content $cfgPath -Raw | ConvertFrom-Json } else { $null }

function Read-Lock { if (Test-Path $lock) { try { Get-Content $lock -Raw | ConvertFrom-Json } catch { $null } } }
function Lease-Held {
  $l = Read-Lock
  if (-not $l) { return $false }
  return ([datetime]$l.expires -gt (Get-Date).ToUniversalTime())
}
function Acquire($agent, $title) {
  $now = (Get-Date).ToUniversalTime()
  $o = [ordered]@{ holder = $agent; title = $title; since = $now.ToString('o'); expires = $now.AddMinutes($LeaseMinutes).ToString('o') }
  ($o | ConvertTo-Json -Compress) | Set-Content -Path $lock -Encoding utf8
}
function Release { if (Test-Path $lock) { Remove-Item $lock -Force } }

$tasks = Get-ChildItem 'queue/pending' -Filter *.json -ErrorAction SilentlyContinue | Sort-Object Name
if (-not $tasks) { Write-Host 'queue empty.'; return }

foreach ($t in $tasks) {
  $task = Get-Content $t.FullName -Raw | ConvertFrom-Json
  $agent = $task.agent
  if (Lease-Held) { Write-Host "lease held by $((Read-Lock).holder); stopping."; break }
  Write-Host "---- $($task.title) [$agent] ----"
  if (-not $Execute) { Write-Host 'DRY-RUN: would lease -> launch -> auto-commit -> release.'; continue }

  Acquire $agent $task.title
  try {
    $ac = $cfg.$agent
    if (-not $ac) { throw "no config for agent '$agent' in $cfgPath" }
    $pf = New-TemporaryFile
    Set-Content -Path $pf -Value $task.prompt -Encoding utf8
    $cmd = @($ac.command | ForEach-Object { $_ -replace '\{PROMPT_FILE\}', $pf })
    $cwd = if ($ac.cwd) { $ac.cwd } else { $repo }
    Write-Host "launch: $($cmd -join ' ')  (cwd=$cwd)"
    Push-Location $cwd
    & $cmd[0] @($cmd[1..($cmd.Count - 1)]); $code = $LASTEXITCODE
    Pop-Location
    Remove-Item $pf -Force
    $wt = if ($task.worktree) { $task.worktree } else { $repo }
    git -C $wt add -A
    git -C $wt commit -F - <<EOF
$($task.title)

Agent: $agent
EOF
    Write-Host "committed (agent exit=$code)."
    Move-Item $t.FullName (Join-Path 'queue/done' $t.Name) -Force
  }
  finally { Release }
}
