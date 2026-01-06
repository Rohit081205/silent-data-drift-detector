import pandas as pd
import numpy as np
import json

# Numeric features to monitor
FEATURES = [
    "amt",
    "lat",
    "long",
    "city_pop",
    "merch_lat",
    "merch_long"
]

# Load baseline data
df = pd.read_csv("baseline.csv")

baseline_stats = {}

for feature in FEATURES:
    values = df[feature].dropna().values

    mean = float(np.mean(values))
    variance = float(np.var(values))

    # Histogram for PSI (fixed bins)
    counts, bin_edges = np.histogram(values, bins=10)

    baseline_stats[feature] = {
        "mean": mean,
        "variance": variance,
        "histogram": {
            "counts": counts.tolist(),
            "bin_edges": bin_edges.tolist()
        }
    }

# Save baseline stats
with open("baseline_stats.json", "w") as f:
    json.dump(baseline_stats, f, indent=4)

print("Baseline statistics saved to baseline_stats.json")