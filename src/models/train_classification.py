import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import joblib
import os

# Config paths
CLEAN_DATA_PATH = "/Users/iskandar/Development/BelajarPython/ProjectAkhir/data/processsed/StudentPerformanceFactorsClean.csv"
MODEL_DIR = "/Users/iskandar/Development/BelajarPython/ProjectAkhir/data/models"

if not os.path.exists(MODEL_DIR):
    os.makedirs(MODEL_DIR)

# 1. Load Data
df = pd.read_csv(CLEAN_DATA_PATH)

# 2. Features and Target
# Match the feature set used in Klasifikasi.ipynb
features = [
    "Hours_Studied", "Attendance", "Extracurricular_Activities", 
    "Previous_Scores", "Internet_Access", "Tutoring_Sessions", 
    "Peer_Influence", "Physical_Activity", "Parental_Education_Level", 
    "Distance_from_Home"
]

X = df[features]
y = df["Academic_Status"]

# 3. Categorical Encoding (same as notebook)
X = pd.get_dummies(X, drop_first=True)

# 4. Target Encoding (Fail: 0, Remidial: 1, Pass: 2)
label_map = {"Fail": 0, "Remidial": 1, "Pass": 2}
y = y.map(label_map)

# 5. Scaling
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# 6. Train Model
model = LogisticRegression(max_iter=1000, random_state=42)
model.fit(X_scaled, y)

# 7. Save Model and Scaler
joblib.dump(model, os.path.join(MODEL_DIR, "model_classification.pkl"))
joblib.dump(scaler, os.path.join(MODEL_DIR, "scaler.pkl"))
# Also save feature names for inference alignment
joblib.dump(X.columns.tolist(), os.path.join(MODEL_DIR, "feature_names.pkl"))

print(f"Model and Scaler saved to {MODEL_DIR}")
print(f"Features trained: {X.columns.tolist()}")
