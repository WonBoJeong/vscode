#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Korean Stock Manager Module
한국 주식 종목 관리 및 검색 기능

Author: AI Assistant & User
Version: 1.0.1 - load_stock_list 메서드 추가
"""

import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from pathlib import Path
import re
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from config import DATA_CONFIG
from .utils import Logger, DataValidator

class KoreanStockManager:
    """한국 주식 관리 클래스"""
    
    def __init__(self):
        self.logger = Logger("KoreanStockManager")
        self.stocks_data = {}
        self.load_korean_stocks()
    
    def load_korean_stocks(self):
        """한국 주식 리스트 로드"""
        try:
            krx_file = Path(DATA_CONFIG['korean_stock_file'])
            
            if not krx_file.exists():
                self.logger.warning(f"KRX stock list file not found: {krx_file}")
                return False
            
            # CSV 파일 로드
            df = pd.read_csv(krx_file, encoding='utf-8')
            
            # 필수 컬럼 확인
            required_columns = ['code', 'name']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                self.logger.error(f"Missing columns in KRX file: {missing_columns}")
                return False
            
            # 데이터 정리 및 저장
            for _, row in df.iterrows():
                try:
                    code = str(row['code']).zfill(6)  # 6자리로 맞춤
                    name = str(row['name']).strip()
                    
                    if code and name and len(code) == 6 and code.isdigit():
                        self.stocks_data[code] = {
                            'name': name,
                            'market': row.get('market', ''),
                            'sector': row.get('sector', ''),
                            'industry': row.get('industry', ''),
                            'listing_date': row.get('listing_date', ''),
                            'market_cap': row.get('market_cap', ''),
                            'stocks': row.get('stocks', '')
                        }
                except Exception as e:
                    continue
            
            self.logger.info(f"Korean stocks loaded: {len(self.stocks_data)} companies")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to load Korean stocks: {e}")
            return False
    
    def load_stock_list(self):
        """주식 리스트 반환 (main.py 호환성을 위한 메서드)"""
        try:
            if not self.stocks_data:
                self.load_korean_stocks()
            
            return self.stocks_data.copy()
            
        except Exception as e:
            self.logger.error(f"Failed to load stock list: {e}")
            return {}
    
    def search_by_name(self, query, max_results=20):
        """회사명으로 검색"""
        if not query or len(query.strip()) < 1:
            return []
        
        query = query.strip().upper()
        results = []
        
        try:
            for code, info in self.stocks_data.items():
                company_name = info['name'].upper()
                
                # 정확히 일치하는 경우 우선순위
                if query == company_name:
                    results.insert(0, {
                        'code': code,
                        'name': info['name'],
                        'market': info.get('market', ''),
                        'sector': info.get('sector', ''),
                        'match_type': 'exact'
                    })
                # 시작하는 경우
                elif company_name.startswith(query):
                    results.append({
                        'code': code,
                        'name': info['name'],
                        'market': info.get('market', ''),
                        'sector': info.get('sector', ''),
                        'match_type': 'start'
                    })
                # 포함하는 경우
                elif query in company_name:
                    results.append({
                        'code': code,
                        'name': info['name'],
                        'market': info.get('market', ''),
                        'sector': info.get('sector', ''),
                        'match_type': 'contain'
                    })
            
            # 최대 결과 수 제한
            return results[:max_results]
            
        except Exception as e:
            self.logger.error(f"Search failed: {e}")
            return []
    
    def search_by_code(self, code):
        """종목 코드로 검색"""
        try:
            code = str(code).zfill(6)
            
            if not DataValidator.is_korean_stock(code):
                return None
            
            if code in self.stocks_data:
                return {
                    'code': code,
                    'name': self.stocks_data[code]['name'],
                    'market': self.stocks_data[code].get('market', ''),
                    'sector': self.stocks_data[code].get('sector', ''),
                    'industry': self.stocks_data[code].get('industry', ''),
                    'listing_date': self.stocks_data[code].get('listing_date', ''),
                    'market_cap': self.stocks_data[code].get('market_cap', ''),
                    'stocks': self.stocks_data[code].get('stocks', '')
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Code search failed: {e}")
            return None
    
    def get_company_name(self, code):
        """종목 코드로 회사명만 가져오기"""
        info = self.search_by_code(code)
        return info['name'] if info else code
    
    def get_all_codes(self):
        """모든 종목 코드 목록 반환"""
        return list(self.stocks_data.keys())
    
    def get_market_list(self):
        """시장 목록 반환"""
        markets = set()
        for info in self.stocks_data.values():
            market = info.get('market', '')
            if market:
                markets.add(market)
        return sorted(list(markets))
    
    def get_sector_list(self):
        """섹터 목록 반환"""
        sectors = set()
        for info in self.stocks_data.values():
            sector = info.get('sector', '')
            if sector:
                sectors.add(sector)
        return sorted(list(sectors))
    
    def filter_by_market(self, market):
        """시장별 필터링"""
        try:
            results = []
            for code, info in self.stocks_data.items():
                if info.get('market', '') == market:
                    results.append({
                        'code': code,
                        'name': info['name'],
                        'market': info.get('market', ''),
                        'sector': info.get('sector', '')
                    })
            return results
        except Exception as e:
            self.logger.error(f"Market filter failed: {e}")
            return []
    
    def filter_by_sector(self, sector):
        """섹터별 필터링"""
        try:
            results = []
            for code, info in self.stocks_data.items():
                if info.get('sector', '') == sector:
                    results.append({
                        'code': code,
                        'name': info['name'],
                        'market': info.get('market', ''),
                        'sector': info.get('sector', '')
                    })
            return results
        except Exception as e:
            self.logger.error(f"Sector filter failed: {e}")
            return []
    
    def get_stock_count(self):
        """등록된 주식 수 반환"""
        return len(self.stocks_data)
    
    def is_valid_code(self, code):
        """유효한 종목 코드인지 확인"""
        try:
            code = str(code).zfill(6)
            return code in self.stocks_data
        except:
            return False

class KoreanStockSearchDialog:
    """한국 주식 검색 다이얼로그"""
    
    def __init__(self, parent, stock_manager):
        self.parent = parent
        self.stock_manager = stock_manager
        self.selected_code = None
        self.selected_name = None
        self.create_dialog()
    
    def create_dialog(self):
        """검색 다이얼로그 생성"""
        self.dialog = tk.Toplevel(self.parent)
        self.dialog.title("🇰🇷 한국 주식 검색")
        self.dialog.geometry("800x600")
        self.dialog.transient(self.parent)
        self.dialog.grab_set()
        
        # 메인 프레임
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(main_frame, text="🇰🇷 한국 주식 종목 검색", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 검색 프레임
        search_frame = ttk.LabelFrame(main_frame, text="검색", padding="15")
        search_frame.pack(fill=tk.X, pady=(0, 15))
        
        # 검색 입력
        search_input_frame = tk.Frame(search_frame)
        search_input_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(search_input_frame, text="회사명 또는 종목코드:", 
                 font=('Segoe UI', 12)).pack(side=tk.LEFT)
        
        self.search_var = tk.StringVar()
        self.search_entry = ttk.Entry(search_input_frame, textvariable=self.search_var, 
                                     font=('Segoe UI', 12), width=30)
        self.search_entry.pack(side=tk.LEFT, padx=(10, 10), fill=tk.X, expand=True)
        
        search_button = ttk.Button(search_input_frame, text="🔍 검색", 
                                  command=self.search_stocks)
        search_button.pack(side=tk.RIGHT)
        
        # Enter 키 바인딩
        self.search_entry.bind('<Return>', lambda e: self.search_stocks())
        self.search_entry.focus()
        
        # 필터 프레임
        filter_frame = tk.Frame(search_frame)
        filter_frame.pack(fill=tk.X)
        
        # 시장 필터
        ttk.Label(filter_frame, text="시장:", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.market_var = tk.StringVar(value="전체")
        market_combo = ttk.Combobox(filter_frame, textvariable=self.market_var, 
                                   values=["전체"] + self.stock_manager.get_market_list(),
                                   state="readonly", width=15)
        market_combo.pack(side=tk.LEFT, padx=(5, 15))
        market_combo.bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # 섹터 필터
        ttk.Label(filter_frame, text="섹터:", font=('Segoe UI', 10)).pack(side=tk.LEFT)
        self.sector_var = tk.StringVar(value="전체")
        sector_combo = ttk.Combobox(filter_frame, textvariable=self.sector_var,
                                   values=["전체"] + self.stock_manager.get_sector_list(),
                                   state="readonly", width=20)
        sector_combo.pack(side=tk.LEFT, padx=(5, 0))
        sector_combo.bind('<<ComboboxSelected>>', self.on_filter_changed)
        
        # 결과 프레임
        result_frame = ttk.LabelFrame(main_frame, text="검색 결과", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # 결과 트리뷰
        columns = ('Code', 'Name', 'Market', 'Sector')
        self.result_tree = ttk.Treeview(result_frame, columns=columns, show='headings', height=15)
        
        # 컬럼 설정
        self.result_tree.heading('Code', text='종목코드')
        self.result_tree.heading('Name', text='회사명')
        self.result_tree.heading('Market', text='시장')
        self.result_tree.heading('Sector', text='섹터')
        
        self.result_tree.column('Code', width=100, anchor='center')
        self.result_tree.column('Name', width=250, anchor='w')
        self.result_tree.column('Market', width=80, anchor='center')
        self.result_tree.column('Sector', width=150, anchor='center')
        
        # 스크롤바
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_tree.yview)
        self.result_tree.configure(yscrollcommand=scrollbar.set)
        
        self.result_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 더블클릭 이벤트
        self.result_tree.bind('<Double-1>', self.on_item_double_click)
        
        # 버튼 프레임
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="✅ 선택", 
                  command=self.select_stock).pack(side=tk.LEFT)
        ttk.Button(button_frame, text="❌ 취소", 
                  command=self.dialog.destroy).pack(side=tk.RIGHT)
        
        # 상태 표시
        self.status_label = ttk.Label(main_frame, 
                                     text=f"총 {self.stock_manager.get_stock_count():,}개 종목이 등록되어 있습니다.",
                                     font=('Segoe UI', 10), foreground='gray')
        self.status_label.pack(pady=(10, 0))
        
        # 초기 검색 (전체 목록)
        self.show_all_stocks()
    
    def search_stocks(self):
        """주식 검색"""
        try:
            query = self.search_var.get().strip()
            
            if not query:
                self.show_all_stocks()
                return
            
            # 종목 코드로 검색 (6자리 숫자)
            if query.isdigit() and len(query) <= 6:
                code_result = self.stock_manager.search_by_code(query.zfill(6))
                if code_result:
                    results = [code_result]
                else:
                    results = []
            else:
                # 회사명으로 검색
                results = self.stock_manager.search_by_name(query, max_results=50)
            
            self.display_results(results)
            
        except Exception as e:
            messagebox.showerror("검색 오류", f"검색 중 오류가 발생했습니다: {e}")
    
    def on_filter_changed(self, event=None):
        """필터 변경 시 호출"""
        try:
            market = self.market_var.get()
            sector = self.sector_var.get()
            
            if market == "전체" and sector == "전체":
                self.show_all_stocks()
                return
            
            results = []
            
            if market != "전체":
                market_results = self.stock_manager.filter_by_market(market)
                if sector != "전체":
                    # 시장과 섹터 둘 다 필터링
                    results = [r for r in market_results if r.get('sector', '') == sector]
                else:
                    results = market_results
            elif sector != "전체":
                results = self.stock_manager.filter_by_sector(sector)
            
            self.display_results(results)
            
        except Exception as e:
            messagebox.showerror("필터 오류", f"필터 적용 중 오류가 발생했습니다: {e}")
    
    def show_all_stocks(self, limit=100):
        """전체 주식 목록 표시 (제한된 수량)"""
        try:
            all_codes = self.stock_manager.get_all_codes()
            results = []
            
            for i, code in enumerate(all_codes):
                if i >= limit:
                    break
                
                info = self.stock_manager.search_by_code(code)
                if info:
                    results.append(info)
            
            self.display_results(results)
            
            if len(all_codes) > limit:
                self.status_label.config(
                    text=f"처음 {limit}개 종목을 표시 중 (전체: {len(all_codes):,}개)"
                )
            
        except Exception as e:
            messagebox.showerror("목록 오류", f"목록 표시 중 오류가 발생했습니다: {e}")
    
    def display_results(self, results):
        """검색 결과 표시"""
        try:
            # 기존 결과 제거
            for item in self.result_tree.get_children():
                self.result_tree.delete(item)
            
            # 새 결과 추가
            for result in results:
                self.result_tree.insert('', 'end', values=(
                    result['code'],
                    result['name'],
                    result.get('market', ''),
                    result.get('sector', '')
                ))
            
            # 상태 업데이트
            self.status_label.config(text=f"검색 결과: {len(results)}개")
            
        except Exception as e:
            messagebox.showerror("표시 오류", f"결과 표시 중 오류가 발생했습니다: {e}")
    
    def on_item_double_click(self, event):
        """아이템 더블클릭 시 선택"""
        self.select_stock()
    
    def select_stock(self):
        """선택된 주식 반환"""
        try:
            selection = self.result_tree.selection()
            if not selection:
                messagebox.showwarning("선택 필요", "종목을 선택해주세요.")
                return
            
            item = self.result_tree.item(selection[0])
            values = item['values']
            
            self.selected_code = values[0]
            self.selected_name = values[1]
            
            self.dialog.destroy()
            
        except Exception as e:
            messagebox.showerror("선택 오류", f"종목 선택 중 오류가 발생했습니다: {e}")
    
    def get_selected(self):
        """선택된 종목 정보 반환"""
        return self.selected_code, self.selected_name

def show_korean_stock_search_dialog(parent):
    """한국 주식 검색 다이얼로그 표시"""
    try:
        stock_manager = KoreanStockManager()
        if stock_manager.get_stock_count() == 0:
            messagebox.showerror("데이터 없음", 
                               "한국 주식 데이터가 없습니다.\nkrx_stock_list.csv 파일을 확인해주세요.")
            return None, None
        
        dialog = KoreanStockSearchDialog(parent, stock_manager)
        parent.wait_window(dialog.dialog)
        
        return dialog.get_selected()
        
    except Exception as e:
        messagebox.showerror("검색 다이얼로그 오류", f"검색 다이얼로그를 열 수 없습니다: {e}")
        return None, None