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

def apply_theme():
    # From Spotify theming: https://github.com/jrieke/advanced-theming-spotify/tree/main
    titleFontSize = "39.5px"
    titleFontWeight = "900"
    headerFontSize = "32px"
    headerFontWeight = "700"
    subheaderFontSize = "24px"
    subheaderFontWeight = "700"
    buttonBorderRadius = "1.6rem"
    secondaryButtonHoverBorderColor = "#ffffff" 
    secondaryButtonHoverTextColor = "inherit"
    primaryButtonHoverBorderColor = "#1ED760"
    pillsBackgroundColor = "#2a2a2a"
    pillsBorderColor = "none"
    pillsHoverBackgroundColor = "#333333"
    pillsHoverTextColor = "inherit"
    activePillBackgroundColor = "#ffffff"
    activePillTextColor = "#000000"
    activePillBorderColor = "none"
    activePillHoverBackgroundColor = "#ffffff"
    activePillHoverTextColor = "#000000"
    st.html(
        f"""
        <style>
        h1 {{
            font-size: {titleFontSize} !important;
            font-weight: {titleFontWeight} !important;
        }}
        
        h2 {{
            font-size: {headerFontSize} !important;
            font-weight: {headerFontWeight} !important;
        }}
        
        h3 {{
            font-size: {subheaderFontSize} !important;
            font-weight: {subheaderFontWeight} !important;
        }}
        
        .stButton button, .stDownloadButton button, .stLinkButton a, .stFormSubmitButton button {{
            border-radius: {buttonBorderRadius} !important;
        }}
        
        .stButton button[kind="secondary"]:hover, .stDownloadButton button[kind="secondary"]:hover, .stLinkButton a[kind="secondary"]:hover, .stFormSubmitButton button[kind="secondary"]:hover {{
            border-color: {secondaryButtonHoverBorderColor} !important;
            color: {secondaryButtonHoverTextColor} !important;
        }}
        
        .stButton button[kind="primary"]:hover, .stDownloadButton button[kind="primary"]:hover, .stLinkButton a[kind="primary"]:hover, .stFormSubmitButton button[kind="primary"]:hover {{
            border-color: {primaryButtonHoverBorderColor} !important;
        }}
        
        [data-testid="stBaseButton-pills"] {{
            background-color: {pillsBackgroundColor} !important;
            border: {pillsBorderColor} !important;
        }}
        
        [data-testid="stBaseButton-pills"]:hover {{
            background-color: {pillsHoverBackgroundColor} !important;
            color: {pillsHoverTextColor} !important;
        }}
        
        [data-testid="stBaseButton-pillsActive"] {{
            background-color: {activePillBackgroundColor} !important;
            color: {activePillTextColor} !important;
            border: {activePillBorderColor} !important;
        }}
        
        [data-testid="stBaseButton-pillsActive"]:hover {{
            background-color: {activePillHoverBackgroundColor} !important;
            color: {activePillHoverTextColor} !important;
        }}
    
        </style>
        """
    )
