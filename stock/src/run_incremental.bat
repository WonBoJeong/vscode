@echo off
chcp 65001 >nul
echo 🚀 VStock Advanced - 스마트 증분 업데이트 시스템
echo ================================================
echo.

REM Python 확인
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

REM yfinance 확인 및 설치
echo 📊 yfinance 라이브러리 확인 중...
python -c "import yfinance" >nul 2>&1
if errorlevel 1 (
    echo ⚠️ yfinance가 설치되지 않았습니다.
    echo 💾 yfinance 설치를 시작합니다...
    pip install yfinance
    
    if errorlevel 1 (
        echo ❌ yfinance 설치 실패
        echo 💡 수동 설치: pip install yfinance
        echo 🔧 yfinance 없이도 기존 파일 분석은 가능합니다
    ) else (
        echo ✅ yfinance 설치 완료!
    )
) else (
    echo ✅ yfinance 사용 가능
)

echo.
echo 🎯 스마트 증분 업데이트 시스템 실행
echo ================================================
echo.
echo ✨ 핵심 기능:
echo • 📁 파일명: 종목명_날짜.csv (예: TQQQ_20250109.csv)
echo • 🔄 증분 업데이트: 마지막 날짜 이후 데이터만 추가
echo • 📊 완전한 분석: 수년간 누적 데이터로 정확한 기술적 분석
echo • 💾 효율적 저장: 중복 다운로드 방지, 빠른 업데이트
echo.
echo 🎮 사용법:
echo • 종목 입력 후 "📊 업데이트+분석" 클릭
echo • 기존 파일 있으면 → 증분 업데이트 후 분석
echo • 기존 파일 없으면 → 3년 데이터 다운로드 후 분석
echo • 일괄 업데이트로 여러 종목 한번에 관리
echo.
echo 💡 장점:
echo • ⚡ 빠른 업데이트 (새 데이터만 다운로드)
echo • 📈 완전한 분석 (전체 히스토리 데이터)
echo • 💾 공간 절약 (중복 제거, 최신 파일만 유지)
echo • 🔄 자동 파일 관리 (오래된 버전 정리)
echo.

REM 데이터 폴더 생성
if not exist "data" mkdir data

REM 실행 파일 우선순위 (증분 업데이트 버전 우선)
if exist "incremental_main.py" (
    echo 🔄 증분 업데이트 시스템으로 실행...
    python incremental_main.py
) else if exist "integrated_main.py" (
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
    echo   5. 데이터 폴더 권한 확인
    echo.
    pause
) else (
    echo.
    echo ✅ 프로그램이 정상적으로 종료되었습니다.
)

echo.
echo 🎉 스마트 증분 업데이트 시스템을 이용해주셔서 감사합니다!
echo 💡 매일 간단한 업데이트로 최신 데이터와 함께 정확한 분석을 즐기세요.
pause