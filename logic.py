from ai_service import ask_ai


# =========================
# AI COACH (REAL AI)
# =========================
def generate_ai_coach(goal, fatigue, load, sleep, bmi, hr_mean):

    prompt = f"""
    Anda adalah pelatih Strength & Conditioning MMA profesional.

    Data Atlet:
    - Goal: {goal}
    - Fatigue Score: {fatigue}/100
    - Training Load: {load}
    - Sleep Hours: {sleep}
    - BMI: {bmi}
    - Average Heart Rate: {hr_mean}

    Tugas:
    1. Analisis kondisi atlet.
    2. Jelaskan risiko yang mungkin muncul.
    3. Berikan rekomendasi latihan berikutnya.

    Aturan:
    - Gunakan Bahasa Indonesia.
    - Jangan memberikan salam.
    - Jangan menjelaskan AI atau model.
    - Fokus pada sport science.
    - Jika fatigue > 80, prioritaskan recovery.
    - Jika fatigue 60–80, kurangi volume latihan.
    - Jika fatigue < 40, atlet siap meningkatkan intensitas.
    - Jika tidur < 6 jam, prioritaskan pemulihan.
    - Jawaban maksimal 200 kata.

    Format:

    📊 Analisis Kondisi
    ...

    ⚠️ Risiko
    ...

    🥊 Rekomendasi Latihan
    ...
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
    Anda adalah Performance Analyst untuk atlet MMA.

    Data Terakhir:
    - Goal: {latest['goal']}
    - Fatigue: {latest['fatigue']}
    - Training Load: {latest['training_load']}
    - Weight: {latest['weight']}
    - Sleep: {latest['sleep']}
    - HR Mean: {latest['hr_mean']}

    Tugas:
    Evaluasi kondisi atlet berdasarkan data tersebut.

    Aturan:
    - Gunakan Bahasa Indonesia.
    - Maksimal 150 kata.
    - Jangan memberi salam.
    - Fokus pada progres latihan dan recovery.
    - Berikan insight yang mudah dipahami atlet.

    Format:

    📈 Progress
    ...

    🚨 Potensi Masalah
    ...

    ✅ Saran Perbaikan
    ...
    """

    return ask_ai(prompt)


# =========================
# AI WEEKLY PLAN
# =========================
def generate_weekly_plan(goal, fatigue):

    prompt = f"""
    Anda adalah pelatih MMA profesional.

    Data Atlet:
    - Goal: {goal}
    - Fatigue Score: {fatigue}/100

    Tugas:
    Buat program latihan selama 7 hari.

    Aturan:
    - Gunakan Bahasa Indonesia.
    - Jangan memberi salam.
    - Setiap hari maksimal 2 kalimat.
    - Sesuaikan intensitas dengan fatigue.
    - Jika fatigue tinggi, tambahkan recovery day.
    - Jika fatigue rendah, boleh meningkatkan intensitas bertahap.
    - Hindari latihan yang berisiko cedera.
    - Sertakan latihan teknik MMA, conditioning, dan recovery bila diperlukan.

    Format:

    Day 1
    Fokus:
    Latihan:

    Day 2
    Fokus:
    Latihan:

    Day 3
    Fokus:
    Latihan:

    Day 4
    Fokus:
    Latihan:

    Day 5
    Fokus:
    Latihan:

    Day 6
    Fokus:
    Latihan:

    Day 7
    Fokus:
    Latihan:

    Kesimpulan:
    ...
    """

    response = ask_ai(prompt)

    return response.split("\n")


# =========================
# RULE-BASED BACKUP COACH
# =========================
def generate_coach_response(goal, fatigue, load, sleep, bmi, hr_mean=None):

    if fatigue > 80:
        return "⚠️ Overtraining terdeteksi. Prioritaskan recovery dan istirahat."

    if fatigue > 60:
        return "🔥 Fatigue cukup tinggi. Kurangi volume latihan pada sesi berikutnya."

    if fatigue < 40:
        return "💪 Kondisi cukup baik. Intensitas latihan dapat ditingkatkan secara bertahap."

    if sleep < 6:
        return "😴 Durasi tidur rendah. Fokus pada pemulihan dan kualitas tidur."

    if goal == "cutting":
        return "🔥 Fokus pada fat loss, conditioning, dan pengaturan kalori."

    if goal == "bulking":
        return "🍗 Fokus pada strength training dan hypertrophy."

    if goal == "maintaining":
        return "⚖️ Fokus menjaga performa, kebugaran, dan recovery yang seimbang."

    return "🏃 Fokus pada latihan umum dan peningkatan kebugaran."


# =========================
# RULE-BASED BACKUP INSIGHT
# =========================
def generate_progress_insight_backup(df):

    if df.empty:
        return "Belum ada data."

    avg = df["fatigue"].mean()

    if avg > 70:
        return "⚠️ Fatigue rata-rata tinggi. Risiko overtraining dan cedera meningkat."

    return "✅ Progress latihan relatif stabil dan terkendali."
