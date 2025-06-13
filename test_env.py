#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Python 환경 테스트
"""

import sys
import pandas as pd
import numpy as np
import tkinter as tk

def test_environment():
    """기본 환경 테스트"""
    print(f"Python 버전: {sys.version}")
    print(f"Pandas 버전: {pd.__version__}")
    print(f"Numpy 버전: {np.__version__}")
    
    # Tkinter 테스트
    try:
        root = tk.Tk()
        root.withdraw()
        print("Tkinter 정상 작동")
    except:
        print("Tkinter 오류 발생")
    
    # 데이터프레임 테스트
    try:
        df = pd.DataFrame({'test': [1, 2, 3]})
        print("Pandas 정상 작동")
    except:
        print("Pandas 오류 발생")

if __name__ == "__main__":
    test_environment()