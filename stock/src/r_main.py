#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VStock Advanced - R 연동 버전
R quantmod 스크립트와 완벽 연동하는 주식 분석 프로그램
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
from datetime import datetime
import sys

# R 데이터 로더 임포트
try:
    from src.r_data_loader import RIntegratedDataLoader
except ImportError:
    print("⚠️ R 데이터 로더를 찾을 수 없습니다. 기본 모드로 실행합니다.")
    RIntegratedDataLoader = None

class VStockAdvancedR:
    def __init__(self):
        """R 연동 주식 분석기 초기화"""
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.init_data_loader()
        self.current_data = None
        self.create_widgets()
        
    def setup_window(self):
        """윈도우 설정"""
        self.root.title("📈 VStock Advanced - R 연동 버전")
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
        
        # R 연동 기본 설정
        default_config = {
            "data_folder": "~/R_stats/R_stock/data",
            "r_integration": {
                "enabled": True,
                "auto_detect_r_files": True
            },
            "etf_symbols": [
                "TQQQ", "SOXL", "FNGU", "NAIL", "TECL", "LABU", 
                "RETL", "WEBL", "DPST", "TNA", "HIBL", "BNKU",
                "DFEN", "PILL", "MIDU", "WANT", "FAS", "TPOR"
            ],
            "default_symbols": [
                "TQQQ", "SOXL", "FNGU", "TNA", "AAPL", "TSLA", "NVDA", "PLTR"
            ]
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
                # 누락된 설정 병합
                for key, value in default_config.items():
                    if key not in self.config:
                        self.config[key] = value
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"설정 로드 실패: {e}")
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
            
    def init_data_loader(self):
        """데이터 로더 초기화"""
        try:
            if RIntegratedDataLoader:
                self.data_loader = RIntegratedDataLoader(self.config.get('data_folder'))
                self.r_enabled = True
            else:
                self.r_enabled = False
                print("⚠️ R 연동 비활성화 - 기본 모드로 동작")
                
        except Exception as e:
            print(f"데이터 로더 초기화 실패: {e}")
            self.r_enabled = False
            
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 헤더 생성
        self.create_header(main_frame)
        
        # 메인 콘텐츠
        self.create_main_content(main_frame)
        
        # 상태바
        self.create_statusbar(main_frame)
        
        # 초기 상태 확인
        self.check_r_status()
        
    def create_header(self, parent):
        """헤더 생성"""
        header_frame = ttk.LabelFrame(parent, text="📈 VStock Advanced - R 연동", padding="20")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 제목 영역
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X, pady=(0, 15))
        
        title_label = ttk.Label(title_frame, text="quantmod 연동 주식 분석 시스템", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(side=tk.LEFT)
        
        # R 상태 표시
        self.r_status_label = ttk.Label(title_frame, text="", 
                                       font=('Segoe UI', 10))
        self.r_status_label.pack(side=tk.RIGHT)
        
        # 검색 영역
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(fill=tk.X)
        
        # 종목 검색
        ttk.Label(search_frame, text="종목 코드:", font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol_var, 
                                     font=('Segoe UI', 12), width=12)
        self.symbol_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.symbol_entry.bind('<Return>', lambda e: self.analyze_stock())
        
        # 분석 버튼
        analyze_btn = ttk.Button(search_frame, text="🔍 분석", command=self.analyze_stock)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # R 종목 빠른 선택 (레버리지 ETF)
        quick_frame = ttk.LabelFrame(search_frame, text="🚀 레버리지 ETF", padding="5")
        quick_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        etf_row1 = ttk.Frame(quick_frame)
        etf_row1.pack(fill=tk.X)
        etf_row2 = ttk.Frame(quick_frame)
        etf_row2.pack(fill=tk.X)
        
        # 주요 레버리지 ETF들
        main_etfs = ["TQQQ", "SOXL", "FNGU", "TNA", "TECL"]
        other_etfs = ["LABU", "RETL", "WEBL", "NAIL", "DPST"]
        
        for symbol in main_etfs:
            btn = ttk.Button(etf_row1, text=symbol, width=7,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=1)
            
        for symbol in other_etfs:
            btn = ttk.Button(etf_row2, text=symbol, width=7,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=1)
        
        # 설정 버튼들
        settings_frame = ttk.Frame(search_frame)
        settings_frame.pack(side=tk.RIGHT)
        
        ttk.Button(settings_frame, text="📂 R 경로", 
                  command=self.select_r_path).pack(side=tk.LEFT, padx=2)
        ttk.Button(settings_frame, text="🔄 새로고침", 
                  command=self.refresh_r_data).pack(side=tk.LEFT, padx=2)
        ttk.Button(settings_frame, text="📊 종목목록", 
                  command=self.show_available_symbols).pack(side=tk.LEFT, padx=2)
        
    def create_main_content(self, parent):
        """메인 콘텐츠 생성"""
        content_frame = ttk.PanedWindow(parent, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (차트)
        self.left_panel = ttk.LabelFrame(content_frame, text="📊 차트 분석", padding="10")
        content_frame.add(self.left_panel, weight=3)
        
        # 오른쪽 패널 (정보)
        self.right_panel = ttk.LabelFrame(content_frame, text="📋 종목 정보", padding="10")
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
        
        # 시간 표시
        self.time_label = ttk.Label(status_frame, text="", 
                                   relief=tk.SUNKEN, anchor=tk.E)
        self.time_label.pack(side=tk.RIGHT)
        self.update_time()
        
    def show_initial_message(self):
        """초기 메시지"""
        welcome_text = """
🚀 R quantmod 연동 주식 분석 시스템

📊 지원 데이터:
• R 스크립트로 다운로드한 ETF 데이터
• 레버리지 ETF (TQQQ, SOXL, FNGU 등)
• 3년간 히스토리 데이터

🎯 사용법:
1. 종목 코드 입력 또는 빠른 선택 버튼 클릭
2. 🔍 분석 버튼으로 차트 및 지표 확인
3. R 스크립트 데이터 자동 연동

💡 팁: R에서 데이터 다운로드 후 자동으로 최신 파일 감지
        """
        
        welcome_label = ttk.Label(self.left_panel, text=welcome_text, 
                                 font=('Segoe UI', 11), justify=tk.CENTER)
        welcome_label.pack(expand=True)
        
    def create_info_panel(self):
        """정보 패널 생성"""
        # 노트북 탭
        self.info_notebook = ttk.Notebook(self.right_panel)
        self.info_notebook.pack(fill=tk.BOTH, expand=True)
        
        # 기본 정보 탭
        self.basic_info_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.basic_info_frame, text="📋 기본정보")
        
        # R 데이터 정보 탭
        self.r_info_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.r_info_frame, text="🔗 R 데이터")
        
        # 기본 정보 레이블들
        self.create_basic_info_labels()
        self.create_r_info_labels()
        
    def create_basic_info_labels(self):
        """기본 정보 레이블 생성"""
        self.info_labels = {}
        info_fields = [
            ("symbol", "종목 코드"),
            ("price", "현재가"),
            ("change", "전일 대비"),
            ("change_percent", "변동률"),
            ("volume", "거래량"),
            ("high", "고가"),
            ("low", "저가"),
            ("date_range", "데이터 기간"),
            ("total_days", "총 일수")
        ]
        
        for field, label_text in info_fields:
            frame = ttk.Frame(self.basic_info_frame)
            frame.pack(fill=tk.X, pady=3)
            
            ttk.Label(frame, text=f"{label_text}:", 
                     font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
            self.info_labels[field] = ttk.Label(frame, text="-", 
                                               font=('Segoe UI', 10))
            self.info_labels[field].pack(side=tk.RIGHT)
            
    def create_r_info_labels(self):
        """R 데이터 정보 레이블 생성"""
        # R 상태 정보
        self.r_info_text = tk.Text(self.r_info_frame, height=20, width=40, 
                                  font=('Consolas', 9), wrap=tk.WORD)
        
        scrollbar = ttk.Scrollbar(self.r_info_frame, orient=tk.VERTICAL, 
                                 command=self.r_info_text.yview)
        self.r_info_text.configure(yscrollcommand=scrollbar.set)
        
        self.r_info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
    def check_r_status(self):
        """R 상태 확인"""
        if self.r_enabled and hasattr(self, 'data_loader'):
            symbols = self.data_loader.get_available_r_symbols()
            status_text = f"🟢 R 연동 활성 ({len(symbols)}개 종목)"
            
            # R 정보 표시
            r_info = f"""🔗 R quantmod 연동 상태

📁 데이터 경로: {self.data_loader.active_r_path}

📊 사용 가능한 종목 ({len(symbols)}개):
{chr(10).join(f"• {symbol}" for symbol in symbols)}

💾 데이터 소스: R quantmod 스크립트
🕐 마지막 확인: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

💡 R 스크립트에서 새 데이터를 다운로드한 후
   '🔄 새로고침' 버튼을 눌러주세요.
"""
            
        else:
            status_text = "🔴 R 연동 비활성"
            r_info = """❌ R 연동이 비활성화되었습니다.

가능한 원인:
• R 데이터 경로를 찾을 수 없음
• 필요한 모듈 누락
• 권한 문제

해결방법:
1. R 스크립트 실행 확인
2. '📂 R 경로' 버튼으로 경로 설정
3. 프로그램 재시작
"""
        
        self.r_status_label.config(text=status_text)
        self.r_info_text.delete(1.0, tk.END)
        self.r_info_text.insert(1.0, r_info)
        
    def quick_analyze(self, symbol):
        """빠른 분석"""
        self.symbol_var.set(symbol)
        self.analyze_stock()
        
    def analyze_stock(self):
        """주식 분석 실행"""
        symbol = self.symbol_var.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력해주세요.")
            return
            
        self.status_label.config(text=f"{symbol} 분석 중...")
        self.root.update()
        
        try:
            # R 데이터 로드
            if self.r_enabled:
                data = self.data_loader.load_stock_data(symbol)
                data_info = self.data_loader.get_data_info(symbol) if data is not None else None
            else:
                data = None
                data_info = None
                
            if data is None or data.empty:
                messagebox.showerror("오류", 
                    f"{symbol} 데이터를 찾을 수 없습니다.\n\n"
                    f"• R 스크립트에서 해당 종목을 다운로드했는지 확인\n"
                    f"• '📊 종목목록' 버튼으로 사용 가능한 종목 확인\n"
                    f"• 파일명이 '{symbol}_YYMMDD.csv' 형식인지 확인")
                self.status_label.config(text="분석 실패")
                return
                
            self.current_data = data
            
            # 차트 생성
            self.create_advanced_chart(symbol, data)
            
            # 정보 업데이트
            self.update_stock_info(symbol, data, data_info)
            
            self.status_label.config(text=f"{symbol} 분석 완료 - {len(data)}일 데이터")
            
        except Exception as e:
            messagebox.showerror("오류", f"분석 중 오류 발생:\n{e}")
            self.status_label.config(text="분석 실패")
            print(f"분석 오류: {e}")
            
    def create_advanced_chart(self, symbol, data):
        """고급 차트 생성"""
        # 기존 위젯 제거
        for widget in self.left_panel.winfo_children():
            widget.destroy()
            
        # Figure 생성
        fig = Figure(figsize=(12, 8), facecolor='white')
        
        # 서브플롯 생성
        ax1 = fig.add_subplot(3, 1, 1)  # 가격 차트
        ax2 = fig.add_subplot(3, 1, 2)  # 거래량
        ax3 = fig.add_subplot(3, 1, 3)  # RSI
        
        # 가격 차트 (캔들스틱 스타일)
        self.plot_candlestick_style(ax1, data, symbol)
        
        # 거래량 차트
        self.plot_volume_chart(ax2, data)
        
        # RSI 차트
        self.plot_rsi_chart(ax3, data)
        
        # 레이아웃 조정
        fig.tight_layout()
        
        # Canvas 생성
        canvas = FigureCanvasTkAgg(fig, self.left_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # 네비게이션 툴바
        toolbar_frame = ttk.Frame(self.left_panel)
        toolbar_frame.pack(fill=tk.X)
        # NavigationToolbar2Tk는 여기서는 생략 (선택사항)
        
    def plot_candlestick_style(self, ax, data, symbol):
        """캔들스틱 스타일 가격 차트"""
        # 종가 라인
        ax.plot(data.index, data['Close'], color='#2563eb', linewidth=2, label='종가')
        
        # 이동평균선들
        if len(data) > 20:
            ma20 = data['Close'].rolling(window=20).mean()
            ax.plot(data.index, ma20, color='#f59e0b', linewidth=1.5, 
                   label='MA20', alpha=0.8)
            
        if len(data) > 50:
            ma50 = data['Close'].rolling(window=50).mean()
            ax.plot(data.index, ma50, color='#ef4444', linewidth=1.5, 
                   label='MA50', alpha=0.8)
            
        # 고가/저가 영역 표시
        ax.fill_between(data.index, data['High'], data['Low'], 
                       alpha=0.1, color='gray', label='고가-저가 범위')
        
        ax.set_title(f'{symbol} - 가격 차트 (R quantmod 데이터)', 
                    fontsize=14, fontweight='bold')
        ax.set_ylabel('가격 ($)', fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.legend()
        
    def plot_volume_chart(self, ax, data):
        """거래량 차트"""
        # 가격 변동에 따른 색상
        colors = ['#16a34a' if close >= open_price else '#ef4444' 
                 for close, open_price in zip(data['Close'], data['Open'])]
        
        ax.bar(data.index, data['Volume'], color=colors, alpha=0.6, width=1)
        ax.set_title('거래량', fontsize=12)
        ax.set_ylabel('거래량', fontsize=10)
        ax.grid(True, alpha=0.3)
        
        # 거래량 이동평균
        if len(data) > 20:
            vol_ma = data['Volume'].rolling(window=20).mean()
            ax.plot(data.index, vol_ma, color='purple', linewidth=1, 
                   label='거래량 MA20', alpha=0.8)
            ax.legend()
            
    def plot_rsi_chart(self, ax, data):
        """RSI 차트"""
        try:
            # 간단한 RSI 계산
            close = data['Close']
            delta = close.diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            window = 14
            avg_gain = gain.rolling(window=window).mean()
            avg_loss = loss.rolling(window=window).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            # RSI 플롯
            ax.plot(data.index, rsi, color='#8b5cf6', linewidth=2, label='RSI(14)')
            
            # 과매수/과매도 라인
            ax.axhline(y=70, color='#ef4444', linestyle='--', alpha=0.7, label='과매수')
            ax.axhline(y=30, color='#16a34a', linestyle='--', alpha=0.7, label='과매도')
            ax.axhline(y=50, color='#64748b', linestyle='-', alpha=0.5)
            
            # 음영
            ax.fill_between(data.index, 70, 100, alpha=0.1, color='red')
            ax.fill_between(data.index, 0, 30, alpha=0.1, color='green')
            
            ax.set_title('RSI (Relative Strength Index)', fontsize=12)
            ax.set_ylabel('RSI', fontsize=10)
            ax.set_ylim(0, 100)
            ax.grid(True, alpha=0.3)
            ax.legend()
            
        except Exception as e:
            ax.text(0.5, 0.5, f'RSI 계산 오류: {e}', 
                   transform=ax.transAxes, ha='center', va='center')
            
    def update_stock_info(self, symbol, data, data_info=None):
        """종목 정보 업데이트"""
        try:
            if data.empty:
                return
                
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100
            
            # 기본 정보 업데이트
            info_data = {
                'symbol': symbol,
                'price': f"${latest['Close']:.2f}",
                'change': f"${change:+.2f}",
                'change_percent': f"{change_percent:+.2f}%",
                'volume': f"{latest['Volume']:,}",
                'high': f"${latest['High']:.2f}",
                'low': f"${latest['Low']:.2f}",
                'date_range': f"{data.index.min().date()} ~ {data.index.max().date()}",
                'total_days': f"{len(data)}일"
            }
            
            for field, value in info_data.items():
                if field in self.info_labels:
                    self.info_labels[field].config(text=value)
                    
            # 변동률 색상
            color = 'green' if change >= 0 else 'red'
            self.info_labels['change'].config(foreground=color)
            self.info_labels['change_percent'].config(foreground=color)
            
            # R 데이터 정보 업데이트
            if data_info:
                r_detail = f"""📊 {symbol} 상세 정보

📁 데이터 소스: {data_info.get('data_source', 'Unknown')}
📅 기간: {data_info['start_date']} ~ {data_info['end_date']}
📈 총 일수: {data_info['total_days']}일

💰 가격 정보:
• 현재가: ${data_info['latest_price']:.2f}
• 최고가: ${data_info['price_range']['max']:.2f}
• 최저가: ${data_info['price_range']['min']:.2f}
• 평균 거래량: {data_info['avg_volume']:,}

📂 파일 정보:
"""
                
                if 'files' in data_info:
                    for file_info in data_info['files']:
                        r_detail += f"• {file_info['name']} ({file_info['size']}) - {file_info['modified']}\n"
                
                r_detail += f"\n🕐 분석 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
                
                self.r_info_text.delete(1.0, tk.END)
                self.r_info_text.insert(1.0, r_detail)
                
        except Exception as e:
            print(f"정보 업데이트 오류: {e}")
            
    def select_r_path(self):
        """R 경로 선택"""
        folder = filedialog.askdirectory(
            title="R 데이터 폴더 선택",
            initialdir=str(Path("~/R_stats/R_stock/data").expanduser())
        )
        if folder:
            self.config['data_folder'] = folder
            self.save_config()
            
            # 데이터 로더 재초기화
            self.init_data_loader()
            self.check_r_status()
            
            messagebox.showinfo("성공", f"R 데이터 경로가 설정되었습니다:\n{folder}")
            
    def refresh_r_data(self):
        """R 데이터 새로고침"""
        self.status_label.config(text="R 데이터 새로고침 중...")
        self.root.update()
        
        try:
            # 캐시 클리어
            if hasattr(self, 'data_loader') and self.data_loader:
                self.data_loader.cache.clear()
                
            # 상태 재확인
            self.check_r_status()
            
            self.status_label.config(text="R 데이터 새로고침 완료")
            messagebox.showinfo("완료", "R 데이터가 새로고침되었습니다.")
            
        except Exception as e:
            self.status_label.config(text="새로고침 실패")
            messagebox.showerror("오류", f"새로고침 실패:\n{e}")
            
    def show_available_symbols(self):
        """사용 가능한 종목 목록 표시"""
        try:
            if self.r_enabled and hasattr(self, 'data_loader'):
                symbols = self.data_loader.get_available_r_symbols()
                
                # 새 창 생성
                symbols_window = tk.Toplevel(self.root)
                symbols_window.title("📊 사용 가능한 종목 목록")
                symbols_window.geometry("600x500")
                
                # 텍스트 위젯
                text_widget = tk.Text(symbols_window, font=('Consolas', 11), wrap=tk.WORD)
                scrollbar = ttk.Scrollbar(symbols_window, orient=tk.VERTICAL, command=text_widget.yview)
                text_widget.configure(yscrollcommand=scrollbar.set)
                
                # 종목 목록 표시
                content = f"""📊 R quantmod 데이터 종목 목록

🔗 데이터 경로: {self.data_loader.active_r_path}
📅 확인 시각: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 사용 가능한 종목 ({len(symbols)}개):

"""
                
                # 종목을 그룹별로 정리
                etf_symbols = [s for s in symbols if s in self.config.get('etf_symbols', [])]
                other_symbols = [s for s in symbols if s not in etf_symbols]
                
                if etf_symbols:
                    content += "🚀 레버리지 ETF:\n"
                    for i, symbol in enumerate(etf_symbols):
                        content += f"  {symbol:<8}"
                        if (i + 1) % 6 == 0:
                            content += "\n"
                    content += "\n\n"
                    
                if other_symbols:
                    content += "📊 기타 종목:\n"
                    for i, symbol in enumerate(other_symbols):
                        content += f"  {symbol:<8}"
                        if (i + 1) % 6 == 0:
                            content += "\n"
                    content += "\n\n"
                
                content += """💡 사용법:
• 종목 코드를 복사하여 메인 화면에서 분석
• 빠른 선택 버튼 활용
• R 스크립트에서 새 종목 다운로드 후 '🔄 새로고침' 클릭
"""
                
                text_widget.insert(1.0, content)
                text_widget.config(state=tk.DISABLED)
                
                text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
                
            else:
                messagebox.showwarning("경고", "R 연동이 비활성화되어 있습니다.")
                
        except Exception as e:
            messagebox.showerror("오류", f"종목 목록을 가져올 수 없습니다:\n{e}")
            
    def update_time(self):
        """시간 업데이트"""
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.time_label.config(text=current_time)
        self.root.after(1000, self.update_time)
        
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except KeyboardInterrupt:
            self.root.quit()
        except Exception as e:
            print(f"애플리케이션 실행 오류: {e}")
            messagebox.showerror("오류", f"애플리케이션 오류: {e}")

def main():
    """메인 함수"""
    try:
        print("🚀 VStock Advanced - R 연동 버전 시작...")
        app = VStockAdvancedR()
        app.run()
    except Exception as e:
        print(f"프로그램 시작 실패: {e}")
        messagebox.showerror("오류", f"프로그램 시작 실패: {e}")

if __name__ == "__main__":
    main()