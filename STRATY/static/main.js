document.addEventListener("DOMContentLoaded", () => {
  document.getElementById("msg").textContent = "Frontend działa ✅";
  console.log("main.js uruchomiony!");
});

const form = document.getElementById("calc-form");
const resultBox = document.getElementById("result");

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  resultBox.textContent = "Liczenie…";

  const payload = {
    L: parseFloat(document.getElementById("L").value),
    r_i: parseFloat(document.getElementById("r_i").value),
    r_o: parseFloat(document.getElementById("r_o").value),
    k: parseFloat(document.getElementById("k").value),
    T_in: parseFloat(document.getElementById("T_in").value),
    T_out: parseFloat(document.getElementById("T_out").value),
  };

  try {
    const res = await fetch("/api/pipe-loss", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (!res.ok) {
      const err = await res.json();
      throw new Error(err.detail || "Błąd API");
    }
    const data = await res.json();
    resultBox.innerHTML = `
      <div><b>q′ (W/m):</b> ${data.q_linear}</div>
      <div><b>Q całkowite (W):</b> ${data.Q_total}</div>
      <small>${data.note}</small>
    `;
  } catch (err) {
    resultBox.innerHTML = `<span class="error">❌ ${err.message}</span>`;
  }
});
