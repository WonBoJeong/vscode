# app.py - 범용 Flask 서버 (jo2s.com + liposuction.pe.kr 지원)
# 두 서버에 동일하게 배치: 
# - F:\home\yeonhoo\public_html\app.py
# - D:\home\venus\public_html\app.py

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
import yfinance as yf
import os
import socket
from datetime import datetime
import json

app = Flask(__name__)
CORS(app)  # 모든 도메인에서 접근 허용

# 서버 정보 자동 감지
def get_server_info():
    """현재 서버 정보 자동 감지"""
    hostname = socket.gethostname()
    current_path = os.getcwd()
    
    # 경로 기반으로 서버 구분
    if 'yeonhoo' in current_path or 'F:' in current_path.upper():
        return {
            'name': 'jo2s',
            'domain': 'jo2s.com',
            'port': 8443,
            'flask_port': 5000,
            'path': 'F:\\home\\yeonhoo\\public_html\\',
            'user': 'yeonhoo'
        }
    elif 'venus' in current_path or 'D:' in current_path.upper():
        return {
            'name': 'lipo',
            'domain': 'liposuction.pe.kr',
            'port': 7443,
            'flask_port': 5001,  # lipo 서버는 다른 포트 사용
            'path': 'D:\\home\\venus\\public_html\\',
            'user': 'venus'
        }
    else:
        # 기본값 (개발환경)
        return {
            'name': 'local',
            'domain': 'localhost',
            'port': 8080,
            'flask_port': 5000,
            'path': os.getcwd(),
            'user': 'developer'
        }

SERVER_INFO = get_server_info()

@app.route('/')
def index():
    """메인 페이지"""
    try:
        return send_from_directory('.', 'stock.html')
    except:
        return jsonify({
            'message': f'{SERVER_INFO["name"]} 서버 Flask API 정상 작동',
            'domain': SERVER_INFO['domain'],
            'web_url': f'https://{SERVER_INFO["domain"]}:{SERVER_INFO["port"]}/public/stock.html',
            'api_url': f'https://{SERVER_INFO["domain"]}:{SERVER_INFO["flask_port"]}/api/health'
        })

@app.route('/stock.html')
def stock_page():
    """주식 페이지"""
    return send_from_directory('.', 'stock.html')

@app.route('/public/stock.html')
def public_stock_page():
    """public 경로 주식 페이지"""
    return send_from_directory('.', 'stock.html')

@app.route('/api/server/info')
def server_info():
    """서버 정보 API"""
    return jsonify({
        'server': SERVER_INFO,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'python_version': os.sys.version,
        'flask_running': True
    })

@app.route('/api/stock/<symbol>')
def get_stock_data(symbol):
    """실제 yfinance 데이터 API"""
    try:
        print(f"[{SERVER_INFO['name']}] 📊 {symbol} 데이터 요청 처리 중...")
        
        ticker = yf.Ticker(symbol.upper())
        
        # 기본 정보
        info = ticker.info
        
        # 최신 가격 데이터 (1일)
        hist = ticker.history(period="1d")
        
        if hist.empty:
            print(f"[{SERVER_INFO['name']}] ❌ {symbol} 데이터 없음")
            return jsonify({'error': f'{symbol} 데이터를 찾을 수 없습니다'}), 404
        
        current_price = float(hist['Close'].iloc[-1])
        prev_close = float(info.get('previousClose', current_price))
        change = current_price - prev_close
        change_percent = (change / prev_close) * 100 if prev_close else 0
        
        # 30일 데이터로 RSI 계산
        try:
            hist_30d = ticker.history(period="30d")
            rsi = calculate_rsi(hist_30d['Close']) if len(hist_30d) > 14 else 50.0
        except:
            rsi = 50.0
        
        stock_data = {
            'symbol': symbol.upper(),
            'name': info.get('longName', f'{symbol.upper()} Corporation'),
            'currentPrice': round(current_price, 2),
            'previousClose': round(prev_close, 2),
            'change': round(change, 2),
            'changePercent': round(change_percent, 2),
            'dayHigh': float(info.get('dayHigh', 0)) if info.get('dayHigh') else current_price,
            'dayLow': float(info.get('dayLow', 0)) if info.get('dayLow') else current_price,
            'volume': int(info.get('volume', 0)) if info.get('volume') else 0,
            'marketCap': int(info.get('marketCap', 0)) if info.get('marketCap') else 0,
            'peRatio': float(info.get('trailingPE', 0)) if info.get('trailingPE') else 0,
            'dividendYield': float(info.get('dividendYield', 0)) * 100 if info.get('dividendYield') else 0,
            'week52High': float(info.get('fiftyTwoWeekHigh', 0)) if info.get('fiftyTwoWeekHigh') else current_price,
            'week52Low': float(info.get('fiftyTwoWeekLow', 0)) if info.get('fiftyTwoWeekLow') else current_price,
            'rsi': round(rsi, 1),
            'lastUpdated': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'server': SERVER_INFO['name']  # 어느 서버에서 조회했는지 표시
        }
        
        print(f"[{SERVER_INFO['name']}] ✅ {symbol} 데이터 전송 완료")
        return jsonify(stock_data)
        
    except Exception as e:
        print(f"[{SERVER_INFO['name']}] ❌ {symbol} 오류: {str(e)}")
        return jsonify({'error': f'데이터 조회 실패: {str(e)}'}), 500

@app.route('/api/stocks/compare')
def compare_stocks():
    """여러 종목 비교"""
    symbols = request.args.get('symbols', '').split(',')
    
    if not symbols or symbols == ['']:
        return jsonify({'error': '종목코드를 입력해주세요'}), 400
    
    results = {}
    for symbol in symbols:
        symbol = symbol.strip().upper()
        if not symbol:
            continue
            
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change_percent = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
                
                results[symbol] = {
                    'name': info.get('longName', symbol),
                    'currentPrice': round(current_price, 2),
                    'changePercent': round(change_percent, 2),
                    'marketCap': int(info.get('marketCap', 0)) if info.get('marketCap') else 0
                }
        except Exception as e:
            print(f"[{SERVER_INFO['name']}] 비교 데이터 오류 {symbol}: {e}")
            continue
    
    return jsonify(results)

@app.route('/api/market/overview')
def market_overview():
    """주요 지수 현황"""
    indices = ['SPY', 'QQQ', 'DIA', 'IWM']
    index_names = {
        'SPY': 'S&P 500',
        'QQQ': 'NASDAQ',
        'DIA': 'Dow Jones',
        'IWM': 'Russell 2000'
    }
    
    market_data = {}
    for symbol in indices:
        try:
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="2d")
            
            if not hist.empty:
                current_price = float(hist['Close'].iloc[-1])
                prev_close = float(hist['Close'].iloc[-2]) if len(hist) > 1 else current_price
                change_percent = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0
                
                market_data[symbol] = {
                    'name': index_names.get(symbol, symbol),
                    'currentPrice': round(current_price, 2),
                    'changePercent': round(change_percent, 2)
                }
        except Exception as e:
            print(f"[{SERVER_INFO['name']}] 지수 데이터 오류 {symbol}: {e}")
            continue
    
    return jsonify(market_data)

@app.route('/api/health')
def health_check():
    """서버 상태 확인"""
    return jsonify({
        'status': 'OK',
        'message': f'{SERVER_INFO["name"]} 서버 Flask yfinance API 정상 작동',
        'server_info': SERVER_INFO,
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'endpoints': {
            'stock_data': f'/api/stock/{{symbol}}',
            'compare': f'/api/stocks/compare?symbols={{symbols}}',
            'market': f'/api/market/overview',
            'health': f'/api/health'
        }
    })

def calculate_rsi(prices, period=14):
    """RSI 계산 함수"""
    try:
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return float(rsi.iloc[-1]) if not rsi.empty and not rsi.iloc[-1] != rsi.iloc[-1] else 50.0
    except:
        return 50.0

if __name__ == '__main__':
    print(f"🚀 [{SERVER_INFO['name']}] Flask yfinance 실제 데이터 서버 시작!")
    print(f"📂 서버: {SERVER_INFO['domain']}")
    print(f"📂 정적 파일 경로: {SERVER_INFO['path']}")
    print(f"🌐 웹 접속 주소: https://{SERVER_INFO['domain']}:{SERVER_INFO['port']}/")
    print(f"🌐 주식 페이지: https://{SERVER_INFO['domain']}:{SERVER_INFO['port']}/public/stock.html")
    print(f"📊 API 엔드포인트:")
    print(f"   - 서버 정보: /api/server/info")
    print(f"   - 주식 조회: /api/stock/AAPL")
    print(f"   - 비교 분석: /api/stocks/compare?symbols=AAPL,MSFT")
    print(f"   - 시장 현황: /api/market/overview")
    print(f"   - 서버 상태: /api/health")
    
    # 서버별 포트 자동 설정
    flask_port = SERVER_INFO['flask_port']
    
    # 프로덕션 환경 설정
    app.run(
        debug=False,  # 프로덕션에서는 False
        host='0.0.0.0',  # 외부 접속 허용
        port=flask_port,  # 서버별 포트
        threaded=True  # 멀티스레딩 지원
    )