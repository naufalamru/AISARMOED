import streamlit as st
import pandas as pd
import datetime
import time
import base64

from utils import *
from logic import *

SESSION_TIMEOUT = 1200

# =====================================================
# PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="Satria Moeda AI System",
    layout="wide"
)

# =====================================================
# LOGO
# =====================================================

def get_base64_image(path):
    with open(path, "rb") as img:
        return base64.b64encode(img.read()).decode()

logo_base64 = get_base64_image("logo.png")

# =====================================================
# STYLE
# =====================================================

st.markdown("""
<style>

.stApp{
    background:#0f0f0f;
}

section[data-testid="stSidebar"]{
    background:#b30000;
}

section[data-testid="stSidebar"] *{
    color:white;
}

h1,h2,h3,h4,h5,h6,p,label,span{
    color:white;
}

.stButton>button{
    background:#ff1a1a;
    color:white;
    border:none;
    border-radius:12px;
    height:55px;
    font-weight:bold;
}

.card{
    background:#1b1b1b;
    border-radius:12px;
    padding:20px;
    color:white;
}

[data-testid="metric-container"]{
    background:#1b1b1b;
    border-radius:12px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

# =====================================================
# SESSION
# =====================================================

if "user" not in st.session_state:
    st.session_state.user = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "last_activity" not in st.session_state:
    st.session_state.last_activity = None

# =====================================================
# AUTO LOGOUT
# =====================================================

if st.session_state.user:

    if st.session_state.last_activity:

        if time.time()-st.session_state.last_activity > SESSION_TIMEOUT:

            st.session_state.user=None
            st.warning("Session berakhir.")
            st.rerun()

    st.session_state.last_activity=time.time()

# =====================================================
# LOGIN REGISTER
# =====================================================

if st.session_state.user is None:

    st.markdown(f"""
    <div style="text-align:center;margin-top:60px">

    <img src="data:image/png;base64,{logo_base64}" width="140">

    <h1>Satria Moeda AI System</h1>

    <p>Smart Training Recommendation System</p>

    </div>
    """, unsafe_allow_html=True)

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        menu=st.radio(
            "",
            ["Login","Register"],
            horizontal=True
        )

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        if menu=="Login":

            username=st.text_input("Username")

            password=st.text_input(
                "Password",
                type="password"
            )

            if st.button(
                "Login",
                use_container_width=True
            ):

                user=login_user(
                    username,
                    password
                )

                if user:

                    st.session_state.user=user
                    st.session_state.last_activity=time.time()

                    st.success("Login berhasil")
                    st.rerun()

                else:

                    st.error("Username atau Password salah")

        else:

            username=st.text_input("Username")

            password=st.text_input(
                "Password",
                type="password"
            )

            weight=st.number_input(
                "Weight",
                30,
                150,
                70
            )

            height=st.number_input(
                "Height",
                1.40,
                2.20,
                1.70
            )

            if st.button(
                "Register",
                use_container_width=True
            ):

                ok=register_user(
                    username,
                    password,
                    weight,
                    height
                )

                if ok:

                    st.success("Registrasi berhasil")

                else:

                    st.error("Username sudah digunakan")

    st.stop()

# =====================================================
# USER
# =====================================================

user=st.session_state.user

if "weight" not in st.session_state:
    st.session_state.weight=float(user["weight"])

if "height" not in st.session_state:
    st.session_state.height=float(user["height"])

# =====================================================
# SIDEBAR
# =====================================================

st.sidebar.markdown(f"""

<div style="text-align:center">

<img src="data:image/png;base64,{logo_base64}" width="120">

<h3>Satria Moeda</h3>

</div>

""", unsafe_allow_html=True)

menu=st.sidebar.radio(

"Navigation",

[
"Home",
"Training Plan",
"Progress",
"Profile",
"Logout"
],

index=[
"Home",
"Training Plan",
"Progress",
"Profile",
"Logout"
].index(
st.session_state.page
)

)

st.session_state.page=menu

st.sidebar.markdown("---")

st.sidebar.write(f"👤 {user['username']}")

# =====================================================
# HOME
# =====================================================

if menu == "Home":

    st.markdown(f"""
    <div style='text-align:center;margin-top:20px;'>

    <img src="data:image/png;base64,{logo_base64}" width="140">

    <h1>MMA AI Assistant</h1>

    <p>Smart Training Recommendation System</p>

    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.subheader("📖 Cara Menggunakan")

    st.info("""

Gunakan aplikasi setelah menyelesaikan sesi latihan.

Sistem akan menghitung indikator kondisi latihan berdasarkan teori
Fitness-Fatigue Model kemudian memberikan rekomendasi latihan
menggunakan Large Language Model.

""")

    st.markdown("""

### Langkah Penggunaan

1. Pilih Goal

2. Pilih Jenis Latihan

3. Masukkan Durasi Latihan

4. Masukkan Jam Tidur

5. Masukkan Berat dan Tinggi Badan

6. Klik Generate

Sistem akan menghasilkan:

- Training Load
- Recovery Score
- Readiness Score
- Estimasi Kalori
- BMI
- Heart Rate

Kemudian AI Coach memberikan rekomendasi latihan berikutnya.

""")

    col1,col2,col3=st.columns([1,2,1])

    with col2:

        if st.button(
            "Let's Start",
            use_container_width=True
        ):

            st.session_state.page="Training Plan"
            st.rerun()

# =====================================================
# TRAINING PLAN
# =====================================================

elif menu=="Training Plan":

    st.markdown(f"""

<div style="text-align:center">

<img src="data:image/png;base64,{logo_base64}" width="120">

<h1>MMA AI Assistant</h1>

<p>Training Recommendation System</p>

</div>

""",unsafe_allow_html=True)

    st.caption("Powered by Fitness-Fatigue Model & OpenRouter")

    goal=st.selectbox(

        "🎯 Goal",

        [
            "cutting",
            "bulking",
            "maintaining"
        ]

    )

    sport=st.selectbox(

        "🥊 Sport",

        [

        "mma",

        "boxing",

        "muay_thai",

        "bjj",

        "wrestling",

        "running",

        "cycling",

        "strength_training",

        "hiit",

        "cardio",

        "rest"

        ]

    )

    duration=st.number_input(

        "⏱ Duration (Minute)",

        min_value=0,

        max_value=300,

        value=60

    )

    sleep=st.number_input(

        "😴 Sleep (Hour)",

        min_value=0.0,

        max_value=12.0,

        value=7.0

    )

    weight=st.number_input(

        "⚖ Weight",

        30,

        150,

        int(user["weight"])

    )

    height=st.number_input(

        "📏 Height",

        1.40,

        2.20,

        float(user["height"])

    )

    if st.button(

        "🚀 Generate",

        use_container_width=True

    ):

        metrics=calculate_training_metrics(

            duration=duration,

            sleep=sleep,

            weight=weight,

            height=height,

            goal=goal,

            sport=sport

        )

        save_progress({

            "username":user["username"],

            "goal":goal,

            "date":datetime.datetime.now(),

            "training_load":metrics["training_load"],

            "recovery_score":metrics["recovery_score"],

            "readiness_score":metrics["readiness_score"],

            "weight":weight,

            "sleep":sleep,

            "hr_mean":metrics["hr_mean"]

        })

        update_user_profile(

            user["username"],

            weight,

            height

        )

        st.session_state.weight=weight
        st.session_state.height=height

        st.markdown("---")

        st.subheader("📊 Training Analysis")

        col1,col2,col3=st.columns(3)

        col1.metric(

            "Training Load",

            f"{metrics['training_load']:.1f}"

        )

        col2.metric(

            "Recovery Score",

            f"{metrics['recovery_score']:.1f}"

        )

        col3.metric(

            "Readiness Score",

            f"{metrics['readiness_score']:.1f}"

        )

        col1,col2,col3=st.columns(3)

        col1.metric(

            "Calories",

            f"{metrics['calories']:.0f}"

        )

        col2.metric(

            "BMI",

            f"{metrics['bmi']:.2f}"

        )

        col3.metric(

            "Heart Rate",

            f"{metrics['hr_mean']:.0f}"

        )
        readiness=metrics["readiness_score"]

        if readiness>=80:

            st.success("🟢 Ready for High Intensity Training")

        elif readiness>=60:

            st.info("🟡 Ready for Moderate Training")

        elif readiness>=40:

            st.warning("🟠 Reduce Training Volume")

        else:

            st.error("🔴 Recovery Recommended")
        st.markdown("---")

        st.subheader("🤖 AI Coach")

        try:

            coach=generate_ai_coach(

                goal=goal,

                training_load=metrics["training_load"],

                recovery_score=metrics["recovery_score"],

                readiness_score=metrics["readiness_score"],

                sleep=sleep,

                bmi=metrics["bmi"],

                hr_mean=metrics["hr_mean"]

            )

        except:

            coach="AI tidak tersedia."

        st.markdown(

            f"<div class='card'>{coach}</div>",

            unsafe_allow_html=True

        )
# =====================================================
# PROGRESS
# =====================================================

elif menu == "Progress":

    st.title("📈 Progress Tracker")

    df = load_progress(user["username"])

    if df.empty:

        st.warning("Belum ada data progress.")

        st.stop()

    df["date"] = pd.to_datetime(df["date"])

    df = df.sort_values("date")

    st.subheader("📋 Data Terbaru")

    st.dataframe(
        df.tail(10),
        use_container_width=True
    )

    latest = df.iloc[-1]

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Training Load",
        f"{latest['training_load']:.1f}"
    )

    col2.metric(
        "Recovery Score",
        f"{latest['recovery_score']:.1f}"
    )

    col3.metric(
        "Readiness Score",
        f"{latest['readiness_score']:.1f}"
    )

    col1,col2,col3 = st.columns(3)

    col1.metric(
        "Weight",
        f"{latest['weight']:.1f} kg"
    )

    bmi = latest["weight"] / (
        st.session_state.height ** 2
    )

    col2.metric(
        "BMI",
        f"{bmi:.2f}"
    )

    col3.metric(
        "Heart Rate",
        f"{latest['hr_mean']:.0f}"
    )

    st.markdown("---")

    st.subheader("📊 Training Load")

    st.line_chart(
        df.set_index("date")["training_load"]
    )

    st.subheader("💤 Recovery Score")

    st.line_chart(
        df.set_index("date")["recovery_score"]
    )

    st.subheader("⚡ Readiness Score")

    st.line_chart(
        df.set_index("date")["readiness_score"]
    )

    st.subheader("⚖ Weight")

    st.line_chart(
        df.set_index("date")["weight"]
    )

    st.markdown("---")

    st.subheader("🧠 AI Progress Insight")

    try:

        insight = generate_progress_insight(df)

    except:

        insight = "AI tidak tersedia."

    st.markdown(

        f"<div class='card'>{insight}</div>",

        unsafe_allow_html=True

    )

    st.markdown("---")

    st.subheader("📅 Weekly Training Plan")

    try:

        weekly = generate_weekly_plan(

            goal=latest["goal"],

            training_load=latest["training_load"],

            recovery_score=latest["recovery_score"],

            readiness_score=latest["readiness_score"]

        )

    except:

        weekly = "AI tidak tersedia."

    st.markdown(

        f"<div class='card'>{weekly}</div>",

        unsafe_allow_html=True

    )


# =====================================================
# PROFILE
# =====================================================

elif menu == "Profile":

    st.title("👤 Profile")

    weight = st.number_input(

        "Weight",

        30,

        150,

        int(st.session_state.weight)

    )

    height = st.number_input(

        "Height",

        1.40,

        2.20,

        float(st.session_state.height)

    )

    if st.button(

        "Update Profile",

        use_container_width=True

    ):

        update_user_profile(

            user["username"],

            weight,

            height

        )

        st.session_state.weight = weight

        st.session_state.height = height

        st.success("Profile berhasil diperbarui.")


# =====================================================
# LOGOUT
# =====================================================

elif menu == "Logout":

    st.session_state.user = None

    st.session_state.page = "Home"

    st.success("Logout berhasil.")

    st.rerun()
