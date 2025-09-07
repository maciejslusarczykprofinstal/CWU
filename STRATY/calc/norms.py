# calc/norms.py
"""
Normy i założenia:
- EN ISO 12241: Izolacje cieplne - Obliczenia strat przez izolację cylindryczną.
- EN 15316-3 (seria): Systemy przygotowania CWU - wydajność energetyczna (profilowanie, straty).
- EN 12828/12831: Symbolika, konwencje, niektóre współczynniki pomocnicze.
"""

PI = 3.141592653589793
SIGMA = 5.670374419e-8  # W/m2K4 (na przyszłość: promieniowanie, jeśli uwzględnimy)
# Typowe zakresy do sanity-check:
H_EXT_RANGE = (5.0, 15.0)   # W/m2K – naturalna konwekcja wewnątrz budynku
LAMBDA_INS_RANGE = (0.028, 0.045)  # W/mK – wełna/armaflex w temp. ~50-60°C
