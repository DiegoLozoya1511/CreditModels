import numpy as np
import pandas as pd
from scipy.stats import norm

from financials import FinancialDataFetcher

class Altman(FinancialDataFetcher):
    def __init__(self, ticker: str):
        super().__init__(ticker)
        self.bs = self.bs.iloc[:, :2]
        self.ist = self.ist.iloc[:, :2]
        
    def liquidity_ratio(self) -> float:
        """
        Calculates the liquidity ratio (working capital / total assets).
        
        Returns:
            float: The liquidity ratio.
        """
        working_capital = self.current_assets() - self.current_liabilities()
        return working_capital / self.total_assets()
    
    def cumulative_profitability_ratio(self) -> float:
        """
        Calculates the cumulative profitability ratio (retained earnings / total assets).
        
        Returns:
            float: The cumulative profitability ratio.
        """
        return self.retained_earnings() / self.total_assets()
    
    def operating_efficiency_ratio(self) -> float:
        """
        Calculates the operating efficiency ratio (EBIT / total assets).
        
        Returns:
            float: The operating efficiency ratio.
        """
        return self.EBIT() / self.total_assets()
    
    def leverage_ratio(self) -> float:
        """
        Calculates the leverage ratio (book value of equity / total liabilities).
        
        Returns:
            float: The leverage ratio.
        """
        return self.BV_Equity() / self.total_liabilities()
    
    def asset_turnover_ratio(self) -> float:
        """
        Calculates the asset turnover ratio (sales / total assets).
        
        Returns:
            float: The asset turnover ratio.
        """
        return self.sales() / self.total_assets()
    
    def get_ratio_components(self) -> dict:
        """
        Returns all five Altman Z-Score component ratios.
        
        Returns:
            dict: Dictionary with ratio names as keys and values as floats.
        """
        return [self.liquidity_ratio(), self.cumulative_profitability_ratio(), self.operating_efficiency_ratio(),
                self.leverage_ratio(), self.asset_turnover_ratio()]
    
    def altman_z_score(self) -> float:
        """
        Calculates the Altman Z-score for bankruptcy prediction.
        X1-X4 are expressed as absolute percentages (e.g., 0.10 -> 10.0)
        X5 is expressed as a decimal ratio (e.g., 2.0 for 200%)
        
        Returns:
            float: The Altman Z-score.
        """
        X1 = self.liquidity_ratio() * 100
        X2 = self.cumulative_profitability_ratio() * 100
        X3 = self.operating_efficiency_ratio() * 100
        X4 = self.leverage_ratio() * 100
        X5 = self.asset_turnover_ratio()

        Z = 0.012 * X1 + 0.014 * X2 + 0.033 * X3 + 0.006 * X4 + 0.999 * X5
        return Z
    

class Merton(FinancialDataFetcher):
    def __init__(self, ticker: str, T: float = 1.0):
        super().__init__(ticker)
        self.T = T
    
    def liability_threshold(self) -> float:
        """
        Calculate the default point L = Current Liabilities + 0.5 x Long-term Debt
        
        Returns:
            float: The default point L.
        """
        current_liabilities = self.current_liabilities()[0]
        total_liabilities = self.total_liabilities()[0]
        
        # Long-term debt = Total - Current
        long_term_liabilities = total_liabilities - current_liabilities
        
        # Threshold
        L = current_liabilities + 0.5 * long_term_liabilities
        return L
    
    def asset_volatility(self) -> float:
        """
        Calculates annualized volatility of asset log returns.
        Assumes annual financial statement data.
        
        Returns:
            float: Annualized asset volatility.
        """
        assets = pd.Series(self.total_assets())
        assets = pd.to_numeric(assets, errors='coerce')
        
        log_returns = np.log(assets / assets.shift(1)).dropna() # Lognormal distribution assumption
        
        sigma_A = log_returns.std()
        return sigma_A

    def expected_asset_return(self) -> float:
        """
        Calculates the expected return of assets as the mean of log returns.
        
        Returns:
            float: Expected return of assets.
        """        
        assets = pd.Series(self.total_assets())
        assets = pd.to_numeric(assets, errors='coerce')
        
        log_returns = np.log(assets / assets.shift(1)).dropna() # Lognormal distribution assumption
        
        return log_returns.mean() 
    
    def distance_to_default(self) -> float:
        """
        Calculates distance to default (DD).
        
        Returns:
            float: Distance to default.
        """
        A = self.total_assets()[0]
        L = self.liability_threshold()
        mu = self.expected_asset_return()
        sigma = self.asset_volatility()
        T = self.T
        
        # Merton DD formula
        numerator = np.log(A/L) + (mu - 0.5 * sigma**2) * T
        denominator = sigma * np.sqrt(T)
        
        DD = numerator / denominator
        return DD
    
    def default_probability(self) -> float:
        """
        Calculates default probability (PD) from distance to default.
        
        Returns:
            float: Default probability.
        """
        DD = self.distance_to_default()
        PD = 1 - norm.cdf(DD)
        return PD