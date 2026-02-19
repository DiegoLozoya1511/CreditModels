import yfinance as yf
import pandas as pd


class FinancialDataFetcher:
    def __init__(self, ticker: str):
        self.ticker = ticker
        self.bs = None
        self.ist = None
        self.get_financials()

    def get_financials(self) -> tuple[pd.DataFrame, pd.DataFrame]:
        """
        Fetches the balance sheet and income statement for the ticker
        stored in self.ticker.

        Returns:
            tuple[pd.DataFrame, pd.DataFrame]: Balance sheet and income statement.
        """
        stock = yf.Ticker(self.ticker)
        self.bs = stock.balance_sheet.iloc[:, :-1]
        self.ist = stock.income_stmt.iloc[:, :-1]
        return self.bs, self.ist

    def total_assets(self) -> float:
        """
        Calculates the total assets from the balance sheet.

        Returns:
            float: The total assets.
        """
        return self.bs.loc['Total Assets'].values

    def total_liabilities(self) -> float:
        """
        Calculates the total liabilities from the balance sheet.

        Returns:
            float: The total liabilities.
        """
        return self.bs.loc['Total Liabilities Net Minority Interest'].values

    def current_assets(self) -> float:
        """
        Calculates the current assets from the balance sheet.

        Returns:
            float: The current assets.
        """
        return self.bs.loc['Current Assets'].values

    def current_liabilities(self) -> float:
        """
        Calculates the current liabilities from the balance sheet.

        Returns:
            float: The current liabilities.
        """
        return self.bs.loc['Current Liabilities'].values

    def retained_earnings(self) -> float:
        """
        Calculates the retained earnings from the balance sheet.

        Returns:
            float: The retained earnings.
        """
        return self.bs.loc['Retained Earnings'].values

    def EBIT(self) -> float:
        """
        Calculates the Earnings Before Interest and Taxes (EBIT) from the income statement.

        Returns:
            float: The EBIT.
        """
        return self.ist.loc['EBIT'].values

    def BV_Equity(self) -> float:
        """
        Calculates the book value of equity from the balance sheet.

        Returns:
            float: The book value of equity.
        """
        return self.bs.loc['Stockholders Equity'].values

    def sales(self) -> float:
        """
        Calculates the total sales from the income statement.

        Returns:
            float: The total sales.
        """
        return self.ist.loc['Total Revenue'].values
