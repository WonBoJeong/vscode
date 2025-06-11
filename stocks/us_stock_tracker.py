import yfinance as yf
import requests
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import json
from typing import Dict, List, Optional
import matplotlib.pyplot as plt
import seaborn as sns
from dataclasses import dataclass
import asyncio
import aiohttp

@dataclass
class StockData:
    symbol: str
    name: str
    current_price: float
    change: float
    change_percent: float
    volume: int
    market_cap: float
    pe_ratio: float
    dividend_yield: float
    day_high: float
    day_low: float
    fifty_two_week_high: float
    fifty_two_week_low: float
    last_updated: str

class USStockTracker:
    def __init__(self):
        self.watchlist = []
        self.api_keys = {
            'alpha_vantage': 'YOUR_ALPHA_VANTAGE_API_KEY',  # 무료 키 필요
            'fmp': 'YOUR_FMP_API_KEY'  # Financial Modeling Prep API
        }
        
    def add_to_watchlist(self, symbols: List[str]):
        """관심종목에 추가"""
        for symbol in symbols:
            if symbol.upper() not in self.watchlist:
                self.watchlist.append(symbol.upper())
        print(f"관심종목 추가됨: {symbols}")
        
    def remove_from_watchlist(self, symbols: List[str]):
        """관심종목에서 제거"""
        for symbol in symbols:
            if symbol.upper() in self.watchlist:
                self.watchlist.remove(symbol.upper())
        print(f"관심종목 제거됨: {symbols}")
        
    def get_stock_info(self, symbol: str) -> Optional[StockData]:
        """개별 주식 정보 조회 (Yahoo Finance 사용)"""
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="1d")
            
            if hist.empty:
                return None
                
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            return StockData(
                symbol=symbol.upper(),
                name=info.get('longName', symbol),
                current_price=round(current_price, 2),
                change=round(change, 2),
                change_percent=round(change_percent, 2),
                volume=info.get('volume', 0),
                market_cap=info.get('marketCap', 0),
                pe_ratio=info.get('trailingPE', 0),
                dividend_yield=info.get('dividendYield', 0) * 100 if info.get('dividendYield') else 0,
                day_high=info.get('dayHigh', 0),
                day_low=info.get('dayLow', 0),
                fifty_two_week_high=info.get('fiftyTwoWeekHigh', 0),
                fifty_two_week_low=info.get('fiftyTwoWeekLow', 0),
                last_updated=datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            )
        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return None
            
    def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, StockData]:
        """여러 주식 정보 한번에 조회"""
        results = {}
        for symbol in symbols:
            data = self.get_stock_info(symbol)
            if data:
                results[symbol.upper()] = data
        return results
        
    def get_watchlist_data(self) -> Dict[str, StockData]:
        """관심종목 전체 조회"""
        if not self.watchlist:
            print("관심종목이 비어있습니다.")
            return {}
        return self.get_multiple_stocks(self.watchlist)
        
    def get_market_movers(self) -> Dict[str, List[StockData]]:
        """시장 주요 움직임 (상승/하락 종목)"""
        # S&P 500 주요 종목들
        major_stocks = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK-B',
            'JNJ', 'V', 'WMT', 'JPM', 'MA', 'PG', 'UNH', 'DIS', 'HD', 'BAC',
            'ADBE', 'CRM', 'NFLX', 'KO', 'PFE', 'ABBV', 'PEP', 'TMO', 'COST'
        ]
        
        stocks_data = self.get_multiple_stocks(major_stocks)
        
        # 상승률 기준 정렬
        sorted_stocks = sorted(stocks_data.values(), key=lambda x: x.change_percent, reverse=True)
        
        return {
            'top_gainers': sorted_stocks[:10],
            'top_losers': sorted_stocks[-10:]
        }
        
    def get_sector_performance(self) -> Dict[str, float]:
        """섹터별 성과"""
        sector_etfs = {
            'Technology': 'XLK',
            'Healthcare': 'XLV', 
            'Financial': 'XLF',
            'Consumer Discretionary': 'XLY',
            'Communication': 'XLC',
            'Industrial': 'XLI',
            'Consumer Staples': 'XLP',
            'Energy': 'XLE',
            'Utilities': 'XLU',
            'Real Estate': 'XLRE',
            'Materials': 'XLB'
        }
        
        sector_performance = {}
        for sector, etf in sector_etfs.items():
            data = self.get_stock_info(etf)
            if data:
                sector_performance[sector] = data.change_percent
                
        return sector_performance
        
    def get_chart_data(self, symbol: str, period: str = "1mo") -> pd.DataFrame:
        """차트 데이터 조회"""
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period=period)
        return hist
        
    def calculate_technical_indicators(self, symbol: str) -> Dict[str, float]:
        """기술적 지표 계산"""
        hist = self.get_chart_data(symbol, "3mo")
        
        if hist.empty:
            return {}
            
        # 이동평균
        ma_5 = hist['Close'].rolling(window=5).mean().iloc[-1]
        ma_20 = hist['Close'].rolling(window=20).mean().iloc[-1]
        ma_50 = hist['Close'].rolling(window=50).mean().iloc[-1]
        
        # RSI 계산
        delta = hist['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs)).iloc[-1]
        
        # 볼린저 밴드
        bb_period = 20
        bb_std = 2
        bb_middle = hist['Close'].rolling(window=bb_period).mean().iloc[-1]
        bb_std_val = hist['Close'].rolling(window=bb_period).std().iloc[-1]
        bb_upper = bb_middle + (bb_std_val * bb_std)
        bb_lower = bb_middle - (bb_std_val * bb_std)
        
        current_price = hist['Close'].iloc[-1]
        
        return {
            'MA5': round(ma_5, 2),
            'MA20': round(ma_20, 2),
            'MA50': round(ma_50, 2),
            'RSI': round(rsi, 2),
            'BB_Upper': round(bb_upper, 2),
            'BB_Middle': round(bb_middle, 2),
            'BB_Lower': round(bb_lower, 2),
            'Price_vs_MA20': round(((current_price - ma_20) / ma_20) * 100, 2)
        }
        
    def get_earnings_calendar(self, symbol: str) -> Dict:
        """실적 발표 일정"""
        try:
            ticker = yf.Ticker(symbol)
            calendar = ticker.calendar
            if calendar is not None and not calendar.empty:
                return {
                    'next_earnings': calendar.index[0].strftime('%Y-%m-%d'),
                    'estimate': calendar.iloc[0, 0] if len(calendar.columns) > 0 else None
                }
        except:
            pass
        return {'next_earnings': 'N/A', 'estimate': 'N/A'}
        
    def get_news_sentiment(self, symbol: str) -> List[Dict]:
        """뉴스 및 센티먼트 (Yahoo Finance 뉴스)"""
        try:
            ticker = yf.Ticker(symbol)
            news = ticker.news[:5]  # 최근 5개 뉴스
            
            formatted_news = []
            for item in news:
                formatted_news.append({
                    'title': item.get('title', ''),
                    'publisher': item.get('publisher', ''),
                    'link': item.get('link', ''),
                    'published': datetime.fromtimestamp(item.get('providerPublishTime', 0)).strftime('%Y-%m-%d %H:%M')
                })
            return formatted_news
        except:
            return []

class StockAnalysisBot:
    def __init__(self):
        self.tracker = USStockTracker()
        
    def analyze_stock(self, symbol: str) -> str:
        """종합 주식 분석"""
        stock_data = self.tracker.get_stock_info(symbol)
        if not stock_data:
            return f"❌ {symbol} 데이터를 찾을 수 없습니다."
            
        technical = self.tracker.calculate_technical_indicators(symbol)
        earnings = self.tracker.get_earnings_calendar(symbol)
        
        analysis = f"""
🔍 **{stock_data.name} ({stock_data.symbol}) 종합 분석**

📊 **현재 시세**
• 현재가: ${stock_data.current_price:,.2f}
• 전일대비: ${stock_data.change:+.2f} ({stock_data.change_percent:+.2f}%)
• 거래량: {stock_data.volume:,}
• 시가총액: ${stock_data.market_cap:,.0f}

📈 **기술적 지표**
• 5일 이평: ${technical.get('MA5', 0):.2f}
• 20일 이평: ${technical.get('MA20', 0):.2f}
• 50일 이평: ${technical.get('MA50', 0):.2f}
• RSI: {technical.get('RSI', 0):.1f}
• 20일 이평 대비: {technical.get('Price_vs_MA20', 0):+.2f}%

💰 **밸류에이션**
• PER: {stock_data.pe_ratio:.2f}
• 배당수익률: {stock_data.dividend_yield:.2f}%

📅 **실적 발표**
• 다음 실적: {earnings.get('next_earnings', 'N/A')}

🎯 **투자 의견**
"""
        
        # 간단한 투자 의견 생성
        if stock_data.change_percent > 3:
            analysis += "• 🟢 강한 상승세, 단기 차익실현 고려\n"
        elif stock_data.change_percent > 1:
            analysis += "• 🟡 상승세, 추가 상승 여력 관찰\n"
        elif stock_data.change_percent > -1:
            analysis += "• ⚪ 보합세, 방향성 확인 필요\n"
        elif stock_data.change_percent > -3:
            analysis += "• 🟡 하락세, 지지선 확인 필요\n"
        else:
            analysis += "• 🔴 급락, 매수 기회 또는 손절 고려\n"
            
        rsi = technical.get('RSI', 50)
        if rsi > 70:
            analysis += "• RSI 과매수 구간, 조정 가능성\n"
        elif rsi < 30:
            analysis += "• RSI 과매도 구간, 반등 가능성\n"
            
        analysis += f"\n⏰ 분석시간: {stock_data.last_updated}"
        
        return analysis
        
    def get_market_summary(self) -> str:
        """시장 전체 요약"""
        # 주요 지수들
        indices = ['SPY', 'QQQ', 'DIA', 'IWM']  # S&P500, NASDAQ, DOW, Russell2000
        index_data = self.tracker.get_multiple_stocks(indices)
        
        sector_perf = self.tracker.get_sector_performance()
        
        summary = "📊 **미국 주식시장 현황**\n\n"
        
        # 주요 지수
        summary += "🏛️ **주요 지수**\n"
        index_names = {'SPY': 'S&P 500', 'QQQ': 'NASDAQ', 'DIA': 'DOW', 'IWM': 'Russell 2000'}
        for symbol, data in index_data.items():
            name = index_names.get(symbol, symbol)
            summary += f"• {name}: ${data.current_price:.2f} ({data.change_percent:+.2f}%)\n"
            
        # 섹터 성과 (상위 5개, 하위 5개)
        sorted_sectors = sorted(sector_perf.items(), key=lambda x: x[1], reverse=True)
        
        summary += "\n🎯 **섹터별 성과 (상위 5개)**\n"
        for sector, perf in sorted_sectors[:5]:
            summary += f"• {sector}: {perf:+.2f}%\n"
            
        summary += "\n📉 **섹터별 성과 (하위 5개)**\n"
        for sector, perf in sorted_sectors[-5:]:
            summary += f"• {sector}: {perf:+.2f}%\n"
            
        summary += f"\n⏰ 업데이트: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        return summary

# 사용 예시 및 메인 실행부
def main():
    """메인 실행 함수"""
    bot = StockAnalysisBot()
    
    print("🚀 미국 주식 분석봇이 시작되었습니다!")
    print("\n사용 가능한 명령어:")
    print("1. 개별 종목 분석: analyze AAPL")
    print("2. 시장 현황: market")
    print("3. 관심종목 추가: add TSLA MSFT GOOGL")
    print("4. 관심종목 조회: watchlist")
    print("5. 종료: quit")
    
    while True:
        try:
            command = input("\n명령어를 입력하세요: ").strip().split()
            
            if not command:
                continue
                
            if command[0].lower() == 'quit':
                print("프로그램을 종료합니다.")
                break
                
            elif command[0].lower() == 'analyze' and len(command) > 1:
                symbol = command[1].upper()
                print(f"\n{symbol} 분석 중...")
                result = bot.analyze_stock(symbol)
                print(result)
                
            elif command[0].lower() == 'market':
                print("\n시장 현황 조회 중...")
                result = bot.get_market_summary()
                print(result)
                
            elif command[0].lower() == 'add' and len(command) > 1:
                symbols = [s.upper() for s in command[1:]]
                bot.tracker.add_to_watchlist(symbols)
                
            elif command[0].lower() == 'watchlist':
                if bot.tracker.watchlist:
                    print("\n📋 관심종목 현황:")
                    watchlist_data = bot.tracker.get_watchlist_data()
                    for symbol, data in watchlist_data.items():
                        print(f"• {data.name} ({symbol}): ${data.current_price:.2f} ({data.change_percent:+.2f}%)")
                else:
                    print("관심종목이 없습니다.")
                    
            else:
                print("올바른 명령어를 입력해주세요.")
                
        except KeyboardInterrupt:
            print("\n프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"오류가 발생했습니다: {e}")

if __name__ == "__main__":
    # 필요한 라이브러리 설치 안내
    required_packages = """
    미국 주식 분석을 위해 다음 라이브러리를 설치해주세요:
    
    pip install yfinance pandas numpy matplotlib seaborn requests aiohttp
    
    주요 기능:
    ✅ 실시간 미국 주식 시세
    ✅ 기술적 지표 분석 (RSI, 이동평균, 볼린저밴드)
    ✅ 섹터별 성과 분석
    ✅ 시장 지수 모니터링
    ✅ 관심종목 관리
    ✅ 실적 발표 일정
    ✅ 뉴스 및 센티먼트
    """
    
    print(required_packages)
    main()
