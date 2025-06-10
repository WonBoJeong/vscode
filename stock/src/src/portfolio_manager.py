#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
포트폴리오 관리 모듈
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
from pathlib import Path

class PortfolioManager:
    def __init__(self):
        """포트폴리오 관리자 초기화"""
        self.holdings = {}
        self.transactions = []
        self.portfolio_file = Path("config/portfolio.json")
        self.load_portfolio()
        
    def load_portfolio(self):
        """포트폴리오 데이터 로드"""
        try:
            if self.portfolio_file.exists():
                with open(self.portfolio_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.holdings = data.get('holdings', {})
                    self.transactions = data.get('transactions', [])
        except Exception as e:
            print(f"포트폴리오 로드 실패: {e}")
            
    def save_portfolio(self):
        """포트폴리오 데이터 저장"""
        try:
            self.portfolio_file.parent.mkdir(exist_ok=True)
            data = {
                'holdings': self.holdings,
                'transactions': self.transactions,
                'last_updated': datetime.now().isoformat()
            }
            with open(self.portfolio_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"포트폴리오 저장 실패: {e}")
            
    def add_transaction(self, symbol, action, quantity, price, date=None):
        """거래 기록 추가"""
        if date is None:
            date = datetime.now().isoformat()
            
        transaction = {
            'symbol': symbol.upper(),
            'action': action.upper(),  # BUY, SELL
            'quantity': float(quantity),
            'price': float(price),
            'date': date,
            'total': float(quantity) * float(price)
        }
        
        self.transactions.append(transaction)
        self._update_holdings(transaction)
        self.save_portfolio()
        
    def _update_holdings(self, transaction):
        """보유 종목 업데이트"""
        symbol = transaction['symbol']
        action = transaction['action']
        quantity = transaction['quantity']
        price = transaction['price']
        
        if symbol not in self.holdings:
            self.holdings[symbol] = {
                'quantity': 0,
                'avg_price': 0,
                'total_cost': 0
            }
            
        holding = self.holdings[symbol]
        
        if action == 'BUY':
            # 매수
            new_quantity = holding['quantity'] + quantity
            new_total_cost = holding['total_cost'] + (quantity * price)
            new_avg_price = new_total_cost / new_quantity if new_quantity > 0 else 0
            
            holding['quantity'] = new_quantity
            holding['avg_price'] = new_avg_price
            holding['total_cost'] = new_total_cost
            
        elif action == 'SELL':
            # 매도
            if holding['quantity'] >= quantity:
                holding['quantity'] -= quantity
                if holding['quantity'] == 0:
                    holding['avg_price'] = 0
                    holding['total_cost'] = 0
                else:
                    holding['total_cost'] = holding['quantity'] * holding['avg_price']
            else:
                print(f"경고: {symbol} 보유량({holding['quantity']})보다 많은 매도 시도")
                
    def get_portfolio_summary(self, current_prices=None):
        """포트폴리오 요약 정보"""
        if current_prices is None:
            current_prices = {}
            
        summary = {
            'total_symbols': len([h for h in self.holdings.values() if h['quantity'] > 0]),
            'total_cost': 0,
            'current_value': 0,
            'total_gain_loss': 0,
            'total_return_pct': 0,
            'holdings': []
        }
        
        for symbol, holding in self.holdings.items():
            if holding['quantity'] > 0:
                current_price = current_prices.get(symbol, holding['avg_price'])
                current_value = holding['quantity'] * current_price
                gain_loss = current_value - holding['total_cost']
                return_pct = (gain_loss / holding['total_cost'] * 100) if holding['total_cost'] > 0 else 0
                
                holding_summary = {
                    'symbol': symbol,
                    'quantity': holding['quantity'],
                    'avg_price': holding['avg_price'],
                    'current_price': current_price,
                    'total_cost': holding['total_cost'],
                    'current_value': current_value,
                    'gain_loss': gain_loss,
                    'return_pct': return_pct
                }
                
                summary['holdings'].append(holding_summary)
                summary['total_cost'] += holding['total_cost']
                summary['current_value'] += current_value
                
        summary['total_gain_loss'] = summary['current_value'] - summary['total_cost']
        summary['total_return_pct'] = (summary['total_gain_loss'] / summary['total_cost'] * 100) if summary['total_cost'] > 0 else 0
        
        return summary
        
    def get_transaction_history(self, symbol=None, days=None):
        """거래 내역 조회"""
        transactions = self.transactions.copy()
        
        # 심볼 필터
        if symbol:
            transactions = [t for t in transactions if t['symbol'] == symbol.upper()]
            
        # 기간 필터
        if days:
            cutoff_date = datetime.now() - timedelta(days=days)
            transactions = [t for t in transactions 
                          if datetime.fromisoformat(t['date']) >= cutoff_date]
                          
        # 날짜순 정렬
        transactions.sort(key=lambda x: x['date'], reverse=True)
        
        return transactions
        
    def calculate_portfolio_metrics(self, price_data=None):
        """포트폴리오 성과 지표 계산"""
        if not price_data:
            return None
            
        try:
            # 포트폴리오 가치 시계열 계산
            portfolio_values = []
            dates = []
            
            # 각 날짜별 포트폴리오 가치 계산
            for date in price_data.index:
                daily_value = 0
                for symbol, holding in self.holdings.items():
                    if holding['quantity'] > 0 and symbol in price_data.columns:
                        price = price_data.loc[date, symbol]
                        if not pd.isna(price):
                            daily_value += holding['quantity'] * price
                            
                portfolio_values.append(daily_value)
                dates.append(date)
                
            if not portfolio_values:
                return None
                
            portfolio_series = pd.Series(portfolio_values, index=dates)
            returns = portfolio_series.pct_change().dropna()
            
            # 성과 지표 계산
            metrics = {
                'total_return': (portfolio_series.iloc[-1] / portfolio_series.iloc[0] - 1) * 100,
                'annualized_return': returns.mean() * 252 * 100,
                'volatility': returns.std() * np.sqrt(252) * 100,
                'sharpe_ratio': (returns.mean() * 252) / (returns.std() * np.sqrt(252)) if returns.std() > 0 else 0,
                'max_drawdown': self._calculate_max_drawdown(portfolio_series),
                'var_95': np.percentile(returns, 5) * 100,
                'current_value': portfolio_series.iloc[-1],
                'peak_value': portfolio_series.max(),
                'trough_value': portfolio_series.min()
            }
            
            return metrics
            
        except Exception as e:
            print(f"포트폴리오 지표 계산 오류: {e}")
            return None
            
    def _calculate_max_drawdown(self, series):
        """최대 낙폭 계산"""
        try:
            peak = series.expanding().max()
            drawdown = (series - peak) / peak
            return abs(drawdown.min()) * 100
        except:
            return 0
            
    def get_sector_allocation(self):
        """섹터별 할당 (모의 데이터)"""
        # 실제로는 외부 API에서 섹터 정보를 가져와야 함
        sector_mapping = {
            'AAPL': 'Technology',
            'MSFT': 'Technology', 
            'GOOGL': 'Technology',
            'AMZN': 'Consumer Discretionary',
            'TSLA': 'Consumer Discretionary',
            'META': 'Technology',
            'NVDA': 'Technology',
            'PLTR': 'Technology',
            'VOO': 'ETF',
            'VTV': 'ETF',
            'TQQQ': 'ETF',
            'TNA': 'ETF',
            'SOXL': 'ETF',
            'SCHD': 'ETF',
            'JEPI': 'ETF',
            'JEPQ': 'ETF',
            'TSLL': 'ETF'
        }
        
        sector_allocation = {}
        total_value = 0
        
        for symbol, holding in self.holdings.items():
            if holding['quantity'] > 0:
                sector = sector_mapping.get(symbol, 'Unknown')
                value = holding['quantity'] * holding['avg_price']
                
                if sector not in sector_allocation:
                    sector_allocation[sector] = 0
                    
                sector_allocation[sector] += value
                total_value += value
                
        # 비율로 변환
        if total_value > 0:
            for sector in sector_allocation:
                sector_allocation[sector] = (sector_allocation[sector] / total_value) * 100
                
        return sector_allocation
        
    def export_to_csv(self, filename=None):
        """포트폴리오 데이터 CSV 내보내기"""
        if filename is None:
            filename = f"portfolio_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
            
        try:
            # 보유 종목 데이터
            holdings_data = []
            for symbol, holding in self.holdings.items():
                if holding['quantity'] > 0:
                    holdings_data.append({
                        'Symbol': symbol,
                        'Quantity': holding['quantity'],
                        'Average_Price': holding['avg_price'],
                        'Total_Cost': holding['total_cost']
                    })
                    
            holdings_df = pd.DataFrame(holdings_data)
            
            # 거래 내역 데이터
            transactions_df = pd.DataFrame(self.transactions)
            
            # Excel 파일로 저장 (다중 시트)
            with pd.ExcelWriter(filename.replace('.csv', '.xlsx')) as writer:
                holdings_df.to_excel(writer, sheet_name='Holdings', index=False)
                transactions_df.to_excel(writer, sheet_name='Transactions', index=False)
                
            print(f"포트폴리오 데이터 내보내기 완료: {filename}")
            return True
            
        except Exception as e:
            print(f"포트폴리오 내보내기 실패: {e}")
            return False
            
    def import_from_csv(self, filename):
        """CSV에서 포트폴리오 데이터 가져오기"""
        try:
            # Excel 파일에서 거래 내역 읽기
            transactions_df = pd.read_excel(filename, sheet_name='Transactions')
            
            # 기존 데이터 초기화
            self.holdings = {}
            self.transactions = []
            
            # 거래 내역 복원
            for _, row in transactions_df.iterrows():
                self.add_transaction(
                    symbol=row['symbol'],
                    action=row['action'],
                    quantity=row['quantity'],
                    price=row['price'],
                    date=row['date']
                )
                
            print(f"포트폴리오 데이터 가져오기 완료: {filename}")
            return True
            
        except Exception as e:
            print(f"포트폴리오 가져오기 실패: {e}")
            return False
            
    def rebalance_portfolio(self, target_allocation, current_prices=None):
        """포트폴리오 리밸런싱 제안"""
        """
        target_allocation: {'AAPL': 20, 'MSFT': 30, ...} (비율)
        """
        if current_prices is None:
            current_prices = {}
            
        try:
            # 현재 포트폴리오 가치 계산
            total_value = 0
            current_allocation = {}
            
            for symbol, holding in self.holdings.items():
                if holding['quantity'] > 0:
                    current_price = current_prices.get(symbol, holding['avg_price'])
                    value = holding['quantity'] * current_price
                    total_value += value
                    current_allocation[symbol] = value
                    
            # 현재 비율 계산
            for symbol in current_allocation:
                current_allocation[symbol] = (current_allocation[symbol] / total_value) * 100
                
            # 리밸런싱 제안 계산
            rebalance_suggestions = []
            
            for symbol, target_pct in target_allocation.items():
                current_pct = current_allocation.get(symbol, 0)
                target_value = total_value * (target_pct / 100)
                current_value = current_allocation.get(symbol, 0) * total_value / 100
                
                difference = target_value - current_value
                current_price = current_prices.get(symbol, self.holdings.get(symbol, {}).get('avg_price', 100))
                
                if abs(difference) > total_value * 0.01:  # 1% 이상 차이시에만 제안
                    action = 'BUY' if difference > 0 else 'SELL'
                    quantity = abs(difference) / current_price
                    
                    rebalance_suggestions.append({
                        'symbol': symbol,
                        'action': action,
                        'quantity': round(quantity, 2),
                        'price': current_price,
                        'current_pct': round(current_pct, 2),
                        'target_pct': target_pct,
                        'difference_value': round(difference, 2)
                    })
                    
            return rebalance_suggestions
            
        except Exception as e:
            print(f"리밸런싱 계산 오류: {e}")
            return None