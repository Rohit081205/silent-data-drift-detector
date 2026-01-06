# import pandas as pd
# import numpy as np
# import json
# from psi import calculate_psi

# FEATURES = [
#     "amt",
#     "lat",
#     "long",
#     "city_pop",
#     "unix_time",
#     "merch_lat",
#     "merch_long"
# ]

# PSI_THRESHOLD_MODERATE = 0.1
# PSI_THRESHOLD_SEVERE = 0.25

# MEAN_SHIFT_THRESHOLD = 0.2      # 20% relative shift
# VAR_SHIFT_THRESHOLD = 0.3       # 30% relative shift

# # Load baseline stats
# with open("baseline_stats.json") as f:
#     baseline_stats = json.load(f)

# # Load baseline raw data (needed for PSI expected values)
# baseline_df = pd.read_csv("baseline.csv")

# def detect_drift(live_df):
#     drift_report = {}

#     for feature in FEATURES:
#         base_vals = baseline_df[feature].dropna().values
#         live_vals = live_df[feature].dropna().values

#         if len(live_vals) == 0:
#             continue

#         # Mean & variance
#         base_mean = baseline_stats[feature]["mean"]
#         base_var = baseline_stats[feature]["variance"]

#         live_mean = np.mean(live_vals)
#         live_var = np.var(live_vals)

#         mean_shift = abs(live_mean - base_mean) / (abs(base_mean) + 1e-6)
#         var_shift = abs(live_var - base_var) / (abs(base_var) + 1e-6)

#         psi = calculate_psi(base_vals, live_vals, bins=10)

#         status = "NO DRIFT"
#         if psi > PSI_THRESHOLD_SEVERE:
#             status = "SEVERE DRIFT"
#         elif psi > PSI_THRESHOLD_MODERATE:
#             status = "MODERATE DRIFT"

#         if (
#             mean_shift > MEAN_SHIFT_THRESHOLD or
#             var_shift > VAR_SHIFT_THRESHOLD or
#             psi > PSI_THRESHOLD_MODERATE
#         ):
#             drift_report[feature] = {
#                 "mean_shift": round(mean_shift, 3),
#                 "variance_shift": round(var_shift, 3),
#                 "psi": round(psi, 3),
#                 "status": status
#             }

#     return drift_report

import pandas as pd
import numpy as np
import json
from psi import calculate_psi

# ✅ Final features used for drift detection
FEATURES = [
    "amt",
    "lat",
    "long",
    "city_pop",
    "merch_lat",
    "merch_long"
]

PSI_THRESHOLD_MODERATE = 0.1
PSI_THRESHOLD_SEVERE = 0.25

MEAN_SHIFT_THRESHOLD = 0.2      # 20% relative shift
VAR_SHIFT_THRESHOLD = 0.3       # 30% relative shift

# Load baseline stats
with open("baseline_stats.json") as f:
    baseline_stats = json.load(f)

# Load baseline raw data (needed for PSI expected values)
baseline_df = pd.read_csv("baseline.csv")

def detect_drift(live_df):
    drift_report = {}

    for feature in FEATURES:

        # ✅ Defensive check (prevents KeyError)
        if feature not in baseline_stats or feature not in baseline_df.columns:
            continue

        base_vals = baseline_df[feature].dropna().values
        live_vals = live_df[feature].dropna().values

        if len(live_vals) == 0 or len(base_vals) == 0:
            continue

        # Baseline stats
        base_mean = baseline_stats[feature]["mean"]
        base_var = baseline_stats[feature]["variance"]

        # Live stats
        live_mean = np.mean(live_vals)
        live_var = np.var(live_vals)

        mean_shift = abs(live_mean - base_mean) / (abs(base_mean) + 1e-6)
        var_shift = abs(live_var - base_var) / (abs(base_var) + 1e-6)

        # psi = calculate_psi(base_vals, live_vals, bins=10)
        psi = calculate_psi(base_vals, live_vals, buckets=10)

        status = "NO DRIFT"
        if psi > PSI_THRESHOLD_SEVERE:
            status = "SEVERE DRIFT"
        elif psi > PSI_THRESHOLD_MODERATE:
            status = "MODERATE DRIFT"

        if (
            mean_shift > MEAN_SHIFT_THRESHOLD or
            var_shift > VAR_SHIFT_THRESHOLD or
            psi > PSI_THRESHOLD_MODERATE
        ):
            drift_report[feature] = {
                "mean_shift": round(mean_shift, 3),
                "variance_shift": round(var_shift, 3),
                "psi": round(psi, 3),
                "status": status
            }

    return drift_report