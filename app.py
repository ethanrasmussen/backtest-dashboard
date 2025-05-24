import streamlit as st
import vectorbt as vbt
import pandas as pd
import plotly.graph_objs as go
from datetime import datetime
from strategy import EMACrossover, RSIMeanReversion, BBandsBreakout, MACDCrossover, run_backtest
from util import convert_tz, handle_strategy_menu


STRATEGIES = {
    "EMA Crossover": EMACrossover,
    "RSI Mean Reversion": RSIMeanReversion,
    "Bollinger Bands Breakout": BBandsBreakout,
    "MACD Crossover": MACDCrossover
}

# Setup:
st.set_page_config(page_title='Backtesting Dashboard', layout='wide')
st.title("Backtesting Dashboard")


# Sidebar controls:
with st.sidebar:
    st.header("Basic Info")
    ticker = st.text_input("Enter ticker symbol (e.g., 'AAPL')", value="AAPL")
    start_date = st.date_input("Start Date", value=pd.to_datetime("2010-01-01"))
    end_date = st.date_input("End Date", value=pd.to_datetime(datetime.today()))

    st.header("Strategy Selection")
    selected_strat = st.selectbox("Select a Strategy", options=STRATEGIES.keys())
    strat_data = handle_strategy_menu(selected_strat)
    st.write(strat_data)

    st.header("Backtest Controls")
    init_equity = st.number_input("Initial Equity Position", value=25000)
    size = st.number_input("Position Size", value=10)
    size_type = st.selectbox("Size Type", ["Amount", "Value", "Percent"], index=2)
    fees = st.number_input("Fees (as %)", value=0.10, format="%.4f")
    direction = st.selectbox("Direction", ["Long Only", "Short Only", "Both"], index=0)

    bt_ran = st.button("Run Backtest")


# Main page:
if not bt_ran:
    st.warning("This page will populate once you run a backtest! Use the sidebar on the left to input your settings.")
if bt_ran:
    with st.spinner(f"Running backtest for {ticker}..."):
        data = vbt.YFData.download(ticker, start=convert_tz(start_date), end=convert_tz(end_date)).get('Close')
        strat = STRATEGIES[selected_strat](
            strategy_data = strat_data,
            price_data = data
        )
        pf = run_backtest(
            strategy = strat,
            size = size,
            size_type = size_type,
            init_equity = init_equity,
            fees = fees,
            direction = direction
        )
        if isinstance(strat, BBandsBreakout):
            pass
            # TODO: Implement BBands animated graph (may need external API w/ adv. compute)
            # strat.bbands_plot()
    st.write(f"Backtest results for {ticker}:")
    summary, equitycurve, drawdown, trades, stats = st.tabs([
        "Portfolio Summary",
        "Equity Curve",
        "Drawdown Curve",
        "List of Trades",
        "Full Statistics"
    ])

    statdf = pd.DataFrame(pf.stats(), columns=['Value'])
    statdf.index.name = 'Stat/Measure:'
    
    with summary:
        st.markdown("#### Backtest & Portfolio Summary:")
        st.markdown(f"**Total Return:** ${round(statdf.loc['End Value', 'Value'] - statdf.loc['Start Value', 'Value'], 2)} ({round(statdf.loc['Total Return [%]', 'Value'], 2)}%)")
        st.markdown(f"**Final Portfolio Value:** ${round(statdf.loc['End Value', 'Value'], 2)}")
        st.markdown(f"**Total Fees Paid:** ${round(statdf.loc['Total Fees Paid', 'Value'], 2)}")
        st.markdown(f"**Overall:** {statdf.loc['Total Trades', 'Value']} trades over {str(statdf.loc['Period', 'Value']).split(' days')[0]} days with {round(statdf.loc['Win Rate [%]', 'Value'], 2)}% win rate")
        st.markdown("#### Figures (Orders, P/L, Returns):")
        st.plotly_chart(pf.plot(), use_container_width=True)

    with equitycurve:
        data = pf.value()
        eq_trace = go.Scatter(x=data.index, y=data, mode='lines', name='Equity',line=dict(color='green') )
        eq_curve = go.Figure(data=[eq_trace])
        eq_curve.update_layout(title='Equity Curve', xaxis_title='Date', yaxis_title='Equity')
        st.plotly_chart(eq_curve)

    with drawdown:
        data = pf.drawdown() * 100
        ddown_trace = go.Scatter(
            x=data.index,
            y=data,
            mode='lines',
            name='Drawdown',
            fill='tozeroy',
            line=dict(color='red')
        )
        ddown_curve = go.Figure(data=[ddown_trace])
        ddown_curve.update_layout(
            title='Drawdown Curve',
            xaxis_title='Date',
            yaxis_title='% Drawdown',
            template='plotly_white'
        )
        st.plotly_chart(ddown_curve)

    with trades:
        st.markdown("**List of Trades:**")
        tradedf = pf.trades.records_readable
        tradedf = tradedf.round(2)
        tradedf.index.name = 'Trade Num.'
        tradedf.drop(tradedf.columns[[0,1]], axis=1, inplace=True)
        st.dataframe(tradedf)

    with stats:
        st.markdown("**Full Stats from Backtest:**")
        st.dataframe(statdf, height=1025)
