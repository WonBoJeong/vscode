"""
yfinance를 이용한 한국 주식 데이터 다운로드 스크립트
Yahoo Finance에서 한국 주식 데이터를 수집하여 CSV 파일로 저장
"""

import os
import sys
import time
import warnings
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple

import pandas as pd
import numpy as np
import yfinance as yf
from concurrent.futures import ThreadPoolExecutor, as_completed
import matplotlib.pyplot as plt
import seaborn as sns

# 경고 메시지 숨기기
warnings.filterwarnings('ignore')

class KoreanStockDownloader:
    """한국 주식 데이터 다운로드 클래스"""
    
    def __init__(self, data_dir: str = "data"):
        """
        초기화
        
        Args:
            data_dir (str): 데이터 저장 디렉토리
        """
        self.data_dir = data_dir
        self.date_key = datetime.now().strftime("%y%m%d")
        
        # 데이터 디렉토리 생성
        os.makedirs(self.data_dir, exist_ok=True)
        
        # 한국 주요 종목 정보
        self.stock_info = {
            "005930.KS": "삼성전자",
            "000660.KS": "SK하이닉스", 
            "035420.KS": "NAVER",
            "035720.KS": "카카오",
            "000270.KS": "기아",
            "068270.KS": "셀트리온",
            "207940.KS": "삼성바이오로직스",
            "003670.KS": "포스코홀딩스",
            "086520.KS": "에코프로",
            "373220.KS": "LG에너지솔루션",
            "096770.KS": "SK이노베이션",
            "051910.KS": "LG화학",
            "028260.KS": "삼성물산",
            "105560.KS": "KB금융",
            "055550.KS": "신한지주",
            "012330.KS": "현대모비스",
            "066570.KS": "LG전자",
            "323410.KS": "카카오뱅크",
            "003550.KS": "LG",
            "017670.KS": "SK텔레콤"
        }
    
    def get_korea_stock_symbol(self, code: str) -> str:
        """
        한국 종목 코드를 Yahoo Finance 심볼로 변환
        
        Args:
            code (str): 6자리 종목 코드
            
        Returns:
            str: Yahoo Finance 심볼 (예: 005930.KS)
        """
        if not code.endswith('.KS') and not code.endswith('.KQ'):
            # 6자리로 맞추고 .KS 추가 (KOSPI 기본)
            formatted_code = str(code).zfill(6)
            return f"{formatted_code}.KS"
        return code
    
    def download_single_stock(self, 
                            code: str, 
                            period: str = "3y", 
                            start_date: Optional[str] = None,
                            end_date: Optional[str] = None,
                            save_file: bool = True) -> Optional[pd.DataFrame]:
        """
        개별 종목 데이터 다운로드
        
        Args:
            code (str): 종목 코드
            period (str): 기간 ("1y", "2y", "3y", "5y", "10y", "max")
            start_date (str): 시작일 (YYYY-MM-DD)
            end_date (str): 종료일 (YYYY-MM-DD)
            save_file (bool): 파일 저장 여부
            
        Returns:
            pd.DataFrame: 주식 데이터
        """
        symbol = self.get_korea_stock_symbol(code)
        stock_name = self.stock_info.get(symbol, f"종목_{code}")
        
        print(f"다운로드 중: {stock_name} ({symbol})")
        
        try:
            # yfinance 티커 생성
            ticker = yf.Ticker(symbol)
            
            # 데이터 다운로드
            if start_date and end_date:
                data = ticker.history(start=start_date, end=end_date)
            else:
                data = ticker.history(period=period)
            
            if data.empty:
                print(f"경고: {symbol}의 데이터가 없습니다.")
                return None
            
            # 데이터 전처리
            data.reset_index(inplace=True)
            data['Stock_Code'] = code
            data['Symbol'] = symbol
            data['Stock_Name'] = stock_name
            
            # 수익률 및 지표 계산
            data['Return_Rate'] = data['Close'].pct_change() * 100
            data['Volatility'] = data['Return_Rate'].abs()
            data['Trading_Value'] = data['Close'] * data['Volume']
            data['MA_5'] = data['Close'].rolling(window=5).mean()
            data['MA_20'] = data['Close'].rolling(window=20).mean()
            data['MA_60'] = data['Close'].rolling(window=60).mean()
            
            # 볼린저 밴드
            data['BB_Middle'] = data['Close'].rolling(window=20).mean()
            bb_std = data['Close'].rolling(window=20).std()
            data['BB_Upper'] = data['BB_Middle'] + (bb_std * 2)
            data['BB_Lower'] = data['BB_Middle'] - (bb_std * 2)
            
            # RSI 계산
            data['RSI'] = self.calculate_rsi(data['Close'])
            
            # 컬럼 순서 정리
            columns_order = ['Date', 'Stock_Code', 'Symbol', 'Stock_Name', 'Open', 'High', 'Low', 'Close', 
                           'Volume', 'Trading_Value', 'Return_Rate', 'Volatility', 'MA_5', 'MA_20', 'MA_60',
                           'BB_Upper', 'BB_Middle', 'BB_Lower', 'RSI']
            
            data = data[columns_order]
            
            # 파일 저장
            if save_file:
                filename = os.path.join(self.data_dir, f"{code}_{self.date_key}.csv")
                data.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"저장 완료: {filename} ({len(data)}행)")
            
            return data
            
        except Exception as e:
            print(f"오류 발생 ({symbol}): {str(e)}")
            return None
    
    def calculate_rsi(self, prices: pd.Series, window: int = 14) -> pd.Series:
        """
        RSI (Relative Strength Index) 계산
        
        Args:
            prices (pd.Series): 가격 데이터
            window (int): 계산 윈도우
            
        Returns:
            pd.Series: RSI 값
        """
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def download_multiple_stocks(self, 
                                codes: List[str], 
                                period: str = "3y",
                                start_date: Optional[str] = None,
                                end_date: Optional[str] = None,
                                max_workers: int = 5) -> Dict[str, pd.DataFrame]:
        """
        여러 종목 데이터 일괄 다운로드 (멀티스레딩)
        
        Args:
            codes (List[str]): 종목 코드 리스트
            period (str): 기간
            start_date (str): 시작일
            end_date (str): 종료일
            max_workers (int): 최대 워커 수
            
        Returns:
            Dict[str, pd.DataFrame]: 종목별 데이터 딕셔너리
        """
        print("=== 한국 주식 데이터 다운로드 시작 ===")
        print(f"대상 종목: {len(codes)}개")
        print(f"기간: {period if not start_date else f'{start_date} ~ {end_date}'}")
        
        all_data = {}
        success_count = 0
        failed_codes = []
        
        # 순차 다운로드 (API 제한 고려)
        for i, code in enumerate(codes, 1):
            print(f"\n[{i}/{len(codes)}] ", end="")
            
            data = self.download_single_stock(
                code, period=period, 
                start_date=start_date, 
                end_date=end_date
            )
            
            if data is not None:
                all_data[code] = data
                success_count += 1
            else:
                failed_codes.append(code)
            
            # API 제한 방지를 위한 대기
            time.sleep(1)
        
        # 결과 요약
        print(f"\n=== 다운로드 완료 ===")
        print(f"성공: {success_count}개 종목")
        print(f"실패: {len(failed_codes)}개 종목")
        
        if failed_codes:
            print(f"실패한 종목: {', '.join(failed_codes)}")
        
        return all_data
    
    def create_combined_dataset(self, all_data: Dict[str, pd.DataFrame]) -> Optional[pd.DataFrame]:
        """
        통합 데이터셋 생성
        
        Args:
            all_data (Dict[str, pd.DataFrame]): 종목별 데이터
            
        Returns:
            pd.DataFrame: 통합 데이터
        """
        if not all_data:
            print("결합할 데이터가 없습니다.")
            return None
        
        print("데이터를 통합하는 중...")
        
        # 모든 데이터를 하나로 결합
        combined_data = pd.concat(all_data.values(), ignore_index=True)
        
        # 날짜 컬럼 정리
        combined_data['Date'] = pd.to_datetime(combined_data['Date'])
        combined_data = combined_data.sort_values(['Date', 'Stock_Code'])
        
        # 통합 파일 저장
        combined_filename = os.path.join(self.data_dir, f"combined_stocks_{self.date_key}.csv")
        combined_data.to_csv(combined_filename, index=False, encoding='utf-8-sig')
        
        print(f"통합 파일 저장 완료: {combined_filename}")
        print(f"총 데이터: {len(combined_data)}행")
        
        return combined_data
    
    def analyze_stocks(self, combined_data: pd.DataFrame) -> pd.DataFrame:
        """
        주식 데이터 기본 분석
        
        Args:
            combined_data (pd.DataFrame): 통합 데이터
            
        Returns:
            pd.DataFrame: 분석 결과
        """
        if combined_data is None or combined_data.empty:
            print("분석할 데이터가 없습니다.")
            return pd.DataFrame()
        
        print("\n=== 기본 통계 분석 ===")
        
        # 종목별 통계 계산
        summary_stats = combined_data.groupby(['Stock_Code', 'Stock_Name']).agg({
            'Date': ['min', 'max', 'count'],
            'Close': ['first', 'last', 'min', 'max', 'mean'],
            'Volume': 'mean',
            'Trading_Value': 'mean',
            'Return_Rate': ['mean', 'std'],
            'Volatility': 'mean'
        }).round(2)
        
        # 컬럼명 정리
        summary_stats.columns = ['시작일', '종료일', '데이터수', '시작가', '종료가', '최저가', 
                               '최고가', '평균가', '평균거래량', '평균거래대금', '평균수익률', 
                               '수익률표준편차', '평균변동성']
        
        # 총 수익률 계산
        summary_stats['총수익률(%)'] = ((summary_stats['종료가'] - summary_stats['시작가']) / 
                                      summary_stats['시작가'] * 100).round(2)
        
        summary_stats.reset_index(inplace=True)
        
        # 결과 출력
        print(summary_stats.to_string(index=False))
        
        # 수익률 상위 종목
        top_performers = summary_stats.nlargest(5, '총수익률(%)')
        print(f"\n=== 수익률 상위 5개 종목 ===")
        print(top_performers[['Stock_Name', '총수익률(%)']].to_string(index=False))
        
        # 분석 결과 저장
        stats_filename = os.path.join(self.data_dir, f"summary_stats_{self.date_key}.csv")
        summary_stats.to_csv(stats_filename, index=False, encoding='utf-8-sig')
        print(f"\n분석 결과 저장: {stats_filename}")
        
        return summary_stats
    
    def create_visualization(self, combined_data: pd.DataFrame, top_stocks: int = 5):
        """
        주식 데이터 시각화
        
        Args:
            combined_data (pd.DataFrame): 통합 데이터
            top_stocks (int): 상위 몇 개 종목을 시각화할지
        """
        if combined_data is None or combined_data.empty:
            print("시각화할 데이터가 없습니다.")
            return
        
        print("차트를 생성하는 중...")
        
        # 한글 폰트 설정
        plt.rcParams['font.family'] = ['Malgun Gothic', 'DejaVu Sans']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 수익률 상위 종목 선택
        latest_data = combined_data.groupby('Stock_Code').last()
        first_data = combined_data.groupby('Stock_Code').first()
        returns = ((latest_data['Close'] - first_data['Close']) / first_data['Close'] * 100)
        top_stock_codes = returns.nlargest(top_stocks).index.tolist()
        
        # 상위 종목 데이터 필터링
        top_data = combined_data[combined_data['Stock_Code'].isin(top_stock_codes)]
        
        # 시각화
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'한국 주식 분석 대시보드 (상위 {top_stocks}개 종목)', fontsize=16, y=0.98)
        
        # 1. 주가 추이
        ax1 = axes[0, 0]
        for code in top_stock_codes:
            stock_data = top_data[top_data['Stock_Code'] == code]
            stock_name = stock_data['Stock_Name'].iloc[0]
            ax1.plot(stock_data['Date'], stock_data['Close'], label=stock_name, linewidth=2)
        ax1.set_title('주가 추이')
        ax1.set_xlabel('날짜')
        ax1.set_ylabel('종가 (원)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. 거래량 추이
        ax2 = axes[0, 1]
        for code in top_stock_codes:
            stock_data = top_data[top_data['Stock_Code'] == code]
            stock_name = stock_data['Stock_Name'].iloc[0]
            ax2.plot(stock_data['Date'], stock_data['Volume'], label=stock_name, alpha=0.7)
        ax2.set_title('거래량 추이')
        ax2.set_xlabel('날짜')
        ax2.set_ylabel('거래량')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 3. 총 수익률 비교
        ax3 = axes[1, 0]
        returns_data = []
        names = []
        for code in top_stock_codes:
            stock_data = top_data[top_data['Stock_Code'] == code]
            if not stock_data.empty:
                total_return = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / 
                              stock_data['Close'].iloc[0] * 100)
                returns_data.append(total_return)
                names.append(stock_data['Stock_Name'].iloc[0])
        
        bars = ax3.bar(names, returns_data, color=['green' if x > 0 else 'red' for x in returns_data])
        ax3.set_title('총 수익률 비교 (%)')
        ax3.set_ylabel('수익률 (%)')
        ax3.tick_params(axis='x', rotation=45)
        
        # 막대 위에 수치 표시
        for bar, value in zip(bars, returns_data):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height + (1 if height > 0 else -3),
                    f'{value:.1f}%', ha='center', va='bottom' if height > 0 else 'top')
        
        # 4. 변동성 vs 수익률 산점도
        ax4 = axes[1, 1]
        for code in top_stock_codes:
            stock_data = top_data[top_data['Stock_Code'] == code]
            if not stock_data.empty:
                avg_volatility = stock_data['Volatility'].mean()
                total_return = ((stock_data['Close'].iloc[-1] - stock_data['Close'].iloc[0]) / 
                              stock_data['Close'].iloc[0] * 100)
                stock_name = stock_data['Stock_Name'].iloc[0]
                ax4.scatter(avg_volatility, total_return, s=100, alpha=0.7, label=stock_name)
        
        ax4.set_title('변동성 vs 수익률')
        ax4.set_xlabel('평균 변동성 (%)')
        ax4.set_ylabel('총 수익률 (%)')
        ax4.legend()
        ax4.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # 차트 저장
        chart_filename = os.path.join(self.data_dir, f"stock_analysis_chart_{self.date_key}.png")
        plt.savefig(chart_filename, dpi=300, bbox_inches='tight')
        print(f"차트 저장 완료: {chart_filename}")
        
        plt.show()

def main():
    """메인 실행 함수"""
    
    print("=== yfinance 한국 주식 데이터 다운로더 ===\n")
    
    # 다운로더 초기화
    downloader = KoreanStockDownloader()
    
    # 대상 종목 설정 (기본 종목들)
    default_stocks = [
        "005930",  # 삼성전자
        "000660",  # SK하이닉스
        "035420",  # NAVER
        "035720",  # 카카오
        "000270",  # 기아
        "068270",  # 셀트리온
        "207940",  # 삼성바이오로직스
        "003670",  # 포스코홀딩스
        "086520",  # 에코프로
        "373220"   # LG에너지솔루션
    ]
    
    # 사용자 입력 받기
    print("다운로드할 종목을 선택하세요:")
    print("1. 기본 종목 (10개 주요 종목)")
    print("2. 직접 입력")
    
    choice = input("선택 (1 또는 2): ").strip()
    
    if choice == "2":
        codes_input = input("종목 코드를 쉼표로 구분하여 입력하세요 (예: 005930,000660): ")
        stock_codes = [code.strip() for code in codes_input.split(",")]
    else:
        stock_codes = default_stocks
    
    # 기간 설정
    print("\n다운로드 기간을 선택하세요:")
    print("1. 최근 1년")
    print("2. 최근 3년 (기본)")
    print("3. 최근 5년")
    print("4. 직접 입력")
    
    period_choice = input("선택 (1-4): ").strip()
    
    start_date, end_date, period = None, None, "3y"
    
    if period_choice == "1":
        period = "1y"
    elif period_choice == "3":
        period = "5y"
    elif period_choice == "4":
        start_input = input("시작일을 입력하세요 (YYYY-MM-DD): ")
        end_input = input("종료일을 입력하세요 (YYYY-MM-DD): ")
        start_date, end_date = start_input, end_input
        period = None
    
    try:
        # 데이터 다운로드
        all_data = downloader.download_multiple_stocks(
            stock_codes, 
            period=period,
            start_date=start_date,
            end_date=end_date
        )
        
        if all_data:
            # 통합 데이터셋 생성
            combined_data = downloader.create_combined_dataset(all_data)
            
            # 분석 수행
            if combined_data is not None:
                summary_stats = downloader.analyze_stocks(combined_data)
                
                # 시각화
                create_chart = input("\n차트를 생성하시겠습니까? (y/n): ").strip().lower()
                if create_chart == 'y':
                    downloader.create_visualization(combined_data)
                
                print(f"\n=== 모든 작업 완료 ===")
                print(f"생성된 파일:")
                print(f"- 개별 종목 파일: {downloader.data_dir}/ 폴더 내")
                print(f"- 통합 데이터: combined_stocks_{downloader.date_key}.csv")
                print(f"- 요약 통계: summary_stats_{downloader.date_key}.csv")
                if create_chart == 'y':
                    print(f"- 분석 차트: stock_analysis_chart_{downloader.date_key}.png")
        
    except KeyboardInterrupt:
        print("\n\n작업이 사용자에 의해 중단되었습니다.")
    except Exception as e:
        print(f"\n오류 발생: {str(e)}")

if __name__ == "__main__":
    # 필요한 패키지 설치 확인
    try:
        import yfinance as yf
        import matplotlib.pyplot as plt
        import seaborn as sns
    except ImportError as e:
        print("필요한 패키지를 설치해주세요:")
        print("pip install yfinance pandas matplotlib seaborn")
        sys.exit(1)
    
    main()
