import pandas as pd

BATCH_SIZE = 10000

live_df = pd.read_csv("live_stream.csv")

for i in range(0, len(live_df), BATCH_SIZE):
    batch = live_df.iloc[i:i + BATCH_SIZE]
    batch.to_csv(f"live_batch_{i//BATCH_SIZE}.csv", index=False)

print("Live batches created.")