import requests
import pandas as pd

def get_price_data(symbol, count, bin_size="1m"):
    url = "https://www.bitmex.com/api/v1/trade/bucketed"
    params = {
        "binSize": bin_size,
        "partial": "false",
        "symbol": symbol,
        "count": count,
        "reverse": "true"
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        df = pd.DataFrame(data)
        df.set_index("timestamp", inplace=True)
        return df
    else:
        print("Error:", response.status_code)
        return pd.DataFrame()

def apply_strategy(df, crit_entry, crit_exit, side):
    df['weekday'] = pd.to_datetime(df.index).weekday + 1

    # 計算偏差、均值和標準差
    bias = df['close'] - df['close'].rolling(window=20).mean()
    bias_ma = bias.rolling(window=20).mean()
    bias_std = bias.rolling(window=20).std()

    # 計算 High/Low 比率
    rolling_HL_rate = (df['high'] / df['low'] - 1) * 100
    rolling_HL_rate_ma = rolling_HL_rate.rolling(window=20).mean()

    # 進場和出場條件
    long_entry = (bias > bias_ma + crit_entry * bias_std) & df['weekday'].isin([1,2,3,4,5]) & (rolling_HL_rate > rolling_HL_rate_ma)
    long_exit = (bias < bias_ma - crit_exit * bias_std)
    
    short_entry = (bias < bias_ma - crit_entry * bias_std) & df['weekday'].isin([1,2,3,4,5]) & (rolling_HL_rate > rolling_HL_rate_ma)
    short_exit = (bias > bias_ma + crit_exit * bias_std)

    if crit_entry < crit_exit:
        long_entry[:] = False
        long_exit[:] = False
        short_entry[:] = False
        short_exit[:] = False

    if side == 'long':
        short_entry[:] = False
        short_exit[:] = False
    elif side == 'short':
        long_entry[:] = False
        long_exit[:] = False

    # 返回交易信號
    return long_entry, long_exit, short_entry, short_exit

# 獲取數據
df = get_price_data("SOLUSDT", 100)


crit_entry = 1.0
crit_exit = 0.5
side = 'both' 


long_entry, long_exit, short_entry, short_exit = apply_strategy(df, crit_entry, crit_exit, side)


