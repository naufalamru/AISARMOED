import streamlit as st
import joblib
import pandas as pd
import datetime
import time
import base64
import supabase

from utils import *
from logic import *

SESSION_TIMEOUT = 1200

# =========================
# 🎨 CONFIG
# =========================
st.set_page_config(page_title="MMA AI Assistant", layout="wide")

# =========================
# 🎨 LOAD LOGO (BASE64)
# =========================
def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# =========================
# 🎨 STYLE
# =========================
st.markdown("""
<style>
/* BACKGROUND */
.stApp {
    background-color: #0f0f0f;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background-color: #b30000 !important;
}

/* TEXT */
h1, h2, h3, h4, h5, h6, p, span, label {
    color: white !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
}

/* BUTTON */
.stButton>button {
    background-color: #ff1a1a;
    color: white;
    border-radius: 12px;
    border: none;
    height: 60px;
    font-size: 20px;
    font-weight: bold;
}

/* CARD */
.card {
    background-color: #1c1c1c;
    padding: 15px;
    border-radius: 12px;
    margin-top: 10px;
    color: white !important;
}

.card * {
    color: white !important;
}

.card a {
    color: #ff4d4d !important;
}

/* METRIC */
[data-testid="metric-container"] {
    background-color: #1c1c1c;
    border-radius: 10px;
    padding: 10px;
}

/* INPUT */
input, textarea {
    color: black !important;
}

/* SELECT */
div[data-baseweb="select"] * {
    color: black !important;
}

html, body, [class*="css"] {
    color: white !important;
}

.stMarkdown,
.stMarkdown p,
.stMarkdown li,
.stMarkdown strong,
.stMarkdown h1,
.stMarkdown h2,
.stMarkdown h3,
.stMarkdown h4 {
    color: white !important;
}

[data-testid="stAlert"] *, .stSuccess *, .stInfo *, .stWarning *, .stError * {
    color: white !important;
}
</style>
""", unsafe_allow_html=True)

# =========================
# LOAD MODEL
# =========================
@st.cache_resource
def load_model():
    return joblib.load("model.pkl")

model = load_model()

# =========================
# SESSION
# =========================
if "user" not in st.session_state:
    st.session_state.user = None

if "last_activity" not in st.session_state:
    st.session_state.last_activity = None

# =========================
# TIMEOUT
# =========================
if st.session_state.user:
    if st.session_state.last_activity:
        if time.time() - st.session_state.last_activity > SESSION_TIMEOUT:
            st.session_state.user = None
            st.warning("Session habis")
            st.rerun()

    st.session_state.last_activity = time.time()

# =========================
# AUTH (LOGIN / REGISTER)
# =========================
if st.session_state.user is None:
    st.markdown(f"""
    <div style="text-align:center; margin-top:60px;">
        <img src="data:image/png;base64,{logo_base64}" width="140" style="margin-bottom:20px;">
        <h1 style="color:white;">Satria Moeda AI System</h1>
        <p style="color:gray;">Smart Training Assistant</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        menu = st.radio("", ["Login", "Register"], horizontal=True)

    col1, col2, col3 = st.columns([1,2,1])

    with col2:
        if menu == "Login":
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")

            if st.button("Login", use_container_width=True):
                user = login_user(u, p)
                if user:
                    st.session_state.user = user
                    st.session_state.last_activity = time.time()
                    st.success("Login berhasil")
                    st.rerun()
                else:
                    st.error("Username / Password salah")

        else:
            u = st.text_input("Username")
            p = st.text_input("Password", type="password")
            w = st.number_input("Weight", 30, 150, 70)
            h = st.number_input("Height", 1.4, 2.2, 1.7)

            if st.button("Register", use_container_width=True):
                if register_user(u, p, w, h):
                    st.success("Registrasi berhasil")
                else:
                    st.error("Username sudah ada")

    st.stop()

# =========================
# USER
# =========================
user = st.session_state.user

# Simpan height & weight di session state agar aman diakses di halaman lain
if "height" not in st.session_state:
    st.session_state.height = float(user.get("height", 1.75))
if "weight" not in st.session_state:
    st.session_state.weight = float(user.get("weight", 70.0))

# =========================
# SIDEBAR
# =========================
st.sidebar.markdown(f"""
<div style='text-align:center;'>
    <img src="data:image/png;base64,{logo_base64}" width="120">
    <h3>Satria Moeda</h3>
</div>
""", unsafe_allow_html=True)

if "page" not in st.session_state:
    st.session_state.page = "Home"

st.sidebar.markdown("---")
menu = st.sidebar.radio(
    "Navigation",
    ["Home", "Training Plan", "Progress", "Profile", "Logout"],
    index=["Home", "Training Plan", "Progress", "Profile", "Logout"].index(
        st.session_state.page
    )
)

st.session_state.page = menu
st.sidebar.markdown("---")
st.sidebar.write(f"👤 {user['username']}")

# =========================
# HOME
# =========================
if menu == "Home":
    st.markdown(f"""
    <div style='text-align:center; margin-top:20px;'>
        <img src="data:image/png;base64,{logo_base64}" width="140">
        <h1>MMA AI Assistant</h1>
        <p style='color:gray;'>Smart Training Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.subheader("📖 Cara Menggunakan Aplikasi")

    st.info("""
    Aplikasi ini direkomendasikan digunakan SETELAH Anda menyelesaikan sesi latihan.
    
    Tujuan sistem adalah membantu mengevaluasi kondisi tubuh, tingkat kelelahan,
    dan memberikan rekomendasi pemulihan maupun latihan berikutnya.
    """)

    st.markdown("""
    ### Langkah Penggunaan

    **1. Selesaikan latihan terlebih dahulu**
    - MMA, Boxing, Muay Thai, BJJ, Wrestling, Running, Strength Training, HIIT

    **2. Masukkan data latihan**
    - Jenis latihan, durasi, jam tidur, berat & tinggi badan

     **3. Klik tombol Generate**
    - Sistem menghitung Fatigue Score, Training Load, Kalori, BMI, HR Mean, dan Performance Score

    **4. Baca rekomendasi AI Coach & pantau progress**
    """)

    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        if st.button("Let's Start !", use_container_width=True):
            st.session_state.page = "Training Plan"
            st.rerun()

# =========================
# TRAINING PLAN
# =========================
elif menu == "Training Plan":
    st.markdown(f"""
    <div style='text-align:center; margin-top:20px;'>
        <img src="data:image/png;base64,{logo_base64}" width="120">
        <h1>MMA AI Assistant</h1>
        <p style='color:gray;'>Smart Training Recommendation System</p>
    </div>
    """, unsafe_allow_html=True)

    st.caption("Powered by Machine Learning & LLM (OpenRouter)")

    goal = st.selectbox("🎯 Goal", ["cutting", "bulking", "maintaining"])
    sport = st.selectbox("🏋️ Sport Type", [
        "mma","boxing","muay_thai","bjj","wrestling",
        "running","cycling","strength_training","hiit","cardio","rest"
    ])
    duration = st.number_input("⏱️ Duration (menit)", min_value=0, max_value=10000, value=60)
    if duration > 600:
        st.warning("⚠️ Durasi sangat tinggi, pastikan ini benar.")
    sleep = st.number_input("😴 Sleep", 0.0, 12.0, 7.0)
    weight = st.number_input("⚖️ Weight", 30, 150, int(user["weight"]))
    height = st.number_input("📏 Height", 1.4, 2.2, float(user["height"]))

if st.button("🚀 Generate"):
        with st.spinner("Melakukan Analisis..."):
            f = map_user_to_model_features(
                duration, sleep, weight, height, goal, sport
            )

            model_input = pd.DataFrame([{
                "bmi": float(f.get("bmi", 24.5)),
                "calories": float(f.get("calories", 0.0)),
                "duration": float(f.get("duration", 0.0)),
                "sleep_hours": float(f.get("sleep_hours", 7.0)),
                "hr_mean": float(f.get("hr_mean", 100.0)),
                "hr_max": float(f.get("hr_max", 150.0)),
                "goal_cutting": int(f.get("goal_cutting", 0)),        
                "goal_bulking": int(f.get("goal_bulking", 0)),        
                "goal_maintaining": int(f.get("goal_maintaining", 0))
            }])

            fatigue = model.predict(model_input)[0]

            flags = detect_unrealistic_training(
                duration=f["duration"],
                hr_mean=f["hr_mean"],
                training_load=f["training_load"]
            )

            fatigue = adjust_fatigue(fatigue, flags)

        save_progress({
            "date": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "username": user["username"],
            "goal": goal,
            "sport": sport,
            "fatigue": fatigue,
            "training_load": f["training_load"],
            "calories": f["calories"],
            "weight": weight,
            "sleep": sleep,
            "bmi": f["bmi"],
            "hr_mean": f["hr_mean"],
            "performance_score": f["performance_score"]
        })

        update_user_profile(user["username"], weight, height)
        st.session_state.weight = float(weight)
        st.session_state.height = float(height)

        st.subheader("📊 Hasil")

        col1, col2, col3 = st.columns(3)
        col1.metric("Fatigue", f"{fatigue:.2f}")
        col2.metric("Load", f"{f['training_load']:.0f}")
        col3.metric("Calories", f"{f['calories']:.0f}")

        col1, col2 = st.columns(2)
        col1.metric("BMI", f"{f['bmi']:.2f}")
        col2.metric("HR Mean", f"{f['hr_mean']:.0f}")

        st.metric("Performance Score", f"{f['performance_score']:.0f}")

        if fatigue > 80:
            st.error("Overtraining Risk")
        elif fatigue < 40:
            st.success("Ready for Training")

        st.subheader("🤖 AI Coach")

        try:
            coach = generate_ai_coach(
                goal, fatigue, f["training_load"], sleep, f["bmi"], f["hr_mean"]
            )
            if coach.startswith("⚠️ ERROR API"):
                coach = generate_coach_response(
                    goal, fatigue, f["training_load"], sleep, f["bmi"], f["hr_mean"]
                )
        except:
            coach = generate_coach_response(
                goal, fatigue, f["training_load"], sleep, f["bmi"]
            )

        st.markdown(f"<div class='card'>{coach}</div>", unsafe_allow_html=True)

# =========================
# PROGRESS
# =========================
elif menu == "Progress":
    st.title("📈 Progress Tracker")

    df = load_progress()

    if df.empty:
        st.warning("Belum ada data progress")
        st.stop()

    df["username"] = df["username"].astype(str)
    df = df[df["username"] == str(user["username"])]

    if df.empty:
        st.info("Belum ada data untuk user ini")
        st.stop()

    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.dropna(subset=["date"])
    df = df.sort_values("date")

    st.subheader("🎯 Filter")
    goal_list = ["All"] + df["goal"].unique().tolist()
    selected_goal = st.selectbox("Pilih Goal", goal_list)

    if selected_goal != "All":
        df = df[df["goal"] == selected_goal]

    st.subheader("📋 Data Terakhir")
    st.dataframe(df.tail(10), use_container_width=True)

    latest = df.iloc[-1]

    col1, col2, col3 = st.columns(3)
    col1.metric("Fatigue", f"{latest['fatigue']:.2f}")
    col2.metric("Training Load", f"{latest['training_load']:.0f}")
    col3.metric("Weight", f"{latest['weight']:.1f} kg")

    col1, col2 = st.columns(2)
    user_height = st.session_state.get("height", float(user.get("height", 1.75)))
    current_weight = latest.get("weight", 0)
    bmi_value = current_weight / (user_height ** 2) if user_height and user_height > 0 else 0

    col1.metric("BMI", f"{bmi_value:.2f}")
    col2.metric("Rata-rata Heart Rate", f"{latest['hr_mean']:.0f}")

    if "performance_score" in latest and pd.notna(latest["performance_score"]):
        perf_score = latest["performance_score"]
    else:
        sleep_val = latest.get("sleep", 7)
        load_val = latest.get("training_load", 100)
        hr_val = latest.get("hr_mean", 120)
        
        intensity = min(100, (hr_val / 190) * 100)
        sleep_score = min(100, (sleep_val / 8) * 100)
        perf_score = (0.4 * intensity) + (0.4 * sleep_score) + (0.2 * (load_val / 100))

    st.metric("Performance Score", f"{perf_score:.0f}")

    st.subheader("⚡ Performance Score")
    perf = max(0, min(100, perf_score))
    st.progress(int(perf))

    if perf > 80:
        st.success(f"🔥 Peak Performance ({perf:.0f})")
    elif perf > 60:
        st.info(f"⚡ Good Performance ({perf:.0f})")
    elif perf > 40:
        st.warning(f"⚠️ Moderate ({perf:.0f})")
    else:
        st.error(f"❌ Low Performance ({perf:.0f})")

    st.subheader("Grafik Progress Fatigue")
    st.line_chart(df.set_index("date")[["fatigue"]])
    st.subheader("Grafik Progress Training Load")
    st.line_chart(df.set_index("date")[["training_load"]])
    st.subheader("Grafik Progress Berat Badan")
    st.line_chart(df.set_index("date")[["weight"]])

    st.subheader("🧠 AI Insight")
    try:
        with st.spinner("Menyiapkan Insight..."):
            insight = generate_progress_insight(df)
    except:
        insight = "⚠️ AI tidak tersedia"

    st.info(insight)

    st.subheader("🏋️ Weekly Training Plan")
    goal_for_plan = selected_goal if selected_goal != "All" else latest["goal"]

    try:
        with st.spinner("Menyusun program latihan..."):
            plan = generate_weekly_plan(
                goal=goal_for_plan,
                fatigue=latest["fatigue"]
            )
    except:
        plan = ["AI tidak tersedia"]

    if not isinstance(plan, list):
        plan = [str(plan)]

    st.markdown("<div class='card'>", unsafe_allow_html=True)
    for day in plan:
        st.markdown(f"<p style='color:white; margin:5px 0;'>{day}</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# =========================
# PROFILE
# =========================
elif menu == "Profile":
    st.title("👤 Profile")

    w = st.number_input("Weight", 30, 150, int(user["weight"]))
    h = st.number_input("Height", 1.4, 2.2, float(user["height"]))

    if st.button("Update"):
        update_user_profile(user["username"], w, h)
        st.session_state.weight = float(w)
        st.session_state.height = float(h)
        st.success("Updated")

# =========================
# LOGOUT
# =========================
elif menu == "Logout":
    st.session_state.user = None
    st.success("Logout berhasil")
    st.rerun()
