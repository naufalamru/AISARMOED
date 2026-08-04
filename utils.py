import pandas as pd
import streamlit as st
from supabase import create_client, Client

# ==========================================================
# SUPABASE
# ==========================================================

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)

# ==========================================================
# USER
# ==========================================================

def load_users():

    try:

        response = (
            supabase
            .table("users")
            .select("*")
            .execute()
        )

        if response.data:

            return pd.DataFrame(response.data)

    except:
        pass

    return pd.DataFrame(
        columns=[
            "username",
            "password",
            "weight",
            "height"
        ]
    )


def login_user(username,password):

    try:

        response=(
            supabase
            .table("users")
            .select("*")
            .eq("username",username)
            .eq("password",password)
            .execute()
        )

        if response.data:

            return response.data[0]

    except:
        pass

    return None


def register_user(username,password,weight,height):

    try:

        exist=(
            supabase
            .table("users")
            .select("username")
            .eq("username",username)
            .execute()
        )

        if exist.data:

            return False

        supabase.table("users").insert({

            "username":username,
            "password":password,
            "weight":weight,
            "height":height

        }).execute()

        return True

    except:

        return False


def update_user_profile(username,weight,height):

    try:

        (
            supabase
            .table("users")
            .update({

                "weight":weight,
                "height":height

            })
            .eq("username",username)
            .execute()
        )

    except:
        pass

# ==========================================================
# PROGRESS
# ==========================================================

def save_progress(data):

    payload={

        "username":data.get("username"),

        "goal":data.get("goal"),

        "date":data.get("date"),

        "training_load":data.get("training_load"),

        "recovery_score":data.get("recovery_score"),

        "readiness_score":data.get("readiness_score"),

        "weight":data.get("weight"),

        "sleep":data.get("sleep"),

        "hr_mean":data.get("hr_mean")

    }

    try:

        supabase.table(
            "progress"
        ).insert(payload).execute()

        return {"status":"success"}

    except Exception as e:

        return {

            "status":"error",

            "message":str(e)

        }


def load_progress(username=None):

    try:

        query=(
            supabase
            .table("progress")
            .select("*")
        )

        if username:

            query=query.eq(
                "username",
                username
            )

        response=query.execute()

        if response.data:

            return pd.DataFrame(
                response.data
            )

    except:
        pass

    return pd.DataFrame(
        columns=[
            "username",
            "goal",
            "date",
            "training_load",
            "recovery_score",
            "readiness_score",
            "weight",
            "sleep",
            "hr_mean"
        ]
    )

# ==========================================================
# FITNESS FATIGUE MODEL
# ==========================================================

def calculate_training_metrics(
    duration,
    sleep,
    weight,
    height,
    goal,
    sport
):

    bmi = weight / (height ** 2)

    met_table = {

        "mma":10,

        "boxing":9,

        "muay_thai":10,

        "bjj":8,

        "wrestling":9,

        "running":8,

        "cycling":7,

        "strength_training":6,

        "hiit":9,

        "cardio":7,

        "rest":1

    }

    met = met_table.get(sport,6)

    calories = met * weight * (duration / 60)

    hr_mean = 70 + (met * 5)

    hr_max = hr_mean + 20

    # ===========================================
    # Training Load
    # Foster (1998)
    # ===========================================

    training_load = duration * met

    # ===========================================
    # Recovery Score
    # ===========================================

    sleep_score = min(
        100,
        (sleep / 8) * 100
    )

    recovery_score = sleep_score

    # ===========================================
    # Readiness Score
    # Fitness Fatigue Model
    # ===========================================

    readiness_score = (

        (0.5 * recovery_score)

        +

        (0.3 * (100 - min(training_load/6,100)))

        +

        (0.2 * (100 - abs(hr_mean-120)))

    )

    readiness_score=max(
        0,
        min(
            readiness_score,
            100
        )
    )

    if goal=="cutting":

        calories*=0.90

    elif goal=="bulking":

        calories*=1.10

    elif goal=="maintaining":

        calories*=1.00

    return{

        "training_load":training_load,

        "recovery_score":recovery_score,

        "readiness_score":readiness_score,

        "calories":calories,

        "bmi":bmi,

        "hr_mean":hr_mean,

        "hr_max":hr_max

    }
