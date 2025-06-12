#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Analysis Engine Module
기술적 분석 엔진 - 매매 시점 분석, SP500 비교, 신뢰구간 계산

Author: AI Assistant & User
Version: 2.1.0
"""

import pandas as pd
import numpy as np
import yfinance as yf
from datetime import datetime, timedelta
import logging
from .utils import Logger


class AnalysisEngine:
    """기술적 분석 엔진 - 매매 시점 분석, SP500 비교, 신뢰구간 계산"""
    
    def __init__(self):
        self.logger = Logger('AnalysisEngine')
        self.sp500_data = None
        self.sp500_cache_time = None
        
    def analyze_stock(self, data, symbol=None):
        """종합 주식 분석"""
        try:
            if data is None or data.empty:
                self.logger.warning("No data provided for analysis")
                return None
            
            # 기본 지표 계산
            basic_metrics = self._calculate_basic_metrics(data)
            
            # 기술적 지표 계산
            indicators = self._calculate_technical_indicators(data)
            
            # 3일 평균가 분석
            three_day_analysis = self._analyze_three_day_average(data)
            
            # 95% 신뢰구간 계산
            confidence_interval = self._calculate_confidence_interval(data)
            
            # SP500 비교 분석
            sp500_comparison = self._compare_with_sp500(data, symbol)
            
            # 추세 분석
            trend_analysis = self._analyze_trend(data)
            
            # 매매 신호 생성
            signals = self._generate_signals(data, indicators)
            
            # 매매 결정 분석
            trading_decision = self._analyze_trading_decision(data, indicators, signals)
            
            return {
                'basic_metrics': basic_metrics,
                'indicators': indicators,
                'three_day_analysis': three_day_analysis,
                'confidence_interval': confidence_interval,
                'sp500_comparison': sp500_comparison,
                'trend_analysis': trend_analysis,
                'signals': signals,
                'trading_decision': trading_decision,
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            self.logger.error(f"Stock analysis failed: {e}")
            return None
    
    def _analyze_three_day_average(self, data):
        """최근 3일 평균가 분석"""
        try:
            if len(data) < 3:
                return None
            
            # 최근 3일 종가
            recent_prices = data['Close'].tail(3)
            three_day_avg = recent_prices.mean()
            current_price = data['Close'].iloc[-1]
            
            # 3일 평균 대비 현재가 위치
            deviation_pct = ((current_price - three_day_avg) / three_day_avg) * 100
            
            # 신호 생성
            if deviation_pct > 1.0:
                signal = "강세"
                description = "현재가가 3일 평균보다 높음"
            elif deviation_pct < -1.0:
                signal = "약세"  
                description = "현재가가 3일 평균보다 낮음"
            else:
                signal = "보합"
                description = "현재가가 3일 평균 근처"
            
            return {
                'three_day_average': three_day_avg,
                'current_price': current_price,
                'deviation_pct': deviation_pct,
                'signal': signal,
                'description': description
            }
            
        except Exception as e:
            self.logger.error(f"Three day analysis failed: {e}")
            return None
    
    def _calculate_confidence_interval(self, data, confidence=0.95):
        """95% 신뢰구간 계산"""
        try:
            if len(data) < 30:
                return None
            
            # 최근 30일 수익률 계산
            prices = data['Close'].tail(30)
            returns = prices.pct_change().dropna()
            
            if len(returns) == 0:
                return None
            
            # 통계값 계산
            mean_return = returns.mean()
            std_return = returns.std()
            current_price = data['Close'].iloc[-1]
            
            # 95% 신뢰구간 계산 (z-score = 1.96)
            z_score = 1.96
            margin_of_error = z_score * std_return
            
            # 가격 기준 신뢰구간
            upper_bound = current_price * (1 + mean_return + margin_of_error)
            lower_bound = current_price * (1 + mean_return - margin_of_error)
            
            # 매수/매도 신호 생성
            if current_price < lower_bound:
                position_signal = "🟢 매수 고려 구간"
                signal_strength = "HIGH"
            elif current_price > upper_bound:
                position_signal = "🔴 매도 고려 구간"
                signal_strength = "HIGH"
            else:
                position_signal = "🟡 관망 구간"
                signal_strength = "MEDIUM"
            
            return {
                'upper_bound': upper_bound,
                'lower_bound': lower_bound,
                'current_price': current_price,
                'position_signal': position_signal,
                'signal_strength': signal_strength,
                'mean_return': mean_return,
                'volatility': std_return
            }
            
        except Exception as e:
            self.logger.error(f"Confidence interval calculation failed: {e}")
            return None
    
    def _compare_with_sp500(self, data, symbol):
        """SP500과 비교 분석"""
        try:
            if len(data) < 30:
                return None
            
            # SP500 데이터 가져오기
            sp500_data = self._get_sp500_data()
            if sp500_data is None or sp500_data.empty:
                return None
            
            # 같은 기간 맞추기
            start_date = data.index[0]
            sp500_period = sp500_data[sp500_data.index >= start_date]
            
            if len(sp500_period) < 10:
                return None
            
            # 수익률 계산
            stock_returns = data['Close'].pct_change().dropna()
            sp500_returns = sp500_period['Close'].pct_change().dropna()
            
            # 기간 맞추기
            min_length = min(len(stock_returns), len(sp500_returns))
            if min_length < 10:
                return None
                
            stock_returns = stock_returns.tail(min_length)
            sp500_returns = sp500_returns.tail(min_length)
            
            # 누적 수익률
            stock_cumulative = (1 + stock_returns).cumprod().iloc[-1] - 1
            sp500_cumulative = (1 + sp500_returns).cumprod().iloc[-1] - 1
            
            # 상대 성과
            relative_performance = stock_cumulative - sp500_cumulative
            
            # 베타 계산
            beta = np.cov(stock_returns, sp500_returns)[0][1] / np.var(sp500_returns)
            
            # 상관관계
            correlation = np.corrcoef(stock_returns, sp500_returns)[0][1]
            
            # 성과 평가
            if relative_performance > 0.05:  # 5% 이상 우수
                performance_rating = "🎯 우수"
            elif relative_performance > 0:
                performance_rating = "🔵 양호"
            elif relative_performance > -0.05:
                performance_rating = "🟡 유사"
            else:
                performance_rating = "🔴 부진"
            
            return {
                'stock_return': stock_cumulative,
                'sp500_return': sp500_cumulative,
                'relative_performance': relative_performance,
                'relative_performance_pct': relative_performance * 100,
                'beta': beta,
                'correlation': correlation,
                'performance_rating': performance_rating,
                'analysis_period_days': min_length
            }
            
        except Exception as e:
            self.logger.error(f"SP500 comparison failed: {e}")
            return None
    
    def _get_sp500_data(self):
        """SP500 데이터 가져오기 (캐시 적용)"""
        try:
            # 캐시 확인 (1시간마다 갱신)
            if (self.sp500_data is not None and 
                self.sp500_cache_time is not None and 
                datetime.now() - self.sp500_cache_time < timedelta(hours=1)):
                return self.sp500_data
            
            # 새로운 데이터 다운로드
            sp500 = yf.download('^GSPC', period='1y', progress=False)
            if not sp500.empty:
                self.sp500_data = sp500
                self.sp500_cache_time = datetime.now()
                self.logger.info("SP500 data updated successfully")
                return sp500
            
            return None
            
        except Exception as e:
            self.logger.error(f"SP500 data download failed: {e}")
            return None
    
    def _analyze_trading_decision(self, data, indicators, signals):
        """매매 결정 분석"""
        try:
            current_price = data['Close'].iloc[-1]
            
            # 신호 점수 계산
            buy_score = 0
            sell_score = 0
            
            # RSI 기반 점수
            if 'rsi' in indicators:
                rsi = indicators['rsi']
                if rsi < 30:
                    buy_score += 3
                elif rsi < 40:
                    buy_score += 1
                elif rsi > 70:
                    sell_score += 3
                elif rsi > 60:
                    sell_score += 1
            
            # 이동평균 기반 점수
            ma_signals = 0
            for period in [5, 20, 60]:
                if f'ma_{period}' in indicators:
                    if current_price > indicators[f'ma_{period}']:
                        ma_signals += 1
                    else:
                        ma_signals -= 1
            
            if ma_signals >= 2:
                buy_score += 2
            elif ma_signals <= -2:
                sell_score += 2
            
            # MACD 기반 점수
            if 'macd_trend' in indicators:
                if indicators['macd_trend'] == 'BULLISH':
                    buy_score += 1
                else:
                    sell_score += 1
            
            # 볼린저 밴드 기반 점수
            if 'bb_signal' in indicators:
                if indicators['bb_signal'] == 'OVERSOLD':
                    buy_score += 2
                elif indicators['bb_signal'] == 'OVERBOUGHT':
                    sell_score += 2
            
            # 최종 결정
            total_score = buy_score - sell_score
            
            if total_score >= 4:
                decision = 'STRONG_BUY'
                confidence = 'HIGH'
                signal_text = '🚀 적극매수'
            elif total_score >= 2:
                decision = 'BUY'
                confidence = 'MEDIUM'
                signal_text = '📈 매수'
            elif total_score <= -4:
                decision = 'STRONG_SELL'
                confidence = 'HIGH'
                signal_text = '🔻 적극매도'
            elif total_score <= -2:
                decision = 'SELL'
                confidence = 'MEDIUM'
                signal_text = '📉 매도'
            else:
                decision = 'HOLD'
                confidence = 'LOW'
                signal_text = '⏸️ 관망'
            
            return {
                'decision': decision,
                'signal_text': signal_text,
                'confidence': confidence,
                'buy_score': buy_score,
                'sell_score': sell_score,
                'total_score': total_score,
                'reasoning': self._generate_decision_reasoning(indicators, buy_score, sell_score)
            }
            
        except Exception as e:
            self.logger.error(f"Trading decision analysis failed: {e}")
            return None
    
    def _generate_decision_reasoning(self, indicators, buy_score, sell_score):
        """매매 결정 근거 생성"""
        try:
            reasons = []
            
            # RSI 근거
            if 'rsi' in indicators:
                rsi = indicators['rsi']
                if rsi < 30:
                    reasons.append(f"RSI 과매도 신호 ({rsi:.1f})")
                elif rsi > 70:
                    reasons.append(f"RSI 과매수 신호 ({rsi:.1f})")
            
            # 이동평균 근거
            if 'ma_20' in indicators and 'ma_20_signal' in indicators:
                reasons.append(f"20일선 {'상향' if indicators['ma_20_signal'] == 'BUY' else '하향'} 신호")
            
            # MACD 근거
            if 'macd_trend' in indicators:
                trend = '상승' if indicators['macd_trend'] == 'BULLISH' else '하락'
                reasons.append(f"MACD {trend} 추세")
            
            # 볼린저 밴드 근거
            if 'bb_signal' in indicators:
                if indicators['bb_signal'] == 'OVERSOLD':
                    reasons.append("볼린저 밴드 과매도")
                elif indicators['bb_signal'] == 'OVERBOUGHT':
                    reasons.append("볼린저 밴드 과매수")
            
            return " / ".join(reasons) if reasons else "중립적 신호"
            
        except Exception as e:
            self.logger.error(f"Decision reasoning generation failed: {e}")
            return "분석 불가"

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