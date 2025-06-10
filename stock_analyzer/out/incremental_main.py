#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VStock Advanced - 증분 업데이트 버전
파일명: 종목명_날짜.csv
기능: 기존 데이터에 최신 데이터만 추가하여 효율적 관리
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
import json
from pathlib import Path
from datetime import datetime, timedelta
import threading
import queue

# yfinance 임포트 시도
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
    print("✅ yfinance 사용 가능")
except ImportError:
    YFINANCE_AVAILABLE = False
    print("⚠️ yfinance 없음. 'pip install yfinance'로 설치 권장")

class IncrementalStockDownloader:
    def __init__(self):
        """증분 업데이트 주식 분석기"""
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.current_data = None
        self.create_widgets()
        
    def setup_window(self):
        """윈도우 설정"""
        self.root.title("📈 VStock Advanced - 증분 업데이트 시스템")
        self.root.geometry("1400x900")
        self.root.minsize(1000, 700)
        
        # 화면 중앙 배치
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def load_config(self):
        """설정 로드"""
        config_path = Path("config/config.json")
        
        default_config = {
            "data_folder": "data",
            "initial_download_period": "3y",  # 초기 다운로드 기간
            "file_name_format": "{symbol}_{date}.csv",  # 파일명 형식
            "date_format": "%Y%m%d",  # 날짜 형식
            "etf_symbols": [
                "TQQQ", "SOXL", "FNGU", "NAIL", "TECL", "LABU", 
                "RETL", "WEBL", "DPST", "TNA", "HIBL", "BNKU",
                "DFEN", "PILL", "MIDU", "WANT", "FAS", "TPOR"
            ],
            "popular_symbols": [
                "AAPL", "MSFT", "GOOGL", "AMZN", "TSLA", "META", "NVDA", 
                "SPY", "QQQ", "VOO", "VTI", "SCHD", "JEPI", "JEPQ"
            ],
            "default_symbols": [
                "TQQQ", "SOXL", "FNGU", "TNA", "AAPL", "TSLA", "NVDA"
            ]
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
        except:
            self.config = default_config
            
    def save_config(self):
        """설정 저장"""
        config_path = Path("config/config.json")
        config_path.parent.mkdir(exist_ok=True)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 저장 실패: {e}")
            
    def get_file_path(self, symbol, date=None):
        """파일 경로 생성"""
        if date is None:
            date = datetime.now()
        elif isinstance(date, str):
            date = datetime.strptime(date, self.config['date_format'])
            
        date_str = date.strftime(self.config['date_format'])
        filename = self.config['file_name_format'].format(symbol=symbol, date=date_str)
        
        return Path(self.config['data_folder']) / filename
        
    def find_existing_file(self, symbol):
        """기존 파일 찾기"""
        data_folder = Path(self.config['data_folder'])
        if not data_folder.exists():
            return None, None
            
        # 해당 종목의 모든 파일 찾기
        pattern = f"{symbol}_*.csv"
        files = list(data_folder.glob(pattern))
        
        if not files:
            return None, None
            
        # 가장 최신 파일 선택 (날짜 기준)
        latest_file = None
        latest_date = None
        
        for file in files:
            try:
                # 파일명에서 날짜 추출
                name_parts = file.stem.split('_')
                if len(name_parts) >= 2:
                    date_str = name_parts[1]
                    file_date = datetime.strptime(date_str, self.config['date_format'])
                    
                    if latest_date is None or file_date > latest_date:
                        latest_date = file_date
                        latest_file = file
                        
            except ValueError:
                continue  # 날짜 파싱 실패시 무시
                
        return latest_file, latest_date
        
    def load_existing_data(self, file_path):
        """기존 데이터 로드"""
        try:
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            
            # 컬럼명 정규화
            expected_columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in expected_columns):
                # 컬럼명 매핑 시도
                column_mapping = {
                    col.lower(): col for col in expected_columns
                }
                data.columns = [column_mapping.get(col.lower(), col) for col in data.columns]
                
            return data
            
        except Exception as e:
            print(f"기존 데이터 로드 실패: {e}")
            return None
            
    def download_incremental_data(self, symbol):
        """증분 데이터 다운로드"""
        if not YFINANCE_AVAILABLE:
            self.log_message(f"❌ yfinance 없음 - {symbol} 다운로드 불가")
            return None
            
        try:
            # 기존 파일 확인
            existing_file, latest_date = self.find_existing_file(symbol)
            
            if existing_file and latest_date:
                # 기존 데이터 로드
                existing_data = self.load_existing_data(existing_file)
                
                if existing_data is not None:
                    # 마지막 데이터 날짜 확인
                    last_data_date = existing_data.index.max()
                    
                    # 다음날부터 현재까지 데이터 다운로드
                    start_date = last_data_date + timedelta(days=1)
                    end_date = datetime.now()
                    
                    self.log_message(f"📊 {symbol} 증분 업데이트: {start_date.strftime('%Y-%m-%d')} ~ {end_date.strftime('%Y-%m-%d')}")
                    
                    # 새 데이터가 필요한지 확인
                    if start_date.date() >= end_date.date():
                        self.log_message(f"✅ {symbol}: 이미 최신 데이터임")
                        return {
                            'data': existing_data,
                            'updated': False,
                            'filename': existing_file
                        }
                        
                    # yfinance로 증분 데이터 다운로드
                    ticker = yf.Ticker(symbol)
                    new_data = ticker.history(start=start_date, end=end_date)
                    
                    if new_data.empty:
                        self.log_message(f"✅ {symbol}: 새로운 데이터 없음")
                        return {
                            'data': existing_data,
                            'updated': False,
                            'filename': existing_file
                        }
                        
                    # 데이터 컬럼 정규화
                    new_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                    
                    # 기존 데이터와 합치기
                    combined_data = pd.concat([existing_data, new_data])
                    combined_data = combined_data[~combined_data.index.duplicated(keep='last')]
                    combined_data.sort_index(inplace=True)
                    
                    # 새 파일명으로 저장 (오늘 날짜)
                    new_file_path = self.get_file_path(symbol)
                    new_file_path.parent.mkdir(exist_ok=True)
                    combined_data.to_csv(new_file_path)
                    
                    # 기존 파일 삭제 (선택적)
                    if new_file_path != existing_file:
                        try:
                            existing_file.unlink()  # 삭제
                        except:
                            pass  # 삭제 실패시 무시
                            
                    self.log_message(f"✅ {symbol}: {len(new_data)}일 새 데이터 추가 → {new_file_path.name}")
                    
                    return {
                        'data': combined_data,
                        'updated': True,
                        'new_records': len(new_data),
                        'filename': new_file_path
                    }
                    
            # 기존 파일이 없으면 전체 다운로드
            self.log_message(f"📊 {symbol} 초기 다운로드 ({self.config['initial_download_period']})...")
            
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=self.config['initial_download_period'])
            
            if data.empty:
                self.log_message(f"❌ {symbol}: 데이터 없음")
                return None
                
            # 컬럼 정규화
            data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            
            # 파일 저장
            file_path = self.get_file_path(symbol)
            file_path.parent.mkdir(exist_ok=True)
            data.to_csv(file_path)
            
            self.log_message(f"✅ {symbol}: {len(data)}일 초기 데이터 저장 → {file_path.name}")
            
            return {
                'data': data,
                'updated': True,
                'new_records': len(data),
                'filename': file_path
            }
            
        except Exception as e:
            self.log_message(f"❌ {symbol} 다운로드 실패: {e}")
            return None
            
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 헤더
        self.create_header(main_frame)
        
        # 메인 콘텐츠
        self.create_main_content(main_frame)
        
        # 상태바
        self.create_statusbar(main_frame)
        
    def create_header(self, parent):
        """헤더 생성"""
        header_frame = ttk.LabelFrame(parent, text="📈 VStock Advanced - 증분 업데이트 시스템", padding="20")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 제목 영역
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="스마트 증분 데이터 수집 & 분석", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # 시스템 정보
        info_label = ttk.Label(title_frame, text="📁 종목명_날짜.csv | 🔄 자동 증분 업데이트", 
                              font=('Segoe UI', 10))
        info_label.pack(side=tk.RIGHT)
        
        # 검색 및 다운로드 영역
        control_frame = ttk.Frame(header_frame)
        control_frame.pack(fill=tk.X)
        
        # 종목 입력
        input_frame = ttk.LabelFrame(control_frame, text="📍 종목 분석/업데이트", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X)
        
        ttk.Label(entry_frame, text="종목:", font=('Segoe UI', 11)).pack(side=tk.LEFT)
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(entry_frame, textvariable=self.symbol_var, 
                                     font=('Segoe UI', 11), width=10)
        self.symbol_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.symbol_entry.bind('<Return>', lambda e: self.smart_update_and_analyze())
        
        # 버튼들
        btn_frame = ttk.Frame(entry_frame)
        btn_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(btn_frame, text="🔍 분석만", command=self.analyze_only).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="🔄 업데이트", command=self.update_only).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📊 업데이트+분석", command=self.smart_update_and_analyze).pack(side=tk.LEFT, padx=2)
        
        # 빠른 선택 영역
        quick_frame = ttk.LabelFrame(control_frame, text="🚀 빠른 선택", padding="5")
        quick_frame.pack(side=tk.LEFT, padx=(0, 10))
        
        # 레버리지 ETF
        etf_frame = ttk.Frame(quick_frame)
        etf_frame.pack(fill=tk.X)
        ttk.Label(etf_frame, text="ETF:", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        for symbol in ["TQQQ", "SOXL", "FNGU", "TNA"]:
            btn = ttk.Button(etf_frame, text=symbol, width=6,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=1)
            
        # 인기 종목
        stock_frame = ttk.Frame(quick_frame)
        stock_frame.pack(fill=tk.X)
        ttk.Label(stock_frame, text="주식:", font=('Segoe UI', 9)).pack(side=tk.LEFT)
        
        for symbol in ["AAPL", "TSLA", "NVDA", "MSFT"]:
            btn = ttk.Button(stock_frame, text=symbol, width=6,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=1)
            
        # 일괄 업데이트 영역
        batch_frame = ttk.LabelFrame(control_frame, text="📦 일괄 업데이트", padding="10")
        batch_frame.pack(side=tk.RIGHT)
        
        ttk.Button(batch_frame, text="🚀 레버리지ETF", 
                  command=self.batch_update_etfs).pack(pady=2)
        ttk.Button(batch_frame, text="📈 인기종목", 
                  command=self.batch_update_stocks).pack(pady=2)
        ttk.Button(batch_frame, text="🌟 전체", 
                  command=self.batch_update_all).pack(pady=2)
        
    def create_main_content(self, parent):
        """메인 콘텐츠 생성"""
        content_frame = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (차트)
        self.left_panel = ttk.LabelFrame(content_frame, text="📊 차트 분석", padding="10")
        content_frame.add(self.left_panel, weight=3)
        
        # 오른쪽 패널 (정보)
        self.right_panel = ttk.LabelFrame(content_frame, text="📋 정보 & 로그", padding="10")
        content_frame.add(self.right_panel, weight=1)
        
        # 초기 메시지
        self.show_initial_message()
        self.create_info_panel()
        
    def create_statusbar(self, parent):
        """상태바 생성"""
        status_frame = ttk.Frame(parent)
        status_frame.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
        self.status_label = ttk.Label(status_frame, text="준비", 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # yfinance 상태
        yf_status = "🟢 yfinance 사용가능" if YFINANCE_AVAILABLE else "🔴 yfinance 없음"
        self.yf_status_label = ttk.Label(status_frame, text=yf_status, 
                                        relief=tk.SUNKEN, anchor=tk.E)
        self.yf_status_label.pack(side=tk.RIGHT)
        
    def show_initial_message(self):
        """초기 메시지"""
        if YFINANCE_AVAILABLE:
            welcome_text = """
🚀 스마트 증분 업데이트 시스템

✨ 핵심 기능:
• 📁 파일명: 종목명_날짜.csv (예: TQQQ_20250109.csv)
• 🔄 증분 업데이트: 마지막 날짜 이후 데이터만 다운로드
• 📊 즉시 분석: 수년간 누적 데이터로 정확한 기술적 분석
• 💾 효율적 저장: 중복 다운로드 방지, 빠른 업데이트

🎯 사용법:
1. 종목 입력 후 "📊 업데이트+분석" 클릭
2. 기존 파일 있으면 → 증분 업데이트 후 분석
3. 기존 파일 없으면 → 3년 데이터 다운로드 후 분석

💡 장점:
• ⚡ 빠른 업데이트 (새 데이터만)
• 📈 완전한 분석 (전체 히스토리)
• 💾 공간 절약 (중복 제거)
            """
        else:
            welcome_text = """
⚠️ yfinance 라이브러리가 필요합니다

📦 설치 방법:
pip install yfinance

🔧 설치 후:
• 증분 업데이트 시스템 활성화
• Yahoo Finance 실시간 연동
• 효율적인 데이터 관리

💾 현재는 기존 파일만 분석 가능합니다.
            """
            
        welcome_label = ttk.Label(self.left_panel, text=welcome_text, 
                                 font=('Segoe UI', 11), justify=tk.CENTER)
        welcome_label.pack(expand=True)
        
    def create_info_panel(self):
        """정보 패널 생성"""
        # 노트북 탭
        self.info_notebook = ttk.Notebook(self.right_panel)
        self.info_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 종목 정보 탭
        self.stock_info_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.stock_info_frame, text="📋 종목정보")
        
        # 업데이트 로그 탭
        self.update_log_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.update_log_frame, text="🔄 업데이트")
        
        # 파일 관리 탭
        self.files_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.files_frame, text="📁 파일관리")
        
        self.create_stock_info_tab()
        self.create_update_log_tab()
        self.create_files_tab()
        
    def create_stock_info_tab(self):
        """종목 정보 탭"""
        self.info_labels = {}
        info_fields = [
            ("symbol", "종목 코드"),
            ("price", "현재가"),
            ("change", "전일대비"),
            ("change_percent", "변동률"),
            ("volume", "거래량"),
            ("data_period", "데이터 기간"),
            ("total_days", "총 일수"),
            ("last_update", "마지막 업데이트"),
            ("file_name", "파일명"),
            ("file_size", "파일 크기")
        ]
        
        for field, label_text in info_fields:
            frame = ttk.Frame(self.stock_info_frame)
            frame.pack(fill=tk.X, pady=3)
            
            ttk.Label(frame, text=f"{label_text}:", 
                     font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
            self.info_labels[field] = ttk.Label(frame, text="-", 
                                               font=('Segoe UI', 9))
            self.info_labels[field].pack(side=tk.RIGHT)
            
    def create_update_log_tab(self):
        """업데이트 로그 탭"""
        # 로그 텍스트
        self.log_text = tk.Text(self.update_log_frame, height=20, 
                               font=('Consolas', 9), wrap=tk.WORD)
        
        log_scrollbar = ttk.Scrollbar(self.update_log_frame, 
                                     orient=tk.VERTICAL, 
                                     command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 초기 로그
        self.log_message("🚀 VStock Advanced 증분 업데이트 시스템 시작")
        self.log_message("📁 파일 형식: 종목명_날짜.csv")
        self.log_message("🔄 증분 업데이트: 마지막 날짜 이후 데이터만 추가")
        
    def create_files_tab(self):
        """파일 관리 탭"""
        # 컨트롤 버튼들
        control_frame = ttk.Frame(self.files_frame)
        control_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(control_frame, text="🔄 새로고침", 
                  command=self.refresh_file_list).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="🗑️ 정리", 
                  command=self.clean_old_files).pack(side=tk.LEFT, padx=2)
        ttk.Button(control_frame, text="📂 폴더열기", 
                  command=self.open_data_folder).pack(side=tk.LEFT, padx=2)
        
        # 파일 리스트
        self.file_listbox = tk.Listbox(self.files_frame, height=15,
                                      font=('Consolas', 9))
        
        file_scrollbar = ttk.Scrollbar(self.files_frame, 
                                      orient=tk.VERTICAL,
                                      command=self.file_listbox.yview)
        self.file_listbox.configure(yscrollcommand=file_scrollbar.set)
        
        self.file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.file_listbox.bind('<Double-Button-1>', self.on_file_double_click)
        
        # 초기 파일 목록 로드
        self.refresh_file_list()
        
    def log_message(self, message):
        """로그 메시지 추가"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.root.update()
        
    def quick_analyze(self, symbol):
        """빠른 분석"""
        self.symbol_var.set(symbol)
        self.smart_update_and_analyze()
        
    def analyze_only(self):
        """분석만 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        # 기존 파일에서 데이터 로드
        existing_file, _ = self.find_existing_file(symbol)
        if not existing_file:
            messagebox.showwarning("경고", f"{symbol} 데이터 파일이 없습니다.\n'🔄 업데이트' 버튼을 먼저 눌러주세요.")
            return
            
        data = self.load_existing_data(existing_file)
        if data is None:
            messagebox.showerror("오류", f"{symbol} 파일을 읽을 수 없습니다.")
            return
            
        self.analyze_stock(symbol, data, existing_file)
        
    def update_only(self):
        """업데이트만 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        result = self.download_incremental_data(symbol)
        if result:
            self.refresh_file_list()
            if result['updated']:
                messagebox.showinfo("완료", f"{symbol} 업데이트 완료!\n새로운 데이터: {result.get('new_records', 0)}일")
            else:
                messagebox.showinfo("정보", f"{symbol}는 이미 최신 데이터입니다.")
        
    def smart_update_and_analyze(self):
        """스마트 업데이트 + 분석"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        self.status_label.config(text=f"{symbol} 스마트 업데이트 중...")
        
        # 증분 업데이트 실행
        result = self.download_incremental_data(symbol)
        
        if result and 'data' in result:
            # 바로 분석 실행
            self.analyze_stock(symbol, result['data'], result['filename'])
            self.refresh_file_list()
            
            # 상태 메시지
            if result['updated']:
                status_msg = f"{symbol} 업데이트+분석 완료 (새 데이터: {result.get('new_records', 0)}일)"
            else:
                status_msg = f"{symbol} 분석 완료 (최신 데이터 확인됨)"
                
            self.status_label.config(text=status_msg)
        else:
            self.status_label.config(text=f"{symbol} 업데이트 실패")
            
    def analyze_stock(self, symbol, data, file_path=None):
        """주식 분석 실행"""
        try:
            self.current_data = data
            
            # 차트 생성
            self.create_analysis_chart(symbol, data)
            
            # 정보 업데이트
            self.update_stock_info(symbol, data, file_path)
            
        except Exception as e:
            messagebox.showerror("오류", f"분석 실패: {e}")
            
    def create_analysis_chart(self, symbol, data):
        """분석 차트 생성"""
        # 기존 위젯 제거
        for widget in self.left_panel.winfo_children():
            widget.destroy()
            
        # Figure 생성
        fig = Figure(figsize=(12, 8), facecolor='white')
        
        # 서브플롯
        ax1 = fig.add_subplot(3, 1, 1)  # 가격
        ax2 = fig.add_subplot(3, 1, 2)  # 거래량
        ax3 = fig.add_subplot(3, 1, 3)  # RSI
        
        # 가격 차트
        ax1.plot(data.index, data['Close'], 'b-', linewidth=2, label='종가')
        
        # 이동평균
        if len(data) > 20:
            ma20 = data['Close'].rolling(20).mean()
            ax1.plot(data.index, ma20, 'orange', linewidth=1.5, label='MA20')
        if len(data) > 50:
            ma50 = data['Close'].rolling(50).mean()
            ax1.plot(data.index, ma50, 'red', linewidth=1.5, label='MA50')
        if len(data) > 200:
            ma200 = data['Close'].rolling(200).mean()
            ax1.plot(data.index, ma200, 'purple', linewidth=1.5, label='MA200')
            
        ax1.set_title(f'{symbol} - 가격 차트 ({len(data)}일 데이터)', fontsize=14, fontweight='bold')
        ax1.set_ylabel('가격 ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 거래량
        colors = ['g' if c >= o else 'r' for c, o in zip(data['Close'], data['Open'])]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.6)
        if len(data) > 20:
            vol_ma = data['Volume'].rolling(20).mean()
            ax2.plot(data.index, vol_ma, 'purple', linewidth=1, label='거래량 MA20')
            ax2.legend()
        ax2.set_title('거래량')
        ax2.set_ylabel('거래량')
        ax2.grid(True, alpha=0.3)
        
        # RSI
        try:
            close = data['Close']
            delta = close.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(14).mean()
            avg_loss = loss.rolling(14).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            ax3.plot(data.index, rsi, 'purple', linewidth=2, label='RSI(14)')
            ax3.axhline(70, color='r', linestyle='--', alpha=0.7, label='과매수(70)')
            ax3.axhline(30, color='g', linestyle='--', alpha=0.7, label='과매도(30)')
            ax3.axhline(50, color='gray', linestyle='-', alpha=0.5)
            ax3.fill_between(data.index, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(data.index, 0, 30, alpha=0.1, color='green')
            
            # 최신 RSI 값 표시
            latest_rsi = rsi.iloc[-1]
            ax3.text(0.02, 0.95, f'현재 RSI: {latest_rsi:.1f}', 
                    transform=ax3.transAxes, fontsize=12, fontweight='bold',
                    bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
            
            ax3.set_title('RSI (Relative Strength Index)')
            ax3.set_ylabel('RSI')
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
        except Exception as e:
            ax3.text(0.5, 0.5, f'RSI 계산 오류: {e}', 
                   transform=ax3.transAxes, ha='center')
            
        fig.tight_layout()
        
        # Canvas
        canvas = FigureCanvasTkAgg(fig, self.left_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_stock_info(self, symbol, data, file_path=None):
        """종목 정보 업데이트"""
        try:
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100
            
            # 파일 정보
            file_info = {}
            if file_path:
                stat = file_path.stat()
                file_info = {
                    'file_name': file_path.name,
                    'file_size': f"{stat.st_size / 1024:.1f} KB"
                }
            
            # 정보 업데이트
            info_updates = {
                'symbol': symbol,
                'price': f"${latest['Close']:.2f}",
                'change': f"${change:+.2f}",
                'change_percent': f"{change_percent:+.2f}%",
                'volume': f"{latest['Volume']:,}",
                'data_period': f"{data.index.min().date()} ~ {data.index.max().date()}",
                'total_days': f"{len(data)}일",
                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M"),
                **file_info
            }
            
            # 레이블 업데이트
            for field, value in info_updates.items():
                if field in self.info_labels:
                    self.info_labels[field].config(text=value)
                    
            # 색상 적용
            color = 'green' if change >= 0 else 'red'
            self.info_labels['change'].config(foreground=color)
            self.info_labels['change_percent'].config(foreground=color)
            
        except Exception as e:
            print(f"정보 업데이트 오류: {e}")
            
    def batch_update_etfs(self):
        """레버리지 ETF 일괄 업데이트"""
        self.batch_update(self.config['etf_symbols'], "레버리지 ETF")
        
    def batch_update_stocks(self):
        """인기 종목 일괄 업데이트"""
        self.batch_update(self.config['popular_symbols'], "인기 종목")
        
    def batch_update_all(self):
        """전체 일괄 업데이트"""
        all_symbols = self.config['etf_symbols'] + self.config['popular_symbols']
        self.batch_update(all_symbols, "전체 종목")
        
    def batch_update(self, symbols, category_name):
        """일괄 업데이트 실행"""
        if not YFINANCE_AVAILABLE:
            messagebox.showwarning("경고", "yfinance가 설치되지 않았습니다.")
            return
            
        def update_thread():
            total = len(symbols)
            success_count = 0
            updated_count = 0
            
            self.log_message(f"🚀 {category_name} 일괄 업데이트 시작 ({total}개)")
            
            for i, symbol in enumerate(symbols):
                self.status_label.config(text=f"{category_name} 업데이트 중... ({i+1}/{total}) {symbol}")
                
                result = self.download_incremental_data(symbol)
                if result:
                    success_count += 1
                    if result['updated']:
                        updated_count += 1
                        
                # API 제한 방지
                if i < total - 1:
                    time.sleep(0.3)
                    
            # 완료
            self.log_message(f"🎉 {category_name} 일괄 업데이트 완료!")
            self.log_message(f"   성공: {success_count}/{total}, 업데이트: {updated_count}")
            
            self.status_label.config(text=f"{category_name} 업데이트 완료 ({updated_count}개 업데이트)")
            
            # 파일 목록 새로고침
            self.root.after(100, self.refresh_file_list)
            
        # 백그라운드 스레드로 실행
        thread = threading.Thread(target=update_thread)
        thread.daemon = True
        thread.start()
        
    def refresh_file_list(self):
        """파일 목록 새로고침"""
        try:
            self.file_listbox.delete(0, tk.END)
            
            data_folder = Path(self.config['data_folder'])
            if not data_folder.exists():
                self.file_listbox.insert(tk.END, "📁 데이터 폴더가 없습니다")
                return
                
            csv_files = list(data_folder.glob("*.csv"))
            
            if not csv_files:
                self.file_listbox.insert(tk.END, "📄 CSV 파일이 없습니다")
                return
                
            # 파일을 종목별로 그룹화
            file_groups = {}
            for file in csv_files:
                try:
                    name_parts = file.stem.split('_')
                    if len(name_parts) >= 2:
                        symbol = name_parts[0]
                        date_str = name_parts[1]
                        
                        if symbol not in file_groups:
                            file_groups[symbol] = []
                        file_groups[symbol].append((file, date_str))
                except:
                    continue
                    
            # 종목별로 정렬해서 표시
            for symbol in sorted(file_groups.keys()):
                files = file_groups[symbol]
                # 날짜순 정렬 (최신이 먼저)
                files.sort(key=lambda x: x[1], reverse=True)
                
                # 최신 파일만 표시
                latest_file, latest_date = files[0]
                stat = latest_file.stat()
                size_kb = stat.st_size / 1024
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d %H:%M")
                
                info = f"{symbol:<8} {latest_date} {size_kb:>6.1f}KB {mod_time}"
                self.file_listbox.insert(tk.END, info)
                
                # 여러 버전이 있으면 개수 표시
                if len(files) > 1:
                    self.file_listbox.insert(tk.END, f"         └─ (+{len(files)-1}개 이전 버전)")
                
        except Exception as e:
            self.file_listbox.insert(tk.END, f"오류: {e}")
            
    def on_file_double_click(self, event):
        """파일 더블클릭 처리"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
            
        file_info = self.file_listbox.get(selection[0])
        if not file_info or "📁" in file_info or "📄" in file_info or "└─" in file_info:
            return
            
        # 파일명에서 심볼 추출
        symbol = file_info.split()[0]
        
        self.symbol_var.set(symbol)
        self.analyze_only()
        
    def clean_old_files(self):
        """오래된 파일 정리"""
        try:
            data_folder = Path(self.config['data_folder'])
            if not data_folder.exists():
                return
                
            # 종목별로 파일 그룹화
            file_groups = {}
            for file in data_folder.glob("*.csv"):
                try:
                    name_parts = file.stem.split('_')
                    if len(name_parts) >= 2:
                        symbol = name_parts[0]
                        date_str = name_parts[1]
                        
                        if symbol not in file_groups:
                            file_groups[symbol] = []
                        file_groups[symbol].append((file, date_str))
                except:
                    continue
                    
            deleted_count = 0
            
            # 각 종목별로 최신 파일만 남기고 삭제
            for symbol, files in file_groups.items():
                if len(files) > 1:
                    # 날짜순 정렬
                    files.sort(key=lambda x: x[1], reverse=True)
                    
                    # 첫 번째(최신)를 제외하고 나머지 삭제
                    for file, date_str in files[1:]:
                        try:
                            file.unlink()
                            deleted_count += 1
                            self.log_message(f"🗑️ 삭제: {file.name}")
                        except:
                            pass
                            
            if deleted_count > 0:
                messagebox.showinfo("완료", f"{deleted_count}개의 오래된 파일을 정리했습니다.")
                self.refresh_file_list()
            else:
                messagebox.showinfo("정보", "정리할 파일이 없습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"파일 정리 실패: {e}")
            
    def open_data_folder(self):
        """데이터 폴더 열기"""
        try:
            data_folder = Path(self.config['data_folder'])
            data_folder.mkdir(exist_ok=True)
            
            import subprocess
            subprocess.run(['explorer', str(data_folder)], check=True)
        except Exception as e:
            messagebox.showerror("오류", f"폴더 열기 실패: {e}")
            
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("오류", f"애플리케이션 오류: {e}")

def main():
    """메인 함수"""
    try:
        print("🚀 VStock Advanced - 증분 업데이트 시스템")
        app = IncrementalStockDownloader()
        app.run()
    except Exception as e:
        print(f"프로그램 시작 실패: {e}")

if __name__ == "__main__":
    main()