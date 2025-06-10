#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Crash Analyzer Module
폭락장 대응 분석 모듈

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
from config import RISK_CONFIG, LEVERAGE_ETFS
from .utils import Logger, format_currency, format_percentage

class CrashAnalyzer:
    """폭락장 분석 클래스"""
    
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
    
    def calculate_optimal_cutloss(self, current_price, symbol, is_leverage=None):
        """최적 손절가 계산"""
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
    
    def generate_situation_report(self, analysis_result):
        """AI 자문용 상황 리포트 생성"""
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

📊 기본 정보:
• 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
• 분석 종목: {symbol}
• 현재가: {format_currency(current_price)}
• 위험 점수: {risk_score:.1f}/100점
• 심각도: {severity['emoji']} {severity['description']}

🎯 현재 상황:
{recommendation['action']}
{recommendation['details']}

❓ 전문가 자문 요청 사항:
1. 현재 상황에 대한 객관적 진단
2. 가장 합리적인 대응 전략
3. 위험 관리 관점에서의 핵심 고려사항
4. 향후 모니터링해야 할 지표

특히 감정적 판단이 아닌 데이터와 논리에 기반한
객관적 분석과 실행 가능한 구체적 조언을 원합니다.

---
Generated by 1Bo's Plan Crash Analyzer v1.0
"""
            
            return report
            
        except Exception as e:
            self.logger.error(f"Situation report generation failed: {e}")
            return f"리포트 생성 실패: {e}"