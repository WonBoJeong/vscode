@echo off
echo Installing required packages...
pip install matplotlib pandas numpy yfinance requests Pillow

echo.
echo Starting 1Bo's Plan v2.0.0...
python main.py

echo.
pause