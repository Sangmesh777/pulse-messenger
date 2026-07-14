@echo off
cd /d "%~dp0"
where python >nul 2>nul
if %errorlevel% neq 0 (
  echo Python 3 is not installed.
  echo Install it from https://www.python.org/downloads/ and enable "Add Python to PATH".
  pause
  exit /b 1
)
start "" http://localhost:8000
python server.py
pause
