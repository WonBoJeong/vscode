@echo off
echo ==============================================
echo VStock Advanced - Quick Setup and Run
echo ==============================================
echo.

REM Install required libraries
echo Installing required libraries...
pip install pandas numpy matplotlib seaborn ta openpyxl scikit-learn scipy yfinance

if errorlevel 1 (
    echo.
    echo ERROR: Library installation failed.
    echo Trying with basic libraries only...
    pip install pandas numpy matplotlib
)

echo.
echo Installation completed!
echo.

REM Run the program
echo Starting VStock Advanced...
if exist "simple_main.py" (
    python simple_main.py
) else if exist "main.py" (
    python main.py
) else (
    echo ERROR: No main program file found.
    echo Please check if main.py or simple_main.py exists.
)

pause