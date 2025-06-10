#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Analysis Engine Module
기술적 분석 엔진

Author: AI Assistant & User
Version: 1.0.0
"""

import pandas as pd
import numpy as np
from datetime import datetime
from pathlib import Path
import sys

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from .utils import Logger, format_percentage

class AnalysisEngine:
    """기술적 분석 엔진 클래스"""
    
    def __init__(self):
        self.logger = Logger("AnalysisEngine")
    
    def analyze_stock(self, data, symbol):
        """종합 주식 분석"""
        try:
            if data is None or data.empty:
                return None
            
            latest_price = data['Close'].iloc[-1]
            
            # 기본 지표 계산
            basic_metrics = self._calculate_basic_metrics(data)
            
            # 기술적 지표
            technical_indicators = self._calculate_technical_indicators(data)
            
            # 추세 분석
            trend_analysis = self._analyze_trend(data)
            
            # 매매 신호
            signals = self._generate_signals(data, technical_indicators)
            
            result = {
                'symbol': symbol,
                'current_price': latest_price,
                'basic_metrics': basic_metrics,
                'technical_indicators': technical_indicators,
                'trend_analysis': trend_analysis,
                'signals': signals,
                'analysis_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Analysis completed for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Stock analysis failed: {e}")
            return None
    
    def _calculate_basic_metrics(self, data):
        """기본 지표 계산"""
        try:
            current_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else current_price
            
            # 변화율
            daily_change = current_price - prev_price
            daily_change_pct = (daily_change / prev_price) * 100 if prev_price > 0 else 0
            
            # 52주 최고/최저
            high_52w = data['High'].max()
            low_52w = data['Low'].min()
            
            # 평균 거래량
            avg_volume = data['Volume'].mean()
            recent_volume = data['Volume'].iloc[-1]
            
            return {
                'daily_change': daily_change,
                'daily_change_pct': daily_change_pct,
                'high_52w': high_52w,
                'low_52w': low_52w,
                'high_52w_pct': ((current_price - high_52w) / high_52w) * 100,
                'low_52w_pct': ((current_price - low_52w) / low_52w) * 100,
                'avg_volume': avg_volume,
                'recent_volume': recent_volume,
                'volume_ratio': recent_volume / avg_volume if avg_volume > 0 else 1
            }
            
        except Exception as e:
            self.logger.error(f"Basic metrics calculation failed: {e}")
            return {}
    
    def _calculate_technical_indicators(self, data):
        """기술적 지표 계산"""
        try:
            indicators = {}
            
            # 이동평균
            for period in [5, 20, 60, 200]:
                if len(data) >= period:
                    ma = data['Close'].rolling(period).mean().iloc[-1]
                    indicators[f'ma_{period}'] = ma
                    indicators[f'ma_{period}_signal'] = 'BUY' if data['Close'].iloc[-1] > ma else 'SELL'
            
            # RSI 계산
            rsi = self._calculate_rsi(data['Close'])
            if rsi is not None:
                indicators['rsi'] = rsi
                if rsi > 70:
                    indicators['rsi_signal'] = 'OVERBOUGHT'
                elif rsi < 30:
                    indicators['rsi_signal'] = 'OVERSOLD'
                else:
                    indicators['rsi_signal'] = 'NEUTRAL'
            
            # MACD 계산
            macd_data = self._calculate_macd(data['Close'])
            if macd_data:
                indicators.update(macd_data)
            
            # 볼린저 밴드
            bb_data = self._calculate_bollinger_bands(data['Close'])
            if bb_data:
                indicators.update(bb_data)
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Technical indicators calculation failed: {e}")
            return {}
    
    def _calculate_rsi(self, prices, period=14):
        """RSI 계산"""
        try:
            if len(prices) < period:
                return None
            
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi.iloc[-1]
            
        except Exception as e:
            self.logger.error(f"RSI calculation failed: {e}")
            return None
    
    def _calculate_macd(self, prices):
        """MACD 계산"""
        try:
            if len(prices) < 26:
                return None
            
            ema_12 = prices.ewm(span=12).mean()
            ema_26 = prices.ewm(span=26).mean()
            macd_line = ema_12 - ema_26
            signal_line = macd_line.ewm(span=9).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line.iloc[-1],
                'macd_signal': signal_line.iloc[-1],
                'macd_histogram': histogram.iloc[-1],
                'macd_trend': 'BULLISH' if macd_line.iloc[-1] > signal_line.iloc[-1] else 'BEARISH'
            }
            
        except Exception as e:
            self.logger.error(f"MACD calculation failed: {e}")
            return None
    
    def _calculate_bollinger_bands(self, prices, period=20, std_dev=2):
        """볼린저 밴드 계산"""
        try:
            if len(prices) < period:
                return None
            
            sma = prices.rolling(window=period).mean()
            std = prices.rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            current_price = prices.iloc[-1]
            bb_position = (current_price - lower_band.iloc[-1]) / (upper_band.iloc[-1] - lower_band.iloc[-1])
            
            return {
                'bb_upper': upper_band.iloc[-1],
                'bb_middle': sma.iloc[-1],
                'bb_lower': lower_band.iloc[-1],
                'bb_position': bb_position,
                'bb_signal': 'OVERBOUGHT' if bb_position > 0.8 else 'OVERSOLD' if bb_position < 0.2 else 'NEUTRAL'
            }
            
        except Exception as e:
            self.logger.error(f"Bollinger Bands calculation failed: {e}")
            return None
    
    def _analyze_trend(self, data):
        """추세 분석"""
        try:
            prices = data['Close']
            
            # 단기/중기/장기 추세
            short_trend = self._determine_trend(prices.tail(10))
            medium_trend = self._determine_trend(prices.tail(30))
            long_trend = self._determine_trend(prices.tail(60))
            
            # 전체 추세 결정
            trend_signals = [short_trend, medium_trend, long_trend]
            bullish_count = trend_signals.count('BULLISH')
            bearish_count = trend_signals.count('BEARISH')
            
            if bullish_count >= 2:
                overall_trend = 'BULLISH'
            elif bearish_count >= 2:
                overall_trend = 'BEARISH'
            else:
                overall_trend = 'NEUTRAL'
            
            return {
                'short_term': short_trend,
                'medium_term': medium_trend,
                'long_term': long_trend,
                'overall': overall_trend,
                'strength': max(bullish_count, bearish_count) / 3
            }
            
        except Exception as e:
            self.logger.error(f"Trend analysis failed: {e}")
            return {}
    
    def _determine_trend(self, prices):
        """추세 결정"""
        try:
            if len(prices) < 3:
                return 'NEUTRAL'
            
            first_half = prices[:len(prices)//2].mean()
            second_half = prices[len(prices)//2:].mean()
            
            change_pct = ((second_half - first_half) / first_half) * 100
            
            if change_pct > 2:
                return 'BULLISH'
            elif change_pct < -2:
                return 'BEARISH'
            else:
                return 'NEUTRAL'
                
        except Exception as e:
            self.logger.error(f"Trend determination failed: {e}")
            return 'NEUTRAL'
    
    def _generate_signals(self, data, indicators):
        """매매 신호 생성"""
        try:
            signals = []
            
            # RSI 신호
            if 'rsi' in indicators:
                rsi = indicators['rsi']
                if rsi < 30:
                    signals.append({
                        'type': 'BUY',
                        'reason': f'RSI 과매도 ({rsi:.1f})',
                        'strength': 'STRONG' if rsi < 25 else 'MODERATE'
                    })
                elif rsi > 70:
                    signals.append({
                        'type': 'SELL',
                        'reason': f'RSI 과매수 ({rsi:.1f})',
                        'strength': 'STRONG' if rsi > 75 else 'MODERATE'
                    })
            
            # MACD 신호
            if 'macd_trend' in indicators:
                if indicators['macd_trend'] == 'BULLISH':
                    signals.append({
                        'type': 'BUY',
                        'reason': 'MACD 골든크로스',
                        'strength': 'MODERATE'
                    })
                else:
                    signals.append({
                        'type': 'SELL',
                        'reason': 'MACD 데드크로스',
                        'strength': 'MODERATE'
                    })
            
            # 이동평균 신호
            current_price = data['Close'].iloc[-1]
            if 'ma_20' in indicators:
                ma_20 = indicators['ma_20']
                if current_price > ma_20 * 1.02:
                    signals.append({
                        'type': 'BUY',
                        'reason': '20일선 상향돌파',
                        'strength': 'MODERATE'
                    })
                elif current_price < ma_20 * 0.98:
                    signals.append({
                        'type': 'SELL',
                        'reason': '20일선 하향돌파',
                        'strength': 'MODERATE'
                    })
            
            return signals
            
        except Exception as e:
            self.logger.error(f"Signal generation failed: {e}")
            return []