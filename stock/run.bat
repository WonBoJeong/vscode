@echo off
chcp 65001 >nul
echo 🚀 VStock Advanced 주식 분석 프로그램
echo ================================================
echo.

REM 현재 디렉토리 확인
echo 📁 현재 위치: %CD%
echo.

REM Python 설치 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo 💡 https://python.org 에서 Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

echo ✅ Python 확인 완료
python --version

REM 필요한 라이브러리 확인
echo.
echo 📚 필요한 라이브러리 확인 중...
python -c "import pandas, numpy, matplotlib, tkinter" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 필요한 라이브러리가 설치되지 않았습니다.
    echo 💾 라이브러리 설치를 시작합니다...
    echo.
    pip install pandas numpy matplotlib
    if errorlevel 1 (
        echo ❌ 라이브러리 설치에 실패했습니다.
        echo 💡 인터넷 연결을 확인하거나 수동으로 설치해주세요:
        echo    pip install pandas numpy matplotlib
        pause
        exit /b 1
    )
)

echo ✅ 모든 라이브러리 확인 완료
echo.

REM 데이터 폴더 확인
if not exist "data" (
    echo 📂 데이터 폴더를 생성합니다...
    mkdir data
)

if not exist "data\AAPL.csv" (
    echo 📊 샘플 데이터가 없습니다. 샘플 데이터가 이미 생성되어 있어야 합니다.
    echo 💡 data 폴더에 AAPL.csv, TSLA.csv 등의 파일이 있는지 확인해주세요.
)

REM 프로그램 실행
echo ✨ VStock Advanced를 시작합니다...
echo ⭐ 종목 코드 예시: AAPL, TSLA, MSFT, GOOGL, PLTR
echo.

REM 먼저 간단 버전 실행 시도
if exist "simple_main.py" (
    echo 🎯 간단 버전으로 실행합니다...
    python simple_main.py
) else if exist "main.py" (
    echo 🎯 전체 버전으로 실행합니다...
    python main.py
) else (
    echo ❌ 실행 파일을 찾을 수 없습니다.
    echo 💡 main.py 또는 simple_main.py 파일이 있는지 확인해주세요.
    pause
    exit /b 1
)

REM 프로그램 종료 후 처리
if errorlevel 1 (
    echo.
    echo ❌ 프로그램 실행 중 오류가 발생했습니다.
    echo 💡 오류 내용을 확인하고 다시 시도해주세요.
    echo.
    pause
) else (
    echo.
    echo ✅ 프로그램이 정상적으로 종료되었습니다.
)

echo.
echo 👋 VStock Advanced를 이용해주셔서 감사합니다!
pause