# portfolio.py
import pandas as pd
import numpy as np

class Portfolio:
    def __init__(self, initial_cash=10000):
        self.initial_cash = initial_cash
        self.portfolio_history = []
        self.trade_log = []
    
    def backtest(self, signals_df):
        """Run portfolio simulation based on signals"""
        cash = self.initial_cash
        shares = 0
        portfolio_values = []
        
        for i, row in signals_df.iterrows():
            if pd.isna(row.get('MA')):  # Skip days without indicators
                portfolio_values.append(cash)
                continue
            
            # Execute trades based on position changes
            if row['Position'] == 1:  # Buy signal
                if cash > 0:
                    shares = cash / row['Price']
                    cash = 0
                    self.trade_log.append({
                        'Date': i,
                        'Action': 'BUY',
                        'Shares': shares,
                        'Price': row['Price'],
                        'Value': shares * row['Price']
                    })
                    
            elif row['Position'] == -1:  # Sell signal
                if shares > 0:
                    cash = shares * row['Price']
                    self.trade_log.append({
                        'Date': i,
                        'Action': 'SELL',
                        'Shares': shares,
                        'Price': row['Price'],
                        'Value': cash
                    })
                    shares = 0
            
            # Calculate current portfolio value
            current_value = cash + (shares * row['Price'])
            portfolio_values.append(current_value)
        
        # Create portfolio history DataFrame
        self.portfolio_history = pd.DataFrame({
            'Date': signals_df.index,
            'Portfolio_Value': portfolio_values,
            'Price': signals_df['Price']
        })
        
        return self.portfolio_history
    
    def calculate_performance(self):
        """Calculate performance metrics"""
        if not len(self.portfolio_history):
            raise ValueError("No portfolio history. Run backtest() first.")
        
        final_value = self.portfolio_history['Portfolio_Value'].iloc[-1]
        total_return = ((final_value - self.initial_cash) / self.initial_cash) * 100
        
        # Buy and hold comparison
        first_price = self.portfolio_history['Price'].iloc[0]
        last_price = self.portfolio_history['Price'].iloc[-1]
        buy_hold_return = ((last_price - first_price) / first_price) * 100
        
        # Calculate daily returns for additional metrics
        portfolio_returns = self.portfolio_history['Portfolio_Value'].pct_change().dropna()
        
        metrics = {
            'Initial Cash': self.initial_cash,
            'Final Portfolio Value': final_value,
            'Total Return': total_return,
            'Buy & Hold Return': buy_hold_return,
            'Strategy vs Buy & Hold': total_return - buy_hold_return,
            'Number of Trades': len(self.trade_log),
            'Volatility': portfolio_returns.std() * np.sqrt(252),  # Annualized
            'Sharpe Ratio': (portfolio_returns.mean() / portfolio_returns.std()) * np.sqrt(252) if portfolio_returns.std() != 0 else 0
        }
        
        return metrics
    
    def get_trade_log(self):
        """Return trade log as DataFrame"""
        return pd.DataFrame(self.trade_log)
