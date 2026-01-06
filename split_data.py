import pandas as pd

# Columns we decided to keep
COLS = [
    "trans_date_trans_time",
    "amt",
    "lat",
    "long",
    "city_pop",
    "unix_time",
    "merch_lat",
    "merch_long"
]

# Load dataset (memory-safe)
df = pd.read_csv("credit_card.csv", usecols=COLS)

# Convert and sort by time
df["trans_date_trans_time"] = pd.to_datetime(
    df["trans_date_trans_time"],
    dayfirst=True,
    errors="coerce"
)
df = df.sort_values("trans_date_trans_time").reset_index(drop=True)

# 60 / 40 split
split_idx = int(len(df) * 0.6)

baseline_df = df.iloc[:split_idx]
live_df = df.iloc[split_idx:]

# Save outputs
baseline_df.to_csv("baseline.csv", index=False)
live_df.to_csv("live_stream.csv", index=False)

print(f"Baseline rows: {len(baseline_df)}")
print(f"Live rows: {len(live_df)}")