import yfinance as yf
from datetime import datetime, timedelta

# 미리 설정한 주식 심볼 리스트 (예: 삼성전자, 애플, 테슬라 등)
PRESET_SYMBOLS = ['AAPL', 'TSLA', 'MSFT', 'GOOGL', '005930.KS']  # 원하는 심볼로 수정

def get_period_dates(years):
    end = datetime.today()
    start = end - timedelta(days=365 * years)
    return start.strftime('%Y-%m-%d'), end.strftime('%Y-%m-%d')

def download_stock_data(symbol, years):
    start, end = get_period_dates(years)
    df = yf.download(symbol, start=start, end=end)
    filename = f"{symbol}_{years}y.csv"
    df.to_csv(filename)
    print(f"{symbol}의 {years}년치 데이터가 {filename}에 저장되었습니다.")

def show_current_prices(symbols):
    print("현재 시세:")
    data = yf.download(symbols, period="1d")['Close'].iloc[-1]
    for symbol in symbols:
        price = data[symbol] if symbol in data else "데이터 없음"
        print(f"{symbol}: {price}")

def main():
    print("다운로드할 주식 심볼을 입력하세요 (예: AAPL):")
    symbol = input().strip().upper()
    print("기간을 선택하세요: 1, 3, 5, 10 (년)")
    years = int(input().strip())
    if years not in [1, 3, 5, 10]:
        print("올바른 기간을 선택하세요.")
        return
    download_stock_data(symbol, years)
    print("\n미리 설정한 주식들의 현재 시세를 확인합니다.")
    show_current_prices(PRESET_SYMBOLS)

if __name__ == "__main__":
    main()