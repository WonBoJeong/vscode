#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
차트 위젯 모듈
matplotlib을 사용한 주식 차트 생성 및 표시
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
import seaborn as sns

# 한글 폰트 설정
plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

class ChartWidget:
    def __init__(self):
        """차트 위젯 초기화"""
        self.style_config = {
            'background_color': '#f8fafc',
            'grid_color': '#e2e8f0',
            'text_color': '#2d3748',
            'positive_color': '#16a34a',
            'negative_color': '#dc2626',
            'volume_color': '#64748b',
            'ma_colors': ['#3b82f6', '#f59e0b', '#8b5cf6', '#ef4444']
        }
        
    def create_candlestick_chart(self, parent_frame, symbol, data):
        """캔들스틱 차트 생성"""
        try:
            # 기존 위젯들 제거
            for widget in parent_frame.winfo_children():
                widget.destroy()
                
            # Figure 생성
            fig = Figure(figsize=(12, 8), facecolor=self.style_config['background_color'])
            
            # 서브플롯 생성 (가격 차트 + 볼륨 차트)
            gs = fig.add_gridspec(3, 1, height_ratios=[3, 1, 0.1])
            ax_price = fig.add_subplot(gs[0])
            ax_volume = fig.add_subplot(gs[1], sharex=ax_price)
            
            # 날짜 인덱스 처리
            dates = data.index
            if not isinstance(dates, pd.DatetimeIndex):
                dates = pd.to_datetime(dates)
                
            # 캔들스틱 데이터 준비
            opens = data['Open'].values
            highs = data['High'].values
            lows = data['Low'].values
            closes = data['Close'].values
            volumes = data['Volume'].values
            
            # 캔들스틱 그리기
            self._draw_candlesticks(ax_price, dates, opens, highs, lows, closes)
            
            # 이동평균선 추가
            self._add_moving_averages(ax_price, dates, closes)
            
            # 볼륨 차트
            self._draw_volume_chart(ax_volume, dates, volumes, closes)
            
            # 차트 스타일링
            self._style_chart(ax_price, ax_volume, symbol)
            
            # Canvas 생성 및 배치
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 네비게이션 툴바
            toolbar_frame = ttk.Frame(parent_frame)
            toolbar_frame.pack(fill=tk.X)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            return canvas
            
        except Exception as e:
            print(f"캔들스틱 차트 생성 오류: {e}")
            # 오류 메시지 표시
            error_label = ttk.Label(parent_frame, text=f"차트 생성 실패: {e}")
            error_label.pack(expand=True)
            return None
            
    def _draw_candlesticks(self, ax, dates, opens, highs, lows, closes):
        """캔들스틱 그리기"""
        try:
            width = 0.8
            width2 = 0.1
            
            # 상승/하락 구분
            up = closes >= opens
            down = ~up
            
            # 상승 캔들 (초록색)
            ax.bar(dates[up], closes[up] - opens[up], width, bottom=opens[up],
                   color=self.style_config['positive_color'], alpha=0.8)
            ax.bar(dates[up], highs[up] - closes[up], width2, bottom=closes[up],
                   color=self.style_config['positive_color'])
            ax.bar(dates[up], lows[up] - opens[up], width2, bottom=opens[up],
                   color=self.style_config['positive_color'])
            
            # 하락 캔들 (빨간색)
            ax.bar(dates[down], opens[down] - closes[down], width, bottom=closes[down],
                   color=self.style_config['negative_color'], alpha=0.8)
            ax.bar(dates[down], highs[down] - opens[down], width2, bottom=opens[down],
                   color=self.style_config['negative_color'])
            ax.bar(dates[down], lows[down] - closes[down], width2, bottom=closes[down],
                   color=self.style_config['negative_color'])
                   
        except Exception as e:
            print(f"캔들스틱 그리기 오류: {e}")
            
    def _add_moving_averages(self, ax, dates, closes):
        """이동평균선 추가"""
        try:
            # 5일, 20일, 60일 이동평균
            periods = [5, 20, 60]
            colors = self.style_config['ma_colors'][:len(periods)]
            
            for i, period in enumerate(periods):
                if len(closes) > period:
                    ma = pd.Series(closes).rolling(window=period).mean()
                    valid_mask = ~np.isnan(ma)
                    ax.plot(dates[valid_mask], ma[valid_mask], 
                           color=colors[i], linewidth=1.5, alpha=0.8,
                           label=f'MA{period}')
                           
            ax.legend(loc='upper left', frameon=True, fancybox=True, shadow=True)
            
        except Exception as e:
            print(f"이동평균선 추가 오류: {e}")
            
    def _draw_volume_chart(self, ax, dates, volumes, closes):
        """볼륨 차트 그리기"""
        try:
            # 가격 변동에 따른 볼륨 색상
            price_change = np.diff(closes, prepend=closes[0])
            colors = [self.style_config['positive_color'] if change >= 0 
                     else self.style_config['negative_color'] for change in price_change]
            
            ax.bar(dates, volumes, color=colors, alpha=0.6, width=1)
            ax.set_ylabel('Volume', color=self.style_config['text_color'])
            
        except Exception as e:
            print(f"볼륨 차트 그리기 오류: {e}")
            
    def _style_chart(self, ax_price, ax_volume, symbol):
        """차트 스타일링"""
        try:
            # 제목
            ax_price.set_title(f'{symbol} - Stock Chart', 
                             fontsize=16, fontweight='bold',
                             color=self.style_config['text_color'])
            
            # 축 레이블
            ax_price.set_ylabel('Price ($)', color=self.style_config['text_color'])
            ax_volume.set_xlabel('Date', color=self.style_config['text_color'])
            
            # 그리드
            ax_price.grid(True, alpha=0.3, color=self.style_config['grid_color'])
            ax_volume.grid(True, alpha=0.3, color=self.style_config['grid_color'])
            
            # 배경색
            ax_price.set_facecolor(self.style_config['background_color'])
            ax_volume.set_facecolor(self.style_config['background_color'])
            
            # 날짜 형식
            ax_volume.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax_volume.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            
            # 레이블 회전
            plt.setp(ax_volume.xaxis.get_majorticklabels(), rotation=45)
            
            # 여백 조정
            plt.tight_layout()
            
        except Exception as e:
            print(f"차트 스타일링 오류: {e}")
            
    def create_technical_chart(self, parent_frame, symbol, data, indicators):
        """기술적 분석 차트 생성"""
        try:
            # 기존 위젯들 제거
            for widget in parent_frame.winfo_children():
                widget.destroy()
                
            if indicators is None:
                error_label = ttk.Label(parent_frame, text="기술적 지표 데이터가 없습니다.")
                error_label.pack(expand=True)
                return None
                
            # Figure 생성
            fig = Figure(figsize=(12, 10), facecolor=self.style_config['background_color'])
            
            # 서브플롯 생성
            gs = fig.add_gridspec(4, 1, height_ratios=[2, 1, 1, 1])
            ax_price = fig.add_subplot(gs[0])
            ax_rsi = fig.add_subplot(gs[1], sharex=ax_price)
            ax_macd = fig.add_subplot(gs[2], sharex=ax_price)
            ax_stoch = fig.add_subplot(gs[3], sharex=ax_price)
            
            dates = data.index
            if not isinstance(dates, pd.DatetimeIndex):
                dates = pd.to_datetime(dates)
                
            # 가격 차트 + 볼린저 밴드
            self._draw_price_with_bb(ax_price, dates, data, indicators)
            
            # RSI 차트
            self._draw_rsi_chart(ax_rsi, dates, indicators)
            
            # MACD 차트
            self._draw_macd_chart(ax_macd, dates, indicators)
            
            # 스토캐스틱 차트
            self._draw_stochastic_chart(ax_stoch, dates, indicators)
            
            # 스타일링
            self._style_technical_chart(fig, ax_price, ax_rsi, ax_macd, ax_stoch, symbol)
            
            # Canvas 생성
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 툴바
            toolbar_frame = ttk.Frame(parent_frame)
            toolbar_frame.pack(fill=tk.X)
            toolbar = NavigationToolbar2Tk(canvas, toolbar_frame)
            toolbar.update()
            
            return canvas
            
        except Exception as e:
            print(f"기술적 분석 차트 생성 오류: {e}")
            error_label = ttk.Label(parent_frame, text=f"기술적 분석 차트 생성 실패: {e}")
            error_label.pack(expand=True)
            return None
            
    def _draw_price_with_bb(self, ax, dates, data, indicators):
        """가격 차트 + 볼린저 밴드"""
        try:
            # 종가 라인
            ax.plot(dates, data['Close'], color='#2563eb', linewidth=2, label='Close')
            
            # 볼린저 밴드
            if 'BB_Upper' in indicators and 'BB_Lower' in indicators:
                bb_upper = indicators['BB_Upper']
                bb_lower = indicators['BB_Lower']
                bb_middle = indicators.get('BB_Middle', indicators.get('SMA_20'))
                
                ax.plot(dates, bb_upper, color='#ef4444', linewidth=1, alpha=0.7, label='BB Upper')
                ax.plot(dates, bb_lower, color='#ef4444', linewidth=1, alpha=0.7, label='BB Lower')
                if bb_middle is not None:
                    ax.plot(dates, bb_middle, color='#f59e0b', linewidth=1, label='BB Middle')
                
                # 밴드 사이 음영
                ax.fill_between(dates, bb_upper, bb_lower, alpha=0.1, color='#ef4444')
                
            ax.legend(loc='upper left')
            ax.set_title('Price with Bollinger Bands')
            
        except Exception as e:
            print(f"가격 + 볼린저 밴드 차트 오류: {e}")
            
    def _draw_rsi_chart(self, ax, dates, indicators):
        """RSI 차트"""
        try:
            if 'RSI' in indicators:
                rsi = indicators['RSI']
                ax.plot(dates, rsi, color='#8b5cf6', linewidth=2, label='RSI')
                
                # 과매수/과매도 라인
                ax.axhline(y=70, color='#ef4444', linestyle='--', alpha=0.7, label='Overbought')
                ax.axhline(y=30, color='#16a34a', linestyle='--', alpha=0.7, label='Oversold')
                ax.axhline(y=50, color='#64748b', linestyle='-', alpha=0.5)
                
                # 음영
                ax.fill_between(dates, 70, 100, alpha=0.1, color='#ef4444')
                ax.fill_between(dates, 0, 30, alpha=0.1, color='#16a34a')
                
                ax.set_ylim(0, 100)
                ax.legend(loc='upper left')
                ax.set_title('RSI (14)')
                
        except Exception as e:
            print(f"RSI 차트 오류: {e}")
            
    def _draw_macd_chart(self, ax, dates, indicators):
        """MACD 차트"""
        try:
            if 'MACD' in indicators:
                macd = indicators['MACD']
                signal = indicators.get('MACD_Signal')
                histogram = indicators.get('MACD_Histogram')
                
                # MACD 라인
                ax.plot(dates, macd, color='#2563eb', linewidth=2, label='MACD')
                
                # 시그널 라인
                if signal is not None:
                    ax.plot(dates, signal, color='#ef4444', linewidth=2, label='Signal')
                
                # 히스토그램
                if histogram is not None:
                    colors = ['#16a34a' if x >= 0 else '#ef4444' for x in histogram]
                    ax.bar(dates, histogram, color=colors, alpha=0.6, width=1, label='Histogram')
                
                # 0 라인
                ax.axhline(y=0, color='#64748b', linestyle='-', alpha=0.5)
                
                ax.legend(loc='upper left')
                ax.set_title('MACD')
                
        except Exception as e:
            print(f"MACD 차트 오류: {e}")
            
    def _draw_stochastic_chart(self, ax, dates, indicators):
        """스토캐스틱 차트"""
        try:
            if 'Stoch_K' in indicators:
                stoch_k = indicators['Stoch_K']
                stoch_d = indicators.get('Stoch_D')
                
                ax.plot(dates, stoch_k, color='#2563eb', linewidth=2, label='%K')
                
                if stoch_d is not None:
                    ax.plot(dates, stoch_d, color='#ef4444', linewidth=2, label='%D')
                
                # 과매수/과매도 라인
                ax.axhline(y=80, color='#ef4444', linestyle='--', alpha=0.7)
                ax.axhline(y=20, color='#16a34a', linestyle='--', alpha=0.7)
                
                # 음영
                ax.fill_between(dates, 80, 100, alpha=0.1, color='#ef4444')
                ax.fill_between(dates, 0, 20, alpha=0.1, color='#16a34a')
                
                ax.set_ylim(0, 100)
                ax.legend(loc='upper left')
                ax.set_title('Stochastic')
                
        except Exception as e:
            print(f"스토캐스틱 차트 오류: {e}")
            
    def _style_technical_chart(self, fig, ax_price, ax_rsi, ax_macd, ax_stoch, symbol):
        """기술적 분석 차트 스타일링"""
        try:
            # 전체 제목
            fig.suptitle(f'{symbol} - Technical Analysis', fontsize=16, fontweight='bold')
            
            # 그리드
            for ax in [ax_price, ax_rsi, ax_macd, ax_stoch]:
                ax.grid(True, alpha=0.3, color=self.style_config['grid_color'])
                ax.set_facecolor(self.style_config['background_color'])
            
            # X축 레이블 (마지막 subplot에만)
            ax_stoch.set_xlabel('Date')
            
            # 날짜 형식
            ax_stoch.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            ax_stoch.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
            plt.setp(ax_stoch.xaxis.get_majorticklabels(), rotation=45)
            
            # 여백 조정
            plt.tight_layout()
            
        except Exception as e:
            print(f"기술적 분석 차트 스타일링 오류: {e}")
            
    def create_comparison_chart(self, parent_frame, symbols_data):
        """다중 종목 비교 차트"""
        try:
            # 기존 위젯들 제거
            for widget in parent_frame.winfo_children():
                widget.destroy()
                
            if not symbols_data:
                error_label = ttk.Label(parent_frame, text="비교할 데이터가 없습니다.")
                error_label.pack(expand=True)
                return None
                
            # Figure 생성
            fig = Figure(figsize=(12, 8), facecolor=self.style_config['background_color'])
            ax = fig.add_subplot(111)
            
            # 정규화된 가격 비교 (시작점을 100으로)
            colors = ['#2563eb', '#ef4444', '#16a34a', '#f59e0b', '#8b5cf6']
            
            for i, (symbol, data) in enumerate(symbols_data.items()):
                if data is not None and not data.empty:
                    normalized_price = (data['Close'] / data['Close'].iloc[0]) * 100
                    ax.plot(data.index, normalized_price, 
                           color=colors[i % len(colors)], 
                           linewidth=2, label=symbol)
            
            # 스타일링
            ax.set_title('Stock Price Comparison (Normalized)', fontsize=16, fontweight='bold')
            ax.set_xlabel('Date')
            ax.set_ylabel('Normalized Price (Start = 100)')
            ax.legend()
            ax.grid(True, alpha=0.3)
            ax.set_facecolor(self.style_config['background_color'])
            
            # Canvas 생성
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            return canvas
            
        except Exception as e:
            print(f"비교 차트 생성 오류: {e}")
            error_label = ttk.Label(parent_frame, text=f"비교 차트 생성 실패: {e}")
            error_label.pack(expand=True)
            return None
            
    def create_portfolio_chart(self, parent_frame, portfolio_data):
        """포트폴리오 분석 차트"""
        try:
            # 기존 위젯들 제거
            for widget in parent_frame.winfo_children():
                widget.destroy()
                
            if not portfolio_data:
                error_label = ttk.Label(parent_frame, text="포트폴리오 데이터가 없습니다.")
                error_label.pack(expand=True)
                return None
                
            # Figure 생성
            fig = Figure(figsize=(12, 10), facecolor=self.style_config['background_color'])
            
            # 서브플롯 생성
            gs = fig.add_gridspec(2, 2)
            ax_allocation = fig.add_subplot(gs[0, 0])
            ax_performance = fig.add_subplot(gs[0, 1])
            ax_timeline = fig.add_subplot(gs[1, :])
            
            # 포트폴리오 할당 (파이 차트)
            self._draw_allocation_pie(ax_allocation, portfolio_data)
            
            # 성과 비교 (바 차트)
            self._draw_performance_bar(ax_performance, portfolio_data)
            
            # 시간별 수익률 (라인 차트)
            self._draw_timeline_performance(ax_timeline, portfolio_data)
            
            plt.tight_layout()
            
            # Canvas 생성
            canvas = FigureCanvasTkAgg(fig, parent_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            return canvas
            
        except Exception as e:
            print(f"포트폴리오 차트 생성 오류: {e}")
            error_label = ttk.Label(parent_frame, text=f"포트폴리오 차트 생성 실패: {e}")
            error_label.pack(expand=True)
            return None
            
    def _draw_allocation_pie(self, ax, portfolio_data):
        """포트폴리오 할당 파이 차트"""
        # 모의 데이터
        symbols = list(portfolio_data.keys())[:5]  # 상위 5개
        weights = [20, 20, 20, 20, 20]  # 동일 비중
        
        ax.pie(weights, labels=symbols, autopct='%1.1f%%', startangle=90)
        ax.set_title('Portfolio Allocation')
        
    def _draw_performance_bar(self, ax, portfolio_data):
        """성과 바 차트"""
        # 모의 수익률 데이터
        symbols = list(portfolio_data.keys())[:5]
        returns = [5.2, -2.1, 8.7, 3.4, -1.5]  # 모의 수익률
        
        colors = [self.style_config['positive_color'] if r > 0 
                 else self.style_config['negative_color'] for r in returns]
        
        ax.bar(symbols, returns, color=colors)
        ax.set_title('Individual Stock Performance (%)')
        ax.set_ylabel('Return (%)')
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
    def _draw_timeline_performance(self, ax, portfolio_data):
        """시간별 성과 라인 차트"""
        # 모의 포트폴리오 성과 데이터
        dates = pd.date_range(start='2023-01-01', end='2024-01-01', freq='D')
        performance = np.cumsum(np.random.normal(0.001, 0.02, len(dates))) * 100
        
        ax.plot(dates, performance, color=self.style_config['positive_color'], linewidth=2)
        ax.set_title('Portfolio Performance Over Time')
        ax.set_xlabel('Date')
        ax.set_ylabel('Cumulative Return (%)')
        ax.grid(True, alpha=0.3)