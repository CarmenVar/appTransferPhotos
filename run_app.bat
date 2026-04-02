@echo off
echo Starting Cloud Photo Transfer App in a clean environment...
.\venv\Scripts\python main.py
if %ERRORLEVEL% neq 0 (
    echo.
    echo Application exited with error code %ERRORLEVEL%.
    pause
)
