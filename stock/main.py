#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VStock Advanced - 주식 분석 프로그램
Design inspired by advanced.html
Author: AI Assistant
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import pandas as pd
import numpy as np
import json
import os
from datetime import datetime, timedelta
import sys
from pathlib import Path

# 현재 디렉토리를 Python 경로에 추가
current_dir = Path(__file__).parent
sys.path.append(str(current_dir))

# 로컬 모듈 임포트
try:
    from src.data_loader import DataLoader
    from src.technical_analysis import TechnicalAnalysis
    from src.portfolio_manager import PortfolioManager
    from src.chart_widget import ChartWidget
    from src.gui_components import ModernComponents
except ImportError:
    print("⚠️ 필요한 모듈을 찾을 수 없습니다. 모든 파일이 있는지 확인해주세요.")

class VStockAdvanced:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.load_config()
        self.setup_variables()
        self.setup_style()
        self.create_widgets()
        self.init_components()
        
    def setup_window(self):
        """윈도우 기본 설정"""
        self.root.title("📈 VStock Advanced - 고급 주식 분석 시스템")
        self.root.geometry("1600x900")
        self.root.minsize(1200, 700)
        
        # 아이콘 설정 (선택사항)
        try:
            self.root.iconbitmap("icon.ico")
        except:
            pass
            
        # 윈도우 중앙 배치
        self.center_window()
        
    def center_window(self):
        """윈도우를 화면 중앙에 배치"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def load_config(self):
        """설정 파일 로드"""
        config_path = Path("config/config.json")
        default_config = {
            "data_folder": "D:/vscode/stock/data",
            "theme": "modern",
            "auto_refresh": True,
            "refresh_interval": 60,
            "default_symbols": ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "PLTR"],
            "portfolio_symbols": ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"]
        }
        
        try:
            if config_path.exists():
                with open(config_path, 'r', encoding='utf-8') as f:
                    self.config = json.load(f)
            else:
                self.config = default_config
                self.save_config()
        except Exception as e:
            print(f"설정 로드 실패: {e}")
            self.config = default_config
            
    def save_config(self):
        """설정 파일 저장"""
        config_path = Path("config/config.json")
        config_path.parent.mkdir(exist_ok=True)
        
        try:
            with open(config_path, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"설정 저장 실패: {e}")
            
    def setup_variables(self):
        """변수 초기화"""
        self.current_symbol = tk.StringVar(value="")
        self.current_data = None
        self.charts = {}
        self.selected_symbols = []
        
    def setup_style(self):
        """테마 및 스타일 설정"""
        style = ttk.Style()
        
        # 테마 설정
        available_themes = style.theme_names()
        if 'clam' in available_themes:
            style.theme_use('clam')
        elif 'vista' in available_themes:
            style.theme_use('vista')
        else:
            style.theme_use('default')
            
        # 커스텀 스타일 정의
        self.colors = {
            'primary': '#667eea',
            'secondary': '#764ba2', 
            'success': '#4facfe',
            'warning': '#fa709a',
            'background': '#f8fafc',
            'surface': '#ffffff',
            'text_primary': '#2d3748',
            'text_secondary': '#718096',
            'positive': '#16a34a',
            'negative': '#dc2626'
        }
        
        # 스타일 구성
        style.configure('Custom.TFrame', background=self.colors['background'])
        style.configure('Card.TFrame', background=self.colors['surface'], relief='flat', borderwidth=1)
        style.configure('Header.TLabel', font=('Segoe UI', 24, 'bold'), background=self.colors['surface'])
        style.configure('Title.TLabel', font=('Segoe UI', 14, 'bold'), foreground=self.colors['text_primary'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 10), foreground=self.colors['text_secondary'])
        
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 컨테이너
        self.main_frame = ttk.Frame(self.root, style='Custom.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 헤더 생성
        self.create_header()
        
        # 메인 콘텐츠 생성
        self.create_main_content()
        
        # 상태바 생성
        self.create_statusbar()
        
    def create_header(self):
        """헤더 영역 생성"""
        header_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 타이틀
        title_frame = ttk.Frame(header_frame)
        title_frame.pack(fill=tk.X, padx=20, pady=20)
        
        title_label = ttk.Label(title_frame, text="📈 VStock Advanced", style='Header.TLabel')
        title_label.pack(side=tk.LEFT)
        
        subtitle_label = ttk.Label(title_frame, text="차세대 AI 기반 주식 분석 & 포트폴리오 관리 시스템", style='Subtitle.TLabel')
        subtitle_label.pack(side=tk.LEFT, padx=(20, 0))
        
        # 검색 및 제어 영역
        control_frame = ttk.Frame(header_frame)
        control_frame.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # 종목 검색
        search_frame = ttk.LabelFrame(control_frame, text="📍 종목 분석", padding=10)
        search_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.current_symbol, font=('Segoe UI', 12))
        self.symbol_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        self.symbol_entry.bind('<Return>', self.on_analyze_symbol)
        
        analyze_btn = ttk.Button(search_frame, text="🔍 분석", command=self.on_analyze_symbol)
        analyze_btn.pack(side=tk.LEFT, padx=(0, 5))
        
        # 빠른 선택 버튼들
        quick_frame = ttk.Frame(search_frame)
        quick_frame.pack(side=tk.LEFT, padx=(10, 0))
        
        for symbol in ["AAPL", "TSLA", "NVDA", "PLTR"]:
            btn = ttk.Button(quick_frame, text=symbol, width=6,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 설정 버튼들
        settings_frame = ttk.LabelFrame(control_frame, text="⚙️ 설정", padding=10)
        settings_frame.pack(side=tk.RIGHT)
        
        ttk.Button(settings_frame, text="📂 데이터 폴더", command=self.select_data_folder).pack(side=tk.LEFT, padx=2)
        ttk.Button(settings_frame, text="💼 포트폴리오", command=self.show_portfolio).pack(side=tk.LEFT, padx=2)
        ttk.Button(settings_frame, text="⚙️ 설정", command=self.show_settings).pack(side=tk.LEFT, padx=2)
        
    def create_main_content(self):
        """메인 콘텐츠 영역 생성"""
        # 메인 패널 분할
        paned_window = ttk.PanedWindow(self.main_frame, orient=tk.HORIZONTAL)
        paned_window.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (차트 영역)
        self.left_panel = ttk.Frame(paned_window, style='Card.TFrame')
        paned_window.add(self.left_panel, weight=3)
        
        # 오른쪽 패널 (정보 영역)
        self.right_panel = ttk.Frame(paned_window, style='Card.TFrame')
        paned_window.add(self.right_panel, weight=1)
        
        # 왼쪽 패널 구성
        self.create_chart_area()
        
        # 오른쪽 패널 구성
        self.create_info_area()
        
    def create_chart_area(self):
        """차트 영역 생성"""
        # 차트 탭 노트북
        self.chart_notebook = ttk.Notebook(self.left_panel)
        self.chart_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 기본 차트 탭
        self.basic_chart_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(self.basic_chart_frame, text="📊 기본 차트")
        
        # 기술적 분석 탭
        self.technical_chart_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(self.technical_chart_frame, text="📈 기술적 분석")
        
        # 비교 분석 탭
        self.compare_chart_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(self.compare_chart_frame, text="🔄 비교 분석")
        
        # 포트폴리오 분석 탭
        self.portfolio_chart_frame = ttk.Frame(self.chart_notebook)
        self.chart_notebook.add(self.portfolio_chart_frame, text="💼 포트폴리오")
        
        # 각 탭에 대한 초기 메시지
        self.create_chart_placeholders()
        
    def create_chart_placeholders(self):
        """차트 플레이스홀더 생성"""
        for frame, message in [
            (self.basic_chart_frame, "종목을 선택하면 기본 차트가 표시됩니다."),
            (self.technical_chart_frame, "기술적 분석 차트가 여기에 표시됩니다."),
            (self.compare_chart_frame, "여러 종목 비교 차트가 표시됩니다."),
            (self.portfolio_chart_frame, "포트폴리오 분석 결과가 표시됩니다.")
        ]:
            placeholder = ttk.Label(frame, text=message, font=('Segoe UI', 14))
            placeholder.pack(expand=True)
            
    def create_info_area(self):
        """정보 영역 생성"""
        # 정보 탭 노트북
        self.info_notebook = ttk.Notebook(self.right_panel)
        self.info_notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 종목 정보 탭
        self.stock_info_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.stock_info_frame, text="📋 종목 정보")
        
        # 기술적 지표 탭  
        self.indicators_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.indicators_frame, text="📊 기술 지표")
        
        # 관심종목 탭
        self.watchlist_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.watchlist_frame, text="⭐ 관심종목")
        
        # 시장 정보 탭
        self.market_frame = ttk.Frame(self.info_notebook)
        self.info_notebook.add(self.market_frame, text="🌐 시장 정보")
        
        # 정보 영역 초기화
        self.setup_info_tabs()
        
    def setup_info_tabs(self):
        """정보 탭들 설정"""
        # 종목 정보 탭 설정
        self.setup_stock_info_tab()
        
        # 기술적 지표 탭 설정
        self.setup_indicators_tab()
        
        # 관심종목 탭 설정
        self.setup_watchlist_tab()
        
        # 시장 정보 탭 설정
        self.setup_market_tab()
        
    def setup_stock_info_tab(self):
        """종목 정보 탭 설정"""
        # 스크롤 가능한 프레임
        canvas = tk.Canvas(self.stock_info_frame)
        scrollbar = ttk.Scrollbar(self.stock_info_frame, orient=tk.VERTICAL, command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 종목 정보 레이블들
        self.stock_info_labels = {}
        info_fields = [
            ("symbol", "종목 코드"),
            ("price", "현재가"),
            ("change", "전일 대비"),
            ("change_percent", "변동률"),
            ("volume", "거래량"),
            ("high", "고가"),
            ("low", "저가"),
            ("open", "시가")
        ]
        
        for field, label_text in info_fields:
            frame = ttk.Frame(scrollable_frame)
            frame.pack(fill=tk.X, padx=10, pady=5)
            
            ttk.Label(frame, text=f"{label_text}:", style='Title.TLabel').pack(side=tk.LEFT)
            self.stock_info_labels[field] = ttk.Label(frame, text="-", style='Subtitle.TLabel')
            self.stock_info_labels[field].pack(side=tk.RIGHT)
            
    def setup_indicators_tab(self):
        """기술적 지표 탭 설정"""
        # 지표 표시 영역
        indicators_canvas = tk.Canvas(self.indicators_frame)
        indicators_scrollbar = ttk.Scrollbar(self.indicators_frame, orient=tk.VERTICAL, command=indicators_canvas.yview)
        indicators_scrollable = ttk.Frame(indicators_canvas)
        
        indicators_scrollable.bind(
            "<Configure>",
            lambda e: indicators_canvas.configure(scrollregion=indicators_canvas.bbox("all"))
        )
        
        indicators_canvas.create_window((0, 0), window=indicators_scrollable, anchor="nw")
        indicators_canvas.configure(yscrollcommand=indicators_scrollbar.set)
        
        indicators_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        indicators_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 기술적 지표 레이블들
        self.indicator_labels = {}
        indicators = [
            ("rsi", "RSI(14)"),
            ("macd", "MACD"),
            ("macd_signal", "MACD Signal"),
            ("bb_upper", "볼린저 상단"),
            ("bb_lower", "볼린저 하단"),
            ("sma_20", "SMA(20)"),
            ("ema_20", "EMA(20)"),
            ("stoch_k", "스토캐스틱 %K"),
            ("stoch_d", "스토캐스틱 %D")
        ]
        
        for field, label_text in indicators:
            frame = ttk.Frame(indicators_scrollable)
            frame.pack(fill=tk.X, padx=10, pady=3)
            
            ttk.Label(frame, text=f"{label_text}:", style='Title.TLabel').pack(side=tk.LEFT)
            self.indicator_labels[field] = ttk.Label(frame, text="-", style='Subtitle.TLabel')
            self.indicator_labels[field].pack(side=tk.RIGHT)
            
    def setup_watchlist_tab(self):
        """관심종목 탭 설정"""
        # 관심종목 추가 영역
        add_frame = ttk.Frame(self.watchlist_frame)
        add_frame.pack(fill=tk.X, padx=10, pady=10)
        
        ttk.Label(add_frame, text="종목 추가:", style='Title.TLabel').pack(side=tk.LEFT)
        self.watchlist_entry = ttk.Entry(add_frame, width=10)
        self.watchlist_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.watchlist_entry.bind('<Return>', self.add_to_watchlist)
        
        ttk.Button(add_frame, text="➕", command=self.add_to_watchlist).pack(side=tk.LEFT)
        
        # 관심종목 리스트
        self.watchlist_listbox = tk.Listbox(self.watchlist_frame, height=15)
        self.watchlist_listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=(0, 10))
        self.watchlist_listbox.bind('<Double-Button-1>', self.on_watchlist_double_click)
        
        # 초기 관심종목 로드
        self.load_watchlist()
        
    def setup_market_tab(self):
        """시장 정보 탭 설정"""
        # 시장 상태 표시
        market_status_frame = ttk.LabelFrame(self.market_frame, text="📊 시장 현황", padding=10)
        market_status_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.market_status_label = ttk.Label(market_status_frame, text="시장 상태: 확인 중...", style='Title.TLabel')
        self.market_status_label.pack()
        
        # 주요 지수 (모의 데이터)
        indices_frame = ttk.LabelFrame(self.market_frame, text="📈 주요 지수", padding=10)
        indices_frame.pack(fill=tk.X, padx=10, pady=10)
        
        indices = [("S&P 500", "+0.5%"), ("NASDAQ", "+0.8%"), ("DOW", "-0.2%")]
        for name, change in indices:
            frame = ttk.Frame(indices_frame)
            frame.pack(fill=tk.X, pady=2)
            ttk.Label(frame, text=name, style='Title.TLabel').pack(side=tk.LEFT)
            ttk.Label(frame, text=change, style='Subtitle.TLabel').pack(side=tk.RIGHT)
            
    def create_statusbar(self):
        """상태바 생성"""
        self.statusbar = ttk.Frame(self.main_frame)
        self.statusbar.pack(fill=tk.X, side=tk.BOTTOM)
        
        self.status_label = ttk.Label(self.statusbar, text="준비", style='Subtitle.TLabel')
        self.status_label.pack(side=tk.LEFT, padx=10, pady=5)
        
        self.time_label = ttk.Label(self.statusbar, text="", style='Subtitle.TLabel')
        self.time_label.pack(side=tk.RIGHT, padx=10, pady=5)
        
        # 시간 업데이트
        self.update_time()
        
    def init_components(self):
        """컴포넌트 초기화"""
        try:
            self.data_loader = DataLoader(self.config['data_folder'])
            self.technical_analysis = TechnicalAnalysis()
            self.portfolio_manager = PortfolioManager()
            self.chart_widget = ChartWidget()
            self.status_label.config(text="모든 컴포넌트 로드 완료")
        except Exception as e:
            self.status_label.config(text=f"컴포넌트 로드 실패: {e}")
            print(f"컴포넌트 초기화 오류: {e}")
            
    def quick_analyze(self, symbol):
        """빠른 분석 실행"""
        self.current_symbol.set(symbol)
        self.on_analyze_symbol()
        
    def on_analyze_symbol(self, event=None):
        """종목 분석 실행"""
        symbol = self.current_symbol.get().strip().upper()
        if not symbol:
            messagebox.showwarning("경고", "종목 코드를 입력해주세요.")
            return
            
        self.status_label.config(text=f"{symbol} 분석 중...")
        self.root.update()
        
        try:
            # 데이터 로드
            data = self.data_loader.load_stock_data(symbol)
            if data is None or data.empty:
                messagebox.showerror("오류", f"{symbol} 데이터를 찾을 수 없습니다.")
                self.status_label.config(text="분석 실패")
                return
                
            self.current_data = data
            
            # 차트 업데이트
            self.update_charts(symbol, data)
            
            # 정보 업데이트
            self.update_stock_info(symbol, data)
            self.update_technical_indicators(data)
            
            self.status_label.config(text=f"{symbol} 분석 완료")
            
        except Exception as e:
            messagebox.showerror("오류", f"분석 중 오류 발생: {e}")
            self.status_label.config(text="분석 실패")
            print(f"분석 오류: {e}")
            
    def update_charts(self, symbol, data):
        """차트 업데이트"""
        try:
            # 기본 차트 업데이트
            self.chart_widget.create_candlestick_chart(
                self.basic_chart_frame, symbol, data
            )
            
            # 기술적 분석 차트 업데이트
            indicators = self.technical_analysis.calculate_all_indicators(data)
            self.chart_widget.create_technical_chart(
                self.technical_chart_frame, symbol, data, indicators
            )
            
        except Exception as e:
            print(f"차트 업데이트 오류: {e}")
            
    def update_stock_info(self, symbol, data):
        """종목 정보 업데이트"""
        try:
            if data.empty:
                return
                
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100
            
            info = {
                'symbol': symbol,
                'price': f"${latest['Close']:.2f}",
                'change': f"${change:+.2f}",
                'change_percent': f"{change_percent:+.2f}%",
                'volume': f"{latest['Volume']:,}",
                'high': f"${latest['High']:.2f}",
                'low': f"${latest['Low']:.2f}",
                'open': f"${latest['Open']:.2f}"
            }
            
            for field, value in info.items():
                if field in self.stock_info_labels:
                    self.stock_info_labels[field].config(text=value)
                    
        except Exception as e:
            print(f"종목 정보 업데이트 오류: {e}")
            
    def update_technical_indicators(self, data):
        """기술적 지표 업데이트"""
        try:
            indicators = self.technical_analysis.calculate_all_indicators(data)
            
            if indicators is None:
                return
                
            # 최신 값들 추출
            latest_indicators = {}
            for key, series in indicators.items():
                if isinstance(series, pd.Series) and not series.empty:
                    latest_indicators[key] = series.iloc[-1]
                    
            # 표시 형식 설정
            display_indicators = {
                'rsi': f"{latest_indicators.get('RSI', 0):.1f}",
                'macd': f"{latest_indicators.get('MACD', 0):.3f}",
                'macd_signal': f"{latest_indicators.get('MACD_Signal', 0):.3f}",
                'bb_upper': f"${latest_indicators.get('BB_Upper', 0):.2f}",
                'bb_lower': f"${latest_indicators.get('BB_Lower', 0):.2f}",
                'sma_20': f"${latest_indicators.get('SMA_20', 0):.2f}",
                'ema_20': f"${latest_indicators.get('EMA_20', 0):.2f}",
                'stoch_k': f"{latest_indicators.get('Stoch_K', 0):.1f}",
                'stoch_d': f"{latest_indicators.get('Stoch_D', 0):.1f}"
            }
            
            for field, value in display_indicators.items():
                if field in self.indicator_labels:
                    self.indicator_labels[field].config(text=value)
                    
        except Exception as e:
            print(f"기술적 지표 업데이트 오류: {e}")
            
    def add_to_watchlist(self, event=None):
        """관심종목 추가"""
        symbol = self.watchlist_entry.get().strip().upper()
        if symbol and symbol not in self.get_watchlist():
            self.watchlist_listbox.insert(tk.END, symbol)
            self.watchlist_entry.delete(0, tk.END)
            self.save_watchlist()
            
    def on_watchlist_double_click(self, event):
        """관심종목 더블클릭 처리"""
        selection = self.watchlist_listbox.curselection()
        if selection:
            symbol = self.watchlist_listbox.get(selection[0])
            self.quick_analyze(symbol)
            
    def get_watchlist(self):
        """관심종목 목록 반환"""
        return [self.watchlist_listbox.get(i) for i in range(self.watchlist_listbox.size())]
        
    def load_watchlist(self):
        """관심종목 로드"""
        default_watchlist = self.config.get('default_symbols', [])
        for symbol in default_watchlist:
            self.watchlist_listbox.insert(tk.END, symbol)
            
    def save_watchlist(self):
        """관심종목 저장"""
        watchlist = self.get_watchlist()
        self.config['default_symbols'] = watchlist
        self.save_config()
        
    def select_data_folder(self):
        """데이터 폴더 선택"""
        folder = filedialog.askdirectory(
            title="주식 데이터 폴더 선택",
            initialdir=self.config['data_folder']
        )
        if folder:
            self.config['data_folder'] = folder
            self.save_config()
            self.data_loader = DataLoader(folder)
            messagebox.showinfo("성공", f"데이터 폴더가 {folder}로 설정되었습니다.")
            
    def show_portfolio(self):
        """포트폴리오 창 표시"""
        # 포트폴리오 분석 창 구현
        portfolio_window = tk.Toplevel(self.root)
        portfolio_window.title("💼 포트폴리오 분석")
        portfolio_window.geometry("800x600")
        
        ttk.Label(portfolio_window, text="포트폴리오 분석 기능은 곧 추가됩니다.", 
                 font=('Segoe UI', 14)).pack(expand=True)
                 
    def show_settings(self):
        """설정 창 표시"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 설정")
        settings_window.geometry("600x400")
        
        ttk.Label(settings_window, text="설정 기능은 곧 추가됩니다.", 
                 font=('Segoe UI', 14)).pack(expand=True)
                 
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
        app = VStockAdvanced()
        app.run()
    except Exception as e:
        print(f"프로그램 시작 실패: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()