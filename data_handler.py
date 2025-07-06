# data_handler.py
import yfinance as yf
import pandas as pd

class DataHandler:
    def __init__(self, ticker):
        self.ticker = ticker
        self.data = None
    
    def get_data(self, start_date, end_date):
        """Download stock data from Yahoo Finance"""
        print(f"Downloading {self.ticker} data...")
        stock = yf.Ticker(self.ticker)
        self.data = stock.history(start=start_date, end=end_date)
        print(f"Downloaded {len(self.data)} trading days")
        return self.data
    
    def clean_data(self):
        """Clean and validate data"""
        if self.data is None:
            raise ValueError("No data loaded. Call get_data() first.")
        
        # Remove any NaN values
        self.data = self.data.dropna()
        
        # Ensure we have required columns
        required_cols = ['Open', 'High', 'Low', 'Close', 'Volume']
        for col in required_cols:
            if col not in self.data.columns:
                raise ValueError(f"Missing required column: {col}")
        
        return self.data