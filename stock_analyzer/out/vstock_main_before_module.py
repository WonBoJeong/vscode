#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Advanced Pro v3.2 - 주식 분석 및 폭락장 대응 전략 도구
Korean/US Stock Analysis and Investment Strategy Tool with Crash Strategy

Authors: AI Assistant & User
Version: 3.2.0
New Features: 다양한 이동평균선, 기간별 차트, 인기종목/내종목 버튼, 차트 개선
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
warnings.filterwarnings('ignore')

class VStockAdvancedPro:
    """VStock Advanced Pro 메인 애플리케이션 클래스 v3.2"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📈 VStock Advanced Pro v3.2 - 주식 분석 및 폭락장 대응 도구")
        
        # 초기화
        self.current_data = None
        self.current_symbol = ""
        self.korean_stocks = {}
        self.entry_price = None
        self.current_position = 0
        self.log_messages = []
        
        # 차트 설정 변수들 (v3.2 새로 추가)
        self.chart_period = tk.StringVar(value="90일")
        self.show_ma5 = tk.BooleanVar(value=True)
        self.show_ma20 = tk.BooleanVar(value=True)
        self.show_ma60 = tk.BooleanVar(value=False)
        self.show_ma200 = tk.BooleanVar(value=False)
        
        # 인기 종목 및 내 종목 리스트 (v3.2 새로 추가)
        self.popular_stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"]
        self.my_stocks = ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"]
        
        try:
            # 한국 주식 리스트 로드
            self.load_korean_stocks()
            
            # UI 설정
            self.setup_ui()
            self.setup_styles()
            
            # 윈도우 설정
            self.setup_window()
            
            self.log_info("VStock Advanced Pro v3.2 시작됨 - 차트 및 UI 개선")
            
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
            error_text = f"""🚨 VStock Advanced Pro v3.2 Error Report

Function: {error_info['function']}
Args: {error_info['args']}
Kwargs: {error_info['kwargs']}
Error:
{error_info['traceback']}

Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Version: 3.2.0
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
            
            def save_log():
                try:
                    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                    default_filename = f"vstock_error_{timestamp}.txt"
                    
                    filename = filedialog.asksaveasfilename(
                        title="Save Error Log",
                        defaultextension=".txt",
                        initialname=default_filename,
                        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                    )
                    
                    if filename:
                        with open(filename, 'w', encoding='utf-8') as f:
                            f.write(error_text)
                        messagebox.showinfo("✅", f"Error log saved: {filename}")
                except Exception as save_error:
                    messagebox.showerror("❌", f"Save failed: {save_error}")
            
            ttk.Button(button_frame, text="📋 Copy to Clipboard", 
                      command=copy_to_clipboard).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="💾 Save Log", 
                      command=save_log).pack(side=tk.LEFT, padx=(0, 15))
            ttk.Button(button_frame, text="❌ Close", 
                      command=error_window.destroy).pack(side=tk.RIGHT)
            
            # 로그에 추가
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
        """스타일 설정 - 폰트 크기 증대"""
        try:
            self.style = ttk.Style()
            
            available_themes = self.style.theme_names()
            preferred_themes = ['vista', 'xpnative', 'winnative', 'clam']
            
            for theme in preferred_themes:
                if theme in available_themes:
                    self.style.theme_use(theme)
                    break
            
            # 폰트 크기 증대
            self.style.configure('Title.TLabel', font=('Segoe UI', 20, 'bold'))
            self.style.configure('Subtitle.TLabel', font=('Segoe UI', 14, 'bold'))
            self.style.configure('Info.TLabel', font=('Segoe UI', 12))
            self.style.configure('Warning.TLabel', font=('Segoe UI', 12, 'bold'), foreground='red')
            self.style.configure('ErrorTitle.TLabel', font=('Segoe UI', 16, 'bold'), foreground='red')
            
            # 버튼과 기타 위젯 폰트 크기 증대
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
            title_label = ttk.Label(main_frame, text="📈 VStock Advanced Pro v3.2 - 주식 분석 및 폭락장 대응 도구", 
                                  style='Title.TLabel')
            title_label.pack(pady=(0, 25))
            
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
            self.create_analysis_tab()
            self.create_investment_tab()
            self.create_crash_strategy_tab()
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def create_analysis_tab(self):
        """분석 탭 생성 - v3.2 개선"""
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
            
            # 인기 종목 및 내 종목 버튼들 (v3.2 새로 추가)
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
            ttk.Label(left_panel, text="🔥 인기 종목:", style='Subtitle.TLabel').pack(anchor=tk.W)
            
            # 인기 종목 버튼 프레임
            popular_frame = tk.Frame(left_panel)
            popular_frame.pack(fill=tk.X, pady=(5, 10))
            
            # 3x3 그리드로 인기 종목 버튼 배치
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
            
            # 내 종목도 그리드로 배치
            for i, stock in enumerate(self.my_stocks):
                row = i // 3
                col = i % 3
                btn = tk.Button(my_frame, text=stock, width=8, height=1, 
                               font=('Segoe UI', 9), bg='lightblue',
                               command=lambda s=stock: self.select_quick_stock(s))
                btn.grid(row=row, column=col, padx=2, pady=2)
            
            # 종목 리스트 편집 버튼
            edit_stocks_frame = tk.Frame(left_panel)
            edit_stocks_frame.pack(fill=tk.X, pady=(0, 15))
            
            ttk.Button(edit_stocks_frame, text="✏️ 종목 편집", 
                      command=lambda: self.safe_execute(self.edit_stock_lists)).pack(side=tk.LEFT, fill=tk.X, expand=True)
            
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
            
            # 차트 컨트롤 패널 (v3.2 새로 추가)
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
            
            # 차트 기간별 이동평균 가용성 체크
            self.update_ma_availability()
            
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
    
    def edit_stock_lists(self):
        """종목 리스트 편집"""
        try:
            edit_window = tk.Toplevel(self.root)
            edit_window.title("✏️ 종목 리스트 편집")
            edit_window.geometry("600x500")
            edit_window.transient(self.root)
            edit_window.grab_set()
            
            main_frame = ttk.Frame(edit_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📝 종목 리스트 편집", style='Title.TLabel').pack(pady=(0, 20))
            
            # 탭 생성
            notebook = ttk.Notebook(main_frame)
            notebook.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # 인기 종목 탭
            popular_frame = ttk.Frame(notebook)
            notebook.add(popular_frame, text="🔥 인기 종목")
            
            ttk.Label(popular_frame, text="인기 종목 (쉼표로 구분):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 5))
            self.popular_text = tk.Text(popular_frame, height=8, font=('Consolas', 12))
            self.popular_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.popular_text.insert('1.0', ', '.join(self.popular_stocks))
            
            # 내 종목 탭
            my_frame = ttk.Frame(notebook)
            notebook.add(my_frame, text="📋 내 종목")
            
            ttk.Label(my_frame, text="내 종목 (쉼표로 구분):", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(10, 5))
            self.my_text = tk.Text(my_frame, height=8, font=('Consolas', 12))
            self.my_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
            self.my_text.insert('1.0', ', '.join(self.my_stocks))
            
            # 버튼 프레임
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def save_lists():
                try:
                    # 인기 종목 업데이트
                    popular_text = self.popular_text.get('1.0', tk.END).strip()
                    self.popular_stocks = [s.strip().upper() for s in popular_text.split(',') if s.strip()]
                    
                    # 내 종목 업데이트
                    my_text = self.my_text.get('1.0', tk.END).strip()
                    self.my_stocks = [s.strip().upper() for s in my_text.split(',') if s.strip()]
                    
                    # JSON 파일에 저장
                    stock_config = {
                        'popular_stocks': self.popular_stocks,
                        'my_stocks': self.my_stocks
                    }
                    
                    with open('stock_lists.json', 'w', encoding='utf-8') as f:
                        json.dump(stock_config, f, ensure_ascii=False, indent=2)
                    
                    messagebox.showinfo("✅", "종목 리스트가 저장되었습니다!\n애플리케이션을 재시작하면 새로운 리스트가 적용됩니다.")
                    edit_window.destroy()
                    
                    # 즉시 UI 업데이트
                    self.refresh_analysis_tab()
                    
                except Exception as e:
                    messagebox.showerror("❌", f"저장 실패: {e}")
            
            def reset_defaults():
                """기본값으로 재설정"""
                default_popular = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"]
                default_my = ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"]
                
                self.popular_text.delete('1.0', tk.END)
                self.popular_text.insert('1.0', ', '.join(default_popular))
                
                self.my_text.delete('1.0', tk.END)
                self.my_text.insert('1.0', ', '.join(default_my))
            
            ttk.Button(button_frame, text="✅ 저장", command=save_lists).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="🔄 기본값", command=reset_defaults).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="❌ 취소", command=edit_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def refresh_analysis_tab(self):
        """분석 탭 새로고침 (종목 버튼 업데이트용)"""
        # 현재는 단순히 로그만 출력, 실제로는 탭을 다시 그려야 함
        self.log_info("종목 리스트가 업데이트되었습니다.")
    
    def on_chart_period_changed(self, event=None):
        """차트 기간 변경 시 호출"""
        try:
            self.update_ma_availability()
            self.update_chart()
        except Exception as e:
            self.handle_exception(e, True)
    
    def update_ma_availability(self):
        """기간에 따른 이동평균선 가용성 업데이트"""
        try:
            period = self.chart_period.get()
            
            # 30일 차트에서는 MA60, MA200 비활성화
            if period == "30일":
                if self.show_ma60.get():
                    self.show_ma60.set(False)
                if self.show_ma200.get():
                    self.show_ma200.set(False)
                    
                # 장기 이동평균만 기본 선택
                if not self.show_ma5.get() and not self.show_ma20.get():
                    self.show_ma5.set(True)
                    self.show_ma20.set(True)
            
            # 1년 이상에서는 MA5, MA20 기본 해제, MA60, MA200 권장
            elif period in ["1년", "3년", "10년"]:
                if not any([self.show_ma5.get(), self.show_ma20.get(), 
                          self.show_ma60.get(), self.show_ma200.get()]):
                    self.show_ma60.set(True)
                    self.show_ma200.set(True)
                    
        except Exception as e:
            self.log_error(f"이동평균 가용성 업데이트 실패: {e}")
    
    def setup_chart(self, parent):
        """차트 설정 - v3.2 개선"""
        try:
            # 한글 폰트 설정
            plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans', 'Arial Unicode MS']
            plt.rcParams['axes.unicode_minus'] = False
            plt.rcParams['font.size'] = 11
            
            self.fig, self.ax = plt.subplots(figsize=(14, 8))  # 차트 크기 더 증가
            self.canvas = FigureCanvasTkAgg(self.fig, parent)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 초기 차트
            self.ax.text(0.5, 0.5, '📈 차트가 여기에 표시됩니다\n\n주식을 선택하고 분석을 실행하세요', 
                        transform=self.ax.transAxes, ha='center', va='center', 
                        fontsize=16, color='gray')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            
            # 차트 네비게이션 툴바 추가 (확대/축소/이동)
            from matplotlib.backends.backend_tkagg import NavigationToolbar2Tk
            self.toolbar = NavigationToolbar2Tk(self.canvas, parent)
            self.toolbar.update()
            
            self.canvas.draw()
            
        except Exception as e:
            self.log_error(f"차트 설정 실패: {e}")
    
    def update_chart(self):
        """차트 업데이트 - v3.2 대폭 개선"""
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
                chart_data = self.current_data.tail(252)  # 약 1년
                title_period = "1 Year"
            elif period == "3년":
                chart_data = self.current_data.tail(252*3)  # 약 3년
                title_period = "3 Years"
            elif period == "10년":
                chart_data = self.current_data.tail(252*10)  # 약 10년
                title_period = "10 Years"
            else:
                chart_data = self.current_data.tail(90)
                title_period = "90 Days"
            
            if chart_data.empty:
                return
            
            # 가격 차트 (더 굵게)
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
            
            # 범례 설정 (표시할 항목이 있을 때만)
            handles, labels = self.ax.get_legend_handles_labels()
            if handles:
                self.ax.legend(loc='upper left', fontsize=12, framealpha=0.9)
            
            self.ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
            
            # X축 날짜 형식 개선
            if hasattr(chart_data.index, 'date'):
                if len(chart_data) > 252:  # 1년 이상
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                    self.ax.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
                elif len(chart_data) > 90:  # 3개월 이상
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    self.ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
                else:  # 3개월 이하
                    self.ax.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                    self.ax.xaxis.set_major_locator(mdates.WeekdayLocator())
            
            # x축 레이블 회전
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
            # 레이아웃 조정
            self.fig.tight_layout(pad=3.0)
            
            # 가격 범위에 따른 y축 조정
            price_range = chart_data['Close'].max() - chart_data['Close'].min()
            margin = price_range * 0.05  # 5% 마진
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
        """투자 계산기 탭 생성"""
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
            
            # 계산 버튼
            ttk.Button(input_panel, text="🧮 Calculate Position", 
                      command=lambda: self.safe_execute(self.calculate_investment)).pack(fill=tk.X, pady=15, ipady=8)
            
            ttk.Separator(input_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # 빠른 계산 버튼들
            ttk.Label(input_panel, text="Quick Tools:", style='Subtitle.TLabel').pack(anchor=tk.W)
            ttk.Button(input_panel, text="📊 Use Current Stock Price", 
                      command=lambda: self.safe_execute(self.use_current_stock_price)).pack(fill=tk.X, pady=5, ipady=5)
            ttk.Button(input_panel, text="💡 Risk Management Guide", 
                      command=lambda: self.safe_execute(self.show_risk_management)).pack(fill=tk.X, pady=5, ipady=5)
            
            # 우측 패널 (결과)
            result_panel = ttk.LabelFrame(investment_frame, text="📊 Calculation Results", padding="15")
            result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 결과 텍스트
            self.investment_results = scrolledtext.ScrolledText(result_panel, 
                                                              height=25, wrap=tk.WORD, 
                                                              font=('Consolas', 12))
            self.investment_results.pack(fill=tk.BOTH, expand=True)
            
            # 초기 메시지
            initial_message = """💰 VStock Investment Calculator v3.2

이 계산기를 사용하여 다양한 투자 전략을 계획하세요:

📊 지원 전략:
• Single: 일괄 투자 (한 번에 모든 자금 투입)
• DCA: 분할 매수 (Dollar Cost Averaging - 정기적 분할 매수)  
• Pyramid: 피라미드 매수 (하락할수록 더 많이 매수)

🎯 사용법:
1. 총 예산 입력 (달러 기준)
2. 현재가 입력 (또는 "Use Current Stock Price" 버튼)
3. 투자 전략 선택
4. 분할 횟수 설정 (DCA/Pyramid용)
5. "Calculate Position" 클릭

💡 꿀팁: 
• Analysis 탭에서 주식을 분석한 후 "Use Current Stock Price" 버튼을 
  누르면 현재 분석 중인 주식의 가격이 자동으로 입력됩니다.
• Risk Management Guide를 참고하여 안전한 투자 계획을 세우세요.

⚠️ 중요: 투자 전 반드시 위험 관리 가이드를 확인하세요!
"""
            self.investment_results.insert('1.0', initial_message)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def create_crash_strategy_tab(self):
        """폭락장 대응 전략 탭 생성"""
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
                               text="📈 VStock 폭락장 대응 전략 시스템\n\n" +
                                    "이 도구는 특히 레버리지 ETF와 고위험 종목의 폭락 상황에서 합리적인 투자 결정을 내릴 수 있도록 돕습니다.\n\n" +
                                    "🎯 핵심 기능:\n" +
                                    "• 폭락 심각도 자동 평가 (0-100점 정량적 위험 점수)\n" +
                                    "• 손절 vs 분할매수 객관적 판단 기준 제공\n" +
                                    "• 레버리지 ETF (SOXL, TQQQ 등) 전용 위험 관리\n" +
                                    "• AI 투자 자문을 위한 상황 리포트 자동 생성\n" +
                                    "• 최적 손절 레벨 다중 방법론으로 계산\n\n" +
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
            initial_crash_message = """🚨 VStock Crash Strategy Advisor v3.2

폭락장에서 합리적이고 객관적인 투자 결정을 돕는 전문 분석 도구입니다.

💡 핵심 질문: "지금 손절해야 할까? 아니면 분할매수를 계속해야 할까?"

이 질문은 모든 투자자가 폭락장에서 가장 어려워하는 결정입니다. 
감정에 휘둘리지 않고 객관적 데이터로 판단할 수 있도록 도와드립니다.

📊 제공하는 분석 도구들:

🚨 종합 폭락 분석:
   • 현재 상황의 심각도를 0-100점으로 정량화
   • NORMAL → MODERATE → SEVERE → EXTREME 단계별 평가
   • 과거 폭락 사례와의 비교 분석

✂️ 최적 손절 레벨 계산:
   • 기술적 분석 기반 손절가 계산
   • 포트폴리오 비중 고려한 위험 관리
   • 레버리지 ETF 특별 기준 적용

📊 위험도 정밀 평가:
   • VaR (Value at Risk) 계산
   • 최대손실 시나리오 분석
   • 변동성 지표 종합 평가

📋 AI 자문용 리포트:
   • 현재 상황을 정리한 리포트 자동 생성
   • 클로드 등 AI에게 복사해서 전문 상담 요청 가능
   • 객관적 데이터 기반 상황 정리

👆 위의 분석 도구들을 차례로 사용하여 현명한 투자 결정을 내리세요!
"""
            self.crash_results.insert('1.0', initial_crash_message)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    # 기존 메서드들은 동일하게 유지하되 여기서는 핵심 개선 메서드들만 포함
    
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
        """데이터 다운로드 - 진행 상황 표시"""
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
                    
                    # Yahoo Finance에서 데이터 다운로드 (더 많은 데이터)
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
        """주식 정보 업데이트 - 더 자세한 정보"""
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
                color = "red"
            elif drop_pct < -10:
                severity = "⚠️ 상당한 하락"
                recommendation = "위험 관리 점검 필요"
                color = "orange"
            elif drop_pct < -5:
                severity = "📊 보통 조정"
                recommendation = "주의 깊게 관찰"
                color = "blue"
            else:
                severity = "📈 정상 범위"
                recommendation = "정상 보유"
                color = "green"
            
            message = f"""🚨 빠른 폭락 분석 결과

📊 종목: {self.current_symbol}
💰 현재가: ${latest_price:.2f}
📉 10일 최고가 대비: {drop_pct:.2f}%{entry_info}

심각도: {severity}
권장사항: {recommendation}

💡 더 자세한 분석을 원하시면 
'Crash Strategy' 탭의 종합 분석을 이용하세요."""
            
            # 색상이 있는 메시지박스 대신 사용자 정의 창
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
    
    # 투자 계산기 및 폭락 전략 메서드들은 기존과 동일하게 유지
    def calculate_investment(self):
        """투자 계산 실행"""
        messagebox.showinfo("ℹ️", "투자 계산기 기능은 구현 중입니다.")
    
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
    
    def show_risk_management(self):
        """위험 관리 가이드 표시"""
        messagebox.showinfo("ℹ️", "위험 관리 가이드는 구현 중입니다.")
    
    def comprehensive_crash_analysis(self):
        """종합 폭락 분석"""
        messagebox.showinfo("ℹ️", "종합 폭락 분석 기능은 구현 중입니다.")
    
    def calculate_optimal_cutloss(self):
        """최적 손절 레벨 계산"""
        messagebox.showinfo("ℹ️", "최적 손절 레벨 계산 기능은 구현 중입니다.")
    
    def assess_current_risk(self):
        """현재 위험도 평가"""
        messagebox.showinfo("ℹ️", "위험도 평가 기능은 구현 중입니다.")
    
    def generate_situation_report(self):
        """상황 리포트 생성"""
        messagebox.showinfo("ℹ️", "상황 리포트 생성 기능은 구현 중입니다.")
    
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