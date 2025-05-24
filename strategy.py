import vectorbt as vbt
from util import prep_size


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
        fast_ema = vbt.MA.run(self.price_data, window=self.strategy_data['fast_ema_window'], ewm=True).ma
        slow_ema = vbt.MA.run(self.price_data, window=self.strategy_data['slow_ema_window'], ewm=True).ma
        self.entries = fast_ema > slow_ema
        self.exits = fast_ema < slow_ema


class RSIMeanReversion(TradeStrategy):
    ### STRAT DATA ###
    # rsi_window
    # oversold_threshold
    # overbought_threshold
    ##################
    def populate_signals(self):
        rsi = vbt.RSI.run(self.price_data, window=self.strategy_data['rsi_window']).rsi
        self.entries = rsi < self.strategy_data['oversold_threshold']
        self.exits = rsi > self.strategy_data['overbought_threshold']


class BBandsBreakout(TradeStrategy):
    ### STRAT DATA ###
    # bb_window
    # alpha
    # middle_band_type
    ##################
    def populate_signals(self):
        self.bb = vbt.BBANDS.run(
            self.price_data,
            window=self.strategy_data['bb_window'],
            alpha=self.strategy_data['alpha'],
            ewm=(self.strategy_data['middle_band_type'] == "EMA")
        )
        self.entries = self.price_data < self.bb.lower
        self.exits = self.price_data > self.bb.upper

    def plot(index, bbands):
        bbands = bbands.loc[index]
        fig = vbt.make_subplots(
            rows=2, cols=1, shared_xaxes=True, vertical_spacing=0.15,
            subplot_titles=('%B', 'Bandwidth'))
        fig.update_layout(template='vbt_dark', showlegend=False, width=750, height=400)
        bbands.percent_b.vbt.ts_heatmap(
            trace_kwargs=dict(zmin=0, zmid=0.5, zmax=1, colorscale='Spectral', colorbar=dict(
                y=(fig.layout.yaxis.domain[0] + fig.layout.yaxis.domain[1]) / 2, len=0.5
            )), add_trace_kwargs=dict(row=1, col=1), fig=fig)
        bbands.bandwidth.vbt.ts_heatmap(
            trace_kwargs=dict(colorbar=dict(
                y=(fig.layout.yaxis2.domain[0] + fig.layout.yaxis2.domain[1]) / 2, len=0.5
            )), add_trace_kwargs=dict(row=2, col=1), fig=fig)
        return fig
    
    def bbands_plot(self):
        # TODO: Implement generically
        price = vbt.YFData.download("AAPL", period='6mo', missing_index='drop').get('Close')
        bbands = vbt.BBANDS.run(price)
        vbt.save_animation('bbands.gif', bbands.wrapper.index, BBandsBreakout.plot, bbands, delta=90, step=3, fps=3)


class MACDCrossover(TradeStrategy):
    ### STRAT DATA ###
    # fast_window
    # slow_window
    # signal_window
    ##################
    def populate_signals(self):
        macd_res = vbt.MACD.run(
            self.price_data,
            fast_window=self.strategy_data['fast_window'],
            slow_window=self.strategy_data['slow_window'],
            signal_window=self.strategy_data['signal_window']
        )
        self.entries = macd_res.macd > macd_res.signal
        self.exits = macd_res.macd < macd_res.signal


class Momentum(TradeStrategy):
    ### STRAT DATA ###
    # num_days
    ##################
    def populate_signals(self):
        momentum = self.price_data / (self.price_data.shift(self.strategy_data['num_days']) - 1)
        self.entries = (momentum > 0) & (momentum.shift(1) <= 0)
        self.exits = (momentum < 0) & (momentum.shift(1) >= 0)


def run_backtest(strategy:TradeStrategy, size:int, size_type:str, init_equity:int, fees:int, direction:str):
    # Calculate from strategy
    strategy.populate_signals()
    entries, exits = strategy.get_signals()

    # Ensure position closed on final timestamp
    exits.iloc[-1] = True

    # Run portfolio
    pf = vbt.Portfolio.from_signals(
        strategy.price_data, entries, exits,
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
