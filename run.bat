@echo off
setlocal

REM Activate the virtual environment
call .\.venv\Scripts\activate.bat

REM Start Ingest
start "INGEST" cmd /k "call .\.venv\Scripts\activate.bat && cd /d %cd% && python -m app.ingest"

REM Start Processor
start "PROCESSOR" cmd /k "call .\.venv\Scripts\activate.bat && cd /d %cd% && python -m app.processor"

REM Start API
start "API" cmd /k "call .\.venv\Scripts\activate.bat && cd /d %cd% && uvicorn app.api:app --reload --port 8000"
