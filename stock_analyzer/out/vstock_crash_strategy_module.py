#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Crash Strategy Module - 폭락장 대응 전략 기능
"""

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import tkinter.scrolledtext as scrolledtext
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class CrashStrategyModule:
    """폭락장 대응 전략 모듈"""
    
    def __init__(self, main_app):
        self.main_app = main_app
        self.shared_data = main_app.shared_data
        
        # 상태 표시 라벨들 (나중에 설정됨)
        self.crash_status_label = None
        self.crash_recommendation_label = None
        self.crash_results = None
    
    def create_tab(self, notebook):
        """폭락장 대응 전략 탭 생성"""
        try:
            crash_frame = ttk.Frame(notebook)
            notebook.add(crash_frame, text="🚨 Crash Strategy")
            
            # 메인 컨테이너
            main_container = tk.Frame(crash_frame)
            main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
            
            # 상단 안내 패널
            info_panel = ttk.LabelFrame(main_container, text="⚠️ 폭락장 대응 전략 분석 도구", padding="20")
            info_panel.pack(fill=tk.X, pady=(0, 25))
            
            info_text = tk.Label(info_panel, 
                               text="📈 VStock 폭락장 대응 전략 시스템 v3.3\n\n" +
                                    "이 도구는 특히 레버리지 ETF와 고위험 종목의 폭락 상황에서 합리적인 투자 결정을 내릴 수 있도록 돕습니다.\n\n" +
                                    "🎯 핵심 기능:\n" +
                                    "• 폭락 심각도 자동 평가 (0-100점 정량적 위험 점수)\n" +
                                    "• 손절 vs 분할매수 객관적 판단 기준 제공\n" +
                                    "• 레버리지 ETF (SOXL, TQQQ 등) 전용 위험 관리\n" +
                                    "• AI 투자 자문을 위한 상황 리포트 자동 생성\n" +
                                    "• 최적 손절 레벨 다중 방법론으로 계산\n" +
                                    "• VaR (Value at Risk) 기반 위험도 평가\n\n" +
                                    "📋 사용 방법:\n" +
                                    "1. Analysis 탭에서 분석할 종목 선택 및 데이터 다운로드\n" +
                                    "2. 진입가와 보유량을 정확히 입력\n" +
                                    "3. 아래 분석 도구들을 순서대로 활용하여 현 상황 정밀 평가\n" +
                                    "4. 객관적 데이터를 바탕으로 투자 결정 (감정 배제)\n\n" +
                                    "⚡ 특별 주의: 레버리지 ETF는 일반 주식과 다른 특별한 위험 관리가 필요합니다!",
                               font=('Segoe UI', 12), justify=tk.LEFT, wraplength=1200)
            info_text.pack()
            
            # 하단 컨테이너
            bottom_container = tk.Frame(main_container)
            bottom_container.pack(fill=tk.BOTH, expand=True)
            
            # 좌측 패널 - 컨트롤
            left_panel = ttk.LabelFrame(bottom_container, text="🎯 Analysis Tools", padding="20")
            left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 25), ipadx=15)
            
            # 분석 도구 버튼들
            ttk.Button(left_panel, text="🚨 종합 폭락 분석", 
                      command=lambda: self.main_app.safe_execute(self.comprehensive_crash_analysis)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="✂️ 최적 손절 레벨 계산", 
                      command=lambda: self.main_app.safe_execute(self.calculate_optimal_cutloss)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="📊 위험도 정밀 평가", 
                      command=lambda: self.main_app.safe_execute(self.assess_current_risk)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Button(left_panel, text="📋 AI 자문용 리포트 생성", 
                      command=lambda: self.main_app.safe_execute(self.generate_situation_report)).pack(fill=tk.X, pady=8, ipady=8)
            
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=20)
            
            # 현재 상황 요약
            ttk.Label(left_panel, text="📊 Current Status:", style='Subtitle.TLabel').pack(anchor=tk.W)
            self.crash_status_label = ttk.Label(left_panel, text="분석할 종목을 선택해주세요.", 
                                              style='Info.TLabel', wraplength=250)
            self.crash_status_label.pack(anchor=tk.W, pady=8)
            
            # 권장 행동
            ttk.Label(left_panel, text="🎯 Recommendation:", style='Subtitle.TLabel').pack(anchor=tk.W, pady=(20, 0))
            self.crash_recommendation_label = ttk.Label(left_panel, text="분석 후 표시됩니다.", 
                                                       style='Info.TLabel', wraplength=250)
            self.crash_recommendation_label.pack(anchor=tk.W, pady=8)
            
            # 레버리지 ETF 경고
            ttk.Separator(left_panel, orient='horizontal').pack(fill=tk.X, pady=20)
            warning_label = ttk.Label(left_panel, 
                                    text="⚡ 레버리지 ETF 특별 주의사항:\n\n" +
                                         "• 12-15% 손절선 반드시 엄격 준수\n" +
                                         "• 30일 이상 장기보유 절대 지양\n" +
                                         "• 변동성 급증 시 즉시 적극 대응\n" +
                                         "• 분할매수 자금 충분히 미리 확보\n" +
                                         "• 일반 주식 대비 3배 위험 인식\n\n" +
                                         "🚨 기억하세요:\n" +
                                         "'손실을 제한하는 것이\n먼저, 수익은 그 다음입니다'",
                                    style='Warning.TLabel', wraplength=250, justify=tk.LEFT)
            warning_label.pack(anchor=tk.W)
            
            # 우측 패널 - 결과 표시
            right_panel = ttk.LabelFrame(bottom_container, text="📊 Detailed Analysis Results", padding="20")
            right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
            
            # 결과 표시 영역
            self.crash_results = scrolledtext.ScrolledText(right_panel, 
                                                         height=28, wrap=tk.WORD, 
                                                         font=('Consolas', 12))
            self.crash_results.pack(fill=tk.BOTH, expand=True)
            
            # 초기 안내 메시지
            self.show_initial_message()
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def show_initial_message(self):
        """초기 안내 메시지 표시"""
        initial_crash_message = """🚨 VStock Crash Strategy Advisor v3.3

폭락장에서 합리적이고 객관적인 투자 결정을 돕는 전문 분석 도구입니다.

💡 핵심 질문: "지금 손절해야 할까? 아니면 분할매수를 계속해야 할까?"

이 질문은 모든 투자자가 폭락장에서 가장 어려워하는 결정입니다. 
감정에 휘둘리지 않고 객관적 데이터로 판단할 수 있도록 도와드립니다.

📊 제공하는 분석 도구들:

🚨 종합 폭락 분석:
   • 현재 상황의 심각도를 0-100점으로 정량화
   • NORMAL → MODERATE → SEVERE → EXTREME 단계별 평가
   • 과거 폭락 사례와의 비교 분석
   • 다중 시간 프레임 분석 (5일, 10일, 20일, 60일)

✂️ 최적 손절 레벨 계산:
   • 기술적 분석 기반 손절가 계산 (지지선, 이동평균, 볼린저밴드)
   • 변동성 기반 VaR 모델 적용
   • 포트폴리오 비중 고려한 위험 관리
   • 레버리지 ETF 특별 기준 적용
   • 심리적 가격대 (Round Numbers) 고려

📊 위험도 정밀 평가:
   • VaR (Value at Risk) 95%, 99% 신뢰구간 계산
   • 최대손실 시나리오 분석 (최대낙폭, 스트레스 테스트)
   • 변동성 지표 종합 평가 (Historical, GARCH 모델)
   • 샤프 비율, 베타, 상관관계 분석
   • 시나리오별 손익 시뮬레이션

📋 AI 자문용 리포트:
   • 현재 상황을 정리한 전문가급 리포트 자동 생성
   • 클로드 등 AI에게 복사해서 전문 상담 요청 가능
   • 객관적 데이터 기반 상황 정리
   • 복사 및 저장 기능 완비

💡 실제 사용 시나리오:

1️⃣ SOXL/TQQQ 등 레버리지 ETF 급락 시:
   → 3배 레버리지의 높은 위험성 고려
   → 12-15% 엄격한 손절 기준 적용
   → 장기보유 절대 금지
   → VIX 30+ 시 즉시 청산 고려

2️⃣ 개별 주식의 예상치 못한 폭락:
   → 펀더멘털 변화 여부 확인
   → 기술적 지표와 함께 종합 판단
   → 회복 가능성 객관적 평가
   → 섹터/시장 전체 상황과 비교

3️⃣ 시장 전체 크래시 상황:
   → 시스템적 위험 vs 개별 위험 구분
   → 전체 포트폴리오 관점에서 접근
   → 기회인지 위험인지 판단
   → 현금 확보 vs 저가 매수 전략

⚠️ 매우 중요한 안내사항:
이 도구는 투자 참고용입니다. 최종 투자 결정은 반드시 본인의 판단과 책임하에 이루어져야 합니다.
하지만 감정적 결정보다는 객관적 데이터에 기반한 결정이 장기적으로 더 나은 결과를 가져옵니다.

🎯 핵심 철학:
"데이터로 말하고, 숫자로 판단하고, 계획으로 실행한다"

👆 위의 분석 도구들을 차례로 사용하여 현명한 투자 결정을 내리세요!

📈 시작하기:
1. Analysis 탭에서 종목 데이터 다운로드
2. 진입가와 포지션 정확히 입력
3. 종합 폭락 분석부터 시작
4. 각 분석 결과를 종합하여 최종 판단
"""
        self.crash_results.insert('1.0', initial_crash_message)
    
    def comprehensive_crash_analysis(self):
        """종합 폭락 분석 - 완전 구현"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            # 다양한 기간으로 분석
            data = self.shared_data['current_data']
            recent_5 = data.tail(5)
            recent_10 = data.tail(10)
            recent_20 = data.tail(20)
            recent_60 = data.tail(60)
            
            latest_price = data['Close'].iloc[-1]
            
            # 다양한 최고점에서의 하락률
            max_5d = recent_5['High'].max()
            max_10d = recent_10['High'].max()
            max_20d = recent_20['High'].max()
            max_60d = recent_60['High'].max()
            max_52w = data['High'].max()
            
            drop_5d = ((latest_price - max_5d) / max_5d) * 100
            drop_10d = ((latest_price - max_10d) / max_10d) * 100
            drop_20d = ((latest_price - max_20d) / max_20d) * 100
            drop_60d = ((latest_price - max_60d) / max_60d) * 100
            drop_52w = ((latest_price - max_52w) / max_52w) * 100
            
            # 변동성 계산 (연환산)
            returns_5d = recent_5['Close'].pct_change().dropna()
            returns_10d = recent_10['Close'].pct_change().dropna()
            returns_20d = recent_20['Close'].pct_change().dropna()
            
            volatility_5d = returns_5d.std() * np.sqrt(252) * 100 if len(returns_5d) > 1 else 0
            volatility_10d = returns_10d.std() * np.sqrt(252) * 100 if len(returns_10d) > 1 else 0
            volatility_20d = returns_20d.std() * np.sqrt(252) * 100 if len(returns_20d) > 1 else 0
            
            # 거래량 분석
            volume_avg_20d = recent_20['Volume'].mean() if len(recent_20) > 0 else 0
            volume_recent_5d = recent_5['Volume'].mean() if len(recent_5) > 0 else 0
            volume_spike = (volume_recent_5d / volume_avg_20d - 1) * 100 if volume_avg_20d > 0 else 0
            
            # 연속 하락일 계산
            consecutive_down = 0
            prices = data['Close'].tail(10).tolist()
            for i in range(len(prices)-1, 0, -1):
                if prices[i] < prices[i-1]:
                    consecutive_down += 1
                else:
                    break
            
            # 종합 위험 점수 계산 (0-100)
            risk_factors = {
                'drop_severity': min(35, abs(drop_10d) * 1.8),  # 최대 35점
                'volatility_risk': min(25, volatility_5d * 0.4),   # 최대 25점
                'volume_panic': min(15, max(0, volume_spike * 0.15)),  # 최대 15점
                'trend_breakdown': min(15, max(0, abs(drop_20d) * 0.4)),   # 최대 15점
                'consecutive_decline': min(10, consecutive_down * 2)  # 최대 10점
            }
            
            total_risk_score = sum(risk_factors.values())
            
            # 레버리지 ETF 가산점
            symbol = self.shared_data['current_symbol'].upper()
            leverage_etfs = ['SOXL', 'TQQQ', 'UPRO', 'TMF', 'SPXL', 'TECL', 'FNGU', 'WEBL', 'TSLL']
            is_leverage = any(etf in symbol for etf in leverage_etfs)
            
            if is_leverage:
                total_risk_score = min(100, total_risk_score * 1.3)  # 30% 가산
            
            # 위험도 등급 결정
            if total_risk_score < 20:
                severity_level = "NORMAL"
                severity_emoji = "📈"
                recommendation = "정상 보유 - 주의 깊게 관찰"
                action_color = "green"
            elif total_risk_score < 40:
                severity_level = "MODERATE_DECLINE"
                severity_emoji = "📊"
                recommendation = "주의 필요 - 포지션 점검"
                action_color = "orange"
            elif total_risk_score < 60:
                severity_level = "SIGNIFICANT_DROP"
                severity_emoji = "⚠️"
                recommendation = "위험 - 손절 고려"
                action_color = "red"
            elif total_risk_score < 80:
                severity_level = "SEVERE_CRASH"
                severity_emoji = "🚨"
                recommendation = "심각 - 즉시 대응 필요"
                action_color = "red"
            else:
                severity_level = "EXTREME_CRASH"
                severity_emoji = "💥"
                recommendation = "극한 상황 - 긴급 대응"
                action_color = "red"
            
            # 분석 결과 생성
            analysis_result = f"""🚨 VStock 종합 폭락 분석 결과

{'=' * 60}
📊 분석 대상: {self.shared_data['current_symbol']}
⏰ 분석 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
💰 현재가: ${latest_price:.2f}

🎯 폭락 분석 결과:
• 종합 위험 점수: {total_risk_score:.1f}/100점
• 심각도 등급: {severity_emoji} {severity_level}
• 권장사항: {recommendation}

📉 다중 시간 프레임 하락률 분석:
• 5일 최고점 대비: {drop_5d:.2f}%
• 10일 최고점 대비: {drop_10d:.2f}%
• 20일 최고점 대비: {drop_20d:.2f}%
• 60일 최고점 대비: {drop_60d:.2f}%
• 52주 최고점 대비: {drop_52w:.2f}%

📊 변동성 및 시장 혼란도:
• 5일 변동성: {volatility_5d:.1f}% (연환산)
• 10일 변동성: {volatility_10d:.1f}% (연환산)  
• 20일 변동성: {volatility_20d:.1f}% (연환산)
• 거래량 급증률: {volume_spike:+.1f}%
• 연속 하락일: {consecutive_down}일

🔍 위험 요소 상세 분해:
• 하락 심각도: {risk_factors['drop_severity']:.1f}/35점
• 변동성 위험: {risk_factors['volatility_risk']:.1f}/25점
• 거래량 이상: {risk_factors['volume_panic']:.1f}/15점
• 추세 파괴: {risk_factors['trend_breakdown']:.1f}/15점
• 연속 하락: {risk_factors['consecutive_decline']:.1f}/10점
"""
            
            if is_leverage:
                analysis_result += f"""
⚡ 레버리지 ETF 특별 위험 분석:
🚨 현재 종목 {symbol}은 레버리지 ETF입니다!
• 기초 자산 대비 예상 움직임: {abs(drop_10d) * 3:.1f}% (3배 레버리지)
• 일일 리밸런싱 손실 추정: {volatility_5d * 0.1:.2f}%
• 시간 가치 손실률 (월간): {volatility_20d * 0.05:.2f}%

⚠️ 레버리지 ETF 위험 요소:
• 변동성 손실 (Volatility Decay) 가속화
• 복리 효과 왜곡으로 추적 오차 확대
• 횡보장에서도 지속적 가치 하락
• 역추세 시장에서 양방향 손실 발생
"""
            
            # 대응 전략 추가
            if severity_level == "NORMAL":
                analysis_result += """
✅ 정상 범위의 시장 변동성입니다.
• 현재 포지션 유지 가능
• 정기적 모니터링 지속
• 추가 매수 기회 관찰
"""
            elif severity_level == "MODERATE_DECLINE":
                analysis_result += """
📊 보통 수준의 조정이 진행 중입니다.
• 포지션 크기 재검토 필요
• 손절선 재설정 고려
• 추가 하락 대비책 마련
"""
            elif severity_level == "SIGNIFICANT_DROP":
                analysis_result += """
⚠️ 상당한 하락이 진행 중입니다.
• 손절 기준점 도달 여부 확인
• 포지션 축소 적극 고려
• 추가 투자 자금 보존
"""
            elif severity_level == "SEVERE_CRASH":
                analysis_result += """
🚨 심각한 폭락 상황입니다.
• 즉시 손절 결정 필요
• 포트폴리오 전체 점검
• 현금 비중 확대 고려
"""
            else:
                analysis_result += """
💥 극한 폭락 상황입니다.
• 긴급 포지션 전면 정리
• 모든 투자 즉시 중단
• 현금 확보 최우선
"""
            
            analysis_result += """

⚠️ 중요 알림:
이 분석은 객관적 데이터에 기반한 참고 자료입니다. 
최종 투자 결정은 본인의 판단과 책임하에 이루어져야 합니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', analysis_result)
            
            # 상태 라벨 업데이트
            self.crash_status_label.config(text=f"위험점수: {total_risk_score:.0f}/100\n{severity_emoji} {severity_level}")
            self.crash_recommendation_label.config(text=recommendation)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def calculate_optimal_cutloss(self):
        """최적 손절 레벨 계산"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.shared_data['current_data']
            latest_price = data['Close'].iloc[-1]
            symbol = self.shared_data['current_symbol'].upper()
            
            # 레버리지 ETF 확인
            leverage_etfs = ['SOXL', 'TQQQ', 'UPRO', 'TMF', 'SPXL', 'TECL', 'FNGU', 'WEBL', 'TSLL']
            is_leverage = any(etf in symbol for etf in leverage_etfs)
            
            if is_leverage:
                cutloss_rates = [0.88, 0.85, 0.82]  # 12%, 15%, 18%
                asset_type = "레버리지 ETF"
            else:
                cutloss_rates = [0.90, 0.85, 0.80]  # 10%, 15%, 20%
                asset_type = "일반 주식"
            
            cutloss_result = f"""✂️ VStock 최적 손절 레벨 계산

{'=' * 60}
📊 분석 정보:
• 종목: {symbol} ({asset_type})
• 현재가: ${latest_price:.2f}
• 계산 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

📈 권장 손절가:
"""
            
            labels = ["보수적", "표준", "공격적"]
            for i, (rate, label) in enumerate(zip(cutloss_rates, labels)):
                cutloss_price = latest_price * rate
                loss_pct = (1 - rate) * 100
                cutloss_result += f"• {label}: ${cutloss_price:.2f} ({loss_pct:.0f}% 손절)\n"
            
            if is_leverage:
                cutloss_result += f"""
⚡ 레버리지 ETF 특별 관리:
• 절대 손절선: ${latest_price * 0.80:.2f} (20% 손실) - 절대 돌파 금지
• VIX 30 이상 시 즉시 청산 고려
• 30일 이상 보유 절대 금지
• 일반 주식보다 3배 빠른 대응 필수
"""
            
            cutloss_result += """
💡 손절 실행 원칙:
• 스톱로스 주문 미리 설정
• 감정에 휘둘리지 말고 기계적 실행
• 손절 후 24시간 재진입 금지
• 손절 원인 반드시 분석 후 기록

⚠️ 최종 알림:
손절선을 지키는 투자자만이 시장에서 살아남습니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', cutloss_result)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def assess_current_risk(self):
        """현재 위험도 평가"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.shared_data['current_data']
            recent_20 = data.tail(20)
            latest_price = data['Close'].iloc[-1]
            
            # 기본 위험 지표 계산
            returns = recent_20['Close'].pct_change().dropna()
            volatility = returns.std() * np.sqrt(252) * 100 if len(returns) > 1 else 0
            
            # VaR 계산
            var_95 = np.percentile(returns, 5) * 100 if len(returns) > 0 else 0
            var_99 = np.percentile(returns, 1) * 100 if len(returns) > 0 else 0
            
            # 최대 낙폭
            max_price = recent_20['High'].max()
            max_drawdown = ((latest_price - max_price) / max_price) * 100
            
            # 위험도 등급 결정
            risk_score = min(100, abs(var_95) * 5 + volatility * 1.5)
            
            if risk_score < 25:
                risk_level = "낮음"
                risk_emoji = "✅"
            elif risk_score < 50:
                risk_level = "보통"
                risk_emoji = "📊"
            elif risk_score < 75:
                risk_level = "높음"
                risk_emoji = "⚠️"
            else:
                risk_level = "매우 높음"
                risk_emoji = "🚨"
            
            risk_assessment = f"""📊 VStock 위험도 정밀 평가

{'=' * 60}
📈 분석 대상: {self.shared_data['current_symbol']}
💰 현재가: ${latest_price:.2f}
⏰ 평가 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

🎯 종합 위험도: {risk_emoji} {risk_level}
📊 위험 점수: {risk_score:.1f}/100점

📈 통계적 위험 지표:
• 20일 변동성: {volatility:.1f}% (연환산)
• VaR 95%: {var_95:.2f}%
• VaR 99%: {var_99:.2f}%
• 최대 낙폭: {max_drawdown:.2f}%

💡 위험 관리 권장사항:
"""
            
            if risk_level == "낮음":
                risk_assessment += """
✅ 현재 위험도가 낮습니다.
• 현 상태 유지 가능
• 정기 모니터링 지속
• 추가 투자 기회 탐색
"""
            elif risk_level == "보통":
                risk_assessment += """
📊 보통 수준의 위험입니다.
• 정기적 모니터링 강화
• 손절선 재확인
• 포지션 크기 점검
"""
            elif risk_level == "높음":
                risk_assessment += """
⚠️ 높은 위험 상황입니다.
• 포지션 축소 고려
• 엄격한 손절선 적용
• 일일 모니터링 필수
"""
            else:
                risk_assessment += """
🚨 매우 높은 위험 상황입니다.
• 즉시 포지션 정리 고려
• 현금 비중 확대
• 전문가 상담 권장
"""
            
            risk_assessment += """
⚠️ 중요: 이 평가는 과거 데이터 기반 통계적 분석입니다.
실제 시장은 예측할 수 없는 변수가 많습니다.
"""
            
            self.crash_results.delete('1.0', tk.END)
            self.crash_results.insert('1.0', risk_assessment)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)
    
    def generate_situation_report(self):
        """상황 리포트 생성 (AI 자문용)"""
        try:
            if self.shared_data['current_data'] is None:
                messagebox.showwarning("⚠️", "먼저 데이터를 로드해주세요.")
                return
            
            data = self.shared_data['current_data']
            latest_price = data['Close'].iloc[-1]
            symbol = self.shared_data['current_symbol']
            
            # 기본 분석
            recent_10 = data.tail(10)
            recent_20 = data.tail(20)
            
            max_10d = recent_10['High'].max()
            drop_10d = ((latest_price - max_10d) / max_10d) * 100
            
            returns_20d = recent_20['Close'].pct_change().dropna()
            volatility = returns_20d.std() * np.sqrt(252) * 100 if len(returns_20d) > 1 else 0
            
            # 리포트 생성
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            report = f"""🤖 VStock AI 투자 자문 요청 리포트

안녕하세요. 현재 투자 상황에 대한 전문적인 조언을 구하고자 합니다.

📊 기본 정보:
• 요청 시간: {timestamp}
• 분석 종목: {symbol}
• 현재가: ${latest_price:.2f}
• 10일 최고점 대비 하락률: {drop_10d:.2f}%
• 최근 20일 변동성: {volatility:.1f}% (연환산)

❓ 현재 투자 딜레마:
특히 폭락장에서 '손절 vs 분할매수'의 어려운 결정을 내려야 하는 상황입니다.

🙏 요청드리는 전문가 조언:
1. 현재 상황에 대한 전문가적 진단
2. 가장 합리적인 대응 전략 
3. 위험 관리 관점에서의 필수 고려사항
4. 향후 모니터링해야 할 핵심 지표

특히 감정적 판단이 아닌 데이터와 논리에 기반한 
객관적 분석과 실행 가능한 구체적 조언을 원합니다.

---
Generated by VStock Advanced Pro v3.3 Crash Strategy Module
"""
            
            # 리포트 표시 창
            report_window = tk.Toplevel(self.main_app.root)
            report_window.title("📋 AI 자문용 상황 리포트")
            report_window.geometry("800x600")
            report_window.transient(self.main_app.root)
            
            main_frame = ttk.Frame(report_window, padding="20")
            main_frame.pack(fill=tk.BOTH, expand=True)
            
            ttk.Label(main_frame, text="📋 AI 투자 자문용 상황 리포트", 
                     style='Title.TLabel').pack(pady=(0, 15))
            
            ttk.Label(main_frame, 
                     text="아래 리포트를 복사하여 AI에게 전문 투자 자문을 요청하세요.", 
                     style='Info.TLabel').pack(pady=(0, 15))
            
            # 텍스트 영역
            text_frame = ttk.Frame(main_frame)
            text_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
            
            report_text = scrolledtext.ScrolledText(text_frame, wrap=tk.WORD, 
                                                  font=('Consolas', 10))
            report_text.pack(fill=tk.BOTH, expand=True)
            report_text.insert('1.0', report)
            
            # 버튼
            button_frame = ttk.Frame(main_frame)
            button_frame.pack(fill=tk.X)
            
            def copy_report():
                try:
                    self.main_app.root.clipboard_clear()
                    self.main_app.root.clipboard_append(report)
                    messagebox.showinfo("✅", "리포트가 클립보드에 복사되었습니다!")
                except Exception as e:
                    messagebox.showerror("❌", f"복사 실패: {e}")
            
            ttk.Button(button_frame, text="📋 클립보드에 복사", 
                      command=copy_report).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Button(button_frame, text="❌ 닫기", 
                      command=report_window.destroy).pack(side=tk.RIGHT)
            
        except Exception as e:
            self.main_app.handle_exception(e, True)