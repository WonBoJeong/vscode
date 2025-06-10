#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
데이터 로더 모듈
다양한 형태의 주식 데이터 파일을 로드하고 처리
"""

import pandas as pd
import numpy as np
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
import glob

class DataLoader:
    def __init__(self, data_folder="D:/vscode/stock/data"):
        """
        데이터 로더 초기화
        
        Args:
            data_folder (str): 주식 데이터가 저장된 폴더 경로
        """
        self.data_folder = Path(data_folder)
        self.supported_formats = ['.csv', '.xlsx', '.xls', '.json', '.txt']
        self.cache = {}  # 데이터 캐시
        
        print(f"📂 데이터 폴더: {self.data_folder}")
        if not self.data_folder.exists():
            print(f"⚠️ 데이터 폴더가 존재하지 않습니다: {data_folder}")
            # 샘플 데이터 생성
            self.create_sample_data()
        else:
            print(f"✅ 데이터 폴더 확인됨")
            
    def create_sample_data(self):
        """샘플 데이터 생성"""
        try:
            self.data_folder.mkdir(parents=True, exist_ok=True)
            
            # 샘플 종목들
            symbols = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "PLTR"]
            
            for symbol in symbols:
                sample_data = self.generate_sample_stock_data(symbol)
                file_path = self.data_folder / f"{symbol}.csv"
                sample_data.to_csv(file_path, index=True)
                print(f"📊 샘플 데이터 생성: {symbol}")
                
        except Exception as e:
            print(f"❌ 샘플 데이터 생성 실패: {e}")
            
    def generate_sample_stock_data(self, symbol, days=1095):  # 3년 데이터
        """샘플 주식 데이터 생성"""
        np.random.seed(hash(symbol) % 2**32)  # 종목별 고유 시드
        
        # 기본 설정
        start_date = datetime.now() - timedelta(days=days)
        dates = pd.date_range(start=start_date, periods=days, freq='D')
        
        # 초기 가격
        base_price = np.random.uniform(50, 500)
        
        # 가격 변동 시뮬레이션
        daily_returns = np.random.normal(0.001, 0.02, days)  # 평균 0.1%, 표준편차 2%
        
        # 트렌드 추가 (일부 종목에 상승 트렌드)
        if symbol in ["AAPL", "TSLA", "NVDA"]:
            trend = np.linspace(0, 0.5, days)  # 50% 상승 트렌드
            daily_returns += trend / days
            
        # 누적 수익률로 가격 계산
        price_multipliers = np.cumprod(1 + daily_returns)
        close_prices = base_price * price_multipliers
        
        # OHLCV 데이터 생성
        data = []
        for i, (date, close) in enumerate(zip(dates, close_prices)):
            # 고가, 저가, 시가 계산
            daily_volatility = abs(daily_returns[i])
            high = close * (1 + daily_volatility * np.random.uniform(0, 1))
            low = close * (1 - daily_volatility * np.random.uniform(0, 1))
            
            if i == 0:
                open_price = close
            else:
                open_price = close_prices[i-1] * (1 + np.random.normal(0, 0.005))
            
            # 거래량 (가격 변동이 클수록 거래량 증가)
            base_volume = np.random.uniform(1000000, 5000000)
            volume_multiplier = 1 + abs(daily_returns[i]) * 10
            volume = int(base_volume * volume_multiplier)
            
            data.append({
                'Date': date,
                'Open': max(0.01, open_price),
                'High': max(close, high),
                'Low': min(close, low),
                'Close': max(0.01, close),
                'Volume': volume
            })
            
        df = pd.DataFrame(data)
        df.set_index('Date', inplace=True)
        return df
        
    def find_stock_files(self, symbol):
        """특정 종목의 데이터 파일 찾기"""
        symbol = symbol.upper()
        possible_files = []
        
        for ext in self.supported_formats:
            # 정확한 파일명 매칭
            exact_file = self.data_folder / f"{symbol}{ext}"
            if exact_file.exists():
                possible_files.append(exact_file)
                
            # 패턴 매칭 (예: AAPL_data.csv, AAPL_2023.xlsx 등)
            pattern_files = list(self.data_folder.glob(f"{symbol}*{ext}"))
            possible_files.extend(pattern_files)
            
            # 대소문자 구분 없는 검색
            pattern_files_lower = list(self.data_folder.glob(f"{symbol.lower()}*{ext}"))
            possible_files.extend(pattern_files_lower)
            
        # 중복 제거
        return list(set(possible_files))
        
    def load_csv_file(self, file_path):
        """CSV 파일 로드"""
        try:
            # 다양한 구분자와 인코딩 시도
            encodings = ['utf-8', 'cp949', 'euc-kr', 'latin1']
            separators = [',', '\t', ';', '|']
            
            for encoding in encodings:
                for sep in separators:
                    try:
                        df = pd.read_csv(file_path, encoding=encoding, sep=sep)
                        if len(df.columns) > 3:  # 최소한의 컬럼 수 확인
                            return self.normalize_dataframe(df)
                    except:
                        continue
                        
            # 기본 로드 시도
            df = pd.read_csv(file_path)
            return self.normalize_dataframe(df)
            
        except Exception as e:
            print(f"❌ CSV 파일 로드 실패 {file_path}: {e}")
            return None
            
    def load_excel_file(self, file_path):
        """Excel 파일 로드"""
        try:
            # 첫 번째 시트 로드
            df = pd.read_excel(file_path, sheet_name=0)
            return self.normalize_dataframe(df)
        except Exception as e:
            print(f"❌ Excel 파일 로드 실패 {file_path}: {e}")
            return None
            
    def load_json_file(self, file_path):
        """JSON 파일 로드"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                df = pd.DataFrame(data)
            elif isinstance(data, dict):
                df = pd.DataFrame([data])
            else:
                return None
                
            return self.normalize_dataframe(df)
        except Exception as e:
            print(f"❌ JSON 파일 로드 실패 {file_path}: {e}")
            return None
            
    def normalize_dataframe(self, df):
        """데이터프레임 정규화"""
        try:
            # 컬럼명 정규화 (대소문자, 공백 처리)
            df.columns = df.columns.str.strip().str.replace(' ', '_')
            
            # 표준 컬럼명 매핑
            column_mapping = {
                # Date 컬럼
                'date': 'Date', 'timestamp': 'Date', 'time': 'Date', 'dt': 'Date',
                '날짜': 'Date', '일자': 'Date',
                
                # OHLCV 컬럼
                'open': 'Open', '시가': 'Open', 'opening_price': 'Open',
                'high': 'High', '고가': 'High', 'highest_price': 'High',
                'low': 'Low', '저가': 'Low', 'lowest_price': 'Low',
                'close': 'Close', '종가': 'Close', 'closing_price': 'Close', 'price': 'Close',
                'volume': 'Volume', '거래량': 'Volume', 'vol': 'Volume', 'trading_volume': 'Volume',
                
                # 기타
                'adj_close': 'Adj_Close', 'adjusted_close': 'Adj_Close'
            }
            
            # 컬럼명 변환
            df.columns = [column_mapping.get(col.lower(), col) for col in df.columns]
            
            # Date 컬럼 처리
            date_columns = ['Date', 'date', 'timestamp', 'time']
            date_col = None
            for col in date_columns:
                if col in df.columns:
                    date_col = col
                    break
                    
            if date_col:
                try:
                    df[date_col] = pd.to_datetime(df[date_col])
                    df.set_index(date_col, inplace=True)
                except:
                    pass
                    
            # 숫자 컬럼 변환
            numeric_columns = ['Open', 'High', 'Low', 'Close', 'Volume', 'Adj_Close']
            for col in numeric_columns:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    
            # 결측값 처리
            df = df.dropna(subset=['Close'])  # Close 가격이 없는 행 제거
            
            # 정렬
            if isinstance(df.index, pd.DatetimeIndex):
                df = df.sort_index()
                
            # 기본 컬럼 확인 및 생성
            required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_columns:
                if col not in df.columns:
                    if col == 'Volume':
                        df[col] = 1000000  # 기본 거래량
                    else:
                        df[col] = df.get('Close', 100)  # Close 가격으로 대체
                        
            return df
            
        except Exception as e:
            print(f"❌ 데이터 정규화 실패: {e}")
            return df
            
    def load_stock_data(self, symbol):
        """주식 데이터 로드"""
        symbol = symbol.upper()
        
        # 캐시 확인
        if symbol in self.cache:
            cache_time, data = self.cache[symbol]
            if datetime.now() - cache_time < timedelta(minutes=5):  # 5분 캐시
                print(f"🗂️ 캐시에서 {symbol} 데이터 반환")
                return data
                
        print(f"📈 {symbol} 데이터 로딩...")
        
        # 파일 찾기
        files = self.find_stock_files(symbol)
        
        if not files:
            print(f"❌ {symbol} 데이터 파일을 찾을 수 없습니다")
            return None
            
        # 가장 최신 파일 선택
        latest_file = max(files, key=lambda f: f.stat().st_mtime)
        print(f"📄 파일 로드: {latest_file}")
        
        # 파일 형식에 따라 로드
        file_ext = latest_file.suffix.lower()
        
        if file_ext == '.csv':
            data = self.load_csv_file(latest_file)
        elif file_ext in ['.xlsx', '.xls']:
            data = self.load_excel_file(latest_file)
        elif file_ext == '.json':
            data = self.load_json_file(latest_file)
        else:
            print(f"❌ 지원하지 않는 파일 형식: {file_ext}")
            return None
            
        if data is not None and not data.empty:
            # 캐시에 저장
            self.cache[symbol] = (datetime.now(), data)
            print(f"✅ {symbol} 데이터 로드 완료 ({len(data)}일)")
            return data
        else:
            print(f"❌ {symbol} 데이터 로드 실패")
            return None
            
    def get_available_symbols(self):
        """사용 가능한 종목 목록 반환"""
        symbols = set()
        
        for ext in self.supported_formats:
            files = list(self.data_folder.glob(f"*{ext}"))
            for file in files:
                # 파일명에서 종목 코드 추출
                name = file.stem
                # 기본적인 종목 코드 패턴 (3-5글자 대문자)
                import re
                match = re.match(r'^([A-Z]{3,5})', name.upper())
                if match:
                    symbols.add(match.group(1))
                    
        return sorted(list(symbols))
        
    def get_data_info(self, symbol):
        """데이터 정보 반환"""
        data = self.load_stock_data(symbol)
        if data is None or data.empty:
            return None
            
        info = {
            'symbol': symbol,
            'total_days': len(data),
            'start_date': str(data.index.min()),
            'end_date': str(data.index.max()),
            'latest_price': float(data['Close'].iloc[-1]),
            'price_range': {
                'min': float(data['Close'].min()),
                'max': float(data['Close'].max())
            },
            'avg_volume': int(data['Volume'].mean()),
            'columns': list(data.columns)
        }
        
        return info
        
    def export_data(self, symbol, output_path=None, format='csv'):
        """데이터 내보내기"""
        data = self.load_stock_data(symbol)
        if data is None or data.empty:
            return False
            
        if output_path is None:
            output_path = f"{symbol}_export.{format}"
            
        try:
            if format.lower() == 'csv':
                data.to_csv(output_path)
            elif format.lower() in ['xlsx', 'excel']:
                data.to_excel(output_path)
            elif format.lower() == 'json':
                data.to_json(output_path, orient='records', date_format='iso')
                
            print(f"✅ {symbol} 데이터 내보내기 완료: {output_path}")
            return True
            
        except Exception as e:
            print(f"❌ 데이터 내보내기 실패: {e}")
            return False