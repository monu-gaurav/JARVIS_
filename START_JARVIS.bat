@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\pythonw.exe" (
  echo JARVIS is not installed yet. Run INSTALL_JARVIS.bat first.
  pause
  exit /b 1
)
start "" ".venv\Scripts\pythonw.exe" "main.py"
exit /b 0
