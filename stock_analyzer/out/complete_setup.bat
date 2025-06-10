@echo off
echo =============================================
echo VStock Advanced - Complete Setup and Run
echo =============================================
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed!
    echo Please install Python from https://python.org
    pause
    exit /b 1
)

echo Python found: 
python --version
echo.

REM Install libraries
echo Step 1: Installing required libraries...
pip install pandas numpy matplotlib seaborn

echo.
echo Step 2: Creating sample data...
python create_sample_data_eng.py

echo.
echo Step 3: Starting VStock Advanced...
if exist "simple_main.py" (
    echo Running simple version...
    python simple_main.py
) else (
    echo Running full version...
    python main.py
)

echo.
echo Program finished.
pause