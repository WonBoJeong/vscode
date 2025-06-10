@echo off
echo Installing Python packages for 1Bo's Plan...
echo.

echo [1/6] Installing matplotlib...
pip install matplotlib
if errorlevel 1 echo Failed to install matplotlib

echo [2/6] Installing pandas...
pip install pandas
if errorlevel 1 echo Failed to install pandas

echo [3/6] Installing numpy...
pip install numpy
if errorlevel 1 echo Failed to install numpy

echo [4/6] Installing yfinance...
pip install yfinance
if errorlevel 1 echo Failed to install yfinance

echo [5/6] Installing requests...
pip install requests
if errorlevel 1 echo Failed to install requests

echo [6/6] Installing Pillow...
pip install Pillow
if errorlevel 1 echo Failed to install Pillow

echo.
echo Package installation completed!
echo You can now run: python main.py
echo.
pause