

        
        # 종목명으로 티커를 찾을 수 있는 역방향 매핑
        self.name_to_ticker = {v: k for k, v in self.watchlist.items()}

    def find_ticker(self, company_name):
        """회사명으로 티커 찾기"""
        return self.name_to_ticker.get(company_name)

    def download_stock_data(self, symbol, period_years):
        """주식 데이터 다운로드"""
        try:
            end_date = datetime.now()
            start_date = end_date - timedelta(days=period_years * 365)
            
            df = yf.download(symbol, 
                           start=start_date, 
                           end=end_date, 
                           progress=False)
            
            return df
        except Exception as e:
            print(f"데이터 다운로드 중 오류 발생: {e}")
            return None

    def get_current_price(self, symbol):
        """현재 주가 조회"""
        try:
            stock = yf.Ticker(symbol)
            current_price = stock.info['regularMarketPrice']
            return current_price
        except Exception as e:
            print(f"현재가 조회 중 오류 발생: {e}")
            return None

    def show_watchlist_prices(self):
        """관심 종목 현재가 조회"""
        print("\n=== 관심 종목 현재가 ===")
        for symbol, name in self.watchlist.items():
            price = self.get_current_price(symbol)
            if price:
                print(f"{name} ({symbol}): {price:,.0f}원")
            time.sleep(1)  # API 호출 간격 조절

    def save_stock_data(self, symbol, df, period_years):
        """주식 데이터 CSV 파일로 저장"""
        if df is not None:
            filename = f"{self.watchlist.get(symbol, symbol)}_{period_years}년_{datetime.now().strftime('%Y%m%d')}.csv"
            df.to_csv(filename, encoding='utf-8-sig')
            print(f"데이터가 {filename}로 저장되었습니다.")

def main():
    analyzer = StockAnalyzer()
    
    while True:
        print("\n=== 주식 데이터 다운로더 ===")
        print("1. 특정 기간 데이터 다운로드")
        print("2. 관심 종목 현재가 조회")
        print("3. 종료")
        
        choice = input("선택하세요 (1-3): ")
        
        if choice == '1':
            print("\n=== 관심 종목 목록 ===")
            for name in sorted(analyzer.name_to_ticker.keys()):
                ticker = analyzer.name_to_ticker[name]
                print(f"{name} ({ticker})")
            
            company_name = input("\n회사명을 입력하세요 (예: 삼성전자): ")
            symbol = analyzer.find_ticker(company_name)
            
            if not symbol:
                print("해당 회사를 찾을 수 없습니다.")
                continue
                
            print("\n기간 선택:")
            print("1. 1년")
            print("2. 3년")
            print("3. 5년")
            print("4. 10년")
            
            period_choice = input("기간을 선택하세요 (1-4): ")
            period_map = {'1': 1, '2': 3, '3': 5, '4': 10}
            
            if period_choice in period_map:
                years = period_map[period_choice]
                print(f"\n{company_name}의 {years}년 데이터 다운로드 중...")
                df = analyzer.download_stock_data(symbol, years)
                analyzer.save_stock_data(symbol, df, years)
            else:
                print("잘못된 선택입니다.")
                
        elif choice == '2':
            analyzer.show_watchlist_prices()
            
        elif choice == '3':
            print("프로그램을 종료합니다.")
            break
            
        else:
            print("잘못된 선택입니다.")

if __name__ == "__main__":
    main()