from django.db import models

# security/models.py
from django.db import models

class Security(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField()
    industry = models.CharField(max_length=50)
    sector = models.CharField(max_length=50)
    djia = models.BooleanField()
    sp500 = models.BooleanField()
    stock_price = models.FloatField()
    net_income = models.FloatField()
    revenues = models.FloatField()
    profit_margin = models.FloatField()
    total_liabilities = models.FloatField()
    total_equity = models.FloatField()
    debt_to_equity_ratio = models.FloatField()
    basic_eps = models.FloatField()
    diluted_eps = models.FloatField()
    free_cash_flow = models.FloatField()
    sales_per_share = models.FloatField()
    market_capitalization = models.FloatField()
    dividend_yield = models.FloatField()
    pe_ratio = models.FloatField()
    ps_ratio = models.FloatField()
    dividend_yield_date = models.DateField()

    def __str__(self):
        return self.name
