#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Chart Manager Module
차트 생성 및 관리 기능

Author: AI Assistant & User
Version: 1.0.0
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import pandas as pd
import numpy as np
import tkinter as tk
from tkinter import messagebox, filedialog, ttk
from datetime import datetime
from pathlib import Path
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from config import CHART_CONFIG
from .utils import Logger, format_currency_auto, get_color_by_change, DataValidator

class ChartManager:
    """차트 관리 클래스"""
    
    def __init__(self, parent_widget):
        self.parent_widget = parent_widget
        self.logger = Logger("ChartManager")
        
        # 차트 설정
        self.figure = None
        self.canvas = None
        self.toolbar = None
        self.axes = None
        
        # 데이터 및 설정
        self.current_data = None
        self.current_symbol = ""
        self.entry_price = None
        self.is_korean_stock = False
        
        # 차트 옵션
        self.period = CHART_CONFIG['default_period']
        self.show_ma5 = True
        self.show_ma20 = True
        self.show_ma60 = False
        self.show_ma200 = False
        
        # 초기화
        self.setup_chart()
    
    def setup_chart(self):
        """차트 초기 설정"""
        try:
            # matplotlib 설정
            plt.rcParams['font.family'] = CHART_CONFIG['font_family']
            plt.rcParams['axes.unicode_minus'] = CHART_CONFIG['enable_unicode_minus']
            plt.rcParams['font.size'] = 11
            
            # Figure 생성
            self.figure, self.axes = plt.subplots(
                figsize=CHART_CONFIG['figure_size'], 
                dpi=CHART_CONFIG['dpi']
            )
            
            # Canvas 생성
            self.canvas = FigureCanvasTkAgg(self.figure, self.parent_widget)
            self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            
            # 네비게이션 툴바
            self.toolbar = NavigationToolbar2Tk(self.canvas, self.parent_widget)
            self.toolbar.update()
            
            # 초기 차트
            self.show_empty_chart()
            
            self.logger.info("Chart setup completed")
            
        except Exception as e:
            self.logger.error(f"Chart setup failed: {e}")
            raise
    
    def show_empty_chart(self):
        """빈 차트 표시"""
        try:
            self.axes.clear()
            self.axes.text(0.5, 0.5, '📈 차트가 여기에 표시됩니다\n\n주식을 선택하고 분석을 실행하세요', 
                          transform=self.axes.transAxes, ha='center', va='center', 
                          fontsize=16, color='gray')
            self.axes.set_xticks([])
            self.axes.set_yticks([])
            self.canvas.draw()
        except Exception as e:
            self.logger.error(f"Empty chart display failed: {e}")
    
    def update_chart(self, data, symbol, entry_price=None, company_name=None):
        """차트 업데이트"""
        try:
            if data is None or data.empty:
                self.show_empty_chart()
                return False
            
            self.current_data = data
            self.current_symbol = symbol
            self.entry_price = entry_price
            # 한국 주식 여부 확인
            self.is_korean_stock = DataValidator.is_korean_stock(symbol)
            
            # 차트 클리어
            self.axes.clear()
            
            # 기간별 데이터 선택
            chart_data = self.get_period_data(data)
            
            if chart_data.empty:
                self.show_empty_chart()
                return False
            
            # 가격 차트 그리기
            self.plot_price_line(chart_data)
            
            # 이동평균선 그리기
            self.plot_moving_averages(chart_data)
            
            # 진입가 라인 그리기
            if entry_price:
                self.plot_entry_line(entry_price)
            
            # 차트 스타일링
            self.style_chart(symbol, company_name)
            
            # X축 날짜 형식 설정
            self.format_x_axis(chart_data)
            
            # Y축 범위 조정
            self.adjust_y_axis(chart_data)
            
            # 그리드 및 기타 설정
            self.finalize_chart()
            
            # 차트 그리기
            self.canvas.draw()
            
            self.logger.info(f"Chart updated for {symbol} (Korean: {self.is_korean_stock})")
            return True
            
        except Exception as e:
            self.logger.error(f"Chart update failed: {e}")
            self.show_empty_chart()
            return False
    
    def get_period_data(self, data):
        """기간별 데이터 선택"""
        try:
            if self.period == "30일":
                return data.tail(30)
            elif self.period == "90일":
                return data.tail(90)
            elif self.period == "1년":
                return data.tail(252)
            elif self.period == "3년":
                return data.tail(252*3)
            elif self.period == "10년":
                return data.tail(252*10)
            else:
                return data.tail(90)  # 기본값
        except Exception as e:
            self.logger.error(f"Period data selection failed: {e}")
            return data
    
    def plot_price_line(self, data):
        """가격 라인 그리기"""
        try:
            colors = CHART_CONFIG['colors']
            self.axes.plot(data.index, data['Close'], 
                          color=colors['price'], linewidth=3, 
                          label='Close Price', alpha=0.8)
        except Exception as e:
            self.logger.error(f"Price line plotting failed: {e}")
    
    def plot_moving_averages(self, data):
        """이동평균선 그리기"""
        try:
            colors = CHART_CONFIG['colors']
            
            ma_settings = [
                (self.show_ma5, 5, 'MA5', colors['ma5']),
                (self.show_ma20, 20, 'MA20', colors['ma20']),
                (self.show_ma60, 60, 'MA60', colors['ma60']),
                (self.show_ma200, 200, 'MA200', colors['ma200'])
            ]
            
            for show, period, label, color in ma_settings:
                if show and len(data) >= period:
                    ma = data['Close'].rolling(period).mean()
                    self.axes.plot(data.index, ma, color=color, linewidth=2, 
                                  alpha=0.7, label=label)
                    
        except Exception as e:
            self.logger.error(f"Moving averages plotting failed: {e}")
    
    def plot_entry_line(self, entry_price):
        """평단가 라인 그리기"""
        try:
            if entry_price and entry_price > 0:
                colors = CHART_CONFIG['colors']
                # 한국/미국 구분해서 라벨 표시 - "Mean" 용어 사용
                if self.is_korean_stock:
                    label_text = f'Mean: ₩{entry_price:,.0f}'
                else:
                    label_text = f'Mean: ${entry_price:.2f}'
                
                self.axes.axhline(y=entry_price, color=colors['entry_line'], 
                                 linestyle='--', linewidth=2, alpha=0.8, 
                                 label=label_text)
        except Exception as e:
            self.logger.error(f"Entry line plotting failed: {e}")
    
    def style_chart(self, symbol, company_name=None):
        """차트 스타일링"""
        try:
            # 제목 설정
            if company_name and company_name != symbol:
                title = f'{company_name} ({symbol}) - {self.period}'
            else:
                title = f'{symbol} - {self.period}'
                
            self.axes.set_title(title, fontsize=18, fontweight='bold', pad=20)
            
            # Y축 라벨 설정 (한국/미국 구분)
            if self.is_korean_stock:
                self.axes.set_ylabel('Price (₩)', fontsize=14)
            else:
                self.axes.set_ylabel('Price ($)', fontsize=14)
            
            # 범례 설정
            handles, labels = self.axes.get_legend_handles_labels()
            if handles:
                self.axes.legend(loc='upper left', fontsize=12, framealpha=0.9)
                
        except Exception as e:
            self.logger.error(f"Chart styling failed: {e}")
    
    def format_x_axis(self, data):
        """X축 날짜 형식 설정"""
        try:
            if not hasattr(data.index, 'date'):
                return
            
            data_length = len(data)
            
            if data_length > 252:  # 1년 이상
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
                self.axes.xaxis.set_major_locator(mdates.MonthLocator(interval=3))
            elif data_length > 90:  # 90일 이상
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                self.axes.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            else:  # 90일 미만
                self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
                self.axes.xaxis.set_major_locator(mdates.WeekdayLocator())
            
            # 날짜 라벨 회전
            plt.setp(self.axes.xaxis.get_majorticklabels(), rotation=45, ha='right')
            
        except Exception as e:
            self.logger.error(f"X-axis formatting failed: {e}")
    
    def adjust_y_axis(self, data):
        """Y축 범위 조정"""
        try:
            if 'Close' in data.columns:
                price_min = data['Close'].min()
                price_max = data['Close'].max()
                price_range = price_max - price_min
                margin = price_range * 0.05  # 5% 마진
                
                self.axes.set_ylim(price_min - margin, price_max + margin)
                
                # Y축 포맷터 설정 (한국/미국 구분)
                if self.is_korean_stock:
                    # 한국 주식: 원화, 천 단위 구분기호, 소수점 없음
                    self.axes.yaxis.set_major_formatter(plt.FuncFormatter(
                        lambda x, p: f'₩{x:,.0f}'
                    ))
                else:
                    # 미국 주식: 달러, 소수점 있음
                    self.axes.yaxis.set_major_formatter(plt.FuncFormatter(
                        lambda x, p: f'${x:,.2f}'
                    ))
                    
        except Exception as e:
            self.logger.error(f"Y-axis adjustment failed: {e}")
    
    def finalize_chart(self):
        """차트 마무리 설정"""
        try:
            # 그리드 설정
            grid_color = CHART_CONFIG['colors']['grid']
            self.axes.grid(True, alpha=0.3, linestyle='-', linewidth=0.5, color=grid_color)
            
            # 레이아웃 조정
            self.figure.tight_layout(pad=3.0)
            
        except Exception as e:
            self.logger.error(f"Chart finalization failed: {e}")
    
    def set_period(self, period):
        """차트 기간 설정"""
        try:
            if period in ["30일", "90일", "1년", "3년", "10년"]:
                self.period = period
                self.logger.info(f"Chart period set to: {period}")
                return True
            else:
                self.logger.warning(f"Invalid period: {period}")
                return False
        except Exception as e:
            self.logger.error(f"Period setting failed: {e}")
            return False
    
    def set_moving_averages(self, ma5=None, ma20=None, ma60=None, ma200=None):
        """이동평균선 표시 설정"""
        try:
            if ma5 is not None:
                self.show_ma5 = ma5
            if ma20 is not None:
                self.show_ma20 = ma20
            if ma60 is not None:
                self.show_ma60 = ma60
            if ma200 is not None:
                self.show_ma200 = ma200
                
            self.logger.info(f"Moving averages set: MA5={self.show_ma5}, MA20={self.show_ma20}, MA60={self.show_ma60}, MA200={self.show_ma200}")
            return True
            
        except Exception as e:
            self.logger.error(f"Moving averages setting failed: {e}")
            return False
    
    def refresh_chart(self):
        """차트 새로고침"""
        try:
            if self.current_data is not None:
                return self.update_chart(self.current_data, self.current_symbol, 
                                       self.entry_price)
            else:
                self.show_empty_chart()
                return True
        except Exception as e:
            self.logger.error(f"Chart refresh failed: {e}")
            return False
    
    def save_chart(self, filepath=None):
        """차트 저장"""
        try:
            if self.current_data is None:
                raise ValueError("No chart data to save")
            
            if filepath is None:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                default_filename = f"chart_{self.current_symbol}_{timestamp}.png"
                
                filepath = filedialog.asksaveasfilename(
                    title="Save Chart",
                    defaultextension=".png",
                    initialname=default_filename,
                    filetypes=[
                        ("PNG files", "*.png"), 
                        ("PDF files", "*.pdf"), 
                        ("SVG files", "*.svg"),
                        ("All files", "*.*")
                    ]
                )
                
                if not filepath:
                    return False
            
            # 차트 저장
            self.figure.savefig(filepath, dpi=300, bbox_inches='tight', 
                               facecolor='white', edgecolor='none')
            
            self.logger.info(f"Chart saved: {filepath}")
            return True
            
        except Exception as e:
            self.logger.error(f"Chart save failed: {e}")
            return False
    
    def get_chart_info(self):
        """차트 정보 반환"""
        try:
            if self.current_data is None:
                return None
            
            data = self.get_period_data(self.current_data)
            
            info = {
                'symbol': self.current_symbol,
                'period': self.period,
                'data_points': len(data),
                'is_korean': self.is_korean_stock,
                'date_range': {
                    'start': data.index.min().strftime('%Y-%m-%d') if hasattr(data.index, 'strftime') else str(data.index.min()),
                    'end': data.index.max().strftime('%Y-%m-%d') if hasattr(data.index, 'strftime') else str(data.index.max())
                },
                'price_range': {
                    'min': float(data['Close'].min()),
                    'max': float(data['Close'].max()),
                    'current': float(data['Close'].iloc[-1]) if len(data) > 0 else None
                },
                'moving_averages': {
                    'ma5': self.show_ma5,
                    'ma20': self.show_ma20,
                    'ma60': self.show_ma60,
                    'ma200': self.show_ma200
                },
                'entry_price': self.entry_price
            }
            
            return info
            
        except Exception as e:
            self.logger.error(f"Chart info retrieval failed: {e}")
            return None
    
    def clear_chart(self):
        """차트 클리어"""
        try:
            self.current_data = None
            self.current_symbol = ""
            self.entry_price = None
            self.is_korean_stock = False
            self.show_empty_chart()
            self.logger.info("Chart cleared")
        except Exception as e:
            self.logger.error(f"Chart clear failed: {e}")
    
    def destroy(self):
        """차트 매니저 정리"""
        try:
            if self.canvas:
                self.canvas.get_tk_widget().destroy()
            if self.toolbar:
                self.toolbar.destroy()
            if self.figure:
                plt.close(self.figure)
            self.logger.info("Chart manager destroyed")
        except Exception as e:
            self.logger.error(f"Chart manager destruction failed: {e}")

class ChartControlPanel:
    """차트 컨트롤 패널"""
    
    def __init__(self, parent, chart_manager):
        self.parent = parent
        self.chart_manager = chart_manager
        self.logger = Logger("ChartControlPanel")
        
        # 변수들
        self.period_var = tk.StringVar(value=chart_manager.period)
        self.ma5_var = tk.BooleanVar(value=chart_manager.show_ma5)
        self.ma20_var = tk.BooleanVar(value=chart_manager.show_ma20)
        self.ma60_var = tk.BooleanVar(value=chart_manager.show_ma60)
        self.ma200_var = tk.BooleanVar(value=chart_manager.show_ma200)
        
        self.create_controls()
    
    def create_controls(self):
        """컨트롤 생성 - 한 줄로 배치"""
        try:
            # 모든 컨트롤을 한 줄로 배치
            control_row = tk.Frame(self.parent)
            control_row.pack(fill=tk.X, pady=(0, 5))
            
            # 기간 선택
            tk.Label(control_row, text="기간:", font=('Segoe UI', 11)).pack(side=tk.LEFT)
            period_combo = ttk.Combobox(control_row, textvariable=self.period_var, 
                                       values=["30일", "90일", "1년", "3년", "10년"], 
                                       state="readonly", width=8)
            period_combo.pack(side=tk.LEFT, padx=(5, 15))
            period_combo.bind('<<ComboboxSelected>>', self.on_period_changed)
            
            # 차트 액션 버튼들 (저장 버튼 제거)
            ttk.Button(control_row, text="🔄 새로고침", 
                      command=self.refresh_chart).pack(side=tk.LEFT, padx=(0, 5))
            ttk.Button(control_row, text="ℹ️ 정보", 
                      command=self.show_chart_info).pack(side=tk.LEFT, padx=(0, 15))
            
            # 이동평균선 선택
            tk.Label(control_row, text="이동평균:", font=('Segoe UI', 11)).pack(side=tk.LEFT)
            
            ma5_check = ttk.Checkbutton(control_row, text="MA5", variable=self.ma5_var,
                                       command=self.on_ma_changed)
            ma5_check.pack(side=tk.LEFT, padx=5)
            
            ma20_check = ttk.Checkbutton(control_row, text="MA20", variable=self.ma20_var,
                                        command=self.on_ma_changed)
            ma20_check.pack(side=tk.LEFT, padx=5)
            
            ma60_check = ttk.Checkbutton(control_row, text="MA60", variable=self.ma60_var,
                                        command=self.on_ma_changed)
            ma60_check.pack(side=tk.LEFT, padx=5)
            
            ma200_check = ttk.Checkbutton(control_row, text="MA200", variable=self.ma200_var,
                                         command=self.on_ma_changed)
            ma200_check.pack(side=tk.LEFT, padx=5)
            
        except Exception as e:
            self.logger.error(f"Control creation failed: {e}")
    
    def on_period_changed(self, event=None):
        """기간 변경 이벤트"""
        try:
            period = self.period_var.get()
            if self.chart_manager.set_period(period):
                self.chart_manager.refresh_chart()
        except Exception as e:
            self.logger.error(f"Period change failed: {e}")
    
    def on_ma_changed(self):
        """이동평균선 변경 이벤트"""
        try:
            self.chart_manager.set_moving_averages(
                ma5=self.ma5_var.get(),
                ma20=self.ma20_var.get(),
                ma60=self.ma60_var.get(),
                ma200=self.ma200_var.get()
            )
            self.chart_manager.refresh_chart()
        except Exception as e:
            self.logger.error(f"Moving averages change failed: {e}")
    
    def refresh_chart(self):
        """차트 새로고침"""
        try:
            if self.chart_manager.refresh_chart():
                messagebox.showinfo("✅", "차트가 새로고침되었습니다.")
            else:
                messagebox.showwarning("⚠️", "새로고침할 차트 데이터가 없습니다.")
        except Exception as e:
            self.logger.error(f"Chart refresh failed: {e}")
            messagebox.showerror("❌", f"차트 새로고침 실패: {e}")
    
    def save_chart(self):
        """차트 저장"""
        try:
            if self.chart_manager.save_chart():
                messagebox.showinfo("✅", "차트가 저장되었습니다.")
            else:
                messagebox.showwarning("⚠️", "저장할 차트가 없거나 취소되었습니다.")
        except Exception as e:
            self.logger.error(f"Chart save failed: {e}")
            messagebox.showerror("❌", f"차트 저장 실패: {e}")
    
    def show_chart_info(self):
        """차트 정보 표시"""
        try:
            info = self.chart_manager.get_chart_info()
            
            if not info:
                messagebox.showwarning("⚠️", "차트 정보가 없습니다.")
                return
            
            # 한국/미국 구분해서 정보 표시
            if info['is_korean']:
                current_price = f"₩{info['price_range']['current']:,.0f}"
                max_price = f"₩{info['price_range']['max']:,.0f}"
                min_price = f"₩{info['price_range']['min']:,.0f}"
                entry_text = f"• 평단가: ₩{info['entry_price']:,.0f}" if info['entry_price'] else ""
            else:
                current_price = f"${info['price_range']['current']:.2f}"
                max_price = f"${info['price_range']['max']:.2f}"
                min_price = f"${info['price_range']['min']:.2f}"
                entry_text = f"• 평단가: ${info['entry_price']:.2f}" if info['entry_price'] else ""
            
            info_text = f"""📊 차트 정보

• 종목: {info['symbol']} ({'한국 주식' if info['is_korean'] else '미국 주식'})
• 기간: {info['period']}
• 데이터 포인트: {info['data_points']:,}개
• 날짜 범위: {info['date_range']['start']} ~ {info['date_range']['end']}

💰 가격 정보:
• 현재가: {current_price}
• 최고가: {max_price}
• 최저가: {min_price}

📈 이동평균선:
• MA5: {'표시' if info['moving_averages']['ma5'] else '숨김'}
• MA20: {'표시' if info['moving_averages']['ma20'] else '숨김'}
• MA60: {'표시' if info['moving_averages']['ma60'] else '숨김'}
• MA200: {'표시' if info['moving_averages']['ma200'] else '숨김'}

{entry_text}"""
            
            messagebox.showinfo("📊 차트 정보", info_text)
            
        except Exception as e:
            self.logger.error(f"Chart info display failed: {e}")
            messagebox.showerror("❌", f"차트 정보 표시 실패: {e}")
