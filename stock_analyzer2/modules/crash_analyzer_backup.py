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
                '2_100_percent_cutl