#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Main Application
모듈형 주식 분석 프로그램 (4개 정보 패널로 개선, 4가지 폭락 전략 분석 추가)

Author: AI Assistant & User
Version: 1.3.0 - 4가지 폭락 대응 전략 분석 추가
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
from pathlib import Path
from datetime import datetime

# 프로젝트 모듈 import
from config import APP_NAME, APP_VERSION, UI_CONFIG, POPULAR_STOCKS, MY_STOCKS
from modules.utils import Logger, ErrorHandler, DataValidator, format_currency_auto
from modules.data_manager import DataManager, show_download_dialog
from modules.korean_stock_manager import KoreanStockManager, show_korean_stock_search_dialog
from modules.chart_manager import ChartManager, ChartControlPanel
from modules.analysis_engine import AnalysisEngine
from modules.investment_calculator import InvestmentCalculator
from modules.crash_analyzer import CrashAnalyzer

class BosPlanApp:
    """1Bo's Plan 메인 애플리케이션"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} v{APP_VERSION}")
        
        # 로깅 및 에러 처리
        self.logger = Logger("BosPlanApp")
        self.error_handler = ErrorHandler(self.root)
        
        # 모듈 초기화
        self.data_manager = DataManager()
        self.korean_manager = KoreanStockManager()
        self.analysis_engine = AnalysisEngine()
        self.investment_calculator = InvestmentCalculator()
        self.crash_analyzer = CrashAnalyzer()
        
        # 🎯 UI 변수 - "평단가" 용어로 변경
        self.symbol_var = tk.StringVar()
        self.avg_price_var = tk.StringVar()  # 진입가 → 평단가
        self.position_var = tk.StringVar(value="0")
        self.current_symbol = ""  # 현재 선택된 종목 추적
        
        # 차트 관련 변수
        self.chart_manager = None
        self.chart_control_panel = None
        
        # 🎯 4개 정보 패널 변수
        self.stock_info_panel = None
        self.position_info_panel = None
        self.technical_info_panel = None
        self.signal_info_panel = None
        self.stock_info_label = None
        self.position_info_label = None
        self.technical_info_label = None
        self.signal_info_label = None
        
        try:
            self.setup_ui()
            self.setup_window()
            self.logger.info(f"{APP_NAME} v{APP_VERSION} started successfully")
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Application initialization")
    
    def setup_window(self):
        """윈도우 설정 - 세로로 더 크게 설정"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # 기본 크기보다 가로 20%, 세로 40% 더 크게 설정
            base_width = UI_CONFIG['window_width']
            base_height = UI_CONFIG['window_height']
            
            window_width = int(base_width * 1.2)
            window_height = int(base_height * 1.4)  # 세로를 더 크게
            
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
            
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
            self.root.minsize(UI_CONFIG['min_width'], UI_CONFIG['min_height'])
            
        except Exception as e:
            self.logger.error(f"Window setup failed: {e}")
    
    def setup_ui(self):
        """UI 구성"""
        try:
            main_frame = tk.Frame(self.root, padx=15, pady=15)
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            title_label = tk.Label(main_frame, 
                                 text=f"📈 {APP_NAME} v{APP_VERSION}", 
                                 font=(UI_CONFIG['font_family'], UI_CONFIG['font_size_title'], 'bold'))
            title_label.pack(pady=(0, 20))
            
            self.notebook = ttk.Notebook(main_frame)
            self.notebook.pack(fill=tk.BOTH, expand=True)
            
            self.create_analysis_tab()
            self.create_investment_tab()
            self.create_crash_tab()
            
        except Exception as e:
            self.error_handler.handle_exception(e, True, "UI setup")
    
    def create_analysis_tab(self):
        """분석 탭 생성 - 🎯 4개 정보 패널로 개선"""
        try:
            analysis_frame = ttk.Frame(self.notebook)
            self.notebook.add(analysis_frame, text="📊 Analysis")
            
            left_panel = ttk.LabelFrame(analysis_frame, text="🔍 Stock Selection", padding="15")
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
            
            tk.Label(left_panel, text="Symbol/Code:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            tk.Label(left_panel, text="(US: AAPL, SOXL / KR: 005930, 5930)", foreground='gray').pack(anchor=tk.W)
            
            symbol_frame = tk.Frame(left_panel)
            symbol_frame.pack(fill=tk.X, pady=(5, 10))
            
            symbol_entry = tk.Entry(symbol_frame, textvariable=self.symbol_var, font=('Segoe UI', 12))
            symbol_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
            symbol_entry.bind('<Return>', lambda e: self.download_data())
            # 종목 변경 감지
            self.symbol_var.trace('w', self.on_symbol_change)
            
            search_btn = tk.Button(symbol_frame, text="🔍", width=3, command=self.search_korean_stock)
            search_btn.pack(side=tk.RIGHT, padx=(5, 0))
            
            tk.Label(left_panel, text="🔥 인기 종목:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(10, 5))
            
            popular_frame = tk.Frame(left_panel)
            popular_frame.pack(fill=tk.X, pady=(0, 10))
            
            # 인기 종목 8개를 4x2로 배치
            for i, stock in enumerate(POPULAR_STOCKS[:8]):
                row = i // 4
                col = i % 4
                btn = tk.Button(popular_frame, text=stock, width=6,
                               command=lambda s=stock: self.select_stock(s))
                btn.grid(row=row, column=col, padx=2, pady=2)
            
            tk.Label(left_panel, text="📋 내 종목:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(10, 5))
            
            my_frame = tk.Frame(left_panel)
            my_frame.pack(fill=tk.X, pady=(0, 15))
            
            # 내 종목 8개를 4x2로 배치
            for i, stock in enumerate(MY_STOCKS[:8]):
                row = i // 4
                col = i % 4
                btn = tk.Button(my_frame, text=stock, width=6, bg='lightblue',
                               command=lambda s=stock: self.select_stock(s))
                btn.grid(row=row, column=col, padx=2, pady=2)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
            
            # 🎯 포트폴리오 정보 - "평단가" 용어로 변경
            tk.Label(left_panel, text="📊 Portfolio Info:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            
            tk.Label(left_panel, text="평단가 (Average Price):").pack(anchor=tk.W)
            tk.Entry(left_panel, textvariable=self.avg_price_var).pack(fill=tk.X, pady=(2, 8))
            
            tk.Label(left_panel, text="보유량 (Position):").pack(anchor=tk.W)
            tk.Entry(left_panel, textvariable=self.position_var).pack(fill=tk.X, pady=(2, 15))
            
            # 🎯 자동 설정 버튼 추가
            tk.Button(left_panel, text="📥 Download & Auto Setup", 
                     command=self.download_and_auto_setup,
                     bg='#4CAF50', fg='white', font=('Segoe UI', 10, 'bold')).pack(fill=tk.X, pady=2)
            
            tk.Button(left_panel, text="📥 Download Data", command=self.download_data).pack(fill=tk.X, pady=2)
            tk.Button(left_panel, text="📈 Analyze", command=self.analyze_stock).pack(fill=tk.X, pady=2)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=10)
            tk.Label(left_panel, text="📁 Data Files:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
            
            self.files_listbox = tk.Listbox(left_panel, height=8)
            self.files_listbox.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            self.files_listbox.bind('<Double-Button-1>', self.load_selected_file)
            
            # 우측 패널
            right_panel = ttk.Frame(analysis_frame)
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 🎯 4개 정보 패널을 가로로 배치
            info_container = tk.Frame(right_panel)
            info_container.pack(fill=tk.X, pady=(0, 10))
            
            # 1. 종목 정보 패널
            self.stock_info_panel = ttk.LabelFrame(info_container, text="📊 Stock Info", padding="8")
            self.stock_info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            
            self.stock_info_label = tk.Label(self.stock_info_panel, text="종목을 선택하세요", 
                                           font=('Segoe UI', 9), justify=tk.LEFT, wraplength=200)
            self.stock_info_label.pack(anchor=tk.W)
            
            # 2. 포지션 정보 패널
            self.position_info_panel = ttk.LabelFrame(info_container, text="💼 Position", padding="8")
            self.position_info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            
            self.position_info_label = tk.Label(self.position_info_panel, text="포지션 없음", 
                                               font=('Segoe UI', 9), justify=tk.LEFT, wraplength=200)
            self.position_info_label.pack(anchor=tk.W)
            
            # 3. 기술적 분석 패널
            self.technical_info_panel = ttk.LabelFrame(info_container, text="🔍 Technical", padding="8")
            self.technical_info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
            
            self.technical_info_label = tk.Label(self.technical_info_panel, text="분석 대기중", 
                                                font=('Segoe UI', 9), justify=tk.LEFT, wraplength=200)
            self.technical_info_label.pack(anchor=tk.W)
            
            # 4. 매매 신호 패널
            self.signal_info_panel = ttk.LabelFrame(info_container, text="🎯 Trading Signal", padding="8")
            self.signal_info_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            
            self.signal_info_label = tk.Label(self.signal_info_panel, text="신호 없음", 
                                             font=('Segoe UI', 9), justify=tk.LEFT, wraplength=200)
            self.signal_info_label.pack(anchor=tk.W)
            
            # 차트 패널 - 🎯 더 넓은 공간 확보
            chart_panel = ttk.LabelFrame(right_panel, text="📈 Chart", padding="10")
            chart_panel.pack(fill=tk.BOTH, expand=True)
            
            # 🎯 차트 컨트롤 패널 먼저 생성
            chart_controls_frame = tk.Frame(chart_panel)
            chart_controls_frame.pack(fill=tk.X, pady=(0, 10))
            
            # 차트 매니저 생성
            self.chart_manager = ChartManager(chart_panel)
            
            # 🎯 차트 컨트롤 패널 생성 (기존에 구현된 기능 복원)
            self.chart_control_panel = ChartControlPanel(chart_controls_frame, self.chart_manager)
            
            self.refresh_files_list()
            
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Analysis tab creation")
    
    def create_investment_tab(self):
        """투자 계산기 탭"""
        try:
            investment_frame = ttk.Frame(self.notebook)
            self.notebook.add(investment_frame, text="💰 Investment")
            
            input_panel = ttk.LabelFrame(investment_frame, text="💵 Investment Calculator", padding="15")
            input_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
            
            tk.Label(input_panel, text="Total Budget:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            self.budget_var = tk.StringVar(value="10000")  # 기본값 (미국 주식용)
            budget_entry = tk.Entry(input_panel, textvariable=self.budget_var, font=('Segoe UI', 12))
            budget_entry.pack(fill=tk.X, pady=(5, 10))
            
            tk.Label(input_panel, text="Current Price:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            self.current_price_var = tk.StringVar()
            current_price_entry = tk.Entry(input_panel, textvariable=self.current_price_var, font=('Segoe UI', 12))
            current_price_entry.pack(fill=tk.X, pady=(5, 10))
            
            tk.Label(input_panel, text="Strategy:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            self.strategy_var = tk.StringVar(value="single")
            strategy_combo = ttk.Combobox(input_panel, textvariable=self.strategy_var,
                                        values=["single", "dca", "pyramid"], state="readonly")
            strategy_combo.pack(fill=tk.X, pady=(5, 10))
            
            tk.Label(input_panel, text="Splits:", font=('Segoe UI', 12, 'bold')).pack(anchor=tk.W)
            self.splits_var = tk.StringVar(value="4")
            tk.Spinbox(input_panel, from_=2, to=20, textvariable=self.splits_var).pack(fill=tk.X, pady=(5, 15))
            
            tk.Button(input_panel, text="🧮 Calculate", font=('Segoe UI', 12, 'bold'),
                     command=self.calculate_investment).pack(fill=tk.X, pady=10)
            
            ttk.Separator(input_panel, orient='horizontal').pack(fill=tk.X, pady=10)
            tk.Button(input_panel, text="📊 Use Current Price", command=self.use_current_price).pack(fill=tk.X, pady=5)
            tk.Button(input_panel, text="🎯 Risk Assessment", command=self.assess_risk).pack(fill=tk.X, pady=5)
            
            result_panel = ttk.LabelFrame(investment_frame, text="📊 Results", padding="15")
            result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            self.investment_results = scrolledtext.ScrolledText(result_panel, wrap=tk.WORD, 
                                                              font=('Consolas', 11))
            self.investment_results.pack(fill=tk.BOTH, expand=True)
            
            self.investment_results.insert('1.0', f"""💰 {APP_NAME} Investment Calculator

이 도구는 다양한 투자 전략을 계산하고 비교합니다.

📊 제공 기능:
• Single: 일괄 투자
• DCA: 분할 매수 (Dollar Cost Averaging)  
• Pyramid: 피라미드 매수

🎯 사용법:
1. Analysis 탭에서 종목 선택
2. "Download & Auto Setup" 버튼으로 자동 설정
3. 투자 예산 확인/수정
4. 전략 선택 후 계산

✨ 새 기능: 자동 포트폴리오 설정
• 평단가 자동 설정 (현재가의 90%)
• 보유량 자동 설정 (1000주)
• 한국/미국 주식별 예산 조정

🎉 UI 개선: 4개 정보 패널
• 종목 정보 / 포지션 / 기술적 분석 / 매매 신호
• 차트 공간 확보로 더 나은 시각화

시작하려면 좌측 설정을 입력하고 Calculate를 누르세요!""")
            
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Investment tab creation")
    
    def create_crash_tab(self):
        """폭락장 대응 탭"""
        try:
            crash_frame = ttk.Frame(self.notebook)
            self.notebook.add(crash_frame, text="🚨 Crash Strategy")
            
            info_frame = ttk.LabelFrame(crash_frame, text="⚠️ 폭락장 대응 전략", padding="15")
            info_frame.pack(fill=tk.X, padx=15, pady=(15, 10))
            
            info_text = tk.Label(info_frame, 
                               text=f"📈 {APP_NAME} 폭락장 대응 시스템\n\n" +
                                    "레버리지 ETF와 고위험 종목의 폭락 상황에서 객관적 판단을 지원합니다.\n" +
                                    "🎯 새로운 기능: 10% 폭락 시 4가지 대응 전략 분석 포함\n" +
                                    "Analysis 탭에서 'Download & Auto Setup'으로 포트폴리오를 설정한 후 분석하세요.",
                               wraplength=1000, justify=tk.LEFT, font=('Segoe UI', 11))
            info_text.pack()
            
            main_container = tk.Frame(crash_frame)
            main_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
            
            control_panel = ttk.LabelFrame(main_container, text="🎯 Analysis Controls", padding="15")
            control_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
            
            tk.Button(control_panel, text="🚨 폭락 상황 분석", command=self.analyze_crash_situation).pack(fill=tk.X, pady=5)
            tk.Button(control_panel, text="✂️ 최적 손절가 계산", command=self.calculate_cutloss).pack(fill=tk.X, pady=5)
            tk.Button(control_panel, text="📋 AI 자문 리포트", command=self.generate_ai_report).pack(fill=tk.X, pady=5)
            
            ttk.Separator(control_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            tk.Label(control_panel, text="📊 Current Status:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W)
            self.crash_status = tk.Label(control_panel, text="종목을 선택해주세요.", wraplength=200)
            self.crash_status.pack(anchor=tk.W, pady=5)
            
            tk.Label(control_panel, text="🎯 Recommendation:", font=('Segoe UI', 11, 'bold')).pack(anchor=tk.W, pady=(10, 0))
            self.crash_recommendation = tk.Label(control_panel, text="분석 후 표시됩니다.", wraplength=200)
            self.crash_recommendation.pack(anchor=tk.W, pady=5)
            
            result_panel = ttk.LabelFrame(main_container, text="📊 Analysis Results", padding="15")
            result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            self.crash_results = scrolledtext.ScrolledText(result_panel, wrap=tk.WORD, font=('Consolas', 11))
            self.crash_results.pack(fill=tk.BOTH, expand=True)
            
            self.crash_results.insert('1.0', f"""🚨 {APP_NAME} Crash Strategy Advisor

폭락장에서 합리적 투자 결정을 위한 전문 분석 도구입니다.

💡 핵심 질문: "지금 손절해야 할까? 아니면 분할매수를 계속해야 할까?"

📊 제공 기능:
• 폭락 심각도 정량적 평가 (0-100점)
• 객관적 손절 vs 분할매수 판단
• 레버리지 ETF 특별 위험 관리
• AI 투자 자문용 상황 리포트

🎯 새로운 기능: 4가지 폭락 대응 전략 분석
• 전략 1: 추가 매수 (즉시 반등 시 최적)
• 전략 2: 100% 손절 (추가 하락 시 최적)
• 전략 3: 50% 손절 (중간 하락 시 적절)
• 전략 4: 25% 손절 (소폭 하락 시 보수적)

✨ 자동 포트폴리오 설정
• "Download & Auto Setup"으로 원클릭 설정
• 평단가 기반 정확한 손익 분석
• 개선된 자동 설정 (현재가의 90% 평단가)

🎉 UI 개선: 4개 정보 패널로 체계적 분석
• 종목 정보 / 포지션 / 기술적 분석 / 매매 신호 분리
• 차트 공간 확보로 더 나은 시각화

🎯 사용법:
1. Analysis 탭에서 "Download & Auto Setup" 클릭
2. 자동 설정된 포트폴리오 정보 확인/수정
3. 폭락 상황 분석 실행
4. 객관적 데이터 기반 투자 결정

⚡ 특히 레버리지 ETF (SOXL, TQQQ 등)는 특별 관리가 필요합니다!

시작하려면 왼쪽 분석 도구를 사용하세요.""")
            
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Crash tab creation")
    
    # 🎯 새로운 자동 설정 메서드
    def download_and_auto_setup(self):
        """다운로드 및 자동 포트폴리오 설정"""
        try:
            symbol = self.symbol_var.get().strip()
            if not symbol:
                messagebox.showwarning("⚠️", "종목 코드를 입력해주세요.")
                return
            
            # 한국 주식 코드 처리
            if symbol.isdigit():
                symbol = symbol.zfill(6)
                self.symbol_var.set(symbol)
            
            # 먼저 데이터 다운로드
            result = show_download_dialog(self.root, symbol, self.data_manager)
            
            if result and result['success']:
                # 다운로드 성공 시 자동 설정
                data = result['data']
                current_price = data['Close'].iloc[-1]
                
                # 🎯 평단가 자동 설정 (현재가의 90%)
                auto_avg_price = current_price * 0.9
                
                # 🎯 보유량 자동 설정 (기본 1000주)
                auto_position = 1000
                
                # 한국/미국 구분해서 설정
                is_korean = DataValidator.is_korean_stock(symbol)
                
                if is_korean:
                    # 한국 주식: 정수로 설정
                    self.avg_price_var.set(f"{auto_avg_price:.0f}")
                    # 한국 주식 예산도 자동 조정
                    self.budget_var.set("10000000")  # 1천만원
                else:
                    # 미국 주식: 소수점 포함
                    self.avg_price_var.set(f"{auto_avg_price:.2f}")
                    # 미국 주식 예산
                    self.budget_var.set("10000")  # 1만달러
                
                self.position_var.set(str(auto_position))
                
                # UI 업데이트
                self.refresh_files_list()
                self.update_stock_info(data, symbol)
                self.chart_manager.update_chart(data, symbol, auto_avg_price, self.get_company_name(symbol))
                
                # 성공 메시지
                company_name = self.get_company_name(symbol)
                if is_korean:
                    price_text = f"₩{current_price:,.0f}"
                    avg_price_text = f"₩{auto_avg_price:,.0f}"
                else:
                    price_text = f"${current_price:.2f}"
                    avg_price_text = f"${auto_avg_price:.2f}"
                
                success_msg = f"""✅ 자동 설정 완료!

📈 종목: {company_name} ({symbol})
💰 현재가: {price_text}
📊 평단가: {avg_price_text} (현재가의 90%)
📦 보유량: {auto_position:,}주

🎉 UI 개선사항:
• 4개 정보 패널로 깔끔한 정보 표시
• 차트 공간 확보로 더 나은 시각화
• 종목정보/포지션/기술분석/매매신호 분리

🎯 새로운 기능:
• 4가지 폭락 대응 전략 분석 가능
• 강화된 AI 자문 리포트 제공

이제 Investment 탭에서 투자 계산을 하거나
Crash Strategy 탭에서 위험 분석을 하세요!"""
                
                messagebox.showinfo("🎉 자동 설정 완료", success_msg)
                
            else:
                messagebox.showerror("❌", result['message'] if result else "다운로드 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Auto setup")
    
    # 기존 메서드들 (동일)
    def on_symbol_change(self, *args):
        """종목 변경 시 호출되는 콜백 함수"""
        try:
            new_symbol = self.symbol_var.get().strip()
            if new_symbol != self.current_symbol:
                self.current_symbol = new_symbol
                self.update_budget_for_market()
        except Exception as e:
            self.logger.error(f"Symbol change handling failed: {e}")
    
    def update_budget_for_market(self):
        """시장에 따라 예산 기본값 업데이트"""
        try:
            symbol = self.current_symbol
            if not symbol:
                return
            
            # 한국 주식 코드 처리
            if symbol.isdigit():
                symbol = symbol.zfill(6)
            
            is_korean = DataValidator.is_korean_stock(symbol)
            
            if is_korean:
                # 한국 주식: 1천만원 기본
                self.budget_var.set("10000000")
            else:
                # 미국 주식: 1만달러 기본
                self.budget_var.set("10000")
            
            self.logger.info(f"Budget updated for {'Korean' if is_korean else 'US'} stock: {symbol}")
            
        except Exception as e:
            self.logger.error(f"Budget update failed: {e}")
    
    def search_korean_stock(self):
        """한국 주식 검색"""
        try:
            code, name = show_korean_stock_search_dialog(self.root)
            if code:
                self.symbol_var.set(code)
                self.logger.info(f"Korean stock selected: {name} ({code})")
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Korean stock search")
    
    def select_stock(self, symbol):
        """주식 선택"""
        # 한국 주식 코드인 경우 6자리로 포맷
        if symbol.isdigit():
            symbol = symbol.zfill(6)
        self.symbol_var.set(symbol)
        self.logger.info(f"Stock selected: {symbol}")
    
    def download_data(self):
        """데이터 다운로드"""
        try:
            symbol = self.symbol_var.get().strip()
            if not symbol:
                messagebox.showwarning("⚠️", "종목 코드를 입력해주세요.")
                return
            
            # 한국 주식 코드 처리
            if symbol.isdigit():
                symbol = symbol.zfill(6)
                self.symbol_var.set(symbol)  # UI에도 반영
            
            result = show_download_dialog(self.root, symbol, self.data_manager)
            
            if result and result['success']:
                messagebox.showinfo("✅", result['message'])
                self.refresh_files_list()
                self.update_stock_info(result['data'], symbol)
                
                # 평단가가 입력되어 있으면 차트에 반영
                try:
                    avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                except:
                    avg_price = None
                
                company_name = self.get_company_name(symbol)
                self.chart_manager.update_chart(result['data'], symbol, avg_price, company_name)
            else:
                messagebox.showerror("❌", result['message'] if result else "다운로드 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Data download")
    
    def analyze_stock(self):
        """주식 분석 - 🎯 기술적 분석 결과 활용 강화"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            
            if data is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 다운로드해주세요.")
                return
            
            # 🎯 강화된 분석 실행
            analysis_result = self.analysis_engine.analyze_stock(data, symbol)
            
            if analysis_result:
                # Stock Information 업데이트 (기술적 분석 포함)
                self.update_stock_info(data, symbol, analysis_result)
                
                # 평단가 사용
                try:
                    avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                except:
                    avg_price = None
                
                company_name = self.get_company_name(symbol)
                self.chart_manager.update_chart(data, symbol, avg_price, company_name)
                
                # 🎯 분석 결과 요약 메시지
                success_msg = self._generate_analysis_summary(analysis_result, symbol)
                messagebox.showinfo("✅ 분석 완료", success_msg)
            else:
                messagebox.showerror("❌", "분석 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Stock analysis")
    
    def _generate_analysis_summary(self, analysis, symbol):
        """분석 결과 요약 생성"""
        try:
            company_name = self.get_company_name(symbol)
            summary = f"📊 {company_name} ({symbol}) 분석 완료!\n\n"
            
            # 매매 결정 요약
            if 'trading_decision' in analysis and analysis['trading_decision']:
                decision = analysis['trading_decision']
                decision_text = self._translate_decision(decision['decision'])
                confidence_text = self._translate_confidence(decision['confidence'])
                
                summary += f"🎯 매매 신호: {decision_text}\n"
                summary += f"📊 신뢰도: {confidence_text}\n"
                summary += f"💡 근거: {decision['reasoning']}\n\n"
            
            # 주요 지표 요약
            if 'recent_stats' in analysis and analysis['recent_stats']:
                stats = analysis['recent_stats']
                summary += f"📈 3일 평균 대비: {stats['diff_pct']:+.1f}%\n"
            
            if 'confidence_interval' in analysis and analysis['confidence_interval']:
                ci = analysis['confidence_interval']
                ci_signal_text = {
                    'POTENTIAL_BUY': '💚 매수 고려 구간',
                    'POTENTIAL_SELL': '🔴 매도 고려 구간',
                    'HOLD': '🟡 관망 구간'
                }.get(ci['signal'], '보합')
                summary += f"🎯 신뢰구간: {ci_signal_text}\n"
            
            if 'sp500_comparison' in analysis and analysis['sp500_comparison']:
                sp500 = analysis['sp500_comparison']
                if sp500['outperforming']:
                    summary += f"🏆 SP500 대비 +{sp500['relative_performance']:.1f}% 우수\n"
                else:
                    summary += f"📊 SP500 대비 {sp500['relative_performance']:.1f}% 부진\n"
            
            summary += "\n🎉 새로운 4개 패널로 정보가 깔끔하게 정리되었습니다!"
            return summary
            
        except Exception as e:
            self.logger.error(f"Analysis summary generation failed: {e}")
            return f"'{symbol}' 분석이 완료되었습니다!\n자세한 결과는 4개 정보 패널을 확인하세요."
    
    def calculate_investment(self):
        """투자 계산"""
        try:
            try:
                budget = float(self.budget_var.get())
                current_price = float(self.current_price_var.get()) if self.current_price_var.get() else None
                splits = int(self.splits_var.get())
            except ValueError:
                messagebox.showerror("❌", "올바른 숫자를 입력해주세요.")
                return
            
            if current_price is None:
                data = self.data_manager.get_current_data()
                if data is not None:
                    current_price = data['Close'].iloc[-1]
                    # 한국 주식인 경우 소수점 없이 표시
                    symbol = self.data_manager.get_current_symbol()
                    if DataValidator.is_korean_stock(symbol):
                        self.current_price_var.set(f"{current_price:.0f}")
                    else:
                        self.current_price_var.set(f"{current_price:.2f}")
                else:
                    messagebox.showwarning("⚠️", "현재가를 입력하거나 종목 데이터를 로드해주세요.")
                    return
            
            strategy = self.strategy_var.get()
            symbol = self.data_manager.get_current_symbol()
            
            if strategy == "single":
                result = self.investment_calculator.calculate_single_investment(budget, current_price)
            elif strategy == "dca":
                result = self.investment_calculator.calculate_dca_investment(budget, current_price, splits)
            elif strategy == "pyramid":
                drop_rate = 0.05
                result = self.investment_calculator.calculate_pyramid_investment(budget, current_price, splits, drop_rate)
            
            if result:
                report = self.investment_calculator.generate_investment_report(result, symbol or "Unknown")
                self.investment_results.delete('1.0', tk.END)
                self.investment_results.insert('1.0', report)
            else:
                messagebox.showerror("❌", "계산 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Investment calculation")
    
    def use_current_price(self):
        """현재가 사용"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            
            if data is not None:
                current_price = data['Close'].iloc[-1]
                
                # 한국/미국 구분해서 소수점 처리
                if DataValidator.is_korean_stock(symbol):
                    self.current_price_var.set(f"{current_price:.0f}")
                    messagebox.showinfo("✅", f"현재가 ₩{current_price:,.0f}이 입력되었습니다.")
                else:
                    self.current_price_var.set(f"{current_price:.2f}")
                    messagebox.showinfo("✅", f"현재가 ${current_price:.2f}이 입력되었습니다.")
            else:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Use current price")
    
    def assess_risk(self):
        """위험 평가"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            budget = float(self.budget_var.get()) if self.budget_var.get() else 10000
            
            if data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            risk_result = self.investment_calculator.assess_investment_risk(data, budget)
            
            if risk_result:
                # 한국/미국 구분해서 화폐 표시
                is_korean = DataValidator.is_korean_stock(symbol)
                if is_korean:
                    loss_text = f"₩{risk_result['estimated_loss_95']:,.0f}"
                else:
                    loss_text = f"${risk_result['estimated_loss_95']:,.0f}"
                
                risk_text = f"""📊 위험 평가 결과

위험 등급: {risk_result['risk_level']}
위험 점수: {risk_result['risk_score']:.1f}/100점

변동성: {risk_result['volatility']:.1f}%
VaR 95%: {risk_result['var_95']:.2f}%
최대 낙폭: {risk_result['max_drawdown']:.2f}%

추정 손실 (95%): {loss_text}

권장사항: {risk_result['recommendation']}"""
                
                messagebox.showinfo("📊 위험 평가", risk_text)
            else:
                messagebox.showerror("❌", "위험 평가 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Risk assessment")
    
    def analyze_crash_situation(self):
        """폭락 상황 분석"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            
            if data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 평단가 용어 사용
            try:
                avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
            except ValueError:
                avg_price = None
                position = 0
            
            crash_result = self.crash_analyzer.analyze_crash_situation(data, symbol, avg_price, position)
            
            if crash_result:
                severity = crash_result['severity']
                recommendation = crash_result['recommendation']
                risk_score = crash_result['risk_score']
                
                self.crash_status.config(text=f"위험점수: {risk_score:.0f}/100\n{severity['emoji']} {severity['description']}")
                self.crash_recommendation.config(text=recommendation['action'])
                
                # 한국/미국 구분해서 화폐 표시
                is_korean = DataValidator.is_korean_stock(symbol)
                if is_korean:
                    price_text = f"₩{crash_result['current_price']:,.0f}"
                else:
                    price_text = f"${crash_result['current_price']:.2f}"
                
                result_text = f"""🚨 {APP_NAME} 폭락장 분석 결과

{'=' * 50}
📊 분석 정보:
• 종목: {symbol}
• 현재가: {price_text}
• 위험 점수: {risk_score:.1f}/100점
• 심각도: {severity['emoji']} {severity['description']}

🎯 권장사항:
• 액션: {recommendation['action']}
• 상세: {recommendation['details']}
• 모니터링: {recommendation['monitoring']}

📊 분석 지표:
"""
                
                metrics = crash_result['crash_metrics']
                for key, value in metrics.items():
                    if isinstance(value, (int, float)):
                        result_text += f"• {key}: {value:.2f}\n"
                
                if crash_result['is_leverage_etf']:
                    result_text += "\n⚡ 레버리지 ETF 특별 경고:\n"
                    result_text += "• 즉시 15% 손절선 점검 필요\n"
                    result_text += "• 30일 이상 장기 보유 절대 금지\n"
                    result_text += "• 섹터 집중 위험 (반도체 업계 전반적 영향)\n"
                    result_text += "\n🚨 레버리지 ETF는 수학적 최적화보다 리스크 관리가 우선입니다!\n"
                
                result_text += f"""

{'=' * 70}
💡 투자 결정 가이드라인
{'=' * 70}

🤔 **어떤 전략을 선택해야 할까요?**

1. **정치·경제적 상황 분석**이 가장 중요합니다:
   • 현재 시장 전반적 상황 (금리, 정책, 경제지표)
   • 해당 섹터의 특별한 이슈나 호재/악재
   • 국제 정세 및 무역 분쟁 등의 영향

2. **개인 투자 성향**:
   • 리스크 감수 능력
   • 투자 기간 (단기 vs 장기)
   • 다른 투자처의 현금 필요성

3. **기술적 지표 확인**:
   • RSI, MACD 등 과매도/과매수 신호
   • 이동평균선 지지/저항 레벨
   • 거래량 패턴 분석

4. **객관적 판단 기준**:
   • 감정적 결정 배제
   • 미리 정한 손절선 준수
   • 분산투자를 통한 리스크 관리

💬 **AI 투자 자문 추천**: 
   현재 상황과 위 분석 결과를 AI에게 제공하여
   정치·경제적 상황을 종합한 전문 조언을 받아보세요!
   (Crash Strategy 탭의 'AI 자문 리포트' 버튼 이용)

📊 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                self.crash_results.delete('1.0', tk.END)
                self.crash_results.insert('1.0', result_text)
                
                # 상태 패널 업데이트
                if position > 0:
                    status_text = f"4가지 전략 분석 완료\n보유: {position:,.0f}주"
                    recommendation_text = "상황별 최적 전략\n확인 후 결정"
                else:
                    status_text = "기본 손절가 계산 완료\n포지션 정보 입력 필요"
                    recommendation_text = "평단가/보유량 입력 시\n4가지 전략 분석 가능"
                
                self.crash_status.config(text=status_text)
                self.crash_recommendation.config(text=recommendation_text)
                
            else:
                messagebox.showerror("❌", "손절가 계산 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Enhanced cutloss calculation")

    def calculate_cutloss(self):
        """🎯 강화된 손절가 계산 - 4가지 폭락 대응 전략 포함"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            
            if data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            current_price = data['Close'].iloc[-1]
            
            # 평단가와 포지션 정보 가져오기
            try:
                avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
                available_cash = 0  # 추가 현금은 일단 0으로 가정
            except ValueError:
                avg_price = None
                position = 0
                available_cash = 0
            
            # 🎯 새로운 4가지 전략 분석 기능 호출
            four_strategy_result = self.crash_analyzer.calculate_four_strategy_analysis(
                current_price, symbol, avg_price, position, available_cash
            )
            
            # 기존 손절가 계산도 포함
            cutloss_result = self.crash_analyzer.calculate_optimal_cutloss(current_price, symbol)
            
            if cutloss_result and four_strategy_result:
                # 한국/미국 구분
                is_korean = DataValidator.is_korean_stock(symbol)
                currency_symbol = "₩" if is_korean else "$"
                
                # 🎯 종합 결과 리포트 생성
                result_text = f"""✂️ {APP_NAME} 최적 손절가 계산 & 4가지 폭락 대응 전략

{'=' * 70}
📊 분석 정보:
• 종목: {symbol} ({cutloss_result['asset_type']})
• 현재가: {format_currency_auto(current_price, symbol)}
"""
                
                if avg_price and position > 0:
                    pnl = (current_price - avg_price) * position
                    pnl_pct = ((current_price - avg_price) / avg_price) * 100
                    result_text += f"• 평단가: {format_currency_auto(avg_price, symbol)}\n"
                    result_text += f"• 보유량: {position:,.0f}주\n"
                    result_text += f"• 평가손익: {format_currency_auto(pnl, symbol)} ({pnl_pct:+.2f}%)\n"
                
                result_text += f"\n📊 기본 권장 손절가:\n"
                
                for level in cutloss_result['cutloss_levels']:
                    price_text = format_currency_auto(level['price'], symbol)
                    result_text += f"• {level['level']}: {price_text} ({level['description']})\n"
                
                absolute_stop_text = format_currency_auto(cutloss_result['absolute_stop'], symbol)
                result_text += f"\n🚨 절대 손절선: {absolute_stop_text}\n"
                result_text += f"💡 권장사항: {cutloss_result['recommendation']}\n"
                
                # 🎯 새로운 4가지 전략 분석 결과 추가
                if position > 0:
                    crashed_price = four_strategy_result.get('crashed_price', current_price * 0.9)
                    strategies = four_strategy_result.get('strategies', {})
                    
                    result_text += f"""

{'=' * 70}
🔥 10% 폭락 시 4가지 대응 전략 분석
{'=' * 70}

📍 현재 상황:
• 현재가: {currency_symbol}{current_price:,.2f if not is_korean else current_price:,.0f}
• 10% 폭락 가격: {currency_symbol}{crashed_price:,.2f if not is_korean else crashed_price:,.0f}
• 보유 주식 수: {position:,.0f}주
• 폭락 후 평가액: {currency_symbol}{(position * crashed_price):,.2f if not is_korean else (position * crashed_price):,.0f}

💡 핵심 질문: "지금 바로 반등할까? 아니면 더 떨어질까?"
🤔 미래는 모르므로, 각 시나리오별 최적 전략을 비교 분석합니다.

"""
                    
                    # 전략 1: 추가 매수
                    if '1_additional_buy' in strategies:
                        strategy = strategies['1_additional_buy']
                        result_text += f"""📈 **전략 1: 추가 매수**
• 설명: {strategy['description']}
• 현재 보유: {strategy.get('current_shares', 0):,.0f}주
• 추가 매수: {strategy.get('additional_shares', 0):,.0f}주 (현금 부족으로 0주)
• 총 보유 예상: {strategy.get('total_shares', 0):,.0f}주
• 장점: 주가 반등 시 최대 수익, 평단가 하향 조정
• 단점: 추가 하락 시 손실 확대, 현금 소진
• 🎯 최적 시나리오: 즉시 반등

"""
                    
                    # 전략 2: 100% 손절
                    if '2_100_percent_cutloss' in strategies:
                        strategy = strategies['2_100_percent_cutloss']
                        scenarios = strategy.get('scenarios', [])
                        
                        result_text += f"""💰 **전략 2: 100% 손절 (전량 매도)**
• 설명: {strategy['description']}
• 손절 주식: {strategy.get('cutloss_shares', 0):,.0f}주
• 확보 현금: {currency_symbol}{strategy.get('cash_from_sale', 0):,.2f if not is_korean else strategy.get('cash_from_sale', 0):,.0f}
• 즉시 손실: {currency_symbol}{strategy.get('loss_amount', 0):,.2f if not is_korean else strategy.get('loss_amount', 0):,.0f} ({strategy.get('loss_pct', 0):.1f}%)

📊 **재매수 시나리오 (주요 구간):**"""
                        
                        # 주요 재매수 시나리오 표시
                        key_scenarios = [s for s in scenarios if s['additional_decline_pct'] in [20, 30, 50, 70]]
                        for scenario in key_scenarios:
                            result_text += f"""
• 추가 {scenario['additional_decline_pct']:.0f}% 하락 시: {scenario['buyable_shares']:,.0f}주 매수 가능 (원래의 {scenario['increase_ratio']:.1f}배)"""
                        
                        result_text += f"""
• 장점: 추가 하락 시 최대 주식 수 확보, 손실 확정으로 리스크 제거
• 단점: 주가 반등 시 기회 상실, 재진입 타이밍 어려움
• 🎯 최적 시나리오: 추가 20% 이상 하락

"""
                    
                    # 전략 3: 50% 손절
                    if '3_50_percent_cutloss' in strategies:
                        strategy = strategies['3_50_percent_cutloss']
                        scenarios = strategy.get('scenarios', [])
                        
                        result_text += f"""⚖️ **전략 3: 50% 손절 (절반 매도)**
• 설명: {strategy['description']}
• 손절 주식: {strategy.get('cutloss_shares', 0):,.0f}주
• 보유 주식: {strategy.get('remaining_shares', 0):,.0f}주
• 확보 현금: {currency_symbol}{strategy.get('cash_from_sale', 0):,.2f if not is_korean else strategy.get('cash_from_sale', 0):,.0f}
• 부분 손실: {currency_symbol}{strategy.get('loss_amount', 0):,.2f if not is_korean else strategy.get('loss_amount', 0):,.0f} ({strategy.get('loss_pct', 0):.1f}%)

📊 **재매수 후 총 보유 주식 (주요 구간):**"""
                        
                        key_scenarios = [s for s in scenarios if s['additional_decline_pct'] in [20, 30, 50, 70]]
                        for scenario in key_scenarios:
                            result_text += f"""
• 추가 {scenario['additional_decline_pct']:.0f}% 하락 시: {scenario['total_shares']:,.0f}주 총 보유 (원래의 {scenario['increase_ratio']:.1f}배)"""
                        
                        result_text += f"""
• 장점: 리스크 부분 제거, 주가 반등 시 일부 수익 확보
• 단점: 기회비용 발생, 복잡한 포지션 관리
• 🎯 최적 시나리오: 중간 정도 하락 또는 횡보

"""
                    
                    # 전략 4: 25% 손절
                    if '4_25_percent_cutloss' in strategies:
                        strategy = strategies['4_25_percent_cutloss']
                        scenarios = strategy.get('scenarios', [])
                        
                        result_text += f"""🛡️ **전략 4: 25% 손절 (1/4 매도)**
• 설명: {strategy['description']}
• 손절 주식: {strategy.get('cutloss_shares', 0):,.0f}주
• 보유 주식: {strategy.get('remaining_shares', 0):,.0f}주
• 확보 현금: {currency_symbol}{strategy.get('cash_from_sale', 0):,.2f if not is_korean else strategy.get('cash_from_sale', 0):,.0f}
• 최소 손실: {currency_symbol}{strategy.get('loss_amount', 0):,.2f if not is_korean else strategy.get('loss_amount', 0):,.0f} ({strategy.get('loss_pct', 0):.1f}%)

📊 **재매수 후 총 보유 주식 (주요 구간):**"""
                        
                        key_scenarios = [s for s in scenarios if s['additional_decline_pct'] in [20, 30, 50, 70]]
                        for scenario in key_scenarios:
                            result_text += f"""
• 추가 {scenario['additional_decline_pct']:.0f}% 하락 시: {scenario['total_shares']:,.0f}주 총 보유 (원래의 {scenario['increase_ratio']:.1f}배)"""
                        
                        result_text += f"""
• 장점: 최소 리스크 제거, 대부분 포지션 유지
• 단점: 제한적 리스크 해소, 추가 하락 시 제한적 대응
• 🎯 최적 시나리오: 소폭 하락 후 반등

"""
                    
                    # 전략별 기대 시나리오
                    scenarios_info = four_strategy_result.get('scenarios', {})
                    if scenarios_info:
                        result_text += f"""🎯 **시나리오별 최적 전략 요약:**

🚀 **즉시 반등 시나리오** (10% 폭락 후 바로 원래 가격 회복):
   → 최적 전략: {scenarios_info.get('immediate_recovery', {}).get('best_strategy', 'N/A')}
   → 이유: {scenarios_info.get('immediate_recovery', {}).get('reason', 'N/A')}

📉 **추가 20% 하락 시나리오** (총 28% 하락):
   → 최적 전략: {scenarios_info.get('continued_decline_20', {}).get('best_strategy', 'N/A')}
   → 이유: {scenarios_info.get('continued_decline_20', {}).get('reason', 'N/A')}

💥 **추가 50% 하락 시나리오** (총 55% 하락):
   → 최적 전략: {scenarios_info.get('continued_decline_50', {}).get('best_strategy', 'N/A')}
   → 이유: {scenarios_info.get('continued_decline_50', {}).get('reason', 'N/A')}

📊 **횡보 지속 시나리오** (10% 하락 후 계속 횡보):
   → 최적 전략: {scenarios_info.get('sideways', {}).get('best_strategy', 'N/A')}
   → 이유: {scenarios_info.get('sideways', {}).get('reason', 'N/A')}

"""
                else:
                    result_text += f"""

🔸 4가지 전략 분석을 위해서는 포지션 정보가 필요합니다.
   Analysis 탭에서 평단가와 보유량을 입력해주세요.
"""
                
                # 레버리지 ETF 특별 주의사항
                if cutloss_result['is_leverage']:
                    result_text += f"""

{'=' * 70}
⚡ 레버리지 ETF 특별 고려사항
{'=' * 70}
• 3배 레버리지로 인한 변동성 확대
• 일반 주식보다 엄격한 손절 기준 적용 (15% 절대 손절)
• 감정에 휘둘리지 말고 기계적 실행
• 30일 이상 장기 보유 절대 금지
• 시장 상황 악화 시 빠른 결단 필요

🎯 레버리지 ETF 투자자를 위한 특별 조언:
• 현재 시장이 기술주/반도체 섹터에 불리한 상황인지 파악
• VIX 지수, 금리 동향, 경제 지표를 더 민감하게 모니터링
• 일반 주식 대비 2-3배 빠른 의사결정 필요
• "조금 더 기다려보자"는 생각이 가장 위험
"""
                
                result_text += f"""

{'=' * 70}
🎯 실전 적용 가이드
{'=' * 70}

💡 **어떤 전략을 선택해야 할까요?**

🔍 **시장 분석이 우선**:
1. 현재 시장 전반적 상황 (금리, 정책, 경제지표)
2. 해당 섹터의 특별한 이슈나 호재/악재
3. 국제 정세 및 무역 분쟁 등의 영향
4. 기술적 지표 (RSI, MACD, 이동평균선)

🎯 **개인 상황 고려**:
1. 리스크 감수 능력
2. 투자 기간 (단기 vs 장기)
3. 다른 현금 필요성
4. 심리적 스트레스 정도

📊 **전략 선택 기준**:
• **즉시 반등 확신** → 전략 1 (추가 매수) 또는 전략 4 (25% 손절)
• **추가 하락 예상** → 전략 2 (100% 손절)
• **불확실성 높음** → 전략 3 (50% 손절)
• **레버리지 ETF** → 무조건 보수적 접근 (전략 2 또는 3)

⚠️ **주의사항**:
• 감정적 결정 절대 금지
• 미리 정한 손절선 기계적 준수
• 분산투자를 통한 리스크 관리
• 한 번 결정하면 중도 변경 금지

💬 **AI 자문 추천**: 
현재 상황과 위 분석 결과를 Claude 등 AI에게 제공하여
정치·경제적 상황을 종합한 전문 조언을 받아보세요!

📊 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
"""
                
                self.crash_results.delete('1.0', tk.END)
                self.crash_results.insert('1.0', result_text)
                
                # 상태 패널 업데이트
                if position > 0:
                    status_text = f"4가지 전략 분석 완료\n보유: {position:,.0f}주"
                    recommendation_text = "상황별 최적 전략\n확인 후 결정"
                else:
                    status_text = "기본 손절가 계산 완료\n포지션 정보 입력 필요"
                    recommendation_text = "평단가/보유량 입력 시\n4가지 전략 분석 가능"
                
                self.crash_status.config(text=status_text)
                self.crash_recommendation.config(text=recommendation_text)
                
            else:
                messagebox.showerror("❌", "손절가 계산 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Enhanced cutloss calculation")

    def generate_ai_report(self):
        """🎯 강화된 AI 자문 리포트 생성 - 4가지 전략 분석 및 기술적 분석 포함"""
        try:
            data = self.data_manager.get_current_data()
            symbol = self.data_manager.get_current_symbol()
            
            if data is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 평단가와 포지션 정보 가져오기
            try:
                avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
            except ValueError:
                avg_price = None
                position = 0
            
            # 폭락 상황 분석
            crash_result = self.crash_analyzer.analyze_crash_situation(data, symbol, avg_price, position)
            
            # 기술적 분석 수행
            technical_analysis = self.analysis_engine.analyze_stock(data, symbol)
            
            # 4가지 전략 분석 (포지션이 있는 경우)
            four_strategy_result = None
            if position > 0:
                current_price = data['Close'].iloc[-1]
                four_strategy_result = self.crash_analyzer.calculate_four_strategy_analysis(
                    current_price, symbol, avg_price, position, 0  # 추가 현금은 0으로 가정
                )
            
            if crash_result:
                # 🎯 강화된 종합 AI 자문 리포트 생성
                report = self.crash_analyzer.generate_comprehensive_ai_report(
                    crash_result, 
                    technical_analysis, 
                    {'avg_price': avg_price, 'position': position},
                    four_strategy_result
                )
                
                # 리포트 표시 창 생성
                report_window = tk.Toplevel(self.root)
                report_window.title("📋 종합 AI 자문용 리포트 (4가지 전략 포함)")
                report_window.geometry("1000x700")
                report_window.transient(self.root)
                
                main_frame = tk.Frame(report_window, padx=20, pady=20)
                main_frame.pack(fill=tk.BOTH, expand=True)
                
                # 제목 및 안내
                title_frame = tk.Frame(main_frame)
                title_frame.pack(fill=tk.X, pady=(0, 15))
                
                tk.Label(title_frame, 
                        text="📋 종합 AI 투자 자문용 리포트", 
                        font=('Segoe UI', 16, 'bold')).pack(side=tk.LEFT)
                
                tk.Label(title_frame, 
                        text=f"v{APP_VERSION}", 
                        font=('Segoe UI', 10), foreground='gray').pack(side=tk.RIGHT)
                
                # 설명
                desc_text = """아래 종합 리포트를 AI에게 제공하여 전문적인 투자 자문을 받으세요.
🎯 새로운 기능: 10% 폭락 시 4가지 대응 전략 분석 포함
📊 강화된 기능: 기술적 분석, 포트폴리오 분석, 위험도 평가 통합"""
                
                tk.Label(main_frame, text=desc_text, 
                        font=('Segoe UI', 11), wraplength=900).pack(pady=(0, 15))
                
                # 리포트 텍스트 영역
                text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                      font=('Consolas', 9))
                text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
                text_widget.insert('1.0', report)
                
                # 버튼 프레임
                button_frame = tk.Frame(main_frame)
                button_frame.pack(fill=tk.X)
                
                def copy_report():
                    try:
                        self.root.clipboard_clear()
                        self.root.clipboard_append(report)
                        messagebox.showinfo("✅", "종합 리포트가 클립보드에 복사되었습니다!\n\nAI에게 현재 시장 상황을 고려한 전문 투자 자문을 요청하세요.")
                    except Exception as e:
                        messagebox.showerror("❌", f"복사 실패: {e}")
                
                def save_report():
                    try:
                        from tkinter import filedialog
                        filename = filedialog.asksaveasfilename(
                            defaultextension=".txt",
                            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
                            initialname=f"{symbol}_AI_Advisory_Report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
                        )
                        if filename:
                            with open(filename, 'w', encoding='utf-8') as f:
                                f.write(report)
                            messagebox.showinfo("✅", f"리포트가 저장되었습니다:\n{filename}")
                    except Exception as e:
                        messagebox.showerror("❌", f"저장 실패: {e}")
                
                # 버튼들
                tk.Button(button_frame, text="📋 클립보드에 복사", 
                         command=copy_report, font=('Segoe UI', 11, 'bold'),
                         bg='#4CAF50', fg='white').pack(side=tk.LEFT, padx=(0, 10))
                
                tk.Button(button_frame, text="💾 파일로 저장", 
                         command=save_report, font=('Segoe UI', 11)).pack(side=tk.LEFT, padx=(0, 10))
                
                tk.Button(button_frame, text="❌ 닫기", 
                         command=report_window.destroy, font=('Segoe UI', 11)).pack(side=tk.RIGHT)
                
                # 추가 안내
                info_frame = tk.Frame(main_frame)
                info_frame.pack(fill=tk.X, pady=(10, 0))
                
                info_text = """💡 사용 팁: 
• 리포트를 Claude, ChatGPT 등 AI에게 제공하여 현재 정치·경제적 상황을 고려한 투자 조언 요청
• 특히 4가지 전략 중 어떤 것이 현재 시장 상황에 가장 적합한지 문의
• 감정적 판단을 배제한 객관적이고 실행 가능한 구체적 조언 요청"""
                
                tk.Label(info_frame, text=info_text, 
                        font=('Segoe UI', 9), foreground='#666666', 
                        wraplength=900, justify=tk.LEFT).pack()
                
            else:
                messagebox.showerror("❌", "리포트 생성 실패")
                
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Enhanced AI report generation")
    
    # 🎯 새로운 4패널 업데이트 메서드들
    def update_stock_info(self, data, symbol, analysis=None):
        """🎯 주식 정보 업데이트 - 4개 패널로 분리"""
        try:
            if data is None or data.empty:
                self._clear_all_info_panels()
                return
            
            company_name = self.get_company_name(symbol)
            latest_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
            change = latest_price - prev_price
            change_pct = (change / prev_price) * 100 if prev_price != 0 else 0
            
            # 한국/미국 구분해서 화폐 표시
            is_korean = DataValidator.is_korean_stock(symbol)
            
            # 🎯 1. 종목 정보 패널 업데이트
            self._update_stock_info_panel(company_name, symbol, latest_price, change, change_pct, len(data), is_korean)
            
            # 🎯 2. 포지션 정보 패널 업데이트
            self._update_position_info_panel(latest_price, is_korean)
            
            # 🎯 3. 기술적 분석 및 매매 신호 패널 업데이트
            if analysis is None:
                # 분석이 제공되지 않은 경우 새로 실행
                analysis = self.analysis_engine.analyze_stock(data, symbol)
            
            if analysis:
                self._update_technical_info_panel(analysis, is_korean)
                self._update_signal_info_panel(analysis)
            else:
                self.technical_info_label.config(text="분석 실패")
                self.signal_info_label.config(text="신호 없음")
            
        except Exception as e:
            self.logger.error(f"Stock info update failed: {e}")
    
    def _clear_all_info_panels(self):
        """모든 정보 패널 초기화"""
        self.stock_info_label.config(text="데이터가 없습니다.")
        self.position_info_label.config(text="포지션 없음")
        self.technical_info_label.config(text="분석 대기중")
        self.signal_info_label.config(text="신호 없음")
    
    def _update_stock_info_panel(self, company_name, symbol, latest_price, change, change_pct, data_days, is_korean):
        """1. 종목 정보 패널 업데이트"""
        try:
            info_text = f"{company_name}\n({symbol})\n\n"
            
            if is_korean:
                info_text += f"현재가: ₩{latest_price:,.0f}\n"
                info_text += f"변동: ₩{change:+,.0f}\n"
                info_text += f"변동률: {change_pct:+.2f}%\n"
            else:
                info_text += f"현재가: ${latest_price:.2f}\n"
                info_text += f"변동: ${change:+.2f}\n"
                info_text += f"변동률: {change_pct:+.2f}%\n"
            
            info_text += f"데이터: {data_days}일"
            
            self.stock_info_label.config(text=info_text)
            
        except Exception as e:
            self.logger.error(f"Stock info panel update failed: {e}")
    
    def _update_position_info_panel(self, latest_price, is_korean):
        """2. 포지션 정보 패널 업데이트"""
        try:
            try:
                avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
            except ValueError:
                avg_price = None
                position = 0
            
            if avg_price and position > 0:
                pnl = (latest_price - avg_price) * position
                pnl_pct = ((latest_price - avg_price) / avg_price) * 100
                
                if is_korean:
                    position_text = f"평단가:\n₩{avg_price:,.0f}\n\n"
                    position_text += f"보유량:\n{position:,.0f}주\n\n"
                    position_text += f"평가손익:\n₩{pnl:+,.0f}\n"
                    position_text += f"({pnl_pct:+.2f}%)"
                else:
                    position_text = f"평단가:\n${avg_price:.2f}\n\n"
                    position_text += f"보유량:\n{position:,.0f}주\n\n"
                    position_text += f"평가손익:\n${pnl:+,.2f}\n"
                    position_text += f"({pnl_pct:+.2f}%)"
                
                self.position_info_label.config(text=position_text)
            else:
                self.position_info_label.config(text="포지션 정보를\n입력해주세요")
                
        except Exception as e:
            self.logger.error(f"Position info panel update failed: {e}")
    
    def _update_technical_info_panel(self, analysis, is_korean):
        """3. 기술적 분석 패널 업데이트"""
        try:
            tech_text = ""
            
            # 최근 3일 평균가 정보
            if 'recent_stats' in analysis and analysis['recent_stats']:
                stats = analysis['recent_stats']
                avg_3_days = stats['avg_3_days']
                diff_pct = stats['diff_pct']
                
                if is_korean:
                    tech_text += f"3일평균:\n₩{avg_3_days:,.0f}\n"
                else:
                    tech_text += f"3일평균:\n${avg_3_days:.2f}\n"
                
                tech_text += f"({diff_pct:+.1f}%)\n\n"
            
            # 95% 신뢰구간 정보
            if 'confidence_interval' in analysis and analysis['confidence_interval']:
                ci = analysis['confidence_interval']
                
                if is_korean:
                    tech_text += f"신뢰구간:\n₩{ci['lower_bound']:,.0f}~\n₩{ci['upper_bound']:,.0f}\n\n"
                else:
                    tech_text += f"신뢰구간:\n${ci['lower_bound']:.2f}~\n${ci['upper_bound']:.2f}\n\n"
                
                # 포지션 신호
                if ci['signal'] == 'POTENTIAL_BUY':
                    tech_text += "💚 매수고려구간"
                elif ci['signal'] == 'POTENTIAL_SELL':
                    tech_text += "🔴 매도고려구간"
                else:
                    tech_text += "🟡 관망구간"
            
            # SP500 비교 정보
            if 'sp500_comparison' in analysis and analysis['sp500_comparison']:
                sp500 = analysis['sp500_comparison']
                relative_perf = sp500['relative_performance']
                
                tech_text += f"\n\nSP500대비:\n"
                if sp500['outperforming']:
                    tech_text += f"🎯 +{relative_perf:.1f}% 우수"
                else:
                    tech_text += f"📊 {relative_perf:.1f}% 부진"
            
            if not tech_text:
                tech_text = "분석 데이터\n부족"
            
            self.technical_info_label.config(text=tech_text)
            
        except Exception as e:
            self.logger.error(f"Technical info panel update failed: {e}")
            self.technical_info_label.config(text="분석 오류")
    
    def _update_signal_info_panel(self, analysis):
        """4. 매매 신호 패널 업데이트"""
        try:
            signal_text = ""
            
            # 매매 결정 정보
            if 'trading_decision' in analysis and analysis['trading_decision']:
                decision = analysis['trading_decision']
                
                decision_text = self._translate_decision(decision['decision'])
                confidence_text = self._translate_confidence(decision['confidence'])
                
                signal_text += f"{decision_text}\n\n"
                signal_text += f"신뢰도: {confidence_text}\n\n"
                signal_text += f"근거:\n{decision['reasoning']}"
                
                # RSI 추가 정보
                if 'technical_indicators' in analysis and 'rsi' in analysis['technical_indicators']:
                    rsi = analysis['technical_indicators']['rsi']
                    signal_text += f"\n\nRSI: {rsi:.1f}"
                    
                    if rsi < 30:
                        signal_text += "\n(과매도)"
                    elif rsi > 70:
                        signal_text += "\n(과매수)"
                    else:
                        signal_text += "\n(중립)"
            else:
                signal_text = "매매신호\n분석중"
            
            self.signal_info_label.config(text=signal_text)
            
        except Exception as e:
            self.logger.error(f"Signal info panel update failed: {e}")
            self.signal_info_label.config(text="신호 오류")
    
    def _translate_decision(self, decision):
        """매매 결정 번역"""
        translations = {
            'STRONG_BUY': '🚀 적극매수',
            'BUY': '💚 매수',
            'HOLD': '🟡 보유',
            'SELL': '🔴 매도',
            'STRONG_SELL': '💥 적극매도'
        }
        return translations.get(decision, decision)
    
    def _translate_confidence(self, confidence):
        """신뢰도 번역"""
        translations = {
            'HIGH': '높음',
            'MEDIUM': '보통',
            'LOW': '낮음'
        }
        return translations.get(confidence, confidence)
    
    # 유틸리티 메서드들
    def refresh_files_list(self):
        """파일 목록 새로고침"""
        try:
            self.files_listbox.delete(0, tk.END)
            file_list = self.data_manager.get_file_list()
            for file_info in file_list:
                self.files_listbox.insert(tk.END, file_info['display_info'])
        except Exception as e:
            self.logger.error(f"Files list refresh failed: {e}")
    
    def load_selected_file(self, event):
        """선택된 파일 로드"""
        try:
            selection = self.files_listbox.curselection()
            if not selection:
                return
            
            file_list = self.data_manager.get_file_list()
            if selection[0] < len(file_list):
                file_info = file_list[selection[0]]
                result = self.data_manager.load_stock_data(file_info['filepath'])
                
                if result['success']:
                    self.symbol_var.set(file_info['symbol'])
                    self.update_stock_info(result['data'], file_info['symbol'])
                    
                    # 평단가가 설정되어 있으면 차트에 반영
                    try:
                        avg_price = float(self.avg_price_var.get()) if self.avg_price_var.get() else None
                    except:
                        avg_price = None
                    
                    self.chart_manager.update_chart(result['data'], file_info['symbol'], avg_price)
                    self.logger.info(f"File loaded: {file_info['filename']}")
                else:
                    messagebox.showerror("❌", result['message'])
                    
        except Exception as e:
            self.error_handler.handle_exception(e, True, "File loading")
    
    def get_company_name(self, symbol):
        """회사명 가져오기"""
        try:
            # 한국 주식 코드 처리
            if symbol.isdigit():
                symbol = symbol.zfill(6)
                return self.korean_manager.get_company_name(symbol)
            else:
                return symbol
        except:
            return symbol
    
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except Exception as e:
            self.error_handler.handle_exception(e, True, "Application execution")

if __name__ == "__main__":
    try:
        app = BosPlanApp()
        app.run()
    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()