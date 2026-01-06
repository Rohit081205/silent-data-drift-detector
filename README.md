# 🚨 Silent Data Drift Detector for Startups

A lightweight, production-friendly system to **detect silent data drift** in machine learning pipelines **before model performance degrades**.

---

## ❓ Why This Project?

Startups often deploy ML models quickly, but over time:

- User behavior changes
- Feature distributions shift
- Model accuracy drops **silently**
- Labels are unavailable in production

Most teams notice only **after business damage occurs**.

Existing drift tools are often **heavy, expensive, or overkill** for early-stage startups.

---

## 💡 Solution Overview

This project implements a **lightweight data drift monitoring system** that:

- Compares **incoming live data** with **training-time baseline data**
- Detects **statistical distribution drift**
- Works **without labels**
- Requires **no retraining**
- Has **no cloud dependency**

It provides **early warnings** so teams can act *before* models fail.

---

## 🧠 Key Idea

Instead of monitoring model accuracy (which requires labels),  
we monitor **data distributions** directly using statistical metrics.

> If the data changes, the model is at risk — even if accuracy hasn’t dropped yet.

---

## 🏗️ System Architecture

Raw Historical Data
↓
Baseline Statistics (Mean, Variance, PSI bins)
↓
Live Data (Simulated as Batches)
↓
Drift Detection Engine
↓
Early Warnings (Console / Logs)


---

## 📊 Drift Detection Metrics Used

For each numeric feature, the system monitors:

- **Mean Shift** – relative change in average
- **Variance Shift** – spread change
- **Population Stability Index (PSI)** – distributional shift  
  (implemented using **percentile-based bins**, industry standard)

### PSI Interpretation
- `PSI < 0.10` → No drift  
- `0.10 ≤ PSI < 0.25` → Moderate drift  
- `PSI ≥ 0.25` → Severe drift  

---

## ⚠️ Important Design Decisions

- **Timestamps are excluded** from drift detection  
  (they are monotonically increasing and always drift by definition)

- **No labels are used**  
  (reflects real production constraints)

- **Baseline statistics are stored**, not raw training data  
  (memory-efficient and reusable)

---

## 🧪 Drift Simulation (Validation)

To validate the system, **controlled drift** is injected into live data:

- Transaction amounts are artificially scaled (e.g., 2× increase)
- Early batches show **no drift**
- Later batches correctly trigger **SEVERE DRIFT alerts**

This demonstrates that the system:
- Avoids false positives
- Detects real distribution changes reliably

---

## 📁 Project Structure

```text
silent-data-drift-detector/
├── compute_baseline_stats.py     # Compute baseline feature statistics
├── create_live_batches.py        # Simulate streaming data
├── split_data.py                 # Time-based train/live split
├── inject_drift.py               # Inject artificial drift
├── psi.py                        # Percentile-based PSI implementation
├── drift_detector.py             # Core drift detection logic
├── monitor.py                    # Monitor live batches
├── baseline_stats.json           # Stored baseline reference
├── requirements.txt              # Dependencies
├── README.md
└── .gitignore

---

▶️ How to Run

1️⃣ Install Dependencies
pip install -r requirements.txt

2️⃣ Prepare Baseline & Live Data
python split_data.py
python create_live_batches.py

3️⃣ Compute Baseline Statistics
python compute_baseline_stats.py

4️⃣ (Optional) Inject Drift
python inject_drift.py

5️⃣ Monitor for Drift
python monitor.py

📌 Example Output
📦 Monitoring live_batch_25.csv
⚠️ amt | PSI=0.58 | MeanShift=1.01 | VarShift=3.57 | SEVERE DRIFT

🎯 Why Startups Would Use This

🚫 Prevents silent ML failures
💸 Saves customer trust & revenue
🧠 Encourages proactive ML monitoring
⚡ Lightweight & low infrastructure cost
🔌 Easy to integrate into existing pipelines

🛠 Tech Stack

Python
pandas, numpy
scipy
No cloud services
No MLOps frameworks

📌 Future Enhancements

Streamlit dashboard for visual monitoring
Logging / email alerts
Categorical feature drift detection
Integration with CI/CD or model registries