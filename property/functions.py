
def calculate_cap_rate(value: int, rent: int, property_tax_rate: float=0.0091, mgmt_fee_rate: float=.01, insurance: int=136)-> float:
    if rent == 0:
        return 0
    ann_gross_income = rent * 12
    mo_maintance = rent * 0.08
    mo_mgmt_fee = rent * mgmt_fee_rate
    mo_property_taxes = (value * property_tax_rate) / 12
    mo_operating_exp = mo_maintance + mo_property_taxes + mo_mgmt_fee + insurance
    ann_operating_ex = mo_operating_exp * 12
    net_income = ann_gross_income - ann_operating_ex
    cap_rate = net_income / value
    return cap_rate
