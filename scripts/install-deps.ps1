# Run from repo root when you have a stable internet connection
$ErrorActionPreference = "Stop"
Set-Location (Split-Path -Parent $PSScriptRoot)

Write-Host "Installing Python dependencies (OpenCV ~40MB may take several minutes)..."
.\.venv\Scripts\pip install -r requirements.txt
Write-Host "Done."
