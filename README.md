# Demo Video:

https://github.com/user-attachments/assets/5e39d971-8f85-463a-9456-8bf67bfca00c

# Supported Strategies:

### EMA Crossover:
Two exponential moving averages of the price, where buy orders occur when fast EMA rises above slow EMA, and sell orders occur when the inverse occurs. 

Users can set:
 - fast_ema_window
 - slow_ema_window

### RSI Mean Reversion:
Buy orders when Relative Strength Index dips below the "oversold threshold", and sell when RSI climbs above "overbought threshold."

Users can set:
 - rsi_window
 - oversold_threshold
 - overbought_threshold

### Bollinger Bands Breakout:
Use Bollinger bands that expand & contract with volatility. When price closes below the lower band, set buy orders, and set sell orders when price closes above the upper band.

Users can set:
 - bb_window
 - alpha
 - middle_band_type

### MACD Crossover:
Buy orders when MACD line crosses above signal line, and sell orders for the inverse.

Users can set:
 - fast_window
 - slow_window
 - signal_window

# Supported Metrics/Analytics:

### Trade Figures (Orders, P/L, Cumulative Returns):
Several trade figures are available on the first page of the backtest results:

1. Order history imposed on close price line
2. Profit/loss per trade over period of backtest
3. Cumulative returns over period of backtest

### Equity Curve:
Time series of total portfolio value over the backtest period, which visualizes overall growth/ROI & risk of strategy. Traders should aim for a steadily rising curve without large dips -- an indicator of a robust strategy.

### Drawdown Curve:
Graph showing, at each point in time, the decline from the most recent peak of the equity curve. Drawdowns quantify the worst losses, and can indicate the risk and psychological stress associated with a specific strategy.

# Usage/Setup:

To run locally, you'll need the Python runtime installed. Then, clone this repo and run:

`python3 -m pip install -r requirements.txt && python3 -m streamlit run`