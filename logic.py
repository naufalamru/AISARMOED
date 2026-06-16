from ai_service import ask_ai


# =========================
# AI COACH (REAL AI)
# =========================
def generate_ai_coach(goal, fatigue, load, sleep, bmi, hr_mean):

    prompt = f"""
    no need to greet
    Always use Bahasa Indonesia
    Anda adalah pelatih MMA profesional.

    Data user:
    - Goal: {goal}
    - Fatigue: {fatigue}
    - Training Load: {load}
    - Sleep: {sleep}
    - BMI: {bmi}
    - Rata-rata Heart Rate: {hr_mean}

    Berikan:
    1. Analisis kondisi
    2. Risiko (jika ada)
    3. Saran latihan hari ini

    Gunakan bahasa santai tapi profesional serta singkat, padat, dan jelas.
    """

    return ask_ai(prompt)


# =========================
# AI PROGRESS INSIGHT
# =========================
def generate_progress_insight(df):

    if df.empty:
        return "Belum ada data."

    latest = df.iloc[-1]

    prompt = f"""
    no need greetings
    Always use Bahasa Indonesia
    Anda adalah AI physique training analyst.

    Data terakhir:
    - Goal: {latest['goal']}
    - Fatigue: {latest['fatigue']}
    - Training Load: {latest['training_load']}
    - Weight: {latest['weight']}
    - Sleep: {latest['sleep']}
    - HR Mean: {latest['hr_mean']}

    Analisis:
    - kondisi progress
    - apakah ada overtraining
    - saran perbaikan

    Jawab singkat, jelas, dan profesional.
    """

    return ask_ai(prompt)


# =========================
# AI WEEKLY PLAN
# =========================
def generate_weekly_plan(goal, fatigue):

    prompt = f"""
    Always use Bahasa Indonesia
    Buatkan program latihan selama 7 hari.

    Data:
    - Goal: {goal}
    - Fatigue: {fatigue}

    Format:
    Day 1: ...
    Day 2: ...
    sampai Day 7

    Sesuaikan intensitas dengan fatigue.
    """

    response = ask_ai(prompt)

    return response.split("\n")

def generate_coach_response(goal, fatigue, load, sleep, bmi, hr_mean=None):

    if fatigue > 80:
        return "⚠️ Overtraining! Hari ini wajib REST."

    if fatigue > 60:
        return "🔥 Intensitas tinggi, kurangi volume besok."

    if fatigue < 40:
        return "💪 Kondisi optimal, bisa tambah intensitas."

    if sleep < 6:
        return "😴 Kurang tidur, prioritaskan recovery."

    if goal == "cutting":
        return "🔥 Fokus fat loss + conditioning."

    if goal == "bulking":
        return "🍗 Fokus strength + hypertrophy."

    if goal == "maintaining":
        return "⚖️ Fokus menjaga berat badan, balance antara latihan & recovery."

    return "🏃 Fokus latihan umum."


def generate_progress_insight_backup(df):

    if df.empty:
        return "Belum ada data."

    avg = df["fatigue"].mean()

    if avg > 70:
        return "⚠️ Fatigue tinggi terus → risiko cedera."

    return "✅ Progress stabil."