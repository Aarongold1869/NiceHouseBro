
fn calculate_cap_rate(value: Int, rent: Int, property_tax_rate: Float64=0.0091, mgmt_fee: Int=10, insurance: Int=136)-> Float64:
    var ann_gross_income: Int = rent * 12
    var mo_maintance: Float64 = rent * 0.08
    var mo_property_taxes: Float64 = value * property_tax_rate
    var mo_operating_exp: Float64 = mo_maintance + mo_property_taxes + mgmt_fee + insurance
    var ann_operating_ex: Float64 = mo_operating_exp * 12
    var net_income: Float64 = ann_gross_income - ann_operating_ex
    var cap_rate: Float64 = net_income / value
    return cap_rate

# fn calculate_cap_rate(value: Int, rent: Int)-> Float64:
#     return rent / value

def main():
    print('nice')
    var cap_rate = calculate_cap_rate(value=250000, rent=1000)
    print(cap_rate)