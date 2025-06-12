# quick_test.py - 설치 확인 및 애플 주식 조회

print("🔍 라이브러리 설치 확인 중...")

try:
    import yfinance as yf
    import pandas as pd
    print("✅ yfinance, pandas 설치 완료!")
    
    print("\n🍎 애플 주식 조회 중...")
    
    # 애플 주식 데이터 가져오기
    apple = yf.Ticker("AAPL")
    
    # 기본 정보
    info = apple.info
    name = info.get('longName', 'Apple Inc')
    
    # 최신 가격 (1일 데이터)
    hist = apple.history(period="1d")
    
    if not hist.empty:
        current_price = hist['Close'].iloc[-1]
        prev_close = info.get('previousClose', current_price)
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close else 0
        
        print(f"\n🎉 성공! {name} 데이터 조회 완료")
        print(f"📊 현재가: ${current_price:.2f}")
        print(f"📈 등락: ${change:+.2f} ({change_percent:+.2f}%)")
        print(f"💰 시가총액: ${info.get('marketCap', 0):,}")
        print(f"📅 업데이트: {hist.index[-1].strftime('%Y-%m-%d %H:%M:%S')}")
        
        print("\n🚀 모든 설정이 완료되었습니다!")
        print("이제 main 프로그램을 실행할 수 있습니다.")
        
    else:
        print("❌ 가격 데이터를 가져올 수 없습니다.")
        print("인터넷 연결을 확인해주세요.")
        
except ImportError as e:
    print(f"❌ 라이브러리 설치 필요: {e}")
    print("\n🔧 해결 방법:")
    print("pip install yfinance pandas")
    print("또는")
    print("pip3 install yfinance pandas")
    
except Exception as e:
    print(f"❌ 오류 발생: {e}")
    print("인터넷 연결 또는 Yahoo Finance 서비스를 확인해주세요.")

input("\n⏸️ 아무 키나 누르면 종료됩니다...")
