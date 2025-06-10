#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
샘플 데이터 생성 스크립트
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path

def generate_sample_stock_data(symbol, days=1095, base_price=None):
    """샘플 주식 데이터 생성"""
    np.random.seed(hash(symbol) % 2**32)  # 종목별 고유 시드
    
    # 기본 설정
    start_date = datetime.now() - timedelta(days=days)
    dates = pd.date_range(start=start_date, periods=days, freq='D')
    
    # 종목별 초기 가격 설정
    if base_price is None:
        price_ranges = {
            'AAPL': (150, 200),
            'TSLA': (200, 300),
            'MSFT': (250, 350),
            'GOOGL': (2000, 3000),
            'AMZN': (100, 150),
            'META': (200, 350),
            'NVDA': (400, 800),
            'PLTR': (15, 30),
            'VOO': (350, 450),
            'VTV': (120, 160),
            'TQQQ': (40, 80),
            'TNA': (20, 50),
            'SOXL': (20, 40),
            'SCHD': (70, 80),
            'JEPI': (55, 65),
            'JEPQ': (50, 60),
            'TSLL': (10, 30)
        }
        
        min_price, max_price = price_ranges.get(symbol, (50, 200))
        base_price = np.random.uniform(min_price, max_price)
    
    # 가격 변동 시뮬레이션
    daily_returns = np.random.normal(0.001, 0.02, days)  # 평균 0.1%, 표준편차 2%
    
    # 종목별 특성 반영
    if symbol in ["AAPL", "MSFT", "GOOGL"]:  # 안정적 성장
        trend = np.linspace(0, 0.3, days)  # 30% 상승 트렌드
        daily_returns += trend / days
        daily_returns = np.random.normal(0.0005, 0.015, days)  # 낮은 변동성
        
    elif symbol in ["TSLA", "NVDA"]:  # 고변동성
        trend = np.linspace(0, 0.5, days)  # 50% 상승 트렌드
        daily_returns += trend / days
        daily_returns = np.random.normal(0.001, 0.035, days)  # 높은 변동성
        
    elif symbol in ["PLTR"]:  # 신생 기업 패턴
        # 초기 급등 후 조정
        initial_surge = np.exp(-np.linspace(0, 3, days//3))
        trend = np.concatenate([initial_surge, np.ones(days - len(initial_surge))])
        daily_returns = np.random.normal(0.0005, 0.025, days) * trend
        
    elif "ETF" in symbol or symbol in ["VOO", "VTV", "SCHD", "JEPI", "JEPQ"]:  # ETF 패턴
        daily_returns = np.random.normal(0.0003, 0.012, days)  # 낮은 변동성
        
    elif symbol in ["TQQQ", "TNA", "SOXL", "TSLL"]:  # 레버리지 ETF
        daily_returns = np.random.normal(0.001, 0.045, days)  # 매우 높은 변동성
    
    # 누적 수익률로 가격 계산
    price_multipliers = np.cumprod(1 + daily_returns)
    close_prices = base_price * price_multipliers
    
    # OHLCV 데이터 생성
    data = []
    for i, (date, close) in enumerate(zip(dates, close_prices)):
        # 일간 변동성
        daily_volatility = abs(daily_returns[i])
        
        # 고가, 저가 계산
        high_factor = 1 + daily_volatility * np.random.uniform(0.2, 1.0)
        low_factor = 1 - daily_volatility * np.random.uniform(0.2, 1.0)
        
        high = close * high_factor
        low = close * low_factor
        
        # 시가 계산
        if i == 0:
            open_price = close
        else:
            gap = np.random.normal(0, 0.005)  # 갭 상승/하락
            open_price = close_prices[i-1] * (1 + gap)
            
        # 실제 거래 패턴 반영 (고가 >= 종가, 저가 <= 종가)
        high = max(high, close, open_price)
        low = min(low, close, open_price)
        
        # 거래량 계산
        base_volume = {
            'AAPL': 50000000,
            'TSLA': 25000000,
            'MSFT': 30000000,
            'GOOGL': 1500000,
            'AMZN': 35000000,
            'META': 20000000,
            'NVDA': 40000000,
            'PLTR': 30000000,
            'VOO': 5000000,
            'VTV': 2000000,
            'TQQQ': 15000000,
            'TNA': 8000000,
            'SOXL': 10000000,
            'SCHD': 3000000,
            'JEPI': 2000000,
            'JEPQ': 1500000,
            'TSLL': 5000000
        }.get(symbol, 10000000)
        
        # 변동성이 클수록 거래량 증가
        volume_multiplier = 1 + abs(daily_returns[i]) * 20
        
        # 요일별 패턴 (월요일과 금요일에 거래량 증가)
        weekday = date.weekday()
        if weekday in [0, 4]:  # 월요일, 금요일
            volume_multiplier *= 1.2
        elif weekday in [2, 3]:  # 수요일, 목요일
            volume_multiplier *= 0.8
            
        volume = int(base_volume * volume_multiplier * np.random.uniform(0.5, 1.5))
        
        data.append({
            'Date': date,
            'Open': max(0.01, open_price),
            'High': max(0.01, high),
            'Low': max(0.01, low),
            'Close': max(0.01, close),
            'Volume': volume
        })
        
    df = pd.DataFrame(data)
    df.set_index('Date', inplace=True)
    
    # 주말 제거 (실제 거래일만)
    df = df[df.index.weekday < 5]
    
    return df

def create_all_sample_data():
    """모든 샘플 데이터 생성"""
    data_folder = Path("data")
    data_folder.mkdir(exist_ok=True)
    
    # 주요 종목들
    symbols = [
        'AAPL', 'TSLA', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'PLTR',
        'VOO', 'VTV', 'TQQQ', 'TNA', 'SOXL', 'SCHD', 'JEPI', 'JEPQ', 'TSLL'
    ]
    
    print("📊 샘플 주식 데이터 생성 중...")
    
    for symbol in symbols:
        try:
            print(f"  📈 {symbol} 데이터 생성 중...")
            
            # 3년 데이터 생성
            data = generate_sample_stock_data(symbol, days=1095)
            
            # CSV 파일로 저장
            csv_file = data_folder / f"{symbol}.csv"
            data.to_csv(csv_file)
            
            # 일부 종목은 Excel 형태로도 저장
            if symbol in ['AAPL', 'TSLA', 'NVDA']:
                excel_file = data_folder / f"{symbol}_data.xlsx"
                data.to_excel(excel_file)
                
            print(f"  ✅ {symbol}: {len(data)}일 데이터 저장 완료")
            
        except Exception as e:
            print(f"  ❌ {symbol} 데이터 생성 실패: {e}")
    
    print(f"\n🎉 모든 샘플 데이터 생성 완료!")
    print(f"📁 데이터 위치: {data_folder.absolute()}")
    print(f"📊 총 {len(symbols)}개 종목, 약 3년간의 일별 데이터")

if __name__ == "__main__":
    create_all_sample_data()