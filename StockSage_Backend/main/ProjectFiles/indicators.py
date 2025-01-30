import numpy as np

def exponentialMovingAverage(df, days=20):
    """
    Calculate the exponential moving average (EMA) of a stock's closing price.
    
    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the stock's closing price.
    days : int, optional
        The number of days to use for the EMA. Defaults to 20.
    
    Returns
    -------
    list
        The list of EMA values.
    """
    df = df.copy()
    df['EMA'] = df['Close'].ewm(span=days, adjust=False).mean()
            
    return df['EMA'].tolist()


def relativeStrengthIndex(df, days=14):
    """
    Calculate the Relative Strength Index (RSI) of a stock's closing price.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the stock's closing price.
    days : int, optional
        The number of days to use for calculating the RSI. Defaults to 14.

    Returns
    -------
    list
        The list of RSI values.
    """

    df = df.copy()
    
    df['Change'] = df['Close'].diff()
    df['Gain'] = df.Change.mask(df.Change < 0, 0.0)
    df['Loss'] = -df.Change.mask(df.Change > 0, -0.0)
    
    def rma(x, n):
        a = np.full_like(x, np.nan)
        a[n] = x[1:n+1].mean()
        for i in range(n+1, len(x)):
            a[i] = (a[i-1] * (n - 1) + x[i]) / n
        return a

    df['Average Gain'] = rma(df.Gain.to_numpy(), days)
    df['Average Loss'] = rma(df.Loss.to_numpy(), days)

    df['RS'] = df['Average Gain'] / df['Average Loss']
    df['RSI'] = 100 - (100 / (1 + df.RS))
    
    return df['RSI'].tolist()


def movingAverageConvergenceDivergence(df, ema1=12, ema2=26, emaSignal=9):
    """
    Calculate the Moving Average Convergence Divergence (MACD) of a stock's closing price.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the stock's closing price.
    ema1 : int, optional
        The number of days for the shorter EMA. Defaults to 12.
    ema2 : int, optional
        The number of days for the longer EMA. Defaults to 26.
    emaSignal : int, optional
        The number of days for the signal line. Defaults to 9.

    Returns
    -------
    tuple
        A tuple containing the list of MACD values and the list of Signal Line values.
    """
    df = df.copy()
    
    df[f'EMA{ema1}'] = exponentialMovingAverage(df, days=ema1)
    df[f'EMA{ema2}'] = exponentialMovingAverage(df, days=ema2)
    
    df['MACD'] = df[f'EMA{ema1}'] - df[f'EMA{ema2}']
    df['Signal Line'] = exponentialMovingAverage(df, days=emaSignal)
    
    return df['MACD'].tolist(), df['Signal Line'].tolist()

def stochasticOscillator(df, days=14):
    """
    Calculate the Stochastic Oscillator of a stock's closing price.

    Parameters
    ----------
    df : pandas.DataFrame
        The dataframe containing the stock's closing price.
    days : int, optional
        The number of days to use for calculating the Stochastic Oscillator. Defaults to 14.

    Returns
    -------
    tuple
        A tuple containing the list of Fast%K values and the list of Slow%D values.
    """

    df = df.copy()
    
    df[f'{days}DayLow'] = df['Close'].rolling(window=days, min_periods=1).min()
    df[f'{days}DayHigh'] = df['Close'].rolling(window=days, min_periods=1).max()
    
    df['Fast%K'] = 100 * (df['Close'] - df[f'{days}DayLow']) / (df[f'{days}DayHigh'] - df[f'{days}DayLow'])
    df['Slow%D'] = df['Fast%K'].rolling(3).mean()
    
    return df['Fast%K'].tolist(), df['Slow%D'].tolist()