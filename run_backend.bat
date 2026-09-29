@echo off
cd /d %~dp0backend
if not exist .venv (
  py -m venv .venv 2>nul || python -m venv .venv
)
call .venv\Scripts\activate.bat
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8000
