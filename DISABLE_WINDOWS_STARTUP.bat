@echo off
setlocal
set "STARTUP=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\JARVIS.lnk"
if exist "%STARTUP%" del "%STARTUP%"
echo JARVIS will no longer start automatically when you sign in.
pause
