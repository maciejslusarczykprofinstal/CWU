# calc/dhw_demand.py
"""
Profile zapotrzebowania CWU (EN 15316-3-x):
- Tu wprowadzimy klasy profili poboru (M, L, XL...) i dobowy rozkład.
- Na razie placeholder z interfejsem gotowym na późniejsze wdrożenie.
"""

from dataclasses import dataclass

@dataclass
class DHWProfile:
    name: str
    daily_volume_l: float  # całkowity dzienny pobór [l]
    T_cold: float          # temp. wody zimnej [°C]
    T_dhw: float           # temp. zadana CWU [°C]

def daily_energy_kWh(profile: DHWProfile, rho_kg_per_l=0.998, c_kJ_per_kgK=4.186):
    """
    E_d = m*c*ΔT; m = objętość [l] * gęstość [kg/l]
    Wynik [kWh/d]; uproszczony, bez cyrkulacji i strat przesyłu (dodamy w bilansie).
    """
    m_kg = profile.daily_volume_l * rho_kg_per_l
    dT = max(0.0, profile.T_dhw - profile.T_cold)
    E_kJ = m_kg * c_kJ_per_kgK * dT
    return E_kJ / 3600.0  # kWh
