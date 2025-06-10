@echo off
echo Starting VStock Simple Data Downloader...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

REM Install required packages if needed
echo Checking required packages...
python -c "import pandas, yfinance" >nul 2>&1
if errorlevel 1 (
    echo Installing required packages...
    pip install pandas yfinance
    if errorlevel 1 (
        echo ERROR: Failed to install packages
        pause
        exit /b 1
    )
)

REM Run the application
echo.
echo Starting VStock Simple...
python vstock_simple.py

if errorlevel 1 (
    echo.
    echo Program encountered an error.
    echo Please check the error message above.
    pause
)
