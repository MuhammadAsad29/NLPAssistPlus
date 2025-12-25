@echo off
cd /d "%~dp0"
call .venv\Scripts\activate
echo Starting Backend...
python -m uvicorn main:app --app-dir backend --reload --port 8000
pause
