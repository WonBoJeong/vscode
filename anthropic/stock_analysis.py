import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import time
import os
import requests

class StockAnalyzer:
    def __init__(self):
        self.data_folder = "data"
        if not os.path.exists(self.data_folder):
            os.makedirs(self.data_folder)

        # 티커 정보 파일 경로
        self.ticker_file = os.path.join(self.data_folder, "korea_tickers.csv")
        
        # 티커 정보 로드 또는 다운로드
        self.load_tickers()

    def load_tickers(self):
        """한국 주식 티커 정보 로드"""
        try:
            if os.path.exists(self.ticker_file):
                print("기존 티커 파일을 불러옵니다...")
                try:
                    self.ticker_df = pd.read_csv(self.ticker_file)
                    print(f"로드된 종목 수: {len(self.ticker_df)}")
                    print("컬럼 목록:", self.ticker_df.columns.tolist())
                except Exception as e:
                    print(f"CSV 파일 로드 중 에러 발생: {e}")
                    raise
            else:
                print("티커 정보 다운로드 중...")
                try:
                    # KRX 웹사이트에서 종목 정보 가져오기
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
                    }
                    url = 'http://kind.krx.co.kr/corpgeneral/corpList.do'
                    params = {
                        'method': 'download',
                        'searchType': '13'
                    }
                    response = requests.get(url, params=params, headers=headers)
                    
                    if response.status_code != 200:
                        raise Exception(f"HTTP 에러: {response.status_code}")
                    
                    # 더 많은 기업 데이터 포함
                    backup_data = {
                        'Ticker': [
                            '005930.KS', '000660.KS', '035420.KS', '035720.KS', '051910.KS',
                            '005380.KS', '006400.KS', '207940.KS', '035720.KS', '055550.KS'
                        ],
                        'Name': [
                            '삼성전자', 'SK하이닉스', '네이버', '카카오', 'LG화학',
                            '현대차', '삼성SDI', '삼성바이오로직스', '카카오', '신한지주'
                        ]
                    }
                    self.ticker_df = pd.DataFrame(backup_data)
                    self.ticker_df.to_csv(self.ticker_file, index=False, encoding='utf-8-sig')
                    print("기본 티커 정보 저장 완료")
                    print(f"저장된 종목 수: {len(self.ticker_df)}")
                    
                except Exception as e:
                    print(f"\n=== KRX 데이터 다운로드 중 에러 발생 ===")
                    print(f"에러 유형: {type(e).__name__}")
                    print(f"에러 메시지: {str(e)}")
                    
                    # 기본 데이터로 시작
                    self.ticker_df = pd.DataFrame(backup_data)
                    self.ticker_df.to_csv(self.ticker_file, index=False, encoding='utf-8-sig')
                    print("기본 데이터로 시작합니다.")
    
        except Exception as e:
            print("\n=== 티커 정보 로드 실패 ===")
            print(f"최종 에러: {str(e)}")
            # 최소한의 백업 데이터 설정
            backup_data = {
                'Ticker': [
                    '005930.KS', '000660.KS', '035420.KS', '035720.KS', '051910.KS',
                    '005380.KS', '006400.KS', '207940.KS', '035720.KS', '055550.KS'
                ],
                'Name': [
                    '삼성전자', 'SK하이닉스', '네이버', '카카오', 'LG화학',
                    '현대차', '삼성SDI', '삼성바이오로직스', '카카오', '신한지주'
                ]
            }
            self.ticker_df = pd.DataFrame(backup_data)

    def search_company(self, keyword):
        """회사명으로 검색"""
        result = self.ticker_df[self.ticker_df['Name'].str.contains(keyword, case=False, na=False)]
        return result

        def show_menu(self):
        """메인 메뉴 표시"""
        try:
            while True:
                print("\n=== 주식 데이터 다운로더 ===")
                print("1. 종목 검색 및 다운로드")
                print("2. 종목 현재가 조회")
                print("3. 종료")
                
                try:
                    choice = input("\n선택하세요 (1-3): ")
                    
                    if choice == '1':
                        self.download_menu()
                    elif choice == '2':
                        self.show_current_prices()
                    elif choice == '3':
                        print("프로그램을 종료합니다.")
                        break
                    else:
                        print("잘못된 선택입니다. 1-3 사이의 숫자를 입력해주세요.")
                except ValueError:
                    print("잘못된 입력입니다. 다시 시도해주세요.")
                    
        except KeyboardInterrupt:
            print("\n\n프로그램을 안전하게 종료합니다.")
        except Exception as e:
            print(f"\n예기치 않은 오류가 발생했습니다: {str(e)}")
        finally:
            print("\n프로그램을 종료합니다. 이용해주셔서 감사합니다.")
    
    def download_menu(self):
        """다운로드 메뉴"""
        try:
            while True:
                print("\n=== 종목 검색 ===")
                keyword = input("검색할 회사명을 입력하세요 (종료: q): ")
                
                if keyword.lower() == 'q':
                    print("메인 메뉴로 돌아갑니다.")
                    break
                if not keyword.strip():
                    print("검색어를 입력해주세요.")
                    continue
    
                # 회사 검색
                matches = self.search_company(keyword)
                
                if len(matches) == 0:
                    print("검색 결과가 없습니다.")
                    continue
                
                # 검색 결과 출력
                print("\n=== 검색 결과 ===")
                for i, (_, row) in enumerate(matches.iterrows(), 1):
                    print(f"{i}. {row['Name']} ({row['Ticker']})")
                
                try:
                    choice = input("\n다운로드할 종목 번호를 선택하세요 (취소: q): ")
                    if choice.lower() == 'q':
                        continue
                        
                    choice = int(choice)
                    if 1 <= choice <= len(matches):
                        selected = matches.iloc[choice-1]
                        
                        # 기간 선택
                        print("\n=== 기간 선택 ===")
                        print("1. 1년")
                        print("2. 3년")
                        print("3. 5년")
                        print("4. 10년")
                        print("5. 취소")
                        
                        period_map = {'1': 1, '2': 3, '3': 5, '4': 10}
                        period_choice = input("기간을 선택하세요 (1-5): ")
                        
                        if period_choice == '5':
                            continue
                        elif period_choice in period_map:
                            years = period_map[period_choice]
                            symbol = selected['Ticker']
                            print(f"\n{selected['Name']}의 {years}년 데이터 다운로드 중...")
                            self.analyze_stock(symbol, years, selected['Name'])
                        else:
                            print("잘못된 선택입니다.")
                    else:
                        print("잘못된 선택입니다.")
                except ValueError:
                    print("잘못된 입력입니다.")
                
        except KeyboardInterrupt:
            print("\n\n검색을 중단하고 메인 메뉴로 돌아갑니다.")
        except Exception as e:
            print(f"\n오류가 발생했습니다: {str(e)}")

    def show_menu(self):
        """메인 메뉴 표시"""
        while True:
            print("\n=== 주식 데이터 다운로더 ===")
            print("1. 종목 검색 및 다운로드")
            print("2. 종목 현재가 조회")
            print("3. 종료")
            
            choice = input("선택하세요 (1-3): ")
            
            if choice == '1':
                self.download_menu()
            elif choice == '2':
                self.show_current_prices()
            elif choice == '3':
                print("프로그램을 종료합니다.")
                break
            else:
                print("잘못된 선택입니다.")

    def download_menu(self):
        """다운로드 메뉴"""
        while True:
            print("\n=== 종목 검색 ===")
            keyword = input("검색할 회사명을 입력하세요 (종료: q): ")
            
            if keyword.lower() == 'q':
                break

            # 회사 검색
            matches = self.search_company(keyword)
            
            if len(matches) == 0:
                print("검색 결과가 없습니다.")
                continue
            
            # 검색 결과 출력
            print("\n=== 검색 결과 ===")
            for i, (_, row) in enumerate(matches.iterrows(), 1):
                print(f"{i}. {row['Name']} ({row['Ticker']})")
            
            try:
                choice = int(input("\n다운로드할 종목 번호를 선택하세요: "))
                if 1 <= choice <= len(matches):
                    selected = matches.iloc[choice-1]
                    
                    # 기간 선택
                    print("\n=== 기간 선택 ===")
                    print("1. 1년")
                    print("2. 3년")
                    print("3. 5년")
                    print("4. 10년")
                    
                    period_map = {'1': 1, '2': 3, '3': 5, '4': 10}
                    period_choice = input("기간을 선택하세요 (1-4): ")
                    
                    if period_choice in period_map:
                        years = period_map[period_choice]
                        symbol = selected['Ticker']
                        print(f"\n{selected['Name']}의 {years}년 데이터 다운로드 중...")
                        self.analyze_stock(symbol, years, selected['Name'])
                    else:
                        print("잘못된 선택입니다.")
                else:
                    print("잘못된 선택입니다.")
            except ValueError:
                print("잘못된 입력입니다.")

    def show_current_prices(self):
        """현재가 조회"""
        print("\n=== 종목 검색 ===")
        keyword = input("검색할 회사명을 입력하세요: ")
        
        matches = self.search_company(keyword)
        if len(matches) == 0:
            print("검색 결과가 없습니다.")
            return
            
        print("\n=== 현재가 ===")
        for _, row in matches.iterrows():
            try:
                stock = yf.Ticker(row['Ticker'])
                current_price = stock.info['regularMarketPrice']
                print(f"{row['Name']}: {current_price:,.0f}원")
                time.sleep(1)  # API 호출 간격 조절
            except Exception as e:
                print(f"{row['Name']}: 가격 조회 실패")

    def download_stock_data(self, symbol, start_date, end_date):
        """주식 데이터 다운로드"""
        try:
            df = yf.download(symbol, start=start_date, end=end_date, progress=False)
            return df
        except Exception as e:
            print(f"데이터 다운로드 중 오류 발생: {e}")
            return pd.DataFrame()

    def calculate_technical_indicators(self, df):
        """기술적 지표 계산"""
        # 종가 기준 계산
        close = df['Close']
        
        # 이동평균선
        df['MA20'] = close.rolling(window=20).mean()
        df['MA60'] = close.rolling(window=60).mean()

        # 볼린저 밴드
        middle_band = close.rolling(window=20).mean()
        std_dev = close.rolling(window=20).std()
        df['BB_Upper'] = middle_band + (std_dev * 2)
        df['BB_Lower'] = middle_band - (std_dev * 2)

        # MACD
        exp1 = close.ewm(span=12, adjust=False).mean()
        exp2 = close.ewm(span=26, adjust=False).mean()
        df['MACD'] = exp1 - exp2
        df['Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()

        # RSI
        delta = close.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        return df

    def analyze_stock(self, symbol, period_years, company_name):
        """주식 데이터 분석"""
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365*period_years)

        df = self.download_stock_data(symbol, start_date, end_date)
        if df.empty:
            print(f"데이터가 없습니다: {company_name}")
            return

        # 기술적 지표 계산
        df = self.calculate_technical_indicators(df)
        
        self.save_stock_data(symbol, df, period_years, company_name)
        print(f"{company_name} 분석 완료")

    def save_stock_data(self, symbol, df, period_years, company_name):
        """주식 데이터 CSV 파일로 저장"""
        if df is not None and not df.empty:
            filename = f"{company_name}_{period_years}년_{datetime.now().strftime('%Y%m%d')}.csv"
            filepath = os.path.join(self.data_folder, filename)
            df.to_csv(filepath, encoding='utf-8-sig')
            print(f"데이터가 {filepath}로 저장되었습니다.")

if __name__ == "__main__":
    analyzer = StockAnalyzer()
    analyzer.show_menu()