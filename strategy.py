# strategy.py
import pandas as pd
import numpy as np

class Strategy:
    def __init__(self, data):
        self.data = data.copy()
        self.signals = pd.DataFrame(index=data.index)
        self.signals['Price'] = data['Close']
    
    def moving_average_crossover(self, short_window=20, long_window=50):
        """Generate signals based on moving average crossover"""
        from indicators import TechnicalIndicators
        
        # Calculate moving averages
        self.signals['Short_MA'] = TechnicalIndicators.simple_moving_average(
            self.data['Close'], short_window
        )
        self.signals['Long_MA'] = TechnicalIndicators.simple_moving_average(
            self.data['Close'], long_window
        )
        
        # Generate signals
        self.signals['Signal'] = 0
        self.signals['Signal'][self.signals['Short_MA'] > self.signals['Long_MA']] = 1
        self.signals['Signal'][self.signals['Short_MA'] < self.signals['Long_MA']] = -1
        
        # Create position changes (only trade on signal changes)
        self.signals['Position'] = self.signals['Signal'].diff()
        
        return self.signals
    
    def simple_ma_strategy(self, ma_period=20):
        """Simple strategy: Buy when price > MA, Sell when price < MA"""
        from indicators import TechnicalIndicators
        
        # Calculate moving average
        self.signals['MA'] = TechnicalIndicators.simple_moving_average(
            self.data['Close'], ma_period
        )
        
        # Generate signals
        self.signals['Signal'] = 0
        self.signals['Signal'][self.signals['Price'] > self.signals['MA']] = 1
        self.signals['Signal'][self.signals['Price'] < self.signals['MA']] = -1
        
        # Create position changes
        self.signals['Position'] = self.signals['Signal'].diff()
        
        return self.signals
