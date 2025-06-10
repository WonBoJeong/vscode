# 🚀 VStock Advanced 설치 및 사용 가이드

## 📦 완성된 파일 구조
```
D:\vscode\stock\                    # 여기에 복사해주세요
├── 📁 config/                      # 설정 파일
│   └── config.json
├── 📁 data/                        # 주식 데이터 (샘플 포함)
│   ├── AAPL.csv
│   ├── TSLA.csv
│   ├── MSFT.csv
│   ├── GOOGL.csv
│   └── PLTR.csv
├── 📁 src/                         # 핵심 모듈들
│   ├── __init__.py
│   ├── data_loader.py              # 데이터 로더
│   ├── technical_analysis.py       # 기술적 분석
│   ├── chart_widget.py             # 차트 위젯
│   ├── portfolio_manager.py        # 포트폴리오 관리
│   └── gui_components.py           # GUI 컴포넌트
├── 📄 main.py                      # 메인 프로그램 (전체 기능)
├── 📄 simple_main.py               # 간단 버전 (빠른 테스트)
├── 📄 run.bat                      # 실행 파일 (Windows)
├── 📄 requirements.txt             # 필요 라이브러리
├── 📄 create_sample_data.py        # 샘플 데이터 생성
└── 📄 README.md                    # 상세 문서
```

## ⚡ 빠른 시작 (3단계)

### 1️⃣ 파일 복사
현재 생성된 모든 파일을 `D:\vscode\stock\` 폴더에 복사해주세요.

### 2️⃣ 실행
`run.bat` 파일을 더블클릭하세요!

### 3️⃣ 분석 시작
- 종목 코드 입력 (예: AAPL)
- "🔍 분석" 버튼 클릭
- 차트와 분석 결과 확인

## 🔧 상세 설치 가이드

### Python 설치 확인
```bash
python --version
# Python 3.8 이상 필요
```

### 라이브러리 설치
```bash
# 자동 설치 (run.bat 실행시)
# 또는 수동 설치:
pip install pandas numpy matplotlib tkinter
```

### 데이터 폴더 설정
1. **자동**: 프로그램이 `D:/vscode/stock/data` 자동 감지
2. **수동**: "📂 데이터 폴더" 버튼으로 경로 설정

## 📊 주요 기능

### 🎯 기본 분석
- **실시간 차트**: 캔들스틱, 라인차트, 거래량
- **이동평균선**: MA20, MA50 자동 표시
- **가격 정보**: 현재가, 변동률, 거래량 등

### 📈 기술적 분석 (main.py)
- **RSI**: 과매수/과매도 구간
- **MACD**: 매매 신호
- **볼린저 밴드**: 변동성 분석
- **스토캐스틱**: 모멘텀 지표

### 💼 포트폴리오 관리 (main.py)
- **보유 종목**: 매수/매도 기록
- **수익률 계산**: 실시간 손익
- **섹터 분석**: 분산 투자 현황

## 🎮 사용법

### 기본 사용
1. **종목 입력**: 검색창에 'AAPL' 입력
2. **분석 실행**: 🔍 버튼 클릭 또는 Enter
3. **결과 확인**: 좌측 차트, 우측 정보 패널

### 빠른 선택
- 버튼 클릭: [AAPL] [TSLA] [MSFT] [GOOGL] [PLTR]

### 지원 종목
**샘플 데이터 포함:**
- AAPL (Apple)
- TSLA (Tesla)
- MSFT (Microsoft)
- GOOGL (Google)
- PLTR (Palantir)

**추가 가능:** 사용자 데이터 파일 (.csv, .xlsx)

## 📁 데이터 형식

### CSV 파일 예시
```csv
Date,Open,High,Low,Close,Volume
2022-01-03,182.63,182.88,177.71,182.01,104487900
2022-01-04,182.63,182.94,179.12,179.70,99310400
```

### 지원 컬럼명
- **영어**: Date, Open, High, Low, Close, Volume
- **한글**: 날짜, 시가, 고가, 저가, 종가, 거래량

## ⚙️ 설정 옵션

### config.json 편집
```json
{
  "data_folder": "D:/vscode/stock/data",
  "default_symbols": ["AAPL", "TSLA", "MSFT"],
  "chart_settings": {
    "show_volume": true,
    "candlestick_style": true
  }
}
```

## 🐛 문제 해결

### 자주 발생하는 문제들

**1. "모듈을 찾을 수 없습니다"**
```bash
# 해결방법:
pip install pandas numpy matplotlib
```

**2. "데이터 파일을 찾을 수 없습니다"**
- data 폴더에 CSV 파일 확인
- 파일명이 종목코드와 일치하는지 확인 (예: AAPL.csv)

**3. "차트가 표시되지 않습니다"**
```bash
# matplotlib 재설치:
pip install --upgrade matplotlib
```

**4. "한글이 깨집니다"**
- Windows 기본 폰트 사용
- 파일 인코딩을 UTF-8로 저장

### 성능 최적화

**메모리 사용량 줄이기:**
- 대용량 파일은 기간별로 분할
- 불필요한 차트 탭 닫기

**속도 향상:**
- SSD 사용 권장
- 데이터 파일을 로컬에 저장

## 🔄 버전 선택

### simple_main.py (추천)
- ✅ 빠른 실행
- ✅ 기본 차트 + 정보
- ✅ 안정적 동작
- ❌ 제한된 기능

### main.py (고급)
- ✅ 모든 기능
- ✅ 기술적 분석
- ✅ 포트폴리오 관리
- ❌ 복잡한 구조

## 📞 지원

### 오류 신고
- GitHub Issues
- 로그 파일 첨부
- 재현 단계 설명

### 기능 요청
- 새로운 지표 추가
- UI 개선 사항
- 데이터 소스 확장

## 🚀 업그레이드 로드맵

### v1.1 (계획)
- [ ] 실시간 데이터 연동
- [ ] 더 많은 기술적 지표
- [ ] 백테스팅 기능

### v1.2 (계획)  
- [ ] 머신러닝 예측
- [ ] 모바일 앱 연동
- [ ] 클라우드 저장

---

## 🎉 축하합니다!

**📈 VStock Advanced** 주식 분석 프로그램이 완성되었습니다!

### 특징
- ✨ **현대적 UI**: advanced.html 디자인 기반
- 📊 **전문 차트**: 캔들스틱, 기술적 분석
- 💼 **포트폴리오**: 실시간 손익 계산
- 🔍 **스마트 분석**: AI 기반 매매 신호
- 📁 **유연한 데이터**: CSV, Excel 자동 인식

### 즉시 사용 가능
1. `run.bat` 더블클릭
2. 종목 코드 입력 (AAPL)
3. 🔍 분석 버튼 클릭
4. 전문적인 분석 결과 확인!

**Happy Trading! 📈💰**