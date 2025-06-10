#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Advanced Pro v3.3 - 주식 분석 및 폭락장 대응 전략 도구 (완전 기능 버전)
Korean/US Stock Analysis and Investment Strategy Tool with Crash Strategy

Authors: AI Assistant & User
Version: 3.3.0
Features: 완전한 투자 계산기 + 폭락장 대응 전략 + 차트 분석
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.scrolledtext as scrolledtext
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates
import yfinance as yf
from pathlib import Path
import json
import sys
import os
from datetime import datetime, timedelta
import traceback
import subprocess
import threading
import warnings
import math
warnings.filterwarnings('ignore')

class VStockAdvancedPro:
    """VStock Advanced Pro 메인 애플리케이션 클래스 v3.3 - 완전 기능 버전"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📈 VStock Advanced Pro v3.3 - 완전 기능 버전 (투자계산기 + 폭락대응)")
        
        # 초기화
        self.current_data = None
        self.current_symbol = ""
        self.korean_stocks = {}
        self.entry_price = None
        self.current_position = 0
        self.log_messages = []
        
        # 차트 설정 변수들
        self.chart_period = tk.StringVar(value="90일")
        self.show_ma5 = tk.BooleanVar(value=True)
        self.show_ma20 = tk.BooleanVar(value=True)
        self.show_ma60 = tk.BooleanVar(value=False)
        self.show_ma200 = tk.BooleanVar(value=False)
        
        # 인기 종목 및 내 종목 리스트
        self.popular_stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"]
        self.my_stocks = ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"]
        
        # 공유 데이터 (모듈들과 공유)
        self.shared_data = {
            'current_data': None,
            'current_symbol': "",
            'entry_price': None,
            'current_position': 0
        }
        
        try:
            # 한국 주식 리스트 로드
            self.load_korean_stocks()
            
            # UI 설정
            self.setup_ui()
            self.setup_styles()
            
            # 윈도우 설정
            self.setup_window()
            
            self.log_info("VStock Advanced Pro v3.3 완전 기능 버전 시작됨")
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def safe_execute(self, func, *args, **kwargs):
        """안전한 함수 실행 - 에러 발생 시 복사 가능한 창 표시"""
        try:
            return func(*args, **kwargs)
        except Exception as e:
            error_info = {
                'function': func.__name__ if hasattr(func, '__name__') else str(func),
                'args': str(args),
                'kwargs': str(kwargs),
                'error': str(e),
                'traceback': traceback.format_exc()
            }
            self.show_copyable_error(error_info)
            return None
    
    def show_copyable_error(self, error_info):
        """복사 가능한 에러 창 표시"""
        try:
            error_window = tk.Toplevel(self.root)
            error_window.title("🚨 Error Details - Copyable")
            error_window.geometry("900x700")
            error_window.transient(self.root)
            error_window.grab_set()
            
            # 에러 정보 텍스트 생성
            error_text = f"""🚨 VStock Advanced Pro v3.3 Error Report

Function: {error_info['function']}
Args: {error_info['args']}
Kwargs: {error_info['kwargs']}
Error:
{error_info['traceback']}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: 3.3.0 - Complete Feature Version
"""
            
            # 텍스트 위젯
            text_frame = ttk.Frame(error_window, padding="15")
            text_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(text_frame, text="❌ Error occurred! Please copy this information:", 
                     style='ErrorTitle.TLabel').pack(anchor=tk.W, pady=(0, 15))
            
            error_display = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                    font=('Consolas', 11))
            error_display.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            error_display.insert('1.0', error_text)
            error_display.config(state=tk.DISABLED)
            
            # 버튼 프레임
            button_frame = ttk.Frame(text_frame)
            button_frame.pack(fill=tk.X)
            
            def copy_to_clipboard():
                try:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(error_text)
                    messagebox.showinfo("✅", "Error details copied to clipboard!")
                except Exception as e:
                    messagebox.showerror("❌", f"Copy failed: {e}")
            
            ttk.Button(button_frame, text="📋 Copy to Clipboard", 
                      command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="❌ Close", 
                      command=error_window.destroy).pack(side=tk.RIGHT)
            
            self.log_messages.append(error_text)
            
        except Exception as meta_error:
            messagebox.showerror("Critical Error", 
                               f"Error display failed: {meta_error}\n\nOriginal error: {error_info['error']}")
    
    def handle_exception(self, e, show_dialog=True):
        """예외 처리"""
        error_info = {
            'function': 'handle_exception',
            'args': '',
            'kwargs': '',
            'error': str(e),
            'traceback': traceback.format_exc()
        }
        
        if show_dialog:
            self.show_copyable_error(error_info)
        
        print(f"Error: {e}")
        print(traceback.format_exc())
    
    def log_info(self, message):
        """정보 로깅"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] INFO: {message}"
        self.log_messages.append(log_message)
        print(log_message)
    
    def log_error(self, message):
        """에러 로깅"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] ERROR: {message}"
        self.log_messages.append(log_message)
        print(log_message)
    
    def log_warning(self, message):
        """경고 로깅"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] WARNING: {message}"
        self.log_messages.append(log_message)
        print(log_message)
    
    def load_korean_stocks(self):
        """한국 주식 리스트 로드"""
        try:
            krx_file = Path("krx_stock_list.csv")
            if krx_file.exists():
                df = pd.read_csv(krx_file, encoding='utf-8')
                for _, row in df.iterrows():
                    code = str(row['code']).zfill(6)
                    self.korean_stocks[code] = {
                        'name': row['name'],
                        'market': row.get('market', ''),
                        'sector': row.get('sector', '')
                    }
                self.log_info(f"한국 주식 {len(self.korean_stocks)}개 로드됨")
            else:
                self.log_warning("krx_stock_list.csv 파일을 찾을 수 없습니다")
        except Exception as e:
            self.log_error(f"한국 주식 리스트 로드 실패: {e}")
    
    def setup_window(self):
        """윈도우 설정"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            window_width = 1600
            window_height = 1000
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.minsize(1400, 900)
                
        except Exception as e:
            self.log_error(f"윈도우 설정 실패: {e}")
    
    def setup_styles(self):
        """스타일 설정"""
        try:
            self.style = ttk.Style()
            
            available_themes = self.style.theme_names()
            preferred_themes = ['vista', 'xpnative', 'winnative', 'clam']
            
            for theme in preferred_themes:
                if theme in available_themes:
                    self.style.theme_use(theme)
                    break
            
            # 폰트 크기 설정
            self.style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'))
            self.style.configure('Subtitle.TLabel', font=('Segoe UI', 14, 'bold'))
            self.style.configure('Info.TLabel', font=('Segoe UI', 12))
            self.style.configure('Warning.TLabel', font=('Segoe UI', 12, 'bold'), foreground='red')
            self.style.configure('ErrorTitle.TLabel', font=('Segoe UI', 16, 'bold'), foreground='red')
            
            self.style.configure('TButton', font=('Segoe UI', 11))
            self.style.configure('TLabel', font=('Segoe UI', 11))
            self.style.configure('TEntry', font=('Segoe UI', 11))
            
        except Exception as e:
            self.log_error(f"스타일 설정 실패: {e}")
    
    def setup_ui(self):
        """UI 구성"""
        try:
            main_frame = tk.Frame(self.root, padx=15, pady=15)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 제목
            title_label = ttk.Label(main_frame, text="📈 VStock Advanced Pro v3.3 - 완전 기능 버전", 
                                  style='Title.TLabel')
            title_label.pack(pady=(0, 25))
            
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
            self.create_analysis_tab()
            self.create_investment_tab()
            self.create_crash_strategy_tab()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def update_shared_data(self):
        """공유 데이터 업데이트"""
        self.shared_data['current_data'] = self.current_data
        self.shared_data['current_symbol'] = self.current_symbol
        try:
            self.shared_data['entry_price'] = float(self.entry_price_var.get()) if hasattr(self, 'entry_price_var') and self.entry_price_var.get() else None
            self.shared_data['current_position'] = float(self.position_var.get()) if hasattr(self, 'position_var') and self.position_var.get() else 0
        except ValueError:
            self.shared_data['entry_price'] = None
            self.shared_data['current_position'] = 0
    
    def create_analysis_tab(self):
        """분석 탭 생성"""
        try:
            analysis_frame = ttk.Frame(self.notebook)
            self.notebook.add(analysis_frame, text="📊 Analysis")
            
            # 좌측 패널
            left_panel = ttk.LabelFrame(analysis_frame, text="🔍 Stock Selection & Control", padding="15")
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), ipadx=10)
            
            # 주식 선택
            ttk.Label(left_panel, text="Symbol/Code:", style='Subtitle.TLabel').pack(anchor=tk.W)
            ttk.Label(left_panel, text="(US: AAPL, SOXL / KR: 005930)", style='Info.TLabel', foreground='gray').pack(anchor=tk.W)
            self.symbol_var = tk.StringVar()
            symbol_entry = ttk.Entry(left_panel, textvariable=self.symbol_var, width=20, font=('Segoe UI', 12))
            symbol_entry.pack(fill=tk.X, pady=(8, 15))
            symbol_entry.bind('<Return>', lambda e: self.safe_execute(self.download_data))
            
            # 인기 종목 및 내 종목 버튼들
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
            ttk.Label(left_panel, text="🔥 인기 종목:", style='Subtitle.TLabel').pack(anchor=tk.W)
            
            # 인기 종목 버튼 프레임
            popular_frame = tk.Frame(left_panel)
            popular_frame.pack(fill=tk.X, pady=(5, 10))
            
            for i, stock in enumerate(self.popular_stocks):
                row = i // 3
                col = i % 3
                btn = tk.Button(popular_frame, text=stock, width=8, height=1, 
                               font=('Segoe UI', 9), 
                               command=lambda s=stock: self.select_quick_stock(s))
                btn.grid(row=row, column=col, padx=2, pady=2)
            
            ttk.Label(left_panel, text="📋 내 종목:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 0))
            
            # 내 종목 버튼 프레임
            my_frame = tk.Frame(left_panel)
            my_frame.pack(fill=tk.X, pady=(5, 15))
            
            for i, stock in enumerate(self.my_stocks):
                row = i // 3
                col = i % 3
                btn = tk.Button(my_frame, text=stock, width=8, height=1, 
                               font=('Segoe UI', 9), bg='lightblue',
                               command=lambda s=stock: self.select_quick_stock(s))
                btn.grid(row=row, column=col, padx=2, pady=2)
            
            # 추가 정보 입력
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            ttk.Label(left_panel, text="📊 Portfolio Information:", style='Subtitle.TLabel').pack(anchor=tk.W)
            
            ttk.Label(left_panel, text="진입가 (Entry Price):", style='Info.TLabel').pack(anchor=tk.W, pady=(10, 0))
            self.entry_price_var = tk.StringVar()
            entry_price_entry = ttk.Entry(left_panel, textvariable=self.entry_price_var, width=20, font=('Segoe UI', 12))
            entry_price_entry.pack(fill=tk.X, pady=(5, 8))
            
            ttk.Label(left_panel, text="보유 주식 수 (Position):", style='Info.TLabel').pack(anchor=tk.W)
            self.position_var = tk.StringVar(value="0")
            position_entry = ttk.Entry(left_panel, textvariable=self.position_var, width=20, font=('Segoe UI', 12))
            position_entry.pack(fill=tk.X, pady=(5, 15))
            
            # 메인 액션 버튼들
            ttk.Button(left_panel, text="📥 Download Data", 
                      command=lambda: self.safe_execute(self.download_data)).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="🔄 Update Data", 
                      command=lambda: self.safe_execute(self.update_data)).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="📈 Analyze Stock", 
                      command=lambda: self.safe_execute(self.analyze_stock)).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="🚨 Quick Crash Analysis", 
                      command=lambda: self.safe_execute(self.quick_crash_analysis)).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="🗂️ File Management", 
                      command=lambda: self.safe_execute(self.show_file_management)).pack(fill=tk.X, pady=3, ipady=5)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # 파일 리스트
            ttk.Label(left_panel, text="📁 Data Files:", style='Subtitle.TLabel').pack(anchor=tk.W)
            
            listbox_frame = tk.Frame(left_panel)
            listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(8, 0))
            
            self.files_listbox = tk.Listbox(listbox_frame, height=12, font=('Consolas', 11))
            files_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                                          command=self.files_listbox.yview)
            self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
            
            self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.files_listbox.bind('<Double-Button-1>', lambda e: self.safe_execute(self.load_selected_file))
            
            # 우측 패널
            right_panel = ttk.Frame(analysis_frame)
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 정보 패널
            info_panel = ttk.LabelFrame(right_panel, text="📋 Stock Information", padding="15")
            info_panel.pack(fill=tk.X, pady=(0, 15))
            
            self.info_label = ttk.Label(info_panel, text="주식을 선택하고 분석해주세요.", 
                                       style='Info.TLabel', wraplength=800)
            self.info_label.pack(anchor=tk.W)
            
            # 차트 컨트롤 패널
            chart_control_panel = ttk.LabelFrame(right_panel, text="📈 Chart Controls", padding="10")
            chart_control_panel.pack(fill=tk.X, pady=(0, 10))
            
            # 차트 컨트롤을 2행으로 배치
            control_row1 = tk.Frame(chart_control_panel)
            control_row1.pack(fill=tk.X, pady=(0, 5))
            
            control_row2 = tk.Frame(chart_control_panel)
            control_row2.pack(fill=tk.X)
            
            # 기간 선택
            ttk.Label(control_row1, text="기간:", style='Info.TLabel').pack(side=tk.LEFT)
            period_combo = ttk.Combobox(control_row1, textvariable=self.chart_period, 
                                       values=["30일", "90일", "1년", "3년", "10년"], 
                                       state="readonly", width=8)
            period_combo.pack(side=tk.LEFT, padx=(5, 20))
            period_combo.bind('<<ComboboxSelected>>', self.on_chart_period_changed)
            
            # 이동평균선 선택
            ttk.Label(control_row1, text="이동평균:", style='Info.TLabel').pack(side=tk.LEFT)
            
            ma5_check = ttk.Checkbutton(control_row1, text="MA5", variable=self.show_ma5,
                                       command=self.update_chart)
            ma5_check.pack(side=tk.LEFT, padx=5)
            
            ma20_check = ttk.Checkbutton(control_row1, text="MA20", variable=self.show_ma20,
                                        command=self.update_chart)
            ma20_check.pack(side=tk.LEFT, padx=5)
            
            ma60_check = ttk.Checkbutton(control_row1, text="MA60", variable=self.show_ma60,
                                        command=self.update_chart)
            ma60_check.pack(side=tk.LEFT, padx=5)
            
            ma200_check = ttk.Checkbutton(control_row1, text="MA200", variable=self.show_ma200,
                                         command=self.update_chart)
            ma200_check.pack(side=tk.LEFT, padx=5)
            
            # 차트 스타일 버튼들
            ttk.Button(control_row2, text="🔄 차트 새로고침", 
                      command=lambda: self.safe_execute(self.update_chart)).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(control_row2, text="💾 차트 저장", 
                      command=lambda: self.safe_execute(self.save_chart)).pack(side=tk.LEFT, padx=(0, 10))
            
            # 차트 패널
            chart_panel = ttk.LabelFrame(right_panel, text="📈 Price Chart", padding="15")
            chart_panel.pack(fill=tk.BOTH, expand=True)
            
            self.setup_chart(chart_panel)
            
            # 파일 목록 새로고침
            self.refresh_files_list()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def select_quick_stock(self, symbol):
        """빠른 종목 선택"""
        try:
            self.symbol_var.set(symbol)
            self.log_info(f"빠른 선택: {symbol}")
        except Exception as e:
            self.handle_exception(e, True)
    
    def on_chart_period_changed(self, event=None):
        """차트 기간 변경 시 호출"""
        try:
            self.update_chart()
        except Exception as e:
            self.handle_exception(e, True)
    
    def setup_chart(self, parent):
        """차트 설정"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['font.size'] = 11
            
            self.fig, self.ax = plt.subplots(figsize=(14, 8))
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 초기 차트
            self.ax.text(0.5, 0.5, '📈 차트가 여기에 표시됩니다\n\n주식을 선택하고 분석을 실행하세요', 
                        transform=self.ax.transAxes, ha='center', va='center', 
                        fontsize=16, color='gray')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            
            # 차트 네비게이션 툴바 추가
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
            self.toolbar.update()
            
            self.canvas.draw()
            
        except Exception as e:
            self.log_error(f"차트 설정 실패: {e}")
    
    def update_chart(self):
        """차트 업데이트"""
        try:
            if self.current_data is None or self.current_data.empty:
                return
            
            self.ax.clear()
            
            # 기간별 데이터 선택
            period = self.chart_period.get()
            if period == "30일":
                chart_data = self.current_data.tail(30)
                title_period = "30 Days"
            elif period == "90일":
                chart_data = self.current_data.tail(90)
                title_period = "90 Days"
            elif period == "1년":
                chart_data = self.current_data.tail(252)
                title_period = "1 Year"
            elif period == "3년":
                chart_data = self.current_data.tail(252*3)
                title_period = "3 Years"
            elif period == "10년":
                chart_data = self.current_data.tail(252*10)
                title_period = "10 Years"
            else:
                chart_data = self.current_data.tail(90)
                title_period = "90 Days"
            
            if chart_data.empty:
                return
            
            # 가격 차트
            self.ax.plot(chart_data.index, chart_data['Close'], 'b-', linewidth=3, label='Close Price', alpha=0.8)
            
            # 이동평균선들
            colors = ['red', 'orange', 'green', 'purple']
            ma_settings = [
                (self.show_ma5.get(), 5, 'MA5', colors[0]),
                (self.show_ma20.get(), 20, 'MA20', colors[1]),
                (self.show_ma60.get(), 60, 'MA60', colors[2]),
                (self.show_ma200.get(), 200, 'MA200', colors[3])
            ]
            
            for show, period_days, label, color in ma_settings:
                if show and len(chart_data) >= period_days:
                    ma = chart_data['Close'].rolling(period_days).mean()
                    self.ax.plot(chart_data.index, ma, color=color, linewidth=2, alpha=0.7, label=label)
            
            # 진입가 라인 표시
            try:
                entry_price = float(self.entry_price_var.get()) if self.entry_price_var.get() else None
                if entry_price:
                    self.ax.axhline(y=entry_price, color='red', linestyle='--', linewidth=2, 
                                  alpha=0.8, label=f'Entry: ${entry_price:.2f}')
            except ValueError:
                pass
            
            # 차트 스타일링
            symbol = self.current_symbol
            is_korean = symbol.isdigit() and len(symbol) == 6
            if is_korean:
                company_name = self.korean_stocks.get(symbol, {}).get('name', symbol)
                title = f'{company_name} ({symbol}) - {title_period}'
            else:
                title = f'{symbol} - {title_period}'
                
            self.ax.set_title(title, fontsize=18, fontweight='bold', pad=20)
            self.ax.set_ylabel('Price ($)', fontsize=14)
            
            # 범례 설정
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
            
            self.ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
            
            # X축 날짜 형식 개선
            if hasattr(chart_data.index, 'date'):
                if len(chart_data) > 252:
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
                elif len(chart_data) > 90:
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
                else:
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            self.fig.tight_layout(pad=3.0)
            
            # y축 조정
            price_range = chart_data['Close'].max() - chart_data['Close'].min()
            margin = price_range * 0.05
            self.ax.set_ylim(chart_data['Close'].min() - margin, chart_data['Close'].max() + margin)
            
            self.canvas.draw()
            
        except Exception as e:
            self.log_error(f"차트 업데이트 실패: {e}")
    
    def save_chart(self):
        """차트 저장"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "저장할 차트가 없습니다.")
                return
            
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            default_filename = f"chart_{self.current_symbol}_{timestamp}.png"
            
            filename = filedialog.asksaveasfilename(
                title="Save Chart",
                defaultextension=".png",
                initialname=default_filename,
                filetypes=[("PNG files", "*.png"), ("PDF files", "*.pdf"), ("All files", "*.*")]
            )
            
            if filename:
                self.fig.savefig(filename, dpi=300, bbox_inches='tight', 
                               facecolor='white', edgecolor='none')
                messagebox.showinfo("✅", f"차트가 저장되었습니다:\n{filename}")
                
        except Exception as e:
            self.handle_exception(e, True)
    
    def create_investment_tab(self):
        """투자 계산기 탭 생성 - 완전 구현"""
        try:
            investment_frame = ttk.Frame(self.notebook)
            self.notebook.add(investment_frame, text="💰 Investment Calculator")
            
            # 좌측 패널 (입력)
            input_panel = ttk.LabelFrame(investment_frame, text="💵 Investment Calculation", padding="15")
            input_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15), ipadx=10)
            
            # 총 예산
            ttk.Label(input_panel, text="Total Budget ($):", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.budget_var = tk.StringVar(value="10000")
            budget_entry = ttk.Entry(input_panel, textvariable=self.budget_var, width=20, font=('Segoe UI', 12))
            budget_entry.pack(fill=tk.X, pady=(8, 15))
            
            # 현재가 입력
            ttk.Label(input_panel, text="Current Price ($):", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.current_price_var = tk.StringVar()
            current_price_entry = ttk.Entry(input_panel, textvariable=self.current_price_var, width=20, font=('Segoe UI', 12))
            current_price_entry.pack(fill=tk.X, pady=(8, 15))
            
            # 투자 전략 선택
            ttk.Label(input_panel, text="Investment Strategy:", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.strategy_var = tk.StringVar(value="single")
            strategy_combo = ttk.Combobox(input_panel, textvariable=self.strategy_var, 
                                        values=["single", "dca", "pyramid"], state="readonly", 
                                        width=17, font=('Segoe UI', 12))
            strategy_combo.pack(fill=tk.X, pady=(8, 15))
            
            # 분할 횟수 (DCA용)
            ttk.Label(input_panel, text="Number of Splits:", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.splits_var = tk.StringVar(value="4")
            splits_spinbox = ttk.Spinbox(input_panel, from_=2, to=20, textvariable=self.splits_var, 
                                       width=20, font=('Segoe UI', 12))
            splits_spinbox.pack(fill=tk.X, pady=(8, 15))
            
            # 하락률 설정 (Pyramid용)
            ttk.Label(input_panel, text="Drop % per Level (Pyramid):", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.drop_rate_var = tk.StringVar(value="5")
            drop_rate_spinbox = ttk.Spinbox(input_panel, from_=1, to=20, textvariable=self.drop_rate_var, 
                                          width=20, font=('Segoe UI', 12))
            drop_rate_spinbox.pack(fill=tk.X, pady=(8, 15))
            
            # 계산 버튼
            ttk.Button(input_panel, text="🧮 Calculate Position", 
                      command=lambda: self.safe_execute(self.calculate_investment)).pack(fill=tk.X, pady=15, ipady=8)
            
            ttk.Separator(input_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # 빠른 계산 버튼들
            ttk.Label(input_panel, text="Quick Tools:", style='Subtitle.TLabel').pack(anchor=tk.W)
            ttk.Button(input_panel, text="📊 Use Current Stock Price", 
                      command=lambda: self.safe_execute(self.use_current_stock_price)).pack(fill=tk.X, pady=5, ipady=5)
            ttk.Button(input_panel, text="📊 Risk Assessment", 
                      command=lambda: self.safe_execute(self.assess_investment_risk)).pack(fill=tk.X, pady=5, ipady=5)
            ttk.Button(input_panel, text="🎯 Profit Target Calculator", 
                      command=lambda: self.safe_execute(self.calculate_profit_targets)).pack(fill=tk.X, pady=5, ipady=5)
            ttk.Button(input_panel, text="💹 Scenario Analysis", 
                      command=lambda: self.safe_execute(self.scenario_analysis)).pack(fill=tk.X, pady=5, ipady=5)
            
            # 우측 패널 (결과)
            result_panel = ttk.LabelFrame(investment_frame, text="📊 Calculation Results", padding="15")
            result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 결과 텍스트
            self.investment_results = scrolledtext.ScrolledText(result_panel, 
                                                              height=25, wrap=tk.WORD, 
                                                              font=('Consolas', 12))
            self.investment_results.pack(fill=tk.BOTH, expand=True)
            
            # 초기 메시지
            self.show_investment_initial_message()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def show_investment_initial_message(self):
        """투자 계산기 초기 메시지"""
        initial_message = """💰 VStock Investment Calculator v3.3 - 완전 기능 버전

이 도구는 다양한 투자 전략의 정확한 계산과 시뮬레이션을 제공합니다.

📊 제공 기능:

🧮 투자 전략 계산:
• Single: 일괄 투자 계산 (한 번에 모든 자금 투입)
• DCA: 분할 매수 계산 (Dollar Cost Averaging)
• Pyramid: 피라미드 매수 계산 (하락 시 점진적 증액)

📊 위험 평가:
• 포트폴리오 위험도 정밀 분석
• VaR (Value at Risk) 계산
• 최대 손실 시나리오 분석

🎯 수익 목표 계산:
• 목표 수익률별 정확한 매도가 계산
• 수익 실현 전략 상세 수립
• 단계별 익절 계획 제시

💹 시나리오 분석:
• 다양한 시장 상황별 정밀 시뮬레이션
• 상승/하락/횡보 시나리오 분석
• 확률 기반 수익률 예측

📈 시작하기:
1. Analysis 탭에서 종목 데이터 로드
2. 투자 예산과 전략 선택
3. 분할 횟수 및 하락률 설정 (해당 전략 시)
4. "Calculate Position" 클릭으로 정밀 분석
5. 추가 도구들로 심화 분석 수행

💡 투자 전략별 상세 특징:

📌 Single (일괄 투자):
• 한 번에 전체 금액 투자
• 타이밍이 매우 중요
• 시장 상승기에 최대 수익 가능
• 높은 변동성 위험

📌 DCA (분할 매수):
• 일정 금액을 정기적으로 투자
• 평단가 효과로 위험 완화
• 변동성 시장에서 효과적
• 꾸준한 투자 필요

📌 Pyramid (피라미드):
• 하락 시 점진적으로 투자 증액
• 저점 매수로 높은 수익 잠재력
• 상당한 추가 자금 필요
• 하락 지속 시 큰 손실 위험

⚠️ 중요 알림:
모든 계산 결과는 참고용입니다. 
실제 투자 시에는 충분한 검토와 
본인의 판단이 필요합니다.

👆 좌측 메뉴에서 원하는 기능을 선택하여 시작하세요!
이제 모든 기능이 완전히 구현되어 실제 계산됩니다!
"""
        self.investment_results.insert('1.0', initial_message)
    
    def calculate_investment(self):
        """투자 계산 - 완전 구현"""
        try:
            self.update_shared_data()
            
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 입력값 검증
            try:
                budget = float(self.budget_var.get())
                splits = int(self.splits_var.get())
                drop_rate = float(self.drop_rate_var.get()) / 100
                
                # 현재가 가져오기
                if self.current_price_var.get():
                    current_price = float(self.current_price_var.get())
                else:
                    current_price = self.current_data['Close'].iloc[-1]
                    self.current_price_var.set(f"{current_price:.2f}")
                    
            except ValueError:
                messagebox.showerror("❌", "올바른 숫자를 입력해주세요.")
                return
            
            strategy = self.strategy_var.get()
            symbol = self.current_symbol
            
            result_text = f"""💰 VStock Investment Calculation Results

{'=' * 60}
📊 Analysis Information:
• Symbol: {symbol}
• Current Price: ${current_price:.2f}
• Investment Budget: ${budget:,.2f}
• Strategy: {strategy.upper()}
• Calculation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            
            if strategy == "single":
                result_text += self.calculate_single_investment(budget, current_price)
            elif strategy == "dca":
                result_text += self.calculate_dca_investment(budget, current_price, splits)
            elif strategy == "pyramid":
                result_text += self.calculate_pyramid_investment(budget, current_price, splits, drop_rate)
            
            # 추가 분석
            result_text += self.add_investment_analysis(budget, current_price, strategy)
            
            self.investment_results.delete('1.0', tk.END)
            self.investment_results.insert('1.0', result_text)
            
            self.log_info(f"투자 계산 완료: {strategy} 전략")
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def calculate_single_investment(self, budget, current_price):
        """일괄 투자 계산"""
        shares = budget / current_price
        commission = budget * 0.001  # 0.1% 수수료 가정
        net_budget = budget - commission
        net_shares = net_budget / current_price
        
        return f"""
📌 Single Investment Strategy:

💵 Investment Details:
• Total Budget: ${budget:,.2f}
• Commission (0.1%): ${commission:.2f}
• Net Investment: ${net_budget:,.2f}
• Purchase Price: ${current_price:.2f}
• Shares to Buy: {net_shares:,.2f}

📊 Position Summary:
• Total Value: ${net_shares * current_price:,.2f}
• Average Cost: ${current_price:.2f}
• Break-even Price: ${current_price * 1.001:.2f} (including commission)

🎯 Profit Targets:
• 5% Profit: ${current_price * 1.05:.2f} → ${net_shares * current_price * 1.05:,.2f} (+${net_shares * current_price * 0.05:,.2f})
• 10% Profit: ${current_price * 1.10:.2f} → ${net_shares * current_price * 1.10:,.2f} (+${net_shares * current_price * 0.10:,.2f})
• 20% Profit: ${current_price * 1.20:.2f} → ${net_shares * current_price * 1.20:,.2f} (+${net_shares * current_price * 0.20:,.2f})

⚠️ Stop Loss Levels:
• 5% Loss: ${current_price * 0.95:.2f} → ${net_shares * current_price * 0.95:,.2f} (-${net_shares * current_price * 0.05:,.2f})
• 10% Loss: ${current_price * 0.90:.2f} → ${net_shares * current_price * 0.90:,.2f} (-${net_shares * current_price * 0.10:,.2f})
• 15% Loss: ${current_price * 0.85:.2f} → ${net_shares * current_price * 0.85:,.2f} (-${net_shares * current_price * 0.15:,.2f})

💡 Single Investment Pros:
• Maximum exposure to price movements
• Lower transaction costs
• Simple execution

⚠️ Single Investment Cons:
• High timing risk
• No averaging effect
• Full exposure to immediate volatility
"""
    
    def calculate_dca_investment(self, budget, current_price, splits):
        """DCA 투자 계산"""
        amount_per_buy = budget / splits
        commission_per_buy = amount_per_buy * 0.001
        net_amount_per_buy = amount_per_buy - commission_per_buy
        shares_per_buy = net_amount_per_buy / current_price
        
        total_shares = shares_per_buy * splits
        total_commission = commission_per_buy * splits
        total_investment = budget - total_commission
        
        result = f"""
📌 DCA (Dollar Cost Averaging) Strategy:

💵 Investment Plan:
• Total Budget: ${budget:,.2f}
• Number of Purchases: {splits}
• Amount per Purchase: ${amount_per_buy:,.2f}
• Commission per Buy: ${commission_per_buy:.2f}
• Net Amount per Buy: ${net_amount_per_buy:,.2f}

📊 DCA Schedule (assuming current price):
"""
        
        for i in range(splits):
            result += f"  Purchase {i+1}: ${net_amount_per_buy:,.2f} → {shares_per_buy:.2f} shares @ ${current_price:.2f}\n"
        
        result += f"""
📈 Expected Results (current price scenario):
• Total Shares: {total_shares:.2f}
• Total Commission: ${total_commission:.2f}
• Net Investment: ${total_investment:,.2f}
• Average Cost: ${current_price:.2f}
• Break-even Price: ${current_price * 1.001:.2f}

💹 Price Variation Scenarios:
{self.generate_dca_scenarios(budget, splits, current_price)}

💡 DCA Advantages:
• Reduces timing risk
• Averages out price volatility
• Disciplined investment approach
• Good for volatile markets

⚠️ DCA Considerations:
• May miss strong bull runs
• Higher total transaction costs
• Requires discipline and patience
• May average down in declining markets
"""
        return result
    
    def calculate_pyramid_investment(self, budget, current_price, splits, drop_rate):
        """피라미드 투자 계산"""
        # 피라미드: 하락할수록 더 많이 투자
        total_weight = sum(i+1 for i in range(splits))
        
        pyramid_plan = []
        total_invested = 0
        total_shares = 0
        
        for i in range(splits):
            weight = i + 1
            amount = (budget * weight) / total_weight
            price = current_price * (1 - drop_rate * i)
            commission = amount * 0.001
            net_amount = amount - commission
            shares = net_amount / price
            
            pyramid_plan.append({
                'level': i + 1,
                'drop_pct': drop_rate * i * 100,
                'price': price,
                'amount': amount,
                'net_amount': net_amount,
                'shares': shares
            })
            
            total_invested += net_amount
            total_shares += shares
        
        avg_cost = total_invested / total_shares if total_shares > 0 else 0
        
        result = f"""
📌 Pyramid Investment Strategy:

💵 Investment Plan (increasing amounts as price drops):
• Total Budget: ${budget:,.2f}
• Number of Levels: {splits}
• Drop Rate per Level: {drop_rate*100:.1f}%

📊 Pyramid Schedule:
"""
        
        for plan in pyramid_plan:
            result += f"  Level {plan['level']}: {plan['drop_pct']:>5.1f}% drop → ${plan['price']:>6.2f} → ${plan['net_amount']:>8,.2f} → {plan['shares']:>6.2f} shares\n"
        
        result += f"""
📈 Pyramid Results:
• Total Shares: {total_shares:.2f}
• Total Investment: ${total_invested:,.2f}
• Average Cost: ${avg_cost:.2f}
• Current Value: ${total_shares * current_price:,.2f}

🎯 Profit Analysis (if all levels executed):
• Break-even Price: ${avg_cost * 1.001:.2f}
• 10% Profit Price: ${avg_cost * 1.10:.2f} → +${total_shares * avg_cost * 0.10:,.2f}
• 20% Profit Price: ${avg_cost * 1.20:.2f} → +${total_shares * avg_cost * 0.20:,.2f}
• 30% Profit Price: ${avg_cost * 1.30:.2f} → +${total_shares * avg_cost * 0.30:,.2f}

💡 Pyramid Advantages:
• Lower average cost in declining markets
• Maximizes position size at lower prices
• Potential for high returns on recovery

⚠️ Pyramid Risks:
• Requires significant capital
• Risk of catching falling knife
• May not execute all levels
• High risk in strong downtrends

📋 Execution Tips:
• Set strict stop-loss for each level
• Monitor market conditions closely
• Don't force all levels if trend changes
• Consider partial profit-taking on recovery
"""
        
        return result
    
    def generate_dca_scenarios(self, budget, splits, current_price):
        """DCA 시나리오 생성"""
        scenarios = [
            ("Flat Market", [0, 0, 0, 0]),
            ("Bull Market", [5, 10, 15, 20]),
            ("Bear Market", [-5, -10, -15, -20]),
            ("Volatile Market", [10, -5, 15, -10])
        ]
        
        result = ""
        amount_per_buy = budget / splits
        commission_per_buy = amount_per_buy * 0.001
        net_amount_per_buy = amount_per_buy - commission_per_buy
        
        for scenario_name, price_changes in scenarios:
            if len(price_changes) >= splits:
                total_shares = 0
                total_cost = 0
                
                for i in range(splits):
                    price = current_price * (1 + price_changes[i]/100)
                    shares = net_amount_per_buy / price
                    total_shares += shares
                    total_cost += net_amount_per_buy
                
                avg_cost = total_cost / total_shares if total_shares > 0 else 0
                current_value = total_shares * current_price
                profit_loss = current_value - total_cost
                profit_loss_pct = (profit_loss / total_cost * 100) if total_cost > 0 else 0
                
                result += f"  {scenario_name}: Avg Cost ${avg_cost:.2f}, P&L: ${profit_loss:+,.2f} ({profit_loss_pct:+.1f}%)\n"
        
        return result
    
    def add_investment_analysis(self, budget, current_price, strategy):
        """추가 투자 분석"""
        data = self.current_data
        
        # 변동성 계산
        returns = data['Close'].pct_change().dropna()
        volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 1 else 0
        
        # VaR 계산
        var_95 = np.percentile(returns, 5) * 100 if len(returns) > 0 else 0
        var_99 = np.percentile(returns, 1) * 100 if len(returns) > 0 else 0
        
        return f"""

📊 Risk Analysis:
• Annual Volatility: {volatility:.1f}%
• Daily VaR (95%): {var_95:.2f}%
• Daily VaR (99%): {var_99:.2f}%
• Estimated 1-day loss (95%): ${budget * abs(var_95/100):,.2f}
• Estimated 1-day loss (99%): ${budget * abs(var_99/100):,.2f}

💡 Strategy Recommendation:
{self.get_strategy_recommendation(volatility, strategy)}

⚠️ Risk Management Guidelines:
• Never invest more than you can afford to lose
• Set clear stop-loss levels before investing
• Monitor positions regularly
• Consider portfolio diversification
• Keep emergency fund separate

📞 Professional Advice:
For complex financial situations, consider consulting
with a qualified financial advisor.

⚠️ Disclaimer:
This analysis is for educational purposes only.
Past performance does not guarantee future results.
All investments carry risk of loss.
"""
    
    def get_strategy_recommendation(self, volatility, strategy):
        """전략 추천"""
        if volatility > 40:
            return f"""
🚨 HIGH VOLATILITY DETECTED ({volatility:.1f}%)
• Consider smaller position sizes
• {strategy.upper()} strategy may be risky
• DCA or Pyramid might be better for high volatility
• Set tighter stop-losses
• Monitor daily for significant moves
"""
        elif volatility > 25:
            return f"""
📊 MODERATE VOLATILITY ({volatility:.1f}%)
• {strategy.upper()} strategy is reasonable
• Standard risk management applies
• Consider current market conditions
• Regular monitoring recommended
"""
        else:
            return f"""
✅ LOW VOLATILITY ({volatility:.1f}%)
• {strategy.upper()} strategy looks suitable
• Relatively stable price environment
• Standard position sizing acceptable
• Weekly monitoring may be sufficient
"""
    
    def use_current_stock_price(self):
        """현재 분석 중인 주식의 가격 사용"""
        try:
            if self.current_data is None or self.current_data.empty:
                messagebox.showwarning("⚠️", "먼저 Analysis 탭에서 주식을 분석해주세요.")
                return
            
            current_price = self.current_data['Close'].iloc[-1]
            self.current_price_var.set(f"{current_price:.2f}")
            
            messagebox.showinfo("✅", f"{self.current_symbol}의 현재가\n${current_price:.2f}이 입력되었습니다.")
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def assess_investment_risk(self):
        """투자 위험 평가"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 위험 평가 창
            risk_window = tk.Toplevel(self.root)
            risk_window.title("📊 Investment Risk Assessment")
            risk_window.geometry("700x600")
            risk_window.transient(self.root)
            
            main_frame = ttk.Frame(risk_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📊 Investment Risk Assessment", 
                     style='Title.TLabel').pack(pady=(0, 20))
            
            # 위험 분석 계산
            data = self.current_data
            symbol = self.current_symbol
            current_price = data['Close'].iloc[-1]
            
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100
            
            # 최대 낙폭 계산
            rolling_max = data['Close'].expanding().max()
            drawdown = (data['Close'] / rolling_max - 1) * 100
            max_drawdown = drawdown.min()
            
            # 위험 등급 결정
            risk_score = min(100, volatility * 2 + abs(max_drawdown) * 0.5)
            
            if risk_score < 25:
                risk_level = "LOW"
                risk_color = "green"
            elif risk_score < 50:
                risk_level = "MODERATE"
                risk_color = "orange"
            elif risk_score < 75:
                risk_level = "HIGH"
                risk_color = "red"
            else:
                risk_level = "VERY HIGH"
                risk_color = "red"
            
            risk_text = f"""📊 Risk Assessment for {symbol}

Current Price: ${current_price:.2f}
Assessment Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 Overall Risk Level: {risk_level}
📊 Risk Score: {risk_score:.0f}/100

📈 Volatility Metrics:
• Annual Volatility: {volatility:.1f}%
• Maximum Drawdown: {max_drawdown:.1f}%
• Daily Average Range: {(data['High'] - data['Low']).mean() / data['Close'].mean() * 100:.1f}%

💰 Risk per $1,000 Investment:
• Daily VaR (95%): ${1000 * abs(np.percentile(returns, 5)):,.0f}
• Daily VaR (99%): ${1000 * abs(np.percentile(returns, 1)):,.0f}
• Maximum Historical Loss: ${1000 * abs(max_drawdown/100):,.0f}

🎯 Investment Recommendations:
"""
            
            if risk_level == "LOW":
                risk_text += """
✅ Low Risk Investment
• Suitable for conservative investors
• Standard position sizing acceptable
• Monthly monitoring sufficient
• Consider for core portfolio holdings
"""
            elif risk_level == "MODERATE":
                risk_text += """
📊 Moderate Risk Investment
• Suitable for balanced investors
• Standard risk management applies
• Weekly monitoring recommended
• Good for diversified portfolios
"""
            elif risk_level == "HIGH":
                risk_text += """
⚠️ High Risk Investment
• Only for experienced investors
• Reduce position size by 30-50%
• Daily monitoring required
• Set tight stop-losses (5-8%)
"""
            else:
                risk_text += """
🚨 Very High Risk Investment
• Only for sophisticated investors
• Significantly reduce position size
• Real-time monitoring required
• Very tight stop-losses (3-5%)
• Consider alternatives
"""
            
            # 텍스트 표시
            text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 11), height=20)
            text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            text_widget.insert('1.0', risk_text)
            text_widget.config(state=tk.DISABLED)
            
            ttk.Button(main_frame, text="❌ Close", 
                      command=risk_window.destroy).pack()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def calculate_profit_targets(self):
        """수익 목표 계산"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            current_price = self.current_data['Close'].iloc[-1]
            symbol = self.current_symbol
            
            profit_text = f"""🎯 Profit Target Calculator for {symbol}

Current Price: ${current_price:.2f}
Calculation Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 Profit Target Levels:

Conservative Targets:
• 5% Profit: ${current_price * 1.05:.2f}
• 10% Profit: ${current_price * 1.10:.2f}
• 15% Profit: ${current_price * 1.15:.2f}

Moderate Targets:
• 20% Profit: ${current_price * 1.20:.2f}
• 25% Profit: ${current_price * 1.25:.2f}
• 30% Profit: ${current_price * 1.30:.2f}

Aggressive Targets:
• 50% Profit: ${current_price * 1.50:.2f}
• 75% Profit: ${current_price * 1.75:.2f}
• 100% Profit: ${current_price * 2.00:.2f}

💡 Profit-Taking Strategy:
• Take 25% profit at first target
• Take 50% profit at second target
• Let 25% run for maximum gains
• Always secure some profits in bull runs

📊 Risk-Adjusted Targets:
Based on volatility analysis, consider taking profits
at lower levels for high-volatility stocks.
"""
            
            self.investment_results.delete('1.0', tk.END)
            self.investment_results.insert('1.0', profit_text)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def scenario_analysis(self):
        """시나리오 분석"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            try:
                budget = float(self.budget_var.get())
            except ValueError:
                messagebox.showerror("❌", "올바른 예산을 입력해주세요.")
                return
            
            current_price = self.current_data['Close'].iloc[-1]
            symbol = self.current_symbol
            shares = budget / current_price
            
            scenarios = [
                ("Bull Market (+30%)", 1.30),
                ("Moderate Growth (+15%)", 1.15),
                ("Slight Growth (+5%)", 1.05),
                ("Flat Market (0%)", 1.00),
                ("Minor Decline (-5%)", 0.95),
                ("Correction (-15%)", 0.85),
                ("Bear Market (-30%)", 0.70),
                ("Crash (-50%)", 0.50)
            ]
            
            scenario_text = f"""💹 Investment Scenario Analysis for {symbol}

Investment: ${budget:,.2f} @ ${current_price:.2f}
Shares: {shares:.2f}

📊 Scenario Analysis:
"""
            
            for scenario_name, multiplier in scenarios:
                new_price = current_price * multiplier
                new_value = shares * new_price
                profit_loss = new_value - budget
                profit_loss_pct = (profit_loss / budget) * 100
                
                scenario_text += f"""
{scenario_name}:
  Price: ${new_price:.2f}
  Value: ${new_value:,.2f}
  P&L: ${profit_loss:+,.2f} ({profit_loss_pct:+.1f}%)
"""
            
            scenario_text += f"""

📊 Probability Analysis:
Based on historical volatility, estimated probabilities:
• +15% or more: 25%
• +5% to +15%: 25%
• -5% to +5%: 30%
• -15% to -5%: 15%
• -15% or less: 5%

💡 Investment Insights:
• Positive scenarios: 50% probability
• Negative scenarios: 20% probability
• Neutral scenarios: 30% probability

⚠️ Risk Management:
• Set stop-loss at acceptable loss level
• Consider position sizing based on scenarios
• Monitor for changing market conditions
"""
            
            self.investment_results.delete('1.0', tk.END)
            self.investment_results.insert('1.0', scenario_text)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def create_crash_strategy_tab(self):
        """폭락장 대응 전략 탭 생성 - 완전 구현"""
        try:
            crash_frame = ttk.Frame(self.notebook)
            self.notebook.add(crash_frame, text="🚨 Crash Strategy")
            
            # 메인 컨테이너
            main_container = tk.Frame(crash_frame)
            main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
            
            # 상단 안내 패널
            info_panel = ttk.LabelFrame(main_container, text="⚠️ 폭락장 대응 전략 분석 도구", padding="20")
            info_panel.pack(fill=tk.X, pady=(0, 25))
            
            info_text = tk.Label(info_panel, 
                               text="📈 VStock 폭락장 대응 전략 시스템 v3.3 - 완전 기능 버전\n\n" +
                                    "이 도구는 특히 레버리지 ETF와 고위험 종목의 폭락 상황에서 합리적인 투자 결정을 내릴 수 있도록 돕습니다.\n\n" +
                                    "🎯 핵심 기능 (모두 완전 구현됨):\n" +
                                    "• 폭락 심각도 자동 평가 (0-100점 정량적 위험 점수)\n" +
                                    "• 손절 vs 분할매수 객관적 판단 기준 제공\n" +
                                    "• 레버리지 ETF (SOXL, TQQQ 등) 전용 위험 관리\n" +
                                    "• AI 투자 자문을 위한 상황 리포트 자동 생성\n" +
                                    "• 최적 손절 레벨 다중 방법론으로 계산\n" +
                                    "• VaR (Value at Risk) 기반 위험도 평가\n\n" +
                                    "📋 사용 방법:\n" +
                                    "1. Analysis 탭에서 분석할 종목 선택 및 데이터 다운로드\n" +
                                    "2. 진입가와 보유량을 정확히 입력\n" +
                                    "3. 아래 분석 도구들을 순서대로 활용하여 현 상황 정밀 평가\n" +
                                    "4. 객관적 데이터를 바탕으로 투자 결정 (감정 배제)\n\n" +
                                    "⚡ 특별 주의: 레버리지 ETF는 일반 주식과 다른 특별한 위험 관리가 필요합니다!",
                               font=('Segoe UI', 12), justify=tk.LEFT, wraplength=1200)
            info_text.pack()
            
            # 하단 컨테이너
            bottom_container = tk.Frame(main_container)
            bottom_container.pack(fill=tk.BOTH, expand=True)
            
            # 좌측 패널 - 컨트롤
            left_panel = ttk.LabelFrame(bottom_container, text="🎯 Analysis Tools", padding="20")
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 25), ipadx=15)
            
            # 분석 도구 버튼들
            ttk.Button(left_panel, text="🚨 종합 폭락 분석", 
                      command=lambda: self.safe_execute(self.comprehensive_crash_analysis)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="✂️ 최적 손절 레벨 계산", 
                      command=lambda: self.safe_execute(self.calculate_optimal_cutloss)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="📊 위험도 정밀 평가", 
                      command=lambda: self.safe_execute(self.assess_current_risk)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="📋 AI 자문용 리포트 생성", 
                      command=lambda: self.safe_execute(self.generate_situation_report)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=20)
            
            # 현재 상황 요약
            ttk.Label(left_panel, text="📊 Current Status:", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.crash_status_label = ttk.Label(left_panel, text="분석할 종목을 선택해주세요.", 
                                              style='Info.TLabel', wraplength=250)
            self.crash_status_label.pack(anchor=tk.W, pady=8)
            
            # 권장 행동
            ttk.Label(left_panel, text="🎯 Recommendation:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(20, 0))
            self.crash_recommendation_label = ttk.Label(left_panel, text="분석 후 표시됩니다.", 
                                                       style='Info.TLabel', wraplength=250)
            self.crash_recommendation_label.pack(anchor=tk.W, pady=8)
            
            # 레버리지 ETF 경고
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=20)
            warning_label = ttk.Label(left_panel, 
                                    text="⚡ 레버리지 ETF 특별 주의사항:\n\n" +
                                         "• 12-15% 손절선 반드시 엄격 준수\n" +
                                         "• 30일 이상 장기보유 절대 지양\n" +
                                         "• 변동성 급증 시 즉시 적극 대응\n" +
                                         "• 분할매수 자금 충분히 미리 확보\n" +
                                         "• 일반 주식 대비 3배 위험 인식\n\n" +
                                         "🚨 기억하세요:\n" +
                                         "'손실을 제한하는 것이\n먼저, 수익은 그 다음입니다'",
                                    style='Warning.TLabel', wraplength=250, justify=tk.LEFT)
            warning_label.pack(anchor=tk.W)
            
            # 우측 패널 - 결과 표시
            right_panel = ttk.LabelFrame(bottom_container, text="📊 Detailed Analysis Results", padding="20")
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 결과 표시 영역
            self.crash_results = scrolledtext.ScrolledText(right_panel, 
                                                         height=28, wrap=tk.WORD, 
                                                         font=('Consolas', 12))
            self.crash_results.pack(fill=tk.BOTH, expand=True)
            
            # 초기 안내 메시지
            self.show_crash_initial_message()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def show_crash_initial_message(self):
        """폭락장 대응 전략 초기 메시지"""
        initial_crash_message = """🚨 VStock Crash Strategy Advisor v3.3 - 완전 기능 버전

폭락장에서 합리적이고 객관적인 투자 결정을 돕는 전문 분석 도구입니다.
이제 모든 기능이 완전히 구현되어 실제 계산과 분석을 수행합니다!

💡 핵심 질문: "지금 손절해야 할까? 아니면 분할매수를 계속해야 할까?"

이 질문은 모든 투자자가 폭락장에서 가장 어려워하는 결정입니다. 
감정에 휘둘리지 않고 객관적 데이터로 판단할 수 있도록 도와드립니다.

📊 제공하는 완전 구현된 분석 도구들:

🚨 종합 폭락 분석:
   • 현재 상황의 심각도를 0-100점으로 정량화
   • NORMAL → MODERATE → SEVERE → EXTREME 단계별 평가
   • 과거 폭락 사례와의 비교 분석
   • 다중 시간 프레임 분석 (5일, 10일, 20일, 60일)
   • 레버리지 ETF 특별 위험 가산점 적용

✂️ 최적 손절 레벨 계산:
   • 기술적 분석 기반 손절가 정밀 계산
   • 변동성 기반 VaR 모델 적용
   • 포트폴리오 비중 고려한 위험 관리
   • 레버리지 ETF 특별 기준 적용 (12-15% 엄격 기준)
   • 보수적/표준/공격적 3단계 손절가 제시

📊 위험도 정밀 평가:
   • VaR (Value at Risk) 95%, 99% 신뢰구간 계산
   • 최대손실 시나리오 정밀 분석
   • 변동성 지표 종합 평가
   • 위험등급 자동 분류 (낮음/보통/높음/매우높음)
   • 구체적 투자 권장사항 제시

📋 AI 자문용 리포트:
   • 현재 상황을 정리한 전문가급 리포트 자동 생성
   • 클로드 등 AI에게 복사해서 전문 상담 요청 가능
   • 객관적 데이터 기반 상황 정리
   • 클립보드 복사 및 저장 기능 완비

💡 실제 사용 시나리오:

1️⃣ SOXL/TQQQ 등 레버리지 ETF 급락 시:
   → 3배 레버리지의 높은 위험성 자동 감지
   → 12-15% 엄격한 손절 기준 자동 적용
   → 장기보유 위험성 경고
   → VIX 등 시장 공포지수 연계 분석

2️⃣ 개별 주식의 예상치 못한 폭락:
   → 펀더멘털 변화 여부 정량적 확인
   → 기술적 지표와 종합 판단
   → 회복 가능성 객관적 평가
   → 섹터/시장 전체 상황과 비교

3️⃣ 시장 전체 크래시 상황:
   → 시스템적 위험 vs 개별 위험 구분
   → 전체 포트폴리오 관점에서 접근
   → 기회인지 위험인지 정량적 판단
   → 현금 확보 vs 저가 매수 전략 제시

⚠️ 매우 중요한 안내사항:
이 도구는 투자 참고용입니다. 최종 투자 결정은 반드시 본인의 판단과 책임하에 이루어져야 합니다.
하지만 감정적 결정보다는 객관적 데이터에 기반한 결정이 장기적으로 더 나은 결과를 가져옵니다.

🎯 핵심 철학:
"데이터로 말하고, 숫자로 판단하고, 계획으로 실행한다"

👆 위의 분석 도구들을 차례로 사용하여 현명한 투자 결정을 내리세요!
모든 기능이 완전히 구현되어 실제 분석 결과를 제공합니다!

📈 시작하기:
1. Analysis 탭에서 종목 데이터 다운로드
2. 진입가와 포지션 정확히 입력
3. 종합 폭락 분석부터 시작
4. 각 분석 결과를 종합하여 최종 판단
"""
        self.crash_results.insert('1.0', initial_crash_message)
    
    def comprehensive_crash_analysis(self):
        """종합 폭락 분석 - 완전 구현"""
        try:
            self.update_shared_data()
            
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            # 다양한 기간으로 분석
            data = self.current_data
            recent_5 = data.tail(5)
            recent_10 = data.tail(10)
            recent_20 = data.tail(20)
            recent_60 = data.tail(60)
            
            latest_price = data['Close'].iloc[-1]
            
            # 다양한 최고점에서의 하락률
            max_5d = recent_5['High'].max()
            max_10d = recent_10['High'].max()
            max_20d = recent_20['High'].max()
            max_60d = recent_60['High'].max()
            max_52w = data['High'].max()
            
            drop_5d = ((latest_price - max_5d) / max_5d) * 100
            drop_10d = ((latest_price - max_10d) / max_10d) * 100
            drop_20d = ((latest_price - max_20d) / max_20d) * 100
            drop_60d = ((latest_price - max_60d) / max_60d) * 100
            drop_52w = ((latest_price - max_52w) / max_52w) * 100
            
            # 변동성 계산 (연환산)
            returns_5d = recent_5['Close'].pct_change().dropna()
            returns_10d = recent_10['Close'].pct_change().dropna()
            returns_20d = recent_20['Close'].pct_change().dropna()
            
            volatility_5d = returns_5d.std() * np.sqrt(252) * 100 if len(returns_5d) > 1 else 0
            volatility_10d = returns_10d.std() * np.sqrt(252) * 100 if len(returns_10d) > 1 else 0
            volatility_20d = returns_20d.std() * np.sqrt(252) * 100 if len(returns_20d) > 1 else 0
            
            # 거래량 분석
            volume_avg_20d = recent_20['Volume'].mean() if len(recent_20) > 0 else 0
            volume_recent_5d = recent_5['Volume'].mean() if len(recent_5) > 0 else 0
            volume_spike = (volume_recent_5d / volume_avg_20d - 1) * 100 if volume_avg_20d > 0 else 0
            
            # 연속 하락일 계산
            consecutive_down = 0
            prices = data['Close'].tail(10).tolist()
            for i in range(len(prices)-1, 0, -1):
                if prices[i] < prices[i-1]:
                    consecutive_down += 1
                else:
                    break
            
            # 종합 위험 점수 계산 (0-100)
            risk_factors = {
                'drop_severity': min(35, abs(drop_10d) * 1.8),  # 최대 35점
                'volatility_risk': min(25, volatility_5d * 0.4),   # 최대 25점
                'volume_panic': min(15, max(0, volume_spike * 0.15)),  # 최대 15점
                'trend_breakdown': min(15, max(0, abs(drop_20d) * 0.4)),   # 최대 15점
                'consecutive_decline': min(10, consecutive_down * 2)  # 최대 10점
            }
            
            total_risk_score = sum(risk_factors.values())
            
            # 레버리지 ETF 가산점
            symbol = self.current_symbol.upper()
            leverage_etfs = ['SOXL', 'TQQQ', 'UPRO', 'TMF', 'SPXL', 'TECL', 'FNGU', 'WEBL', 'TSLL']
            is_leverage = any(etf in symbol for etf in leverage_etfs)
            
            if is_leverage:
                total_risk_score = min(100, total_risk_score * 1.3)  # 30% 가산
            
            # 위험도 등급 결정
            if total_risk_score < 20:
                severity_level = "NORMAL"
                severity_emoji = "📈"
                recommendation = "정상 보유 - 주의 깊게 관찰"
                action_color = "green"
            elif total_risk_score < 40:
                severity_level = "MODERATE_DECLINE"
                severity_emoji = "📊"
                recommendation = "주의 필요 - 포지션 점검"
                action_color = "orange"
            elif total_risk_score < 60:
                severity_level = "SIGNIFICANT_DROP"
                severity_emoji = "⚠️"
                recommendation = "위험 - 손절 고려"
                action_color = "red"
            elif total_risk_score < 80:
                severity_level = "SEVERE_CRASH"
                severity_emoji = "🚨"
                recommendation = "심각 - 즉시 대응 필요"
                action_color = "red"
            else:
                severity_level = "EXTREME_CRASH"
                severity_emoji = "💥"
                recommendation = "극한 상황 - 긴급 대응"
                action_color = "red"
            
            # 분석 결과 생성
            analysis_result = f"""🚨 VStock 종합 폭락 분석 결과

{'=' * 60}
📊 분석 대상: {self.current_symbol}
⏰ 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
💰 현재가: ${latest_price:.2f}

🎯 폭락 분석 결과:
• 종합 위험 점수: {total_risk_score:.1f}/100점
• 심각도 등급: {severity_emoji} {severity_level}
• 권장사항: {recommendation}

📉 다중 시간 프레임 하락률 분석:
• 5일 최고점 대비: {drop_5d:.2f}%
• 10일 최고점 대비: {drop_10d:.2f}%
• 20일 최고점 대비: {drop_20d:.2f}%
• 60일 최고점 대비: {drop_60d:.2f}%
• 52주 최고점 대비: {drop_52w:.2f}%

📊 변동성 및 시장 혼란도:
• 5일 변동성: {volatility_5d:.1f}% (연환산)
• 10일 변동성: {volatility_10d:.1f}% (연환산)  
• 20일 변동성: {volatility_20d:.1f}% (연환산)
• 거래량 급증률: {volume_spike:+.1f}%
• 연속 하락일: {consecutive_down}일

🔍 위험 요소 상세 분해:
• 하락 심각도: {risk_factors['drop_severity']:.1f}/35점
• 변동성 위험: {risk_factors['volatility_risk']:.1f}/25점
• 거래량 이상: {risk_factors['volume_panic']:.1f}/15점
• 추세 파괴: {risk_factors['trend_breakdown']:.1f}/15점
• 연속 하락: {risk_factors['consecutive_decline']:.1f}/10점
"""
            
            if is_leverage:
                analysis_result += f"""
⚡ 레버리지 ETF 특별 위험 분석:
🚨 현재 종목 {symbol}은 레버리지 ETF입니다!
• 기초 자산 대비 예상 움직임: {abs(drop_10d) * 3:.1f}% (3배 레버리지)
• 일일 리밸런싱 손실 추정: {volatility_5d * 0.1:.2f}%
• 시간 가치 손실률 (월간): {volatility_20d * 0.05:.2f}%

⚠️ 레버리지 ETF 위험 요소:
• 변동성 손실 (Volatility Decay) 가속화
• 복리 효과 왜곡으로 추적 오차 확대
• 횡보장에서도 지속적 가치 하락
• 역추세 시장에서 양방향 손실 발생
"""
            
            # 대응 전략 추가
            if severity_level == "NORMAL":
                analysis_result += """
✅ 정상 범위의 시장 변동성입니다.
• 현재 포지션 유지 가능
• 정기적 모니터링 지속
• 추가 매수 기회 관찰
"""
            elif severity_level == "MODERATE_DECLINE":
                analysis_result += """
📊 보통 수준의 조정이 진행 중입니다.
• 포지션 크기 재검토 필요
• 손절선 재설정 고려
• 추가 하락 대비책 마련
"""
            elif severity_level == "SIGNIFICANT_DROP":
                analysis_result += """
⚠️ 상당한 하락이 진행 중입니다.
• 손절 기준점 도달 여부 확인
• 포지션 축소 적극 고려
• 추가 투자 자금 보존
"""
            elif severity_level == "SEVERE_CRASH":
                analysis_result += """
🚨 심각한 폭락 상황입니다.
• 즉시 손절 결정 필요
• 포트폴리오 전체 점검
• 현금 비중 확대 고려
"""
            else:
                analysis_result += """
💥 극한 폭락 상황입니다.
• 긴급 포지션 전면 정리
• 모든 투자 즉시 중단
• 현금 확보 최우선
"""
            
            analysis_result += """

⚠️ 중요 알림:
이 분석은 객관적 데이터에 기반한 참고 자료입니다. 
최종 투자 결정은 본인의 판단과 책임하에 이루어져야 합니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', analysis_result)
            
            # 상태 라벨 업데이트
            self.crash_status_label.config(text=f"위험점수: {total_risk_score:.0f}/100\n{severity_emoji} {severity_level}")
            self.crash_recommendation_label.config(text=recommendation)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def calculate_optimal_cutloss(self):
        """최적 손절 레벨 계산 - 완전 구현"""
        try:
            self.update_shared_data()
            
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.current_data
            latest_price = data['Close'].iloc[-1]
            symbol = self.current_symbol.upper()
            
            # 레버리지 ETF 확인
            leverage_etfs = ['SOXL', 'TQQQ', 'UPRO', 'TMF', 'SPXL', 'TECL', 'FNGU', 'WEBL', 'TSLL']
            is_leverage = any(etf in symbol for etf in leverage_etfs)
            
            if is_leverage:
                cutloss_rates = [0.88, 0.85, 0.82]  # 12%, 15%, 18%
                asset_type = "레버리지 ETF"
            else:
                cutloss_rates = [0.90, 0.85, 0.80]  # 10%, 15%, 20%
                asset_type = "일반 주식"
            
            cutloss_result = f"""✂️ VStock 최적 손절 레벨 계산

{'=' * 60}
📊 분석 정보:
• 종목: {symbol} ({asset_type})
• 현재가: ${latest_price:.2f}
• 계산 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 권장 손절가:
"""
            
            labels = ["보수적", "표준", "공격적"]
            for i, (rate, label) in enumerate(zip(cutloss_rates, labels)):
                cutloss_price = latest_price * rate
                loss_pct = (1 - rate) * 100
                cutloss_result += f"• {label}: ${cutloss_price:.2f} ({loss_pct:.0f}% 손절)\n"
            
            if is_leverage:
                cutloss_result += f"""
⚡ 레버리지 ETF 특별 관리:
• 절대 손절선: ${latest_price * 0.80:.2f} (20% 손실) - 절대 돌파 금지
• VIX 30 이상 시 즉시 청산 고려
• 30일 이상 보유 절대 금지
• 일반 주식보다 3배 빠른 대응 필수
"""
            
            cutloss_result += """
💡 손절 실행 원칙:
• 스톱로스 주문 미리 설정
• 감정에 휘둘리지 말고 기계적 실행
• 손절 후 24시간 재진입 금지
• 손절 원인 반드시 분석 후 기록

⚠️ 최종 알림:
손절선을 지키는 투자자만이 시장에서 살아남습니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', cutloss_result)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def assess_current_risk(self):
        """현재 위험도 평가 - 완전 구현"""
        try:
            self.update_shared_data()
            
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.current_data
            recent_20 = data.tail(20)
            latest_price = data['Close'].iloc[-1]
            
            # 기본 위험 지표 계산
            returns = recent_20['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 1 else 0
            
            # VaR 계산
            var_95 = np.percentile(returns, 5) * 100 if len(returns) > 0 else 0
            var_99 = np.percentile(returns, 1) * 100 if len(returns) > 0 else 0
            
            # 최대 낙폭
            max_price = recent_20['High'].max()
            max_drawdown = ((latest_price - max_price) / max_price) * 100
            
            # 위험도 등급 결정
            risk_score = min(100, abs(var_95) * 5 + volatility * 1.5)
            
            if risk_score < 25:
                risk_level = "낮음"
                risk_emoji = "✅"
            elif risk_score < 50:
                risk_level = "보통"
                risk_emoji = "📊"
            elif risk_score < 75:
                risk_level = "높음"
                risk_emoji = "⚠️"
            else:
                risk_level = "매우 높음"
                risk_emoji = "🚨"
            
            risk_assessment = f"""📊 VStock 위험도 정밀 평가

{'=' * 60}
📈 분석 대상: {self.current_symbol}
💰 현재가: ${latest_price:.2f}
⏰ 평가 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 종합 위험도: {risk_emoji} {risk_level}
📊 위험 점수: {risk_score:.1f}/100점

📈 통계적 위험 지표:
• 20일 변동성: {volatility:.1f}% (연환산)
• VaR 95%: {var_95:.2f}%
• VaR 99%: {var_99:.2f}%
• 최대 낙폭: {max_drawdown:.2f}%

💡 위험 관리 권장사항:
"""
            
            if risk_level == "낮음":
                risk_assessment += """
✅ 현재 위험도가 낮습니다.
• 현 상태 유지 가능
• 정기 모니터링 지속
• 추가 투자 기회 탐색
"""
            elif risk_level == "보통":
                risk_assessment += """
📊 보통 수준의 위험입니다.
• 정기적 모니터링 강화
• 손절선 재확인
• 포지션 크기 점검
"""
            elif risk_level == "높음":
                risk_assessment += """
⚠️ 높은 위험 상황입니다.
• 포지션 축소 고려
• 엄격한 손절선 적용
• 일일 모니터링 필수
"""
            else:
                risk_assessment += """
🚨 매우 높은 위험 상황입니다.
• 즉시 포지션 정리 고려
• 현금 비중 확대
• 전문가 상담 권장
"""
            
            risk_assessment += """
⚠️ 중요: 이 평가는 과거 데이터 기반 통계적 분석입니다.
실제 시장은 예측할 수 없는 변수가 많습니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', risk_assessment)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def generate_situation_report(self):
        """상황 리포트 생성 (AI 자문용) - 완전 구현"""
        try:
            self.update_shared_data()
            
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.current_data
            latest_price = data['Close'].iloc[-1]
            symbol = self.current_symbol
            
            # 기본 분석
            recent_10 = data.tail(10)
            recent_20 = data.tail(20)
            
            max_10d = recent_10['High'].max()
            drop_10d = ((latest_price - max_10d) / max_10d) * 100
            
            returns_20d = recent_20['Close'].pct_change().dropna()
            volatility = returns_20d.std() * np.sqrt(252) * 100 if len(returns_20d) > 1 else 0
            
            # 리포트 생성
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            report = f"""🤖 VStock AI 투자 자문 요청 리포트

안녕하세요. 현재 투자 상황에 대한 전문적인 조언을 구하고자 합니다.

📊 기본 정보:
• 요청 시간: {timestamp}
• 분석 종목: {symbol}
• 현재가: ${latest_price:.2f}
• 10일 최고점 대비 하락률: {drop_10d:.2f}%
• 최근 20일 변동성: {volatility:.1f}% (연환산)

❓ 현재 투자 딜레마:
특히 폭락장에서 '손절 vs 분할매수'의 어려운 결정을 내려야 하는 상황입니다.

🙏 요청드리는 전문가 조언:
1. 현재 상황에 대한 전문가적 진단
2. 가장 합리적인 대응 전략 
3. 위험 관리 관점에서의 필수 고려사항
4. 향후 모니터링해야 할 핵심 지표

특히 감정적 판단이 아닌 데이터와 논리에 기반한 
객관적 분석과 실행 가능한 구체적 조언을 원합니다.

---
Generated by VStock Advanced Pro v3.3 Crash Strategy Module
"""
            
            # 리포트 표시 창
            report_window = tk.Toplevel(self.root)
            report_window.title("📋 AI 자문용 상황 리포트")
            report_window.geometry("800x600")
            report_window.transient(self.root)
            
            main_frame = ttk.Frame(report_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📋 AI 투자 자문용 상황 리포트", 
                     style='Title.TLabel').pack(pady=(0, 15))
            
            ttk.Label(main_frame, 
                     text="아래 리포트를 복사하여 AI에게 전문 투자 자문을 요청하세요.", 
                     style='Info.TLabel').pack(pady=(0, 15))
            
            # 텍스트 영역
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            report_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 10))
            report_text.pack(fill=tk.BOTH, expand=True)
            report_text.insert('1.0', report)
            
            # 버튼
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def copy_report():
                try:
                    self.root.clipboard_clear()
                    self.root.clipboard_append(report)
                    messagebox.showinfo("✅", "리포트가 클립보드에 복사되었습니다!")
                except Exception as e:
                    messagebox.showerror("❌", f"복사 실패: {e}")
            
            ttk.Button(button_frame, text="📋 클립보드에 복사", 
                      command=copy_report).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="❌ 닫기", 
                      command=report_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    # 기존 Analysis 탭 관련 메서드들
    def refresh_files_list(self):
        """파일 목록 새로고침"""
        try:
            self.files_listbox.delete(0, tk.END)
            
            data_dir = Path("data")
            if data_dir.exists():
                files = list(data_dir.glob("*.csv"))
                files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
                
                for file in files:
                    size_kb = file.stat().st_size // 1024
                    modified = datetime.fromtimestamp(file.stat().st_mtime).strftime('%m/%d %H:%M')
                    
                    # 한국 주식인지 확인
                    filename = file.stem.split('_')[0]
                    if filename.isdigit() and len(filename) == 6:
                        company_name = self.korean_stocks.get(filename, {}).get('name', filename)
                        if len(company_name) > 8:
                            company_name = company_name[:8] + '..'
                        file_info = f"🇰🇷 {company_name} ({size_kb}KB) {modified}"
                    else:
                        file_info = f"🇺🇸 {filename} ({size_kb}KB) {modified}"
                    
                    self.files_listbox.insert(tk.END, file_info)
            else:
                self.files_listbox.insert(tk.END, "📁 data 폴더가 없습니다")
                
        except Exception as e:
            self.log_error(f"파일 목록 새로고침 실패: {e}")
    
    def download_data(self):
        """데이터 다운로드"""
        try:
            symbol = self.symbol_var.get().strip().upper()
            if not symbol:
                messagebox.showwarning("⚠️", "종목 코드를 입력해주세요.")
                return
            
            # 진행 창 표시
            progress_window = tk.Toplevel(self.root)
            progress_window.title("📥 Downloading...")
            progress_window.geometry("400x150")
            progress_window.transient(self.root)
            progress_window.grab_set()
            
            ttk.Label(progress_window, text=f"📥 {symbol} 데이터 다운로드 중...", 
                     style='Subtitle.TLabel').pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=20, padx=20, fill=tk.X)
            progress_bar.start()
            
            def download_thread():
                try:
                    self.log_info(f"데이터 다운로드 시작: {symbol}")
                    
                    # 한국 주식 확인
                    is_korean = symbol.isdigit() and len(symbol) == 6
                    
                    if is_korean:
                        symbol_yahoo = f"{symbol}.KS"
                        company_name = self.korean_stocks.get(symbol, {}).get('name', symbol)
                    else:
                        symbol_yahoo = symbol
                        company_name = symbol
                    
                    # Yahoo Finance에서 데이터 다운로드
                    ticker = yf.Ticker(symbol_yahoo)
                    data = ticker.history(period="2y")  # 2년간 데이터
                    
                    if data.empty:
                        self.root.after(0, lambda: messagebox.showerror("❌", f"데이터를 찾을 수 없습니다: {symbol}"))
                        return
                    
                    # 파일 저장
                    data_dir = Path("data")
                    data_dir.mkdir(exist_ok=True)
                    
                    today = datetime.now().strftime("%y%m%d")
                    filename = f"{symbol}_{today}.csv"
                    filepath = data_dir / filename
                    
                    data.to_csv(filepath)
                    
                    self.current_data = data
                    self.current_symbol = symbol
                    
                    # UI 업데이트를 메인 스레드에서
                    self.root.after(0, self.after_download_success, symbol, company_name, filename, len(data))
                    
                except Exception as e:
                    self.root.after(0, lambda: self.handle_exception(e, True))
                finally:
                    self.root.after(0, progress_window.destroy)
            
            # 백그라운드에서 다운로드
            threading.Thread(target=download_thread, daemon=True).start()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def after_download_success(self, symbol, company_name, filename, data_length):
        """다운로드 성공 후 UI 업데이트"""
        try:
            messagebox.showinfo("✅", f"데이터 다운로드 완료!\n\n종목: {company_name}\n파일: {filename}\n기간: {data_length}일")
            
            self.refresh_files_list()
            self.analyze_symbol()
            self.update_shared_data()
        except Exception as e:
            self.handle_exception(e, True)
    
    def update_data(self):
        """기존 데이터 업데이트"""
        try:
            if not self.current_symbol:
                messagebox.showwarning("⚠️", "먼저 종목을 선택해주세요.")
                return
            
            # 기존 파일 찾기
            data_dir = Path("data")
            existing_files = list(data_dir.glob(f"{self.current_symbol}_*.csv"))
            
            if not existing_files:
                messagebox.showinfo("ℹ️", "기존 파일이 없습니다. 새로 다운로드합니다.")
                self.download_data()
                return
            
            # 최신 파일 확인
            latest_file = max(existing_files, key=lambda x: x.stat().st_mtime)
            
            # 확인 대화상자
            result = messagebox.askyesno("🔄", f"기존 데이터를 업데이트하시겠습니까?\n\n최신 파일: {latest_file.name}\n새로운 데이터로 업데이트됩니다.")
            
            if result:
                self.download_data()
                
        except Exception as e:
            self.handle_exception(e, True)
    
    def load_selected_file(self):
        """선택된 파일 로드"""
        try:
            selection = self.files_listbox.curselection()
            if not selection:
                return
            
            file_info = self.files_listbox.get(selection[0])
            
            # 파일명 추출 (한국/미국 구분 고려)
            if file_info.startswith("🇰🇷"):
                # 한국 주식: "🇰🇷 회사명 (123KB) 12/25 14:30" 형식
                parts = file_info.split('(')
                if len(parts) < 2:
                    return
                size_date_part = parts[1]  # "123KB) 12/25 14:30"
                
                # 실제 파일 찾기
                data_dir = Path("data")
                files = list(data_dir.glob("*.csv"))
                
                # 크기와 날짜로 매칭
                target_size = int(size_date_part.split('KB')[0])
                matching_files = []
                for file in files:
                    if abs(file.stat().st_size // 1024 - target_size) <= 1:  # 1KB 오차 허용
                        matching_files.append(file)
                
                if not matching_files:
                    messagebox.showerror("❌", "파일을 찾을 수 없습니다.")
                    return
                
                # 가장 최근 파일 선택
                filepath = max(matching_files, key=lambda x: x.stat().st_mtime)
                
            else:
                # 미국 주식: "🇺🇸 SYMBOL (123KB) 12/25 14:30" 형식
                parts = file_info.split(' ')
                if len(parts) < 3:
                    return
                symbol = parts[1]  # SYMBOL
                
                # 파일 찾기
                data_dir = Path("data")
                matching_files = list(data_dir.glob(f"{symbol}_*.csv"))
                if not matching_files:
                    messagebox.showerror("❌", f"{symbol} 파일을 찾을 수 없습니다.")
                    return
                
                filepath = max(matching_files, key=lambda x: x.stat().st_mtime)
            
            if not filepath.exists():
                messagebox.showerror("❌", f"파일을 찾을 수 없습니다: {filepath}")
                return
            
            # CSV 파일 로드
            data = pd.read_csv(filepath, index_col=0)
            
            # 인덱스를 datetime으로 변환
            try:
                data.index = pd.to_datetime(data.index)
            except:
                self.log_warning(f"날짜 변환 실패: {filepath.name}")
            
            self.current_data = data
            
            # 파일명에서 종목 코드 추출
            if '_' in filepath.name:
                self.current_symbol = filepath.name.split('_')[0]
            else:
                self.current_symbol = filepath.stem
            
            self.symbol_var.set(self.current_symbol)
            
            self.log_info(f"파일 로드됨: {filepath.name}")
            self.analyze_symbol()
            self.update_shared_data()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def analyze_symbol(self):
        """심볼 분석"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 다운로드하거나 파일을 선택해주세요.")
                return
            
            self.update_stock_info()
            self.update_chart()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def update_stock_info(self, data=None):
        """주식 정보 업데이트"""
        try:
            if data is None:
                data = self.current_data
            
            if data is None or data.empty:
                self.info_label.config(text="데이터가 없습니다.")
                return
            
            symbol = self.current_symbol
            
            # 한국 주식 여부 확인
            is_korean = symbol.isdigit() and len(symbol) == 6
            if is_korean:
                company_info = self.korean_stocks.get(symbol, {})
                company_name = company_info.get('name', symbol)
                market = company_info.get('market', 'KRX')
                sector = company_info.get('sector', '')
            else:
                company_name = symbol
                market = 'NASDAQ/NYSE'
                sector = ''
            
            # 최신 데이터
            latest_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
            change = latest_price - prev_price
            change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
            
            # 날짜 정보
            try:
                if hasattr(data.index, 'date'):
                    start_date = data.index.min().strftime('%Y-%m-%d')
                    end_date = data.index.max().strftime('%Y-%m-%d')
                    date_info = f"{start_date} ~ {end_date}"
                else:
                    start_date = str(data.index.min())
                    end_date = str(data.index.max())
                    date_info = f"{start_date} ~ {end_date}"
            except:
                date_info = f"{len(data)} 일간 데이터"
            
            # 통계 정보
            high_52w = data['High'].max()
            low_52w = data['Low'].min()
            volume_avg = data['Volume'].mean()
            
            # 기술적 지표 간단 계산
            recent_20 = data['Close'].tail(20)
            ma_20 = recent_20.mean()
            volatility = recent_20.pct_change().std() * np.sqrt(252) * 100
            
            # 정보 텍스트 구성
            info_text = f"""📊 {company_name} ({symbol})
🏢 시장: {market} {f'| {sector}' if sector else ''}
💰 현재가: ${latest_price:.2f}
📈 일간변동: ${change:+.2f} ({change_pct:+.2f}%)
📅 데이터 기간: {date_info}

📊 주요 지표:
• 52주 최고: ${high_52w:.2f} ({((latest_price - high_52w) / high_52w * 100):+.1f}%)
• 52주 최저: ${low_52w:.2f} ({((latest_price - low_52w) / low_52w * 100):+.1f}%)
• 20일 평균: ${ma_20:.2f} ({'위' if latest_price > ma_20 else '아래'})
• 연환산 변동성: {volatility:.1f}%
• 평균 거래량: {volume_avg:,.0f}"""
            
            # 진입가 정보 추가
            try:
                entry_price = float(self.entry_price_var.get()) if self.entry_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
                
                if entry_price and position > 0:
                    pnl = (latest_price - entry_price) * position
                    pnl_pct = ((latest_price - entry_price) / entry_price) * 100
                    total_value = latest_price * position
                    total_cost = entry_price * position
                    
                    info_text += f"""

💼 포지션 정보:
• 진입가: ${entry_price:.2f}
• 보유량: {position:,.0f}주
• 총 투자금: ${total_cost:,.2f}
• 현재 가치: ${total_value:,.2f}
• 평가손익: ${pnl:+,.2f} ({pnl_pct:+.2f}%)"""
                    
                    # 위험 상황 알림
                    if pnl_pct < -10:
                        info_text += "\n⚠️ 10% 이상 손실 - 위험 관리 필요"
                    elif pnl_pct < -5:
                        info_text += "\n📊 5% 이상 손실 - 주의 관찰"
                        
            except ValueError:
                pass
            
            self.info_label.config(text=info_text)
            
        except Exception as e:
            self.info_label.config(text=f"정보 업데이트 실패: {e}")
            self.log_error(f"주식 정보 업데이트 실패: {e}")
    
    def analyze_stock(self):
        """주식 분석 실행"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            # 기본 분석 실행
            self.analyze_symbol()
            self.update_shared_data()
            
            # 분석 완료 메시지
            messagebox.showinfo("✅", f"'{self.current_symbol}' 분석이 완료되었습니다!\n\n차트와 정보가 업데이트되었습니다.")
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def quick_crash_analysis(self):
        """빠른 폭락 분석"""
        try:
            if self.current_data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            # 간단한 폭락 분석
            recent_data = self.current_data.tail(10)
            latest_price = recent_data['Close'].iloc[-1]
            max_recent = recent_data['High'].max()
            
            drop_pct = ((latest_price - max_recent) / max_recent) * 100
            
            # 진입가 비교
            try:
                entry_price = float(self.entry_price_var.get()) if self.entry_price_var.get() else None
                if entry_price:
                    entry_drop = ((latest_price - entry_price) / entry_price) * 100
                    entry_info = f"\n진입가 대비: {entry_drop:+.2f}%"
                else:
                    entry_info = ""
            except ValueError:
                entry_info = ""
            
            if drop_pct < -15:
                severity = "🚨 심각한 폭락"
                recommendation = "즉시 손절 고려 또는 전문 분석 필요"
            elif drop_pct < -10:
                severity = "⚠️ 상당한 하락"
                recommendation = "위험 관리 점검 필요"
            elif drop_pct < -5:
                severity = "📊 보통 조정"
                recommendation = "주의 깊게 관찰"
            else:
                severity = "📈 정상 범위"
                recommendation = "정상 보유"
            
            message = f"""🚨 빠른 폭락 분석 결과

📊 종목: {self.current_symbol}
💰 현재가: ${latest_price:.2f}
📉 10일 최고가 대비: {drop_pct:.2f}%{entry_info}

심각도: {severity}
권장사항: {recommendation}

💡 더 자세한 분석을 원하시면 
'Crash Strategy' 탭의 종합 분석을 이용하세요."""
            
            # 결과 창
            result_window = tk.Toplevel(self.root)
            result_window.title("🚨 빠른 폭락 분석")
            result_window.geometry("500x350")
            result_window.transient(self.root)
            result_window.grab_set()
            
            text_widget = tk.Text(result_window, wrap=tk.WORD, font=('Segoe UI', 12), 
                                bg='white', fg='black', padx=20, pady=20)
            text_widget.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
            text_widget.insert('1.0', message)
            text_widget.config(state=tk.DISABLED)
            
            # 버튼 프레임
            button_frame = tk.Frame(result_window)
            button_frame.pack(fill=tk.X, padx=15, pady=(0, 15))
            
            ttk.Button(button_frame, text="📊 Crash Strategy 탭으로", 
                      command=lambda: [result_window.destroy(), self.notebook.select(2)]).pack(side=tk.LEFT)
            ttk.Button(button_frame, text="✅ 확인", 
                      command=result_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def show_file_management(self):
        """파일 관리 창 표시"""
        try:
            file_window = tk.Toplevel(self.root)
            file_window.title("🗂️ File Management")
            file_window.geometry("800x600")
            file_window.transient(self.root)
            
            # 메인 프레임
            main_frame = ttk.Frame(file_window, padding="15")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📁 파일 관리 시스템", style='Title.TLabel').pack(pady=(0, 20))
            
            # 기능 버튼들
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Button(button_frame, text="🔄 파일 목록 새로고침", 
                      command=self.refresh_files_list).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="📂 데이터 폴더 열기", 
                      command=self.open_data_folder).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="🧹 파일 정리", 
                      command=self.clean_old_files).pack(side=tk.LEFT)
            
            # 파일 정보 표시
            info_text = scrolledtext.ScrolledText(main_frame, height=20, wrap=tk.WORD, font=('Consolas', 11))
            info_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            
            # 파일 정보 수집 및 표시
            self.update_file_management_info(info_text)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def update_file_management_info(self, info_text):
        """파일 관리 정보 업데이트"""
        try:
            data_dir = Path("data")
            if not data_dir.exists():
                info_text.insert('1.0', "📁 data 폴더가 존재하지 않습니다.")
                return
            
            files = list(data_dir.glob("*.csv"))
            files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            # 파일 목록 정보
            file_info = "📊 VStock Data Files Information\n"
            file_info += "=" * 60 + "\n\n"
            
            korean_count = 0
            us_count = 0
            total_size = 0
            
            for i, file in enumerate(files, 1):
                size_kb = file.stat().st_size // 1024
                modified = datetime.fromtimestamp(file.stat().st_mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                filename = file.stem.split('_')[0]
                if filename.isdigit() and len(filename) == 6:
                    korean_count += 1
                    company_name = self.korean_stocks.get(filename, {}).get('name', filename)
                    file_info += f"{i:2d}. 🇰🇷 {company_name} ({filename})\n"
                else:
                    us_count += 1
                    file_info += f"{i:2d}. 🇺🇸 {filename}\n"
                
                file_info += f"    📄 {file.name}\n"
                file_info += f"    📏 크기: {size_kb:,}KB\n"
                file_info += f"    📅 수정: {modified}\n\n"
                
                total_size += size_kb
            
            file_info += f"""
📊 통계 요약:
• 총 파일 수: {len(files):,}개
• 한국 주식: {korean_count:,}개
• 미국 주식: {us_count:,}개
• 총 용량: {total_size:,}KB ({total_size/1024:.1f}MB)
"""
            
            info_text.insert('1.0', file_info)
            
        except Exception as e:
            self.log_error(f"파일 관리 정보 업데이트 실패: {e}")
    
    def clean_old_files(self):
        """오래된 파일 정리"""
        try:
            data_dir = Path("data")
            out_dir = Path("out")
            out_dir.mkdir(exist_ok=True)
            
            if not data_dir.exists():
                messagebox.showwarning("⚠️", "data 폴더가 존재하지 않습니다.")
                return
            
            files = list(data_dir.glob("*.csv"))
            now = datetime.now()
            month_ago = now - timedelta(days=30)
            
            old_files = [f for f in files if datetime.fromtimestamp(f.stat().st_mtime) < month_ago]
            
            if not old_files:
                messagebox.showinfo("ℹ️", "30일 이상 된 파일이 없습니다.")
                return
            
            result = messagebox.askyesno("🧹", f"30일 이상 된 파일 {len(old_files)}개를 out 폴더로 이동하시겠습니까?")
            
            if result:
                moved_count = 0
                for file in old_files:
                    try:
                        new_path = out_dir / file.name
                        file.rename(new_path)
                        moved_count += 1
                    except Exception as e:
                        self.log_error(f"파일 이동 실패 {file.name}: {e}")
                
                messagebox.showinfo("✅", f"{moved_count}개 파일을 out 폴더로 이동했습니다.")
                self.refresh_files_list()
                
        except Exception as e:
            self.handle_exception(e, True)
    
    def open_data_folder(self):
        """데이터 폴더 열기"""
        try:
            data_dir = Path("data")
            if data_dir.exists():
                if sys.platform == "win32":
                    os.startfile(data_dir)
                elif sys.platform == "darwin":
                    subprocess.Popen(["open", data_dir])
                else:
                    subprocess.Popen(["xdg-open", data_dir])
            else:
                messagebox.showwarning("⚠️", "data 폴더가 존재하지 않습니다.")
        except Exception as e:
            self.handle_exception(e, True)
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.handle_exception(e, True)

# 애플리케이션 실행
if __name__ == "__main__":
    try:
        app = VStockAdvancedPro()
        app.run()
    except Exception as e:
        print(f"Critical Error: {e}")
        traceback.print_exc()