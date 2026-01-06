import pandas as pd
import glob
import os

# How strong the drift should be
DRIFT_FACTOR = 2.0   # 2x increase in transaction amount

# Inject drift only after this batch index
DRIFT_START_BATCH = 20

batch_files = sorted(glob.glob("live_batch_*.csv"))

os.makedirs("drifted_batches", exist_ok=True)

for batch_file in batch_files:
    batch_id = int(batch_file.split("_")[-1].replace(".csv", ""))
    df = pd.read_csv(batch_file)

    # Inject drift only for later batches
    if batch_id >= DRIFT_START_BATCH:
        df["amt"] = df["amt"] * DRIFT_FACTOR

    df.to_csv(f"drifted_batches/{os.path.basename(batch_file)}", index=False)

print("✅ Drift injected into later batches.")