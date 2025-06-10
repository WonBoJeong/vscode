@echo off
chcp 65001 >nul
echo 🚀 VStock Advanced - R quantmod 연동 버전
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
        pause
        exit /b 1
    )
)

echo ✅ 모든 라이브러리 확인 완료
echo.

REM R 데이터 경로 확인
echo 🔍 R quantmod 데이터 경로 확인 중...

set "R_PATHS[0]=D:\R_stats\R_stock\data"
set "R_PATHS[1]=C:\R_stats\R_stock\data"
set "R_PATHS[2]=%USERPROFILE%\R_stats\R_stock\data"
set "R_PATHS[3]=..\R_stock\data"

set "R_FOUND=0"
for /l %%i in (0,1,3) do (
    call set "current_path=%%R_PATHS[%%i]%%"
    if exist "!current_path!" (
        echo ✅ R 데이터 경로 발견: !current_path!
        set "R_FOUND=1"
        goto :r_check_done
    )
)

:r_check_done
if "%R_FOUND%"=="0" (
    echo ⚠️ R quantmod 데이터 경로를 찾을 수 없습니다.
    echo 💡 다음 중 한 경로에 R 스크립트 데이터가 있어야 합니다:
    echo    • D:\R_stats\R_stock\data\
    echo    • C:\R_stats\R_stock\data\
    echo    • %USERPROFILE%\R_stats\R_stock\data\
    echo.
    echo 📋 R 스크립트에서 다음 명령으로 데이터를 다운로드하세요:
    echo    setwd("~/R_stats/R_stock/")
    echo    library(quantmod)
    echo    d(pkgcode, key)
    echo.
    echo 🎯 샘플 데이터로 실행하려면 계속 진행하세요.
    echo.
)

REM 프로그램 실행
echo ✨ VStock Advanced R 연동 버전을 시작합니다...
echo.
echo 🎯 지원 기능:
echo • R quantmod 스크립트 데이터 자동 연동
echo • 레버리지 ETF 전문 분석 (TQQQ, SOXL, FNGU 등)
echo • 실시간 차트 및 기술적 지표
echo • RSI, 이동평균, 거래량 분석
echo.
echo 📊 지원 종목 예시:
echo • TQQQ, SOXL, FNGU, TNA, TECL, LABU
echo • RETL, WEBL, DPST, NAIL, HIBL
echo.

REM R 연동 버전 실행
if exist "r_main.py" (
    echo 🔗 R 연동 버전으로 실행합니다...
    python r_main.py
) else if exist "simple_main.py" (
    echo 🎯 간단 버전으로 실행합니다...
    python simple_main.py
) else if exist "main.py" (
    echo 🎯 기본 버전으로 실행합니다...
    python main.py
) else (
    echo ❌ 실행 파일을 찾을 수 없습니다.
    echo 💡 r_main.py, main.py 또는 simple_main.py 파일이 필요합니다.
    pause
    exit /b 1
)

REM 프로그램 종료 후 처리
if errorlevel 1 (
    echo.
    echo ❌ 프로그램 실행 중 오류가 발생했습니다.
    echo.
    echo 💡 문제 해결 가이드:
    echo   1. R 스크립트로 데이터 다운로드 확인
    echo   2. 데이터 파일이 SYMBOL_YYMMDD.csv 형식인지 확인
    echo   3. Python 라이브러리 재설치: pip install pandas numpy matplotlib
    echo   4. 프로그램 내 '📂 R 경로' 버튼으로 수동 설정
    echo.
    pause
) else (
    echo.
    echo ✅ 프로그램이 정상적으로 종료되었습니다.
)

echo.
echo 🎯 R quantmod 연동 주식 분석을 이용해주셔서 감사합니다!
echo 💡 새로운 ETF 데이터를 다운로드한 후 '🔄 새로고침' 버튼을 활용하세요.
pause