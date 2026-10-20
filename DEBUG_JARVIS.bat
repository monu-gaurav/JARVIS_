@echo off
setlocal
cd /d "%~dp0"
title JARVIS - Debug
if not exist ".venv\Scripts\python.exe" (
  echo JARVIS is not installed yet. Run INSTALL_JARVIS.bat first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" "main.py"
echo.
echo JARVIS closed. If an error appeared above, save it for troubleshooting.
pause
