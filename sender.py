import requests
import random
import time
import os

# Accumulated energy (kWh) — grows over time
energy_kwh = 0.0
last_time = time.time()

SERVER_URL = os.environ.get("SERVER_URL", "http://127.0.0.1:5000/data")

print("⚡ ElectraVision Simulator starting...")

while True:
    now = time.time()
    dt_hours = (now - last_time) / 3600  # time delta in hours
    last_time = now

    voltage   = round(random.uniform(210, 230), 2)
    current   = round(random.uniform(5, 15), 2)
    power     = round(voltage * current, 2)                     # Watts
    frequency = round(random.uniform(49.5, 50.5), 2)            # Hz  (nominal 50 Hz)
    pf        = round(random.uniform(0.80, 0.99), 2)            # Power factor

    # Accumulate energy: E(kWh) += P(W) / 1000 * Δt(h)
    energy_kwh += (power / 1000) * dt_hours
    energy_kwh  = round(energy_kwh, 4)

    data = {
        "voltage":   voltage,
        "current":   current,
        "power":     power,
        "frequency": frequency,
        "pf":        pf,
        "energy":    energy_kwh,
    }

    try:
        resp = requests.post(SERVER_URL, json=data, timeout=3)
        print(f"[{time.strftime('%H:%M:%S')}] Sent → V={voltage}V  I={current}A  "
              f"P={power}W  f={frequency}Hz  PF={pf}  E={energy_kwh}kWh  "
              f"| HTTP {resp.status_code}")
    except requests.exceptions.ConnectionError:
        print(f"[{time.strftime('%H:%M:%S')}] ⚠  Server unreachable — retrying...")

    time.sleep(1)