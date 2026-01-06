import pandas as pd
from drift_detector import detect_drift
import glob

# batch_files = sorted(glob.glob("live_batch_*.csv"))
batch_files = sorted(glob.glob("drifted_batches/live_batch_*.csv"))

for batch_file in batch_files:
    live_df = pd.read_csv(batch_file)
    report = detect_drift(live_df)

    print(f"\n📦 Monitoring {batch_file}")

    if not report:
        print("✅ No drift detected")
    else:
        for feature, details in report.items():
            print(
                f"⚠️ {feature} | "
                f"PSI={details['psi']} | "
                f"MeanShift={details['mean_shift']} | "
                f"VarShift={details['variance_shift']} | "
                f"{details['status']}"
            )