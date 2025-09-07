# calc/finance.py
def kWh_to_GJ(kwh: float) -> float:
    return kwh / 277.7777777778

def annual_cost_from_GJ(GJ: float, price_per_GJ: float) -> float:
    return GJ * price_per_GJ

def annual_energy_from_power_kW(power_kW: float, hours_per_day=24, days_per_year=365) -> float:
    return power_kW * hours_per_day * days_per_year  # kWh/rok
