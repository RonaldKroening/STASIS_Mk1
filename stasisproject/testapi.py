import requests

def get_stock_data(api_key, ticker):
    base_url = "https://www.alphavantage.co/query"
    
    # Function to get company overview
    def get_company_overview(api_key, ticker):
        params = {
            "function": "OVERVIEW",
            "symbol": ticker,
            "apikey": api_key
        }
        response = requests.get(base_url, params=params)
        return response.json()

    # Function to get stock quote
    def get_stock_quote(api_key, ticker):
        params = {
            "function": "GLOBAL_QUOTE",
            "symbol": ticker,
            "apikey": api_key
        }
        response = requests.get(base_url, params=params)
        return response.json()

    overview = get_company_overview(api_key, ticker)
    quote = get_stock_quote(api_key, ticker)["Global Quote"]

    data = {
        "TCKR": ticker,
        "NAME": overview.get("Name", "N/A"),
        "DESC": overview.get("Description", "N/A"),
        "INDUSTRY": overview.get("Industry", "N/A"),
        "SECTOR": overview.get("Sector", "N/A"),
        "DJIA": {"$numberInt": "1" if ticker == "AAPL" else "0"},  # Assuming AAPL is in DJIA
        "SP500": {"$numberInt": "1" if ticker == "AAPL" else "0"},  # Assuming AAPL is in S&P 500
        "marketItems": {
            "Stock Price": {"$numberDouble": quote.get("05. price", "N/A")},
            "Net Income": {"$numberDouble": overview.get("NetIncomeTTM", "N/A")},
            "Revenues": {"$numberDouble": overview.get("RevenueTTM", "N/A")},
            "Profit Margin": {"$numberDouble": overview.get("ProfitMargin", "N/A")},
            "Total Liabilities": {"$numberDouble": overview.get("TotalLiabilities", "N/A")},
            "Total Equity": {"$numberDouble": overview.get("TotalShareholderEquity", "N/A")},
            "Debt-to-Equity Ratio": {"$numberDouble": overview.get("DebtEquityRatio", "N/A")},
            "Basic EPS": {"$numberDouble": overview.get("EPS", "N/A")},
            "Diluted EPS": {"$numberDouble": overview.get("DilutedEPS", "N/A")},
            "Free Cash Flow": {"$numberDouble": overview.get("FreeCashFlowTTM", "N/A")},
            "Sales per Share": {"$numberDouble": overview.get("RevenuePerShareTTM", "N/A")},
            "Market Capitalization": {"$numberDouble": overview.get("MarketCapitalization", "N/A")},
            "Dividend Yield": {"$numberDouble": overview.get("DividendYield", "N/A")},
            "P/E Ratio": {"$numberDouble": overview.get("PERatio", "N/A")},
            "P/S Ratio": {"$numberDouble": overview.get("PriceToSalesRatioTTM", "N/A")},
        },
        "dividend_yield": f"{overview.get('DividendYield', 'N/A')} @ {overview.get('DividendDate', 'N/A')}"
    }

    return data

# Usage
api_key = "ROFX6T3DF0LVOPUZ"
ticker = "AAPL"
stock_data = get_stock_data(api_key, ticker)
print(stock_data)
print(stock_data.keys())