#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
1Bo's Plan - Configuration Settings
주식 분석 프로그램 설정 파일

Author: AI Assistant & User
Version: 2.0.0 - 10년 다운로드 지원
"""

import os
from pathlib import Path

# 애플리케이션 정보
APP_NAME = "1Bo's Plan"
APP_VERSION = "2.0.0"
APP_DESCRIPTION = "Advanced Stock Analysis Tool with Smart Data Management"

# 파일 경로 설정
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"
OUT_DIR = BASE_DIR / "out"
LOG_DIR = BASE_DIR / "logs"

# 디렉토리 생성
DATA_DIR.mkdir(exist_ok=True)
OUT_DIR.mkdir(exist_ok=True)
LOG_DIR.mkdir(exist_ok=True)

# UI 설정
UI_CONFIG = {
    'window_width': 1600,
    'window_height': 1000,
    'min_width': 1400,
    'min_height': 900,
    'theme': 'vista',  # 기본 테마
    'font_family': 'Segoe UI',
    'font_size_default': 11,
    'font_size_title': 20,
    'font_size_subtitle': 14,
    'font_size_info': 12,
}

# 🔥 차트 설정 - ma120 색상 추가
CHART_CONFIG = {
    'default_period': '90일',
    'figure_size': (14, 8),
    'dpi': 100,
    'colors': {
        'price': 'blue',
        'ma5': 'red',
        'ma20': 'orange', 
        'ma60': 'green',
        'ma120': 'cyan',        # 🔥 추가된 부분!
        'ma200': 'purple',
        'entry_line': 'red',
        'grid': 'gray'
    },
    'font_family': ['Malgun Gothic', 'DejaVu Sans', 'Arial Unicode MS'],
    'enable_unicode_minus': False
}

# 인기 종목 및 내 종목 (각각 8개씩)
POPULAR_STOCKS = ["AAPL", "TSLA", "MSFT", "GOOGL", "AMZN", "META", "NVDA", "NFLX"]
MY_STOCKS = ["VOO", "VTV", "PLTR", "TQQQ", "TNA", "SOXL", "SCHD", "JEPI"]

# 레버리지 ETF 목록
LEVERAGE_ETFS = ['SOXL', 'TQQQ', 'UPRO', 'TMF', 'SPXL', 'TECL', 'FNGU', 'WEBL', 'TSLL', 'TNA']

# 투자 계산 설정
INVESTMENT_CONFIG = {
    'default_budget': 10000,
    'default_splits': 4,
    'default_drop_rate': 5,  # %
    'commission_rate': 0.001,  # 0.1%
    'strategies': ['single', 'dca', 'pyramid']
}

# 위험 관리 설정
RISK_CONFIG = {
    'normal_cutloss_rates': [0.90, 0.85, 0.80],  # 10%, 15%, 20%
    'leverage_cutloss_rates': [0.88, 0.85, 0.82],  # 12%, 15%, 18%
    'risk_score_thresholds': {
        'normal': 20,
        'moderate': 40,
        'significant': 60,
        'severe': 80
    },
    'leverage_risk_multiplier': 1.3
}

# 데이터 설정 (v2.0.0 - 10년 다운로드 지원)
DATA_CONFIG = {
    'download_period': '10y',  # 기본 10년치 다운로드
    'initial_download_period': '10y',  # 첫 다운로드시 기간
    'update_mode': 'incremental',  # 증분 업데이트 모드
    'file_name_format': '{symbol}_{date}.csv',
    'date_format': '%y%m%d',
    'korean_stock_file': 'krx_stock_list.csv',
    'max_file_age_days': 30,  # 오래된 파일 정리 기준
    'update_threshold_days': 1,  # 1일 이상 오래된 데이터면 업데이트
}

# 로깅 설정
LOG_CONFIG = {
    'level': 'INFO',
    'format': '[%(asctime)s] %(levelname)s: %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S',
    'max_log_files': 10,
    'max_log_size_mb': 10
}

# 에러 처리 설정
ERROR_CONFIG = {
    'show_detailed_errors': True,
    'enable_error_logging': True,
    'enable_clipboard_copy': True,
    'auto_backup_on_error': False
}

# 기본 설정 함수들
def get_config(category, key=None, default=None):
    """설정값 가져오기"""
    config_dict = {
        'ui': UI_CONFIG,
        'chart': CHART_CONFIG,
        'investment': INVESTMENT_CONFIG,
        'risk': RISK_CONFIG,
        'data': DATA_CONFIG,
        'log': LOG_CONFIG,
        'error': ERROR_CONFIG
    }
    
    if category not in config_dict:
        return default
    
    if key is None:
        return config_dict[category]
    
    return config_dict[category].get(key, default)

def update_config(category, key, value):
    """설정값 업데이트"""
    config_dict = {
        'ui': UI_CONFIG,
        'chart': CHART_CONFIG,
        'investment': INVESTMENT_CONFIG,
        'risk': RISK_CONFIG,
        'data': DATA_CONFIG,
        'log': LOG_CONFIG,
        'error': ERROR_CONFIG
    }
    
    if category in config_dict:
        config_dict[category][key] = value
        return True
    return False

# 환경별 설정
def is_development():
    """개발 환경 여부 확인"""
    return os.getenv('DEVELOPMENT', 'False').lower() == 'true'

def get_log_level():
    """로그 레벨 가져오기"""
    if is_development():
        return 'DEBUG'
    return LOG_CONFIG['level']