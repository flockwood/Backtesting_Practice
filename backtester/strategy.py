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
        from backtester.indicators import TechnicalIndicators
        
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
        from backtester.indicators import TechnicalIndicators
        
        # Calculate moving average
        self.signals['MA'] = TechnicalIndicators.simple_moving_average(
            self.data['Close'], ma_period
        )
        
        # Initialize all columns
        self.signals['Signal'] = 0
        self.signals['Position'] = 0
        
        # Get valid data (drop NaN values from MA calculation)
        valid_data = self.signals.dropna(subset=['MA']).copy()
        
        print(f"Valid data points: {len(valid_data)}")
        
        # Generate signals for valid data only
        valid_data['Signal'] = 0
        valid_data.loc[valid_data['Price'] > valid_data['MA'], 'Signal'] = 1   # Buy
        valid_data.loc[valid_data['Price'] < valid_data['MA'], 'Signal'] = -1  # Sell
        
        # Debug signal counts
        signal_counts = valid_data['Signal'].value_counts().sort_index()
        print(f"Signal distribution: {dict(signal_counts)}")
        
        # Manual position change detection
        valid_data['Position'] = 0
        prev_signal = 0  # Start with no position
        
        position_changes = []
        
        for i, (date, row) in enumerate(valid_data.iterrows()):
            current_signal = row['Signal']
            
            # Check if signal changed
            if current_signal != prev_signal:
                valid_data.loc[date, 'Position'] = current_signal
                action = "BUY" if current_signal == 1 else "SELL" if current_signal == -1 else "NEUTRAL"
                position_changes.append({
                    'Date': date,
                    'Action': action,
                    'Price': row['Price'],
                    'MA': row['MA'],
                    'Signal': current_signal
                })
                print(f"Position change {len(position_changes)}: {date.date()} - {action} at ${row['Price']:.2f} (MA: ${row['MA']:.2f})")
            
            prev_signal = current_signal
        
        # Copy back to main signals DataFrame
        self.signals.update(valid_data[['Signal', 'Position']])
        
        # Summary
        buy_count = len([p for p in position_changes if p['Signal'] == 1])
        sell_count = len([p for p in position_changes if p['Signal'] == -1])
        
        print(f"\n=== STRATEGY SUMMARY ===")
        print(f"Total position changes: {len(position_changes)}")
        print(f"Buy signals: {buy_count}")
        print(f"Sell signals: {sell_count}")
        
        if len(position_changes) == 0:
            print("ERROR: No position changes detected!")
            print("This suggests the signal never changes from its initial value.")
            
            # Emergency debug: check first few days
            print("\nFirst 10 valid days:")
            print(valid_data[['Price', 'MA', 'Signal']].head(10))
        
        return self.signals