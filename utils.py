import pandas as pd
import streamlit as st
from supabase import create_client, Client

# Inisialisasi Koneksi Supabase
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# =========================
# USER (SUPABASE)
# =========================

def load_users():
    """Memuat data user dari database Supabase"""
    try:
        response = supabase.table("users").select("*").execute()
        data = response.data
        if data:
            return pd.DataFrame(data)
    except Exception:
        pass
    return pd.DataFrame(columns=["username", "password", "weight", "height"])

def login_user(username, password):
    try:
        response = supabase.table("users").select("*").eq("username", username).eq("password", password).execute()
        data = response.data
        if data:
            return data[0]
    except Exception:
        pass
    return None

def register_user(username, password, weight, height):
    try:
        # Cek apakah username sudah ada
        existing = supabase.table("users").select("username").eq("username", username).execute()
        if existing.data:
            return False
        
        # Simpan user baru ke Supabase
        supabase.table("users").insert({
            "username": username,
            "password": password,
            "weight": weight,
            "height": height
        }).execute()
        return True
    except Exception:
        return False

def update_user_profile(username, weight, height):
    try:
        supabase.table("users").update({
            "weight": weight,
            "height": height
        }).eq("username", username).execute()
    except Exception:
        pass

# =========================
# PROGRESS (SUPABASE)
# =========================

def save_progress(data):
    try:
        payload = {
            "username": data.get("username"),
            "fatigue": data.get("fatigue"),
            "training_load": data.get("training_load"),
            "weight": data.get("weight"),
            "sleep": data.get("sleep"),
            "hr_mean": data.get("hr_mean"),
            "goal": data.get("goal"),
            "date": data.get("date")
        }
        supabase.table("progress").insert(payload).execute()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

def load_progress(username=None):
    try:
        query = supabase.table("progress").select("*")
        if username:
            query = query.eq("username", username)
        response = query.execute()
        data = response.data
        if data:
            return pd.DataFrame(data)
    except Exception:
        pass
    return pd.DataFrame(columns=["username", "fatigue", "training_load", "weight", "sleep", "hr_mean", "goal", "date"])

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

    goal_cutting = 1 if goal == "cutting" else 0
    goal_bulking = 1 if goal == "bulking" else 0
    goal_maintaining = 1 if goal == "maintaining" else 0

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
        "goal_cutting": goal_cutting,         
        "goal_bulking": goal_bulking,         
        "goal_maintaining": goal_maintaining, 
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
