import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
import pickle
import os

# -------------------------------
# 1. Dataset Path
# -------------------------------
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # project root
data_path = os.path.join(base_dir, "dataset", "house_data.csv")

# -------------------------------
# 2. Load Dataset
# -------------------------------
data = pd.read_csv(data_path)

# -------------------------------
# 3. Clean DistanceToCity column
# -------------------------------
if "DistanceToCity" in data.columns:
    data["DistanceToCity"] = (
        data["DistanceToCity"].astype(str).str.replace("km", "", regex=False).astype(float)
    )

# -------------------------------
# 4. Encode Categorical Columns
# -------------------------------
categorical_cols = ["Location", "NearbyFacilities", "HouseType", "Condition", "Amenities"]
le_dict = {}
for col in categorical_cols:
    if col in data.columns:
        le = LabelEncoder()
        data[col] = le.fit_transform(data[col].astype(str))
        le_dict[col] = le   # save encoder for later use if needed

# -------------------------------
# 5. Define Features & Target
# -------------------------------
features = [
    "Bedrooms", "Bathrooms", "Area_sqft", "Location", "Floors", "YearBuilt",
    "Parking", "NearbyFacilities", "HouseType", "LotSize",
    "Condition", "DistanceToCity", "Amenities"
]

X = data[features]
y = data["Price"]

# -------------------------------
# 6. Train-Test Split
# -------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# -------------------------------
# 7. Train Model
# -------------------------------
model = LinearRegression()
model.fit(X_train, y_train)

# -------------------------------
# 8. Save Model
# -------------------------------
model_dir = os.path.join(base_dir, "model")
os.makedirs(model_dir, exist_ok=True)

model_path = os.path.join(model_dir, "model.pkl")
with open(model_path, "wb") as f:
    pickle.dump(model, f)

print(f"✅ Model trained successfully and saved at {model_path}")
