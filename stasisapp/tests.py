from django.test import TestCase
from .models import Security
from datetime import date

class SecurityModelTest(TestCase):

    def setUp(self):
        self.security = Security.objects.create(
            ticker="AAPL",
            name="Apple Inc.",
            description="Apple Inc. is a technology giant renowned for its innovative hardware, software, and services, including the iPhone, Mac, and iOS ecosystem.",
            industry="Consumer Electronics",
            sector="Technology",
            djia=True,
            sp500=True,
            stock_price=178.39,
            net_income=19881000000.0,
            revenues=81797000000.0,
            profit_margin=24.305292370135824,
            total_liabilities=274764000000.0,
            total_equity=60274000000.0,
            debt_to_equity_ratio=4.558582473371603,
            basic_eps=1.27,
            diluted_eps=1.26,
            free_cash_flow=2769000000.0,
            sales_per_share=4.11433026507721,
            market_capitalization=733.9553759871234,
            dividend_yield=0.0,
            pe_ratio=3.6917427492939154e-8,
            ps_ratio=8.972888687691766e-9,
            dividend_yield_date=date(2023, 9, 20)
        )

    def test_security_creation(self):
        self.assertEqual(self.security.ticker, "AAPL")
        self.assertEqual(self.security.name, "Apple Inc.")
        self.assertEqual(self.security.description, "Apple Inc. is a technology giant renowned for its innovative hardware, software, and services, including the iPhone, Mac, and iOS ecosystem.")
        self.assertEqual(self.security.industry, "Consumer Electronics")
        self.assertEqual(self.security.sector, "Technology")
        self.assertTrue(self.security.djia)
        self.assertTrue(self.security.sp500)
        self.assertEqual(self.security.stock_price, 178.39)
        self.assertEqual(self.security.net_income, 19881000000.0)
        self.assertEqual(self.security.revenues, 81797000000.0)
        self.assertEqual(self.security.profit_margin, 24.305292370135824)
        self.assertEqual(self.security.total_liabilities, 274764000000.0)
        self.assertEqual(self.security.total_equity, 60274000000.0)
        self.assertEqual(self.security.debt_to_equity_ratio, 4.558582473371603)
        self.assertEqual(self.security.basic_eps, 1.27)
        self.assertEqual(self.security.diluted_eps, 1.26)
        self.assertEqual(self.security.free_cash_flow, 2769000000.0)
        self.assertEqual(self.security.sales_per_share, 4.11433026507721)
        self.assertEqual(self.security.market_capitalization, 733.9553759871234)
        self.assertEqual(self.security.dividend_yield, 0.0)
        self.assertEqual(self.security.pe_ratio, 3.6917427492939154e-8)
        self.assertEqual(self.security.ps_ratio, 8.972888687691766e-9)
        self.assertEqual(self.security.dividend_yield_date, date(2023, 9, 20))

    def test_security_str_method(self):
        self.assertEqual(str(self.security), "Apple Inc.")
