from flask import Flask, render_template, request
from calc.pipes import loop_losses, DN_OUTER_DIAM_MM
from calc.storage import tank_standby_loss
from calc.finance import annual_energy_from_power_kW, kWh_to_GJ, annual_cost_from_GJ

app = Flask(__name__)

DEFAULTS = {
    # Rurociąg cyrkulacyjny
    "L_m": 150.0,
    "d_out_mm": 26.9,      # DN20 stal
    "insulation_mm": 30.0,
    "lambda_ins": 0.035,
    "h_ext": 7.0,
    "T_hot": 55.0,
    "T_amb": 20.0,

    # Zasobnik
    "UA_tank": 2.0,        # W/K (placeholder - docelowo z karty katalogowej)
    "T_tank": 55.0,

    # Bilans i koszty
    "hours_per_day": 24,
    "days_per_year": 365,
    "price_per_GJ": 70.0
}

@app.route("/", methods=["GET", "POST"])
def index():
    form = DEFAULTS.copy()
    result = None
    error = None
    dn_map = DN_OUTER_DIAM_MM

    if request.method == "POST":
        try:
            # Pozwalamy na wybór DN (nadpisuje d_out_mm jeśli podano)
            dn_key = request.form.get("dn_key", "")
            for k in form.keys():
                val = request.form.get(k)
                if val is not None and val != "":
                    form[k] = float(val)
            if dn_key and dn_key in dn_map:
                form["d_out_mm"] = dn_map[dn_key]

            # Straty pętli
            loop = loop_losses(
                L_m=form["L_m"],
                d_out_mm=form["d_out_mm"],
                insulation_mm=form["insulation_mm"],
                lambda_ins=form["lambda_ins"],
                h_ext=form["h_ext"],
                T_hot=form["T_hot"],
                T_amb=form["T_amb"]
            )
            # Straty zasobnika (postojowe)
            tank_W = tank_standby_loss(form["UA_tank"], form["T_tank"], form["T_amb"])

            # Suma mocy strat
            total_kW = loop["Qdot_kW"] + (tank_W / 1000.0)

            # Energia i koszt roczny
            E_kWh_year = annual_energy_from_power_kW(
                total_kW, form["hours_per_day"], form["days_per_year"]
            )
            E_GJ_year = kWh_to_GJ(E_kWh_year)
            cost_year = annual_cost_from_GJ(E_GJ_year, form["price_per_GJ"])

            result = {
                "loop_q_wpm": loop["q_wpm"],
                "loop_Qdot_kW": loop["Qdot_kW"],
                "tank_loss_W": tank_W,
                "total_kW": total_kW,
                "E_kWh_year": E_kWh_year,
                "E_GJ_year": E_GJ_year,
                "cost_year": cost_year
            }
        except Exception as e:
            error = str(e)

    return render_template("4_Straty.html", form=form, dn_map=dn_map, result=result, error=error)

if __name__ == "__main__":
    app.run(debug=True)
