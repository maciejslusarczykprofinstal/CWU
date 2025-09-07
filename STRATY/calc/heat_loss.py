# calc/heat_loss.py
import math

def heat_loss_per_meter(d_out_mm, insulation_mm, lambda_ins=0.035, h_ext=7.0,
                        T_hot=55.0, T_amb=20.0) -> float:
    """
    Model: przewodzenie przez izolację cylindryczną + konwekcja zewnętrzna.
    R_cond = ln(r2/r1)/(2πλ), R_ext = 1/(h_ext·2π·r2), q = ΔT / (R_cond + R_ext)
    """
    # Walidacja wejść
    if d_out_mm <= 0:
        raise ValueError("Średnica zewnętrzna rury musi być > 0 mm")
    if insulation_mm <= 0:
        raise ValueError("Grubość izolacji musi być > 0 mm")
    if lambda_ins <= 0:
        raise ValueError("Współczynnik przewodzenia izolacji musi być > 0")
    if h_ext <= 0:
        raise ValueError("Współczynnik konwekcji zewnętrznej musi być > 0")

    r1 = (d_out_mm / 1000.0) / 2.0
    r2 = r1 + (insulation_mm / 1000.0)
    R_cond = math.log(r2 / r1) / (2 * math.pi * lambda_ins)
    R_ext  = 1.0 / (h_ext * 2 * math.pi * r2)
    q = (T_hot - T_amb) / (R_cond + R_ext)  # W/m
    return q

def compute_report(L_m, d_out_mm, insulation_mm, T_hot, T_amb,
                   lambda_ins=0.035, h_ext=7.0,
                   hours_per_day=24, days_per_year=365, price_per_GJ=60.0) -> dict:
    """
    Oblicza raport strat ciepła i kosztów.
    Zwraca słownik z wynikami.
    """
    # Walidacja wejść
    if L_m <= 0:
        raise ValueError("Długość rurociągu musi być > 0 m")
    if hours_per_day <= 0 or days_per_year <= 0:
        raise ValueError("Czas pracy musi być > 0")
    if price_per_GJ < 0:
        raise ValueError("Cena ciepła nie może być ujemna")

    q_wpm = heat_loss_per_meter(d_out_mm, insulation_mm, lambda_ins, h_ext, T_hot, T_amb)
    Qdot_W = q_wpm * L_m
    Qdot_kW = Qdot_W / 1000.0
    E_kWh_year = Qdot_kW * hours_per_day * days_per_year
    E_GJ_year = E_kWh_year / 277.7777777778
    cost_year = E_GJ_year * price_per_GJ
    return {
        "q_wpm": q_wpm,
        "Qdot_kW": Qdot_kW,
        "E_kWh_year": E_kWh_year,
        "E_GJ_year": E_GJ_year,
        "cost_year": cost_year
    }
