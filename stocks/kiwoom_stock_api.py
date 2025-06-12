import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QTextEdit, QLineEdit, QLabel
from PyQt5.QAxContainer import QAxWidget
from PyQt5.QtCore import QEventLoop, QTimer
import pandas as pd
import json
from datetime import datetime

class KiwoomAPI:
    def __init__(self):
        self.ocx = QAxWidget("KHOPENAPI.KHOpenAPICtrl.1")
        self.ocx.OnEventConnect.connect(self._event_connect)
        self.ocx.OnReceiveTrData.connect(self._receive_tr_data)
        self.ocx.OnReceiveRealData.connect(self._receive_real_data)
        
        self.login_event_loop = QEventLoop()
        self.tr_event_loop = QEventLoop()
        
        self.tr_data = {}
        self.real_data = {}
        
    def comm_connect(self):
        """키움증권 로그인"""
        self.ocx.dynamicCall("CommConnect()")
        self.login_event_loop.exec_()
        
    def _event_connect(self, err_code):
        """로그인 이벤트 처리"""
        if err_code == 0:
            print("로그인 성공")
        else:
            print(f"로그인 실패: {err_code}")
        self.login_event_loop.exit()
        
    def get_code_list_by_market(self, market):
        """시장별 종목코드 리스트 조회"""
        code_list = self.ocx.dynamicCall("GetCodeListByMarket(QString)", market)
        return code_list.split(';')[:-1]
        
    def get_master_code_name(self, code):
        """종목명 조회"""
        return self.ocx.dynamicCall("GetMasterCodeName(QString)", code)
        
    def set_input_value(self, id, value):
        """TR 입력값 설정"""
        self.ocx.dynamicCall("SetInputValue(QString, QString)", id, value)
        
    def comm_rq_data(self, rqname, trcode, next, screen_no):
        """TR 요청"""
        self.ocx.dynamicCall("CommRqData(QString, QString, int, QString)", 
                           rqname, trcode, next, screen_no)
        self.tr_event_loop.exec_()
        
    def _receive_tr_data(self, screen_no, rqname, trcode, record_name, next, unused1, unused2, unused3, unused4):
        """TR 데이터 수신"""
        if next == '2':
            self.remained_data = True
        else:
            self.remained_data = False
            
        if rqname == "주식기본정보요청":
            self._opt10001(rqname, trcode)
        elif rqname == "주식일봉차트조회요청":
            self._opt10081(rqname, trcode)
            
        try:
            self.tr_event_loop.exit()
        except:
            pass
            
    def _opt10001(self, rqname, trcode):
        """주식기본정보 데이터 처리"""
        data = {}
        data['종목명'] = self._get_comm_data(trcode, rqname, 0, "종목명")
        data['현재가'] = int(self._get_comm_data(trcode, rqname, 0, "현재가"))
        data['전일대비'] = int(self._get_comm_data(trcode, rqname, 0, "전일대비"))
        data['등락률'] = float(self._get_comm_data(trcode, rqname, 0, "등락률"))
        data['거래량'] = int(self._get_comm_data(trcode, rqname, 0, "거래량"))
        data['시가'] = int(self._get_comm_data(trcode, rqname, 0, "시가"))
        data['고가'] = int(self._get_comm_data(trcode, rqname, 0, "고가"))
        data['저가'] = int(self._get_comm_data(trcode, rqname, 0, "저가"))
        data['시가총액'] = int(self._get_comm_data(trcode, rqname, 0, "시가총액"))
        data['PER'] = float(self._get_comm_data(trcode, rqname, 0, "PER")) if self._get_comm_data(trcode, rqname, 0, "PER") else 0
        data['PBR'] = float(self._get_comm_data(trcode, rqname, 0, "PBR")) if self._get_comm_data(trcode, rqname, 0, "PBR") else 0
        
        self.tr_data = data
        
    def _opt10081(self, rqname, trcode):
        """주식일봉차트 데이터 처리"""
        data_cnt = self._get_repeat_cnt(trcode, rqname)
        
        for i in range(data_cnt):
            date = self._get_comm_data(trcode, rqname, i, "일자")
            open_price = int(self._get_comm_data(trcode, rqname, i, "시가"))
            high_price = int(self._get_comm_data(trcode, rqname, i, "고가"))
            low_price = int(self._get_comm_data(trcode, rqname, i, "저가"))
            close_price = int(self._get_comm_data(trcode, rqname, i, "현재가"))
            volume = int(self._get_comm_data(trcode, rqname, i, "거래량"))
            
            if 'chart_data' not in self.tr_data:
                self.tr_data['chart_data'] = []
                
            self.tr_data['chart_data'].append({
                '일자': date,
                '시가': open_price,
                '고가': high_price,
                '저가': low_price,
                '종가': close_price,
                '거래량': volume
            })
        
    def _get_comm_data(self, trcode, rqname, index, item_name):
        """통신 데이터 조회"""
        ret = self.ocx.dynamicCall("GetCommData(QString, QString, int, QString)", 
                                 trcode, rqname, index, item_name)
        return ret.strip()
        
    def _get_repeat_cnt(self, trcode, rqname):
        """반복 데이터 개수 조회"""
        ret = self.ocx.dynamicCall("GetRepeatCnt(QString, QString)", trcode, rqname)
        return ret
        
    def get_stock_info(self, code):
        """주식 기본정보 조회"""
        self.set_input_value("종목코드", code)
        self.comm_rq_data("주식기본정보요청", "opt10001", 0, "0101")
        return self.tr_data
        
    def get_stock_chart(self, code, date="", period=20):
        """주식 차트 데이터 조회"""
        self.tr_data = {}
        self.set_input_value("종목코드", code)
        self.set_input_value("기준일자", date)
        self.set_input_value("수정주가구분", 1)
        self.comm_rq_data("주식일봉차트조회요청", "opt10081", 0, "0101")
        return self.tr_data.get('chart_data', [])[:period]

class StockAnalyzer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.kiwoom = KiwoomAPI()
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("키움증권 주식 분석기")
        self.setGeometry(100, 100, 800, 600)
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QVBoxLayout()
        
        # 종목코드 입력
        self.code_label = QLabel("종목코드 입력 (예: 005930)")
        layout.addWidget(self.code_label)
        
        self.code_input = QLineEdit()
        layout.addWidget(self.code_input)
        
        # 버튼들
        self.login_btn = QPushButton("키움증권 로그인")
        self.login_btn.clicked.connect(self.login_kiwoom)
        layout.addWidget(self.login_btn)
        
        self.get_price_btn = QPushButton("현재가 조회")
        self.get_price_btn.clicked.connect(self.get_stock_price)
        layout.addWidget(self.get_price_btn)
        
        self.get_chart_btn = QPushButton("차트 데이터 조회")
        self.get_chart_btn.clicked.connect(self.get_stock_chart)
        layout.addWidget(self.get_chart_btn)
        
        # 결과 출력 영역
        self.result_text = QTextEdit()
        layout.addWidget(self.result_text)
        
        central_widget.setLayout(layout)
        
    def login_kiwoom(self):
        """키움증권 로그인"""
        try:
            self.kiwoom.comm_connect()
            self.result_text.append("로그인이 완료되었습니다.\n")
        except Exception as e:
            self.result_text.append(f"로그인 실패: {str(e)}\n")
            
    def get_stock_price(self):
        """주식 현재가 조회"""
        code = self.code_input.text().strip()
        if not code:
            self.result_text.append("종목코드를 입력해주세요.\n")
            return
            
        try:
            stock_info = self.kiwoom.get_stock_info(code)
            
            result = f"""
=== {stock_info['종목명']} ({code}) ===
현재가: {stock_info['현재가']:,}원
전일대비: {stock_info['전일대비']:,}원 ({stock_info['등락률']:.2f}%)
거래량: {stock_info['거래량']:,}주
시가: {stock_info['시가']:,}원
고가: {stock_info['고가']:,}원
저가: {stock_info['저가']:,}원
시가총액: {stock_info['시가총액']:,}원
PER: {stock_info['PER']:.2f}
PBR: {stock_info['PBR']:.2f}
조회시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

"""
            self.result_text.append(result)
            
        except Exception as e:
            self.result_text.append(f"데이터 조회 실패: {str(e)}\n")
            
    def get_stock_chart(self):
        """주식 차트 데이터 조회"""
        code = self.code_input.text().strip()
        if not code:
            self.result_text.append("종목코드를 입력해주세요.\n")
            return
            
        try:
            chart_data = self.kiwoom.get_stock_chart(code)
            
            if chart_data:
                self.result_text.append(f"\n=== {code} 최근 20일 차트 데이터 ===\n")
                self.result_text.append("날짜\t\t시가\t고가\t저가\t종가\t거래량\n")
                self.result_text.append("-" * 70 + "\n")
                
                for data in chart_data[:10]:  # 최근 10일만 표시
                    self.result_text.append(
                        f"{data['일자']}\t{data['시가']:,}\t{data['고가']:,}\t"
                        f"{data['저가']:,}\t{data['종가']:,}\t{data['거래량']:,}\n"
                    )
                self.result_text.append("\n")
                
        except Exception as e:
            self.result_text.append(f"차트 데이터 조회 실패: {str(e)}\n")

def main():
    app = QApplication(sys.argv)
    window = StockAnalyzer()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()

# 사용법 및 주의사항
"""
1. 설치 필요 라이브러리:
   pip install PyQt5
   pip install pandas

2. 키움증권 OpenAPI+ 설치 필요:
   - 키움증권 홈페이지에서 OpenAPI+ 다운로드 및 설치
   - 계좌개설 및 API 사용 신청 필요

3. 주요 기능:
   - 실시간 주식 가격 조회
   - 차트 데이터 조회
   - 종목 정보 분석

4. 종목코드 예시:
   - 삼성전자: 005930
   - SK하이닉스: 000660
   - NAVER: 035420
   - 카카오: 035720

5. 사용 시 주의사항:
   - 키움증권 HTS가 설치되어 있어야 함
   - Windows 환경에서만 동작
   - 장 중에만 실시간 데이터 제공
"""