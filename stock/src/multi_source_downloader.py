#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🌐 다양한 Python 주식 데이터 소스
yfinance 외에도 여러 옵션 제공
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import requests
import json

class MultiSourceDownloader:
    def __init__(self, data_folder="data"):
        """다중 소스 데이터 다운로더"""
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(exist_ok=True)
        
        # API 키들 (사용자가 설정)
        self.api_keys = {
            'alpha_vantage': None,  # https://www.alphavantage.co/
            'quandl': None,         # https://www.quandl.com/
            'polygon': None,        # https://polygon.io/
            'iex': None            # https://iexcloud.io/
        }
        
    def set_api_key(self, provider, key):
        """API 키 설정"""
        self.api_keys[provider] = key
        print(f"✅ {provider} API 키 설정됨")
        
    def download_yfinance(self, symbol, period="3y"):
        """yfinance로 다운로드"""
        try:
            import yfinance as yf
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period)
            
            if data.empty:
                return None
                
            # 기본 정보도 함께
            info = ticker.info
            
            return {
                'data': data,
                'info': info,
                'source': 'Yahoo Finance (yfinance)'
            }
            
        except ImportError:
            print("❌ yfinance 설치 필요: pip install yfinance")
            return None
        except Exception as e:
            print(f"❌ yfinance 오류: {e}")
            return None
            
    def download_alpha_vantage(self, symbol, outputsize="full"):
        """Alpha Vantage API로 다운로드"""
        if not self.api_keys['alpha_vantage']:
            print("❌ Alpha Vantage API 키가 필요합니다")
            return None
            
        try:
            url = "https://www.alphavantage.co/query"
            params = {
                'function': 'TIME_SERIES_DAILY',
                'symbol': symbol,
                'outputsize': outputsize,
                'apikey': self.api_keys['alpha_vantage']
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'Time Series (Daily)' not in data:
                print(f"❌ Alpha Vantage: {symbol} 데이터 없음")
                return None
                
            # 데이터 변환
            time_series = data['Time Series (Daily)']
            df_data = []
            
            for date, values in time_series.items():
                df_data.append({
                    'Date': pd.to_datetime(date),
                    'Open': float(values['1. open']),
                    'High': float(values['2. high']),
                    'Low': float(values['3. low']),
                    'Close': float(values['4. close']),
                    'Volume': int(values['5. volume'])
                })
                
            df = pd.DataFrame(df_data)
            df.set_index('Date', inplace=True)
            df.sort_index(inplace=True)
            
            return {
                'data': df,
                'info': data.get('Meta Data', {}),
                'source': 'Alpha Vantage'
            }
            
        except Exception as e:
            print(f"❌ Alpha Vantage 오류: {e}")
            return None
            
    def download_polygon(self, symbol, start_date=None, end_date=None):
        """Polygon.io API로 다운로드"""
        if not self.api_keys['polygon']:
            print("❌ Polygon API 키가 필요합니다")
            return None
            
        try:
            if not start_date:
                start_date = (datetime.now() - timedelta(days=1095)).strftime('%Y-%m-%d')
            if not end_date:
                end_date = datetime.now().strftime('%Y-%m-%d')
                
            url = f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/1/day/{start_date}/{end_date}"
            params = {
                'adjusted': 'true',
                'sort': 'asc',
                'apikey': self.api_keys['polygon']
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if 'results' not in data:
                print(f"❌ Polygon: {symbol} 데이터 없음")
                return None
                
            # 데이터 변환
            df_data = []
            for item in data['results']:
                df_data.append({
                    'Date': pd.to_datetime(item['t'], unit='ms'),
                    'Open': item['o'],
                    'High': item['h'],
                    'Low': item['l'],
                    'Close': item['c'],
                    'Volume': item['v']
                })
                
            df = pd.DataFrame(df_data)
            df.set_index('Date', inplace=True)
            
            return {
                'data': df,
                'info': {'symbol': symbol, 'count': data.get('resultsCount', 0)},
                'source': 'Polygon.io'
            }
            
        except Exception as e:
            print(f"❌ Polygon 오류: {e}")
            return None
            
    def download_iex_cloud(self, symbol, range_period="3y"):
        """IEX Cloud API로 다운로드"""
        if not self.api_keys['iex']:
            print("❌ IEX Cloud API 키가 필요합니다")
            return None
            
        try:
            url = f"https://cloud.iexapis.com/stable/stock/{symbol}/chart/{range_period}"
            params = {
                'token': self.api_keys['iex']
            }
            
            response = requests.get(url, params=params)
            data = response.json()
            
            if not data:
                print(f"❌ IEX Cloud: {symbol} 데이터 없음")
                return None
                
            # 데이터 변환
            df_data = []
            for item in data:
                df_data.append({
                    'Date': pd.to_datetime(item['date']),
                    'Open': item['open'],
                    'High': item['high'],
                    'Low': item['low'],
                    'Close': item['close'],
                    'Volume': item['volume']
                })
                
            df = pd.DataFrame(df_data)
            df.set_index('Date', inplace=True)
            
            return {
                'data': df,
                'info': {'symbol': symbol, 'count': len(data)},
                'source': 'IEX Cloud'
            }
            
        except Exception as e:
            print(f"❌ IEX Cloud 오류: {e}")
            return None
            
    def download_with_fallback(self, symbol, prefer_source='yfinance'):
        """여러 소스를 순차적으로 시도"""
        sources = {
            'yfinance': self.download_yfinance,
            'alpha_vantage': self.download_alpha_vantage,
            'polygon': self.download_polygon,
            'iex': self.download_iex_cloud
        }
        
        # 선호 소스를 먼저 시도
        if prefer_source in sources:
            print(f"🎯 {prefer_source}로 {symbol} 다운로드 시도...")
            result = sources[prefer_source](symbol)
            if result:
                print(f"✅ {prefer_source} 성공!")
                return result
                
        # 나머지 소스들 시도
        for source_name, source_func in sources.items():
            if source_name == prefer_source:
                continue  # 이미 시도했음
                
            print(f"🔄 {source_name}로 {symbol} 재시도...")
            result = source_func(symbol)
            if result:
                print(f"✅ {source_name} 성공!")
                return result
                
        print(f"❌ 모든 소스에서 {symbol} 다운로드 실패")
        return None
        
    def save_data(self, symbol, result):
        """데이터 저장"""
        if not result or 'data' not in result:
            return None
            
        try:
            data = result['data']
            source = result.get('source', 'Unknown')
            
            # 파일명에 소스 정보 포함
            date_key = datetime.now().strftime("%y%m%d")
            source_key = source.lower().replace(' ', '_').replace('.', '')
            filename = self.data_folder / f"{symbol}_{date_key}_{source_key}.csv"
            
            # 저장
            data.to_csv(filename)
            
            print(f"💾 {symbol} 저장: {filename}")
            return filename
            
        except Exception as e:
            print(f"❌ 저장 실패: {e}")
            return None

# 사용 예시
def demo_multi_source():
    """다중 소스 사용 예시"""
    downloader = MultiSourceDownloader()
    
    print("🌐 다중 소스 주식 데이터 다운로더 테스트")
    print("=" * 50)
    
    # 1. yfinance만 사용 (기본)
    print("\n1️⃣ yfinance로 AAPL 다운로드")
    result = downloader.download_yfinance("AAPL")
    if result:
        downloader.save_data("AAPL", result)
        
    # 2. API 키 설정 예시 (실제로는 사용자가 설정)
    # downloader.set_api_key('alpha_vantage', 'YOUR_API_KEY')
    
    # 3. 폴백 기능 테스트
    print("\n3️⃣ 폴백으로 TSLA 다운로드")
    result = downloader.download_with_fallback("TSLA")
    if result:
        downloader.save_data("TSLA", result)
        
    print("\n🎉 다중 소스 테스트 완료!")

if __name__ == "__main__":
    demo_multi_source()
