import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os

class StockManager:
    def __init__(self):
        # Preset stock symbols (you can modify this list)
        self.preset_stocks = {
            'Samsung Electronics': '005930.KS',
            'SK Hynix': '000660.KS',
            'NAVER': '035420.KS',
            'Kakao': '035720.KS'
        }
        
    def get_period_dates(self, years):
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365 * years)
        return start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d')

    def download_stock_data(self, symbol, years):
        start_date, end_date = self.get_period_dates(years)
        stock = yf.Ticker(symbol)
        df = stock.history(start=start_date, end=end_date)
        
        # Create downloads directory if it doesn't exist
        if not os.path.exists('downloads'):
            os.makedirs('downloads')
            
        # Save to CSV
        filename = f'downloads/{symbol}_{years}years_{datetime.now().strftime("%Y%m%d")}.csv'
        df.to_csv(filename)
        print(f"Data saved to {filename}")
        return df

    def get_current_prices(self):
        prices = {}
        for name, symbol in self.preset_stocks.items():
            try:
                stock = yf.Ticker(symbol)
                current_price = stock.info['regularMarketPrice']
                prices[name] = current_price
            except:
                prices[name] = "Failed to fetch"
        return prices

def main():
    sm = StockManager()
    
    while True:
        print("\n=== Stock Manager ===")
        print("1. Download stock data")
        print("2. Show current prices")
        print("3. Exit")
        
        choice = input("Choose an option (1-3): ")
        
        if choice == '1':
            symbol = input("Enter stock symbol (e.g., 005930.KS for Samsung): ")
            print("\nChoose period:")
            print("1. 1 year")
            print("2. 3 years")
            print("3. 5 years")
            print("4. 10 years")
            
            period_choice = input("Select period (1-4): ")
            years_map = {'1': 1, '2': 3, '3': 5, '4': 10}
            
            if period_choice in years_map:
                sm.download_stock_data(symbol, years_map[period_choice])
            else:
                print("Invalid period choice")
                
        elif choice == '2':
            prices = sm.get_current_prices()
            print("\nCurrent Stock Prices:")
            for name, price in prices.items():
                print(f"{name}: {price}")
                
        elif choice == '3':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice")

if __name__ == "__main__":
    main()