import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import numba as nb
import pandas_ta 
import os
import datetime
import json
from tabulate import tabulate
import sys
sys.path.append('../..')
import vectorbtpro as vbt
from vectorbtpro.portfolio.enums import SizeType
from src.utils import fu
from src.utils import plot_return_mdd
from src.strategy.BackTester import BackTester
from src.strategy.Analyzer import Analyzer
from src.strategy.PositionSizer import PositionSizer
from src.strategy.MultiTester import MultiTester
from src.utils import plot_return_mdd,twinx_plot # as utils
import json
config_f = open('..\configs\config.json')
config = json.load(config_f)# %%

def get_data(coin):
    pair = f'{coin}USDT'
    df = pd.read_hdf(r'{}\price_data\binance\1m\{}_PERPETUAL.h5'.format(config['DATA_PATH'],pair))
    return df

class Strategy(BackTester):

    def __init__(self, df, configs, **kwargs):
        super().__init__(**kwargs)
        self.configs = configs
        self.freq = self.configs['freq']
        self.fee = self.configs['fee']
        self.df = self.resample_df(df=df, freq=self.freq)
        self._strategy_setting()
        self.indicator = pd.DataFrame()
    
    def get_data(coin):
        pair = f'{coin}USDT'
        df = pd.read_hdf(r'X:\price_data\binance\1m\{}_PERPETUAL.h5'.format(pair))
        # oi_df = pd.read_csv(r'Z:\binance_zip\futures\um\metrics\{}_metrics.csv'.format(pair))
        # oi_df.index = pd.to_datetime(oi_df['create_time'],format='ISO8601') # type: ignore
        # df['sum_open_interest'] = oi_df['sum_open_interest']
        return df
    
    def resample_df(self,df,freq = '1h'):
        cols = ['open', 'high', 'low', 'close','volume']
        agg =  ['first','max',  'min', 'last', 'sum']

        df = df[cols]
        df = df.resample(freq).agg(dict(zip(cols,agg)))
        return df.dropna()
    
    def _strategy(self, df, side='both', **params):
        
        # params
        window = int(params['window'])
        crit_entry = params['crit_entry']
        crit_exit = params['crit_exit']
        N = params['N']
        
        df['weekday'] = df.index.weekday+1
        bias = (df['close'] - df['close'].rolling(window).mean())
        bias_ma = bias.rolling(window).mean()
        bias_std = bias.rolling(window).std()
        
        freq_sec = pd.Timedelta(self.freq).seconds
        
        window_1d = int(86400/freq_sec)
        window_Nd = int(window_1d*N)

        rolling_high = df['high'].rolling(window_1d).max()
        rolling_low = df['low'].rolling(window_1d).min()
        rolling_HL_rate = (rolling_high/rolling_low-1)*100
        rolling_HL_rate_ma = rolling_HL_rate.rolling(window_Nd).mean()

        # 進場
        long_entry = (bias > bias_ma + crit_entry * bias_std) & (df['weekday'].isin([1,2,3,4,5])) & (rolling_HL_rate > rolling_HL_rate_ma)
        long_exit =  (bias < bias_ma - crit_exit * bias_std)
        
        # 出場
        short_entry = (bias < bias_ma - crit_entry * bias_std) & (df['weekday'].isin([1,2,3,4,5])) & (rolling_HL_rate > rolling_HL_rate_ma)
        short_exit =  (bias > bias_ma + crit_exit * bias_std)
        
        if crit_entry < crit_exit :
            long_entry, long_exit, short_entry, short_exit = False,False,False,False

        if side == 'long':
            short_entry = False
            short_exit = False

        elif side == 'short':
            long_entry = False
            long_exit = False

        price = df['open'].shift(-self.lag)
        pf = vbt.Portfolio.from_signals(price, # type: ignore
                                        open = df['open'],
                                        high = df['high'],
                                        low  = df['low'],
                                        entries=long_entry,
                                        exits=long_exit,
                                        short_entries=short_entry,
                                        short_exits=short_exit,
                                        sl_stop= np.nan/100,
                                        upon_opposite_entry='reverse'
                                        )
        return pf, params