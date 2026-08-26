# Activates Good Bot's tracked git hooks for this clone or worktree.
# Run once per clone/worktree:  pwsh tools/setup-hooks.ps1
$ErrorActionPreference = 'Stop'

$repo = (git rev-parse --show-toplevel).Trim()
git config core.hooksPath 'tools/git-hooks'
Write-Host "core.hooksPath -> tools/git-hooks"
Write-Host "Good Bot hooks active in: $repo"
Write-Host "Guarded: private/, logs/raw|review|staging/, secrets, queue state, TURN.lock;"
Write-Host "Required: an 'Agent: claude|openai|shared' trailer on every commit."
Write-Host ""
Write-Host "Note: per-worktree identity (goodbot.agent) is set by tools/worktrees.ps1."
Write-Host "Do NOT set goodbot.agent in a shared working dir - both agents use it."
