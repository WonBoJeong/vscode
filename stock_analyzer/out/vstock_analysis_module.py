#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Analysis Module - 주식 분석 기능
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import yfinance as yf
from pathlib import Path
from datetime import datetime, timedelta
import os

class AnalysisModule:
    """주식 분석 모듈"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.shared_data = main_app.shared_data
        
        # UI 요소들 (나중에 설정됨)
        self.symbol_var = None
        self.entry_price_var = None
        self.position_var = None
        self.files_listbox = None
        self.info_label = None
        self.chart_canvas = None
        self.chart_frame = None
    
    def create_tab(self, notebook):
        """분석 탭 생성"""
        try:
            analysis_frame = ttk.Frame(notebook)
            notebook.add(analysis_frame, text="📊 Analysis")
            
            # 좌측 패널 (입력 및 컨트롤)
            left_panel = ttk.LabelFrame(analysis_frame, text="🔍 Stock Selection", padding="15")
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 15))
            
            # 주식 선택
            ttk.Label(left_panel, text="Symbol/Code:", style='Info.TLabel').pack(anchor=tk.W)
            ttk.Label(left_panel, text="(US: AAPL, SOXL / KR: 005930)", 
                     style='Info.TLabel', foreground='gray').pack(anchor=tk.W)
            self.symbol_var = tk.StringVar()
            symbol_entry = ttk.Entry(left_panel, textvariable=self.symbol_var, width=18)
            symbol_entry.pack(fill=tk.X, pady=(5, 15))
            symbol_entry.bind('<Return>', lambda e: self.download_data())
            
            # 빠른 선택 버튼들
            quick_frame = ttk.LabelFrame(left_panel, text="Quick Select", padding="10")
            quick_frame.pack(fill=tk.X, pady=(0, 15))
            
            # 인기 종목 (메인 앱에서 가져오기)
            popular_label = ttk.Label(quick_frame, text="인기 종목:", style='Info.TLabel')
            popular_label.pack(anchor=tk.W)
            
            # 메인 앱의 설정에서 인기 종목 가져오기
            popular_symbols = getattr(self.main_app, 'popular_stocks', 
                ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX", "IONQ"])
            
            for i, symbol in enumerate(popular_symbols[:9]):  # 최대 9개
                if i % 3 == 0:
                    row_frame = tk.Frame(quick_frame)
                    row_frame.pack(fill=tk.X, pady=2)
                
                btn = tk.Button(row_frame, text=symbol, width=6, 
                               command=lambda s=symbol: self.symbol_var.set(s))
                btn.pack(side=tk.LEFT, padx=2)
            
            # 내 종목
            my_label = ttk.Label(quick_frame, text="내 종목:", style='Info.TLabel')
            my_label.pack(anchor=tk.W, pady=(10, 0))
            
            # 메인 앱의 설정에서 내 종목 가져오기
            my_symbols = getattr(self.main_app, 'my_stocks', 
                ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI", "JEPQ", "TSLL"])
            
            for i, symbol in enumerate(my_symbols[:9]):  # 최대 9개
                if i % 3 == 0:
                    row_frame = tk.Frame(quick_frame)
                    row_frame.pack(fill=tk.X, pady=2)
                
                btn = tk.Button(row_frame, text=symbol, width=6,
                               command=lambda s=symbol: self.symbol_var.set(s))
                btn.pack(side=tk.LEFT, padx=2)
            
            # 추가 정보 입력
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            ttk.Label(left_panel, text="📊 Portfolio Information:", style='Subtitle.TLabel').pack(anchor=tk.W)
            
            ttk.Label(left_panel, text="Entry Price:", style='Info.TLabel').pack(anchor=tk.W)
            self.entry_price_var = tk.StringVar()
            entry_price_entry = ttk.Entry(left_panel, textvariable=self.entry_price_var, width=18)
            entry_price_entry.pack(fill=tk.X, pady=(2, 10))
            
            ttk.Label(left_panel, text="Position Size:", style='Info.TLabel').pack(anchor=tk.W)
            self.position_var = tk.StringVar(value="0")
            position_entry = ttk.Entry(left_panel, textvariable=self.position_var, width=18)
            position_entry.pack(fill=tk.X, pady=(2, 15))
            
            # 버튼들
            ttk.Button(left_panel, text="📥 Download Data", 
                      command=self.download_data).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="📈 Analyze", 
                      command=self.analyze_stock).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="🔄 Refresh Files", 
                      command=self.refresh_files_list).pack(fill=tk.X, pady=3, ipady=5)
            ttk.Button(left_panel, text="🗂️ File Management", 
                      command=self.show_file_management).pack(fill=tk.X, pady=3, ipady=5)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # 파일 리스트
            ttk.Label(left_panel, text="📁 Data Files:", style='Info.TLabel').pack(anchor=tk.W)
            
            listbox_frame = tk.Frame(left_panel)
            listbox_frame.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
            
            self.files_listbox = tk.Listbox(listbox_frame, height=12)
            files_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                                          command=self.files_listbox.yview)
            self.files_listbox.configure(yscrollcommand=files_scrollbar.set)
            
            self.files_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            files_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            self.files_listbox.bind('<Double-Button-1>', self.load_selected_file)
            
            # 우측 패널 (차트 및 결과)
            right_panel = ttk.Frame(analysis_frame)
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 정보 패널
            info_panel = ttk.LabelFrame(right_panel, text="📋 Stock Information", padding="15")
            info_panel.pack(fill=tk.X, pady=(0, 15))
            
            self.info_label = ttk.Label(info_panel, text="주식을 선택하고 분석해주세요.", 
                                       style='Info.TLabel')
            self.info_label.pack(anchor=tk.W)
            
            # 차트 패널
            self.chart_frame = ttk.LabelFrame(right_panel, text="📈 Chart", padding="15")
            self.chart_frame.pack(fill=tk.BOTH, expand=True)
            
            # 초기 차트 설정
            self.setup_chart()
            
            # 파일 목록 새로고침
            self.refresh_files_list()
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def setup_chart(self):
        """차트 설정"""
        try:
            # Matplotlib 설정
            plt.rcParams['figure.facecolor'] = 'white'
            plt.rcParams['axes.facecolor'] = 'white'
            
            # 초기 빈 차트
            self.fig, self.ax = plt.subplots(figsize=(10, 6))
            self.ax.text(0.5, 0.5, 'Select a stock and download data to see chart', 
                        ha='center', va='center', transform=self.ax.transAxes, 
                        fontsize=14, color='gray')
            self.ax.set_xticks([])
            self.ax.set_yticks([])
            
            # 캔버스 생성
            self.chart_canvas = FigureCanvasTkAgg(self.fig, self.chart_frame)
            self.chart_canvas.draw()
            self.chart_canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
        except Exception as e:
            self.main_app.log_error(f"차트 설정 실패: {e}")
    
    def download_data(self):
        """데이터 다운로드"""
        try:
            symbol = self.symbol_var.get().strip().upper()
            if not symbol:
                messagebox.showwarning("⚠️", "종목 코드를 입력해주세요.")
                return
            
            self.main_app.log_info(f"데이터 다운로드 시작: {symbol}")
            
            # 진행상황 표시
            progress_window = tk.Toplevel(self.main_app.root)
            progress_window.title("데이터 다운로드 중...")
            progress_window.geometry("400x100")
            progress_window.transient(self.main_app.root)
            progress_window.grab_set()
            
            progress_label = ttk.Label(progress_window, text=f"Downloading {symbol} data...")
            progress_label.pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=20, fill=tk.X)
            progress_bar.start()
            
            progress_window.update()
            
            try:
                # Yahoo Finance에서 데이터 다운로드
                # 한국 주식인 경우 .KS 추가
                if symbol.isdigit() and len(symbol) == 6:
                    download_symbol = f"{symbol}.KS"
                    is_korean = True
                else:
                    download_symbol = symbol
                    is_korean = False
                
                # 2년간의 데이터 다운로드
                end_date = datetime.now()
                start_date = end_date - timedelta(days=730)
                
                data = yf.download(download_symbol, start=start_date, end=end_date, progress=False)
                
                if data.empty:
                    progress_window.destroy()
                    messagebox.showerror("❌", f"데이터를 찾을 수 없습니다: {symbol}")
                    return
                
                # 데이터 정리
                data = data.dropna()
                data.index = pd.to_datetime(data.index)
                
                # 파일 저장
                os.makedirs("data", exist_ok=True)
                
                today = datetime.now().strftime("%y%m%d")
                filename = f"data/{symbol}_{today}.csv"
                
                data.to_csv(filename)
                
                # 공유 데이터에 저장
                self.shared_data['current_data'] = data
                self.shared_data['current_symbol'] = symbol
                
                progress_window.destroy()
                
                # 정보 업데이트
                latest_price = data['Close'].iloc[-1]
                data_start = data.index[0].strftime('%Y-%m-%d')
                data_end = data.index[-1].strftime('%Y-%m-%d')
                
                if is_korean and symbol in self.shared_data['korean_stocks']:
                    company_name = self.shared_data['korean_stocks'][symbol]['name']
                    info_text = f"📊 {company_name} ({symbol})\n"
                else:
                    info_text = f"📊 {symbol}\n"
                
                info_text += f"💰 Current Price: ${latest_price:.2f}\n"
                info_text += f"📅 Data Period: {data_start} ~ {data_end}\n"
                info_text += f"📈 Total Records: {len(data):,}\n"
                info_text += f"💾 Saved: {filename}"
                
                self.info_label.config(text=info_text)
                
                # 차트 업데이트
                self.update_chart(data, symbol)
                
                # 파일 목록 새로고침
                self.refresh_files_list()
                
                # 진입가 및 포지션 정보 업데이트
                self.update_portfolio_info()
                
                self.main_app.log_info(f"데이터 다운로드 완료: {symbol}")
                messagebox.showinfo("✅", f"데이터 다운로드 완료!\n{filename}")
                
            except Exception as download_error:
                progress_window.destroy()
                error_msg = f"다운로드 실패: {download_error}"
                self.main_app.log_error(error_msg)
                messagebox.showerror("❌", error_msg)
                
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def update_chart(self, data, symbol):
        """차트 업데이트"""
        try:
            self.ax.clear()
            
            # 가격 차트
            data['Close'].plot(ax=self.ax, linewidth=2, color='blue', label='Close Price')
            
            # 이동평균선 추가
            if len(data) >= 20:
                data['Close'].rolling(20).mean().plot(ax=self.ax, color='orange', 
                                                     alpha=0.7, label='MA20')
            if len(data) >= 50:
                data['Close'].rolling(50).mean().plot(ax=self.ax, color='red', 
                                                     alpha=0.7, label='MA50')
            
            self.ax.set_title(f'{symbol} Stock Price Chart', fontsize=14, fontweight='bold')
            self.ax.set_xlabel('Date')
            self.ax.set_ylabel('Price ($)')
            self.ax.legend()
            self.ax.grid(True, alpha=0.3)
            
            # 가격 범위 표시
            latest_price = data['Close'].iloc[-1]
            max_price = data['Close'].max()
            min_price = data['Close'].min()
            
            self.ax.axhline(y=latest_price, color='blue', linestyle='--', alpha=0.5, 
                           label=f'Current: ${latest_price:.2f}')
            
            # 진입가가 있는 경우 표시
            try:
                entry_price = float(self.entry_price_var.get()) if self.entry_price_var.get() else None
                if entry_price:
                    self.ax.axhline(y=entry_price, color='green', linestyle=':', alpha=0.7,
                                   label=f'Entry: ${entry_price:.2f}')
            except ValueError:
                pass
            
            plt.setp(self.ax.xaxis.get_majorticklabels(), rotation=45)
            plt.tight_layout()
            
            self.chart_canvas.draw()
            
        except Exception as e:
            self.main_app.log_error(f"차트 업데이트 실패: {e}")
    
    def analyze_stock(self):
        """주식 분석"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 다운로드해주세요.")
                return
            
            data = self.shared_data['current_data']
            symbol = self.shared_data['current_symbol']
            
            # 기본 분석
            latest_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
            price_change = latest_price - prev_price
            price_change_pct = (price_change / prev_price) * 100 if prev_price != 0 else 0
            
            # 기간별 수익률
            returns_1w = ((latest_price - data['Close'].iloc[-5]) / data['Close'].iloc[-5] * 100) if len(data) >= 5 else 0
            returns_1m = ((latest_price - data['Close'].iloc[-20]) / data['Close'].iloc[-20] * 100) if len(data) >= 20 else 0
            returns_3m = ((latest_price - data['Close'].iloc[-60]) / data['Close'].iloc[-60] * 100) if len(data) >= 60 else 0
            
            # 변동성 계산
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 1 else 0
            
            # 기술적 지표
            rsi = self.calculate_rsi(data['Close']) if len(data) >= 14 else 50
            
            # 지지/저항선
            recent_high = data['High'].tail(20).max()
            recent_low = data['Low'].tail(20).min()
            
            # 분석 결과 창
            analysis_window = tk.Toplevel(self.main_app.root)
            analysis_window.title(f"📊 {symbol} Analysis Results")
            analysis_window.geometry("700x600")
            analysis_window.transient(self.main_app.root)
            
            main_frame = ttk.Frame(analysis_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 제목
            title_label = ttk.Label(main_frame, text=f"📊 {symbol} Technical Analysis", 
                                   style='Title.TLabel')
            title_label.pack(pady=(0, 20))
            
            # 분석 결과
            analysis_text = f"""
💰 Price Information:
• Current Price: ${latest_price:.2f}
• Daily Change: ${price_change:+.2f} ({price_change_pct:+.2f}%)
• 20-Day High: ${recent_high:.2f}
• 20-Day Low: ${recent_low:.2f}

📈 Performance:
• 1 Week: {returns_1w:+.2f}%
• 1 Month: {returns_1m:+.2f}%
• 3 Month: {returns_3m:+.2f}%

📊 Technical Indicators:
• Volatility (Annual): {volatility:.1f}%
• RSI (14): {rsi:.1f}
• Support Level: ${recent_low:.2f}
• Resistance Level: ${recent_high:.2f}

🎯 Analysis Summary:
"""
            
            # 분석 요약
            if rsi > 70:
                analysis_text += "• RSI indicates OVERBOUGHT condition\n"
            elif rsi < 30:
                analysis_text += "• RSI indicates OVERSOLD condition\n"
            else:
                analysis_text += "• RSI is in NEUTRAL range\n"
            
            if volatility > 30:
                analysis_text += "• HIGH volatility - Consider risk management\n"
            elif volatility < 15:
                analysis_text += "• LOW volatility - Stable price movement\n"
            else:
                analysis_text += "• MODERATE volatility - Normal market condition\n"
            
            if price_change_pct > 5:
                analysis_text += "• Strong BULLISH momentum today\n"
            elif price_change_pct < -5:
                analysis_text += "• Strong BEARISH pressure today\n"
            
            # 텍스트 위젯
            import tkinter.scrolledtext as scrolledtext
            text_widget = scrolledtext.ScrolledText(main_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 11), height=20)
            text_widget.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            text_widget.insert('1.0', analysis_text)
            text_widget.config(state=tk.DISABLED)
            
            # 닫기 버튼
            ttk.Button(main_frame, text="❌ Close", 
                      command=analysis_window.destroy).pack()
            
            self.main_app.log_info(f"분석 완료: {symbol}")
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def calculate_rsi(self, prices, window=14):
        """RSI 계산"""
        try:
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1] if not rsi.empty else 50
        except:
            return 50
    
    def refresh_files_list(self):
        """파일 목록 새로고침"""
        try:
            self.files_listbox.delete(0, tk.END)
            
            data_dir = Path("data")
            if not data_dir.exists():
                data_dir.mkdir()
                return
            
            csv_files = list(data_dir.glob("*.csv"))
            csv_files.sort(key=lambda x: x.stat().st_mtime, reverse=True)
            
            for file_path in csv_files:
                # 파일명에서 정보 추출
                filename = file_path.stem
                file_size = file_path.stat().st_size
                file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                
                # 파일 정보 표시
                size_mb = file_size / 1024 / 1024
                date_str = file_date.strftime("%m/%d %H:%M")
                
                display_text = f"{filename} ({size_mb:.1f}MB) - {date_str}"
                self.files_listbox.insert(tk.END, display_text)
            
            self.main_app.log_info(f"파일 목록 새로고침: {len(csv_files)}개 파일")
            
        except Exception as e:
            self.main_app.log_error(f"파일 목록 새로고침 실패: {e}")
    
    def load_selected_file(self, event):
        """선택된 파일 로드"""
        try:
            selection = self.files_listbox.curselection()
            if not selection:
                return
            
            # 파일명 추출
            display_text = self.files_listbox.get(selection[0])
            filename = display_text.split(' (')[0]  # 크기 정보 제거
            
            file_path = Path(f"data/{filename}.csv")
            if not file_path.exists():
                messagebox.showerror("❌", f"파일을 찾을 수 없습니다: {file_path}")
                return
            
            # 데이터 로드
            data = pd.read_csv(file_path, index_col=0, parse_dates=True)
            
            # 심볼 추출 (파일명에서)
            symbol = filename.split('_')[0]
            
            # 공유 데이터에 저장
            self.shared_data['current_data'] = data
            self.shared_data['current_symbol'] = symbol
            
            # UI 업데이트
            self.symbol_var.set(symbol)
            
            # 정보 표시
            latest_price = data['Close'].iloc[-1]
            data_start = data.index[0].strftime('%Y-%m-%d')
            data_end = data.index[-1].strftime('%Y-%m-%d')
            
            # 한국 주식인지 확인
            if symbol.isdigit() and len(symbol) == 6 and symbol in self.shared_data['korean_stocks']:
                company_name = self.shared_data['korean_stocks'][symbol]['name']
                info_text = f"📊 {company_name} ({symbol})\n"
            else:
                info_text = f"📊 {symbol}\n"
            
            info_text += f"💰 Current Price: ${latest_price:.2f}\n"
            info_text += f"📅 Data Period: {data_start} ~ {data_end}\n"
            info_text += f"📈 Total Records: {len(data):,}\n"
            info_text += f"📁 Loaded from: {file_path.name}"
            
            self.info_label.config(text=info_text)
            
            # 차트 업데이트
            self.update_chart(data, symbol)
            
            # 포트폴리오 정보 업데이트
            self.update_portfolio_info()
            
            self.main_app.log_info(f"파일 로드 완료: {filename}")
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def update_portfolio_info(self):
        """포트폴리오 정보 업데이트"""
        try:
            # 입력된 진입가와 포지션을 공유 데이터에 저장
            try:
                entry_price = float(self.entry_price_var.get()) if self.entry_price_var.get() else None
                position = float(self.position_var.get()) if self.position_var.get() else 0
                
                self.shared_data['entry_price'] = entry_price
                self.shared_data['current_position'] = position
                
            except ValueError:
                self.shared_data['entry_price'] = None
                self.shared_data['current_position'] = 0
            
        except Exception as e:
            self.main_app.log_error(f"포트폴리오 정보 업데이트 실패: {e}")
    
    def show_file_management(self):
        """파일 관리 창 표시"""
        try:
            file_mgmt_window = tk.Toplevel(self.main_app.root)
            file_mgmt_window.title("🗂️ File Management")
            file_mgmt_window.geometry("600x500")
            file_mgmt_window.transient(self.main_app.root)
            
            main_frame = ttk.Frame(file_mgmt_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="🗂️ Data File Management", 
                     style='Title.TLabel').pack(pady=(0, 20))
            
            # 파일 리스트
            files_frame = ttk.LabelFrame(main_frame, text="📁 Data Files", padding="10")
            files_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
            
            # 리스트박스
            listbox_frame = tk.Frame(files_frame)
            listbox_frame.pack(fill=tk.BOTH, expand=True)
            
            file_listbox = tk.Listbox(listbox_frame, font=('Consolas', 10))
            file_scrollbar = ttk.Scrollbar(listbox_frame, orient=tk.VERTICAL, 
                                         command=file_listbox.yview)
            file_listbox.configure(yscrollcommand=file_scrollbar.set)
            
            file_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            file_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # 파일 목록 로드
            data_dir = Path("data")
            if data_dir.exists():
                for file_path in sorted(data_dir.glob("*.csv"), 
                                       key=lambda x: x.stat().st_mtime, reverse=True):
                    file_size = file_path.stat().st_size / 1024 / 1024
                    file_date = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    display_text = f"{file_path.name} - {file_size:.1f}MB - {file_date.strftime('%Y-%m-%d %H:%M')}"
                    file_listbox.insert(tk.END, display_text)
            
            # 버튼 프레임
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def delete_selected():
                try:
                    selection = file_listbox.curselection()
                    if not selection:
                        messagebox.showwarning("⚠️", "삭제할 파일을 선택해주세요.")
                        return
                    
                    filename = file_listbox.get(selection[0]).split(' - ')[0]
                    file_path = Path(f"data/{filename}")
                    
                    if messagebox.askyesno("🗑️", f"정말로 삭제하시겠습니까?\n{filename}"):
                        file_path.unlink()
                        file_listbox.delete(selection[0])
                        messagebox.showinfo("✅", "파일이 삭제되었습니다.")
                        
                except Exception as e:
                    messagebox.showerror("❌", f"삭제 실패: {e}")
            
            def move_to_out():
                try:
                    selection = file_listbox.curselection()
                    if not selection:
                        messagebox.showwarning("⚠️", "이동할 파일을 선택해주세요.")
                        return
                    
                    filename = file_listbox.get(selection[0]).split(' - ')[0]
                    source_path = Path(f"data/{filename}")
                    
                    # out 폴더 생성
                    out_dir = Path("out")
                    out_dir.mkdir(exist_ok=True)
                    
                    dest_path = out_dir / filename
                    source_path.rename(dest_path)
                    
                    file_listbox.delete(selection[0])
                    messagebox.showinfo("✅", f"파일이 out 폴더로 이동되었습니다.\n{filename}")
                    
                except Exception as e:
                    messagebox.showerror("❌", f"이동 실패: {e}")
            
            def open_data_folder():
                try:
                    import subprocess
                    import sys
                    
                    data_path = Path("data").absolute()
                    if sys.platform == "win32":
                        subprocess.run(["explorer", str(data_path)])
                    elif sys.platform == "darwin":
                        subprocess.run(["open", str(data_path)])
                    else:
                        subprocess.run(["xdg-open", str(data_path)])
                        
                except Exception as e:
                    messagebox.showerror("❌", f"폴더 열기 실패: {e}")
            
            ttk.Button(button_frame, text="🗑️ Delete", 
                      command=delete_selected).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="📤 Move to Out", 
                      command=move_to_out).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="📁 Open Folder", 
                      command=open_data_folder).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="🔄 Refresh", 
                      command=lambda: self.refresh_files_list()).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="❌ Close", 
                      command=file_mgmt_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
            