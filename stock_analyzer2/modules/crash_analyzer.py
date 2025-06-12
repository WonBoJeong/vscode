#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Enhanced Crash Analyzer Module v2.1
폭락장 대응 분석 모듈 (4가지 전략 분석 및 AI 자문 강화)

Author: AI Assistant & User  
Version: 2.1.0 - 4가지 폭락 대응 전략 분석, AI 자문 리포트 강화
"""

import numpy as np
import pandas as pd
from datetime import datetime
from pathlib import Path
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from config import RISK_CONFIG, LEVERAGE_ETFS
from .utils import Logger, format_currency, format_percentage, DataValidator

class CrashAnalyzer:
    """폭락장 분석 클래스 (4가지 전략 및 AI 자문 강화 버전)"""
    
    def __init__(self):
        self.logger = Logger("CrashAnalyzer")
        self.risk_thresholds = RISK_CONFIG['risk_score_thresholds']
        self.leverage_multiplier = RISK_CONFIG['leverage_risk_multiplier']
    
    def analyze_crash_situation(self, data, symbol, entry_price=None, position=0):
        """종합 폭락 분석"""
        try:
            if data is None or data.empty:
                return None
            
            latest_price = data['Close'].iloc[-1]
            
            # 다중 시간 프레임 분석
            crash_metrics = self._calculate_crash_metrics(data)
            
            # 레버리지 ETF 확인
            is_leverage = any(etf in symbol.upper() for etf in LEVERAGE_ETFS)
            
            # 위험 점수 계산
            risk_score = self._calculate_risk_score(crash_metrics, is_leverage)
            
            # 심각도 등급 결정
            severity = self._determine_severity(risk_score)
            
            # 권장사항 생성
            recommendation = self._generate_recommendation(severity, is_leverage, entry_price, latest_price)
            
            result = {
                'symbol': symbol,
                'current_price': latest_price,
                'entry_price': entry_price,
                'position': position,
                'is_leverage_etf': is_leverage,
                'crash_metrics': crash_metrics,
                'risk_score': risk_score,
                'severity': severity,
                'recommendation': recommendation,
                'analysis_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Crash analysis completed for {symbol}: {severity} ({risk_score:.1f})")
            return result
            
        except Exception as e:
            self.logger.error(f"Crash analysis failed: {e}")
            return None
    
    def calculate_four_strategy_analysis(self, current_price, symbol, entry_price=None, position=0, available_cash=0):
        """🎯 10% 폭락 시 4가지 전략 상세 분석"""
        try:
            is_leverage = any(etf in symbol.upper() for etf in LEVERAGE_ETFS)
            is_korean = DataValidator.is_korean_stock(symbol)
            currency_symbol = "₩" if is_korean else "$"
            
            # 기본 정보
            crashed_price = current_price * 0.9  # 10% 폭락 가정
            current_value = position * current_price if position > 0 else 0
            
            # 4가지 전략 계산
            strategies = {
                '1_additional_buy': self._calculate_additional_buy_strategy(
                    current_price, crashed_price, position, available_cash, is_korean
                ),
                '2_100_percent_cutloss': self._calculate_100_percent_cutloss_strategy(
                    current_price, crashed_price, position, is_korean
                ),
                '3_50_percent_cutloss': self._calculate_50_percent_cutloss_strategy(
                    current_price, crashed_price, position, is_korean
                ),
                '4_25_percent_cutloss': self._calculate_25_percent_cutloss_strategy(
                    current_price, crashed_price, position, is_korean
                )
            }
            
            # 기대 수익률 시나리오 분석
            scenarios = self._calculate_expectation_scenarios(strategies, current_price, crashed_price)
            
            result = {
                'symbol': symbol,
                'current_price': current_price,
                'entry_price': entry_price,
                'position': position,
                'available_cash': available_cash,
                'crashed_price': crashed_price,
                'current_value': current_value,
                'is_leverage': is_leverage,
                'is_korean': is_korean,
                'currency_symbol': currency_symbol,
                'strategies': strategies,
                'scenarios': scenarios,
                'analysis_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Four strategy analysis completed for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Four strategy analysis failed: {e}")
            return None
    
    def _calculate_additional_buy_strategy(self, current_price, crashed_price, position, available_cash, is_korean):
        """전략 1: 추가 매수 (10% 폭락 시 추가 매수)"""
        try:
            # 현재 보유 주식 가치 (폭락 후)
            current_shares = position
            current_value_after_crash = current_shares * crashed_price
            
            # 추가 매수 가능 주식 수
            additional_shares = int(available_cash / crashed_price) if crashed_price > 0 else 0
            total_shares_after_buy = current_shares + additional_shares
            total_value_after_buy = total_shares_after_buy * crashed_price
            
            # 향후 시나리오별 결과
            scenarios = []
            price_changes = [-0.5, -0.3, -0.2, -0.1, 0, 0.1, 0.2, 0.3, 0.5]  # -50% ~ +50%
            
            for change in price_changes:
                future_price = crashed_price * (1 + change)
                future_value = total_shares_after_buy * future_price
                return_pct = ((future_price - crashed_price) / crashed_price) * 100 if crashed_price > 0 else 0
                
                scenarios.append({
                    'price_change_pct': change * 100,
                    'future_price': future_price,
                    'total_value': future_value,
                    'return_pct': return_pct
                })
            
            return {
                'name': '전략 1: 추가 매수',
                'description': '10% 폭락 시 추가 현금으로 매수',
                'current_shares': current_shares,
                'additional_shares': additional_shares,
                'total_shares': total_shares_after_buy,
                'cash_used': additional_shares * crashed_price,
                'remaining_cash': available_cash - (additional_shares * crashed_price),
                'total_investment': current_value_after_crash + (additional_shares * crashed_price),
                'scenarios': scenarios,
                'pros': [
                    '주가 반등 시 최대 수익',
                    '평단가 하향 조정',
                    '추가 하락 시에도 보유 주식 수 증가'
                ],
                'cons': [
                    '추가 하락 시 손실 확대',
                    '현금 소진으로 유동성 부족',
                    '하락장 지속 시 막대한 손실'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Additional buy strategy calculation failed: {e}")
            return {}
    
    def _calculate_100_percent_cutloss_strategy(self, current_price, crashed_price, position, is_korean):
        """전략 2: 100% 손절 (전량 매도)"""
        try:
            # 손절 후 현금 확보
            cash_from_sale = position * crashed_price
            
            # 향후 재매수 시나리오
            scenarios = []
            additional_declines = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
            
            for decline in additional_declines:
                reentry_price = crashed_price * (1 - decline)
                buyable_shares = int(cash_from_sale / reentry_price) if reentry_price > 0 else 0
                increase_ratio = buyable_shares / position if position > 0 else 0
                
                scenarios.append({
                    'additional_decline_pct': decline * 100,
                    'reentry_price': reentry_price,
                    'buyable_shares': buyable_shares,
                    'increase_ratio': increase_ratio,
                    'increase_shares': buyable_shares - position
                })
            
            return {
                'name': '전략 2: 100% 손절',
                'description': '전량 매도 후 추가 하락 시 재매수',
                'cutloss_shares': position,
                'cash_from_sale': cash_from_sale,
                'loss_amount': position * (current_price - crashed_price),
                'loss_pct': -10.0,
                'scenarios': scenarios,
                'pros': [
                    '추가 하락 시 최대 주식 수 확보',
                    '손실 확정으로 리스크 제거',
                    '현금 확보로 기회 포착 가능'
                ],
                'cons': [
                    '주가 반등 시 기회 상실',
                    '재진입 타이밍 어려움',
                    '세금 및 거래 수수료 발생'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"100% cutloss strategy calculation failed: {e}")
            return {}
    
    def _calculate_50_percent_cutloss_strategy(self, current_price, crashed_price, position, is_korean):
        """전략 3: 50% 손절 (절반 매도)"""
        try:
            # 손절 주식 수 및 현금
            cutloss_shares = int(position * 0.5)
            remaining_shares = position - cutloss_shares
            cash_from_sale = cutloss_shares * crashed_price
            
            # 향후 재매수 시나리오
            scenarios = []
            additional_declines = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
            
            for decline in additional_declines:
                reentry_price = crashed_price * (1 - decline)
                buyable_shares = int(cash_from_sale / reentry_price) if reentry_price > 0 else 0
                total_shares = remaining_shares + buyable_shares
                increase_ratio = total_shares / position if position > 0 else 0
                
                scenarios.append({
                    'additional_decline_pct': decline * 100,
                    'reentry_price': reentry_price,
                    'buyable_shares': buyable_shares,
                    'total_shares': total_shares,
                    'increase_ratio': increase_ratio,
                    'increase_shares': total_shares - position
                })
            
            return {
                'name': '전략 3: 50% 손절',
                'description': '절반 매도 후 추가 하락 시 재매수',
                'cutloss_shares': cutloss_shares,
                'remaining_shares': remaining_shares,
                'cash_from_sale': cash_from_sale,
                'loss_amount': cutloss_shares * (current_price - crashed_price),
                'loss_pct': -5.0,  # 전체 포지션의 5% 손실
                'scenarios': scenarios,
                'pros': [
                    '리스크 부분 제거',
                    '주가 반등 시 일부 수익 확보',
                    '추가 하락 시 재매수 여력 확보'
                ],
                'cons': [
                    '기회비용 발생',
                    '복잡한 포지션 관리',
                    '부분적 손실 확정'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"50% cutloss strategy calculation failed: {e}")
            return {}
    
    def _calculate_25_percent_cutloss_strategy(self, current_price, crashed_price, position, is_korean):
        """전략 4: 25% 손절 (1/4 매도)"""
        try:
            # 손절 주식 수 및 현금
            cutloss_shares = int(position * 0.25)
            remaining_shares = position - cutloss_shares
            cash_from_sale = cutloss_shares * crashed_price
            
            # 향후 재매수 시나리오
            scenarios = []
            additional_declines = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.40, 0.50, 0.60, 0.70, 0.80, 0.90]
            
            for decline in additional_declines:
                reentry_price = crashed_price * (1 - decline)
                buyable_shares = int(cash_from_sale / reentry_price) if reentry_price > 0 else 0
                total_shares = remaining_shares + buyable_shares
                increase_ratio = total_shares / position if position > 0 else 0
                
                scenarios.append({
                    'additional_decline_pct': decline * 100,
                    'reentry_price': reentry_price,
                    'buyable_shares': buyable_shares,
                    'total_shares': total_shares,
                    'increase_ratio': increase_ratio,
                    'increase_shares': total_shares - position
                })
            
            return {
                'name': '전략 4: 25% 손절',
                'description': '1/4 매도 후 추가 하락 시 재매수',
                'cutloss_shares': cutloss_shares,
                'remaining_shares': remaining_shares,
                'cash_from_sale': cash_from_sale,
                'loss_amount': cutloss_shares * (current_price - crashed_price),
                'loss_pct': -2.5,  # 전체 포지션의 2.5% 손실
                'scenarios': scenarios,
                'pros': [
                    '최소 리스크 제거',
                    '대부분 포지션 유지',
                    '소량 현금 확보'
                ],
                'cons': [
                    '제한적 리스크 해소',
                    '추가 하락 시 제한적 대응',
                    '미미한 현금 확보'
                ]
            }
            
        except Exception as e:
            self.logger.error(f"25% cutloss strategy calculation failed: {e}")
            return {}
    
    def _calculate_expectation_scenarios(self, strategies, current_price, crashed_price):
        """기대 수익률 시나리오 분석"""
        try:
            scenarios = {
                'immediate_recovery': {
                    'name': '즉시 반등 (+10%)',
                    'description': '10% 폭락 후 즉시 원래 가격으로 회복',
                    'future_price': current_price,
                    'best_strategy': '전략 1: 추가 매수',
                    'reason': '추가 매수로 평단가 하향 조정, 최대 수익'
                },
                'continued_decline_20': {
                    'name': '추가 하락 20%',
                    'description': '10% 폭락 후 추가로 20% 더 하락',
                    'future_price': crashed_price * 0.8,
                    'best_strategy': '전략 2: 100% 손절',
                    'reason': '전량 매도로 현금 확보, 더 낮은 가격에서 재매수'
                },
                'continued_decline_50': {
                    'name': '추가 하락 50%',
                    'description': '10% 폭락 후 추가로 50% 더 하락',
                    'future_price': crashed_price * 0.5,
                    'best_strategy': '전략 2: 100% 손절',
                    'reason': '2배 주식 수 확보 가능'
                },
                'sideways': {
                    'name': '횡보 지속',
                    'description': '10% 폭락 후 횡보',
                    'future_price': crashed_price,
                    'best_strategy': '전략 3: 50% 손절 또는 전략 4: 25% 손절',
                    'reason': '적절한 리스크 관리와 기회 보존의 균형'
                }
            }
            
            return scenarios
            
        except Exception as e:
            self.logger.error(f"Expectation scenarios calculation failed: {e}")
            return {}
    
    def calculate_optimal_cutloss_with_reentry(self, current_price, symbol, entry_price=None, position=0, additional_cash=0):
        """🎯 강화된 손절가 계산 - 재매수 시나리오 포함"""
        try:
            is_leverage = any(etf in symbol.upper() for etf in LEVERAGE_ETFS)
            is_korean = DataValidator.is_korean_stock(symbol)
            
            if is_leverage:
                cutloss_rates = RISK_CONFIG['leverage_cutloss_rates']
                asset_type = "레버리지 ETF"
            else:
                cutloss_rates = RISK_CONFIG['normal_cutloss_rates']
                asset_type = "일반 주식"
            
            # 기본 손절 레벨
            cutloss_levels = []
            labels = ["보수적", "표준", "공격적"]
            
            for i, rate in enumerate(cutloss_rates):
                cutloss_price = current_price * rate
                loss_pct = (1 - rate) * 100
                
                cutloss_levels.append({
                    'level': labels[i],
                    'price': cutloss_price,
                    'loss_percentage': loss_pct,
                    'description': f"{loss_pct:.0f}% 손절"
                })
            
            # 🎯 4가지 전략 분석 추가
            four_strategy_analysis = self.calculate_four_strategy_analysis(
                current_price, symbol, entry_price, position, additional_cash
            )
            
            result = {
                'symbol': symbol,
                'current_price': current_price,
                'entry_price': entry_price,
                'position': position,
                'additional_cash': additional_cash,
                'asset_type': asset_type,
                'is_leverage': is_leverage,
                'is_korean': is_korean,
                'cutloss_levels': cutloss_levels,
                'absolute_stop': current_price * 0.75 if is_leverage else current_price * 0.70,
                'recommendation': "보수적 기준 권장" if is_leverage else "표준 기준 권장",
                'four_strategy_analysis': four_strategy_analysis  # 🎯 새로 추가
            }
            
            self.logger.info(f"Enhanced cutloss analysis completed for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Enhanced cutloss calculation failed: {e}")
            return None
    
    def calculate_optimal_cutloss(self, current_price, symbol, is_leverage=None):
        """기존 손절가 계산 메서드 (호환성 유지)"""
        try:
            if is_leverage is None:
                is_leverage = any(etf in symbol.upper() for etf in LEVERAGE_ETFS)
            
            if is_leverage:
                cutloss_rates = RISK_CONFIG['leverage_cutloss_rates']
                asset_type = "레버리지 ETF"
            else:
                cutloss_rates = RISK_CONFIG['normal_cutloss_rates']
                asset_type = "일반 주식"
            
            cutloss_levels = []
            labels = ["보수적", "표준", "공격적"]
            
            for i, rate in enumerate(cutloss_rates):
                cutloss_price = current_price * rate
                loss_pct = (1 - rate) * 100
                
                cutloss_levels.append({
                    'level': labels[i],
                    'price': cutloss_price,
                    'loss_percentage': loss_pct,
                    'description': f"{loss_pct:.0f}% 손절"
                })
            
            result = {
                'symbol': symbol,
                'current_price': current_price,
                'asset_type': asset_type,
                'is_leverage': is_leverage,
                'cutloss_levels': cutloss_levels,
                'absolute_stop': current_price * 0.75 if is_leverage else current_price * 0.70,
                'recommendation': "보수적 기준 권장" if is_leverage else "표준 기준 권장"
            }
            
            self.logger.info(f"Cutloss levels calculated for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Cutloss calculation failed: {e}")
            return None
    
    def generate_comprehensive_ai_report(self, analysis_result, technical_analysis=None, portfolio_info=None, four_strategy_result=None):
        """🎯 종합 AI 자문용 리포트 생성 - 4가지 전략 분석 포함"""
        try:
            if not analysis_result:
                return "분석 결과가 없습니다."
            
            symbol = analysis_result['symbol']
            current_price = analysis_result['current_price']
            entry_price = analysis_result.get('entry_price')
            position = analysis_result.get('position', 0)
            severity = analysis_result['severity']
            recommendation = analysis_result['recommendation']
            risk_score = analysis_result['risk_score']
            is_korean = DataValidator.is_korean_stock(symbol)
            is_leverage = analysis_result.get('is_leverage_etf', False)
            
            # 화폐 포맷팅
            currency_symbol = "₩" if is_korean else "$"
            
            # 수정: f-string 내 조건문 오류 해결
            # 화폐 포맷팅을 사전에 처리
            if is_korean:
                current_price_text = f"₩{current_price:,.0f}"
            else:
                current_price_text = f"${current_price:.2f}"
            
            asset_type_text = "레버리지 ETF" if is_leverage else "일반 주식"
            
            report = f"""🤖 1Bo's Plan - 종합 투자 자문 리포트 (4가지 폭락 대응 전략 포함)

안녕하세요. 현재 보유 포지션에 대한 전문적인 투자 자문을 구하고자 합니다.
특히 10% 폭락 시 4가지 대응 전략에 대해 정치적, 경제적, 기술적 요소를 종합적으로 고려하여 
최적의 투자 전략을 조언해 주시기 바랍니다.

== 기본 포트폴리오 정보 ==
• 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• 보유 종목: {symbol}
• 자산 유형: {asset_type_text}
• 현재가: {current_price_text}"""
            
            if entry_price and position > 0:
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
                pnl_amount = (current_price - entry_price) * position
                total_value = current_price * position
                
                # 수정: 추가 화폐 포맷팅
                if is_korean:
                    entry_price_text = f"₩{entry_price:,.0f}"
                    total_value_text = f"₩{total_value:,.0f}"
                    pnl_amount_text = f"₩{pnl_amount:+,.0f}"
                else:
                    entry_price_text = f"${entry_price:.2f}"
                    total_value_text = f"${total_value:.2f}"
                    pnl_amount_text = f"${pnl_amount:+.2f}"
                
                report += f"""
• 평단가: {entry_price_text}
• 보유량: {position:,.0f}주
• 총 평가액: {total_value_text}
• 평가손익: {pnl_amount_text} ({pnl_pct:+.2f}%)"""
            
            report += f"""

== 현재 위험도 분석 ==
• 위험 점수: {risk_score:.1f}/100점
• 심각도: {severity['emoji']} {severity['description']}
• 시스템 권장: {recommendation['action']}
• 상세 의견: {recommendation['details']}"""
            
            # 기술적 분석 정보 추가
            if technical_analysis:
                report += f"""

== 기술적 분석 현황 =="""
                
                # RSI 정보
                if 'technical_indicators' in technical_analysis:
                    indicators = technical_analysis['technical_indicators']
                    if 'rsi' in indicators:
                        rsi = indicators['rsi']
                        rsi_status = "과매도" if rsi < 30 else "과매수" if rsi > 70 else "중립"
                        report += f"""
• RSI: {rsi:.1f} ({rsi_status})"""
                    
                    if 'macd_trend' in indicators:
                        macd_trend = indicators['macd_trend']
                        report += f"""
• MACD: {macd_trend} 추세"""
                
                # 최근 3일 평균 분석
                if 'recent_stats' in technical_analysis:
                    stats = technical_analysis['recent_stats']
                    
                    # 수정: 화폐 포맷팅
                    if is_korean:
                        avg_3_days_text = f"₩{stats['avg_3_days']:,.0f}"
                    else:
                        avg_3_days_text = f"${stats['avg_3_days']:.2f}"
                    
                    trend_text = '상승추세' if stats['diff_pct'] > 0 else '하락추세' if stats['diff_pct'] < 0 else '보합'
                    
                    report += f"""
• 3일 평균가: {avg_3_days_text}
• 현재가 대비: {stats['diff_pct']:+.1f}% ({trend_text})"""
                
                # 95% 신뢰구간 분석
                if 'confidence_interval' in technical_analysis:
                    ci = technical_analysis['confidence_interval']
                    signal_text = {
                        'POTENTIAL_BUY': '매수 고려 구간',
                        'POTENTIAL_SELL': '매도 고려 구간',
                        'HOLD': '관망 구간'
                    }.get(ci['signal'], '보합')
                    
                    # 수정: 화폐 포맷팅
                    if is_korean:
                        ci_lower_text = f"₩{ci['lower_bound']:,.0f}"
                        ci_upper_text = f"₩{ci['upper_bound']:,.0f}"
                    else:
                        ci_lower_text = f"${ci['lower_bound']:.2f}"
                        ci_upper_text = f"${ci['upper_bound']:.2f}"
                    
                    report += f"""
• 95% 신뢰구간: {ci_lower_text} ~ {ci_upper_text}
• 구간 분석: {signal_text}"""
                
                # SP500 비교 (미국 주식인 경우)
                if not is_korean and 'sp500_comparison' in technical_analysis:
                    sp500 = technical_analysis['sp500_comparison']
                    performance_text = f"+{sp500['relative_performance']:.1f}% 우수" if sp500['outperforming'] else f"{sp500['relative_performance']:.1f}% 부진"
                    report += f"""
• SP500 대비 성과: {performance_text}
• 베타 계수: {sp500.get('beta', 'N/A')}
• 상관관계: {sp500.get('correlation', 'N/A')}"""
                
                # 매매 결정 분석
                if 'trading_decision' in technical_analysis:
                    decision = technical_analysis['trading_decision']
                    decision_text = {
                        'STRONG_BUY': '🚀 적극매수',
                        'BUY': '💚 매수',
                        'HOLD': '🟡 보유',
                        'SELL': '🔴 매도',
                        'STRONG_SELL': '💥 적극매도'
                    }.get(decision['decision'], decision['decision'])
                    
                    confidence_text = {
                        'HIGH': '높음',
                        'MEDIUM': '보통',
                        'LOW': '낮음'
                    }.get(decision['confidence'], decision['confidence'])
                    
                    report += f"""
• 기술적 매매신호: {decision_text}
• 신호 신뢰도: {confidence_text}
• 판단 근거: {decision['reasoning']}"""
            
            # 4가지 폭락 대응 전략 상세 분석 (핵심 부분만)
            if four_strategy_result and position > 0:
                crashed_price = four_strategy_result.get('crashed_price', current_price * 0.9)
                strategies = four_strategy_result.get('strategies', {})
                
                # 수정: 추가 화폐 포맷팅
                if is_korean:
                    crashed_price_text = f"₩{crashed_price:,.0f}"
                    position_crashed_value_text = f"₩{(position * crashed_price):,.0f}"
                else:
                    crashed_price_text = f"${crashed_price:.2f}"
                    position_crashed_value_text = f"${(position * crashed_price):,.2f}"
                
                report += f"""

== 10% 폭락 시 4가지 대응 전략 분석 ==

현재 상황:
• 현재가: {current_price_text}
• 10% 폭락 가격: {crashed_price_text}
• 보유 주식 수: {position:,.0f}주
• 폭락 후 평가액: {position_crashed_value_text}

전략별 상세 분석:"""
                
                # 각 전략에 대한 간단한 요약만 포함 (전체 메서드가 너무 길어지므로)
                for strategy_key in ['1_additional_buy', '2_100_percent_cutloss', '3_50_percent_cutloss', '4_25_percent_cutloss']:
                    if strategy_key in strategies:
                        strategy = strategies[strategy_key]
                        report += f"""

• {strategy['name']}: {strategy['description']}
  - 장점: {', '.join(strategy.get('pros', [])[:2])}  
  - 단점: {', '.join(strategy.get('cons', [])[:2])}"""
                
                # 시나리오별 최적 전략
                scenarios_info = four_strategy_result.get('scenarios', {})
                if scenarios_info:
                    report += f"""

시나리오별 최적 전략:
• 즉시 반등 시: {scenarios_info.get('immediate_recovery', {}).get('best_strategy', 'N/A')}
• 추가 20% 하락 시: {scenarios_info.get('continued_decline_20', {}).get('best_strategy', 'N/A')}
• 추가 50% 하락 시: {scenarios_info.get('continued_decline_50', {}).get('best_strategy', 'N/A')}
• 횡보 지속 시: {scenarios_info.get('sideways', {}).get('best_strategy', 'N/A')}"""
            
            # 위험 요소 및 모니터링 포인트
            crash_metrics = analysis_result.get('crash_metrics', {})
            report += f"""

== 주요 위험 지표 =="""
            
            if 'drop_10d' in crash_metrics:
                report += f"""
• 10일 최고점 대비 하락: {crash_metrics['drop_10d']:+.1f}%"""
            if 'volatility_5d' in crash_metrics:
                report += f"""
• 5일 변동성: {crash_metrics['volatility_5d']:.1f}% (연환산)"""
            if 'consecutive_down_days' in crash_metrics:
                report += f"""
• 연속 하락일: {crash_metrics['consecutive_down_days']:.0f}일"""
            if 'volume_spike' in crash_metrics:
                report += f"""
• 거래량 급증: {crash_metrics['volume_spike']:+.1f}%"""
            
            # 레버리지 ETF 특별 주의사항
            if is_leverage:
                report += f"""

== 레버리지 ETF 특별 고려사항 ==
• 3배 레버리지로 인한 변동성 확대
• 일일 리밸런싱으로 장기 보유 시 손실 누적 위험
• 절대 손절선: 15% (일반 주식 대비 엄격한 기준)
• 권장 최대 보유기간: 30일 이내
• 섹터 집중 위험 (반도체 업계 전반적 영향)"""
            
            report += f"""

== 전문가 자문 요청 사항 ==

다음 사항들에 대해 현재 정치·경제적 상황을 고려하여 조언해 주시기 바랍니다:

1. 4가지 전략 중 최적 선택:
   - 현재 시장 상황에서 가장 합리적인 전략은?
   - 미래 불확실성을 고려할 때 위험 대비 수익이 가장 좋은 전략은?

2. 정치·경제적 환경 분석:
   - 현재 정치적 상황(정책 변화, 규제 등)이 해당 종목에 미치는 영향
   - 경제적 지표(금리, 인플레이션, GDP 등)가 섹터에 미치는 영향
   - 국제적 요인(무역분쟁, 지정학적 리스크 등) 고려사항

3. 리스크 관리 전략:
   - 현재 위험도 {risk_score:.0f}점에 대한 객관적 평가
   - 각 전략의 리스크-리턴 프로파일 분석
   - 추가 모니터링해야 할 핵심 지표나 이벤트

4. 실행 전략 및 타이밍:
   - 구체적이고 실행 가능한 단계별 행동 계획
   - 각 전략 실행 시 주의사항 및 조건
   - 감정적 판단을 배제한 객관적 기준점 설정

5. 미래 시나리오별 대응:
   - 즉시 반등 vs 추가 하락 각각의 확률적 평가
   - 장기적 관점에서의 해당 종목/섹터 전망
   - 포트폴리오 차원에서의 종합적 조언

특히 중요한 것은:
- 감정이 아닌 데이터와 논리에 기반한 객관적 분석
- 현실적으로 실행 가능한 구체적 조언
- 정치·경제적 거시 환경과 개별 종목 분석의 조화
- 불확실성 하에서의 최적 의사결정 가이드라인

---
Generated by 1Bo's Plan Enhanced Crash Analyzer v2.1
분석 도구: 기술적 분석 + 포트폴리오 분석 + 위험도 평가 + 4가지 전략 분석 통합"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Comprehensive AI report generation failed: {e}")
            return f"종합 리포트 생성 실패: {e}"
    
    def generate_enhanced_ai_report(self, analysis_result, technical_analysis=None, portfolio_info=None):
        """🎯 강화된 AI 자문용 리포트 생성 - 기술적 분석 및 포트폴리오 정보 포함 (호환성 유지)"""
        return self.generate_comprehensive_ai_report(analysis_result, technical_analysis, portfolio_info)
    
    def generate_situation_report(self, analysis_result):
        """기존 AI 자문용 상황 리포트 생성 (호환성 유지)"""
        try:
            if not analysis_result:
                return "분석 결과가 없습니다."
            
            symbol = analysis_result['symbol']
            current_price = analysis_result['current_price']
            severity = analysis_result['severity']
            recommendation = analysis_result['recommendation']
            risk_score = analysis_result['risk_score']
            
            report = f"""🤖 1Bo's Plan AI Advisory Report

현재 상황에 대한 전문적인 조언을 구하고자 합니다.

기본 정보:
• 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• 분석 종목: {symbol}
• 현재가: {format_currency(current_price)}
• 위험 점수: {risk_score:.1f}/100점
• 심각도: {severity['emoji']} {severity['description']}

현재 상황:
{recommendation['action']}
{recommendation['details']}

전문가 자문 요청 사항:
1. 현재 상황에 대한 객관적 진단
2. 가장 합리적인 대응 전략
3. 위험 관리 관점에서의 핵심 고려사항
4. 향후 모니터링해야 할 지표

특히 감정적 판단이 아닌 데이터와 논리에 기반한
객관적 분석과 실행 가능한 구체적 조언을 원합니다.

---
Generated by 1Bo's Plan Crash Analyzer v2.1"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Situation report generation failed: {e}")
            return f"리포트 생성 실패: {e}"
    
    # 기존 메서드들 그대로 유지
    def _calculate_crash_metrics(self, data):
        """폭락 지표 계산"""
        try:
            metrics = {}
            
            # 다양한 기간의 최고점에서 하락률
            for period in [5, 10, 20, 60]:
                recent_data = data.tail(period)
                if not recent_data.empty:
                    max_price = recent_data['High'].max()
                    current_price = data['Close'].iloc[-1]
                    drop_pct = ((current_price - max_price) / max_price) * 100
                    metrics[f'drop_{period}d'] = drop_pct
            
            # 변동성 계산
            for period in [5, 10, 20]:
                recent_data = data.tail(period)
                if len(recent_data) > 1:
                    returns = recent_data['Close'].pct_change().dropna()
                    volatility = returns.std() * np.sqrt(252) * 100
                    metrics[f'volatility_{period}d'] = volatility
            
            # 거래량 급증 분석
            vol_20d = data['Volume'].tail(20).mean()
            vol_5d = data['Volume'].tail(5).mean()
            volume_spike = ((vol_5d - vol_20d) / vol_20d) * 100 if vol_20d > 0 else 0
            metrics['volume_spike'] = volume_spike
            
            # 연속 하락일
            consecutive_down = 0
            prices = data['Close'].tail(10).tolist()
            for i in range(len(prices)-1, 0, -1):
                if prices[i] < prices[i-1]:
                    consecutive_down += 1
                else:
                    break
            metrics['consecutive_down_days'] = consecutive_down
            
            return metrics
            
        except Exception as e:
            self.logger.error(f"Crash metrics calculation failed: {e}")
            return {}
    
    def _calculate_risk_score(self, metrics, is_leverage):
        """위험 점수 계산 (0-100)"""
        try:
            score = 0
            
            # 하락 심각도 (최대 35점)
            drop_10d = abs(metrics.get('drop_10d', 0))
            score += min(35, drop_10d * 1.8)
            
            # 변동성 위험 (최대 25점)
            volatility_5d = metrics.get('volatility_5d', 0)
            score += min(25, volatility_5d * 0.4)
            
            # 거래량 이상 (최대 15점)
            volume_spike = max(0, metrics.get('volume_spike', 0))
            score += min(15, volume_spike * 0.15)
            
            # 추세 파괴 (최대 15점)
            drop_20d = abs(metrics.get('drop_20d', 0))
            score += min(15, drop_20d * 0.4)
            
            # 연속 하락 (최대 10점)
            consecutive_days = metrics.get('consecutive_down_days', 0)
            score += min(10, consecutive_days * 2)
            
            # 레버리지 ETF 가산점
            if is_leverage:
                score = min(100, score * self.leverage_multiplier)
            
            return score
            
        except Exception as e:
            self.logger.error(f"Risk score calculation failed: {e}")
            return 0
    
    def _determine_severity(self, risk_score):
        """심각도 등급 결정"""
        thresholds = self.risk_thresholds
        
        if risk_score < thresholds['normal']:
            return {
                'level': 'NORMAL',
                'emoji': '📈',
                'description': '정상 범위'
            }
        elif risk_score < thresholds['moderate']:
            return {
                'level': 'MODERATE_DECLINE',
                'emoji': '📊',
                'description': '보통 조정'
            }
        elif risk_score < thresholds['significant']:
            return {
                'level': 'SIGNIFICANT_DROP',
                'emoji': '⚠️',
                'description': '상당한 하락'
            }
        elif risk_score < thresholds['severe']:
            return {
                'level': 'SEVERE_CRASH',
                'emoji': '🚨',
                'description': '심각한 폭락'
            }
        else:
            return {
                'level': 'EXTREME_CRASH',
                'emoji': '💥',
                'description': '극한 폭락'
            }
    
    def _generate_recommendation(self, severity, is_leverage, entry_price, current_price):
        """권장사항 생성"""
        level = severity['level']
        
        base_recommendations = {
            'NORMAL': {
                'action': '정상 보유',
                'details': '현재 포지션 유지 가능',
                'monitoring': '정기적 모니터링'
            },
            'MODERATE_DECLINE': {
                'action': '주의 필요',
                'details': '포지션 크기 재검토',
                'monitoring': '주의 깊게 관찰'
            },
            'SIGNIFICANT_DROP': {
                'action': '위험 - 손절 고려',
                'details': '손절 기준점 도달 여부 확인',
                'monitoring': '일일 모니터링 필수'
            },
            'SEVERE_CRASH': {
                'action': '심각 - 즉시 대응 필요',
                'details': '즉시 손절 결정 필요',
                'monitoring': '실시간 모니터링'
            },
            'EXTREME_CRASH': {
                'action': '극한 상황 - 긴급 대응',
                'details': '긴급 포지션 전면 정리',
                'monitoring': '즉시 대응'
            }
        }
        
        recommendation = base_recommendations.get(level, base_recommendations['NORMAL']).copy()
        
        # 레버리지 ETF 특별 권장사항
        if is_leverage:
            recommendation['leverage_warning'] = '레버리지 ETF 특별 관리 필요'
            if level in ['SIGNIFICANT_DROP', 'SEVERE_CRASH', 'EXTREME_CRASH']:
                recommendation['action'] = '즉시 손절 권장'
                recommendation['details'] += ' (레버리지 ETF 15% 손절 기준 적용)'
        
        # 손익 정보 추가
        if entry_price and current_price:
            pnl_pct = ((current_price - entry_price) / entry_price) * 100
            recommendation['current_pnl'] = pnl_pct
            
            if pnl_pct < -10:
                recommendation['pnl_warning'] = '10% 이상 손실 - 추가 손실 제한 필요'
        
        return recommendation