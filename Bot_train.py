import os
import pandas as pd
import numpy as np
import random
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from xgboost import XGBClassifier
import joblib

# Paths to the directories
tops_path = r"C:\Users\Lenovo\OneDrive\Desktop\Midam_codes\DIS_Modara\assets\tops"
pants_path = r"C:\Users\Lenovo\OneDrive\Desktop\Midam_codes\DIS_Modara\assets\pant"

# Function to get file names from a directory
def get_file_names(directory_path):
    return [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

# Get the file names from both directories
tops = get_file_names(tops_path)
bottoms = get_file_names(pants_path)

# Load the fashion trends data
trend_df = pd.read_csv("./fashion_trends.csv")
trends = trend_df['Title'].dropna().unique().tolist()

cities = ["Delhi", "Mumbai", "Bengaluru", "Kolkata", "Chennai", "Hyderabad"]
sky_conditions = ["Sunny", "Cloudy", "Rainy", "Partly Cloudy", "Hazy"]

# ✅ SYNTHETIC DATA GENERATOR
def generate_data(n=500):
    data = []
    for _ in range(n):
        city = random.choice(cities)
        temp = random.randint(20, 40)
        sky = random.choice(sky_conditions)
        trend = random.choice(trends)
        top = random.choice(tops)
        bottom = random.choice(bottoms)
        data.append([city, temp, sky, trend, top, bottom])
    return pd.DataFrame(data, columns=["city", "temperature", "sky", "trend", "top", "bottom"])

# Generate dataset
data = generate_data()

# ✅ LABEL ENCODING
le_city = LabelEncoder()
le_sky = LabelEncoder()
le_trend = LabelEncoder()
le_top = LabelEncoder()
le_bottom = LabelEncoder()

data["city_enc"] = le_city.fit_transform(data["city"])
data["sky_enc"] = le_sky.fit_transform(data["sky"])
data["trend_enc"] = le_trend.fit_transform(data["trend"])
data["top_enc"] = le_top.fit_transform(data["top"])
data["bottom_enc"] = le_bottom.fit_transform(data["bottom"])

# ✅ TREND PREDICTION MODEL (to auto-predict trend later)
X_trend = data[["city_enc", "temperature", "sky_enc"]]
y_trend = data["trend_enc"]
X_train_trend, X_test_trend, y_train_trend, y_test_trend = train_test_split(X_trend, y_trend, test_size=0.2)

trend_model = XGBClassifier()
trend_model.fit(X_train_trend, y_train_trend)

# ✅ MAIN OUTFIT MODEL
X_outfit = data[["city_enc", "temperature", "sky_enc", "trend_enc"]]
y_top = data["top_enc"]
y_bottom = data["bottom_enc"]

X_train_outfit, X_test_outfit, y_train_top, y_test_top = train_test_split(X_outfit, y_top, test_size=0.2)
_, _, y_train_bottom, y_test_bottom = train_test_split(X_outfit, y_bottom, test_size=0.2)

top_model = XGBClassifier()
top_model.fit(X_train_outfit, y_train_top)

bottom_model = XGBClassifier()
bottom_model.fit(X_train_outfit, y_train_bottom)

# ✅ SAVE MODELS + ENCODERS
joblib.dump(trend_model, "trend_predictor.joblib")
joblib.dump(top_model, "top_predictor.joblib")
joblib.dump(bottom_model, "bottom_predictor.joblib")

joblib.dump(le_city, "le_city.joblib")
joblib.dump(le_sky, "le_sky.joblib")
joblib.dump(le_trend, "le_trend.joblib")
joblib.dump(le_top, "le_top.joblib")
joblib.dump(le_bottom, "le_bottom.joblib")

print("✅ Models and encoders saved!")
