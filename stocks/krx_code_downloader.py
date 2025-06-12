import requests
import pandas as pd
from io import BytesIO

def get_krx_code():
    """
    한국거래소(KRX)에서 주식 종목 정보를 다운로드하는 함수
    """
    # OTP 생성을 위한 URL과 파라미터
    gen_url = 'http://data.krx.co.kr/comm/fileDn/GenerateOTP/generate.cmd'
    gen_parms = {
        'mktId': 'ALL',
        'share': '1',
        'csvxls_isNo': 'false',
        'name': 'fileDown',
        'url': 'dbms/MDC/STAT/standard/MDCSTAT01901'
    }
    
    # 헤더 설정
    headers = {
        'Referer': 'http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    }
    
    try:
        # OTP 생성 요청
        print("OTP 생성 중...")
        r = requests.get(url=gen_url, params=gen_parms, headers=headers)
        
        # CSV 다운로드
        down_url = 'http://data.krx.co.kr/comm/fileDn/download_csv/download.cmd'
        data = {
            'code': r.content
        }
        
        print("주식 종목 데이터 다운로드 중...")
        r = requests.post(url=down_url, data=data, headers=headers)
        
        # CSV 파싱
        stock_code = pd.read_csv(BytesIO(r.content), encoding='cp949')
        
        # 필요한 컬럼만 선택 및 컬럼명 변경
        stock_code = stock_code[['한글 종목약명', '단축코드', '시장구분', '액면가', '상장주식수']]
        stock_code = stock_code.rename(columns={
            '시장구분': 'market', 
            '한글 종목약명': 'name', 
            '단축코드': 'code', 
            '액면가': 'par_value', 
            '상장주식수': 'total_shrs'
        })
        
        print(f"총 {len(stock_code)}개 종목 데이터 다운로드 완료!")
        return stock_code
        
    except Exception as e:
        print(f"오류 발생: {e}")
        return None

def save_stock_data(stock_data, filename='krx_stock_list.csv'):
    """
    주식 데이터를 CSV 파일로 저장하는 함수
    """
    if stock_data is not None:
        stock_data.to_csv(filename, encoding='utf-8-sig', index=False)
        print(f"파일 저장 완료: {filename}")
    else:
        print("저장할 데이터가 없습니다.")

def display_sample_data(stock_data, n=10):
    """
    샘플 데이터를 출력하는 함수
    """
    if stock_data is not None:
        print(f"\n=== 상위 {n}개 종목 샘플 ===")
        print(stock_data.head(n))
        
        print(f"\n=== 데이터 요약 정보 ===")
        print(f"총 종목 수: {len(stock_data)}")
        print(f"시장별 분포:")
        print(stock_data['market'].value_counts())

if __name__ == "__main__":
    # 주식 종목 데이터 다운로드
    stock_data = get_krx_code()
    
    if stock_data is not None:
        # 샘플 데이터 출력
        display_sample_data(stock_data)
        
        # CSV 파일로 저장
        save_stock_data(stock_data)
        
        # Excel 파일로도 저장 (선택사항)
        try:
            stock_data.to_excel('krx_stock_list.xlsx', index=False)
            print("Excel 파일 저장 완료: krx_stock_list.xlsx")
        except:
            print("Excel 저장 실패 (openpyxl 라이브러리가 필요합니다)")
    else:
        print("데이터 다운로드에 실패했습니다.")
