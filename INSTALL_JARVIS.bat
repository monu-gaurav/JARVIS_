@echo off
setlocal
cd /d "%~dp0"
title JARVIS - Install

echo.
echo  ======================================
echo          J A R V I S  -  INSTALL
echo  ======================================
echo.

where py >nul 2>nul
if errorlevel 1 (
  echo Python Launcher was not found.
  echo Install Python 3.12 x64 from https://www.python.org/downloads/windows/
  echo During setup, enable the Python Launcher and Add Python to PATH.
  pause
  exit /b 1
)

py -3.12 --version >nul 2>nul
if errorlevel 1 (
  echo Python 3.12 was not found.
  echo Install Python 3.12 x64 from https://www.python.org/downloads/windows/
  echo Then run this installer again.
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [1/3] Creating the JARVIS environment...
  py -3.12 -m venv .venv
  if errorlevel 1 goto :failed
)

echo [2/3] Updating pip...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto :failed

echo [3/3] Installing JARVIS dependencies. This may take a while...
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto :failed

echo.
echo Installation complete.
echo Run START_JARVIS.bat to open the animated corner orb.
echo If anything goes wrong, run DEBUG_JARVIS.bat and read the error shown.
pause
exit /b 0

:failed
echo.
echo Installation failed. Check your Internet connection and run this file again.
echo For details, rerun the installer or open DEBUG_JARVIS.bat after setup.
pause
exit /b 1
