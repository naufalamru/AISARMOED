import pandas as pd
import os
import requests
import streamlit as st

WEB_APP_URL = st.secrets["WEB_APP_URL"]

# =========================
# USER (GOOGLE SHEETS CLOUD)
# =========================

def load_users():
    """Memuat data user dari Google Sheets (Tab 'users')"""
    try:
        response = requests.get(f"{WEB_APP_URL}?sheet=users", timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if not df.empty:
                return df
    except Exception:
        pass
    
    # Fallback ke CSV lokal jika offline
    if os.path.exists("users.csv"):
        return pd.read_csv("users.csv")
    return pd.DataFrame(columns=["username", "password", "weight", "height"])

def login_user(username, password):
    df = load_users()
    if df.empty or "username" not in df.columns:
        return None
    user = df[(df["username"].astype(str) == str(username)) & (df["password"].astype(str) == str(password))]
    return user.iloc[0].to_dict() if not user.empty else None

def register_user(username, password, weight, height):
    """Mengirim data registrasi baru ke Google Sheets"""
    payload = {
        "sheet": "users",
        "action": "register",
        "username": username,
        "password": password,
        "weight": weight,
        "height": height
    }
    try:
        response = requests.post(WEB_APP_URL, json=payload, timeout=10)
        res_json = response.json()
        return res_json.get("status") == "success"
    except Exception:
        return False

def update_user_profile(username, weight, height):
    """Memperbarui profil user di Google Sheets"""
    payload = {
        "sheet": "users",
        "action": "update",
        "username": username,
        "weight": weight,
        "height": height
    }
    try:
        requests.post(WEB_APP_URL, json=payload, timeout=10)
    except Exception:
        pass

# =========================
# PROGRESS (GOOGLE SHEETS CLOUD)
# =========================

def save_progress(data):
    payload = {
        "sheet": "progress",
        "username": data.get("username"),
        "fatigue": data.get("fatigue"),
        "training_load": data.get("training_load"),
        "weight": data.get("weight"),
        "sleep": data.get("sleep"),
        "hr_mean": data.get("hr_mean"),
        "goal": data.get("goal")
    }
    
    try:
        response = requests.post(WEB_APP_URL, json=payload, timeout=10)
        return response.json()
    except Exception as e:
        return {"status": "error", "message": str(e)}

def load_progress(username=None):
    try:
        response = requests.get(f"{WEB_APP_URL}?sheet=progress", timeout=10)
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            if not df.empty and username and "username" in df.columns:
                return df[df["username"] == username]
            return df
    except Exception:
        pass
    
    if os.path.exists("progress.csv"):
        df = pd.read_csv("progress.csv")
        if not df.empty and username and "username" in df.columns:
            return df[df["username"] == username]
        return df
        
    return pd.DataFrame(columns=["username", "fatigue", "training_load", "weight", "sleep", "hr_mean", "goal"])

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

    hr_zone = hr_mean / hr_max
    intensity_score = hr_zone * 100
    sleep_score = min(100, sleep / 8 * 100)

    performance_score = (
        0.4 * intensity_score +
        0.4 * sleep_score +
        0.2 * (training_load / 100)
    )

    goal_bulking = 1 if goal == "bulking" else 0
    goal_cardio = 0

    if goal == "maintaining":
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
    return min(fatigue, 100)
