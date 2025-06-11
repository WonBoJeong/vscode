import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

class KRXStockDownloader:
    def __init__(self, download_folder=None, chromedriver_path=None):
        """
        KRX 주식 데이터 다운로더 초기화
        
        Args:
            download_folder: 다운로드 폴더 경로 (기본값: 현재 디렉토리의 downloads 폴더)
            chromedriver_path: 크롬드라이버 경로 (기본값: 시스템 PATH에서 찾음)
        """
        self.download_folder = download_folder or os.path.join(os.getcwd(), "downloads")
        self.chromedriver_path = chromedriver_path
        
        # 다운로드 폴더 생성
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
            
        self.driver = None
        
    def setup_driver(self):
        """Chrome 드라이버 설정"""
        chrome_options = Options()
        chrome_options.add_experimental_option("prefs", {
            "download.default_directory": self.download_folder,
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
            "safebrowsing.enabled": True
        })
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        if self.chromedriver_path:
            service = Service(self.chromedriver_path)
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
        else:
            self.driver = webdriver.Chrome(options=chrome_options)
    
    def download_stock_data(self, date_list, target_stock_codes=None):
        """
        주식 데이터 다운로드
        
        Args:
            date_list: 다운로드할 날짜 리스트 (예: ["20241201", "20241202"])
            target_stock_codes: 특정 종목 코드 리스트 (예: ["005930", "000660"])
                               None이면 전종목 다운로드
        
        Returns:
            dict: {날짜: DataFrame} 형태의 딕셔너리
        """
        if not self.driver:
            self.setup_driver()
        
        url = "http://data.krx.co.kr/contents/MDC/MDI/mdiLoader/index.cmd?menuId=MDC0201020101"
        self.driver.get(url)
        
        # 페이지 로딩 대기
        WebDriverWait(self.driver, 30).until(
            EC.invisibility_of_element_located((By.CLASS_NAME, 'loading-bar-overlay'))
        )
        
        date_element = self.driver.find_element(By.ID, "trdDd")
        search_button = self.driver.find_element(By.ID, "jsSearchButton")
        
        before_file_list = set(os.listdir(self.download_folder))
        result_data = {}
        
        for date in date_list:
            print(f"처리 중: {date}")
            
            # 날짜 입력
            date_element.click()
            self.driver.execute_script("arguments[0].value = '{}'".format(date), date_element)
            search_button.click()
            
            # 다운로드 버튼 클릭
            download_button = WebDriverWait(self.driver, 30).until(
                lambda x: x.find_element(By.CLASS_NAME, "CI-MDI-UNIT-DOWNLOAD")
            )
            download_button.click()
            
            # CSV 다운로드 버튼 클릭
            csv_button = WebDriverWait(self.driver, 30).until(
                lambda x: x.find_element(By.XPATH, 
                    '/html/body/div[2]/section[2]/section/section/div/div/form/div[2]/div[2]/div[2]/div/div[2]/a')
            )
            csv_button.click()
            
            # 다운로드 완료 대기
            new_file = self._wait_for_download(before_file_list)
            
            if new_file:
                # 파일 읽기 및 처리
                file_path = os.path.join(self.download_folder, new_file)
                df = pd.read_csv(file_path, encoding='cp949')
                
                # 특정 종목만 필터링
                if target_stock_codes:
                    df = df[df['종목코드'].astype(str).str.zfill(6).isin(target_stock_codes)]
                
                result_data[date] = df
                
                # 파일명 변경
                new_file_path = os.path.join(self.download_folder, f"{date}.csv")
                os.rename(file_path, new_file_path)
                
                before_file_list = set(os.listdir(self.download_folder))
                
                print(f"{date} 데이터 다운로드 완료: {len(df)}개 종목")
            
            time.sleep(1)  # 서버 부하 방지
        
        return result_data
    
    def _wait_for_download(self, before_file_list, timeout=60):
        """다운로드 완료 대기"""
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            current_files = set(os.listdir(self.download_folder))
            new_files = current_files - before_file_list
            
            for file in new_files:
                if '.csv' in file and not file.endswith('.tmp'):
                    return file
            
            time.sleep(0.5)
        
        return None
    
    def get_specific_stock_info(self, stock_codes, date_list):
        """
        특정 종목들의 정보만 가져오기
        
        Args:
            stock_codes: 종목 코드 리스트 (예: ["005930", "000660"])
            date_list: 날짜 리스트 (예: ["20241201", "20241202"])
        
        Returns:
            DataFrame: 필터링된 주식 데이터
        """
        # 종목 코드를 6자리로 맞추기
        formatted_codes = [str(code).zfill(6) for code in stock_codes]
        
        print(f"대상 종목: {formatted_codes}")
        print(f"대상 날짜: {date_list}")
        
        # 데이터 다운로드
        stock_data = self.download_stock_data(date_list, formatted_codes)
        
        # 모든 날짜의 데이터를 하나로 합치기
        all_data = []
        for date, df in stock_data.items():
            df['날짜'] = date
            all_data.append(df)
        
        if all_data:
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # 컬럼 순서 조정
            columns = ['날짜', '종목코드', '종목명'] + [col for col in combined_df.columns 
                                                    if col not in ['날짜', '종목코드', '종목명']]
            combined_df = combined_df[columns]
            
            return combined_df
        else:
            return pd.DataFrame()
    
    def save_to_file(self, data, filename):
        """데이터를 파일로 저장"""
        if isinstance(data, dict):
            # 날짜별로 별도 파일 저장
            for date, df in data.items():
                file_path = f"{filename}_{date}.csv"
                df.to_csv(file_path, encoding='utf-8-sig', index=False)
                print(f"저장 완료: {file_path}")
        else:
            # 단일 DataFrame 저장
            file_path = f"{filename}.csv"
            data.to_csv(file_path, encoding='utf-8-sig', index=False)
            print(f"저장 완료: {file_path}")
    
    def close(self):
        """드라이버 종료"""
        if self.driver:
            self.driver.quit()

def main():
    """메인 실행 함수"""
    # 사용 예시
    downloader = KRXStockDownloader()
    
    try:
        # 특정 종목 설정 (삼성전자, SK하이닉스, NAVER, 카카오)
        target_stocks = ["005930", "000660", "035420", "035720"]
        
        # 날짜 설정 (최근 영업일로 수정하세요)
        dates = ["20241201", "20241202", "20241203"]
        
        print("=== 특정 종목 주식 데이터 다운로드 시작 ===")
        
        # 특정 종목 데이터 가져오기
        result_df = downloader.get_specific_stock_info(target_stocks, dates)
        
        if not result_df.empty:
            print(f"\n=== 다운로드 결과 ===")
            print(f"총 {len(result_df)}개 레코드")
            print(f"종목별 분포:")
            print(result_df['종목명'].value_counts())
            
            print(f"\n=== 샘플 데이터 ===")
            print(result_df.head(10))
            
            # 파일 저장
            downloader.save_to_file(result_df, "specific_stocks_data")
            
            # Excel 파일로도 저장 (선택사항)
            try:
                result_df.to_excel("specific_stocks_data.xlsx", index=False)
                print("Excel 파일 저장 완료: specific_stocks_data.xlsx")
            except:
                print("Excel 저장 실패 (openpyxl 라이브러리가 필요합니다)")
        else:
            print("데이터를 가져오지 못했습니다.")
    
    except Exception as e:
        print(f"오류 발생: {e}")
    
    finally:
        downloader.close()

if __name__ == "__main__":
    main()
