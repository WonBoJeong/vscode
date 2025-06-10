@echo off
echo Starting VStock Advanced Stock Analysis Program
echo ================================================
echo.

REM Check current directory
echo Current location: %CD%
echo.

REM Check Python installation
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed.
    echo Please install Python 3.8 or higher from https://python.org
    pause
    exit /b 1
)

echo Python check completed
python --version

REM Check required libraries
echo.
echo Checking required libraries...
python -c "import pandas, numpy, matplotlib, tkinter" >nul 2>&1
if errorlevel 1 (
    echo WARNING: Required libraries are not installed.
    echo Starting library installation...
    echo.
    pip install pandas numpy matplotlib
    if errorlevel 1 (
        echo ERROR: Library installation failed.
        echo Please check internet connection or install manually:
        echo    pip install pandas numpy matplotlib
        pause
        exit /b 1
    )
)

echo All libraries check completed
echo.

REM Check data folder
if not exist "data" (
    echo Creating data folder...
    mkdir data
)

if not exist "data\AAPL.csv" (
    echo Sample data not found. Sample data should already be created.
    echo Please check if files like AAPL.csv, TSLA.csv exist in data folder.
)

REM Run the program
echo Starting VStock Advanced...
echo Stock symbols example: AAPL, TSLA, MSFT, GOOGL, PLTR
echo.

REM Try to run simple version first
if exist "simple_main.py" (
    echo Running simple version...
    python simple_main.py
) else if exist "main.py" (
    echo Running full version...
    python main.py
) else (
    echo ERROR: Cannot find execution file.
    echo Please check if main.py or simple_main.py exists.
    pause
    exit /b 1
)

REM Handle program exit
if errorlevel 1 (
    echo.
    echo ERROR: An error occurred while running the program.
    echo Please check the error message and try again.
    echo.
    pause
) else (
    echo.
    echo Program terminated normally.
)

echo.
echo Thank you for using VStock Advanced!
pause