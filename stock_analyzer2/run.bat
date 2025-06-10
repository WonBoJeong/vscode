@echo off
chcp 65001 > nul
echo Starting 1Bo's Plan v2.0.0...
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python version:
python --version
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo Failed to create virtual environment
        echo Please check Python installation
        pause
        exit /b 1
    )
    echo Virtual environment created successfully.
    echo.
)

echo Activating virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo Failed to activate virtual environment
    echo Trying to run without virtual environment...
    goto :skip_venv
)

echo Installing/updating requirements...
echo This may take a few minutes on first run...
pip install --upgrade pip
pip install -r requirements.txt
if errorlevel 1 (
    echo Package installation failed
    echo Trying to install packages individually...
    pip install matplotlib
    pip install pandas
    pip install numpy
    pip install yfinance
    pip install requests
    pip install Pillow
)

goto :run_app

:skip_venv
echo Running without virtual environment...
echo Installing packages globally...
pip install matplotlib pandas numpy yfinance requests Pillow

:run_app
echo.
echo Starting 1Bo's Plan...
echo.

REM Run the application
python main.py

echo.
echo Application closed.
pause