# calc/storage.py
"""
Straty postojowe zasobnika:
- Model uproszczony: Qdot = U*A * (T_woda - T_amb) [W]
- UA przyjmujemy z karty katalogowej albo szacujemy (TODO: dodać wytyczne z EN 15316-3)
"""

def tank_standby_loss(UA_W_per_K: float, T_hot: float, T_amb: float) -> float:
    """
    Moc strat postojowych [W].
    """
    dT = max(0.0, T_hot - T_amb)
    return UA_W_per_K * dT
