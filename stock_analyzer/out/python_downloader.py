#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🐍 Python으로 주식 데이터 다운로드
yfinance를 사용한 Yahoo Finance 데이터 수집
"""

import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import time

class PythonStockDownloader:
    def __init__(self, data_folder="data"):
        """파이썬 주식 데이터 다운로더"""
        self.data_folder = Path(data_folder)
        self.data_folder.mkdir(exist_ok=True)
        
    def download_single_stock(self, symbol, period="3y", interval="1d"):
        """단일 종목 다운로드"""
        try:
            print(f"📊 {symbol} 다운로드 중...")
            
            # yfinance로 데이터 다운로드
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                print(f"❌ {symbol}: 데이터 없음")
                return None
                
            # 컬럼명 정리
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            data.index.name = 'Date'
            
            # 파일 저장
            date_key = datetime.now().strftime("%y%m%d")
            filename = self.data_folder / f"{symbol}_{date_key}.csv"
            data.to_csv(filename)
            
            print(f"✅ {symbol}: {len(data)}일 데이터 저장 → {filename}")
            return data
            
        except Exception as e:
            print(f"❌ {symbol} 다운로드 실패: {e}")
            return None
            
    def download_multiple_stocks(self, symbols, period="3y", delay=1):
        """다중 종목 다운로드"""
        results = {}
        
        print(f"🚀 {len(symbols)}개 종목 다운로드 시작...")
        
        for i, symbol in enumerate(symbols, 1):
            print(f"[{i}/{len(symbols)}] ", end="")
            
            data = self.download_single_stock(symbol, period)
            if data is not None:
                results[symbol] = data
                
            # API 제한 방지를 위한 딜레이
            if delay > 0 and i < len(symbols):
                time.sleep(delay)
                
        print(f"\n🎉 다운로드 완료! 성공: {len(results)}/{len(symbols)}")
        return results
        
    def download_with_info(self, symbol):
        """상세 정보와 함께 다운로드"""
        try:
            ticker = yf.Ticker(symbol)
            
            # 기본 정보
            info = ticker.info
            
            # 가격 데이터
            data = ticker.history(period="3y")
            
            # 배당금 정보
            dividends = ticker.dividends
            
            # 주식 분할 정보  
            splits = ticker.splits
            
            return {
                'data': data,
                'info': info,
                'dividends': dividends,
                'splits': splits
            }
            
        except Exception as e:
            print(f"❌ {symbol} 상세 정보 다운로드 실패: {e}")
            return None

# R 스크립트와 동일한 ETF 목록
R_ETF_LIST = [
    "TQQQ", "SOXL", "FNGU", "NAIL", "TECL", "LABU", 
    "RETL", "WEBL", "DPST", "TNA", "HIBL", "BNKU",
    "DFEN", "PILL", "MIDU", "WANT", "FAS", "TPOR"
]

# 추가 인기 종목들
POPULAR_STOCKS = [
    "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", 
    "SPY", "QQQ", "VOO", "VTI", "SCHD", "JEPI", "JEPQ"
]

def download_r_equivalent_data():
    """R 스크립트와 동일한 데이터 다운로드"""
    downloader = PythonStockDownloader("data")
    
    print("🔄 R quantmod 대신 Python yfinance로 데이터 다운로드")
    print("=" * 60)
    
    # 레버리지 ETF 다운로드
    print("🚀 레버리지 ETF 다운로드...")
    etf_results = downloader.download_multiple_stocks(R_ETF_LIST, period="3y", delay=0.5)
    
    # 인기 종목 다운로드
    print("\n📈 인기 종목 다운로드...")
    stock_results = downloader.download_multiple_stocks(POPULAR_STOCKS, period="3y", delay=0.5)
    
    # 결과 요약
    total_success = len(etf_results) + len(stock_results)
    total_attempted = len(R_ETF_LIST) + len(POPULAR_STOCKS)
    
    print(f"\n📊 다운로드 완료 요약:")
    print(f"• 레버리지 ETF: {len(etf_results)}/{len(R_ETF_LIST)}")
    print(f"• 인기 종목: {len(stock_results)}/{len(POPULAR_STOCKS)}")
    print(f"• 전체 성공률: {total_success}/{total_attempted} ({total_success/total_attempted*100:.1f}%)")
    
    return etf_results, stock_results

if __name__ == "__main__":
    # 예시 1: 단일 종목 다운로드
    downloader = PythonStockDownloader()
    
    # TQQQ 데이터 다운로드
    tqqq_data = downloader.download_single_stock("TQQQ", period="3y")
    
    # 예시 2: 레버리지 ETF 전체 다운로드
    # download_r_equivalent_data()
    
    print("\n💡 사용법:")
    print("1. 기본: python python_downloader.py")
    print("2. 전체: download_r_equivalent_data() 함수 호출")
    print("3. VStock에서 바로 사용 가능!")
