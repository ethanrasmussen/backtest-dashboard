import streamlit as st
from datetime import datetime
import pytz

# Date to datetime with timezone
def convert_tz(date):
    return datetime.combine(date, datetime.min.time()).replace(tzinfo=pytz.UTC)

def prep_size(size_str_rep:str, size_type:str):
    # Convert size to appropriate type
    if size_type == 'Percent':
        size_value = float(size_str_rep) / 100.0
    else:
        size_value = float(size_str_rep)
    return size_value

def handle_strategy_menu(selected_strat:str):
    strategy_dict = {}
    match selected_strat:

        case "EMA Crossover":
            strategy_dict['fast_ema_window'] = st.number_input(label="Fast EMA Window", value=10)
            strategy_dict['slow_ema_window'] = st.number_input(label="Slow EMA Window", value=20)

        case "RSI Mean Reversion":
            strategy_dict['rsi_window'] = st.number_input(label="RSI Window/Period", value=14)
            strategy_dict['oversold_threshold'] = st.number_input(label="Threshold to be 'Oversold'", value=30)
            strategy_dict['overbought_threshold'] = st.number_input(label="Threshold to be 'Overbought'", value=70)

        case "Bollinger Bands Breakout":
            strategy_dict['bb_window'] = st.number_input(label="BB Window/Period", value=20)
            strategy_dict['alpha'] = st.number_input(label="Alpha", value=2)
            strategy_dict['middle_band_type'] = st.selectbox(label="Middle Band Type", options=["EMA","SMA"])

        case "MACD Crossover":
            strategy_dict['fast_window'] = st.number_input(label="Fast Window", value=12)
            strategy_dict['slow_window'] = st.number_input(label="Slow Window", value=26)
            strategy_dict['signal_window'] = st.number_input(label="Signal Window", value=9)

        case "Momentum":
            strategy_dict['num_days'] = st.number_input(label="Number of Days", value=20)

        case _:
            st.error("Invalid strategy selected.")

    return strategy_dict
