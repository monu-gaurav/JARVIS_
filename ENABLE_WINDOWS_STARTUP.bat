@echo off
setlocal
cd /d "%~dp0"
set "JARVIS_DIR=%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "$target = Join-Path $env:JARVIS_DIR 'START_JARVIS.bat'; $startup = [Environment]::GetFolderPath('Startup'); $w = New-Object -ComObject WScript.Shell; $s = $w.CreateShortcut((Join-Path $startup 'JARVIS.lnk')); $s.TargetPath = $target; $s.WorkingDirectory = $env:JARVIS_DIR; $s.WindowStyle = 7; $s.Description = 'Launch the JARVIS animated assistant orb'; $s.Save()"
if errorlevel 1 (
  echo Could not create the Startup shortcut.
  pause
  exit /b 1
)
echo JARVIS will start when you sign in to Windows.
pause
