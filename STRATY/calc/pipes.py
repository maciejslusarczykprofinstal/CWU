# calc/pipes.py
import math
from .norms import PI

# Przykładowe mapy średnic zewnętrznych (mm) dla ułatwienia wyboru DN
DN_OUTER_DIAM_MM = {
    # stal wg DIN/EN (przyjmujemy średnicę zewn.)
    "DN15_stal": 21.3, "DN20_stal": 26.9, "DN25_stal": 33.7, "DN32_stal": 42.4,
    "DN40_stal": 48.3, "DN50_stal": 60.3,
    # miedź (średnica zewnętrzna)
    "Cu_18": 18.0, "Cu_22": 22.0, "Cu_28": 28.0, "Cu_35": 35.0,
    # PEX/PP (zależne od systemu)
    "PEX_25": 25.0, "PEX_32": 32.0,
}

def heat_loss_per_meter_iso12241(d_out_mm: float,
                                 insulation_mm: float,
                                 lambda_ins: float = 0.035,
                                 h_ext: float = 7.0,
                                 T_hot: float = 55.0,
                                 T_amb: float = 20.0) -> float:
    """
    Strata liniowa q [W/m] dla rury z izolacją cylindryczną (EN ISO 12241):
      R_cond = ln(r2/r1) / (2πλ)
      R_ext  = 1 / (h_ext · 2π · r2)
      q = ΔT / (R_cond + R_ext)
    Pomijamy opór wewnętrzny i promieniowanie w v1 (do dodania później).
    """
    if insulation_mm <= 0:
        raise ValueError("Grubość izolacji musi być > 0 mm")
    if d_out_mm <= 0:
        raise ValueError("Średnica zewnętrzna musi być > 0 mm")
    r1 = (d_out_mm / 1000.0) / 2.0
    r2 = r1 + (insulation_mm / 1000.0)
    if r2 <= r1:
        raise ValueError("Błędna geometria izolacji (r2 <= r1).")
    deltaT = (T_hot - T_amb)
    if deltaT <= 0:
        return 0.0

    R_cond = math.log(r2 / r1) / (2 * PI * lambda_ins)
    R_ext  = 1.0 / (h_ext * 2 * PI * r2)
    q = deltaT / (R_cond + R_ext)
    return q

def loop_losses(L_m: float, **kwargs) -> dict:
    """
    Bilans strat dla pętli cyrkulacyjnej:
    - q [W/m] z ISO 12241
    - Qdot [kW] = q * L
    Zwraca słownik z wartościami + echo wejścia.
    """
    q = heat_loss_per_meter_iso12241(**kwargs)
    Qdot_kW = (q * L_m) / 1000.0
    return {"q_wpm": q, "Qdot_kW": Qdot_kW}
