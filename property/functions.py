from typing import List

def calculate_cap_rate(
    value: int, 
    rent: int, 
    annual_property_tax_rate: float=0.0091, 
    monthly_management_fee_rate: float=.01, 
    monthly_maintance_as_rate: float=0.08,
    monthly_insurance: int=136,
    monthly_leasing_fee: int=0,
    monthly_hoa_fee: int=0,
    monthly_utilities: int=0,
    )-> List[int]:
    
    if rent == 0 or value == 0:
        return 0, 0, 0, 0
    annual_gross_income = rent * 12
    mo_maintance = rent * monthly_maintance_as_rate
    mo_mgmt_fee = rent * monthly_management_fee_rate
    mo_property_taxes = (value * annual_property_tax_rate) / 12
    mo_operating_exp = mo_maintance + mo_property_taxes + mo_mgmt_fee + monthly_insurance + monthly_leasing_fee + monthly_hoa_fee + monthly_utilities
    annual_operating_expenses = mo_operating_exp * 12
    net_operating_income = annual_gross_income - annual_operating_expenses
    cap_rate = round((net_operating_income / value), 4)
    return annual_gross_income, annual_operating_expenses, net_operating_income, cap_rate

