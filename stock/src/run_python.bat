@echo off
chcp 65001 >nul
echo 🐍 VStock Advanced - Python 실시간 다운로드 통합 버전
echo ================================================
echo.

REM Python 및 라이브러리 확인
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python이 설치되지 않았습니다.
    echo 💡 https://python.org 에서 Python 3.8 이상을 설치해주세요.
    pause
    exit /b 1
)

echo ✅ Python 확인 완료
python --version

REM 기본 라이브러리 확인
echo.
echo 📚 기본 라이브러리 확인 중...
python -c "import pandas, numpy, matplotlib, tkinter" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ 기본 라이브러리 설치 필요
    pip install pandas numpy matplotlib
)

REM yfinance 확인
echo 📊 yfinance 라이브러리 확인 중...
python -c "import yfinance" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ yfinance가 설치되지 않았습니다.
    echo 💾 yfinance 설치를 시작합니다...
    pip install yfinance
    
    if errorlevel 1 (
        echo ❌ yfinance 설치 실패
        echo 💡 수동 설치: pip install yfinance
        echo 🔧 yfinance 없이도 기본 기능은 사용 가능합니다
    ) else (
        echo ✅ yfinance 설치 완료!
    )
) else (
    echo ✅ yfinance 사용 가능
)

echo.
echo 🎯 VStock Advanced 통합 버전 실행
echo ================================================
echo.
echo ✨ 주요 기능:
echo • 📥 실시간 Yahoo Finance 데이터 다운로드
echo • 📊 즉시 차트 분석 (캔들스틱 + RSI + 이동평균)
echo • 🚀 레버리지 ETF 전문 지원
echo • 📈 일괄 다운로드 (레버리지ETF/인기종목/전체)
echo • 💾 자동 파일 저장 및 관리
echo.
echo 🎮 사용법:
echo • 종목 입력 후 "📊 분석+다운" 클릭
echo • 또는 빠른 선택 버튼 활용  
echo • 일괄 다운로드로 여러 종목 한번에 수집
echo.
echo 📊 지원 종목:
echo • 레버리지 ETF: TQQQ, SOXL, FNGU, TNA, TECL 등
echo • 인기 종목: AAPL, TSLA, NVDA, MSFT, GOOGL 등
echo.

REM 데이터 폴더 생성
if not exist "data" mkdir data

REM 실행 파일 우선순위
if exist "integrated_main.py" (
    echo 🚀 통합 다운로드 버전으로 실행...
    python integrated_main.py
) else if exist "r_main.py" (
    echo 🔗 R 연동 버전으로 실행...
    python r_main.py
) else if exist "simple_main.py" (
    echo 🎯 간단 버전으로 실행...
    python simple_main.py
) else if exist "main.py" (
    echo 🎯 기본 버전으로 실행...
    python main.py
) else (
    echo ❌ 실행 파일을 찾을 수 없습니다.
    pause
    exit /b 1
)

REM 종료 처리
if errorlevel 1 (
    echo.
    echo ❌ 프로그램 실행 중 오류가 발생했습니다.
    echo.
    echo 💡 문제 해결 가이드:
    echo   1. yfinance 설치: pip install yfinance
    echo   2. 인터넷 연결 확인 (실시간 다운로드용)
    echo   3. 방화벽 설정 확인
    echo   4. Python 라이브러리 재설치
    echo.
    pause
) else (
    echo.
    echo ✅ 프로그램이 정상적으로 종료되었습니다.
)

echo.
echo 🎉 Python 실시간 주식 분석을 이용해주셔서 감사합니다!
echo 💡 새로운 종목을 다운로드하려면 언제든지 다시 실행하세요.
pause