import yfinance as yf
import pandas as pd
import numpy as np
import logging

import torch
import joblib
import os

from sklearn.preprocessing import RobustScaler
from numpy.lib.stride_tricks import as_strided

from .indicators import *

rootDir: str = os.path.dirname(__file__)
logger = logging.getLogger(__name__)

def preprocess(df: pd.DataFrame, addFeatures: list[str] = [], logToFile: bool = True):
    df = df.copy()
    df.reset_index(inplace=True)
    if not pd.api.types.is_datetime64_any_dtype(df['Date']):
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', utc=True)
        
    df['Day'] = df['Date'].dt.weekday
    df['Month'] = df['Date'].dt.month
    df['Year'] = df['Date'].dt.year
    df['Date'] = df['Date'].dt.day
    
    if logToFile:
        logger.info('Added Day, Month, and Year columns and converted Date column to days.')

    if len(addFeatures) > 0:
        if 'rsi' in addFeatures:
            df['rsi'] = relativeStrengthIndex(df)
        if 'ema' in addFeatures:
            df['ema'] = exponentialMovingAverage(df)
        if 'macd' in addFeatures: 
            df['macd'], _ = movingAverageConvergenceDivergence(df)
        if 'signal line' in addFeatures:
            _, df['signal line'] = movingAverageConvergenceDivergence(df)
        if 'fast%k' in addFeatures:
            df['fast%k'], _ = stochasticOscillator(df)
        if 'slow%d' in addFeatures:
            _, df['slow%d'] = stochasticOscillator(df)
            
    if logToFile:
        logger.info(f'Added additional features. {addFeatures}')
    
    return df[30:]

def getInput(
        df: pd.DataFrame,
        features: list[str], 
        logToFile: bool = True
    ):
    
    X = df[features].values
    if logToFile:
        logger.debug(f'Input data shape: {X.shape}')
    return torch.tensor(X, dtype=torch.float)

def STOCK(ticker: str, period: str ='max'):
    return yf.Ticker(ticker).history(period=period)

def loadData(
        ticker: str, 
        saveToFile: str = None, 
        period: str = 'max',
        logToFile: bool = True
    ):

    os.makedirs(os.path.join(rootDir, f'./Models/{saveToFile}_files/Tickers/'), exist_ok=True)
    
    if logToFile:
        logger.info(f'Loading data for {ticker}...')
    
    try:
        df = pd.read_csv(os.path.join(rootDir, f'./Models/{saveToFile}_files/Tickers/{ticker}.csv'))
    except FileNotFoundError:
        if logToFile:
            logger.warning('Ticker data not found. Loading data from yfinance...')
            
        df = STOCK(ticker, period)
        if saveToFile:
            if logToFile:
                logger.info(f'Saving data for {ticker} to {os.path.join(rootDir, f'./Models/{saveToFile}_files/Tickers/{ticker}.csv')}...')
            df.to_csv(os.path.join(rootDir, f'./Models/{saveToFile}_files/Tickers/{ticker}.csv'))
    except Exception as e:
        if logToFile:
            logger.error(f'An error occured while loading data: {e}')
        raise RuntimeError(f"An error occurred while loading data: {e}")
    
    return df

def prepareInput(
        tickers: list[str],
        saveToFile: str = None,
        timeframe: int = 30,
        features: list[str] = [],
        addFeatures: list[str] = [],
        period: str = 'max',
        returnScaler: bool = False,
        loadScaler: str = None,
        logToFile: bool = True,
        debugging: bool = False,
    ):
    
    xFeats = features+addFeatures
    yFeats = ['Open', 'High', 'Low', 'Close', 'Volume']
    
    if logToFile:
        if debugging:
            logger.setLevel(logging.DEBUG)
        else:
            logger.setLevel(logging.INFO)
            
        logger.info('X features: ' + str(xFeats))
        logger.info('Y features: ' + str(yFeats))
    
    df = loadData(tickers[0], saveToFile=saveToFile, period=period, logToFile=logToFile)
    df = preprocess(df, addFeatures, logToFile=logToFile)
    
    if logToFile:
        logger.info(f"Preprocessing {tickers[0]} data...")
    
    dfX = getInput(df, features=xFeats)
    dfY = getInput(df, features=yFeats)
    
    for ticker in tickers[1:]:
        df = loadData(ticker, saveToFile=saveToFile, period=period, logToFile=logToFile)
        df = preprocess(df, addFeatures, logToFile=logToFile)
        
        if logToFile:
            logger.info(f"Preprocessing {ticker} data...")
        
        dfX = torch.cat((dfX, getInput(df, features=features+addFeatures)), dim=0)
        dfY = torch.cat((dfY, getInput(df, features=['Open', 'High', 'Low', 'Close', 'Volume'])), dim=0)
    
    if loadScaler is not None:
        scalerX = joblib.load(os.path.join(rootDir, f'./Models/{loadScaler}_files/Scaler/{loadScaler}_scalerX.pkl')) 
        scalerY = joblib.load(os.path.join(rootDir, f'./Models/{loadScaler}_files/Scaler/{loadScaler}_scalerY.pkl'))
        
        if logToFile:
            logger.info(f"Loading scaler from {os.path.join(rootDir, f'./Models/{loadScaler}_files/Scaler/{loadScaler}_scaler[X/Y].pkl')}...")
        
        df_scaledX = scalerX.transform(dfX)
        df_scaledY = scalerY.transform(dfY)
        
        if logToFile:
            logger.info('Provided Scaler loaded successfully. Data Transformed.')
        
    else:
        try:
            scalerX = joblib.load(os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/{saveToFile}_scalerX.pkl'))
            scalerY = joblib.load(os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/{saveToFile}_scalerY.pkl'))
        except FileNotFoundError:
            if logToFile:
                logger.warning('Existing Scaler not found, initializing new scaler...')
            
            scalerX = RobustScaler()
            scalerY = RobustScaler()
            
            
            df_scaledX = scalerX.fit_transform(dfX)
            df_scaledY = scalerY.fit_transform(dfY)
            
            if logToFile:
                logger.info('New Scaler initialized successfully. Data Transformed.')
            
            if saveToFile:
                os.makedirs(os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/'), exist_ok=True)
                
                joblib.dump(scalerX, os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/{saveToFile}_scalerX.pkl'))
                joblib.dump(scalerY, os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/{saveToFile}_scalerY.pkl'))
                
                if logToFile:
                    logger.info(f"Scaler saved as {os.path.join(rootDir, f'./Models/{saveToFile}_files/Scaler/{saveToFile}_scaler[X/Y].pkl')}")
        else:
            df_scaledX = scalerX.transform(dfX)
            df_scaledY = scalerY.transform(dfY)
            
            if logToFile:
                logger.info('Existing Scaler loaded successfully. Data Transformed.')
        
    dfX = df_scaledX
    dfY = df_scaledY
        
    if len(df) < timeframe:
        if logToFile:
            logger.error('Dataframe has insufficient rows for the specified timeframe.')
        raise ValueError(f"Dataframe has insufficient rows ({len(df)}) for the specified timeframe ({timeframe}).")
    
    X, y = [], []
    
    stride_0, stride_1 = dfX.strides
    num_samples = dfX.shape[0] - timeframe
    X = as_strided(
        dfX,
        shape=(num_samples, timeframe, dfX.shape[1]),
        strides=(stride_0, stride_0, stride_1)
    )
        
    y = dfY[timeframe:]

    X = torch.Tensor(np.array(X, dtype=float))
    y = torch.Tensor(np.array(y, dtype=float))
    
    if logToFile:
        logger.info('Data tensors created successfully.')
    
    if saveToFile and (loadScaler is None):
        os.makedirs(os.path.join(rootDir, f'./Models/{saveToFile}_files/Tensors/'), exist_ok=True)
        
        torch.save(X, os.path.join(rootDir, f'./Models/{saveToFile}_files/Tensors/{saveToFile}_input.pt'))
        torch.save(y, os.path.join(rootDir, f'./Models/{saveToFile}_files/Tensors/{saveToFile}_target.pt'))
        
        if logToFile:
            logger.info(f"Data tensors saved as {os.path.join(rootDir, f'./Models/{saveToFile}_files/Tensors/{saveToFile}_[input/target].pt')}")

    if not returnScaler:
        if logToFile:
            logger.debug('Returning data tensors.')
        return X, y
    else:
        if logToFile:
            logger.debug('Returning data tensors and scalers.')
        return X, y, scalerX, scalerY
