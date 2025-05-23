import streamlit as st
import vectorbt as vbt
import pandas as pd
import numpy as np
import plotly.graph_objs as go
from datetime import datetime
import pytz
from util import convert_tz, prep_size


class TradeStrategy():
    def __init__(self, strategy_data:dict, price_data):
        self.entries = None
        self.exits = None
        self.strategy_data = strategy_data
        self.price_data = price_data
    def populate_signals(self):
        pass # Func will be overridden to populate signal values from strategy & price data
    def get_signals(self):
        return self.entries, self.exits
    
class EMACrossover(TradeStrategy):
    ### STRAT DATA ###
    # fast_ema_window
    # slow_ema_window
    ##################
    def populate_signals(self):
        fast_ema = vbt.MA.run(self.price_data, window=self.strategy_data.fast_ema_window, ewm=True).ma
        slow_ema = vbt.MA.run(self.price_data, window=self.strategy_data.slow_ema_window, ewm=True).ma
        self.entries = fast_ema > slow_ema
        self.exits = fast_ema < slow_ema

class RSIMeanReversion(TradeStrategy):
    ### STRAT DATA ###
    # rsi_window
    # oversold_threshold
    # overbought_threshold
    ##################
    def populate_signals(self):
        rsi = vbt.RSI.run(self.price_data, window=self.strategy_data.rsi_window).rsi
        self.entries = rsi < 30
        self.exits = rsi > 70

class BBandsBreakout(TradeStrategy):
    ### STRAT DATA ###
    # bb_window
    # std
    ##################
    def populate_signals(self):
        bb = vbt.BBANDS.run(self.price_data, window=self.strategy_data.bb_window, std=self.strategy_data.std)
        self.entries = self.price_data < bb.lower
        self.exits = self.price_data > bb.upper

class MACDCrossover(TradeStrategy):
    ### STRAT DATA ###
    # fast_window
    # slow_window
    # signal_window
    ##################
    def populate_signals(self):
        macd_res = vbt.MACD.run(self.price_data, fast_window=self.strategy_data.fast_window, slow_window=self.strategy_data.slow_window, signal_window=self.strategy_data.signal_window)
        self.entries = macd_res.macd > macd_res.signal
        self.exits = macd_res.macd < macd_res.signal

class Momentum(TradeStrategy):
    ### STRAT DATA ###
    # num_days
    ##################
    def populate_signals(self):
        momentum = self.price_data / self.price_data.shift(self.strategy_data.num_days) - 1
        self.entries = momentum > 0
        self.exits = momentum < 0

class Testing(TradeStrategy):
    def populate_signals(self):
        short_ema = vbt.MA.run(data, 10, short_name='fast', ewm=True)
        long_ema = vbt.MA.run(data, 20, short_name='slow', ewm=True)
        self.entries = short_ema.ma_crossed_above(long_ema)
        self.exits = short_ema.ma_crossed_below(long_ema)
        # return super().populate_signals()


def run_backtest(strategy:TradeStrategy, ticker:str, start_date:datetime.date, end_date:datetime.date, size:int, size_type:str, init_equity:int, fees:int, direction:str):
    # Fetch data
    data = vbt.YFData.download(ticker, start=convert_tz(start_date), end=convert_tz(end_date)).get('Close')

    # Calculate from strategy
    # TODO: Make this run with multiple strategies
    strategy.populate_signals()
    entries, exits = strategy.get_signals()
    # short_ema = vbt.MA.run(data, 10, short_name='fast', ewm=True)
    # long_ema = vbt.MA.run(data, 20, short_name='slow', ewm=True)
    # entries = short_ema.ma_crossed_above(long_ema)
    # exits = short_ema.ma_crossed_below(long_ema)

    # Run portfolio
    pf = vbt.Portfolio.from_signals(
        data, entries, exits,
        direction = direction.lower().replace(" ", ""),
        size = prep_size(size, size_type),
        size_type = size_type.lower(),
        fees = (fees/100),
        init_cash = init_equity,
        freq = '1D',
        min_size = 1,
        size_granularity = 1
    )
    return pf