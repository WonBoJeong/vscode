@echo off
echo 의료기관 개폐업 현황 분석 프로젝트 시작하기
echo ======================================

cd /d F:\startcoding\medical-stats

echo 필요한 패키지 설치 중...
call npm install

echo.
echo 설치 완료! 개발 서버를 시작합니다...
echo 브라우저에서 http://localhost:3000 주소로 접속하세요.
echo.
echo 종료하려면 이 창에서 Ctrl+C를 누르세요.
echo.

REM 1초 후에 브라우저 열기
start "" "http://localhost:3000"

REM 개발 서버 시작
call npm start
