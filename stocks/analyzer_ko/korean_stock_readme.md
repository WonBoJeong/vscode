# 한국 주식 데이터 다운로더

yfinance를 활용한 한국 주식 시장 데이터 수집 및 분석 도구

## 📊 개요

이 프로젝트는 Yahoo Finance API를 통해 한국 주식 데이터를 자동으로 수집하고, 기술적 분석 지표를 계산하며, 시각화까지 제공하는 종합적인 주식 분석 도구입니다.

### 주요 특징

- 🚀 **자동화된 데이터 수집**: 한국 주요 종목 데이터 원클릭 다운로드
- 📈 **기술적 분석**: 이동평균, RSI, 볼린저 밴드 등 주요 지표 자동 계산
- 📊 **시각화 대시보드**: 주가 추이, 거래량, 수익률 비교 차트
- 💾 **다양한 저장 형식**: CSV, Excel 파일 지원
- 🎯 **맞춤형 설정**: 종목, 기간, 지표 사용자 정의 가능

## 🛠 설치 방법

### 1. Python 환경 준비

Python 3.7 이상이 필요합니다.

```bash
# Python 버전 확인
python --version
```

### 2. 패키지 설치

```bash
# 필수 패키지 설치
pip install yfinance pandas matplotlib seaborn numpy openpyxl

# 또는 requirements.txt 사용 (있는 경우)
pip install -r requirements.txt
```

### 3. 소스 코드 다운로드

```bash
# Git으로 클론 (저장소가 있는 경우)
git clone [repository-url]
cd korean-stock-downloader

# 또는 파일 직접 다운로드
# korean_stock_downloader.py 파일을 작업 디렉토리에 저장
```

## 🚀 빠른 시작

### 기본 실행

```bash
python korean_stock_downloader.py
```

실행하면 대화형 메뉴가 나타납니다:

```
=== yfinance 한국 주식 데이터 다운로더 ===

다운로드할 종목을 선택하세요:
1. 기본 종목 (10개 주요 종목)
2. 직접 입력

선택 (1 또는 2): 1

다운로드 기간을 선택하세요:
1. 최근 1년
2. 최근 3년 (기본)
3. 최근 5년
4. 직접 입력

선택 (1-4): 2
```

## 📋 상세 사용법

### 1. 기본 종목으로 시작하기

프로그램에는 한국의 대표 종목 10개가 미리 설정되어 있습니다:

- **005930**: 삼성전자
- **000660**: SK하이닉스
- **035420**: NAVER
- **035720**: 카카오
- **000270**: 기아
- **068270**: 셀트리온
- **207940**: 삼성바이오로직스
- **003670**: 포스코홀딩스
- **086520**: 에코프로
- **373220**: LG에너지솔루션

### 2. 사용자 정의 종목 설정

직접 종목을 선택하려면:

```
선택 (1 또는 2): 2
종목 코드를 쉼표로 구분하여 입력하세요 (예: 005930,000660): 005930,000660,035420
```

**주요 종목 코드 참고:**
- 삼성전자: 005930
- SK하이닉스: 000660
- NAVER: 035420
- 카카오: 035720
- LG화학: 051910
- 현대모비스: 012330
- LG전자: 066570
- KB금융: 105560
- 신한지주: 055550

### 3. 기간 설정 옵션

#### 사전 정의된 기간
- **1년**: 최근 1년간 데이터
- **3년**: 최근 3년간 데이터 (기본값)
- **5년**: 최근 5년간 데이터

#### 사용자 정의 기간
```
선택 (1-4): 4
시작일을 입력하세요 (YYYY-MM-DD): 2022-01-01
종료일을 입력하세요 (YYYY-MM-DD): 2024-12-31
```

### 4. 실행 과정 모니터링

```
=== 한국 주식 데이터 다운로드 시작 ===
대상 종목: 3개
기간: 3y

[1/3] 다운로드 중: 삼성전자 (005930.KS)
저장 완료: data/005930_241209.csv (782행)

[2/3] 다운로드 중: SK하이닉스 (000660.KS)
저장 완료: data/000660_241209.csv (782행)

[3/3] 다운로드 중: NAVER (035420.KS)
저장 완료: data/035420_241209.csv (782행)

=== 다운로드 완료 ===
성공: 3개 종목
실패: 0개 종목
```

## 📁 출력 파일 구조

실행 후 다음과 같은 파일들이 생성됩니다:

```
프로젝트폴더/
├── korean_stock_downloader.py
└── data/
    ├── 005930_241209.csv              # 개별 종목 데이터
    ├── 000660_241209.csv
    ├── 035420_241209.csv
    ├── combined_stocks_241209.csv     # 통합 데이터
    ├── summary_stats_241209.csv       # 분석 결과
    └── stock_analysis_chart_241209.png # 시각화 차트
```

### 파일별 상세 설명

#### 1. 개별 종목 파일 (예: 005930_241209.csv)

| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| Date | 거래일 | 2024-12-09 |
| Stock_Code | 종목코드 | 005930 |
| Symbol | Yahoo Finance 심볼 | 005930.KS |
| Stock_Name | 종목명 | 삼성전자 |
| Open | 시가 | 71000 |
| High | 고가 | 71500 |
| Low | 저가 | 70500 |
| Close | 종가 | 71200 |
| Volume | 거래량 | 15234567 |
| Trading_Value | 거래대금 | 1084504274400 |
| Return_Rate | 일간수익률(%) | 1.42 |
| Volatility | 변동성(%) | 1.42 |
| MA_5 | 5일 이동평균 | 70800 |
| MA_20 | 20일 이동평균 | 69500 |
| MA_60 | 60일 이동평균 | 68200 |
| BB_Upper | 볼린저밴드 상단 | 72500 |
| BB_Middle | 볼린저밴드 중간 | 70000 |
| BB_Lower | 볼린저밴드 하단 | 67500 |
| RSI | RSI 지수 | 65.4 |

#### 2. 통합 데이터 (combined_stocks_YYMMDD.csv)

모든 종목의 데이터를 날짜와 종목코드 순으로 정렬한 통합 파일입니다.

#### 3. 분석 결과 (summary_stats_YYMMDD.csv)

종목별 주요 통계 지표를 요약한 파일입니다:

- 거래 기간 (시작일, 종료일, 데이터 수)
- 가격 정보 (시작가, 종료가, 최고가, 최저가, 평균가)
- 거래 정보 (평균 거래량, 평균 거래대금)
- 수익률 분석 (평균 수익률, 표준편차, 총 수익률)
- 변동성 지표

## 📊 시각화 대시보드

차트 생성을 선택하면 4개의 분석 차트가 포함된 대시보드가 생성됩니다:

### 1. 주가 추이 차트
- 수익률 상위 5개 종목의 종가 변화
- 시간대별 주가 움직임 비교

### 2. 거래량 추이 차트
- 종목별 거래량 변화 패턴
- 거래 활성도 분석

### 3. 총 수익률 비교 차트
- 기간 내 종목별 수익률 막대 그래프
- 양수(초록색), 음수(빨간색) 구분 표시

### 4. 위험-수익률 산점도
- X축: 평균 변동성 (위험도)
- Y축: 총 수익률
- 각 종목의 위험 대비 수익률 포지셔닝

## 🔧 고급 사용법

### 프로그래밍 방식 사용

```python
from korean_stock_downloader import KoreanStockDownloader

# 다운로더 초기화
downloader = KoreanStockDownloader(data_dir="my_data")

# 특정 종목 1개 다운로드
data = downloader.download_single_stock("005930", period="1y")
print(data.head())

# 여러 종목 다운로드
stocks = ["005930", "000660", "035420"]
all_data = downloader.download_multiple_stocks(stocks, period="2y")

# 특정 기간 지정
all_data = downloader.download_multiple_stocks(
    stocks,
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# 통합 데이터셋 생성
combined = downloader.create_combined_dataset(all_data)

# 분석 수행
stats = downloader.analyze_stocks(combined)

# 시각화
downloader.create_visualization(combined, top_stocks=3)
```

### 클래스 초기화 옵션

```python
# 커스텀 데이터 디렉토리 설정
downloader = KoreanStockDownloader(data_dir="stock_data_2024")

# 종목 정보 사전 확장
downloader.stock_info["123456.KS"] = "새로운종목"
```

### 개별 기능 활용

```python
# RSI 계산
rsi_values = downloader.calculate_rsi(price_series, window=14)

# 종목 심볼 변환
symbol = downloader.get_korea_stock_symbol("005930")  # "005930.KS"
```

## 🎛 설정 및 커스터마이징

### 기본 종목 리스트 수정

코드에서 `stock_info` 딕셔너리를 수정하여 기본 종목을 변경할 수 있습니다:

```python
self.stock_info = {
    "005930.KS": "삼성전자",
    "000660.KS": "SK하이닉스",
    # 여기에 원하는 종목 추가
    "005380.KS": "현대차",
    "028260.KS": "삼성물산"
}
```

### 기술적 지표 파라미터 조정

```python
# 이동평균 기간 변경
data['MA_10'] = data['Close'].rolling(window=10).mean()
data['MA_50'] = data['Close'].rolling(window=50).mean()

# RSI 기간 변경
data['RSI_21'] = self.calculate_rsi(data['Close'], window=21)

# 볼린저 밴드 표준편차 배수 변경
bb_std = data['Close'].rolling(window=20).std()
data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2.5)  # 2.5배 적용
```

### 차트 스타일 커스터마이징

```python
# 한글 폰트 변경
plt.rcParams['font.family'] = ['Nanum Gothic', 'Malgun Gothic']

# 색상 테마 변경
plt.style.use('seaborn-v0_8')  # 또는 'ggplot', 'dark_background' 등

# 차트 크기 조정
fig, axes = plt.subplots(2, 2, figsize=(20, 15))
```

## 🐛 문제 해결

### 자주 발생하는 오류

#### 1. 패키지 설치 오류
```bash
# Windows에서 matplotlib 설치 오류 시
pip install --upgrade pip
pip install matplotlib --user

# Mac에서 한글 폰트 문제 시
brew install font-nanum
```

#### 2. 데이터 다운로드 실패
```
오류 발생 (005930.KS): HTTPError 404
```

**해결 방법:**
- 종목 코드가 정확한지 확인
- 인터넷 연결 상태 확인
- Yahoo Finance 서비스 상태 확인
- 시간을 두고 재시도

#### 3. 한글 폰트 표시 오류

```python
# Windows
plt.rcParams['font.family'] = 'Malgun Gothic'

# Mac
plt.rcParams['font.family'] = 'AppleGothic'

# Linux
plt.rcParams['font.family'] = 'DejaVu Sans'
```

#### 4. 메모리 부족 오류

대량의 데이터 처리 시:
```python
# 청크 단위로 처리
chunk_size = 5  # 한 번에 5개 종목씩 처리
for i in range(0, len(stock_codes), chunk_size):
    chunk = stock_codes[i:i+chunk_size]
    # 처리 로직
```

### 데이터 품질 확인

```python
# 결측값 확인
print(data.isnull().sum())

# 중복 데이터 확인
print(data.duplicated().sum())

# 데이터 타입 확인
print(data.dtypes)

# 기본 통계
print(data.describe())
```

## 📈 활용 예시

### 1. 포트폴리오 분석

```python
# 내 보유 종목들
my_portfolio = ["005930", "000660", "035420", "035720"]

# 데이터 수집
downloader = KoreanStockDownloader()
portfolio_data = downloader.download_multiple_stocks(my_portfolio, period="1y")

# 상관관계 분석
combined = downloader.create_combined_dataset(portfolio_data)
correlation_matrix = combined.pivot_table(
    index='Date', 
    columns='Stock_Name', 
    values='Return_Rate'
).corr()

print("종목간 상관관계:")
print(correlation_matrix)
```

### 2. 기술적 분석 신호

```python
# 골든크로스 신호 감지
def detect_golden_cross(data):
    signals = []
    for i in range(1, len(data)):
        if (data['MA_5'].iloc[i] > data['MA_20'].iloc[i] and 
            data['MA_5'].iloc[i-1] <= data['MA_20'].iloc[i-1]):
            signals.append({
                'Date': data['Date'].iloc[i],
                'Type': 'Golden Cross',
                'Price': data['Close'].iloc[i]
            })
    return signals

# 각 종목별 신호 확인
for code, data in all_data.items():
    signals = detect_golden_cross(data)
    if signals:
        print(f"{code} 골든크로스 신호: {len(signals)}개")
```

### 3. 백테스팅

```python
# 단순 이동평균 전략 백테스팅
def backtest_ma_strategy(data, short_window=5, long_window=20):
    data['Position'] = 0
    data['Position'][short_window:] = np.where(
        data['MA_5'][short_window:] > data['MA_20'][short_window:], 1, 0
    )
    
    data['Strategy_Return'] = data['Position'].shift(1) * data['Return_Rate']
    
    cumulative_strategy = (1 + data['Strategy_Return']/100).cumprod()
    cumulative_market = (1 + data['Return_Rate']/100).cumprod()
    
    return {
        'strategy_return': cumulative_strategy.iloc[-1] - 1,
        'market_return': cumulative_market.iloc[-1] - 1,
        'win_rate': (data['Strategy_Return'] > 0).mean()
    }

# 백테스팅 실행
for code, data in all_data.items():
    result = backtest_ma_strategy(data)
    print(f"{code}: 전략수익률 {result['strategy_return']:.2%}, "
          f"시장수익률 {result['market_return']:.2%}")
```

## 🔄 업데이트 및 유지보수

### 정기 데이터 업데이트

```python
# 스케줄링을 위한 cron job 또는 Task Scheduler 설정
# 매일 장 마감 후 데이터 업데이트

import schedule
import time

def daily_update():
    downloader = KoreanStockDownloader()
    # 어제 데이터만 업데이트
    yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
    today = datetime.now().strftime("%Y-%m-%d")
    
    all_data = downloader.download_multiple_stocks(
        default_stocks,
        start_date=yesterday,
        end_date=today
    )

# 매일 오후 6시에 실행
schedule.every().day.at("18:00").do(daily_update)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### 데이터베이스 연동

```python
import sqlite3

def save_to_database(data, db_path="stocks.db"):
    conn = sqlite3.connect(db_path)
    data.to_sql('stock_data', conn, if_exists='append', index=False)
    conn.close()

# 데이터베이스에서 조회
def load_from_database(stock_code, db_path="stocks.db"):
    conn = sqlite3.connect(db_path)
    query = "SELECT * FROM stock_data WHERE Stock_Code = ? ORDER BY Date"
    data = pd.read_sql_query(query, conn, params=[stock_code])
    conn.close()
    return data
```

## 📞 지원 및 기여

### 버그 리포트

문제가 발생하면 다음 정보와 함께 이슈를 등록해주세요:
- Python 버전
- 설치된 패키지 버전 (`pip list`)
- 에러 메시지 전문
- 실행 환경 (Windows/Mac/Linux)

### 기여 방법

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

### 개발 로드맵

- [ ] 실시간 데이터 스트리밍
- [ ] 더 많은 기술적 지표 추가
- [ ] 웹 대시보드 인터페이스
- [ ] 알림 기능 (이메일, Slack)
- [ ] 포트폴리오 최적화 도구

## 📄 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다. 자세한 내용은 `LICENSE` 파일을 참조하세요.

## 🙏 감사의 말

- **yfinance**: Yahoo Finance API 접근 제공
- **pandas**: 데이터 처리 및 분석
- **matplotlib/seaborn**: 데이터 시각화
- **한국 투자자 커뮤니티**: 피드백 및 개선 아이디어

---

**⚠️ 면책 조항**: 이 도구는 교육 및 연구 목적으로 제작되었습니다. 실제 투자 결정은 본인의 책임 하에 신중하게 내리시기 바랍니다.