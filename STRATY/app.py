from flask import Flask, render_template, request
import os
import traceback

# --- domena obliczeń ---
from calc.pipes import loop_losses, DN_OUTER_DIAM_MM
from calc.storage import tank_standby_loss
from calc.finance import annual_energy_from_power_kW, kWh_to_GJ, annual_cost_from_GJ
# -----------------------

app = Flask(__name__, template_folder="templates", static_folder="static")

# Domyślne parametry
DEFAULTS = {
    # Rurociąg cyrkulacyjny
    "L_m": 150.0,
    "d_out_mm": 26.9,       # DN20 stal
    "insulation_mm": 30.0,
    "lambda_ins": 0.035,
    "h_ext": 7.0,
    "T_hot": 55.0,
    "T_amb": 20.0,

    # Zasobnik
    "UA_tank": 2.0,         # W/K (placeholder – docelowo z karty katalogowej)
    "T_tank": 55.0,

    # Bilans i koszty
    "hours_per_day": 24,
    "days_per_year": 365,
    "price_per_GJ": 70.0,
}

def pfloat(v):
    """Akceptuje '12,3' i '12.3'."""
    if v is None or v == "":
        return None
    return float(str(v).replace(",", ".").strip())

@app.route("/healthz")
def healthz():
    return "ok", 200

@app.route("/", methods=["GET", "POST"])
def index():
    form = dict(DEFAULTS)
    result = None
    error = None
    dn_map = DN_OUTER_DIAM_MM

    if request.method == "POST":
        try:
            # 1) wczytaj pola liczbowe
            for k in DEFAULTS.keys():
                raw = request.form.get(k)
                val = pfloat(raw)
                if val is not None:
                    form[k] = val

            # 2) ew. wybór DN nadpisuje d_out_mm
            dn_key = (request.form.get("dn_key") or "").strip()
            if dn_key and dn_key in dn_map:
                form["d_out_mm"] = dn_map[dn_key]

            # 3) obliczenia
            loop = loop_losses(
                L_m=form["L_m"],
                d_out_mm=form["d_out_mm"],
                insulation_mm=form["insulation_mm"],
                lambda_ins=form["lambda_ins"],
                h_ext=form["h_ext"],
                T_hot=form["T_hot"],
                T_amb=form["T_amb"],
            )

            tank_W = tank_standby_loss(
                form["UA_tank"], form["T_tank"], form["T_amb"]
            )

            total_kW = loop["Qdot_kW"] + (tank_W / 1000.0)

            E_kWh_year = annual_energy_from_power_kW(
                total_kW, form["hours_per_day"], form["days_per_year"]
            )
            E_GJ_year = kWh_to_GJ(E_kWh_year)
            cost_year = annual_cost_from_GJ(E_GJ_year, form["price_per_GJ"])

            result = {
                "loop_q_wpm": loop.get("q_wpm"),
                "loop_Qdot_kW": loop.get("Qdot_kW"),
                "tank_loss_W": tank_W,
                "total_kW": total_kW,
                "E_kWh_year": E_kWh_year,
                "E_GJ_year": E_GJ_year,
                "cost_year": cost_year,
            }

        except Exception as e:
            error = f"{e}\n{traceback.format_exc()}"

    # Spróbuj wyrenderować główny szablon; jeśli go brak – pokaż fallback
    try:
        return render_template(
            "4_Straty.html",
            form=form,
            dn_map=dn_map,
            result=result,
            error=error,
        )
    except Exception:
        html = f"""<!doctype html>
<html lang="pl"><meta charset="utf-8">
<title>STRATY CWU</title>
<body>
  <h1>STRATY CWU – aplikacja działa ✅</h1>
  <p>Brak szablonu <code>templates/4_Straty.html</code> lub błąd renderowania.
     Serwer i obliczenia są OK — to jest widok awaryjny.</p>
  {'<pre style="color:red">'+error+'</pre>' if error else ''}
  <details><summary>Form (debug)</summary><pre>{form}</pre></details>
  <details><summary>Result (debug)</summary><pre>{result}</pre></details>
  <p>Ping: <a href="/healthz">/healthz</a></p>
</body></html>"""
        return html

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True,
    )
