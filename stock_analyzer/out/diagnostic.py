#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Diagnostic Tool - 시스템 진단 및 문제 해결
"""

import sys
import traceback
from datetime import datetime

def print_separator(title=""):
    print("=" * 60)
    if title:
        print(f" {title}")
        print("=" * 60)

def test_python_environment():
    """Python 환경 테스트"""
    print_separator("Python Environment Test")
    try:
        print(f"✅ Python Version: {sys.version}")
        print(f"✅ Python Path: {sys.executable}")
        print(f"✅ Platform: {sys.platform}")
        return True
    except Exception as e:
        print(f"❌ Python Environment Error: {e}")
        return False

def test_package_imports():
    """패키지 임포트 테스트"""
    print_separator("Package Import Test")
    
    packages = {
        'tkinter': 'tkinter',
        'pandas': 'pandas',
        'yfinance': 'yfinance',
        'numpy': 'numpy (optional)',
        'requests': 'requests'
    }
    
    results = {}
    
    for package_name, description in packages.items():
        try:
            if package_name == 'tkinter':
                import tkinter
                print(f"✅ {description}: Available")
                results[package_name] = True
            elif package_name == 'pandas':
                import pandas as pd
                print(f"✅ {description}: Version {pd.__version__}")
                results[package_name] = True
            elif package_name == 'yfinance':
                import yfinance as yf
                print(f"✅ {description}: Available")
                results[package_name] = True
            elif package_name == 'numpy':
                import numpy as np
                print(f"✅ {description}: Version {np.__version__}")
                results[package_name] = True
            elif package_name == 'requests':
                import requests
                print(f"✅ {description}: Version {requests.__version__}")
                results[package_name] = True
                
        except ImportError as e:
            print(f"❌ {description}: NOT FOUND - {e}")
            results[package_name] = False
        except Exception as e:
            print(f"⚠️ {description}: ERROR - {e}")
            results[package_name] = False
    
    return results

def test_internet_connection():
    """인터넷 연결 테스트"""
    print_separator("Internet Connection Test")
    
    try:
        import requests
        
        # Google DNS 테스트
        response = requests.get("http://8.8.8.8", timeout=5)
        print("✅ Basic Internet: Connected")
        
        # Yahoo Finance 접근 테스트
        response = requests.get("https://finance.yahoo.com", timeout=10)
        if response.status_code == 200:
            print("✅ Yahoo Finance: Accessible")
        else:
            print(f"⚠️ Yahoo Finance: Status Code {response.status_code}")
        
        return True
        
    except ImportError:
        print("❌ Cannot test internet - requests module not available")
        return False
    except requests.exceptions.ConnectTimeout:
        print("❌ Internet Connection: TIMEOUT")
        return False
    except requests.exceptions.ConnectionError:
        print("❌ Internet Connection: FAILED")
        return False
    except Exception as e:
        print(f"❌ Internet Connection Error: {e}")
        return False

def test_yfinance_download():
    """YFinance 다운로드 테스트"""
    print_separator("YFinance Download Test")
    
    try:
        import yfinance as yf
        import pandas as pd
        
        print("🔄 Testing AAPL data download...")
        
        # 간단한 데이터 다운로드 테스트
        ticker = yf.Ticker("AAPL")
        hist = ticker.history(period="5d")
        
        if len(hist) > 0:
            latest_price = hist['Close'].iloc[-1]
            print(f"✅ YFinance Download: SUCCESS")
            print(f"   AAPL Latest Price: ${latest_price:.2f}")
            print(f"   Data Points: {len(hist)}")
            return True
        else:
            print("❌ YFinance Download: NO DATA RETURNED")
            return False
            
    except ImportError as e:
        print(f"❌ YFinance Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ YFinance Download Error: {e}")
        print(f"   Full Error: {traceback.format_exc()}")
        return False

def test_tkinter_gui():
    """Tkinter GUI 테스트"""
    print_separator("Tkinter GUI Test")
    
    try:
        import tkinter as tk
        
        # 간단한 창 테스트
        root = tk.Tk()
        root.title("Test Window")
        root.geometry("300x200")
        
        label = tk.Label(root, text="✅ Tkinter is working!")
        label.pack(pady=50)
        
        # 2초 후 자동으로 닫기
        root.after(2000, root.destroy)
        
        print("✅ Tkinter GUI: Working (test window will appear briefly)")
        root.mainloop()
        
        return True
        
    except ImportError as e:
        print(f"❌ Tkinter Import Error: {e}")
        return False
    except Exception as e:
        print(f"❌ Tkinter Error: {e}")
        return False

def generate_install_commands(failed_packages):
    """실패한 패키지들의 설치 명령 생성"""
    if not failed_packages:
        return
    
    print_separator("Installation Commands")
    print("Copy and run these commands to install missing packages:\n")
    
    if 'pandas' in failed_packages:
        print("pip install pandas")
    if 'yfinance' in failed_packages:
        print("pip install yfinance")
    if 'numpy' in failed_packages:
        print("pip install numpy")
    if 'requests' in failed_packages:
        print("pip install requests")
    
    print("\nOr install all at once:")
    print("pip install pandas yfinance numpy requests")
    
    print("\nIf pip doesn't work, try:")
    print("python -m pip install pandas yfinance numpy requests")

def main():
    """메인 진단 함수"""
    print("🔍 VStock System Diagnostic Tool")
    print(f"⏰ Test Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print_separator()
    
    failed_packages = []
    
    # 1. Python 환경 테스트
    if not test_python_environment():
        print("\n❌ CRITICAL: Python environment issue detected!")
        return
    
    print()
    
    # 2. 패키지 임포트 테스트
    package_results = test_package_imports()
    for package, success in package_results.items():
        if not success and package in ['pandas', 'yfinance', 'tkinter']:
            failed_packages.append(package)
    
    print()
    
    # 3. 인터넷 연결 테스트
    internet_ok = test_internet_connection()
    
    print()
    
    # 4. YFinance 테스트 (패키지가 있는 경우만)
    if 'yfinance' not in failed_packages and 'pandas' not in failed_packages:
        yfinance_ok = test_yfinance_download()
    else:
        print_separator("YFinance Download Test")
        print("❌ Skipped - Required packages not available")
        yfinance_ok = False
    
    print()
    
    # 5. Tkinter 테스트 (패키지가 있는 경우만)
    if 'tkinter' not in failed_packages:
        tkinter_ok = test_tkinter_gui()
    else:
        print_separator("Tkinter GUI Test")
        print("❌ Skipped - Tkinter not available")
        tkinter_ok = False
    
    print()
    
    # 결과 요약
    print_separator("DIAGNOSTIC SUMMARY")
    
    if failed_packages:
        print("❌ ISSUES FOUND:")
        for package in failed_packages:
            print(f"   • {package} is not installed")
    
    if not internet_ok:
        print("❌ NETWORK ISSUE: Cannot access internet or Yahoo Finance")
    
    if failed_packages or not internet_ok:
        print("\n🔧 RECOMMENDED ACTIONS:")
        
        if failed_packages:
            print("1. Install missing packages (see commands below)")
        
        if not internet_ok:
            print("2. Check your internet connection")
            print("3. Check firewall/antivirus settings")
            print("4. Try using a VPN if Yahoo Finance is blocked")
        
        generate_install_commands(failed_packages)
    
    else:
        print("✅ ALL TESTS PASSED!")
        print("Your system should be ready to run VStock applications.")
    
    print_separator()
    
    # 에러 로그 파일 생성
    try:
        with open("vstock_diagnostic_log.txt", "w", encoding="utf-8") as f:
            f.write(f"VStock Diagnostic Log - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Python Version: {sys.version}\n")
            f.write(f"Platform: {sys.platform}\n\n")
            f.write("Package Results:\n")
            for package, success in package_results.items():
                f.write(f"  {package}: {'✅' if success else '❌'}\n")
            f.write(f"\nInternet: {'✅' if internet_ok else '❌'}\n")
            f.write(f"YFinance: {'✅' if 'yfinance_ok' in locals() and yfinance_ok else '❌'}\n")
            f.write(f"Tkinter: {'✅' if 'tkinter_ok' in locals() and tkinter_ok else '❌'}\n")
        
        print("📝 Diagnostic log saved to: vstock_diagnostic_log.txt")
    
    except Exception as e:
        print(f"⚠️ Could not save log file: {e}")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n🛑 Diagnostic interrupted by user")
    except Exception as e:
        print(f"\n\n💥 CRITICAL ERROR in diagnostic tool:")
        print(f"Error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
    
    input("\nPress Enter to exit...")
