#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R 스크립트 파일 형식 지원을 위한 개선된 데이터 로더
"""

import pandas as pd
import numpy as np
import os
import glob
from pathlib import Path
from datetime import datetime
import re

class RIntegratedDataLoader:
    def __init__(self, data_folder=None):
        """R 스크립트 연동 데이터 로더"""
        self.data_folder = Path(data_folder) if data_folder else Path("data")
        self.cache = {}
        
        # R 스크립트 경로들 시도
        self.r_paths = [
            Path("~/R_stats/R_stock/data").expanduser(),
            Path("D:/R_stats/R_stock/data"),
            Path("../R_stock/data"),
            self.data_folder
        ]
        
        self.active_r_path = None
        self._detect_r_path()
        
    def _detect_r_path(self):
        """R 데이터 경로 자동 감지"""
        for path in self.r_paths:
            if path.exists() and any(path.glob("*.csv")):
                self.active_r_path = path
                print(f"✅ R 데이터 경로 감지: {path}")
                break
        
        if not self.active_r_path:
            print(f"⚠️ R 데이터 경로를 찾을 수 없습니다. 기본 경로 사용: {self.data_folder}")
            self.active_r_path = self.data_folder
            
    def find_r_stock_files(self, symbol):
        """R 스크립트 형식의 파일 찾기"""
        symbol = symbol.upper()
        possible_files = []
        
        # R 스크립트 형식: SYMBOL_YYMMDD.csv
        r_pattern = f"{symbol}_*.csv"
        r_files = list(self.active_r_path.glob(r_pattern))
        
        if r_files:
            # 가장 최신 파일 선택 (날짜순)
            r_files.sort(key=lambda x: x.stem.split('_')[-1], reverse=True)
            possible_files.extend(r_files)
            
        # 기본 형식들도 확인
        basic_patterns = [f"{symbol}.csv", f"{symbol}_data.csv", f"{symbol}.xlsx"]
        for pattern in basic_patterns:
            files = list(self.active_r_path.glob(pattern))
            possible_files.extend(files)
            
        return possible_files
        
    def load_r_stock_data(self, symbol):
        """R 스크립트 데이터 로드"""
        files = self.find_r_stock_files(symbol)
        
        if not files:
            return None
            
        # 첫 번째 파일 로드 시도
        for file_path in files:
            try:
                print(f"📊 R 파일 로드: {file_path.name}")
                
                # CSV 로드
                data = pd.read_csv(file_path)
                
                # R 스크립트 형식 정규화
                data = self._normalize_r_data(data)
                
                if data is not None and not data.empty:
                    print(f"✅ {symbol}: {len(data)}일 데이터 로드 성공")
                    return data
                    
            except Exception as e:
                print(f"❌ {file_path} 로드 실패: {e}")
                continue
                
        return None
        
    def _normalize_r_data(self, data):
        """R 데이터 정규화"""
        try:
            # 컬럼명 정리
            data.columns = data.columns.str.lower().str.strip()
            
            # 날짜 컬럼 처리
            if 'date' in data.columns:
                data['date'] = pd.to_datetime(data['date'])
                data.set_index('date', inplace=True)
            elif data.index.name == 'date' or isinstance(data.index, pd.DatetimeIndex):
                pass  # 이미 날짜 인덱스
            else:
                # 첫 번째 컬럼이 날짜인 경우
                data.iloc[:, 0] = pd.to_datetime(data.iloc[:, 0])
                data.set_index(data.columns[0], inplace=True)
                
            # 컬럼명 표준화
            column_mapping = {
                'open': 'Open',
                'high': 'High', 
                'low': 'Low',
                'close': 'Close',
                'volume': 'Volume',
                'adj.close': 'Adj_Close',
                'adjusted': 'Adj_Close'
            }
            
            data.columns = [column_mapping.get(col.lower(), col.title()) for col in data.columns]
            
            # 필수 컬럼 확인
            required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
            for col in required_cols:
                if col not in data.columns:
                    if col == 'Volume':
                        data[col] = 1000000  # 기본 거래량
                    else:
                        # Close 가격으로 대체
                        data[col] = data.get('Close', 100)
                        
            # 숫자형 변환
            for col in required_cols:
                data[col] = pd.to_numeric(data[col], errors='coerce')
                
            # 결측값 제거
            data = data.dropna()
            
            # 정렬
            data = data.sort_index()
            
            return data
            
        except Exception as e:
            print(f"❌ R 데이터 정규화 실패: {e}")
            return None
            
    def get_available_r_symbols(self):
        """R 데이터에서 사용 가능한 심볼 목록"""
        symbols = set()
        
        # R 패턴 파일들 찾기
        csv_files = list(self.active_r_path.glob("*.csv"))
        
        for file in csv_files:
            name = file.stem
            
            # R 형식: SYMBOL_YYMMDD
            if '_' in name:
                symbol = name.split('_')[0].upper()
                symbols.add(symbol)
            else:
                # 기본 형식: SYMBOL
                symbols.add(name.upper())
                
        return sorted(list(symbols))
        
    def load_stock_data(self, symbol):
        """통합 주식 데이터 로드 (R + 기본)"""
        symbol = symbol.upper()
        
        # 캐시 확인
        if symbol in self.cache:
            cache_time, data = self.cache[symbol]
            if (datetime.now() - cache_time).seconds < 300:  # 5분 캐시
                return data
                
        # R 데이터 먼저 시도
        data = self.load_r_stock_data(symbol)
        
        if data is not None:
            self.cache[symbol] = (datetime.now(), data)
            return data
            
        # R 데이터가 없으면 기본 데이터 로드
        return self._load_basic_data(symbol)
        
    def _load_basic_data(self, symbol):
        """기본 데이터 로드"""
        try:
            basic_files = [
                self.data_folder / f"{symbol}.csv",
                self.data_folder / f"{symbol}_data.csv", 
                self.data_folder / f"{symbol}.xlsx"
            ]
            
            for file_path in basic_files:
                if file_path.exists():
                    if file_path.suffix == '.csv':
                        data = pd.read_csv(file_path, index_col=0, parse_dates=True)
                    else:
                        data = pd.read_excel(file_path, index_col=0, parse_dates=True)
                        
                    return self._normalize_r_data(data)
                    
            return None
            
        except Exception as e:
            print(f"❌ 기본 데이터 로드 실패: {e}")
            return None
            
    def get_data_info(self, symbol):
        """데이터 정보 상세"""
        data = self.load_stock_data(symbol)
        if data is None:
            return None
            
        # 파일 정보도 함께 반환
        files = self.find_r_stock_files(symbol)
        file_info = []
        
        for file in files[:3]:  # 최대 3개 파일 정보
            stat = file.stat()
            file_info.append({
                'name': file.name,
                'size': f"{stat.st_size / 1024:.1f} KB",
                'modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M')
            })
            
        info = {
            'symbol': symbol,
            'total_days': len(data),
            'start_date': str(data.index.min().date()),
            'end_date': str(data.index.max().date()),
            'latest_price': float(data['Close'].iloc[-1]),
            'price_range': {
                'min': float(data['Close'].min()),
                'max': float(data['Close'].max())
            },
            'avg_volume': int(data['Volume'].mean()),
            'data_source': 'R Script' if self.active_r_path != self.data_folder else 'Basic',
            'files': file_info
        }
        
        return info

# 사용 예시
if __name__ == "__main__":
    loader = RIntegratedDataLoader()
    
    # 사용 가능한 심볼 확인
    symbols = loader.get_available_r_symbols()
    print(f"📊 사용 가능한 심볼: {symbols}")
    
    # 데이터 로드 테스트
    for symbol in symbols[:3]:
        data = loader.load_stock_data(symbol)
        if data is not None:
            print(f"✅ {symbol}: {len(data)}일 데이터")
            info = loader.get_data_info(symbol)
            print(f"   📁 소스: {info['data_source']}")
            print(f"   📅 기간: {info['start_date']} ~ {info['end_date']}")
        else:
            print(f"❌ {symbol}: 데이터 로드 실패")