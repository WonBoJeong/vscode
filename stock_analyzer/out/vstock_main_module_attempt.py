#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Advanced Pro v3.3 - 주식 분석 및 폭락장 대응 전략 도구 (모듈화)
Korean/US Stock Analysis and Investment Strategy Tool with Crash Strategy

Authors: AI Assistant & User
Version: 3.3.0
Features: 모듈화된 구조, 핵심 기능 완전 구현
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
from pathlib import Path
import json
import sys
import os
from datetime import datetime
import traceback
import warnings
warnings.filterwarnings('ignore')

# 모듈 임포트
try:
    from vstock_analysis import AnalysisModule
    from vstock_investment import InvestmentModule
    from vstock_crash_strategy import CrashStrategyModule
except ImportError as e:
    print(f"모듈 임포트 오류: {e}")
    print("필요한 모듈 파일들이 같은 폴더에 있는지 확인해주세요:")
    print("- vstock_analysis.py")
    print("- vstock_investment.py") 
    print("- vstock_crash_strategy.py")
    sys.exit(1)

class VStockAdvancedPro:
    """VStock Advanced Pro 메인 애플리케이션 클래스 v3.3"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📈 VStock Advanced Pro v3.3 - 주식 분석 및 폭락장 대응 도구")
        
        # 공통 데이터 저장소
        self.shared_data = {
            'current_data': None,
            'current_symbol': "",
            'korean_stocks': {},
            'entry_price': None,
            'current_position': 0,
            'log_messages': []
        }
        
        # 설정 로드
        self.load_settings()
        
        try:
            # 한국 주식 리스트 로드
            self.load_korean_stocks()
            
            # 모듈 초기화
            self.init_modules()
            
            # UI 설정
            self.setup_ui()
            self.setup_styles()
            self.setup_window()
            
            self.log_info("VStock Advanced Pro v3.3 시작됨 - 모듈화된 구조")
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def load_settings(self):
        """설정 로드"""
        try:
            settings_file = Path("vstock_settings.json")
            if settings_file.exists():
                with open(settings_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    
                # 종목 리스트 로드
                self.popular_stocks = settings.get('popular_stocks', 
                    ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"])
                self.my_stocks = settings.get('my_stocks',
                    ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"])
            else:
                # 기본값
                self.popular_stocks = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"]
                self.my_stocks = ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"]
                
        except Exception as e:
            self.log_error(f"설정 로드 실패: {e}")
    
    def save_settings(self):
        """설정 저장"""
        try:
            settings = {
                'popular_stocks': self.popular_stocks,
                'my_stocks': self.my_stocks,
                'last_updated': datetime.now().isoformat()
            }
            
            with open("vstock_settings.json", 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
                
        except Exception as e:
            self.log_error(f"설정 저장 실패: {e}")
    
    def load_korean_stocks(self):
        """한국 주식 리스트 로드"""
        try:
            krx_file = Path("krx_stock_list.csv")
            if krx_file.exists():
                df = pd.read_csv(krx_file, encoding='utf-8')
                for _, row in df.iterrows():
                    code = str(row['code']).zfill(6)
                    self.shared_data['korean_stocks'][code] = {
                        'name': row['name'],
                        'market': row.get('market', ''),
                        'sector': row.get('sector', '')
                    }
                self.log_info(f"한국 주식 {len(self.shared_data['korean_stocks'])}개 로드됨")
            else:
                self.log_warning("krx_stock_list.csv 파일을 찾을 수 없습니다")
        except Exception as e:
            self.log_error(f"한국 주식 리스트 로드 실패: {e}")
    
    def init_modules(self):
        """모듈 초기화"""
        try:
            # 각 모듈에 공통 데이터와 메서드 전달
            self.analysis_module = AnalysisModule(self)
            self.investment_module = InvestmentModule(self)
            self.crash_strategy_module = CrashStrategyModule(self)
            
        except Exception as e:
            self.log_error(f"모듈 초기화 실패: {e}")
            raise
    
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
            
            # 종료 시 설정 저장
            self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
                
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
            
            # 위젯 폰트
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
            title_label = ttk.Label(main_frame, 
                                  text="📈 VStock Advanced Pro v3.3 - 주식 분석 및 폭락장 대응 도구 (모듈화)", 
                                  style='Title.TLabel')
            title_label.pack(pady=(0, 25))
            
            # 탭 노트북
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
            # 각 모듈의 탭 생성
            self.analysis_module.create_tab(self.notebook)
            self.investment_module.create_tab(self.notebook)
            self.crash_strategy_module.create_tab(self.notebook)
            
        except Exception as e:
            self.handle_exception(e, True)
    
    def safe_execute(self, func, *args, **kwargs):
        """안전한 함수 실행"""
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
Version: 3.3.0
"""
            
            # 텍스트 위젯
            import tkinter.scrolledtext as scrolledtext
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
            
            # 로그에 추가
            self.shared_data['log_messages'].append(error_text)
            
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
        self.shared_data['log_messages'].append(log_message)
        print(log_message)
    
    def log_error(self, message):
        """에러 로깅"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] ERROR: {message}"
        self.shared_data['log_messages'].append(log_message)
        print(log_message)
    
    def log_warning(self, message):
        """경고 로깅"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] WARNING: {message}"
        self.shared_data['log_messages'].append(log_message)
        print(log_message)
    
    def on_closing(self):
        """애플리케이션 종료 시 호출"""
        try:
            self.save_settings()
            self.root.destroy()
        except Exception as e:
            print(f"종료 중 오류: {e}")
            self.root.destroy()
    
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
        input("Press Enter to exit...")