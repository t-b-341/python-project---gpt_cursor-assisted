# Stop tracking build/cache/profiling/DB/plot artifacts. Run once after adding .gitignore.
# Close other git processes first. Usage: .\untrack_artifacts.ps1

Set-Location $PSScriptRoot
if (Test-Path ".git\index.lock") { Remove-Item ".git\index.lock" -Force }

$actions = @(
    { git rm -r --cached __pycache__ },
    { git rm -r --cached entities/__pycache__ },
    { git rm -r --cached screens/__pycache__ },
    { git rm -r --cached systems/__pycache__ },
    { git rm -r --cached telemetry/__pycache__ },
    { git rm -r --cached build },
    { git rm --cached game_physics.cp312-win_amd64.pyd },
    { git rm --cached game_telemetry.db game_telemetry.db-shm game_telemetry.db-wal high_scores.db },
    { git rm --cached profiling_results.prof profiling_results.txt },
    { git rm -r --cached telemetry_plots }
)
foreach ($a in $actions) {
    try { & $a } catch { }
}
Write-Host "Done. Run: git status"
