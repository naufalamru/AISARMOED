import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib

df = pd.read_csv("dataset.csv")

X = df.drop("fatigue", axis=1)
y = df["fatigue"]

model = RandomForestRegressor(n_estimators=100)
model.fit(X, y)

joblib.dump(model, "../model.pkl")

print("✅ Model trained & saved")