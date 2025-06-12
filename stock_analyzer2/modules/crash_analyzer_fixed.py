#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Fixed Crash Analyzer Module
폭락장 대응 분석 모듈 (F-string 오류 수정)

Author: AI Assistant & User  
Version: 2.2.0 - F-string Format 오류 완전 해결
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

def format_currency_safe(amount, is_korean):
    """안전한 화폐 포맷팅 함수"""
    if is_korean:
        return f"₩{amount:,.0f}"
    else:
        return f"${amount:.2f}"

class CrashAnalyzer:
    """폭락장 분석 클래스 (F-string 오류 수정 버전)"""
    
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
    
    def generate_comprehensive_ai_report(self, analysis_result, technical_analysis=None, portfolio_info=None, four_strategy_result=None):
        """🎯 종합 AI 자문용 리포트 생성 - F-string 오류 완전 수정"""
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
            
            # 🔧 수정: 모든 화폐 포맷팅을 사전에 처리
            current_price_text = format_currency_safe(current_price, is_korean)
            asset_type_text = "레버리지 ETF" if is_leverage else "일반 주식"
            
            report = f"""🤖 1Bo's Plan - 종합 투자 자문 리포트 (4가지 폭락 대응 전략 포함)

안녕하세요. 현재 보유 포지션에 대한 전문적인 투자 자문을 구하고자 합니다.
특히 10% 폭락 시 4가지 대응 전략에 대해 정치적, 경제적, 기술적 요소를 종합적으로 고려하여 
최적의 투자 전략을 조언해 주시기 바랍니다.

📊 == 기본 포트폴리오 정보 ==
• 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• 보유 종목: {symbol}
• 자산 유형: {asset_type_text}
• 현재가: {current_price_text}"""
            
            if entry_price and position > 0:
                pnl_pct = ((current_price - entry_price) / entry_price) * 100
                pnl_amount = (current_price - entry_price) * position
                total_value = current_price * position
                
                entry_price_text = format_currency_safe(entry_price, is_korean)
                total_value_text = format_currency_safe(total_value, is_korean)
                pnl_amount_text = format_currency_safe(pnl_amount, is_korean)
                if pnl_amount >= 0:
                    pnl_amount_text = "+" + pnl_amount_text
                
                report += f"""
• 평단가: {entry_price_text}
• 보유량: {position:,.0f}주
• 총 평가액: {total_value_text}
• 평가손익: {pnl_amount_text} ({pnl_pct:+.2f}%)"""
            
            report += f"""

🚨 == 현재 위험도 분석 ==
• 위험 점수: {risk_score:.1f}/100점
• 심각도: {severity['emoji']} {severity['description']}
• 시스템 권장: {recommendation['action']}
• 상세 의견: {recommendation['details']}"""
            
            # 기술적 분석 정보 추가
            if technical_analysis:
                report += f"""

📈 == 기술적 분석 현황 =="""
                
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
                    avg_3_days_text = format_currency_safe(stats['avg_3_days'], is_korean)
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
                    
                    ci_lower_text = format_currency_safe(ci['lower_bound'], is_korean)
                    ci_upper_text = format_currency_safe(ci['upper_bound'], is_korean)
                    
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
            
            # 🎯 4가지 폭락 대응 전략 상세 분석
            if four_strategy_result and position > 0:
                crashed_price = four_strategy_result.get('crashed_price', current_price * 0.9)
                strategies = four_strategy_result.get('strategies', {})
                
                crashed_price_text = format_currency_safe(crashed_price, is_korean)
                position_crashed_value = position * crashed_price
                position_crashed_value_text = format_currency_safe(position_crashed_value, is_korean)
                
                report += f"""

💥 == 10% 폭락 시 4가지 대응 전략 분석 ==

📍 현재 상황:
• 현재가: {current_price_text}
• 10% 폭락 가격: {crashed_price_text}
• 보유 주식 수: {position:,.0f}주
• 폭락 후 평가액: {position_crashed_value_text}

🎯 **전략별 상세 분석:**"""
                
                # 전략 1: 추가 매수
                if '1_additional_buy' in strategies:
                    strategy = strategies['1_additional_buy']
                    cash_used = strategy.get('cash_used', 0)
                    cash_used_text = format_currency_safe(cash_used, is_korean)
                    
                    report += f"""

📈 **{strategy['name']}**
• 설명: {strategy['description']}
• 추가 매수 주식: {strategy.get('additional_shares', 0):,.0f}주
• 총 보유 예상: {strategy.get('total_shares', 0):,.0f}주
• 사용 현금: {cash_used_text}
• 장점: {', '.join(strategy.get('pros', []))}
• 단점: {', '.join(strategy.get('cons', []))}"""
                
                # 전략 2: 100% 손절
                if '2_100_percent_cutloss' in strategies:
                    strategy = strategies['2_100_percent_cutloss']
                    scenarios = strategy.get('scenarios', [])
                    
                    cash_from_sale = strategy.get('cash_from_sale', 0)
                    loss_amount = strategy.get('loss_amount', 0)
                    cash_from_sale_text = format_currency_safe(cash_from_sale, is_korean)
                    loss_amount_text = format_currency_safe(loss_amount, is_korean)
                    
                    report += f"""

💰 **{strategy['name']}**
• 설명: {strategy['description']}
• 손절 주식: {strategy.get('cutloss_shares', 0):,.0f}주
• 확보 현금: {cash_from_sale_text}
• 즉시 손실: {loss_amount_text} ({strategy.get('loss_pct', 0):.1f}%)

📊 **재매수 시나리오 (주요 구간):**"""
                    
                    # 주요 재매수 시나리오 표시
                    key_scenarios = [s for s in scenarios if s['additional_decline_pct'] in [20, 30, 50, 70]]
                    for scenario in key_scenarios:
                        report += f"""
• 추가 {scenario['additional_decline_pct']:.0f}% 하락 시: {scenario['buyable_shares']:,.0f}주 매수 가능 (원래의 {scenario['increase_ratio']:.1f}배)"""
                    
                    report += f"""
• 장점: {', '.join(strategy.get('pros', []))}
• 단점: {', '.join(strategy.get('cons', []))}"""
                
                # 전략 3과 4도 동일한 패턴으로 처리
                for strategy_key, strategy_name in [('3_50_percent_cutloss', '50% 손절'), ('4_25_percent_cutloss', '25% 손절')]:
                    if strategy_key in strategies:
                        strategy = strategies[strategy_key]
                        scenarios = strategy.get('scenarios', [])
                        
                        cash_from_sale = strategy.get('cash_from_sale', 0)
                        loss_amount = strategy.get('loss_amount', 0)
                        cash_from_sale_text = format_currency_safe(cash_from_sale, is_korean)
                        loss_amount_text = format_currency_safe(loss_amount, is_korean)
                        
                        icon = "⚖️" if strategy_key == '3_50_percent_cutloss' else "🛡️"
                        
                        report += f"""

{icon} **{strategy['name']}**
• 설명: {strategy['description']}
• 손절 주식: {strategy.get('cutloss_shares', 0):,.0f}주
• 보유 주식: {strategy.get('remaining_shares', 0):,.0f}주
• 확보 현금: {cash_from_sale_text}
• 손실: {loss_amount_text} ({strategy.get('loss_pct', 0):.1f}%)

📊 **재매수 후 총 보유 주식 (주요 구간):**"""
                        
                        key_scenarios = [s for s in scenarios if s['additional_decline_pct'] in [20, 30, 50, 70]]
                        for scenario in key_scenarios:
                            report += f"""
• 추가 {scenario['additional_decline_pct']:.0f}% 하락 시: {scenario['total_shares']:,.0f}주 총 보유 (원래의 {scenario['increase_ratio']:.1f}배)"""
                        
                        report += f"""
• 장점: {', '.join(strategy.get('pros', []))}
• 단점: {', '.join(strategy.get('cons', []))}"""
                
                # 전략별 기대 시나리오
                scenarios_info = four_strategy_result.get('scenarios', {})
                if scenarios_info:
                    report += f"""

🎯 **시나리오별 최적 전략:**
• 즉시 반등 시: {scenarios_info.get('immediate_recovery', {}).get('best_strategy', 'N/A')}
  → 이유: {scenarios_info.get('immediate_recovery', {}).get('reason', 'N/A')}
• 추가 20% 하락 시: {scenarios_info.get('continued_decline_20', {}).get('best_strategy', 'N/A')}
  → 이유: {scenarios_info.get('continued_decline_20', {}).get('reason', 'N/A')}
• 추가 50% 하락 시: {scenarios_info.get('continued_decline_50', {}).get('best_strategy', 'N/A')}
  → 이유: {scenarios_info.get('continued_decline_50', {}).get('reason', 'N/A')}
• 횡보 지속 시: {scenarios_info.get('sideways', {}).get('best_strategy', 'N/A')}
  → 이유: {scenarios_info.get('sideways', {}).get('reason', 'N/A')}"""
            
            # 나머지 부분들은 간단하게 처리
            crash_metrics = analysis_result.get('crash_metrics', {})
            report += f"""

⚠️ == 주요 위험 지표 =="""
            
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

⚡ == 레버리지 ETF 특별 고려사항 ==
• 3배 레버리지로 인한 변동성 확대
• 일일 리밸런싱으로 장기 보유 시 손실 누적 위험
• 절대 손절선: 15% (일반 주식 대비 엄격한 기준)
• 권장 최대 보유기간: 30일 이내
• 섹터 집중 위험 (반도체 업계 전반적 영향)"""
            
            report += f"""

❓ == 전문가 자문 요청 사항 ==

다음 사항들에 대해 현재 정치·경제적 상황을 고려하여 조언해 주시기 바랍니다:

1. **4가지 전략 중 최적 선택**:
   - 현재 시장 상황에서 가장 합리적인 전략은?
   - 미래 불확실성을 고려할 때 위험 대비 수익이 가장 좋은 전략은?

2. **정치·경제적 환경 분석**:
   - 현재 정치적 상황(정책 변화, 규제 등)이 해당 종목에 미치는 영향
   - 경제적 지표(금리, 인플레이션, GDP 등)가 섹터에 미치는 영향
   - 국제적 요인(무역분쟁, 지정학적 리스크 등) 고려사항

3. **리스크 관리 전략**:
   - 현재 위험도 {risk_score:.0f}점에 대한 객관적 평가
   - 각 전략의 리스크-리턴 프로파일 분석
   - 추가 모니터링해야 할 핵심 지표나 이벤트

4. **실행 전략 및 타이밍**:
   - 구체적이고 실행 가능한 단계별 행동 계획
   - 각 전략 실행 시 주의사항 및 조건
   - 감정적 판단을 배제한 객관적 기준점 설정

5. **미래 시나리오별 대응**:
   - 즉시 반등 vs 추가 하락 각각의 확률적 평가
   - 장기적 관점에서의 해당 종목/섹터 전망
   - 포트폴리오 차원에서의 종합적 조언

**특히 중요한 것은:**
- 감정이 아닌 데이터와 논리에 기반한 객관적 분석
- 현실적으로 실행 가능한 구체적 조언
- 정치·경제적 거시 환경과 개별 종목 분석의 조화
- 불확실성 하에서의 최적 의사결정 가이드라인

---
Generated by 1Bo's Plan Enhanced Crash Analyzer v2.2 (F-string Fixed)
분석 도구: 기술적 분석 + 포트폴리오 분석 + 위험도 평가 + 4가지 전략 분석 통합"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Comprehensive AI report generation failed: {e}")
            return f"종합 리포트 생성 실패: {e}"