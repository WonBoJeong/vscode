# 미국 주식 데이터 다운로더

yfinance를 활용한 미국 주식 시장 데이터 수집 및 분석 도구

## 📊 개요

이 프로젝트는 Yahoo Finance API를 통해 미국 주식 데이터를 자동으로 수집하고, 고급 기술적 분석 지표를 계산하며, 전문적인 시각화까지 제공하는 종합적인 미국 주식 분석 도구입니다.

### 주요 특징

- 🚀 **포괄적인 데이터 수집**: 개별주, ETF, 레버리지 ETF 등 모든 미국 상장 종목 지원
- 📈 **고급 기술적 분석**: RSI, MACD, 볼린저밴드, Stochastic, Williams %R, ATR 등
- 📊 **전문 시각화**: 정규화 차트, 위험-수익률 분석, 기술적 지표 대시보드
- 💾 **다양한 저장 형식**: CSV, Excel 파일 지원
- 🎯 **카테고리별 선택**: 대형주, ETF, 레버리지 ETF, 섹터별 분류
- 📉 **위험 관리 지표**: 샤프 비율, 최대 낙폭, ATR 등 포함

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
cd us-stock-downloader

# 또는 파일 직접 다운로드
# us_stock_downloader.py 파일을 작업 디렉토리에 저장
```

## 🚀 빠른 시작

### 기본 실행

```bash
python us_stock_downloader.py
```

실행하면 카테고리별 선택 메뉴가 나타납니다:

```
=== yfinance 미국 주식 데이터 다운로더 ===

다운로드할 종목 카테고리를 선택하세요:
1. 인기 대형주 (AAPL, MSFT, GOOGL 등)
2. ETF (SPY, QQQ, VOO 등)
3. 레버리지 ETF (TQQQ, SOXL, SPXL 등)
4. 금융주 (JPM, BAC, V 등)
5. 직접 입력

선택 (1-5): 1
```

## 📋 지원 종목 카테고리

### 1. 대형 기술주 (Mega Cap Tech)
- **AAPL**: Apple Inc.
- **MSFT**: Microsoft Corporation
- **GOOGL**: Alphabet Inc. (Google)
- **AMZN**: Amazon.com Inc.
- **NVDA**: NVIDIA Corporation
- **TSLA**: Tesla Inc.
- **META**: Meta Platforms Inc.
- **NFLX**: Netflix Inc.
- **UBER**: Uber Technologies Inc.
- **ZOOM**: Zoom Video Communications

### 2. ETF (Exchange Traded Funds)
- **SPY**: SPDR S&P 500 ETF Trust
- **QQQ**: Invesco QQQ Trust (NASDAQ-100)
- **VOO**: Vanguard S&P 500 ETF
- **VTI**: Vanguard Total Stock Market ETF
- **IWM**: iShares Russell 2000 ETF
- **EFA**: iShares MSCI EAFE ETF
- **IEMG**: iShares Core MSCI Emerging Markets
- **AGG**: iShares Core US Aggregate Bond ETF
- **TLT**: iShares 20+ Year Treasury Bond ETF

### 3. 레버리지 ETF (3x Leveraged)
- **TQQQ**: ProShares UltraPro QQQ (3x NASDAQ-100)
- **SOXL**: Direxion Daily Semiconductor Bull 3X
- **SPXL**: Direxion Daily S&P 500 Bull 3X
- **TECL**: Direxion Daily Technology Bull 3X
- **UPRO**: ProShares UltraPro S&P500
- **LABU**: Direxion Daily S&P Biotech Bull 3X
- **CURE**: Direxion Daily Healthcare Bull 3X

### 4. 금융주 (Financial Sector)
- **JPM**: JPMorgan Chase & Co.
- **BAC**: Bank of America Corp.
- **WFC**: Wells Fargo & Company
- **GS**: Goldman Sachs Group Inc.
- **MS**: Morgan Stanley
- **V**: Visa Inc.
- **MA**: Mastercard Inc.
- **AXP**: American Express Company

### 5. 섹터 ETF (Sector SPDRs)
- **XLE**: Energy Select Sector SPDR
- **XLF**: Financial Select Sector SPDR
- **XLK**: Technology Select Sector SPDR
- **XLV**: Health Care Select Sector SPDR
- **XLI**: Industrial Select Sector SPDR
- **XLY**: Consumer Discretionary Select Sector SPDR

### 6. 성장주 & 인기 종목
- **PLTR**: Palantir Technologies Inc.
- **SNOW**: Snowflake Inc.
- **COIN**: Coinbase Global Inc.
- **RBLX**: Roblox Corporation
- **HOOD**: Robinhood Markets Inc.
- **RIVN**: Rivian Automotive Inc.
- **SOFI**: SoFi Technologies Inc.

## 📁 출력 파일 구조

실행 후 다음과 같은 파일들이 생성됩니다:

```
프로젝트폴더/
├── us_stock_downloader.py
└── us_data/
    ├── AAPL_241209.csv                     # 개별 종목 데이터
    ├── MSFT_241209.csv
    ├── GOOGL_241209.csv
    ├── combined_us_stocks_241209.csv       # 통합 데이터
    ├── us_summary_stats_241209.csv         # 분석 결과
    └── us_stock_analysis_chart_241209.png  # 시각화 차트
```

### 데이터 컬럼 상세 설명

#### 기본 정보
| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| Date | 거래일 | 2024-12-09 |
| Symbol | 종목 심볼 | AAPL |
| Stock_Name | 회사명 | Apple Inc. |

#### 가격 및 거래 정보
| 컬럼명 | 설명 | 예시 |
|--------|------|------|
| Open | 시가 | 195.50 |
| High | 고가 | 197.25 |
| Low | 저가 | 194.80 |
| Close | 종가 | 196.75 |
| Volume | 거래량 | 45234567 |
| Trading_Value | 거래대금 | 8901234567.25 |

#### 수익률 및 변동성
| 컬럼명 | 설명 | 계산 방식 |
|--------|------|----------|
| Return_Rate | 일간수익률(%) | (Close - Previous Close) / Previous Close * 100 |
| Volatility | 변동성(%) | abs(Return_Rate) |

#### 이동평균선
| 컬럼명 | 설명 | 기간 |
|--------|------|------|
| MA_5 | 5일 이동평균 | 5일 |
| MA_20 | 20일 이동평균 | 20일 |
| MA_50 | 50일 이동평균 | 50일 |
| MA_200 | 200일 이동평균 | 200일 |

#### 볼린저 밴드
| 컬럼명 | 설명 | 계산 방식 |
|--------|------|----------|
| BB_Upper | 볼린저밴드 상단 | MA_20 + (2 * 표준편차) |
| BB_Middle | 볼린저밴드 중간선 | MA_20 |
| BB_Lower | 볼린저밴드 하단 | MA_20 - (2 * 표준편차) |
| BB_Width | 밴드 폭(%) | (상단 - 하단) / 중간선 * 100 |
| BB_Position | 밴드 내 위치 | (Close - 하단) / (상단 - 하단) |

#### 오실레이터 지표
| 컬럼명 | 설명 | 범위 | 해석 |
|--------|------|------|------|
| RSI | 상대강도지수 | 0-100 | 70+ 과매수, 30- 과매도 |
| Stoch_K | 스토캐스틱 K% | 0-100 | 80+ 과매수, 20- 과매도 |
| Stoch_D | 스토캐스틱 D% | 0-100 | K%의 3일 이동평균 |
| Williams_R | 윌리엄스 %R | -100-0 | -20+ 과매수, -80- 과매도 |

#### MACD 지표
| 컬럼명 | 설명 | 계산 방식 |
|--------|------|----------|
| MACD | MACD 라인 | EMA(12) - EMA(26) |
| MACD_Signal | 시그널 라인 | MACD의 EMA(9) |
| MACD_Histogram | 히스토그램 | MACD - Signal |

#### 변동성 지표
| 컬럼명 | 설명 | 용도 |
|--------|------|------|
| ATR | 평균 진실 범위 | 변동성 측정, 손절선 설정 |

## 📊 고급 분석 기능

### 1. 통계 분석 결과

#### 수익률 분석
- **총수익률**: 기간 내 누적 수익률
- **평균수익률**: 일평균 수익률
- **수익률표준편차**: 수익률의 변동성
- **샤프비율**: 위험 대비 수익률 (수익률/표준편차)

#### 위험 분석
- **최대낙폭**: 고점 대비 최대 하락폭
- **평균변동성**: 일평균 가격 변동성
- **평균ATR**: 평균 진실 범위

#### 기술적 분석
- **평균RSI**: 평균 상대강도지수
- **볼린저밴드 분석**: 밴드 폭 및 위치 분석

### 2. 시각화 대시보드

#### Chart 1: 정규화 주가 성과
- 모든 종목을 시작점 100으로 정규화
- 상대적 성과 비교 용이
- 시간대별 성과 추이 분석

#### Chart 2: 거래량 추이
- 종목별 거래량 변화 패턴
- 거래 활성도 분석
- 이벤트 발생 시점 파악

#### Chart 3: 총 수익률 비교
- 기간 내 종목별 수익률 막대 그래프
- 수익(녹색)/손실(빨간색) 구분
- 수치 레이블 포함

#### Chart 4: 위험-수익률 산점도
- X축: 평균 변동성 (위험도)
- Y축: 총 수익률
- 효율적 투자 대상 식별

#### Chart 5: RSI 추이
- 과매수/과매도 구간 표시
- 70선(과매수), 30선(과매도) 기준선
- 매매 시점 판단 지원

#### Chart 6: MACD 분석
- MACD 라인과 시그널 라인
- 히스토그램 표시
- 골든크로스/데드크로스 신호

## 🔧 고급 사용법

### 프로그래밍 방식 사용

```python
from us_stock_downloader import USStockDownloader

# 다운로더 초기화
downloader = USStockDownloader(data_dir="my_us_data")

# 특정 종목 1개 다운로드
data = downloader.download_single_stock("AAPL", period="1y")
print(data.head())

# 포트폴리오 분석
my_portfolio = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA"]
all_data = downloader.download_multiple_stocks(my_portfolio, period="2y")

# 특정 기간 지정
all_data = downloader.download_multiple_stocks(
    my_portfolio,
    start_date="2023-01-01",
    end_date="2024-12-31"
)

# 통합 분석
combined = downloader.create_combined_dataset(all_data)
stats = downloader.analyze_stocks(combined)
downloader.create_visualization(combined, top_stocks=5)
```

### 섹터별 분석

```python
# 섹터별 종목 가져오기
sectors = downloader.get_market_sectors()

# 기술주 섹터 분석
tech_stocks = sectors["대형 기술주"]
tech_data = downloader.download_multiple_stocks(tech_stocks, period="1y")

# 금융주 섹터 분석
finance_stocks = sectors["금융주"]
finance_data = downloader.download_multiple_stocks(finance_stocks, period="1y")
```

### 커스텀 지표 추가

```python
def add_custom_indicators(data):
    """사용자 정의 지표 추가"""
    
    # 가격 채널 (Donchian Channel)
    data['DC_High'] = data['High'].rolling(window=20).max()
    data['DC_Low'] = data['Low'].rolling(window=20).min()
    data['DC_Middle'] = (data['DC_High'] + data['DC_Low']) / 2
    
    # 가격 대비 거래량 (Price Volume Trend)
    data['PVT'] = ((data['Close'] - data['Close'].shift(1)) / 
                   data['Close'].shift(1) * data['Volume']).cumsum()
    
    # 변동성 돌파 신호
    data['Volatility_Breakout'] = (data['Close'] > 
                                  data['Close'].shift(1) + data['ATR'].shift(1))
    
    return data

# 사용 예시
for symbol, data in all_data.items():
    all_data[symbol] = add_custom_indicators(data)
```

## 🎛 전략 백테스팅

### 1. 이동평균 교차 전략

```python
def ma_crossover_strategy(data, short_window=20, long_window=50):
    """이동평균 교차 전략 백테스팅"""
    
    data = data.copy()
    
    # 매매 신호 생성
    data['Signal'] = 0
    data['Signal'][short_window:] = np.where(
        data[f'MA_{short_window}'][short_window:] > data[f'MA_{long_window}'][short_window:], 1, 0
    )
    
    data['Position'] = data['Signal'].diff()
    
    # 수익률 계산
    data['Strategy_Return'] = data['Signal'].shift(1) * data['Return_Rate']
    data['Cumulative_Strategy'] = (1 + data['Strategy_Return']/100).cumprod()
    data['Cumulative_Market'] = (1 + data['Return_Rate']/100).cumprod()
    
    # 성과 지표
    total_strategy_return = data['Cumulative_Strategy'].iloc[-1] - 1
    total_market_return = data['Cumulative_Market'].iloc[-1] - 1
    win_rate = (data['Strategy_Return'] > 0).mean()
    
    return {
        'total_strategy_return': total_strategy_return,
        'total_market_return': total_market_return,
        'win_rate': win_rate,
        'excess_return': total_strategy_return - total_market_return,
        'data': data
    }

# 실행 예시
for symbol, data in all_data.items():
    result = ma_crossover_strategy(data, 20, 50)
    print(f"{symbol}: 전략수익률 {result['total_strategy_return']:.2%}, "
          f"시장수익률 {result['total_market_return']:.2%}, "
          f"초과수익률 {result['excess_return']:.2%}")
```

### 2. RSI 역전 전략

```python
def rsi_reversal_strategy(data, rsi_oversold=30, rsi_overbought=70):
    """RSI 역전 전략"""
    
    data = data.copy()
    
    # 매매 신호
    data['Buy_Signal'] = (data['RSI'] < rsi_oversold) & (data['RSI'].shift(1) >= rsi_oversold)
    data['Sell_Signal'] = (data['RSI'] > rsi_overbought) & (data['RSI'].shift(1) <= rsi_overbought)
    
    # 포지션 계산
    data['Position'] = 0
    buy_indices = data[data['Buy_Signal']].index
    sell_indices = data[data['Sell_Signal']].index
    
    # 매수 후 매도까지 포지션 유지
    for buy_idx in buy_indices:
        next_sell = sell_indices[sell_indices > buy_idx]
        if len(next_sell) > 0:
            data.loc[buy_idx:next_sell[0], 'Position'] = 1
    
    # 수익률 계산
    data['Strategy_Return'] = data['Position'].shift(1) * data['Return_Rate']
    
    return data

# 실행 예시
rsi_results = {}
for symbol, data in all_data.items():
    rsi_data = rsi_reversal_strategy(data)
    strategy_return = (1 + rsi_data['Strategy_Return']/100).prod() - 1
    rsi_results[symbol] = strategy_return
    
# 결과 정렬
sorted_results = sorted(rsi_results.items(), key=lambda x: x[1], reverse=True)
print("RSI 역전 전략 수익률 순위:")
for symbol, return_rate in sorted_results[:5]:
    print(f"{symbol}: {return_rate:.2%}")
```

### 3. 볼린저 밴드 전략

```python
def bollinger_bands_strategy(data):
    """볼린저 밴드 전략"""
    
    data = data.copy()
    
    # 매매 신호 (밴드 이탈 후 복귀)
    data['Oversold'] = data['Close'] < data['BB_Lower']
    data['Overbought'] = data['Close'] > data['BB_Upper'
    data['Buy_Signal'] = (data['Oversold'].shift(1)) & (~data['Oversold'])
    data['Sell_Signal'] = (data['Overbought'].shift(1)) & (~data['Overbought'])
    
    # 밴드 폭 확장 시에만 거래 (변동성 확대 시점)
    data['High_Volatility'] = data['BB_Width'] > data['BB_Width'].rolling(20).mean()
    data['Buy_Signal'] = data['Buy_Signal'] & data['High_Volatility']
    data['Sell_Signal'] = data['Sell_Signal'] & data['High_Volatility']
    
    return data
```

## 📈 실전 투자 활용법

### 1. 포트폴리오 구성

```python
def build_portfolio(symbols, weights=None):
    """포트폴리오 구성 및 분석"""
    
    if weights is None:
        weights = [1/len(symbols)] * len(symbols)  # 동일 가중
    
    # 데이터 수집
    portfolio_data = {}
    for symbol in symbols:
        data = downloader.download_single_stock(symbol, period="2y")
        if data is not None:
            portfolio_data[symbol] = data
    
    # 수익률 매트릭스 생성
    returns_df = pd.DataFrame()
    for symbol, data in portfolio_data.items():
        returns_df[symbol] = data.set_index('Date')['Return_Rate']
    
    # 포트폴리오 수익률 계산
    portfolio_returns = (returns_df * weights).sum(axis=1)
    
    # 위험 지표
    portfolio_vol = portfolio_returns.std()
    portfolio_sharpe = portfolio_returns.mean() / portfolio_vol
    
    # 상관관계 분석
    correlation_matrix = returns_df.corr()
    
    return {
        'returns': portfolio_returns,
        'volatility': portfolio_vol,
        'sharpe_ratio': portfolio_sharpe,
        'correlation': correlation_matrix,
        'individual_data': portfolio_data
    }

# 예시: 균형 포트폴리오
balanced_portfolio = build_portfolio(
    ["SPY", "QQQ", "AGG", "VEA", "IEMG"], 
    [0.4, 0.2, 0.2, 0.1, 0.1]  # 가중치
)
```

### 2. 리스크 관리

```python
def calculate_var(returns, confidence=0.05):
    """VaR (Value at Risk) 계산"""
    return returns.quantile(confidence)

def calculate_max_drawdown(cumulative_returns):
    """최대 낙폭 계산"""
    peak = cumulative_returns.expanding().max()
    drawdown = (cumulative_returns / peak - 1)
    return drawdown.min()

def position_sizing(data, atr_multiplier=2, risk_per_trade=0.02):
    """ATR 기반 포지션 사이징"""
    current_price = data['Close'].iloc[-1]
    current_atr = data['ATR'].iloc[-1]
    stop_loss_distance = current_atr * atr_multiplier
    
    # 거래당 위험금액 기준 포지션 크기
    position_size = risk_per_trade / (stop_loss_distance / current_price)
    
    return {
        'position_size': position_size,
        'stop_loss_price': current_price - stop_loss_distance,
        'risk_amount': risk_per_trade
    }
```

### 3. 스크리닝 및 필터링

```python
def screen_stocks(all_data, criteria):
    """종목 스크리닝"""
    
    screened_stocks = []
    
    for symbol, data in all_data.items():
        if data is None or len(data) < 100:
            continue
            
        latest = data.iloc[-1]
        recent_data = data.tail(50)  # 최근 50일
        
        # 스크리닝 조건 확인
        conditions_met = 0
        total_conditions = len(criteria)
        
        # RSI 조건
        if 'rsi_range' in criteria:
            rsi_min, rsi_max = criteria['rsi_range']
            if rsi_min <= latest['RSI'] <= rsi_max:
                conditions_met += 1
        
        # 볼륨 조건 (평균 대비)
        if 'volume_ratio' in criteria:
            avg_volume = recent_data['Volume'].mean()
            if latest['Volume'] > avg_volume * criteria['volume_ratio']:
                conditions_met += 1
        
        # 가격 위치 (52주 고점 대비)
        if 'price_position' in criteria:
            year_high = data.tail(252)['High'].max()
            price_position = latest['Close'] / year_high
            if price_position >= criteria['price_position']:
                conditions_met += 1
        
        # 이동평균 조건
        if 'ma_trend' in criteria:
            if criteria['ma_trend'] == 'bullish':
                if (latest['MA_20'] > latest['MA_50'] and 
                    latest['Close'] > latest['MA_20']):
                    conditions_met += 1
        
        # 수익률 조건
        if 'return_threshold' in criteria:
            period_return = ((latest['Close'] - recent_data['Close'].iloc[0]) / 
                           recent_data['Close'].iloc[0] * 100)
            if period_return >= criteria['return_threshold']:
                conditions_met += 1
        
        # 조건 만족도 확인
        if conditions_met / total_conditions >= 0.7:  # 70% 이상 조건 만족
            screened_stocks.append({
                'symbol': symbol,
                'name': latest['Stock_Name'],
                'price': latest['Close'],
                'rsi': latest['RSI'],
                'volume_ratio': latest['Volume'] / recent_data['Volume'].mean(),
                'conditions_met': f"{conditions_met}/{total_conditions}"
            })
    
    return screened_stocks

# 스크리닝 예시
screening_criteria = {
    'rsi_range': (30, 70),      # RSI 30-70 사이
    'volume_ratio': 1.2,        # 평균 거래량의 1.2배 이상
    'price_position': 0.8,      # 52주 고점의 80% 이상
    'ma_trend': 'bullish',      # 상승 추세
    'return_threshold': 5       # 최근 50일 수익률 5% 이상
}

screened = screen_stocks(all_data, screening_criteria)
print("스크리닝 결과:")
for stock in screened[:10]:
    print(f"{stock['symbol']}: {stock['name']} - 조건 {stock['conditions_met']}")
```

## 🔄 자동화 및 스케줄링

### 일일 업데이트 스크립트

```python
import schedule
import time
from datetime import datetime, timedelta

def daily_update():
    """일일 데이터 업데이트"""
    print(f"일일 업데이트 시작: {datetime.now()}")
    
    # 관심 종목 리스트
    watchlist = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "SPY", "QQQ"]
    
    downloader = USStockDownloader()
    
    # 어제와 오늘 데이터 업데이트
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d")
    
    all_data = downloader.download_multiple_stocks(
        watchlist,
        start_date=start_date,
        end_date=end_date
    )
    
    # 알림 조건 확인
    alerts = check_alerts(all_data)
    if alerts:
        send_alerts(alerts)
    
    print("일일 업데이트 완료")

def check_alerts(all_data):
    """알림 조건 확인"""
    alerts = []
    
    for symbol, data in all_data.items():
        if data is None or len(data) == 0:
            continue
            
        latest = data.iloc[-1]
        
        # RSI 과매수/과매도 알림
        if latest['RSI'] > 80:
            alerts.append(f"{symbol}: RSI 과매수 ({latest['RSI']:.1f})")
        elif latest['RSI'] < 20:
            alerts.append(f"{symbol}: RSI 과매도 ({latest['RSI']:.1f})")
        
        # 볼린저 밴드 이탈 알림
        if latest['Close'] > latest['BB_Upper']:
            alerts.append(f"{symbol}: 볼린저 밴드 상단 돌파")
        elif latest['Close'] < latest['BB_Lower']:
            alerts.append(f"{symbol}: 볼린저 밴드 하단 이탈")
        
        # 큰 변동성 알림
        if abs(latest['Return_Rate']) > 5:
            direction = "상승" if latest['Return_Rate'] > 0 else "하락"
            alerts.append(f"{symbol}: 큰 변동성 {direction} ({latest['Return_Rate']:.1f}%)")
    
    return alerts

def send_alerts(alerts):
    """알림 전송 (이메일, 슬랙 등)"""
    print("=== 알림 ===")
    for alert in alerts:
        print(alert)
    # 실제 구현 시 이메일이나 슬랙 API 사용

# 스케줄 설정
schedule.every().day.at("18:00").do(daily_update)  # 매일 오후 6시
schedule.every().monday.at("09:00").do(weekly_report)  # 매주 월요일 오전 9시

# 지속적 실행
while True:
    schedule.run_pending()
    time.sleep(60)
```

### 주간 리포트 생성

```python
def weekly_report():
    """주간 투자 리포트 생성"""
    print("주간 리포트 생성 중...")
    
    # 주요 지수 및 관심 종목
    symbols = ["SPY", "QQQ", "AAPL", "MSFT", "GOOGL", "NVDA", "TSLA"]
    
    downloader = USStockDownloader()
    
    # 1개월 데이터 수집
    all_data = downloader.download_multiple_stocks(symbols, period="1mo")
    combined_data = downloader.create_combined_dataset(all_data)
    
    if combined_data is None:
        return
    
    # 주간 성과 분석
    week_ago = datetime.now() - timedelta(days=7)
    recent_data = combined_data[combined_data['Date'] >= week_ago]
    
    weekly_summary = []
    for symbol in symbols:
        symbol_data = recent_data[recent_data['Symbol'] == symbol]
        if len(symbol_data) > 1:
            week_return = ((symbol_data['Close'].iloc[-1] - symbol_data['Close'].iloc[0]) / 
                          symbol_data['Close'].iloc[0] * 100)
            weekly_summary.append({
                'Symbol': symbol,
                'Weekly_Return': week_return,
                'Current_Price': symbol_data['Close'].iloc[-1],
                'RSI': symbol_data['RSI'].iloc[-1]
            })
    
    # 리포트 저장
    report_df = pd.DataFrame(weekly_summary)
    report_filename = f"weekly_report_{datetime.now().strftime('%Y%m%d')}.csv"
    report_df.to_csv(report_filename, index=False)
    
    print(f"주간 리포트 저장: {report_filename}")
    print(report_df)
```

## 📱 모바일 알림 연동

### 슬랙 알림 설정

```python
import requests
import json

def send_slack_notification(webhook_url, message):
    """슬랙으로 알림 전송"""
    payload = {
        'text': message,
        'username': 'Stock Bot',
        'icon_emoji': ':chart_with_upwards_trend:'
    }
    
    response = requests.post(webhook_url, data=json.dumps(payload))
    return response.status_code == 200

# 사용 예시
def check_breakouts(all_data):
    """돌파 신호 확인 후 알림"""
    for symbol, data in all_data.items():
        if len(data) < 50:
            continue
            
        latest = data.iloc[-1]
        recent_high = data.tail(20)['High'].max()
        
        # 20일 고점 돌파
        if latest['Close'] > recent_high:
            message = f"🚀 {symbol} 20일 고점 돌파! 현재가: ${latest['Close']:.2f}"
            send_slack_notification(SLACK_WEBHOOK_URL, message)
        
        # 골든 크로스
        if (latest['MA_20'] > latest['MA_50'] and 
            data.iloc[-2]['MA_20'] <= data.iloc[-2]['MA_50']):
            message = f"✨ {symbol} 골든 크로스 발생! MA20: ${latest['MA_20']:.2f}"
            send_slack_notification(SLACK_WEBHOOK_URL, message)
```

### 이메일 알림 설정

```python
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email_alert(subject, body, to_email):
    """이메일 알림 전송"""
    
    # Gmail SMTP 설정
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    sender_email = "your_email@gmail.com"
    sender_password = "your_app_password"  # 앱 비밀번호 사용
    
    # 메시지 생성
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    
    message.attach(MIMEText(body, "plain"))
    
    # 이메일 전송
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = message.as_string()
        server.sendmail(sender_email, to_email, text)
        server.quit()
        return True
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
        return False

# 일일 리포트 이메일 전송
def send_daily_report_email(summary_stats):
    """일일 리포트 이메일 전송"""
    
    # 상위 수익률 종목
    top_performers = summary_stats.nlargest(3, '총수익률(%)')
    
    subject = f"일일 주식 리포트 - {datetime.now().strftime('%Y-%m-%d')}"
    
    body = f"""
일일 주식 시장 리포트

=== 상위 수익률 종목 ===
{top_performers[['Symbol', 'Stock_Name', '총수익률(%)']].to_string(index=False)}

=== 시장 요약 ===
- 분석 종목 수: {len(summary_stats)}개
- 평균 수익률: {summary_stats['총수익률(%)'].mean():.2f}%
- 상승 종목: {(summary_stats['총수익률(%)'] > 0).sum()}개
- 하락 종목: {(summary_stats['총수익률(%)'] < 0).sum()}개

자세한 분석은 첨부된 파일을 확인하세요.

Happy Trading!
"""
    
    send_email_alert(subject, body, "recipient@email.com")
```

## 🐛 문제 해결 가이드

### 자주 발생하는 오류

#### 1. 데이터 다운로드 실패

```bash
# 오류 메시지
오류 발생 (AAPL): HTTPError 404
```

**원인 및 해결책:**
- **심볼 오타**: 정확한 심볼 확인 (대소문자 구분 없음)
- **상장폐지**: 해당 종목이 상장폐지되었는지 확인
- **API 제한**: 너무 많은 요청으로 인한 일시적 제한
- **네트워크 문제**: 인터넷 연결 상태 확인

```python
# 안전한 다운로드 함수
def safe_download(symbol, retries=3, delay=2):
    for attempt in range(retries):
        try:
            data = downloader.download_single_stock(symbol)
            if data is not None:
                return data
        except Exception as e:
            print(f"시도 {attempt + 1} 실패: {e}")
            if attempt < retries - 1:
                time.sleep(delay * (attempt + 1))
    return None
```

#### 2. 메모리 부족 오류

```python
# 대량 데이터 처리 시 청크 단위 처리
def process_large_dataset(symbols, chunk_size=10):
    all_results = {}
    
    for i in range(0, len(symbols), chunk_size):
        chunk = symbols[i:i+chunk_size]
        print(f"처리 중: {i+1}-{min(i+chunk_size, len(symbols))}/{len(symbols)}")
        
        chunk_data = downloader.download_multiple_stocks(chunk)
        all_results.update(chunk_data)
        
        # 메모리 정리
        import gc
        gc.collect()
    
    return all_results
```

#### 3. 차트 표시 오류

```python
# 백엔드 설정으로 해결
import matplotlib
matplotlib.use('TkAgg')  # 또는 'Qt5Agg', 'Agg'
import matplotlib.pyplot as plt

# 한글 폰트 설정
import platform
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic'
elif platform.system() == 'Darwin':  # macOS
    plt.rcParams['font.family'] = 'AppleGothic'
else:  # Linux
    plt.rcParams['font.family'] = 'DejaVu Sans'
```

### 성능 최적화

#### 1. 다운로드 속도 개선

```python
# 병렬 처리 (주의: API 제한 고려)
from concurrent.futures import ThreadPoolExecutor
import threading

class ThreadSafeDownloader(USStockDownloader):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.lock = threading.Lock()
    
    def parallel_download(self, symbols, max_workers=3):
        def download_with_delay(symbol):
            time.sleep(0.1)  # API 제한 방지
            return self.download_single_stock(symbol)
        
        results = {}
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            future_to_symbol = {
                executor.submit(download_with_delay, symbol): symbol 
                for symbol in symbols
            }
            
            for future in as_completed(future_to_symbol):
                symbol = future_to_symbol[future]
                try:
                    data = future.result()
                    if data is not None:
                        with self.lock:
                            results[symbol] = data
                except Exception as e:
                    print(f"오류 ({symbol}): {e}")
        
        return results
```

#### 2. 데이터 캐싱

```python
import pickle
import os
from datetime import datetime

class CachedDownloader(USStockDownloader):
    def __init__(self, cache_dir="cache", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def get_cache_filename(self, symbol, period):
        return os.path.join(self.cache_dir, f"{symbol}_{period}_{self.date_key}.pkl")
    
    def download_single_stock(self, symbol, period="3y", **kwargs):
        cache_file = self.get_cache_filename(symbol, period)
        
        # 캐시 확인
        if os.path.exists(cache_file):
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    print(f"캐시에서 로드: {symbol}")
                    return cached_data
            except:
                pass  # 캐시 파일이 손상된 경우 새로 다운로드
        
        # 새로 다운로드
        data = super().download_single_stock(symbol, period, **kwargs)
        
        # 캐시 저장
        if data is not None:
            try:
                with open(cache_file, 'wb') as f:
                    pickle.dump(data, f)
            except Exception as e:
                print(f"캐시 저장 실패 ({symbol}): {e}")
        
        return data
```

## 📚 추가 학습 자료

### 기술적 분석 학습

1. **책 추천**
   - "Technical Analysis of the Financial Markets" - John J. Murphy
   - "Japanese Candlestick Charting Techniques" - Steve Nison
   - "Market Wizards" - Jack Schwager

2. **온라인 리소스**
   - [Investopedia Technical Analysis](https://www.investopedia.com/technical-analysis-4689657)
   - [TradingView Education](https://www.tradingview.com/education/)
   - [Yahoo Finance](https://finance.yahoo.com/)

### Python 금융 라이브러리

```python
# 추가 유용한 라이브러리들
pip install QuantLib  # 금융 수학 라이브러리
pip install arch      # GARCH 모델링
pip install pyfolio   # 포트폴리오 분석
pip install zipline   # 백테스팅 프레임워크
pip install empyrical # 금융 성과 지표
```

### API 확장

```python
# Alpha Vantage API 연동 예시
import requests

def get_fundamental_data(symbol, api_key):
    """기본 재무 데이터 가져오기"""
    url = f"https://www.alphavantage.co/query"
    params = {
        'function': 'OVERVIEW',
        'symbol': symbol,
        'apikey': api_key
    }
    
    response = requests.get(url, params=params)
    return response.json()

# 사용 예시
# fundamental = get_fundamental_data("AAPL", "YOUR_API_KEY")
# print(f"P/E Ratio: {fundamental.get('PERatio', 'N/A')}")
```

## 🔮 향후 개발 계획

### 예정된 기능들

- [ ] **실시간 데이터 스트리밍**: WebSocket을 통한 실시간 가격 업데이트
- [ ] **옵션 데이터 분석**: 옵션 체인 및 그릭스 계산
- [ ] **암호화폐 지원**: 비트코인, 이더리움 등 주요 암호화폐 추가
- [ ] **뉴스 감성 분석**: 뉴스 기사의 감성 분석을 통한 투자 신호
- [ ] **머신러닝 예측**: LSTM, Random Forest 등을 활용한 가격 예측
- [ ] **웹 대시보드**: Flask/Django 기반 웹 인터페이스
- [ ] **모바일 앱**: React Native 기반 모바일 알림 앱

### 기여 방법

1. **이슈 제기**: 버그 리포트나 기능 요청
2. **코드 기여**: Pull Request 제출
3. **문서 개선**: README나 주석 개선
4. **테스팅**: 다양한 환경에서의 테스트

```bash
# 개발 환경 설정
git clone [repository]
cd us-stock-downloader
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements-dev.txt
```

## 📄 라이선스 및 면책조항

### 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

### 면책조항

⚠️ **중요**: 이 도구는 교육 및 연구 목적으로 제작되었습니다. 
- 투자 결정은 본인의 책임하에 신중하게 내리시기 바랍니다
- 과거 성과가 미래 수익을 보장하지 않습니다
- 실제 투자 전에 전문가와 상담하시기를 권장합니다
- 레버리지 ETF는 높은 위험을 동반하므로 각별한 주의가 필요합니다

### 데이터 출처

- **Yahoo Finance**: 주가 및 기술적 지표 데이터
- **yfinance 라이브러리**: Python Yahoo Finance API 래퍼

### 연락처

- **GitHub Issues**: 기술적 문제나 기능 요청
- **이메일**: [your-email@example.com]
- **디스코드**: [투자 커뮤니티 링크]

---

**Happy Trading! 📈**

*"The stock market is filled with individuals who know the price of everything, but the value of nothing." - Philip Fisher*