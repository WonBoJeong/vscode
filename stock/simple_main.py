#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
🚀 VStock Advanced - 주식 분석 프로그램 (간단 테스트 버전)
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import os
from pathlib import Path

class SimpleStockAnalyzer:
    def __init__(self):
        """간단한 주식 분석기 초기화"""
        self.root = tk.Tk()
        self.setup_window()
        self.current_data = None
        self.create_widgets()
        
    def setup_window(self):
        """윈도우 설정"""
        self.root.title("📈 VStock Advanced - 주식 분석 시스템")
        self.root.geometry("1200x800")
        self.root.minsize(800, 600)
        
        # 화면 중앙 배치
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")
        
    def create_widgets(self):
        """GUI 위젯 생성"""
        # 메인 프레임
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 헤더
        header_frame = ttk.LabelFrame(main_frame, text="📈 VStock Advanced", padding="20")
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        # 제목
        title_label = ttk.Label(header_frame, text="고급 주식 분석 시스템", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack()
        
        # 검색 프레임
        search_frame = ttk.Frame(header_frame)
        search_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Label(search_frame, text="종목 코드:", font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.symbol_var = tk.StringVar()
        self.symbol_entry = ttk.Entry(search_frame, textvariable=self.symbol_var, 
                                     font=('Segoe UI', 12), width=10)
        self.symbol_entry.pack(side=tk.LEFT, padx=(10, 5))
        self.symbol_entry.bind('<Return>', lambda e: self.analyze_stock())
        
        # 분석 버튼
        analyze_btn = ttk.Button(search_frame, text="🔍 분석", command=self.analyze_stock)
        analyze_btn.pack(side=tk.LEFT, padx=5)
        
        # 빠른 선택 버튼들
        quick_frame = ttk.Frame(search_frame)
        quick_frame.pack(side=tk.LEFT, padx=(20, 0))
        
        for symbol in ["AAPL", "TSLA", "MSFT", "GOOGL", "PLTR"]:
            btn = ttk.Button(quick_frame, text=symbol, width=8,
                           command=lambda s=symbol: self.quick_analyze(s))
            btn.pack(side=tk.LEFT, padx=2)
        
        # 메인 콘텐츠 프레임
        content_frame = ttk.PanedWindow(main_frame, orient=tk.HORIZONTAL)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # 왼쪽 패널 (차트)
        self.left_panel = ttk.LabelFrame(content_frame, text="📊 주식 차트", padding="10")
        content_frame.add(self.left_panel, weight=3)
        
        # 오른쪽 패널 (정보)
        self.right_panel = ttk.LabelFrame(content_frame, text="📋 종목 정보", padding="10")
        content_frame.add(self.right_panel, weight=1)
        
        # 초기 메시지
        self.show_initial_message()
        self.create_info_panel()
        
        # 상태바
        self.status_bar = ttk.Label(main_frame, text="준비", 
                                   relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        
    def show_initial_message(self):
        """초기 메시지 표시"""
        welcome_label = ttk.Label(self.left_panel, 
                                 text="📈 종목 코드를 입력하고 분석 버튼을 눌러주세요!\n\n샘플 종목: AAPL, TSLA, MSFT, GOOGL, PLTR", 
                                 font=('Segoe UI', 14), 
                                 justify=tk.CENTER)
        welcome_label.pack(expand=True)
        
    def create_info_panel(self):
        """정보 패널 생성"""
        # 종목 정보 표시 영역
        self.info_frame = ttk.Frame(self.right_panel)
        self.info_frame.pack(fill=tk.BOTH, expand=True)
        
        # 기본 정보 레이블들
        self.info_labels = {}
        info_fields = [
            ("symbol", "종목 코드"),
            ("price", "현재가"),
            ("change", "전일 대비"),
            ("change_percent", "변동률"),
            ("volume", "거래량"),
            ("high", "고가"),
            ("low", "저가")
        ]
        
        for field, label_text in info_fields:
            frame = ttk.Frame(self.info_frame)
            frame.pack(fill=tk.X, pady=5)
            
            ttk.Label(frame, text=f"{label_text}:", 
                     font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT)
            self.info_labels[field] = ttk.Label(frame, text="-", 
                                               font=('Segoe UI', 10))
            self.info_labels[field].pack(side=tk.RIGHT)
            
    def load_stock_data(self, symbol):
        """주식 데이터 로드"""
        try:
            # 현재 프로그램 경로에서 data 폴더 찾기
            current_dir = Path(__file__).parent
            data_folder = current_dir / "data"
            
            # 파일 경로들 시도
            possible_files = [
                data_folder / f"{symbol}.csv",
                data_folder / f"{symbol}_data.csv",
                data_folder / f"{symbol}.xlsx"
            ]
            
            data_file = None
            for file_path in possible_files:
                if file_path.exists():
                    data_file = file_path
                    break
                    
            if data_file is None:
                return None
                
            # 파일 로드
            if data_file.suffix == '.csv':
                data = pd.read_csv(data_file, index_col=0, parse_dates=True)
            else:
                data = pd.read_excel(data_file, index_col=0, parse_dates=True)
                
            return data
            
        except Exception as e:
            print(f"데이터 로드 오류: {e}")
            return None
            
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
            
        self.status_bar.config(text=f"{symbol} 분석 중...")
        self.root.update()
        
        try:
            # 데이터 로드
            data = self.load_stock_data(symbol)
            if data is None or data.empty:
                messagebox.showerror("오류", f"{symbol} 데이터를 찾을 수 없습니다.\n\n사용 가능한 종목: AAPL, TSLA, MSFT, GOOGL, PLTR")
                self.status_bar.config(text="분석 실패")
                return
                
            self.current_data = data
            
            # 차트 생성
            self.create_chart(symbol, data)
            
            # 정보 업데이트
            self.update_stock_info(symbol, data)
            
            self.status_bar.config(text=f"{symbol} 분석 완료 - {len(data)}일 데이터")
            
        except Exception as e:
            messagebox.showerror("오류", f"분석 중 오류 발생:\n{e}")
            self.status_bar.config(text="분석 실패")
            
    def create_chart(self, symbol, data):
        """차트 생성"""
        # 기존 위젯 제거
        for widget in self.left_panel.winfo_children():
            widget.destroy()
            
        # Figure 생성
        fig = Figure(figsize=(10, 6), facecolor='white')
        
        # 서브플롯 생성
        ax1 = fig.add_subplot(2, 1, 1)  # 가격 차트
        ax2 = fig.add_subplot(2, 1, 2)  # 거래량 차트
        
        # 가격 차트
        ax1.plot(data.index, data['Close'], color='#2563eb', linewidth=2, label='종가')
        ax1.set_title(f'{symbol} - 주가 차트', fontsize=14, fontweight='bold')
        ax1.set_ylabel('가격 ($)', fontsize=12)
        ax1.grid(True, alpha=0.3)
        ax1.legend()
        
        # 이동평균선 추가
        if len(data) > 20:
            ma20 = data['Close'].rolling(window=20).mean()
            ax1.plot(data.index, ma20, color='#f59e0b', linewidth=1, label='MA20', alpha=0.8)
            
        if len(data) > 50:
            ma50 = data['Close'].rolling(window=50).mean()
            ax1.plot(data.index, ma50, color='#ef4444', linewidth=1, label='MA50', alpha=0.8)
            
        ax1.legend()
        
        # 거래량 차트
        colors = ['#16a34a' if close >= open_price else '#ef4444' 
                 for close, open_price in zip(data['Close'], data['Open'])]
        ax2.bar(data.index, data['Volume'], color=colors, alpha=0.6, width=1)
        ax2.set_title('거래량', fontsize=12)
        ax2.set_ylabel('거래량', fontsize=10)
        ax2.grid(True, alpha=0.3)
        
        # 레이아웃 조정
        fig.tight_layout()
        
        # Canvas 생성 및 추가
        canvas = FigureCanvasTkAgg(fig, self.left_panel)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
    def update_stock_info(self, symbol, data):
        """종목 정보 업데이트"""
        try:
            if data.empty:
                return
                
            latest = data.iloc[-1]
            prev = data.iloc[-2] if len(data) > 1 else latest
            
            change = latest['Close'] - prev['Close']
            change_percent = (change / prev['Close']) * 100
            
            # 정보 업데이트
            info_data = {
                'symbol': symbol,
                'price': f"${latest['Close']:.2f}",
                'change': f"${change:+.2f}",
                'change_percent': f"{change_percent:+.2f}%",
                'volume': f"{latest['Volume']:,}",
                'high': f"${latest['High']:.2f}",
                'low': f"${latest['Low']:.2f}"
            }
            
            for field, value in info_data.items():
                if field in self.info_labels:
                    self.info_labels[field].config(text=value)
                    
            # 변동률에 따른 색상 변경
            color = 'green' if change >= 0 else 'red'
            self.info_labels['change'].config(foreground=color)
            self.info_labels['change_percent'].config(foreground=color)
            
        except Exception as e:
            print(f"정보 업데이트 오류: {e}")
            
    def run(self):
        """애플리케이션 실행"""
        try:
            self.root.mainloop()
        except Exception as e:
            print(f"애플리케이션 실행 오류: {e}")
            messagebox.showerror("오류", f"프로그램 오류: {e}")

def main():
    """메인 함수"""
    try:
        print("🚀 VStock Advanced 시작...")
        app = SimpleStockAnalyzer()
        app.run()
    except Exception as e:
        print(f"프로그램 시작 실패: {e}")
        messagebox.showerror("오류", f"프로그램 시작 실패: {e}")

if __name__ == "__main__":
    main()