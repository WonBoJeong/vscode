#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
R 스크립트 연동을 위한 VStock Advanced 설정 업데이트
"""

import json
from pathlib import Path
import os

def update_config_for_r_integration():
    """R 스크립트와 연동을 위한 설정 업데이트"""
    
    # R 스크립트 경로 감지
    r_data_paths = [
        "~/R_stats/R_stock/data",
        "D:/R_stats/R_stock/data", 
        "C:/Users/*/Documents/R_stats/R_stock/data",
        "../R_stock/data",
        "data"  # 현재 폴더
    ]
    
    # 실제 존재하는 경로 찾기
    valid_data_path = None
    for path in r_data_paths:
        expanded_path = Path(path).expanduser()
        if expanded_path.exists():
            valid_data_path = str(expanded_path)
            break
    
    # 설정 업데이트
    config_path = Path("config/config.json")
    
    # 기본 설정 로드
    if config_path.exists():
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
    else:
        config = {}
    
    # R 연동 설정 추가
    config.update({
        "data_folder": valid_data_path or "D:/vscode/stock/data",
        "r_integration": {
            "enabled": True,
            "r_script_path": "~/R_stats/R_stock/",
            "data_path": valid_data_path,
            "auto_detect_r_files": True,
            "supported_file_patterns": [
                "*_*.csv",  # R 스크립트 형태: SYMBOL_DATE.csv
                "*.csv"
            ]
        },
        "etf_symbols": [
            "TQQQ", "SOXL", "FNGU", "NAIL", "TECL", "LABU", 
            "RETL", "WEBL", "DPST", "TNA", "HIBL", "BNKU",
            "DFEN", "PILL", "MIDU", "WANT", "FAS", "TPOR"
        ],
        "portfolio_symbols": [
            "TQQQ", "SOXL", "TNA", "TECL", "FNGU",
            "VOO", "VTV", "PLTR", "SCHD", "JEPI", "JEPQ"
        ],
        "default_symbols": [
            "TQQQ", "SOXL", "FNGU", "TNA", "AAPL", "TSLA", "NVDA", "PLTR"
        ]
    })
    
    # 설정 저장
    config_path.parent.mkdir(exist_ok=True)
    with open(config_path, 'w', encoding='utf-8') as f:
        json.dump(config, f, indent=2, ensure_ascii=False)
    
    print(f"✅ 설정 업데이트 완료!")
    print(f"📁 데이터 경로: {config['data_folder']}")
    print(f"🔗 R 연동: {'활성화' if config['r_integration']['enabled'] else '비활성화'}")
    
    return config

if __name__ == "__main__":
    update_config_for_r_integration()