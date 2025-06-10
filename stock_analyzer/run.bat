@echo off
echo =============================================
echo VStock Advanced - Real Stock Data Analyzer
echo =============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python 3.8+ from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Install required libraries
echo Installing required libraries...
pip install pandas numpy matplotlib seaborn yfinance requests

if errorlevel 1 (
    echo.
    echo WARNING: Some libraries failed to install.
    echo Trying to install basic libraries only...
    pip install pandas numpy matplotlib yfinance
)

echo.
echo Starting VStock Advanced...
python vstock_main.py

if errorlevel 1 (
    echo.
    echo Program encountered an error.
    echo Please check the error message above.
)

echo.
pause