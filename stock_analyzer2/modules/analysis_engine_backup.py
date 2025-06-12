#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Enhanced Analysis Engine Module
기술적 분석 엔진 (매매 시점 분석 강화)

Author: AI Assistant & User
Version: 1.1.0 - 매매 시점 분석 및 SP500 비교 추가
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
import sys
import yfinance as yf

# 로컬 모듈 import
sys.path.append(str(Path(__file__).parent.parent))
from .utils import Logger, format_percentage

class AnalysisEngine:
    """기술적 분석 엔진 클래스"""
    
    def __init__(self):
        self.logger = Logger("AnalysisEngine")
        self.sp500_cache = None
        self.sp500_cache_time = None
    
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
            
            # 🎯 새로운 기능들 추가
            recent_stats = self._calculate_recent_statistics(data)
            confidence_interval = self._calculate_confidence_interval(data)
            sp500_comparison = self._compare_with_sp500(data, symbol)
            trading_decision = self._analyze_trading_decision(data, technical_indicators, signals)
            
            result = {
                'symbol': symbol,
                'current_price': latest_price,
                'basic_metrics': basic_metrics,
                'technical_indicators': technical_indicators,
                'trend_analysis': trend_analysis,
                'signals': signals,
                'recent_stats': recent_stats,  # 🎯 추가
                'confidence_interval': confidence_interval,  # 🎯 추가
                'sp500_comparison': sp500_comparison,  # 🎯 추가
                'trading_decision': trading_decision,  # 🎯 추가
                'analysis_time': datetime.now().isoformat()
            }
            
            self.logger.info(f"Enhanced analysis completed for {symbol}")
            return result
            
        except Exception as e:
            self.logger.error(f"Stock analysis failed: {e}")
            return None
    
    def _calculate_recent_statistics(self, data):
        """최근 3일 통계 계산"""
        try:
            if len(data) < 3:
                return None
            
            recent_3_days = data['Close'].tail(3)
            avg_3_days = recent_3_days.mean()
            current_price = data['Close'].iloc[-1]
            
            # 3일 평균과 현재가 비교
            diff_from_avg = current_price - avg_3_days
            diff_pct = (diff_from_avg / avg_3_days) * 100
            
            return {
                'avg_3_days': avg_3_days,
                'diff_from_avg': diff_from_avg,
                'diff_pct': diff_pct,
                'trend_signal': 'ABOVE_AVG' if diff_pct > 1 else 'BELOW_AVG' if diff_pct < -1 else 'NEAR_AVG'
            }
            
        except Exception as e:
            self.logger.error(f"Recent statistics calculation failed: {e}")
            return None
    
    def _calculate_confidence_interval(self, data, confidence_level=0.95):
        """95% 신뢰구간 계산"""
        try:
            if len(data) < 30:  # 최소 30일 데이터 필요
                return None
            
            recent_data = data['Close'].tail(30)  # 최근 30일
            mean_price = recent_data.mean()
            std_price = recent_data.std()
            
            # 95% 신뢰구간 계산 (z-score = 1.96)
            z_score = 1.96
            margin_error = z_score * (std_price / np.sqrt(len(recent_data)))
            
            lower_bound = mean_price - margin_error
            upper_bound = mean_price + margin_error
            current_price = data['Close'].iloc[-1]
            
            # 현재가가 신뢰구간의 어디에 위치하는지 확인
            if current_price < lower_bound:
                position = 'BELOW_CI'
                signal = 'POTENTIAL_BUY'
            elif current_price > upper_bound:
                position = 'ABOVE_CI'
                signal = 'POTENTIAL_SELL'
            else:
                position = 'WITHIN_CI'
                signal = 'HOLD'
            
            return {
                'mean_price': mean_price,
                'std_price': std_price,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound,
                'margin_error': margin_error,
                'position': position,
                'signal': signal,
                'confidence_level': confidence_level
            }
            
        except Exception as e:
            self.logger.error(f"Confidence interval calculation failed: {e}")
            return None
    
    def _compare_with_sp500(self, data, symbol):
        """SP500 지수와 비교"""
        try:
            # 한국 주식의 경우 KOSPI와 비교하는 것이 더 적절하지만, 
            # 요구사항에 따라 SP500과 비교
            sp500_data = self._get_sp500_data()
            if sp500_data is None:
                return None
            
            # 같은 기간 데이터 맞추기
            start_date = data.index[0]
            end_date = data.index[-1]
            
            # SP500 데이터에서 같은 기간 추출
            try:
                sp500_period = sp500_data.loc[start_date:end_date]
            except:
                # 인덱스가 정확히 맞지 않는 경우 근사치 사용
                sp500_period = sp500_data[sp500_data.index >= start_date]
                sp500_period = sp500_period[sp500_period.index <= end_date]
            
            if sp500_period is None or len(sp500_period) < 5:
                return None
            
            # 수익률 계산 (최근 30일)
            period_days = min(30, len(data), len(sp500_period))
            
            if period_days < 5:
                return None
            
            stock_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-period_days]) - 1) * 100
            sp500_return = ((sp500_period['Close'].iloc[-1] / sp500_period['Close'].iloc[-period_days]) - 1) * 100
            
            # 베타 계산 (주식과 SP500의 상관관계)
            stock_returns = data['Close'].pct_change().dropna().tail(period_days)
            sp500_returns = sp500_period['Close'].pct_change().dropna().tail(period_days)
            
            # 같은 길이로 맞추기
            min_length = min(len(stock_returns), len(sp500_returns))
            if min_length > 5:
                stock_returns = stock_returns.tail(min_length)
                sp500_returns = sp500_returns.tail(min_length)
                
                correlation = np.corrcoef(stock_returns, sp500_returns)[0, 1]
                if not np.isnan(correlation) and np.var(sp500_returns) > 0:
                    beta = np.cov(stock_returns, sp500_returns)[0, 1] / np.var(sp500_returns)
                else:
                    beta = 1.0
                    correlation = 0.0
            else:
                correlation = 0.0
                beta = 1.0
            
            # 상대적 성과
            relative_performance = stock_return - sp500_return
            
            return {
                'sp500_return': sp500_return,
                'stock_return': stock_return,
                'relative_performance': relative_performance,
                'correlation': correlation,
                'beta': beta,
                'outperforming': relative_performance > 0,
                'period_days': period_days
            }
            
        except Exception as e:
            self.logger.error(f"SP500 comparison failed: {e}")
            return None
    
    def _get_sp500_data(self):
        """SP500 데이터 가져오기 (캐시 사용)"""
        try:
            # 캐시 체크 (1시간 유효)
            if (self.sp500_cache is not None and 
                self.sp500_cache_time is not None and 
                (datetime.now() - self.sp500_cache_time).total_seconds() < 3600):
                return self.sp500_cache
            
            # SP500 데이터 다운로드 (^GSPC)
            sp500 = yf.download("^GSPC", period="1y", interval="1d", progress=False)
            
            if sp500 is not None and not sp500.empty:
                self.sp500_cache = sp500
                self.sp500_cache_time = datetime.now()
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
            elif total_score >= 2:
                decision = 'BUY'
                confidence = 'MEDIUM'
            elif total_score <= -4:
                decision = 'STRONG_SELL'
                confidence = 'HIGH'
            elif total_score <= -2:
                decision = 'SELL'
                confidence = 'MEDIUM'
            else:
                decision = 'HOLD'
                confidence = 'LOW'
            
            return {
                'decision': decision,
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
            if 'ma_20' in indicators:
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

    # 기존 메서드들은 그대로 유지
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