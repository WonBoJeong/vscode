# API 키 완전히 불필요! 바로 실행 가능한 미국 주식 조회 프로그램

import yfinance as yf
import pandas as pd
from datetime import datetime
import time

class SimpleStockTracker:
    """API 키 없이 바로 사용하는 주식 조회"""
    
    def __init__(self):
        self.watchlist = []
        print("🚀 API 키 없이 바로 사용하는 주식 추적기 시작!")
        
    def get_stock_price(self, symbol):
        """실시간 주식 가격 조회 - API 키 불필요"""
        try:
            ticker = yf.Ticker(symbol)
            
            # 최신 데이터 가져오기
            hist = ticker.history(period="1d", interval="1m")
            info = ticker.info
            
            if hist.empty:
                return None
                
            current_price = hist['Close'].iloc[-1]
            prev_close = info.get('previousClose', current_price)
            change = current_price - prev_close
            change_percent = (change / prev_close) * 100 if prev_close else 0
            
            return {
                'symbol': symbol.upper(),
                'name': info.get('longName', symbol),
                'current_price': round(current_price, 2),
                'change': round(change, 2),
                'change_percent': round(change_percent, 2),
                'volume': info.get('volume', 0),
                'day_high': info.get('dayHigh', 0),
                'day_low': info.get('dayLow', 0),
                'market_cap': info.get('marketCap', 0),
                'pe_ratio': info.get('trailingPE', 0),
                'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            }
        except Exception as e:
            print(f"❌ {symbol} 조회 실패: {e}")
            return None
    
    def analyze_stock(self, symbol):
        """종목 종합 분석"""
        print(f"📊 {symbol} 분석 중...")
        
        data = self.get_stock_price(symbol)
        if not data:
            return f"❌ {symbol} 데이터를 가져올 수 없습니다."
        
        # 차트 데이터로 기술적 분석
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="3mo")
        
        if not hist.empty:
            # 이동평균 계산
            ma_5 = hist['Close'].rolling(5).mean().iloc[-1]
            ma_20 = hist['Close'].rolling(20).mean().iloc[-1]
            
            # 간단한 RSI 계산
            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs)).iloc[-1]
        else:
            ma_5 = ma_20 = rsi = 0
        
        # 분석 결과 포맷팅
        analysis = f"""
🔍 **{data['name']} ({data['symbol']}) 실시간 분석**

💰 **현재 시세**
├─ 현재가: ${data['current_price']:,.2f}
├─ 전일대비: ${data['change']:+.2f} ({data['change_percent']:+.2f}%)
├─ 거래량: {data['volume']:,}
├─ 일일 고가: ${data['day_high']:,.2f}
└─ 일일 저가: ${data['day_low']:,.2f}

📈 **기술적 지표**
├─ 5일 이평: ${ma_5:.2f}
├─ 20일 이평: ${ma_20:.2f}
└─ RSI(14): {rsi:.1f}

💎 **밸류에이션**
├─ 시가총액: ${data['market_cap']:,.0f}
└─ PER: {data['pe_ratio']:.2f}

🎯 **투자 의견**"""

        # 간단한 투자 시그널
        if data['change_percent'] > 3:
            analysis += "\n🟢 강한 상승! 단기 차익실현 고려"
        elif data['change_percent'] > 1:
            analysis += "\n🟡 상승세 지속, 추가 상승 관찰"
        elif data['change_percent'] > -1:
            analysis += "\n⚪ 보합세, 방향성 확인 필요"
        elif data['change_percent'] > -3:
            analysis += "\n🟡 하락, 지지선 확인 후 매수 검토"
        else:
            analysis += "\n🔴 급락! 매수 기회 또는 손절 결정 필요"
        
        if rsi > 70:
            analysis += "\n⚠️ RSI 과매수(70+), 조정 가능성"
        elif rsi < 30:
            analysis += "\n✅ RSI 과매도(30-), 반등 기대"
        
        current_price = data['current_price']
        if current_price > ma_20:
            trend = "상승"
            analysis += f"\n📈 20일 이평선({ma_20:.2f}) 위 {trend}추세"
        else:
            trend = "하락"
            analysis += f"\n📉 20일 이평선({ma_20:.2f}) 아래 {trend}추세"
        
        analysis += f"\n\n⏰ 업데이트: {data['last_updated']}"
        analysis += "\n💡 이 데이터는 15-20분 지연될 수 있습니다."
        
        return analysis
    
    def compare_stocks(self, symbols):
        """여러 종목 비교"""
        print(f"📊 {len(symbols)}개 종목 비교 분석 중...")
        
        comparison = "\n🔄 **종목 비교 분석**\n"
        comparison += "=" * 50 + "\n"
        
        stocks_data = []
        for symbol in symbols:
            data = self.get_stock_price(symbol)
            if data:
                stocks_data.append(data)
                comparison += f"\n📈 **{data['name']} ({symbol})**\n"
                comparison += f"├─ 현재가: ${data['current_price']:,.2f}\n"
                comparison += f"├─ 등락률: {data['change_percent']:+.2f}%\n"
                comparison += f"├─ 거래량: {data['volume']:,}\n"
                comparison += f"└─ PER: {data['pe_ratio']:.2f}\n"
        
        if len(stocks_data) > 1:
            # 최고 수익률과 최저 수익률
            best = max(stocks_data, key=lambda x: x['change_percent'])
            worst = min(stocks_data, key=lambda x: x['change_percent'])
            
            comparison += f"\n🏆 **오늘의 승자**: {best['name']} ({best['change_percent']:+.2f}%)"
            comparison += f"\n📉 **오늘의 패자**: {worst['name']} ({worst['change_percent']:+.2f}%)"
        
        return comparison
    
    def get_market_overview(self):
        """주요 지수 현황"""
        indices = {
            'SPY': 'S&P 500',
            'QQQ': 'NASDAQ',
            'DIA': 'Dow Jones',
            'IWM': 'Russell 2000'
        }
        
        overview = "\n🏛️ **미국 주요 지수 현황**\n"
        overview += "=" * 40 + "\n"
        
        for symbol, name in indices.items():
            data = self.get_stock_price(symbol)
            if data:
                direction = "🟢" if data['change_percent'] > 0 else "🔴"
                overview += f"{direction} {name}: ${data['current_price']:.2f} ({data['change_percent']:+.2f}%)\n"
        
        return overview

def main():
    """메인 실행 함수 - API 키 완전히 불필요!"""
    tracker = SimpleStockTracker()
    
    print("\n✨ 사용법:")
    print("• 종목 분석: analyze AAPL")
    print("• 비교 분석: compare AAPL MSFT GOOGL")
    print("• 시장 현황: market")
    print("• 종료: quit")
    
    # 인기 종목 추천
    popular_stocks = {
        'AAPL': '애플',
        'MSFT': '마이크로소프트', 
        'GOOGL': '구글',
        'AMZN': '아마존',
        'TSLA': '테슬라',
        'META': '메타',
        'NVDA': '엔비디아',
        'NFLX': '넷플릭스'
    }
    
    print(f"\n📌 인기 종목: {', '.join(popular_stocks.keys())}")
    
    while True:
        try:
            command = input("\n🎯 명령어 입력: ").strip().split()
            
            if not command:
                continue
                
            if command[0].lower() == 'quit':
                print("👋 프로그램을 종료합니다.")
                break
                
            elif command[0].lower() == 'analyze' and len(command) > 1:
                symbol = command[1].upper()
                result = tracker.analyze_stock(symbol)
                print(result)
                
            elif command[0].lower() == 'compare' and len(command) > 2:
                symbols = [s.upper() for s in command[1:]]
                result = tracker.compare_stocks(symbols)
                print(result)
                
            elif command[0].lower() == 'market':
                result = tracker.get_market_overview()
                print(result)
                
            elif command[0].lower() == 'help':
                print("\n📚 도움말:")
                print("analyze AAPL - 애플 주식 분석")
                print("compare AAPL MSFT - 애플과 마이크로소프트 비교")
                print("market - 주요 지수 현황")
                
            else:
                print("❌ 올바른 명령어를 입력해주세요. (help 입력시 도움말)")
                
        except KeyboardInterrupt:
            print("\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류: {e}")

if __name__ == "__main__":
    print("🎉 API 키 없이 바로 사용하는 주식 분석기!")
    print("📦 설치 필요: pip install yfinance pandas")
    print("🚀 준비 완료!")
    
    main()

# 🔥 즉시 테스트 가능한 예시들:
"""
# 터미널에서 바로 실행:
python simple_stock_tracker.py

# 명령어 예시:
analyze AAPL        # 애플 분석
analyze TSLA        # 테슬라 분석  
compare AAPL MSFT   # 애플 vs 마이크로소프트
market              # 시장 현황

🎯 API 키 완전히 불필요!
📊 실시간 데이터 (15-20분 지연)
💰 무료 무제한 사용
✅ 바로 실행 가능
"""