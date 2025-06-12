import yfinance as yf
from datetime import datetime, timedelta

def get_historical_data(ticker, period_years):
    """
    지정한 기간 동안의 주식 데이터를 다운로드하여 CSV 파일로 저장합니다.

    Args:
        ticker (str): 주식 티커 (예: '005930.KS' for 삼성전자)
        period_years (int): 다운로드할 기간 (년)
    """
    end_date = datetime.now()
    start_date = end_date - timedelta(days=period_years * 365)

    try:
        stock_data = yf.download(ticker, start=start_date.strftime('%Y-%m-%d'), end=end_date.strftime('%Y-%m-%d'))
        if stock_data.empty:
            print(f"'{ticker}'에 대한 데이터를 찾을 수 없습니다. 티커를 확인해주세요.")
            return

        file_name = f"{ticker}_{period_years}y_historical_data.csv"
        stock_data.to_csv(file_name)
        print(f"'{ticker}'의 {period_years}년치 데이터가 '{file_name}' 파일로 저장되었습니다.")

    except Exception as e:
        print(f"데이터 다운로드 중 오류가 발생했습니다: {e}")

def get_current_prices(tickers):
    """
    미리 설정된 주식 목록의 현재 시세를 출력합니다.

    Args:
        tickers (list): 주식 티커 리스트
    """
    print("\n--- 미리 설정된 주식 현재 시세 ---")
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            # 'regularMarketPrice'는 정규 시장 가격을 의미합니다.
            # 더 빠른 정보 조회를 위해 'fast_info'를 사용할 수도 있습니다.
            current_price = stock.info.get('currentPrice')
            if current_price:
                 previous_close = stock.info.get('previousClose', 0)
                 change = current_price - previous_close
                 change_percent = (change / previous_close) * 100 if previous_close != 0 else 0

                 print(f"{stock.info.get('shortName', ticker)} ({ticker}): {current_price:,.0f} 원 "
                       f"(전일 대비: {change:+.2f}, {change_percent:+.2f}%)")
            else:
                print(f"'{ticker}'의 현재 시세 정보를 가져올 수 없습니다.")

        except Exception as e:
            print(f"'{ticker}' 정보 조회 중 오류 발생: {e}")


def main():
    """
    메인 실행 함수
    """
    # 현재 시세를 조회할 주식 목록 (예: 삼성전자, SK하이닉스, 네이버, 카카오)
    predefined_tickers = ['005930.KS', '000660.KS', '035420.KS', '035720.KS']

    while True:
        print("\n======================================")
        print("1. 특정 주식 데이터 다운로드 (1/3/5/10년)")
        print("2. 미리 설정된 주식 현재 시세 조회")
        print("3. 종료")
        print("======================================")

        choice = input("원하는 기능의 번호를 입력하세요: ")

        if choice == '1':
            ticker_input = input("다운로드할 주식의 티커를 입력하세요 (예: 005930.KS): ").strip().upper()
            while True:
                period_input = input("다운로드할 기간을 선택하세요 (1, 3, 5, 10년): ")
                if period_input in ['1', '3', '5', '10']:
                    get_historical_data(ticker_input, int(period_input))
                    break
                else:
                    print("잘못된 입력입니다. 1, 3, 5, 10 중 하나를 입력해주세요.")

        elif choice == '2':
            get_current_prices(predefined_tickers)

        elif choice == '3':
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 입력입니다. 1, 2, 3 중 하나를 입력해주세요.")


if __name__ == "__main__":
    main()