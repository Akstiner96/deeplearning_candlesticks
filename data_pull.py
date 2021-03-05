#importing the necessary libraries
import numpy as np
import pandas as pd
import warnings
import os
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from alpha_vantage.timeseries import TimeSeries
import requests
import time

def load():
    #load dotenv in to call api keys with
    load_dotenv()

     #Load Alpaca keys
    #warnings.warn('Make sure your api keys are renamed to fit this function or alter the function to fit your names')
    alpaca_public = os.getenv('ALPACA_API_KEY')
    alpaca_secret = os.getenv('ALPACA_SECRET_KEY')
    api = tradeapi.REST(alpaca_public, alpaca_secret, base_url='https://paper-api.alpaca.markets')

    return api
    
def data_pull(api):
    assets = api.list_assets()
    tick_list = []
    tickers = ['EYES', 'SOS', 'SLGG', 'AMTX', 'KMPH', 'OCGN', 'BPTH']
    
    i = 0
    for ticker in tickers: 
        try:
            df = api.alpha_vantage.historic_quotes(ticker, adjusted=True, output_format='pandas')
            
            df.columns = [f"{ticker} Open",
                          f"{ticker} High",
                          f"{ticker} Low",
                          f"{ticker} Close",
                          f"{ticker} Adjusted Close",
                          f"{ticker} Volume",
                          f"{ticker} Dividend Amount",
                          f"{ticker} Split Coefficient"]
            tick_list.append(df)
            i += 1
            if i % 5 == 0:
                time.sleep(60)
            
        except:
            if ticker in assets:
                raise Exception('The ticker name is right, but AlphaVantage cannot pull its data, make sure the asset is tradeable')
            else:
                raise Exception('That is not a proper ticker symbol')
        
    data = pd.concat(tick_list, axis='columns', join='inner')
    return data



def data_clean(data):
    
    #drop unnecessary data
    data.drop([col for col in data.columns if 'Adjusted' in col], axis=1, inplace=True)
    data.drop([col for col in data.columns if 'Dividend' in col], axis=1, inplace=True)
    data.drop([col for col in data.columns if 'Split' in col], axis=1, inplace=True)
    #data.drop([col for col in data.columns if 'High' in col], axis=1, inplace=True)
    #data.drop([col for col in data.columns if 'Low' in col], axis=1, inplace=True)
    
    return data

api = load()
data = data_pull(api)
cleaned = data_clean(data)