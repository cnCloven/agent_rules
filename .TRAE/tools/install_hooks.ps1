param(
  [string]$RepoRoot = ""
)

if ([string]::IsNullOrWhiteSpace($RepoRoot)) {
  $RepoRoot = (git rev-parse --show-toplevel)
}

Set-Location $RepoRoot
git config core.hooksPath ".TRAE/.githooks"
Write-Output "Installed git hooks path: .TRAE/.githooks"

