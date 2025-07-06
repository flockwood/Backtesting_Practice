# visualizer.py
import matplotlib.pyplot as plt
import pandas as pd

class Visualizer:
    @staticmethod
    def plot_strategy_performance(data, signals, portfolio_history, ticker):
        """Create comprehensive strategy visualization"""
        fig, axes = plt.subplots(3, 1, figsize=(14, 12))
        
        # Plot 1: Price and Moving Average with signals
        ax1 = axes[0]
        ax1.plot(data.index, data['Close'], label=f'{ticker} Close', linewidth=1, alpha=0.8)
        
        if 'MA' in signals.columns:
            ax1.plot(signals.index, signals['MA'], label='Moving Average', linewidth=1.5)
        
        # Mark buy/sell points
        buys = signals[signals['Position'] == 1]
        sells = signals[signals['Position'] == -1]
        
        if len(buys) > 0:
            ax1.scatter(buys.index, buys['Price'], color='green', marker='^', 
                       s=100, label='Buy Signal', zorder=5)
        
        if len(sells) > 0:
            ax1.scatter(sells.index, sells['Price'], color='red', marker='v', 
                       s=100, label='Sell Signal', zorder=5)
        
        ax1.set_title(f'{ticker} Price and Trading Signals', fontsize=14)
        ax1.set_ylabel('Price ($)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Plot 2: Portfolio Performance vs Buy & Hold
        ax2 = axes[1]
        ax2.plot(portfolio_history['Date'], portfolio_history['Portfolio_Value'], 
                label='Strategy Portfolio', linewidth=2, color='blue')
        
        # Buy and hold comparison
        initial_cash = portfolio_history['Portfolio_Value'].iloc[0]
        buy_hold_values = initial_cash * (portfolio_history['Price'] / portfolio_history['Price'].iloc[0])
        ax2.plot(portfolio_history['Date'], buy_hold_values, 
                label='Buy & Hold', linewidth=2, alpha=0.7, color='orange')
        
        ax2.set_title('Portfolio Performance Comparison', fontsize=14)
        ax2.set_ylabel('Portfolio Value ($)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # Plot 3: Daily Returns
        ax3 = axes[2]
        daily_returns = portfolio_history['Portfolio_Value'].pct_change()
        ax3.plot(portfolio_history['Date'], daily_returns * 100, 
                linewidth=1, alpha=0.7, color='purple')
        ax3.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax3.set_title('Daily Returns (%)', fontsize=14)
        ax3.set_ylabel('Return (%)')
        ax3.set_xlabel('Date')
        ax3.grid(True, alpha=0.3)
        
        plt.tight_layout()
        plt.show()
    
    @staticmethod
    def plot_trade_analysis(trade_log):
        """Plot trade analysis"""
        if trade_log.empty:
            print("No trades to analyze")
            return
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))
        
        # Trade timeline
        ax1.scatter(trade_log['Date'], trade_log['Price'], 
                   c=['green' if action == 'BUY' else 'red' for action in trade_log['Action']], 
                   s=100, alpha=0.7)
        ax1.set_title('Trade Timeline')
        ax1.set_ylabel('Price ($)')
        ax1.set_xlabel('Date')
        ax1.grid(True, alpha=0.3)
        
        # Trade distribution
        trade_counts = trade_log['Action'].value_counts()
        ax2.bar(trade_counts.index, trade_counts.values, 
               color=['green' if x == 'BUY' else 'red' for x in trade_counts.index])
        ax2.set_title('Trade Distribution')
        ax2.set_ylabel('Number of Trades')
        
        plt.tight_layout()
        plt.show()