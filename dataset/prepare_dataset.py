import pandas as pd
import numpy as np

# =========================
# LOAD DATA
# =========================
activity = pd.read_csv("dailyActivity_merged.csv")
sleep = pd.read_csv("Sleep_health_and_lifestyle_dataset.csv")
hr = pd.read_csv("heartrate_seconds_merged.csv")

# =========================
# FORMAT DATE
# =========================
activity["date"] = pd.to_datetime(activity["ActivityDate"]).dt.date
hr["date"] = pd.to_datetime(hr["Time"]).dt.date

# =========================
# SLEEP CLEAN
# =========================
sleep = sleep.rename(columns={
    "Sleep Duration": "sleep_hours"
})

sleep["date"] = pd.to_datetime("2024-01-01")  # dummy (karena beda dataset)
sleep = sleep[["sleep_hours"]]

# =========================
# HR AGGREGATE
# =========================
hr_daily = hr.groupby("date")["Value"].agg([
    "mean", "max"
]).reset_index()

hr_daily.columns = ["date", "hr_mean", "hr_max"]

# =========================
# MERGE
# =========================
df = activity.merge(hr_daily, on="date", how="left")

# =========================
# FILL MISSING
# =========================
df["hr_mean"] = df["hr_mean"].fillna(75)
df["hr_max"] = df["hr_max"].fillna(120)

# =========================
# FEATURE ENGINEERING
# =========================

df["sleep_hours"] = np.random.uniform(5, 8, len(df))

df["duration"] = df["VeryActiveMinutes"] + df["FairlyActiveMinutes"]

df["bmi"] = np.random.uniform(18, 28, len(df))

df["goal"] = np.random.choice(["cutting", "bulking", "cardio"], len(df))

df["goal_bulking"] = (df["goal"] == "bulking").astype(int)
df["goal_cardio"] = (df["goal"] == "cardio").astype(int)

df["calories"] = df["Calories"]

# =========================
# TARGET FATIGUE
# =========================
df["fatigue"] = (
    (df["calories"] / 50) +
    (df["TotalSteps"] / 2000) +
    (df["duration"] * 0.4) +
    (df["hr_mean"] * 0.3) +
    (df["hr_max"] * 0.2) -
    (df["sleep_hours"] * 6)
)

df["fatigue"] = df["fatigue"].clip(0, 100)

# =========================
# FINAL DATASET
# =========================
final = df[[
    "bmi",
    "calories",
    "duration",
    "sleep_hours",
    "hr_mean",
    "hr_max",
    "goal_bulking",
    "goal_cardio",
    "fatigue"
]]

final.to_csv("dataset.csv", index=False)

print("✅ Dataset ready:", final.shape)