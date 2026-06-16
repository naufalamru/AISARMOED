import pandas as pd
import os

# =========================
# USER
# =========================

def load_users():
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame(columns=["username", "password", "weight", "height"])

def save_users(df):
    df.to_csv("users.csv", index=False)

def login_user(username, password):
    df = load_users()
    user = df[(df["username"] == username) & (df["password"] == password)]
    return user.iloc[0].to_dict() if not user.empty else None

def register_user(username, password, weight, height):
    df = load_users()

    if username in df["username"].values:
        return False

    new_user = pd.DataFrame([{
        "username": username,
        "password": password,
        "weight": weight,
        "height": height
    }])

    df = pd.concat([df, new_user], ignore_index=True)
    save_users(df)
    return True

def update_user_profile(username, weight, height):
    df = load_users()
    df.loc[df["username"] == username, ["weight", "height"]] = [weight, height]
    save_users(df)

# =========================
# PROGRESS
# =========================

def save_progress(data):
    file = "progress.csv"
    df = pd.DataFrame([data])

    if os.path.exists(file):
        df.to_csv(file, mode="a", header=False, index=False)
    else:
        df.to_csv(file, index=False)

def load_progress():
    if os.path.exists("progress.csv"):
        return pd.read_csv("progress.csv")
    return pd.DataFrame()

# =========================
# FEATURE ENGINEERING (MATCH MODEL)
# =========================

def map_user_to_model_features(duration, sleep, weight, height, goal, sport):

    bmi = weight / (height ** 2)

    met_map = {
        "mma": 10, "boxing": 9, "muay_thai": 10,
        "bjj": 8, "wrestling": 9,
        "running": 8, "cycling": 7,
        "strength_training": 6,
        "hiit": 9, "cardio": 7,
        "rest": 1
    }

    met = met_map.get(sport, 6)

    calories = met * weight * (duration / 60)

    hr_mean = 70 + (met * 5)
    hr_max = hr_mean + 20

    training_load = duration * met

    # =========================
    # PERFORMANCE SCORE
    # =========================
    hr_zone = hr_mean / hr_max
    intensity_score = hr_zone * 100

    sleep_score = min(100, sleep / 8 * 100)

    performance_score = (
        0.4 * intensity_score +
        0.4 * sleep_score +
        0.2 * (training_load / 100)
    )

    # =========================
    # GOAL LOGIC (UPDATED)
    # =========================
    goal_bulking = 1 if goal == "bulking" else 0

    # ❗ maintaining → netral (tidak ubah model)
    goal_cardio = 0

    # =========================
    # TAMBAHAN LOGIC MAINTAINING
    # =========================
    if goal == "maintaining":
        # stabilkan load & kalori
        calories *= 1.0
        training_load *= 0.9

    elif goal == "cutting":
        calories *= 0.9

    elif goal == "bulking":
        calories *= 1.1

    return {
        "bmi": bmi,
        "calories": calories,
        "duration": duration,
        "sleep_hours": sleep,
        "hr_mean": hr_mean,
        "hr_max": hr_max,
        "goal_bulking": goal_bulking,
        "goal_cardio": goal_cardio,
        "training_load": training_load,
        "performance_score": performance_score
    }

def detect_unrealistic_training(duration, hr_mean, training_load):

    flags = []

    if duration > 240:
        flags.append("Durasi terlalu panjang")

    if hr_mean > 190:
        flags.append("Heart rate tidak realistis")

    if training_load > 2000:
        flags.append("Training load ekstrem")

    return flags

def adjust_fatigue(fatigue, flags):

    penalty = 0

    for f in flags:
        if "Durasi" in f:
            penalty += 10
        elif "Heart rate" in f:
            penalty += 15
        elif "load" in f:
            penalty += 20

    fatigue += penalty

    # clamp max 100
    return min(fatigue, 100)