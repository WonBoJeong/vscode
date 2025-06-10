#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VStock Advanced - 실시간 다운로드 통합 버전
R 의존성 없이 Python만으로 모든 기능 구현
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

class VStockWithDownloader:
    def __init__(self):
        """실시간 다운로드 기능이 통합된 VStock"""
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.current_data = None
        self.download_queue = queue.Queue()
        self.create_widgets()
        
    def setup_window(self):
        """윈도우 설정"""
        self.root.title("📈 VStock Advanced - 실시간 다운로드 통합")
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
            "auto_download": True,
            "download_period": "3y",
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
                # 누락 설정 병합
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
        header_frame = ttk.LabelFrame(parent, text="📈 VStock Advanced - 실시간 다운로드", padding="20")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 제목 영역
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="Python 실시간 데이터 수집 & 분석", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # 다운로드 상태
        self.download_status = ttk.Label(title_frame, text="", font=('Segoe UI', 10))
        self.download_status.pack(side=tk.RIGHT)
        
        # 검색 및 다운로드 영역
        control_frame = ttk.Frame(header_frame)
        control_frame.pack(fill=tk.X)
        
        # 종목 입력
        input_frame = ttk.LabelFrame(control_frame, text="📍 종목 분석/다운로드", padding="10")
        input_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        entry_frame = ttk.Frame(input_frame)
        entry_frame.pack(fill=tk.X)
        
        ttk.Label(entry_frame, text="종목:", font=('Segoe UI', 11)).pack(side=tk.LEFT)
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(entry_frame, textvariable=self.symbol_var, 
                                     font=('Segoe UI', 11), width=10)
        self.symbol_entry.pack(side=tk.LEFT, padx=(5, 5))
        self.symbol_entry.bind('<Return>', lambda e: self.analyze_or_download())
        
        # 버튼들
        btn_frame = ttk.Frame(entry_frame)
        btn_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        ttk.Button(btn_frame, text="🔍 분석", command=self.analyze_only).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📥 다운로드", command=self.download_only).pack(side=tk.LEFT, padx=2)
        ttk.Button(btn_frame, text="📊 분석+다운", command=self.analyze_or_download).pack(side=tk.LEFT, padx=2)
        
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
            
        # 일괄 다운로드 영역
        batch_frame = ttk.LabelFrame(control_frame, text="📦 일괄 다운로드", padding="10")
        batch_frame.pack(side=tk.RIGHT)
        
        ttk.Button(batch_frame, text="🚀 레버리지ETF", 
                  command=self.download_leverage_etfs).pack(pady=2)
        ttk.Button(batch_frame, text="📈 인기종목", 
                  command=self.download_popular_stocks).pack(pady=2)
        ttk.Button(batch_frame, text="🌟 전체", 
                  command=self.download_all).pack(pady=2)
        
    def create_main_content(self, parent):
        """메인 콘텐츠 생성"""
        content_frame = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (차트)
        self.left_panel = ttk.LabelFrame(content_frame, text="📊 차트 분석", padding="10")
        content_frame.add(self.left_panel, weight=3)
        
        # 오른쪽 패널 (정보)
        self.right_panel = ttk.LabelFrame(content_frame, text="📋 정보 & 다운로드", padding="10")
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
🚀 Python 실시간 주식 데이터 다운로드 & 분석

✨ 주요 기능:
• 📥 Yahoo Finance에서 실시간 데이터 다운로드
• 📊 즉시 차트 분석 (캔들스틱, RSI, 이동평균)
• 🚀 레버리지 ETF 전문 지원
• 📈 인기 종목 일괄 다운로드

🎯 사용법:
1. 종목 코드 입력 후 "📊 분석+다운" 클릭
2. 또는 빠른 선택 버튼 활용
3. 일괄 다운로드로 여러 종목 한번에 수집

💡 장점:
• R 설치 불필요
• 즉시 최신 데이터 수집
• 자동 파일 저장
            """
        else:
            welcome_text = """
⚠️ yfinance 라이브러리가 필요합니다

📦 설치 방법:
pip install yfinance

🔧 설치 후:
• 프로그램 재시작
• 실시간 데이터 다운로드 가능
• Yahoo Finance 연동

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
        
        # 다운로드 로그 탭
        self.download_log_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.download_log_frame, text="📥 다운로드")
        
        # 파일 목록 탭
        self.files_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.files_frame, text="📁 파일목록")
        
        self.create_stock_info_tab()
        self.create_download_log_tab()
        self.create_files_tab()
        
    def create_stock_info_tab(self):
        """종목 정보 탭"""
        self.info_labels = {}
        info_fields = [
            ("symbol", "종목 코드"),
            ("name", "회사명"),
            ("price", "현재가"),
            ("change", "전일대비"),
            ("change_percent", "변동률"),
            ("volume", "거래량"),
            ("market_cap", "시가총액"),
            ("pe_ratio", "PER"),
            ("data_period", "데이터 기간"),
            ("last_update", "마지막 업데이트")
        ]
        
        for field, label_text in info_fields:
            frame = ttk.Frame(self.stock_info_frame)
            frame.pack(fill=tk.X, pady=3)
            
            ttk.Label(frame, text=f"{label_text}:", 
                     font=('Segoe UI', 9, 'bold')).pack(side=tk.LEFT)
            self.info_labels[field] = ttk.Label(frame, text="-", 
                                               font=('Segoe UI', 9))
            self.info_labels[field].pack(side=tk.RIGHT)
            
    def create_download_log_tab(self):
        """다운로드 로그 탭"""
        # 다운로드 진행률
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(self.download_log_frame, 
                                           variable=self.progress_var, 
                                           maximum=100)
        self.progress_bar.pack(fill=tk.X, padx=10, pady=10)
        
        # 로그 텍스트
        self.log_text = tk.Text(self.download_log_frame, height=20, 
                               font=('Consolas', 9), wrap=tk.WORD)
        
        log_scrollbar = ttk.Scrollbar(self.download_log_frame, 
                                     orient=tk.VERTICAL, 
                                     command=self.log_text.yview)
        self.log_text.configure(yscrollcommand=log_scrollbar.set)
        
        self.log_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        log_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def create_files_tab(self):
        """파일 목록 탭"""
        # 새로고침 버튼
        refresh_btn = ttk.Button(self.files_frame, text="🔄 새로고침", 
                                command=self.refresh_file_list)
        refresh_btn.pack(pady=5)
        
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
        
    def download_stock_data(self, symbol, period="3y"):
        """단일 종목 다운로드"""
        if not YFINANCE_AVAILABLE:
            self.log_message(f"❌ yfinance 없음 - {symbol} 다운로드 불가")
            return None
            
        try:
            self.log_message(f"📊 {symbol} 다운로드 시작...")
            
            # yfinance로 데이터 및 정보 다운로드
            ticker = yf.Ticker(symbol)
            
            # 가격 데이터
            data = ticker.history(period=period)
            if data.empty:
                self.log_message(f"❌ {symbol}: 데이터 없음")
                return None
                
            # 기본 정보
            try:
                info = ticker.info
            except:
                info = {}
                
            # 파일 저장
            data_folder = Path(self.config['data_folder'])
            data_folder.mkdir(exist_ok=True)
            
            date_key = datetime.now().strftime("%y%m%d")
            filename = data_folder / f"{symbol}_{date_key}.csv"
            
            # 컬럼 정리해서 저장
            save_data = data.copy()
            save_data.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
            save_data.index.name = 'Date'
            save_data.to_csv(filename)
            
            self.log_message(f"✅ {symbol}: {len(data)}일 데이터 저장 → {filename.name}")
            
            return {
                'data': data,
                'info': info,
                'filename': filename
            }
            
        except Exception as e:
            self.log_message(f"❌ {symbol} 다운로드 실패: {e}")
            return None
            
    def download_multiple_stocks(self, symbols, period="3y"):
        """다중 종목 다운로드 (백그라운드)"""
        if not YFINANCE_AVAILABLE:
            messagebox.showwarning("경고", "yfinance가 설치되지 않았습니다.\npip install yfinance")
            return
            
        def download_thread():
            total = len(symbols)
            success_count = 0
            
            self.log_message(f"🚀 {total}개 종목 일괄 다운로드 시작")
            
            for i, symbol in enumerate(symbols):
                # 진행률 업데이트
                progress = (i / total) * 100
                self.progress_var.set(progress)
                
                # 다운로드 실행
                result = self.download_stock_data(symbol, period)
                if result:
                    success_count += 1
                    
                # API 제한 방지
                if i < total - 1:
                    time.sleep(0.5)
                    
            # 완료
            self.progress_var.set(100)
            self.log_message(f"🎉 일괄 다운로드 완료! 성공: {success_count}/{total}")
            
            # 파일 목록 새로고침
            self.root.after(100, self.refresh_file_list)
            
        # 백그라운드 스레드로 실행
        thread = threading.Thread(target=download_thread)
        thread.daemon = True
        thread.start()
        
    def load_stock_data(self, symbol):
        """파일에서 주식 데이터 로드"""
        try:
            data_folder = Path(self.config['data_folder'])
            
            # 파일 찾기 (최신순)
            patterns = [
                f"{symbol}_*.csv",
                f"{symbol}.csv",
                f"{symbol}_data.csv"
            ]
            
            files = []
            for pattern in patterns:
                files.extend(list(data_folder.glob(pattern)))
                
            if not files:
                return None
                
            # 최신 파일 선택
            latest_file = max(files, key=lambda f: f.stat().st_mtime)
            
            # 데이터 로드
            data = pd.read_csv(latest_file, index_col=0, parse_dates=True)
            
            # 컬럼명 정규화
            if 'date' in data.columns.str.lower():
                data.set_index('date', inplace=True)
                
            return data
            
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            return None
            
    def quick_analyze(self, symbol):
        """빠른 분석"""
        self.symbol_var.set(symbol)
        self.analyze_or_download()
        
    def analyze_only(self):
        """분석만 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        data = self.load_stock_data(symbol)
        if data is None:
            messagebox.showwarning("경고", f"{symbol} 데이터가 없습니다.\n'📥 다운로드' 버튼을 먼저 눌러주세요.")
            return
            
        self.analyze_stock(symbol, data)
        
    def download_only(self):
        """다운로드만 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        self.download_stock_data(symbol)
        self.refresh_file_list()
        
    def analyze_or_download(self):
        """분석 또는 다운로드 후 분석"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력하세요.")
            return
            
        # 기존 데이터 확인
        data = self.load_stock_data(symbol)
        
        if data is None and YFINANCE_AVAILABLE:
            # 데이터가 없으면 다운로드
            result = self.download_stock_data(symbol)
            if result:
                data = result['data']
                self.refresh_file_list()
        elif data is None:
            messagebox.showwarning("경고", 
                f"{symbol} 데이터가 없고 yfinance도 사용할 수 없습니다.\n"
                "pip install yfinance로 설치하거나 수동으로 데이터 파일을 추가하세요.")
            return
            
        if data is not None:
            self.analyze_stock(symbol, data)
            
    def analyze_stock(self, symbol, data, stock_info=None):
        """주식 분석 실행"""
        try:
            self.status_label.config(text=f"{symbol} 분석 중...")
            self.current_data = data
            
            # 차트 생성
            self.create_analysis_chart(symbol, data)
            
            # 정보 업데이트
            self.update_stock_info(symbol, data, stock_info)
            
            self.status_label.config(text=f"{symbol} 분석 완료")
            
        except Exception as e:
            messagebox.showerror("오류", f"분석 실패: {e}")
            self.status_label.config(text="분석 실패")
            
    def create_analysis_chart(self, symbol, data):
        """분석 차트 생성"""
        # 기존 위젯 제거
        for widget in self.left_panel.winfo_children():
            widget.destroy()
            
        # Figure 생성
        fig = Figure(figsize=(12, 8), facecolor='white')
        
        # 서브플롯
        ax1 = fig.add_subplot(3, 1, 1)
        ax2 = fig.add_subplot(3, 1, 2)
        ax3 = fig.add_subplot(3, 1, 3)
        
        # 가격 차트
        ax1.plot(data.index, data['Close'], 'b-', linewidth=2, label='종가')
        
        # 이동평균
        if len(data) > 20:
            ma20 = data['Close'].rolling(20).mean()
            ax1.plot(data.index, ma20, 'orange', linewidth=1.5, label='MA20')
        if len(data) > 50:
            ma50 = data['Close'].rolling(50).mean()
            ax1.plot(data.index, ma50, 'red', linewidth=1.5, label='MA50')
            
        ax1.set_title(f'{symbol} - 가격 차트', fontsize=14, fontweight='bold')
        ax1.set_ylabel('가격 ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 거래량
        colors = ['g' if c >= o else 'r' for c, o in zip(data['Close'], data['Open'])]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.6)
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
            ax3.axhline(70, color='r', linestyle='--', alpha=0.7, label='과매수')
            ax3.axhline(30, color='g', linestyle='--', alpha=0.7, label='과매도')
            ax3.fill_between(data.index, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(data.index, 0, 30, alpha=0.1, color='green')
            
            ax3.set_title('RSI')
            ax3.set_ylabel('RSI')
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            
        except:
            ax3.text(0.5, 0.5, 'RSI 계산 오류', transform=ax3.transAxes, ha='center')
            
        fig.tight_layout()
        
        # Canvas
        canvas = FigureCanvasTkAgg(fig, self.left_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_stock_info(self, symbol, data, stock_info=None):
        """종목 정보 업데이트"""
        try:
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100
            
            # 기본 정보
            info_updates = {
                'symbol': symbol,
                'price': f"${latest['Close']:.2f}",
                'change': f"${change:+.2f}",
                'change_percent': f"{change_percent:+.2f}%",
                'volume': f"{latest['Volume']:,}",
                'data_period': f"{data.index.min().date()} ~ {data.index.max().date()}",
                'last_update': datetime.now().strftime("%Y-%m-%d %H:%M")
            }
            
            # yfinance 정보가 있으면 추가
            if stock_info:
                info_updates.update({
                    'name': stock_info.get('longName', stock_info.get('shortName', '-')),
                    'market_cap': f"${stock_info.get('marketCap', 0):,}" if stock_info.get('marketCap') else '-',
                    'pe_ratio': f"{stock_info.get('forwardPE', 0):.2f}" if stock_info.get('forwardPE') else '-'
                })
            
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
            
    def download_leverage_etfs(self):
        """레버리지 ETF 일괄 다운로드"""
        self.download_multiple_stocks(self.config['etf_symbols'])
        
    def download_popular_stocks(self):
        """인기 종목 일괄 다운로드"""
        self.download_multiple_stocks(self.config['popular_symbols'])
        
    def download_all(self):
        """전체 종목 일괄 다운로드"""
        all_symbols = self.config['etf_symbols'] + self.config['popular_symbols']
        self.download_multiple_stocks(all_symbols)
        
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
                
            # 파일 정보 표시
            for file in sorted(csv_files, key=lambda f: f.stat().st_mtime, reverse=True):
                stat = file.stat()
                size_kb = stat.st_size / 1024
                mod_time = datetime.fromtimestamp(stat.st_mtime).strftime("%m/%d %H:%M")
                
                info = f"{file.stem:<15} {size_kb:>6.1f}KB {mod_time}"
                self.file_listbox.insert(tk.END, info)
                
        except Exception as e:
            self.file_listbox.insert(tk.END, f"오류: {e}")
            
    def on_file_double_click(self, event):
        """파일 더블클릭 처리"""
        selection = self.file_listbox.curselection()
        if not selection:
            return
            
        file_info = self.file_listbox.get(selection[0])
        if not file_info or "📁" in file_info or "📄" in file_info:
            return
            
        # 파일명에서 심볼 추출
        symbol = file_info.split()[0]
        if "_" in symbol:
            symbol = symbol.split("_")[0]
            
        self.symbol_var.set(symbol)
        self.analyze_only()
        
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except Exception as e:
            messagebox.showerror("오류", f"애플리케이션 오류: {e}")

def main():
    """메인 함수"""
    try:
        print("🚀 VStock Advanced - 실시간 다운로드 통합 버전")
        app = VStockWithDownloader()
        app.run()
    except Exception as e:
        print(f"프로그램 시작 실패: {e}")

if __name__ == "__main__":
    main()