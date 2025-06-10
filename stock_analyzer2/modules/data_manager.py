#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Data Manager Module
데이터 다운로드, 로드, 관리 기능

Author: AI Assistant & User
Version: 1.0.0
"""

import pandas as pd
import yfinance as yf
import tkinter as tk
from tkinter import messagebox, ttk
import threading
from datetime import datetime, timedelta
from pathlib import Path
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_CONFIG, DATA_DIR, OUT_DIR
from .utils import Logger, DataValidator, FileManager
from .korean_stock_manager import KoreanStockManager

class DataManager:
    """데이터 관리 클래스"""
    
    def __init__(self):
        self.logger = Logger("DataManager")
        self.file_manager = FileManager()
        self.korean_manager = KoreanStockManager()
        
        # 현재 로드된 데이터
        self.current_data = None
        self.current_symbol = ""
        self.data_info = {}
        
        # 데이터 디렉토리 확인
        self.file_manager.ensure_dir(DATA_DIR)
        self.file_manager.ensure_dir(OUT_DIR)
    
    def download_stock_data(self, symbol, progress_callback=None):
        """주식 데이터 다운로드"""
        try:
            # 심볼 정리 및 검증
            symbol = symbol.strip().upper()
            
            # 한국 주식 코드 처리 - 6자리로 맞춤
            if symbol.isdigit():
                symbol = symbol.zfill(6)  # 앞에 0 추가하여 6자리로 만듦
                self.logger.info(f"Korean stock code formatted: {symbol}")
            
            if not DataValidator.is_valid_stock_symbol(symbol):
                raise ValueError(f"Invalid stock symbol: {symbol}")
            
            self.logger.info(f"Starting download for {symbol}")
            
            # 한국 주식 확인
            is_korean = DataValidator.is_korean_stock(symbol)
            
            if is_korean:
                yahoo_symbol = f"{symbol}.KS"
                company_info = self.korean_manager.search_by_code(symbol)
                company_name = company_info['name'] if company_info else symbol
                self.logger.info(f"Korean stock: {company_name} ({symbol})")
            else:
                yahoo_symbol = symbol
                company_name = symbol
                self.logger.info(f"US stock: {symbol}")
            
            # Yahoo Finance에서 데이터 다운로드
            if progress_callback:
                progress_callback("Connecting to Yahoo Finance...")
            
            ticker = yf.Ticker(yahoo_symbol)
            data = ticker.history(period=DATA_CONFIG['download_period'])
            
            if data.empty:
                # 한국 주식의 경우 .KQ (코스닥) 시도
                if is_korean:
                    self.logger.info(f"Trying KOSDAQ for {symbol}")
                    if progress_callback:
                        progress_callback("Trying KOSDAQ market...")
                    ticker = yf.Ticker(f"{symbol}.KQ")
                    data = ticker.history(period=DATA_CONFIG['download_period'])
                
                if data.empty:
                    raise ValueError(f"No data found for symbol: {symbol} (tried .KS and .KQ)")
            
            # 파일 저장
            if progress_callback:
                progress_callback("Saving data...")
            
            today = datetime.now().strftime(DATA_CONFIG['date_format'])
            filename = DATA_CONFIG['file_name_format'].format(symbol=symbol, date=today)
            filepath = DATA_DIR / filename
            
            # 기존 파일 백업 (같은 날짜가 아닌 경우)
            existing_files = list(DATA_DIR.glob(f"{symbol}_*.csv"))
            for existing_file in existing_files:
                if existing_file.name != filename:
                    self.file_manager.move_to_out_folder(existing_file, OUT_DIR)
            
            # 새 데이터 저장
            data.to_csv(filepath)
            
            # 메타데이터 저장
            self.data_info = {
                'symbol': symbol,
                'company_name': company_name,
                'is_korean': is_korean,
                'yahoo_symbol': yahoo_symbol,
                'filepath': str(filepath),
                'download_time': datetime.now().isoformat(),
                'data_start': data.index.min().isoformat() if not data.empty else None,
                'data_end': data.index.max().isoformat() if not data.empty else None,
                'total_rows': len(data),
                'file_size_kb': self.file_manager.get_file_size(filepath)
            }
            
            self.current_data = data
            self.current_symbol = symbol
            
            self.logger.info(f"Download completed: {filename} ({len(data)} rows)")
            
            return {
                'success': True,
                'data': data,
                'info': self.data_info,
                'message': f"Successfully downloaded {company_name} ({symbol}) data"
            }
            
        except Exception as e:
            error_msg = f"Download failed for {symbol}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'data': None,
                'info': None,
                'message': error_msg
            }
    
    def load_stock_data(self, filepath):
        """저장된 주식 데이터 로드"""
        try:
            filepath = Path(filepath)
            
            if not filepath.exists():
                raise FileNotFoundError(f"File not found: {filepath}")
            
            # CSV 파일 로드
            data = pd.read_csv(filepath, index_col=0)
            
            # 인덱스를 datetime으로 변환
            try:
                data.index = pd.to_datetime(data.index)
            except Exception as e:
                self.logger.warning(f"Date conversion failed: {e}")
            
            # 파일명에서 심볼 추출
            filename_parts = filepath.stem.split('_')
            if len(filename_parts) >= 2:
                symbol = filename_parts[0]
                # 한국 주식 코드인 경우 6자리로 맞춤
                if symbol.isdigit():
                    symbol = symbol.zfill(6)
            else:
                symbol = filepath.stem
            
            # 메타데이터 생성
            is_korean = DataValidator.is_korean_stock(symbol)
            
            if is_korean:
                company_info = self.korean_manager.search_by_code(symbol)
                company_name = company_info['name'] if company_info else symbol
            else:
                company_name = symbol
            
            self.data_info = {
                'symbol': symbol,
                'company_name': company_name,
                'is_korean': is_korean,
                'filepath': str(filepath),
                'load_time': datetime.now().isoformat(),
                'data_start': data.index.min().isoformat() if not data.empty else None,
                'data_end': data.index.max().isoformat() if not data.empty else None,
                'total_rows': len(data),
                'file_size_kb': self.file_manager.get_file_size(filepath),
                'file_modified': self.file_manager.get_file_modified_time(filepath).isoformat() if self.file_manager.get_file_modified_time(filepath) else None
            }
            
            self.current_data = data
            self.current_symbol = symbol
            
            self.logger.info(f"Data loaded: {filepath.name} ({len(data)} rows)")
            
            return {
                'success': True,
                'data': data,
                'info': self.data_info,
                'message': f"Successfully loaded {company_name} ({symbol}) data"
            }
            
        except Exception as e:
            error_msg = f"Load failed for {filepath}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'data': None,
                'info': None,
                'message': error_msg
            }
    
    def update_stock_data(self, symbol):
        """기존 데이터 업데이트"""
        try:
            # 한국 주식 코드 처리
            if symbol.isdigit():
                symbol = symbol.zfill(6)
            
            # 기존 파일 찾기
            existing_files = list(DATA_DIR.glob(f"{symbol}_*.csv"))
            
            if not existing_files:
                # 기존 파일이 없으면 새로 다운로드
                return self.download_stock_data(symbol)
            
            # 최신 파일의 날짜 확인
            latest_file = max(existing_files, key=lambda x: x.stat().st_mtime)
            file_modified = self.file_manager.get_file_modified_time(latest_file)
            
            # 오늘 날짜와 비교
            if file_modified and file_modified.date() == datetime.now().date():
                # 오늘 이미 다운로드했으면 기존 데이터 로드
                self.logger.info(f"Using today's data: {latest_file.name}")
                return self.load_stock_data(latest_file)
            
            # 새로 다운로드
            return self.download_stock_data(symbol)
            
        except Exception as e:
            error_msg = f"Update failed for {symbol}: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'data': None,
                'info': None,
                'message': error_msg
            }
    
    def get_file_list(self):
        """데이터 파일 목록 반환"""
        try:
            files = list(DATA_DIR.glob("*.csv"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            file_list = []
            
            for file in files:
                # 파일 정보 수집
                size_kb = self.file_manager.get_file_size(file)
                modified_time = self.file_manager.get_file_modified_time(file)
                
                # 심볼 추출
                filename_parts = file.stem.split('_')
                symbol = filename_parts[0] if filename_parts else file.stem
                
                # 한국 주식 코드 처리
                if symbol.isdigit():
                    symbol = symbol.zfill(6)
                
                # 회사명 확인
                is_korean = DataValidator.is_korean_stock(symbol)
                if is_korean:
                    company_info = self.korean_manager.search_by_code(symbol)
                    company_name = company_info['name'] if company_info else symbol
                    flag = "🇰🇷"
                else:
                    company_name = symbol
                    flag = "🇺🇸"
                
                file_info = {
                    'filepath': str(file),
                    'filename': file.name,
                    'symbol': symbol,
                    'company_name': company_name,
                    'display_name': f"{flag} {company_name}",
                    'is_korean': is_korean,
                    'size_kb': size_kb,
                    'modified_time': modified_time,
                    'modified_str': modified_time.strftime('%m/%d %H:%M') if modified_time else '',
                    'display_info': f"{flag} {company_name} ({symbol}) - {size_kb}KB {modified_time.strftime('%m/%d %H:%M') if modified_time else ''}"
                }
                
                file_list.append(file_info)
            
            return file_list
            
        except Exception as e:
            self.logger.error(f"File list generation failed: {e}")
            return []
    
    def get_current_data(self):
        """현재 로드된 데이터 반환"""
        return self.current_data
    
    def get_current_symbol(self):
        """현재 심볼 반환"""
        return self.current_symbol
    
    def get_data_info(self):
        """현재 데이터 정보 반환"""
        return self.data_info.copy()
    
    def cleanup_old_files(self, max_age_days=None):
        """오래된 파일 정리"""
        try:
            if max_age_days is None:
                max_age_days = DATA_CONFIG['max_file_age_days']
            
            old_files = self.file_manager.cleanup_old_files(DATA_DIR, max_age_days)
            
            if not old_files:
                return {
                    'success': True,
                    'moved_count': 0,
                    'message': f"No files older than {max_age_days} days found"
                }
            
            moved_count = 0
            for file in old_files:
                if self.file_manager.move_to_out_folder(file, OUT_DIR):
                    moved_count += 1
            
            return {
                'success': True,
                'moved_count': moved_count,
                'total_old_files': len(old_files),
                'message': f"Moved {moved_count}/{len(old_files)} old files to out folder"
            }
            
        except Exception as e:
            error_msg = f"Cleanup failed: {str(e)}"
            self.logger.error(error_msg)
            return {
                'success': False,
                'moved_count': 0,
                'message': error_msg
            }
    
    def validate_data(self, data=None):
        """데이터 검증"""
        if data is None:
            data = self.current_data
        
        if data is None or data.empty:
            return {
                'valid': False,
                'issues': ['No data available'],
                'warnings': []
            }
        
        issues = []
        warnings = []
        
        # 필수 컬럼 확인
        required_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
        missing_columns = [col for col in required_columns if col not in data.columns]
        
        if missing_columns:
            issues.append(f"Missing columns: {', '.join(missing_columns)}")
        
        # 데이터 무결성 확인
        for col in ['Open', 'High', 'Low', 'Close']:
            if col in data.columns:
                if (data[col] <= 0).any():
                    warnings.append(f"Non-positive values found in {col}")
        
        # High >= Low 확인
        if 'High' in data.columns and 'Low' in data.columns:
            if (data['High'] < data['Low']).any():
                issues.append("High price is less than Low price in some rows")
        
        # 날짜 순서 확인
        if hasattr(data.index, 'is_monotonic_increasing'):
            if not data.index.is_monotonic_increasing:
                warnings.append("Data is not sorted by date")
        
        # 데이터 양 확인
        if len(data) < 10:
            warnings.append("Very limited data (less than 10 days)")
        elif len(data) < 30:
            warnings.append("Limited data (less than 30 days)")
        
        return {
            'valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings
        }

class DownloadProgressDialog:
    """다운로드 진행 상황 다이얼로그"""
    
    def __init__(self, parent, symbol, data_manager):
        self.parent = parent
        self.symbol = symbol.strip()
        # 한국 주식 코드 처리
        if self.symbol.isdigit():
            self.symbol = self.symbol.zfill(6)
        self.data_manager = data_manager
        self.result = None
        self.cancelled = False
        
        self.create_dialog()
        self.start_download()
    
    def create_dialog(self):
        """다이얼로그 생성"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("📥 Downloading Data...")
        self.dialog.geometry("400x200")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 창 닫기 방지
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_cancel)
        
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 심볼 표시
        symbol_label = ttk.Label(main_frame, text=f"📈 {self.symbol}", 
                                font=('Segoe UI', 14, 'bold'))
        symbol_label.pack(pady=(0, 10))
        
        # 상태 메시지
        self.status_label = ttk.Label(main_frame, text="Starting download...", 
                                     font=('Segoe UI', 12))
        self.status_label.pack(pady=(0, 20))
        
        # 프로그레스 바
        self.progress_bar = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress_bar.pack(fill=tk.X, pady=(0, 20))
        self.progress_bar.start()
        
        # 취소 버튼
        cancel_button = ttk.Button(main_frame, text="❌ Cancel", 
                                  command=self.on_cancel)
        cancel_button.pack()
    
    def start_download(self):
        """백그라운드에서 다운로드 시작"""
        def download_thread():
            try:
                self.result = self.data_manager.download_stock_data(
                    self.symbol, 
                    progress_callback=self.update_status
                )
                
                if not self.cancelled:
                    self.parent.after(0, self.on_complete)
                    
            except Exception as e:
                if not self.cancelled:
                    self.result = {
                        'success': False,
                        'data': None,
                        'info': None,
                        'message': f"Download failed: {str(e)}"
                    }
                    self.parent.after(0, self.on_complete)
        
        threading.Thread(target=download_thread, daemon=True).start()
    
    def update_status(self, message):
        """상태 메시지 업데이트"""
        if not self.cancelled:
            self.parent.after(0, lambda: self.status_label.config(text=message))
    
    def on_cancel(self):
        """취소 버튼 클릭"""
        self.cancelled = True
        self.dialog.destroy()
    
    def on_complete(self):
        """다운로드 완료"""
        if not self.cancelled:
            self.dialog.destroy()
    
    def get_result(self):
        """결과 반환"""
        return self.result

def show_download_dialog(parent, symbol, data_manager):
    """다운로드 다이얼로그 표시"""
    try:
        dialog = DownloadProgressDialog(parent, symbol, data_manager)
        parent.wait_window(dialog.dialog)
        return dialog.get_result()
    except Exception as e:
        return {
            'success': False,
            'data': None,
            'info': None,
            'message': f"Dialog error: {str(e)}"
        }