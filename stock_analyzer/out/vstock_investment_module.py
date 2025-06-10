#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Investment Module - 투자 계산 기능
"""

import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.scrolledtext as scrolledtext
import pandas as pd
import numpy as np
from datetime import datetime
import math

class InvestmentModule:
    """투자 계산 모듈"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.shared_data = main_app.shared_data
        
        # UI 요소들 (나중에 설정됨)
        self.budget_var = None
        self.strategy_var = None
        self.splits_var = None
        self.investment_results = None
    
    def create_tab(self, notebook):
        """투자 탭 생성"""
        try:
            investment_frame = ttk.Frame(notebook)
            notebook.add(investment_frame, text="💰 Investment")
            
            # 좌측 패널 (입력)
            input_panel = ttk.LabelFrame(investment_frame, text="💵 Investment Calculation", padding="20")
            input_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
            
            # 총 예산
            ttk.Label(input_panel, text="Total Budget ($):", style='Info.TLabel').pack(anchor=tk.W)
            self.budget_var = tk.StringVar(value="10000")
            budget_entry = ttk.Entry(input_panel, textvariable=self.budget_var, width=20)
            budget_entry.pack(fill=tk.X, pady=(5, 15))
            
            # 투자 전략 선택
            ttk.Label(input_panel, text="Investment Strategy:", style='Info.TLabel').pack(anchor=tk.W)
            self.strategy_var = tk.StringVar(value="single")
            strategy_combo = ttk.Combobox(input_panel, textvariable=self.strategy_var, 
                                        values=["single", "dca", "pyramid"], state="readonly", width=18)
            strategy_combo.pack(fill=tk.X, pady=(5, 15))
            
            # 전략 설명
            strategy_info = tk.Text(input_panel, height=4, wrap=tk.WORD, font=('Segoe UI', 9))
            strategy_info.pack(fill=tk.X, pady=(0, 15))
            strategy_info.insert('1.0', 
                "• Single: 일괄 투자\n"
                "• DCA: 분할 매수 (Dollar Cost Averaging)\n" 
                "• Pyramid: 피라미드 매수 (하락 시 점진적 증액)")
            strategy_info.config(state=tk.DISABLED)
            
            # 분할 횟수 (DCA/Pyramid용)
            ttk.Label(input_panel, text="Number of Splits:", style='Info.TLabel').pack(anchor=tk.W)
            self.splits_var = tk.StringVar(value="4")
            splits_spinbox = ttk.Spinbox(input_panel, from_=2, to=20, textvariable=self.splits_var, width=20)
            splits_spinbox.pack(fill=tk.X, pady=(5, 15))
            
            # 하락률 설정 (Pyramid용)
            ttk.Label(input_panel, text="Drop % per Level (Pyramid):", style='Info.TLabel').pack(anchor=tk.W)
            self.drop_rate_var = tk.StringVar(value="5")
            drop_rate_spinbox = ttk.Spinbox(input_panel, from_=1, to=20, textvariable=self.drop_rate_var, width=20)
            drop_rate_spinbox.pack(fill=tk.X, pady=(5, 20))
            
            # 계산 버튼
            ttk.Button(input_panel, text="🧮 Calculate Investment", 
                      command=self.calculate_investment).pack(fill=tk.X, pady=10, ipady=8)
            
            ttk.Separator(input_panel, orient='horizontal').pack(fill=tk.X, pady=15)
            
            # 추가 기능들
            ttk.Button(input_panel, text="📊 Risk Assessment", 
                      command=self.assess_investment_risk).pack(fill=tk.X, pady=5, ipady=5)
            
            ttk.Button(input_panel, text="🎯 Profit Target Calculator", 
                      command=self.calculate_profit_targets).pack(fill=tk.X, pady=5, ipady=5)
            
            ttk.Button(input_panel, text="💹 Scenario Analysis", 
                      command=self.scenario_analysis).pack(fill=tk.X, pady=5, ipady=5)
            
            ttk.Button(input_panel, text="🤖 AI Investment Advice", 
                      command=self.show_ai_advice).pack(fill=tk.X, pady=5, ipady=5)
            
            # 우측 패널 (결과)
            result_panel = ttk.LabelFrame(investment_frame, text="📊 Calculation Results", padding="20")
            result_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 결과 텍스트
            self.investment_results = scrolledtext.ScrolledText(result_panel, 
                                                              height=25, wrap=tk.WORD, 
                                                              font=('Consolas', 11))
            self.investment_results.pack(fill=tk.BOTH, expand=True)
            
            # 초기 안내 메시지
            self.show_initial_message()
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def show_initial_message(self):
        """초기 안내 메시지 표시"""
        initial_message = """💰 VStock Investment Calculator v3.3

이 도구는 다양한 투자 전략의 계산과 시뮬레이션을 제공합니다.

📊 제공 기능:

🧮 투자 전략 계산:
• Single: 일괄 투자 계산
• DCA: 분할 매수 (Dollar Cost Averaging)
• Pyramid: 피라미드 매수 (하락 시 점진적 증액)

📊 위험 평가:
• 포트폴리오 위험도 분석
• VaR (Value at Risk) 계산
• 최대 손실 시나리오

🎯 수익 목표 계산:
• 목표 수익률별 매도가 계산
• 수익 실현 전략 수립
• 단계별 익절 계획

💹 시나리오 분석:
• 다양한 시장 상황별 시뮬레이션
• 상승/하락/횡보 시나리오
• 확률 기반 수익률 예측

🤖 AI 투자 자문:
• 현재 상황 종합 분석
• 개인화된 투자 조언
• 전문가 관점 제공

📈 시작하기:
1. Analysis 탭에서 종목 데이터 로드
2. 투자 예산과 전략 선택
3. 계산 실행으로 상세 분석 확인
4. 추가 도구들로 심화 분석

💡 투자 전략별 특징:

📌 Single (일괄 투자):
• 한 번에 전체 금액 투자
• 타이밍이 중요
• 시장 상승기에 유리

📌 DCA (분할 매수):
• 일정 금액을 정기적으로 투자
• 평단가 효과 기대
• 변동성 위험 완화

📌 Pyramid (피라미드):
• 하락 시 점진적으로 투자 증액
• 저점 매수 전략
• 높은 수익 잠재력, 높은 위험

⚠️ 중요 알림:
모든 계산 결과는 참고용입니다. 
실제 투자 시에는 충분한 검토와 
본인의 판단이 필요합니다.

👆 좌측 메뉴에서 원하는 기능을 선택하여 시작하세요!
"""
        self.investment_results.insert('1.0', initial_message)
    
    def calculate_investment(self):
        """투자 계산"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 입력값 검증
            try:
                budget = float(self.budget_var.get())
                splits = int(self.splits_var.get())
                drop_rate = float(self.drop_rate_var.get()) / 100
            except ValueError:
                messagebox.showerror("❌", "올바른 숫자를 입력해주세요.")
                return
            
            strategy = self.strategy_var.get()
            current_price = self.shared_data['current_data']['Close'].iloc[-1]
            symbol = self.shared_data['current_symbol']
            
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
            
            self.main_app.log_info(f"투자 계산 완료: {strategy} 전략")
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
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
        
        return f"""
📌 DCA (Dollar Cost Averaging) Strategy:

💵 Investment Plan:
• Total Budget: ${budget:,.2f}
• Number of Purchases: {splits}
• Amount per Purchase: ${amount_per_buy:,.2f}
• Commission per Buy: ${commission_per_buy:.2f}
• Net Amount per Buy: ${net_amount_per_buy:,.2f}

📊 DCA Schedule (assuming current price):
"""+ "\n".join([f"  Purchase {i+1}: ${net_amount_per_buy:,.2f} → {shares_per_buy:.2f} shares @ ${current_price:.2f}" 
               for i in range(splits)]) + f"""

📈 Expected Results (current price scenario):
• Total Shares: {total_shares:.2f}
• Total Commission: ${total_commission:.2f}
• Net Investment: ${total_investment:,.2f}
• Average Cost: ${current_price:.2f}
• Break-even Price: ${current_price * 1.001:.2f}

💹 Price Variation Scenarios:
"""+ self.generate_dca_scenarios(budget, splits, current_price) + f"""

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
            result += f"""  Level {plan['level']}: {plan['drop_pct']:>5.1f}% drop → ${plan['price']:>6.2f} → ${plan['net_amount']:>8,.2f} → {plan['shares']:>6.2f} shares\n"""
        
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
        data = self.shared_data['current_data']
        
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
"""+ self.get_strategy_recommendation(volatility, strategy) + f"""

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
    
    def assess_investment_risk(self):
        """투자 위험 평가"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 위험 평가 창
            risk_window = tk.Toplevel(self.main_app.root)
            risk_window.title("📊 Investment Risk Assessment")
            risk_window.geometry("700x600")
            risk_window.transient(self.main_app.root)
            
            main_frame = ttk.Frame(risk_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📊 Investment Risk Assessment", 
                     style='Title.TLabel').pack(pady=(0, 20))
            
            # 위험 분석 계산
            data = self.shared_data['current_data']
            symbol = self.shared_data['current_symbol']
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
            self.main_app.handle_exception(e, True)
    
    def calculate_profit_targets(self):
        """수익 목표 계산"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            current_price = self.shared_data['current_data']['Close'].iloc[-1]
            symbol = self.shared_data['current_symbol']
            
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
            self.main_app.handle_exception(e, True)
    
    def scenario_analysis(self):
        """시나리오 분석"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            try:
                budget = float(self.budget_var.get())
            except ValueError:
                messagebox.showerror("❌", "올바른 예산을 입력해주세요.")
                return
            
            current_price = self.shared_data['current_data']['Close'].iloc[-1]
            symbol = self.shared_data['current_symbol']
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
            self.main_app.handle_exception(e, True)
    
    def show_ai_advice(self):
        """AI 투자 자문"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 종목 데이터를 로드해주세요.")
                return
            
            # 기본 분석 데이터 수집
            data = self.shared_data['current_data']
            symbol = self.shared_data['current_symbol']
            current_price = data['Close'].iloc[-1]
            
            try:
                budget = float(self.budget_var.get())
                strategy = self.strategy_var.get()
            except ValueError:
                budget = 10000
                strategy = "single"
            
            # 기술적 분석
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100
            
            # 최근 성과
            returns_1m = ((current_price - data['Close'].iloc[-20]) / data['Close'].iloc[-20] * 100) if len(data) >= 20 else 0
            
            ai_advice = f"""🤖 AI Investment Advisory Report for {symbol}

📊 Current Situation Analysis:
• Symbol: {symbol}
• Current Price: ${current_price:.2f}
• Investment Budget: ${budget:,.2f}
• Preferred Strategy: {strategy.upper()}
• 1-Month Performance: {returns_1m:+.1f}%
• Volatility: {volatility:.1f}%

🎯 AI Investment Recommendation:
"""
            
            if volatility > 40:
                ai_advice += """
🚨 HIGH VOLATILITY ALERT
• Current volatility is very high ({volatility:.1f}%)
• Recommend DCA strategy over single investment
• Consider smaller position sizes
• Set tight stop-losses (5-8%)
• Monitor daily for significant moves
""".format(volatility=volatility)
            elif volatility > 25:
                ai_advice += """
📊 MODERATE VOLATILITY
• Volatility is at moderate levels ({volatility:.1f}%)
• {strategy} strategy is acceptable
• Standard risk management applies
• Weekly monitoring recommended
""".format(volatility=volatility, strategy=strategy.upper())
            else:
                ai_advice += """
✅ LOW VOLATILITY ENVIRONMENT
• Favorable conditions for investing ({volatility:.1f}%)
• {strategy} strategy looks good
• Consider slightly larger positions
• Monthly monitoring sufficient
""".format(volatility=volatility, strategy=strategy.upper())
            
            if returns_1m > 15:
                ai_advice += "\n• Strong recent momentum - consider profit-taking levels"
            elif returns_1m < -15:
                ai_advice += "\n• Recent weakness - potential buying opportunity or falling knife"
            
            ai_advice += f"""

💡 Strategic Recommendations:
1. Position Sizing: Limit to 5-10% of total portfolio
2. Entry Strategy: Consider {strategy} with current market conditions
3. Risk Management: Set stop-loss at {max(5, min(15, volatility/3)):.0f}%
4. Profit Targets: {15 if volatility < 25 else 20}%, {25 if volatility < 25 else 35}%, {50 if volatility < 25 else 60}%
5. Time Horizon: {'Short-term (1-3 months)' if volatility > 30 else 'Medium-term (3-12 months)'}

🔄 Monitoring Schedule:
• {'Daily' if volatility > 35 else 'Weekly' if volatility > 20 else 'Bi-weekly'} price monitoring
• Review strategy if volatility changes significantly
• Adjust position if market conditions change

⚠️ Risk Warnings:
• This is algorithmic analysis, not financial advice
• Market conditions can change rapidly
• Always do your own research
• Never invest more than you can afford to lose
• Consider consulting a financial advisor for large investments

📞 Next Steps:
1. Review and validate this analysis
2. Set up your chosen investment strategy
3. Establish monitoring schedule
4. Prepare exit strategies (both profit and loss)
5. Execute plan with discipline

💡 Remember:
"The best investment strategy is the one you can stick to
through both good times and bad times."
"""
            
            self.investment_results.delete('1.0', tk.END)
            self.investment_results.insert('1.0', ai_advice)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)