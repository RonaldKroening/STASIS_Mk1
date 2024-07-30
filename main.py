import django
import json
import requests
import os
import datetime
import pandas as pd
import pymongo
import time
import tensorflow as tf
import json
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
import datetime


api_key = ""

# https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol=IBM&outputsize=full&apikey=api_key
password = ""
def get_client():
    
    uri = "mongodb+srv://ronald_kroening_64:"+password+"@cluster0.0qo2iwi.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    uri = "mongodb+srv://ronald_kroening_64:{password}@cluster0.0qo2iwi.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp"
    client = pymongo.MongoClient(uri)
    return client
from pymongo.mongo_client import MongoClient
uri = ""
print(uri)
# Create a new client and connect to the server
client = MongoClient(uri)
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
def get_valid_tickers():
    client = get_client()
    dataset = client['FinancialData']['MetaData']
    kvp = {}
    for data in dataset.find():
        name = data['NAME']
        tkr = data['TCKR']
        kvp[name] = tkr
    return kvp
        


def load_markets():
    client = get_client()
    dataset = client['FinancialData']['Markets']
    K = {}
    for market in dataset.find():
        for data in market:
            K[data]
        
    
def add_stock_info(asJson):
    client = get_client()
    dataset = client['FinancialData']['MetaData']
    R = dataset.insert_one(asJson)

def add_timeseries(ticker):
    client = get_client()
    dataset = client['FinancialData']['AllStocks']
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol="+ticker+"&outputsize=full&apikey="+api_key
    r = requests.get(url)
    data = r.json()
    if 'timestamp' in data:
        data['timestamp'] = datetime.strptime(data['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    result = dataset.insert_one(data)
    return data

def Model():
    model = Sequential()
    model.add(LSTM(50, return_sequences=True, input_shape=(90, 5))) 
    model.add(LSTM(25, return_sequences=True))
    model.add(Dense(1))  # Output layer for predicting volatility.
    return model


# apikey= str(os.environ.get('apikey'))

#poly: https://api.polygon.io/vX/reference/financials?ticker="+ticker+"&filing_date="+currDate+"&apiKey="+apikey

def get_last(ticker):
    client = get_client()['FinancialData']
    MD =  client['MetaData']
    STOCKS = client['AllStocks']
    data = None
    for item in STOCKS.find():
        if(ticker == item['Meta Data']['2. Symbol']):
            data = item['Time Series (Daily)']
    if(data == None):
        time.sleep(2)
        d = add_timeseries(ticker)
        data = d
    return data[list(data.keys())[0]]

# Get the current year

def get_dividend(ticker):
    MD =  get_client()['FinancialData']['MetaData']
    div = None
    for item in MD.find():
        if(item['TCKR'] == ticker):
            mustRun = False
            if("dividend_yield" in item):
                try:
                    lastDate = datetime.datetime.strptime(item["dividend_yield"][1].split(" @ ")[1], "%Y-%m-%d")
                    current_date = datetime.datetime.strptime(str(datetime.date.today()), last_date_format)
                    time_difference = (current_date - lastDate).days
                    if(time_difference > 30):
                        mustRun = True
                    else:
                        div = item["dividend_yield"].split(" @ ")[0]
                except:
                    i=1
            if("dividend_yield" not in item or mustRun):
                url = f"https://api.polygon.io/v3/reference/dividends?ticker={ticker}&apiKey={api_key}"

                r = requests.get(url)
                data = r.json()['results']
                # print(data)
                div = float(data[0]["cash_amount"])
                ct = 0
                last_payment = data[0]
                last_date_str = last_payment["declaration_date"]
                last_date_format = "%Y-%m-%d"  # Specify the format of the date string
                last_date = datetime.datetime.strptime(last_date_str, last_date_format)

                frequency = last_payment["frequency"]
                threshold_days = 30 * (12 / frequency)

                current_date = datetime.datetime.strptime(str(datetime.date.today()), last_date_format)
                time_difference = (current_date - last_date).days

                if time_difference <= threshold_days:
                    div = last_payment["cash_amount"]*last_payment["frequency"]
                    
                MD.update_one({'TCKR': ticker}, {'$set': {'dividend_yield': str(str(div)+" @ "+str(datetime.date.today()))}})
            break
    if(div == None):
        url = f"https://api.polygon.io/v3/reference/dividends?ticker={ticker}&apiKey={api_key}"

        r = requests.get(url)
        print(r)
        data = r.json()['results']
                # print(data)
        div = float(data[0]["cash_amount"])
        ct = 0
        last_payment = data[0]
        last_date_str = last_payment["declaration_date"]
        last_date_format = "%Y-%m-%d"  # Specify the format of the date string
        last_date = datetime.datetime.strptime(last_date_str, last_date_format)

        frequency = last_payment["frequency"]
        threshold_days = 30 * (12 / frequency)

        current_date = datetime.datetime.strptime(str(datetime.date.today()), last_date_format)
        time_difference = (current_date - last_date).days

        if time_difference <= threshold_days:
            div = last_payment["cash_amount"]*last_payment["frequency"]
                    
        MD.update_one({'TCKR': ticker}, {'$set': {'dividend_yield': str(str(div)+" @ "+str(datetime.date.today()))}})
    return div

def process_market_items(data):
    print(data)
    ticker = data['results'][0]['tickers'][0]
    GL = get_last(ticker)
    stock_price = float(GL["4. close"])
    volume = float(GL["5. volume"])
    financial_data = {}
    financial_data["income_statement"] = data['results'][1]['financials']["income_statement"]
    financial_data["balance_sheet"] = data['results'][0]['financials']["balance_sheet"]
    financial_data["cash_flow_statement"] = data['results'][1]['financials']["cash_flow_statement"]
    dividend = get_dividend(ticker)
    if(type(dividend) != type(0.0)):
        dividend = 0.0
    stock_price = get_stock_price(ticker)
    
    metrics = {
        "Stock Price":stock_price,
        "Net Income": financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'],
        "Revenues": financial_data['income_statement']['revenues']['value'],
        "Profit Margin": (financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] / financial_data['income_statement']['revenues']['value']) * 100,
        "Total Liabilities": financial_data['balance_sheet']['liabilities']['value'],
        "Total Equity": financial_data['balance_sheet']['equity']['value'],
        "Debt-to-Equity Ratio": financial_data['balance_sheet']['liabilities']['value'] / financial_data['balance_sheet']['equity']['value'] if financial_data['balance_sheet']['equity']['value'] != 0 else None,
        "Basic EPS": financial_data['income_statement']['basic_earnings_per_share']['value'],
        "Diluted EPS": financial_data['income_statement']['diluted_earnings_per_share']['value'],
        "Free Cash Flow": financial_data['cash_flow_statement']['net_cash_flow']['value'],
        "Sales per Share": financial_data['income_statement']['revenues']['value'] / financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] if financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] != 0 else None,
        "Market Capitalization": stock_price * (financial_data['income_statement']['revenues']['value'] / financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] if financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] != 0 else None),
        "Dividend Yield": (dividend / stock_price) * 100 if stock_price != 0 else 0,
        "P/E Ratio": stock_price / (financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] / financial_data['income_statement']['revenues']['value']) if financial_data['income_statement']['revenues']['value'] != 0 else None,
        "P/S Ratio": stock_price / (financial_data['income_statement']['revenues']['value'] / financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value']) if financial_data['income_statement']['net_income_loss_available_to_common_stockholders_basic']['value'] != 0 else None,
    }



    if metrics["Net Income"] is not None and metrics["Net Income"] != 0:
        metrics["P/E Ratio"] = metrics["Market Capitalization"] / metrics["Net Income"]

    # Calculate Sales per Share and P/S Ratio
    if metrics["Revenues"] is not None and metrics["Revenues"] != 0:
        metrics["Sales per Share"] = metrics["Revenues"] / metrics["Net Income"]
        metrics["P/S Ratio"] = metrics["Market Capitalization"] / metrics["Revenues"]

    return metrics





def get_stock_price(ticker):
    client = get_client()['FinancialData']
    MD =  client['MetaData']
    STOCKS = client['AllStocks']
    price = None
    
    for item in STOCKS.find():
        if(ticker == item['Meta Data']['2. Symbol']):
            time_series = item['Time Series (Daily)']
            g = get_last(ticker)
            price = float(g["4. close"])
    data = add_timeseries(ticker)
    
    return float(get_last(ticker)['4. close'])

def get_info(ticker):
    client = get_client()['FinancialData']
    MD =  client['MetaData']
    STOCKS = client['AllStocks']
    data = {}
    for item in STOCKS.find():
        if(ticker == item['Meta Data']['2. Symbol']):
            data['graph'] = item['Time Series (Daily)']
    if('graph' not in data):
        time.sleep(2)
        d = add_timeseries(ticker)
        data['graph'] = d
    
    I = None
    for item in MD.find():
        # print(item['TCKR'])
        if item['TCKR'] == ticker:
            data['Name'] = item['NAME']
            data['Industry'] = item['INDUSTRY']
            data['Sector'] = item['SECTOR']
            data['Desc'] = item['DESC']
            I = item
            data['marketIdx'] = [item['DJIA'], item['SP500']]
            markIdx = data.get('marketItems')  # Use data.get() to safely check if 'marketItems' exists

            if markIdx == None: # If 'marketItems' doesn't exist, fetch the financial data from Polygon.io
                r = requests.get(f"https://api.polygon.io/vX/reference/financials?ticker="+ticker+"&apiKey="+api_key)
                response = r.json()
                markIdx = process_market_items(response) 
                MD.update_one({'TCKR': ticker}, {'$set': {'marketItems': markIdx}})
            data["metrics"] = markIdx
            break
    
        
    return data

    
def given_search(ticker):
    r = search_for_company(ticker)
    if(r == None):
        add_timeseries(ticker)
        time.sleep(2)
        r = search_for_company(ticker)
    data = {
            'graph' : r,
            'name' : "",
            'sector' : "",
            'industry' : "",
            'description' : "",
            'information' : get_market_info(ticker)
        }
    return data

def calculate_volatility(timeSeries):
    model = 3
    return model



def find_volatility(ticker):
    time_series = given_search(ticker)
    return calculate_volatility(time_series)      
     
            




def format_data(DATA, GRAPH):

    header = {
        "name": DATA["name"],
        "desc": DATA["desc"],
        "market": DATA["marketItems"]["Stock Price"]["$numberDouble"],
        "open": "",
        "now": "",
        "change": "",
    }

    table = {
        "mcap": DATA["marketItems"]["Market Capitalization"]["$numberDouble"],
        "pe": DATA["marketItems"]["P/E Ratio"]["$numberDouble"],
        "eps": DATA["marketItems"]["Basic EPS"]["$numberDouble"],
        "dividend": DATA["dividend_yield"],
        "vol": GRAPH["Time Series (Daily)"]["2023-09-19"]["5. volume"],
        "profmar": DATA["marketItems"]["Profit Margin"]["$numberDouble"],
        "d2e": DATA["marketItems"]["Debt-to-Equity Ratio"]["$numberDouble"],
        "ps": DATA["marketItems"]["P/S Ratio"]["$numberDouble"],
        "fcf": DATA["marketItems"]["Free Cash Flow"]["$numberDouble"],
    }

    # Extract open, now, and change from GRAPH data
    graph_data = GRAPH["Time Series (Daily)"]["2023-09-19"]
    header["open"] = graph_data["1. open"]
    header["now"] = graph_data["4. close"]
    graph = GRAPH["Time Series (Daily)"]
    return header, graph
    
#stasisproject venv activate python3 manage.py runserver and python3 main.py