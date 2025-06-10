#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Create sample stock data for VStock Advanced
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

def create_sample_data():
    """Create sample stock data"""
    
    # Create data folder if it doesn't exist
    os.makedirs('data', exist_ok=True)
    
    # Stock symbols and their approximate price ranges
    stocks = {
        'AAPL': {'base_price': 175, 'volatility': 0.02},
        'TSLA': {'base_price': 250, 'volatility': 0.04},
        'MSFT': {'base_price': 380, 'volatility': 0.025},
        'GOOGL': {'base_price': 140, 'volatility': 0.03},
        'PLTR': {'base_price': 20, 'volatility': 0.05},
        'NVDA': {'base_price': 450, 'volatility': 0.04},
        'META': {'base_price': 330, 'volatility': 0.035},
        'AMZN': {'base_price': 140, 'volatility': 0.03}
    }
    
    # Generate 2 years of data
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    date_range = pd.date_range(start_date, end_date, freq='D')
    
    for symbol, config in stocks.items():
        print(f"Creating data for {symbol}...")
        
        base_price = config['base_price']
        volatility = config['volatility']
        
        # Generate price data with random walk
        np.random.seed(42 + hash(symbol) % 1000)  # Consistent but different seed per stock
        
        prices = []
        current_price = base_price
        
        for i, date in enumerate(date_range):
            # Skip weekends
            if date.weekday() >= 5:
                continue
                
            # Random price movement
            change = np.random.normal(0, volatility * current_price)
            current_price = max(current_price + change, current_price * 0.5)  # Prevent negative prices
            
            # Generate OHLCV data
            high = current_price * (1 + abs(np.random.normal(0, 0.01)))
            low = current_price * (1 - abs(np.random.normal(0, 0.01)))
            open_price = current_price + np.random.normal(0, current_price * 0.005)
            close_price = current_price
            volume = int(np.random.normal(50000000, 20000000))  # Average volume
            volume = max(volume, 1000000)  # Minimum volume
            
            prices.append({
                'Date': date,
                'Open': round(open_price, 2),
                'High': round(high, 2),
                'Low': round(low, 2),
                'Close': round(close_price, 2),
                'Volume': volume
            })
        
        # Create DataFrame
        df = pd.DataFrame(prices)
        df.set_index('Date', inplace=True)
        
        # Save to CSV
        filename = f'data/{symbol}.csv'
        df.to_csv(filename)
        print(f"Saved {len(df)} records to {filename}")
    
    print("\nSample data creation completed!")
    print("Available stocks:", list(stocks.keys()))
    print("\nYou can now run the stock analyzer!")

if __name__ == "__main__":
    create_sample_data()