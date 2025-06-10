#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
기술적 분석 모듈
다양한 기술적 지표 계산 및 분석
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

class TechnicalAnalysis:
    def __init__(self):
        """기술적 분석 클래스 초기화"""
        self.indicators = {}
        
    def calculate_sma(self, data, window=20):
        """단순 이동평균 (Simple Moving Average)"""
        try:
            return data['Close'].rolling(window=window).mean()
        except Exception as e:
            print(f"SMA 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_ema(self, data, window=20):
        """지수 이동평균 (Exponential Moving Average)"""
        try:
            return data['Close'].ewm(span=window).mean()
        except Exception as e:
            print(f"EMA 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_rsi(self, data, window=14):
        """상대강도지수 (Relative Strength Index)"""
        try:
            close = data['Close']
            delta = close.diff()
            
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=window).mean()
            avg_loss = loss.rolling(window=window).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            print(f"RSI 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_macd(self, data, fast=12, slow=26, signal=9):
        """MACD (Moving Average Convergence Divergence)"""
        try:
            close = data['Close']
            
            # MACD 라인
            ema_fast = close.ewm(span=fast).mean()
            ema_slow = close.ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            
            # 시그널 라인
            signal_line = macd_line.ewm(span=signal).mean()
            
            # 히스토그램
            histogram = macd_line - signal_line
            
            return {
                'MACD': macd_line,
                'MACD_Signal': signal_line,
                'MACD_Histogram': histogram
            }
        except Exception as e:
            print(f"MACD 계산 오류: {e}")
            return {
                'MACD': pd.Series([np.nan] * len(data), index=data.index),
                'MACD_Signal': pd.Series([np.nan] * len(data), index=data.index),
                'MACD_Histogram': pd.Series([np.nan] * len(data), index=data.index)
            }
            
    def calculate_bollinger_bands(self, data, window=20, num_std=2):
        """볼린저 밴드 (Bollinger Bands)"""
        try:
            close = data['Close']
            sma = close.rolling(window=window).mean()
            std = close.rolling(window=window).std()
            
            upper_band = sma + (std * num_std)
            lower_band = sma - (std * num_std)
            
            return {
                'BB_Upper': upper_band,
                'BB_Middle': sma,
                'BB_Lower': lower_band,
                'BB_Width': upper_band - lower_band,
                'BB_Position': (close - lower_band) / (upper_band - lower_band)
            }
        except Exception as e:
            print(f"볼린저 밴드 계산 오류: {e}")
            return {
                'BB_Upper': pd.Series([np.nan] * len(data), index=data.index),
                'BB_Middle': pd.Series([np.nan] * len(data), index=data.index),
                'BB_Lower': pd.Series([np.nan] * len(data), index=data.index),
                'BB_Width': pd.Series([np.nan] * len(data), index=data.index),
                'BB_Position': pd.Series([np.nan] * len(data), index=data.index)
            }
            
    def calculate_stochastic(self, data, window=14, smooth_k=3, smooth_d=3):
        """스토캐스틱 오실레이터 (Stochastic Oscillator)"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # %K 계산
            lowest_low = low.rolling(window=window).min()
            highest_high = high.rolling(window=window).max()
            
            k_percent = 100 * ((close - lowest_low) / (highest_high - lowest_low))
            
            # %K 스무딩
            k_percent_smooth = k_percent.rolling(window=smooth_k).mean()
            
            # %D 계산 (%K의 이동평균)
            d_percent = k_percent_smooth.rolling(window=smooth_d).mean()
            
            return {
                'Stoch_K': k_percent_smooth,
                'Stoch_D': d_percent
            }
        except Exception as e:
            print(f"스토캐스틱 계산 오류: {e}")
            return {
                'Stoch_K': pd.Series([np.nan] * len(data), index=data.index),
                'Stoch_D': pd.Series([np.nan] * len(data), index=data.index)
            }
            
    def calculate_atr(self, data, window=14):
        """평균 참 범위 (Average True Range)"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # 참 범위 계산
            tr1 = high - low
            tr2 = abs(high - close.shift())
            tr3 = abs(low - close.shift())
            
            true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
            atr = true_range.rolling(window=window).mean()
            
            return atr
        except Exception as e:
            print(f"ATR 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_williams_r(self, data, window=14):
        """윌리엄스 %R (Williams %R)"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            highest_high = high.rolling(window=window).max()
            lowest_low = low.rolling(window=window).min()
            
            williams_r = -100 * ((highest_high - close) / (highest_high - lowest_low))
            
            return williams_r
        except Exception as e:
            print(f"Williams %R 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_cci(self, data, window=20):
        """상품 채널 지수 (Commodity Channel Index)"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # 전형적인 가격 (Typical Price)
            typical_price = (high + low + close) / 3
            
            # 단순 이동평균
            sma_tp = typical_price.rolling(window=window).mean()
            
            # 평균 편차
            mad = typical_price.rolling(window=window).apply(
                lambda x: np.mean(np.abs(x - np.mean(x)))
            )
            
            # CCI 계산
            cci = (typical_price - sma_tp) / (0.015 * mad)
            
            return cci
        except Exception as e:
            print(f"CCI 계산 오류: {e}")
            return pd.Series([np.nan] * len(data), index=data.index)
            
    def calculate_volume_indicators(self, data):
        """거래량 지표들"""
        try:
            close = data['Close']
            volume = data['Volume']
            
            # 거래량 이동평균
            volume_sma = volume.rolling(window=20).mean()
            
            # 상대 거래량
            relative_volume = volume / volume_sma
            
            # OBV (On Balance Volume)
            price_change = close.diff()
            obv = (np.sign(price_change) * volume).cumsum()
            
            # 거래량 가중 평균 가격 (VWAP)
            typical_price = (data['High'] + data['Low'] + close) / 3
            vwap = (typical_price * volume).cumsum() / volume.cumsum()
            
            return {
                'Volume_SMA': volume_sma,
                'Relative_Volume': relative_volume,
                'OBV': obv,
                'VWAP': vwap
            }
        except Exception as e:
            print(f"거래량 지표 계산 오류: {e}")
            return {
                'Volume_SMA': pd.Series([np.nan] * len(data), index=data.index),
                'Relative_Volume': pd.Series([np.nan] * len(data), index=data.index),
                'OBV': pd.Series([np.nan] * len(data), index=data.index),
                'VWAP': pd.Series([np.nan] * len(data), index=data.index)
            }
            
    def calculate_support_resistance(self, data, window=20):
        """지지선/저항선 계산"""
        try:
            high = data['High']
            low = data['Low']
            close = data['Close']
            
            # 피벗 포인트
            pivot = (high + low + close) / 3
            
            # 저항선들
            resistance1 = 2 * pivot - low
            resistance2 = pivot + (high - low)
            
            # 지지선들
            support1 = 2 * pivot - high
            support2 = pivot - (high - low)
            
            return {
                'Pivot': pivot,
                'Resistance1': resistance1,
                'Resistance2': resistance2,
                'Support1': support1,
                'Support2': support2
            }
        except Exception as e:
            print(f"지지/저항선 계산 오류: {e}")
            return {
                'Pivot': pd.Series([np.nan] * len(data), index=data.index),
                'Resistance1': pd.Series([np.nan] * len(data), index=data.index),
                'Resistance2': pd.Series([np.nan] * len(data), index=data.index),
                'Support1': pd.Series([np.nan] * len(data), index=data.index),
                'Support2': pd.Series([np.nan] * len(data), index=data.index)
            }
            
    def calculate_all_indicators(self, data):
        """모든 기술적 지표 계산"""
        if data is None or data.empty:
            return None
            
        try:
            indicators = {}
            
            # 이동평균들
            indicators['SMA_5'] = self.calculate_sma(data, 5)
            indicators['SMA_10'] = self.calculate_sma(data, 10)
            indicators['SMA_20'] = self.calculate_sma(data, 20)
            indicators['SMA_50'] = self.calculate_sma(data, 50)
            indicators['SMA_200'] = self.calculate_sma(data, 200)
            
            indicators['EMA_5'] = self.calculate_ema(data, 5)
            indicators['EMA_10'] = self.calculate_ema(data, 10)
            indicators['EMA_20'] = self.calculate_ema(data, 20)
            indicators['EMA_50'] = self.calculate_ema(data, 50)
            
            # 모멘텀 지표들
            indicators['RSI'] = self.calculate_rsi(data, 14)
            
            # MACD
            macd_data = self.calculate_macd(data)
            indicators.update(macd_data)
            
            # 볼린저 밴드
            bb_data = self.calculate_bollinger_bands(data)
            indicators.update(bb_data)
            
            # 스토캐스틱
            stoch_data = self.calculate_stochastic(data)
            indicators.update(stoch_data)
            
            # 기타 지표들
            indicators['ATR'] = self.calculate_atr(data)
            indicators['Williams_R'] = self.calculate_williams_r(data)
            indicators['CCI'] = self.calculate_cci(data)
            
            # 거래량 지표들
            volume_data = self.calculate_volume_indicators(data)
            indicators.update(volume_data)
            
            # 지지/저항선
            sr_data = self.calculate_support_resistance(data)
            indicators.update(sr_data)
            
            return indicators
            
        except Exception as e:
            print(f"기술적 지표 계산 오류: {e}")
            return None
            
    def get_trading_signals(self, data, indicators=None):
        """매매 신호 생성"""
        if indicators is None:
            indicators = self.calculate_all_indicators(data)
            
        if indicators is None:
            return None
            
        signals = {}
        
        try:
            # RSI 신호
            rsi = indicators.get('RSI')
            if rsi is not None:
                signals['RSI_Signal'] = np.where(rsi < 30, 'BUY',
                                               np.where(rsi > 70, 'SELL', 'HOLD'))
            
            # MACD 신호
            macd = indicators.get('MACD')
            macd_signal = indicators.get('MACD_Signal')
            if macd is not None and macd_signal is not None:
                signals['MACD_Signal'] = np.where(macd > macd_signal, 'BUY',
                                                np.where(macd < macd_signal, 'SELL', 'HOLD'))
            
            # 볼린저 밴드 신호
            bb_position = indicators.get('BB_Position')
            if bb_position is not None:
                signals['BB_Signal'] = np.where(bb_position < 0.2, 'BUY',
                                              np.where(bb_position > 0.8, 'SELL', 'HOLD'))
            
            # 스토캐스틱 신호
            stoch_k = indicators.get('Stoch_K')
            stoch_d = indicators.get('Stoch_D')
            if stoch_k is not None and stoch_d is not None:
                signals['Stoch_Signal'] = np.where((stoch_k < 20) & (stoch_k > stoch_d), 'BUY',
                                                 np.where((stoch_k > 80) & (stoch_k < stoch_d), 'SELL', 'HOLD'))
            
            # 이동평균 신호
            close = data['Close']
            sma_20 = indicators.get('SMA_20')
            sma_50 = indicators.get('SMA_50')
            if sma_20 is not None and sma_50 is not None:
                signals['MA_Signal'] = np.where((close > sma_20) & (sma_20 > sma_50), 'BUY',
                                              np.where((close < sma_20) & (sma_20 < sma_50), 'SELL', 'HOLD'))
            
            return signals
            
        except Exception as e:
            print(f"매매 신호 생성 오류: {e}")
            return None
            
    def analyze_trend(self, data, indicators=None):
        """추세 분석"""
        if indicators is None:
            indicators = self.calculate_all_indicators(data)
            
        if indicators is None:
            return None
            
        try:
            close = data['Close']
            analysis = {}
            
            # 단기 추세 (20일)
            sma_20 = indicators.get('SMA_20')
            if sma_20 is not None:
                short_trend = 'UP' if close.iloc[-1] > sma_20.iloc[-1] else 'DOWN'
                analysis['short_trend'] = short_trend
            
            # 중기 추세 (50일)
            sma_50 = indicators.get('SMA_50')
            if sma_50 is not None:
                medium_trend = 'UP' if close.iloc[-1] > sma_50.iloc[-1] else 'DOWN'
                analysis['medium_trend'] = medium_trend
            
            # 장기 추세 (200일)
            sma_200 = indicators.get('SMA_200')
            if sma_200 is not None:
                long_trend = 'UP' if close.iloc[-1] > sma_200.iloc[-1] else 'DOWN'
                analysis['long_trend'] = long_trend
            
            # 전체 추세 강도
            trend_strength = 0
            if analysis.get('short_trend') == 'UP':
                trend_strength += 1
            if analysis.get('medium_trend') == 'UP':
                trend_strength += 1
            if analysis.get('long_trend') == 'UP':
                trend_strength += 1
                
            if trend_strength >= 2:
                analysis['overall_trend'] = 'BULLISH'
            elif trend_strength <= 1:
                analysis['overall_trend'] = 'BEARISH'
            else:
                analysis['overall_trend'] = 'NEUTRAL'
                
            # 변동성 분석
            atr = indicators.get('ATR')
            if atr is not None:
                current_atr = atr.iloc[-1]
                avg_atr = atr.rolling(window=20).mean().iloc[-1]
                volatility = 'HIGH' if current_atr > avg_atr * 1.5 else 'NORMAL'
                analysis['volatility'] = volatility
            
            return analysis
            
        except Exception as e:
            print(f"추세 분석 오류: {e}")
            return None
            
    def calculate_risk_metrics(self, data, risk_free_rate=0.02):
        """리스크 지표 계산"""
        try:
            close = data['Close']
            returns = close.pct_change().dropna()
            
            metrics = {}
            
            # 변동성 (연율화)
            volatility = returns.std() * np.sqrt(252)
            metrics['volatility'] = volatility
            
            # 샤프 비율
            excess_returns = returns.mean() * 252 - risk_free_rate
            sharpe_ratio = excess_returns / volatility if volatility != 0 else 0
            metrics['sharpe_ratio'] = sharpe_ratio
            
            # 최대 낙폭 (Maximum Drawdown)
            cumulative = (1 + returns).cumprod()
            rolling_max = cumulative.expanding().max()
            drawdown = (cumulative - rolling_max) / rolling_max
            max_drawdown = drawdown.min()
            metrics['max_drawdown'] = abs(max_drawdown)
            
            # VaR (Value at Risk) - 95% 신뢰구간
            var_95 = np.percentile(returns, 5)
            metrics['var_95'] = abs(var_95)
            
            # 베타 계산 (시장 지수 대비) - 여기서는 자체 변동성 사용
            beta = volatility / volatility  # 단순화
            metrics['beta'] = beta
            
            return metrics
            
        except Exception as e:
            print(f"리스크 지표 계산 오류: {e}")
            return None
            
    def generate_analysis_summary(self, data):
        """종합 분석 요약"""
        try:
            indicators = self.calculate_all_indicators(data)
            signals = self.get_trading_signals(data, indicators)
            trend_analysis = self.analyze_trend(data, indicators)
            risk_metrics = self.calculate_risk_metrics(data)
            
            # 최신 값들
            latest = data.iloc[-1]
            latest_indicators = {}
            
            if indicators:
                for key, series in indicators.items():
                    if isinstance(series, pd.Series) and not series.empty:
                        latest_indicators[key] = series.iloc[-1]
            
            summary = {
                'symbol': 'UNKNOWN',
                'analysis_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'current_price': latest['Close'],
                'price_change': latest['Close'] - data.iloc[-2]['Close'] if len(data) > 1 else 0,
                'indicators': latest_indicators,
                'signals': signals,
                'trend_analysis': trend_analysis,
                'risk_metrics': risk_metrics,
                'recommendation': self._generate_recommendation(signals, trend_analysis)
            }
            
            return summary
            
        except Exception as e:
            print(f"분석 요약 생성 오류: {e}")
            return None
            
    def _generate_recommendation(self, signals, trend_analysis):
        """추천 의견 생성"""
        if not signals or not trend_analysis:
            return "HOLD"
            
        try:
            buy_signals = 0
            sell_signals = 0
            
            # 신호 집계
            for signal_name, signal_values in signals.items():
                if isinstance(signal_values, np.ndarray) and len(signal_values) > 0:
                    latest_signal = signal_values[-1]
                    if latest_signal == 'BUY':
                        buy_signals += 1
                    elif latest_signal == 'SELL':
                        sell_signals += 1
            
            # 추세 고려
            overall_trend = trend_analysis.get('overall_trend', 'NEUTRAL')
            
            if buy_signals > sell_signals and overall_trend == 'BULLISH':
                return "STRONG_BUY"
            elif buy_signals > sell_signals:
                return "BUY"
            elif sell_signals > buy_signals and overall_trend == 'BEARISH':
                return "STRONG_SELL"
            elif sell_signals > buy_signals:
                return "SELL"
            else:
                return "HOLD"
                
        except Exception as e:
            print(f"추천 의견 생성 오류: {e}")
            return "HOLD"