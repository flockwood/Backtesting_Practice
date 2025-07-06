# main.py
from datetime import datetime, timedelta
from data_handler import DataHandler
from strategy import Strategy
from portfolio import Portfolio
from visualizer import Visualizer

def main():
    # Configuration
    TICKER = 'AAPL'
    INITIAL_CASH = 10000
    MA_PERIOD = 20
    
    # Date range (last 2 years)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=730)
    
    print(f"Starting backtest for {TICKER}")
    print(f"Period: {start_date.date()} to {end_date.date()}")
    print(f"Initial Cash: ${INITIAL_CASH:,}")
    print(f"Moving Average Period: {MA_PERIOD} days")
    print("="*50)
    
    # Step 1: Get and clean data
    data_handler = DataHandler(TICKER)
    data = data_handler.get_data(start_date, end_date)
    clean_data = data_handler.clean_data()
    
    # Step 2: Generate trading signals
    strategy = Strategy(clean_data)
    signals = strategy.simple_ma_strategy(MA_PERIOD)
    
    # Step 3: Run portfolio simulation
    portfolio = Portfolio(INITIAL_CASH)
    portfolio_history = portfolio.backtest(signals)
    
    # Step 4: Calculate performance metrics
    performance = portfolio.calculate_performance()
    
    # Step 5: Display results
    print("\nTRADE LOG:")
    print("-" * 30)
    trade_log = portfolio.get_trade_log()
    if len(trade_log) > 0:
        for _, trade in trade_log.iterrows():
            print(f"{trade['Action']}: {trade['Shares']:.2f} shares at ${trade['Price']:.2f} on {trade['Date'].date()}")
    else:
        print("No trades executed during this period")
    
    print("\nPERFORMANCE RESULTS:")
    print("="*50)
    for key, value in performance.items():
        if 'Return' in key or 'Ratio' in key:
            print(f"{key}: {value:.2f}%")
        elif 'Volatility' in key:
            print(f"{key}: {value:.2f}%")
        elif key == 'Number of Trades':
            print(f"{key}: {value}")
        else:
            print(f"{key}: ${value:,.2f}")
    print("="*50)
    
    # Step 6: Create visualizations
    visualizer = Visualizer()
    visualizer.plot_strategy_performance(clean_data, signals, portfolio_history, TICKER)
    visualizer.plot_trade_analysis(trade_log)
    
    return performance

if __name__ == "__main__":
    results = main()