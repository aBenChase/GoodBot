# Manage per-agent git worktrees for collision-free parallel work.
#   pwsh tools/worktrees.ps1 create   # branches + worktrees + per-agent identity
#   pwsh tools/worktrees.ps1 list
#   pwsh tools/worktrees.ps1 remove   # removes worktrees, keeps branches
[CmdletBinding()]
param(
  [Parameter(Position = 0)][ValidateSet('create', 'list', 'remove')]
  [string]$Action = 'list',
  [string]$Root
)
$ErrorActionPreference = 'Stop'
$repo = (git rev-parse --show-toplevel).Trim()
if (-not $Root) { $Root = Split-Path $repo -Parent }   # default: sibling of the repo

$agents = @(
  @{ name = 'claude'; branch = 'claude/work'; path = (Join-Path $Root 'gb-claude') },
  @{ name = 'openai'; branch = 'openai/work'; path = (Join-Path $Root 'gb-openai') }
)

function Ensure-Branch($branch) {
  git show-ref --verify --quiet "refs/heads/$branch"
  if ($LASTEXITCODE -ne 0) { git branch $branch; Write-Host "created branch $branch" }
}

switch ($Action) {
  'create' {
    git config extensions.worktreeConfig true   # enable per-worktree config (GB-R005)
    foreach ($a in $agents) {
      Ensure-Branch $a.branch
      if (Test-Path $a.path) { Write-Host "exists: $($a.path)" }
      else { git worktree add $a.path $a.branch }
      git -C $a.path config core.hooksPath 'tools/git-hooks'
      git -C $a.path config --worktree goodbot.agent $a.name
      Write-Host "ready: $($a.name) -> $($a.path)  [goodbot.agent=$($a.name)]"
    }
    Write-Host ""
    Write-Host "Launch each agent inside its own worktree; merge to main via commit/PR."
  }
  'list' { git worktree list }
  'remove' {
    foreach ($a in $agents) {
      if (Test-Path $a.path) { git worktree remove $a.path --force }
    }
    git worktree prune
    Write-Host "worktrees removed (branches kept)."
  }
}
