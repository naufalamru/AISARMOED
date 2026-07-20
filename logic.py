from ai_service import ask_ai


# =========================
# AI COACH (REAL AI)
# =========================
def generate_ai_coach(goal, fatigue, load, sleep, bmi, hr_mean):

   prompt = f"""
   Data Atlet:

   Goal: {goal}
   Fatigue Score: {fatigue}/100
   Training Load: {load}
   Sleep Hours: {sleep}
   BMI: {bmi}
   Average Heart Rate: {hr_mean}

   Tugas:
   1. Analisis kondisi atlet.
   2. Jelaskan risiko yang mungkin muncul.
   3. Berikan rekomendasi sesi latihan berikutnya.

   Format:

   📊 Analisis Kondisi
   ...

   ⚠️ Risiko
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
   - Bahasa Indonesia.
   - Maksimal 150 kata.
   - Tidak perlu salam.
   - Fokus pada progres latihan dan recovery.

   Format:

   📈 Progress
   (...)

   🚨 Potensi Masalah
   (...)

   ✅ Saran Perbaikan
   (...)
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

   Buat program latihan 7 hari.

   Aturan:
   - Bahasa Indonesia.
   - Jangan memberi salam.
   - Setiap hari maksimal 2 kalimat.
   - Sesuaikan volume latihan dengan fatigue.
   - Jika fatigue tinggi, tambahkan recovery day.
   - Jika fatigue rendah, boleh meningkatkan intensitas secara bertahap.
   - Jangan membuat latihan yang berbahaya.

   Format:

   Day 1:
   Fokus:
   Latihan:

   Day 2:
   Fokus:
   Latihan:

   ...
   sampai Day 7

   Tambahkan kesimpulan singkat di akhir.
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
