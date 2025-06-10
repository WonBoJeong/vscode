#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VStock Simple - 기본 주식 다운로드 및 분석 도구
"""

import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import yfinance as yf
import os
from datetime import datetime, timedelta
from pathlib import Path

class VStockSimple:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("📈 VStock Simple - Stock Data Downloader")
        self.root.geometry("800x600")
        
        self.current_data = None
        self.current_symbol = ""
        
        self.setup_ui()
        
    def setup_ui(self):
        """UI 설정"""
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 제목
        title_label = ttk.Label(main_frame, text="📈 VStock Simple Data Downloader", 
                               font=('Segoe UI', 16, 'bold'))
        title_label.pack(pady=(0, 20))
        
        # 입력 프레임
        input_frame = ttk.LabelFrame(main_frame, text="Stock Symbol Input", padding="15")
        input_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(input_frame, text="Enter Stock Symbol:").pack(anchor=tk.W)
        ttk.Label(input_frame, text="(US: AAPL, MSFT, TSLA / Korean: 005930, 000660)", 
                 foreground='gray').pack(anchor=tk.W)
        
        self.symbol_var = tk.StringVar()
        symbol_entry = ttk.Entry(input_frame, textvariable=self.symbol_var, font=('Segoe UI', 12))
        symbol_entry.pack(fill=tk.X, pady=(5, 10))
        symbol_entry.bind('<Return>', lambda e: self.download_data())
        
        # 버튼 프레임
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X)
        
        ttk.Button(button_frame, text="📥 Download Data", 
                  command=self.download_data).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(button_frame, text="📁 Open Data Folder", 
                  command=self.open_data_folder).pack(side=tk.LEFT)
        
        # 결과 프레임
        result_frame = ttk.LabelFrame(main_frame, text="Download Results", padding="15")
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = tk.Text(result_frame, wrap=tk.WORD, font=('Consolas', 10))
        scrollbar = ttk.Scrollbar(result_frame, orient=tk.VERTICAL, command=self.result_text.yview)
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        self.result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # 초기 메시지
        self.result_text.insert('1.0', """📈 VStock Simple Data Downloader

This tool downloads stock data from Yahoo Finance and saves it as CSV files.

Features:
• Download US and Korean stock data
• Save data in [Symbol]_YYMMDD.csv format
• Automatic data folder management
• Error handling and reporting

Instructions:
1. Enter a stock symbol (e.g., AAPL, TSLA, 005930)
2. Click 'Download Data' or press Enter
3. Data will be saved to the 'data' folder
4. Use 'Open Data Folder' to view saved files

Supported formats:
• US stocks: AAPL, MSFT, TSLA, etc.
• Korean stocks: 005930, 000660, etc. (will auto-add .KS)

Ready to download stock data!
""")
    
    def download_data(self):
        """데이터 다운로드"""
        try:
            symbol = self.symbol_var.get().strip().upper()
            if not symbol:
                messagebox.showwarning("⚠️", "Please enter a stock symbol!")
                return
            
            self.result_text.delete('1.0', tk.END)
            self.result_text.insert('1.0', f"📥 Starting download for {symbol}...\n\n")
            self.result_text.update()
            
            # 한국 주식인지 확인
            if symbol.isdigit() and len(symbol) == 6:
                download_symbol = f"{symbol}.KS"
                is_korean = True
                self.result_text.insert(tk.END, f"✅ Detected Korean stock: {symbol}\n")
                self.result_text.insert(tk.END, f"   Using Yahoo symbol: {download_symbol}\n\n")
            else:
                download_symbol = symbol
                is_korean = False
                self.result_text.insert(tk.END, f"✅ Detected US stock: {symbol}\n\n")
            
            self.result_text.update()
            
            # 데이터 다운로드
            self.result_text.insert(tk.END, "🔄 Downloading data from Yahoo Finance...\n")
            self.result_text.update()
            
            # 2년 데이터 다운로드
            end_date = datetime.now()
            start_date = end_date - timedelta(days=730)
            
            data = yf.download(download_symbol, start=start_date, end=end_date, progress=False)
            
            if data.empty:
                error_msg = f"❌ No data found for symbol: {symbol}\n"
                error_msg += "   Please check if the symbol is correct.\n"
                error_msg += "   For Korean stocks, use 6-digit codes (e.g., 005930)"
                self.result_text.insert(tk.END, error_msg)
                return
            
            # 데이터 정리
            data = data.dropna()
            data.index = pd.to_datetime(data.index)
            
            self.result_text.insert(tk.END, f"✅ Successfully downloaded {len(data)} records\n")
            self.result_text.insert(tk.END, f"   Date range: {data.index[0].strftime('%Y-%m-%d')} to {data.index[-1].strftime('%Y-%m-%d')}\n\n")
            self.result_text.update()
            
            # 폴더 생성
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            # 파일 저장
            today = datetime.now().strftime("%y%m%d")
            filename = f"{symbol}_{today}.csv"
            filepath = data_dir / filename
            
            data.to_csv(filepath)
            
            # 결과 표시
            latest_price = data['Close'].iloc[-1]
            prev_price = data['Close'].iloc[-2] if len(data) > 1 else latest_price
            change = latest_price - prev_price
            change_pct = (change / prev_price * 100) if prev_price != 0 else 0
            
            result_info = f"""💾 File saved successfully!
   File: {filename}
   Path: {filepath.absolute()}
   Size: {filepath.stat().st_size / 1024:.1f} KB

📊 Stock Information:
   Symbol: {symbol}
   Current Price: ${latest_price:.2f}
   Daily Change: ${change:+.2f} ({change_pct:+.2f}%)
   Total Records: {len(data):,}
   
📈 Data Summary:
   Open: ${data['Open'].iloc[-1]:.2f}
   High: ${data['High'].iloc[-1]:.2f}
   Low: ${data['Low'].iloc[-1]:.2f}
   Close: ${data['Close'].iloc[-1]:.2f}
   Volume: {data['Volume'].iloc[-1]:,}
   
   52-Week High: ${data['High'].max():.2f}
   52-Week Low: ${data['Low'].min():.2f}
   
✅ Download completed successfully!

💡 You can now:
   • Use this data for analysis
   • Open the data folder to view the file
   • Download more symbols
"""
            
            self.result_text.insert(tk.END, result_info)
            
            # 현재 데이터 저장
            self.current_data = data
            self.current_symbol = symbol
            
            messagebox.showinfo("✅ Success!", f"Data downloaded successfully!\nSaved as: {filename}")
            
        except Exception as e:
            error_msg = f"""❌ Download Failed!

Error Details:
{str(e)}

Possible Solutions:
• Check your internet connection
• Verify the stock symbol is correct
• For Korean stocks, use 6-digit codes (005930, not 5930)
• For US stocks, use standard symbols (AAPL, MSFT, etc.)
• Try again in a few moments

If the problem persists, the symbol might not exist or 
Yahoo Finance might be temporarily unavailable.
"""
            self.result_text.insert(tk.END, error_msg)
            messagebox.showerror("❌ Error", f"Download failed: {str(e)}")
    
    def open_data_folder(self):
        """데이터 폴더 열기"""
        try:
            data_dir = Path("data")
            data_dir.mkdir(exist_ok=True)
            
            import subprocess
            import sys
            
            if sys.platform == "win32":
                subprocess.run(["explorer", str(data_dir.absolute())])
            elif sys.platform == "darwin":
                subprocess.run(["open", str(data_dir.absolute())])
            else:
                subprocess.run(["xdg-open", str(data_dir.absolute())])
                
        except Exception as e:
            messagebox.showerror("❌ Error", f"Failed to open folder: {str(e)}")
    
    def run(self):
        """애플리케이션 실행"""
        self.root.mainloop()

if __name__ == "__main__":
    try:
        app = VStockSimple()
        app.run()
    except Exception as e:
        print(f"Critical Error: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")
