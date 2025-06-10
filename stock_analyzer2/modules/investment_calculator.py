#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Investment Calculator Module
투자 계산기 모듈

Author: AI Assistant & User
Version: 1.0.0
"""

import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from config import INVESTMENT_CONFIG, LEVERAGE_ETFS
from .utils import Logger, format_currency, format_percentage, DataValidator, format_currency_auto

class InvestmentCalculator:
    """투자 계산기 클래스"""
    
    def __init__(self):
        self.logger = Logger("InvestmentCalculator")
        self.commission_rate = INVESTMENT_CONFIG['commission_rate']
    
    def calculate_single_investment(self, budget, current_price):
        """일괄 투자 계산"""
        try:
            commission = budget * self.commission_rate
            net_budget = budget - commission
            shares = net_budget / current_price
            
            result = {
                'strategy': 'single',
                'budget': budget,
                'commission': commission,
                'net_budget': net_budget,
                'current_price': current_price,
                'shares': shares,
                'total_value': shares * current_price,
                'average_cost': current_price,
                'break_even_price': current_price * (1 + self.commission_rate),
                'profit_targets': self._calculate_profit_targets(current_price, shares),
                'stop_losses': self._calculate_stop_losses(current_price, shares),
                'summary': f"투자로 {shares:.2f}주 매수"
            }
            
            self.logger.info(f"Single investment calculated: {shares:.2f} shares at {current_price}")
            return result
            
        except Exception as e:
            self.logger.error(f"Single investment calculation failed: {e}")
            return None
    
    def calculate_dca_investment(self, budget, current_price, splits):
        """분할매수 (DCA) 계산"""
        try:
            amount_per_buy = budget / splits
            commission_per_buy = amount_per_buy * self.commission_rate
            net_amount_per_buy = amount_per_buy - commission_per_buy
            shares_per_buy = net_amount_per_buy / current_price
            
            total_shares = shares_per_buy * splits
            total_commission = commission_per_buy * splits
            total_investment = budget - total_commission
            
            # DCA 시나리오 분석
            scenarios = self._generate_dca_scenarios(budget, current_price, splits)
            
            result = {
                'strategy': 'dca',
                'budget': budget,
                'splits': splits,
                'amount_per_buy': amount_per_buy,
                'commission_per_buy': commission_per_buy,
                'net_amount_per_buy': net_amount_per_buy,
                'shares_per_buy': shares_per_buy,
                'total_shares': total_shares,
                'total_commission': total_commission,
                'total_investment': total_investment,
                'average_cost': current_price,
                'break_even_price': current_price * (1 + self.commission_rate),
                'scenarios': scenarios,
                'summary': f"{splits}회 분할로 총 {total_shares:.2f}주 매수 예정"
            }
            
            self.logger.info(f"DCA investment calculated: {splits} splits, {total_shares:.2f} total shares")
            return result
            
        except Exception as e:
            self.logger.error(f"DCA investment calculation failed: {e}")
            return None
    
    def calculate_pyramid_investment(self, budget, current_price, splits, drop_rate):
        """피라미드 투자 계산"""
        try:
            # 피라미드: 하락할수록 더 많이 투자
            total_weight = sum(i+1 for i in range(splits))
            
            pyramid_plan = []
            total_invested = 0
            total_shares = 0
            
            for i in range(splits):
                weight = i + 1
                amount = (budget * weight) / total_weight
                price = current_price * (1 - drop_rate * i)
                commission = amount * self.commission_rate
                net_amount = amount - commission
                shares = net_amount / price
                
                pyramid_plan.append({
                    'level': i + 1,
                    'drop_pct': drop_rate * i * 100,
                    'price': price,
                    'amount': amount,
                    'net_amount': net_amount,
                    'shares': shares,
                    'cumulative_shares': total_shares + shares,
                    'cumulative_investment': total_invested + net_amount
                })
                
                total_invested += net_amount
                total_shares += shares
            
            avg_cost = total_invested / total_shares if total_shares > 0 else 0
            
            result = {
                'strategy': 'pyramid',
                'budget': budget,
                'splits': splits,
                'drop_rate': drop_rate,
                'current_price': current_price,
                'pyramid_plan': pyramid_plan,
                'total_shares': total_shares,
                'total_investment': total_invested,
                'average_cost': avg_cost,
                'break_even_price': avg_cost * (1 + self.commission_rate),
                'profit_targets': self._calculate_profit_targets(avg_cost, total_shares),
                'summary': f"피라미드 {splits}단계로 평균단가"
            }
            
            self.logger.info(f"Pyramid investment calculated: {splits} levels, avg cost {avg_cost}")
            return result
            
        except Exception as e:
            self.logger.error(f"Pyramid investment calculation failed: {e}")
            return None
    
    def _calculate_profit_targets(self, entry_price, shares):
        """수익 목표 계산"""
        targets = []
        profit_levels = [0.05, 0.10, 0.15, 0.20, 0.30, 0.50]
        
        for level in profit_levels:
            target_price = entry_price * (1 + level)
            profit_amount = shares * entry_price * level
            targets.append({
                'percentage': level * 100,
                'price': target_price,
                'profit': profit_amount
            })
        
        return targets
    
    def _calculate_stop_losses(self, entry_price, shares):
        """손절 레벨 계산"""
        stops = []
        loss_levels = [0.05, 0.10, 0.15, 0.20]
        
        for level in loss_levels:
            stop_price = entry_price * (1 - level)
            loss_amount = shares * entry_price * level
            stops.append({
                'percentage': level * 100,
                'price': stop_price,
                'loss': loss_amount
            })
        
        return stops
    
    def _generate_dca_scenarios(self, budget, current_price, splits):
        """DCA 시나리오 생성"""
        scenarios = [
            ("정체 시장", [0, 0, 0, 0]),
            ("상승 시장", [5, 10, 15, 20]),
            ("하락 시장", [-5, -10, -15, -20]),
            ("변동성 시장", [10, -5, 15, -10])
        ]
        
        results = []
        amount_per_buy = budget / splits
        commission_per_buy = amount_per_buy * self.commission_rate
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
                
                results.append({
                    'scenario': scenario_name,
                    'avg_cost': avg_cost,
                    'total_shares': total_shares,
                    'current_value': current_value,
                    'profit_loss': profit_loss,
                    'profit_loss_pct': profit_loss_pct
                })
        
        return results
    
    def assess_investment_risk(self, data, budget):
        """투자 위험 평가"""
        try:
            if data is None or data.empty:
                return None
            
            # 변동성 계산
            returns = data['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100
            
            # VaR 계산
            var_95 = np.percentile(returns, 5) * 100 if len(returns) > 0 else 0
            var_99 = np.percentile(returns, 1) * 100 if len(returns) > 0 else 0
            
            # 최대 낙폭
            rolling_max = data['Close'].expanding().max()
            drawdown = (data['Close'] / rolling_max - 1) * 100
            max_drawdown = drawdown.min()
            
            # 위험도 점수 계산
            risk_score = min(100, abs(var_95) * 5 + volatility * 1.5)
            
            # 위험 등급
            if risk_score < 25:
                risk_level = "낮음"
                recommendation = "보수적 투자자에게 적합"
            elif risk_score < 50:
                risk_level = "보통"
                recommendation = "균형잡힌 포트폴리오에 적합"
            elif risk_score < 75:
                risk_level = "높음"
                recommendation = "경험있는 투자자만 권장"
            else:
                risk_level = "매우 높음"
                recommendation = "고위험 감수 투자자만 권장"
            
            risk_assessment = {
                'volatility': volatility,
                'var_95': var_95,
                'var_99': var_99,
                'max_drawdown': max_drawdown,
                'risk_score': risk_score,
                'risk_level': risk_level,
                'recommendation': recommendation,
                'estimated_loss_95': budget * abs(var_95/100),
                'estimated_loss_99': budget * abs(var_99/100),
                'max_historical_loss': budget * abs(max_drawdown/100)
            }
            
            self.logger.info(f"Risk assessment completed: {risk_level} ({risk_score:.1f})")
            return risk_assessment
            
        except Exception as e:
            self.logger.error(f"Risk assessment failed: {e}")
            return None
    
    def calculate_leverage_etf_strategy(self, symbol, budget, current_price):
        """레버리지 ETF 전용 전략 계산"""
        try:
            is_leverage = any(etf in symbol.upper() for etf in LEVERAGE_ETFS)
            
            if not is_leverage:
                return self.calculate_single_investment(budget, current_price)
            
            # 레버리지 ETF 특별 계산
            # 더 보수적인 접근
            recommended_budget = budget * 0.7  # 70%만 투자 권장
            commission = recommended_budget * self.commission_rate
            net_budget = recommended_budget - commission
            shares = net_budget / current_price
            
            # 레버리지 ETF 위험 요소
            time_decay_monthly = 0.02  # 월 2% 시간가치 손실 추정
            volatility_risk = 1.5  # 일반 주식 대비 1.5배 위험
            
            result = {
                'strategy': 'leverage_etf',
                'original_budget': budget,
                'recommended_budget': recommended_budget,
                'budget_reduction_reason': '레버리지 ETF 위험 관리',
                'commission': commission,
                'net_budget': net_budget,
                'shares': shares,
                'current_price': current_price,
                'time_decay_monthly': time_decay_monthly,
                'volatility_multiplier': volatility_risk,
                'strict_stop_loss': current_price * 0.85,  # 15% 손절
                'max_holding_period': '30일',
                'warning': '레버리지 ETF는 장기보유 부적합',
                'summary': f"레버리지 ETF 특별관리: {shares:.2f}주 (예산의 70%만 투자)"
            }
            
            self.logger.info(f"Leverage ETF strategy calculated for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Leverage ETF strategy calculation failed: {e}")
            return None
    
    def calculate_profit_scenarios(self, entry_price, shares, scenarios=None):
        """수익 시나리오 계산"""
        try:
            if scenarios is None:
                scenarios = [
                    ("강세장 (+30%)", 0.30),
                    ("보통 상승 (+15%)", 0.15),
                    ("소폭 상승 (+5%)", 0.05),
                    ("보합 (0%)", 0.00),
                    ("소폭 하락 (-5%)", -0.05),
                    ("조정 (-15%)", -0.15),
                    ("약세장 (-30%)", -0.30),
                    ("폭락 (-50%)", -0.50)
                ]
            
            results = []
            initial_investment = entry_price * shares
            
            for scenario_name, change in scenarios:
                new_price = entry_price * (1 + change)
                new_value = shares * new_price
                profit_loss = new_value - initial_investment
                profit_loss_pct = (profit_loss / initial_investment) * 100
                
                results.append({
                    'scenario': scenario_name,
                    'price_change': change * 100,
                    'new_price': new_price,
                    'new_value': new_value,
                    'profit_loss': profit_loss,
                    'profit_loss_pct': profit_loss_pct
                })
            
            return results
            
        except Exception as e:
            self.logger.error(f"Profit scenarios calculation failed: {e}")
            return None
    
    def calculate_position_sizing(self, total_portfolio, risk_percentage, volatility):
        """포지션 사이징 계산"""
        try:
            # Kelly Criterion 변형
            max_risk_amount = total_portfolio * (risk_percentage / 100)
            
            # 변동성 기반 조정
            if volatility > 50:
                size_multiplier = 0.5  # 고변동성 시 50% 축소
            elif volatility > 30:
                size_multiplier = 0.7  # 중변동성 시 30% 축소
            else:
                size_multiplier = 1.0   # 정상 사이즈
            
            recommended_amount = max_risk_amount * size_multiplier
            
            result = {
                'total_portfolio': total_portfolio,
                'risk_percentage': risk_percentage,
                'max_risk_amount': max_risk_amount,
                'volatility': volatility,
                'size_multiplier': size_multiplier,
                'recommended_amount': recommended_amount,
                'position_ratio': (recommended_amount / total_portfolio) * 100
            }
            
            return result
            
        except Exception as e:
            self.logger.error(f"Position sizing calculation failed: {e}")
            return None
    
    def generate_investment_report(self, calculation_result, symbol, company_name=None):
        """투자 계산 리포트 생성"""
        try:
            if not calculation_result:
                return "계산 결과가 없습니다."
            
            strategy = calculation_result.get('strategy', 'unknown')
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # 한국/미국 구분
            is_korean = DataValidator.is_korean_stock(symbol) if symbol else False
            
            report = f"""💰 1Bo's Plan Investment Report

{'=' * 60}
📊 Investment Analysis:
• Symbol: {symbol}
{f'• Company: {company_name}' if company_name else ''}
• Strategy: {strategy.upper()}
• Market: {'Korean Stock (KRX)' if is_korean else 'US Stock (NYSE/NASDAQ)'}
• Analysis Time: {timestamp}

"""
            
            if strategy == 'single':
                report += self._generate_single_report(calculation_result, symbol)
            elif strategy == 'dca':
                report += self._generate_dca_report(calculation_result, symbol)
            elif strategy == 'pyramid':
                report += self._generate_pyramid_report(calculation_result, symbol)
            elif strategy == 'leverage_etf':
                report += self._generate_leverage_report(calculation_result, symbol)
            
            report += """
⚠️ Important Disclaimer:
이 분석은 참고용입니다. 실제 투자 시에는 
충분한 검토와 본인의 판단이 필요합니다.
"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Report generation failed: {e}")
            return f"리포트 생성 실패: {e}"
    
    def _generate_single_report(self, result, symbol):
        """일괄투자 리포트"""
        is_korean = DataValidator.is_korean_stock(symbol)
        
        # 화폐 단위에 따른 포맷팅
        budget_text = format_currency_auto(result['budget'], symbol)
        commission_text = format_currency_auto(result['commission'], symbol)
        net_budget_text = format_currency_auto(result['net_budget'], symbol)
        price_text = format_currency_auto(result['current_price'], symbol)
        break_even_text = format_currency_auto(result['break_even_price'], symbol)
        
        # 주식 수 포맷팅
        shares_text = f"{result['shares']:,.0f}" if is_korean else f"{result['shares']:.2f}"
        
        report = f"""📌 Single Investment Strategy:

💵 Investment Details:
• Total Budget: {budget_text}
• Commission: {commission_text}
• Net Investment: {net_budget_text}
• Purchase Price: {price_text}
• Shares to Buy: {shares_text}주
• Break Even Price: {break_even_text}

🎯 Profit Targets:
"""
        
        # 수익 목표 추가
        for target in result['profit_targets']:
            target_price_text = format_currency_auto(target['price'], symbol)
            profit_text = format_currency_auto(target['profit'], symbol)
            report += f"• {target['percentage']:>5.1f}%: {target_price_text} (수익 {profit_text})\n"
        
        report += "\n✂️ Stop Loss Levels:\n"
        
        # 손절 레벨 추가
        for stop in result['stop_losses']:
            stop_price_text = format_currency_auto(stop['price'], symbol)
            loss_text = format_currency_auto(stop['loss'], symbol)
            report += f"• -{stop['percentage']:>4.1f}%: {stop_price_text} (손실 {loss_text})\n"
        
        return report
    
    def _generate_dca_report(self, result, symbol):
        """DCA 리포트"""
        is_korean = DataValidator.is_korean_stock(symbol)
        
        # 화폐 단위에 따른 포맷팅
        budget_text = format_currency_auto(result['budget'], symbol)
        amount_per_buy_text = format_currency_auto(result['amount_per_buy'], symbol)
        commission_per_buy_text = format_currency_auto(result['commission_per_buy'], symbol)
        net_amount_text = format_currency_auto(result['net_amount_per_buy'], symbol)
        total_commission_text = format_currency_auto(result['total_commission'], symbol)
        break_even_text = format_currency_auto(result['break_even_price'], symbol)
        
        # 주식 수 포맷팅
        shares_per_buy_text = f"{result['shares_per_buy']:,.0f}" if is_korean else f"{result['shares_per_buy']:.2f}"
        total_shares_text = f"{result['total_shares']:,.0f}" if is_korean else f"{result['total_shares']:.2f}"
        
        report = f"""📌 DCA (Dollar Cost Averaging) Strategy:

💵 DCA Plan:
• Total Budget: {budget_text}
• Number of Purchases: {result['splits']}회
• Amount per Purchase: {amount_per_buy_text}
• Commission per Purchase: {commission_per_buy_text}
• Net Amount per Purchase: {net_amount_text}
• Shares per Purchase: {shares_per_buy_text}주
• Expected Total Shares: {total_shares_text}주
• Total Commission: {total_commission_text}
• Break Even Price: {break_even_text}

📊 Market Scenarios:
"""
        
        # 시나리오 분석 추가
        for scenario in result['scenarios']:
            avg_cost_text = format_currency_auto(scenario['avg_cost'], symbol)
            current_value_text = format_currency_auto(scenario['current_value'], symbol)
            profit_loss_text = format_currency_auto(abs(scenario['profit_loss']), symbol)
            sign = "+" if scenario['profit_loss'] >= 0 else "-"
            
            # 주식 수 포맷팅
            scenario_shares_text = f"{scenario['total_shares']:,.0f}" if is_korean else f"{scenario['total_shares']:.2f}"
            
            report += f"""• {scenario['scenario']}:
  평균단가: {avg_cost_text}
  보유주식: {scenario_shares_text}주
  현재가치: {current_value_text}
  손익: {sign}{profit_loss_text} ({scenario['profit_loss_pct']:+.2f}%)

"""
        
        return report
    
    def _generate_pyramid_report(self, result, symbol):
        """피라미드 리포트"""
        is_korean = DataValidator.is_korean_stock(symbol)
        
        # 화폐 단위에 따른 포맷팅
        budget_text = format_currency_auto(result['budget'], symbol)
        avg_cost_text = format_currency_auto(result['average_cost'], symbol)
        total_investment_text = format_currency_auto(result['total_investment'], symbol)
        break_even_text = format_currency_auto(result['break_even_price'], symbol)
        
        # 주식 수 포맷팅
        total_shares_text = f"{result['total_shares']:,.0f}" if is_korean else f"{result['total_shares']:.2f}"
        
        report = f"""📌 Pyramid Investment Strategy:

💵 Pyramid Plan:
• Total Budget: {budget_text}
• Number of Levels: {result['splits']}단계
• Drop Rate per Level: {result['drop_rate']*100:.1f}%
• Average Cost: {avg_cost_text}
• Total Shares: {total_shares_text}주
• Total Investment: {total_investment_text}
• Break Even Price: {break_even_text}

📊 Level Details:
"""
        
        # 피라미드 단계별 상세 정보
        for plan in result['pyramid_plan']:
            price_text = format_currency_auto(plan['price'], symbol)
            amount_text = format_currency_auto(plan['amount'], symbol)
            net_amount_text = format_currency_auto(plan['net_amount'], symbol)
            cumulative_investment_text = format_currency_auto(plan['cumulative_investment'], symbol)
            
            # 주식 수 포맷팅
            shares_text = f"{plan['shares']:,.0f}" if is_korean else f"{plan['shares']:.2f}"
            cumulative_shares_text = f"{plan['cumulative_shares']:,.0f}" if is_korean else f"{plan['cumulative_shares']:.2f}"
            
            report += f"""• Level {plan['level']} (-{plan['drop_pct']:.1f}%):
  매수가격: {price_text}
  투자금액: {amount_text}
  순투자금: {net_amount_text}
  매수주식: {shares_text}주
  누적주식: {cumulative_shares_text}주
  누적투자: {cumulative_investment_text}

"""
        
        return report
    
    def _generate_leverage_report(self, result, symbol):
        """레버리지 ETF 리포트"""
        # 화폐 단위에 따른 포맷팅
        original_budget_text = format_currency_auto(result['original_budget'], symbol)
        recommended_budget_text = format_currency_auto(result['recommended_budget'], symbol)
        commission_text = format_currency_auto(result['commission'], symbol)
        net_budget_text = format_currency_auto(result['net_budget'], symbol)
        price_text = format_currency_auto(result['current_price'], symbol)
        stop_loss_text = format_currency_auto(result['strict_stop_loss'], symbol)
        
        report = f"""⚡ Leverage ETF Strategy:

🚨 Special Management Required:
• Original Budget: {original_budget_text}
• Recommended Budget: {recommended_budget_text} (70% 권장)
• Reason: {result['budget_reduction_reason']}
• Commission: {commission_text}
• Net Investment: {net_budget_text}
• Purchase Price: {price_text}
• Shares to Buy: {result['shares']:.2f}주
• Strict Stop Loss: {stop_loss_text} (15% 손절)
• Max Holding Period: {result['max_holding_period']}

⚠️ Leverage ETF Risks:
• Time Decay: {result['time_decay_monthly']*100:.1f}% per month
• Volatility Multiplier: {result['volatility_multiplier']}x
• Warning: {result['warning']}

💡 Management Tips:
• 절대 30일 이상 장기 보유 금지
• 15% 손실 시 즉시 손절 실행
• 일일 변동성 모니터링 필수
• 감정 거래 금지, 기계적 실행
"""
        
        return report