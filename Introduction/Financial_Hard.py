import numpy as np

class Calculator:
    def __init__(self, number1, number2):
        self.number1 = number1
        self.number2 = number2
        
    def sum(self):
        return self.number1 + self.number2
    
    def substract(self):
        return self.number1 - self.number2
    
    def multiply(self):
        return self.number1 * self.number2
    
    def divide(self):
        if self.number2 == 0:
            return "Error: Division by zero"
        return self.number1 / self.number2
    

class FinancialCalculator(Calculator):
    def __init__(self, principal, rate, time):
        super().__init__(principal, rate)
        self.principal = principal
        self.rate = rate
        self.time = time
        
    def simple_interest(self):
        return (self.principal * self.rate * self.time) / 100
    
    def compound_interest(self, n):
        return self.principal * (1 + (self.rate / (n)))**(n * self.time)
    
    def future_value(self):
        return self.principal * np.exp(self.rate * self.time / 100)
    
    def present_value(self, future_value):
        return future_value * np.exp(-self.rate * self.time / 100)
    

class BondCalculator(FinancialCalculator):
    def __init__(self, face_value, coupon_rate, market_rate, years_to_maturity):
        super().__init__(face_value, coupon_rate, years_to_maturity)
        self.face_value = face_value
        self.coupon_rate = coupon_rate
        self.market_rate = market_rate
        self.years_to_maturity = years_to_maturity
        
    def bond_price(self):
        coupon_payment = self.face_value * (self.coupon_rate / 100)
        price = 0
        for t in range(1, self.years_to_maturity + 1):
            price += coupon_payment / (1 + self.market_rate / 100)**t
        price += self.face_value / (1 + self.market_rate / 100)**self.years_to_maturity
        return price
    
    def duration(self):
        coupon_payment = self.face_value * (self.coupon_rate / 100)
        price = self.bond_price()
        duration = 0
        for t in range(1, self.years_to_maturity + 1):
            duration += t * (coupon_payment / (1 + self.market_rate / 100)**t) / price
        duration += self.years_to_maturity * (self.face_value / (1 + self.market_rate / 100)**self.years_to_maturity) / price
        return duration
    
    def modified_duration(self):
        duration = self.duration()
        return duration / (1 + self.market_rate / 100)
    
    
# Example usage:
bond_calc = BondCalculator(face_value=1000, coupon_rate=5, market_rate=4, years_to_maturity=10)

print(f"Bond Price: {bond_calc.bond_price():.2f}")
print(f"Duration: {bond_calc.duration():.2f}")
print(f"Modified Duration: {bond_calc.modified_duration():.2f}")
        