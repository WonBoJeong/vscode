@echo off
chcp 65001 > nul
echo.
echo ========================================
echo   1Bo's Stock Analyzer v2.1
echo   Starting Application...
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo Please install Python 3.8+ and add to PATH
    pause
    exit /b 1
)

REM Install required packages if needed
echo Installing required packages...
pip install --quiet pandas numpy matplotlib yfinance requests Pillow

REM Run the application
echo.
echo Starting Stock Analyzer...
python main.py

echo.
echo Application closed.
pause