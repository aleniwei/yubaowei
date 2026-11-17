@echo off
cd /d "%~dp0"
where py >nul 2>nul
if %errorlevel%==0 (
  py -3 build.py
) else (
  python build.py
)
if errorlevel 1 (
  echo.
  echo Build failed. Please check Python installation and JSON syntax.
  pause
  exit /b 1
)
start "" "%~dp0site\index.html"
