"""
yfinance를 이용한 미국 주식 데이터 다운로드 스크립트
Yahoo Finance에서 미국 주식 데이터를 수집하여 CSV 파일로 저장
"""

import os
import sys
import time
import warnings
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

import pandas as pd
import numpy as np
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
import seaborn as sns

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

class USStockDownloader:
    """미국 주식 데이터 다운로드 클래스"""
    
    def __init__(self, data_dir: str = "us_data"):
        """
        초기화
        
        Args:
            data_dir (str): 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.date_key = datetime.now().strftime("%y%m%d")
        
        # 데이터 디렉토리 생성
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 미국 주요 종목 정보
        self.stock_info = {
            # 대형주 (Mega Cap)
            "AAPL": "Apple Inc.",
            "MSFT": "Microsoft Corporation",
            "GOOGL": "Alphabet Inc. (Google)",
            "AMZN": "Amazon.com Inc.",
            "NVDA": "NVIDIA Corporation",
            "TSLA": "Tesla Inc.",
            "META": "Meta Platforms Inc.",
            "BRK-B": "Berkshire Hathaway Inc.",
            "UNH": "UnitedHealth Group Inc.",
            "JNJ": "Johnson & Johnson",
            
            # 기술주
            "NFLX": "Netflix Inc.",
            "CRM": "Salesforce Inc.",
            "ORCL": "Oracle Corporation",
            "ADBE": "Adobe Inc.",
            "INTC": "Intel Corporation",
            "AMD": "Advanced Micro Devices",
            "PYPL": "PayPal Holdings Inc.",
            "UBER": "Uber Technologies Inc.",
            "SPOT": "Spotify Technology S.A.",
            "ZOOM": "Zoom Video Communications",
            
            # 금융주
            "JPM": "JPMorgan Chase & Co.",
            "BAC": "Bank of America Corp.",
            "WFC": "Wells Fargo & Company",
            "GS": "Goldman Sachs Group Inc.",
            "MS": "Morgan Stanley",
            "C": "Citigroup Inc.",
            "AXP": "American Express Company",
            "V": "Visa Inc.",
            "MA": "Mastercard Inc.",
            "BLK": "BlackRock Inc.",
            
            # ETF
            "SPY": "SPDR S&P 500 ETF Trust",
            "QQQ": "Invesco QQQ Trust",
            "VOO": "Vanguard S&P 500 ETF",
            "VTI": "Vanguard Total Stock Market ETF",
            "IWM": "iShares Russell 2000 ETF",
            "EFA": "iShares MSCI EAFE ETF",
            "VEA": "Vanguard FTSE Developed Markets ETF",
            "IEMG": "iShares Core MSCI Emerging Markets IMI Index ETF",
            "AGG": "iShares Core US Aggregate Bond ETF",
            "TLT": "iShares 20+ Year Treasury Bond ETF",
            
            # 레버리지 ETF
            "TQQQ": "ProShares UltraPro QQQ",
            "SOXL": "Direxion Daily Semiconductor Bull 3X Shares",
            "SPXL": "Direxion Daily S&P 500 Bull 3X Shares",
            "TECL": "Direxion Daily Technology Bull 3X Shares",
            "UPRO": "ProShares UltraPro S&P500",
            "LABU": "Direxion Daily S&P Biotech Bull 3X Shares",
            "CURE": "Direxion Daily Healthcare Bull 3X Shares",
            "NAIL": "Direxion Daily Homebuilders & Supplies Bull 3X Shares",
            
            # 섹터별 주요 종목
            "XLE": "Energy Select Sector SPDR Fund",
            "XLF": "Financial Select Sector SPDR Fund",
            "XLK": "Technology Select Sector SPDR Fund",
            "XLV": "Health Care Select Sector SPDR Fund",
            "XLI": "Industrial Select Sector SPDR Fund",
            "XLY": "Consumer Discretionary Select Sector SPDR Fund",
            "XLP": "Consumer Staples Select Sector SPDR Fund",
            "XLU": "Utilities Select Sector SPDR Fund",
            "XLB": "Materials Select Sector SPDR Fund",
            "XLRE": "Real Estate Select Sector SPDR Fund",
            
            # 인기 종목
            "COIN": "Coinbase Global Inc.",
            "PLTR": "Palantir Technologies Inc.",
            "SNOW": "Snowflake Inc.",
            "RBLX": "Roblox Corporation",
            "HOOD": "Robinhood Markets Inc.",
            "RIVN": "Rivian Automotive Inc.",
            "LCID": "Lucid Group Inc.",
            "SOFI": "SoFi Technologies Inc.",
            "PATH": "UiPath Inc.",
            "CRWD": "CrowdStrike Holdings Inc."
        }
    
    def get_stock_info(self, symbol: str) -> str:
        """
        종목 심볼에 대한 회사명 반환
        
        Args:
            symbol (str): 종목 심볼
            
        Returns:
            str: 회사명
        """
        return self.stock_info.get(symbol.upper(), f"Unknown ({symbol})")
    
    def download_single_stock(self, 
                            symbol: str, 
                            period: str = "3y", 
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            save_file: bool = True) -> Optional[pd.DataFrame]:
        """
        개별 종목 데이터 다운로드
        
        Args:
            symbol (str): 종목 심볼 (예: AAPL, GOOGL)
            period (str): 기간 ("1y", "2y", "3y", "5y", "10y", "max")
            start_date (str): 시작일 (YYYY-MM-DD)
            end_date (str): 종료일 (YYYY-MM-DD)
            save_file (bool): 파일 저장 여부
            
        Returns:
            pd.DataFrame: 주식 데이터
        """
        symbol = symbol.upper()
        stock_name = self.get_stock_info(symbol)
        
        print(f"다운로드 중: {stock_name} ({symbol})")
        
        try:
            # yfinance 티커 생성
            ticker = yf.Ticker(symbol)
            
            # 데이터 다운로드
            if start_date and end_date:
                data = ticker.history(start=start_date, end=end_date)
            else:
                data = ticker.history(period=period)
            
            if data.empty:
                print(f"경고: {symbol}의 데이터가 없습니다.")
                return None
            
            # 데이터 전처리
            data.reset_index(inplace=True)
            data['Symbol'] = symbol
            data['Stock_Name'] = stock_name
            
            # 수익률 및 지표 계산
            data['Return_Rate'] = data['Close'].pct_change() * 100
            data['Volatility'] = data['Return_Rate'].abs()
            data['Trading_Value'] = data['Close'] * data['Volume']
            data['MA_5'] = data['Close'].rolling(window=5).mean()
            data['MA_20'] = data['Close'].rolling(window=20).mean()
            data['MA_50'] = data['Close'].rolling(window=50).mean()
            data['MA_200'] = data['Close'].rolling(window=200).mean()
            
            # 볼린저 밴드 (20일, 2표준편차)
            data['BB_Middle'] = data['Close'].rolling(window=20).mean()
            bb_std = data['Close'].rolling(window=20).std()
            data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
            data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
            data['BB_Width'] = (data['BB_Upper'] - data['BB_Lower']) / data['BB_Middle'] * 100
            data['BB_Position'] = (data['Close'] - data['BB_Lower']) / (data['BB_Upper'] - data['BB_Lower'])
            
            # RSI 계산 (14일)
            data['RSI'] = self.calculate_rsi(data['Close'])
            
            # MACD 계산
            exp1 = data['Close'].ewm(span=12).mean()
            exp2 = data['Close'].ewm(span=26).mean()
            data['MACD'] = exp1 - exp2
            data['MACD_Signal'] = data['MACD'].ewm(span=9).mean()
            data['MACD_Histogram'] = data['MACD'] - data['MACD_Signal']
            
            # Stochastic Oscillator
            low_14 = data['Low'].rolling(window=14).min()
            high_14 = data['High'].rolling(window=14).max()
            data['Stoch_K'] = ((data['Close'] - low_14) / (high_14 - low_14)) * 100
            data['Stoch_D'] = data['Stoch_K'].rolling(window=3).mean()
            
            # ATR (Average True Range)
            data['TR'] = np.maximum(
                data['High'] - data['Low'],
                np.maximum(
                    abs(data['High'] - data['Close'].shift(1)),
                    abs(data['Low'] - data['Close'].shift(1))
                )
            )
            data['ATR'] = data['TR'].rolling(window=14).mean()
            
            # Williams %R
            data['Williams_R'] = ((high_14 - data['Close']) / (high_14 - low_14)) * -100
            
            # 컬럼 순서 정리
            columns_order = [
                'Date', 'Symbol', 'Stock_Name', 'Open', 'High', 'Low', 'Close', 'Volume', 
                'Trading_Value', 'Return_Rate', 'Volatility',
                'MA_5', 'MA_20', 'MA_50', 'MA_200',
                'BB_Upper', 'BB_Middle', 'BB_Lower', 'BB_Width', 'BB_Position',
                'RSI', 'MACD', 'MACD_Signal', 'MACD_Histogram',
                'Stoch_K', 'Stoch_D', 'ATR', 'Williams_R'
            ]
            
            data = data[columns_order]
            
            # 파일 저장
            if save_file:
                filename = os.path.join(self.data_dir, f"{symbol}_{self.date_key}.csv")
                data.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"저장 완료: {filename} ({len(data)}행)")
            
            return data
            
        except Exception as e:
            print(f"오류 발생 ({symbol}): {str(e)}")
            return None
    
    def calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            prices (pd.Series): 가격 데이터
            window (int): 계산 윈도우
            
        Returns:
            pd.Series: RSI 값
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def download_multiple_stocks(self, 
                                symbols: List[str], 
                                period: str = "3y",
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                max_workers: int = 5) -> Dict[str, pd.DataFrame]:
        """
        여러 종목 데이터 일괄 다운로드
        
        Args:
            symbols (List[str]): 종목 심볼 리스트
            period (str): 기간
            start_date (str): 시작일
            end_date (str): 종료일
            max_workers (int): 최대 워커 수
            
        Returns:
            Dict[str, pd.DataFrame]: 종목별 데이터 딕셔너리
        """
        print("=== 미국 주식 데이터 다운로드 시작 ===")
        print(f"대상 종목: {len(symbols)}개")
        print(f"기간: {period if not start_date else f'{start_date} ~ {end_date}'}")
        
        all_data = {}
        success_count = 0
        failed_symbols = []
        
        # 순차 다운로드 (API 제한 고려)
        for i, symbol in enumerate(symbols, 1):
            print(f"\n[{i}/{len(symbols)}] ", end="")
            
            data = self.download_single_stock(
                symbol, period=period, 
                start_date=start_date, 
                end_date=end_date
            )
            
            if data is not None:
                all_data[symbol.upper()] = data
                success_count += 1
            else:
                failed_symbols.append(symbol)
            
            # API 제한 방지를 위한 대기
            time.sleep(0.5)
        
        # 결과 요약
        print(f"\n=== 다운로드 완료 ===")
        print(f"성공: {success_count}개 종목")
        print(f"실패: {len(failed_symbols)}개 종목")
        
        if failed_symbols:
            print(f"실패한 종목: {', '.join(failed_symbols)}")
        
        return all_data
    
    def create_combined_dataset(self, all_data: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        통합 데이터셋 생성
        
        Args:
            all_data (Dict[str, pd.DataFrame]): 종목별 데이터
            
        Returns:
            pd.DataFrame: 통합 데이터
        """
        if not all_data:
            print("결합할 데이터가 없습니다.")
            return None
        
        print("데이터를 통합하는 중...")
        
        # 모든 데이터를 하나로 결합
        combined_data = pd.concat(all_data.values(), ignore_index=True)
        
        # 날짜 컬럼 정리
        combined_data['Date'] = pd.to_datetime(combined_data['Date'])
        combined_data = combined_data.sort_values(['Date', 'Symbol'])
        
        # 통합 파일 저장
        combined_filename = os.path.join(self.data_dir, f"combined_us_stocks_{self.date_key}.csv")
        combined_data.to_csv(combined_filename, index=False, encoding='utf-8-sig')
        
        print(f"통합 파일 저장 완료: {combined_filename}")
        print(f"총 데이터: {len(combined_data)}행")
        
        return combined_data
    
    def analyze_stocks(self, combined_data: pd.DataFrame) -> pd.DataFrame:
        """
        주식 데이터 기본 분석
        
        Args:
            combined_data (pd.DataFrame): 통합 데이터
            
        Returns:
            pd.DataFrame: 분석 결과
        """
        if combined_data is None or combined_data.empty:
            print("분석할 데이터가 없습니다.")
            return pd.DataFrame()
        
        print("\n=== 기본 통계 분석 ===")
        
        # 종목별 통계 계산
        summary_stats = combined_data.groupby(['Symbol', 'Stock_Name']).agg({
            'Date': ['min', 'max', 'count'],
            'Close': ['first', 'last', 'min', 'max', 'mean'],
            'Volume': 'mean',
            'Trading_Value': 'mean',
            'Return_Rate': ['mean', 'std'],
            'Volatility': 'mean',
            'RSI': 'mean',
            'ATR': 'mean'
        }).round(4)
        
        # 컬럼명 정리
        summary_stats.columns = [
            '시작일', '종료일', '데이터수', '시작가', '종료가', '최저가', '최고가', '평균가',
            '평균거래량', '평균거래대금', '평균수익률', '수익률표준편차', '평균변동성',
            '평균RSI', '평균ATR'
        ]
        
        # 총 수익률 계산
        summary_stats['총수익률(%)'] = ((summary_stats['종료가'] - summary_stats['시작가']) / 
                                      summary_stats['시작가'] * 100).round(2)
        
        # 샤프 비율 계산 (무위험 수익률을 0으로 가정)
        summary_stats['샤프비율'] = (summary_stats['평균수익률'] / summary_stats['수익률표준편차']).round(2)
        
        # 최대 낙폭 계산
        max_drawdowns = []
        for symbol in combined_data['Symbol'].unique():
            symbol_data = combined_data[combined_data['Symbol'] == symbol].copy()
            symbol_data['Cumulative'] = (1 + symbol_data['Return_Rate']/100).cumprod()
            symbol_data['Peak'] = symbol_data['Cumulative'].expanding().max()
            symbol_data['Drawdown'] = (symbol_data['Cumulative'] / symbol_data['Peak'] - 1) * 100
            max_drawdown = symbol_data['Drawdown'].min()
            max_drawdowns.append(max_drawdown)
        
        summary_stats['최대낙폭(%)'] = max_drawdowns
        
        summary_stats.reset_index(inplace=True)
        
        # 결과 출력
        print(summary_stats.to_string(index=False))
        
        # 수익률 상위/하위 종목
        top_performers = summary_stats.nlargest(5, '총수익률(%)')
        bottom_performers = summary_stats.nsmallest(5, '총수익률(%)')
        
        print(f"\n=== 수익률 상위 5개 종목 ===")
        print(top_performers[['Stock_Name', '총수익률(%)']].to_string(index=False))
        
        print(f"\n=== 수익률 하위 5개 종목 ===")
        print(bottom_performers[['Stock_Name', '총수익률(%)']].to_string(index=False))
        
        # 샤프 비율 상위 종목
        top_sharpe = summary_stats.nlargest(5, '샤프비율')
        print(f"\n=== 샤프비율 상위 5개 종목 ===")
        print(top_sharpe[['Stock_Name', '샤프비율']].to_string(index=False))
        
        # 분석 결과 저장
        stats_filename = os.path.join(self.data_dir, f"us_summary_stats_{self.date_key}.csv")
        summary_stats.to_csv(stats_filename, index=False, encoding='utf-8-sig')
        print(f"\n분석 결과 저장: {stats_filename}")
        
        return summary_stats
    
    def create_visualization(self, combined_data: pd.DataFrame, top_stocks: int = 5):
        """
        주식 데이터 시각화
        
        Args:
            combined_data (pd.DataFrame): 통합 데이터
            top_stocks (int): 상위 몇 개 종목을 시각화할지
        """
        if combined_data is None or combined_data.empty:
            print("시각화할 데이터가 없습니다.")
            return
        
        print("차트를 생성하는 중...")
        
        # 폰트 설정
        plt.rcParams['font.family'] = ['DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 수익률 상위 종목 선택
        latest_data = combined_data.groupby('Symbol').last()
        first_data = combined_data.groupby('Symbol').first()
        returns = ((latest_data['Close'] - first_data['Close']) / first_data['Close'] * 100)
        top_symbols = returns.nlargest(top_stocks).index.tolist()
        
        # 상위 종목 데이터 필터링
        top_data = combined_data[combined_data['Symbol'].isin(top_symbols)]
        
        # 시각화
        fig, axes = plt.subplots(3, 2, figsize=(18, 15))
        fig.suptitle(f'US Stock Analysis Dashboard (Top {top_stocks} Performers)', fontsize=16, y=0.98)
        
        # 1. 주가 추이 (정규화)
        ax1 = axes[0, 0]
        for symbol in top_symbols:
            stock_data = top_data[top_data['Symbol'] == symbol].copy()
            stock_name = stock_data['Stock_Name'].iloc[0]
            # 정규화 (시작점을 100으로)
            normalized_price = (stock_data['Close'] / stock_data['Close'].iloc[0]) * 100
            ax1.plot(stock_data['Date'], normalized_price, label=f"{symbol}", linewidth=2)
        ax1.set_title('Normalized Price Performance (Base=100)')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Normalized Price')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 거래량 추이
        ax2 = axes[0, 1]
        for symbol in top_symbols:
            stock_data = top_data[top_data['Symbol'] == symbol]
            ax2.plot(stock_data['Date'], stock_data['Volume'], label=f"{symbol}", alpha=0.7)
        ax2.set_title('Volume Trends')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Volume')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        ax2.ticklabel_format(style='scientific', axis='y', scilimits=(0,0))
        
        # 3. 총 수익률 비교
        ax3 = axes[1, 0]
        returns_data = []
        labels = []
        for symbol in top_symbols:
            stock_data = top_data[top_data['Symbol'] == symbol]
            if not stock_data.empty:
                total_return = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / 
                              stock_data['Close'].iloc[0] * 100)
                returns_data.append(total_return)
                labels.append(symbol)
        
        colors = ['green' if x > 0 else 'red' for x in returns_data]
        bars = ax3.bar(labels, returns_data, color=colors, alpha=0.7)
        ax3.set_title('Total Returns (%)')
        ax3.set_ylabel('Return (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 막대 위에 수치 표시
        for bar, value in zip(bars, returns_data):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                    f'{value:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        # 4. 변동성 vs 수익률 산점도
        ax4 = axes[1, 1]
        for symbol in top_symbols:
            stock_data = top_data[top_data['Symbol'] == symbol]
            if not stock_data.empty:
                avg_volatility = stock_data['Volatility'].mean()
                total_return = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / 
                              stock_data['Close'].iloc[0] * 100)
                ax4.scatter(avg_volatility, total_return, s=100, alpha=0.7, label=symbol)
        
        ax4.set_title('Risk-Return Profile')
        ax4.set_xlabel('Average Volatility (%)')
        ax4.set_ylabel('Total Return (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        # 5. RSI 추이
        ax5 = axes[2, 0]
        for symbol in top_symbols:
            stock_data = top_data[top_data['Symbol'] == symbol]
            ax5.plot(stock_data['Date'], stock_data['RSI'], label=f"{symbol}", alpha=0.8)
        
        ax5.axhline(y=70, color='r', linestyle='--', alpha=0.5, label='Overbought (70)')
        ax5.axhline(y=30, color='g', linestyle='--', alpha=0.5, label='Oversold (30)')
        ax5.set_title('RSI Trends')
        ax5.set_xlabel('Date')
        ax5.set_ylabel('RSI')
        ax5.legend()
        ax5.grid(True, alpha=0.3)
        ax5.set_ylim(0, 100)
        
        # 6. MACD 신호 (첫 번째 종목)
        ax6 = axes[2, 1]
        if top_symbols:
            first_symbol = top_symbols[0]
            stock_data = top_data[top_data['Symbol'] == first_symbol].copy()
            
            ax6.plot(stock_data['Date'], stock_data['MACD'], label='MACD', color='blue')
            ax6.plot(stock_data['Date'], stock_data['MACD_Signal'], label='Signal', color='red')
            ax6.bar(stock_data['Date'], stock_data['MACD_Histogram'], 
                   label='Histogram', alpha=0.3, color='gray')
            
            ax6.set_title(f'MACD Analysis - {first_symbol}')
            ax6.set_xlabel('Date')
            ax6.set_ylabel('MACD')
            ax6.legend()
            ax6.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 차트 저장
        chart_filename = os.path.join(self.data_dir, f"us_stock_analysis_chart_{self.date_key}.png")
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        print(f"차트 저장 완료: {chart_filename}")
        
        plt.show()
    
    def get_market_sectors(self) -> Dict[str, List[str]]:
        """
        시장 섹터별 종목 분류 반환
        
        Returns:
            Dict[str, List[str]]: 섹터별 종목 딕셔너리
        """
        return {
            "대형 기술주": ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "META"],
            "금융주": ["JPM", "BAC", "WFC", "GS", "MS", "C", "V", "MA"],
            "ETF (Index)": ["SPY", "QQQ", "VOO", "VTI", "IWM"],
            "레버리지 ETF": ["TQQQ", "SOXL", "SPXL", "TECL", "UPRO"],
            "성장주": ["TSLA", "NFLX", "UBER", "ZOOM", "PLTR", "SNOW"],
            "섹터 ETF": ["XLE", "XLF", "XLK", "XLV", "XLI", "XLY"]
        }

def main():
    """메인 실행 함수"""
    
    print("=== yfinance 미국 주식 데이터 다운로더 ===\n")
    
    # 다운로더 초기화
    downloader = USStockDownloader()
    
    # 기본 종목 리스트들
    popular_stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "NVDA", "TSLA", "META", "NFLX", "UBER", "ZOOM"]
    etf_stocks = ["SPY", "QQQ", "VOO", "VTI", "TQQQ", "SOXL", "SPXL"]
    leverage_etf = ["TQQQ", "SOXL", "SPXL", "TECL", "UPRO", "LABU"]
    financial_stocks = ["JPM", "BAC", "V", "MA", "GS", "MS"]
    
    # 사용자 입력 받기
    print("다운로드할 종목 카테고리를 선택하세요:")
    print("1. 인기 대형주 (AAPL, MSFT, GOOGL 등)")
    print("2. ETF (SPY, QQQ, VOO 등)")
    print("3. 레버리지 ETF (TQQQ, SOXL, SPXL 등)")
    print("4. 금융주 (JPM, BAC, V 등)")
    print("5. 직접 입력")
    
    choice = input("선택 (1-5): ").strip()
    
    if choice == "1":
        stock_symbols = popular_stocks
    elif choice == "2":
        stock_symbols = etf_stocks
    elif choice == "3":
        stock_symbols = leverage_etf
    elif choice == "4":
        stock_symbols = financial_stocks
    elif choice == "5":
        symbols_input = input("종목 심볼을 쉼표로 구분하여 입력하세요 (예: AAPL,MSFT,GOOGL): ")
        stock_symbols = [symbol.strip().upper() for symbol in symbols_input.split(",")]
    else:
        print("잘못된 선택입니다. 기본 인기 대형주로 설정합니다.")
        stock_symbols = popular_stocks
    
    # 기간 설정
    print(f"\n선택된 종목: {', '.join(stock_symbols)}")
    print("\n다운로드 기간을 선택하세요:")
    print("1. 최근 1년")
    print("2. 최근 3년 (기본)")
    print("3. 최근 5년")
    print("4. 최근 10년")
    print("5. 직접 입력")
    
    period_choice = input("선택 (1-5): ").strip()
    
    start_date, end_date, period = None, None, "3y"
    
    if period_choice == "1":
        period = "1y"
    elif period_choice == "3":
        period = "5y"
    elif period_choice == "4":
        period = "10y"
    elif period_choice == "5":
        start_input = input("시작일을 입력하세요 (YYYY-MM-DD): ")
        end_input = input("종료일을 입력하세요 (YYYY-MM-DD): ")
        start_date, end_date = start_input, end_input
        period = None
    
    try:
        # 데이터 다운로드
        all_data = downloader.download_multiple_stocks(
            stock_symbols, 
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        
        if all_data:
            # 통합 데이터셋 생성
            combined_data = downloader.create_combined_dataset(all_data)
            
            # 분석 수행
            if combined_data is not None:
                summary_stats = downloader.analyze_stocks(combined_data)
                
                # 시각화
                create_chart = input("\n차트를 생성하시겠습니까? (y/n): ").strip().lower()
                if create_chart == 'y':
                    downloader.create_visualization(combined_data)
                
                print(f"\n=== 모든 작업 완료 ===")
                print(f"생성된 파일:")
                print(f"- 개별 종목 파일: {downloader.data_dir}/ 폴더 내")
                print(f"- 통합 데이터: combined_us_stocks_{downloader.date_key}.csv")
                print(f"- 요약 통계: us_summary_stats_{downloader.date_key}.csv")
                if create_chart == 'y':
                    print(f"- 분석 차트: us_stock_analysis_chart_{downloader.date_key}.png")
        
    except KeyboardInterrupt:
        print("\n\n작업이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {str(e)}")

if __name__ == "__main__":
    # 필요한 패키지 설치 확인
    try:
        import yfinance as yf
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        print("필요한 패키지를 설치해주세요:")
        print("pip install yfinance pandas matplotlib seaborn")
        sys.exit(1)
    
    main()
