@echo off
cd /d "%~dp0\frontend"
echo Installing dependencies (if needed)...
call npm install
echo Starting Frontend...
npm run dev
pause
