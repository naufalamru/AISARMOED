from ai_service import ask_ai

# =====================================================
# AI COACH
# =====================================================

def generate_ai_coach(
    goal,
    training_load,
    recovery_score,
    readiness_score,
    sleep,
    bmi,
    hr_mean
):

    prompt = f"""
Anda adalah pelatih Strength & Conditioning MMA profesional.

Data Atlet

- Goal : {goal}
- Training Load : {training_load:.2f}
- Recovery Score : {recovery_score:.2f}/100
- Readiness Score : {readiness_score:.2f}/100
- Sleep Hours : {sleep}
- BMI : {bmi:.2f}
- Average Heart Rate : {hr_mean:.0f}

Tugas

1. Analisis kondisi atlet.
2. Jelaskan risiko latihan.
3. Berikan rekomendasi latihan berikutnya.

Aturan

- Gunakan Bahasa Indonesia.
- Jangan memberi salam.
- Jangan menjelaskan AI.
- Fokus pada sport science.
- Jika Recovery Score rendah, prioritaskan recovery.
- Jika Readiness tinggi, latihan dapat ditingkatkan bertahap.
- Jika tidur < 6 jam, prioritaskan pemulihan.

Format

📊 Analisis Kondisi
...

⚠️ Risiko
...

✅ Rekomendasi
...
"""

    return ask_ai(prompt)

# =====================================================
# AI PROGRESS
# =====================================================

def generate_progress_insight(df):

    if df.empty:
        return "Belum ada data."

    latest = df.iloc[-1]

    prompt = f"""
Anda adalah Performance Analyst atlet MMA.

Data Terakhir

Goal : {latest['goal']}

Training Load : {latest['training_load']}

Recovery Score : {latest['recovery_score']}

Readiness Score : {latest['readiness_score']}

Weight : {latest['weight']}

Sleep : {latest['sleep']}

Heart Rate : {latest['hr_mean']}

Tugas

Evaluasi kondisi atlet berdasarkan data tersebut.

Format

📈 Progress

...

⚠️ Potensi Masalah

...

✅ Saran

...
"""

    return ask_ai(prompt)

# =====================================================
# WEEKLY PLAN
# =====================================================

def generate_weekly_plan(goal, readiness_score):

    prompt = f"""
Anda adalah pelatih MMA profesional.

Data Atlet

Goal : {goal}

Readiness Score : {readiness_score}/100

Buat program latihan selama 7 hari.

Aturan

- Gunakan Bahasa Indonesia.
- Jangan memberi salam.
- Maksimal dua kalimat setiap hari.
- Sesuaikan intensitas dengan Readiness Score.
- Jika readiness rendah, tambahkan recovery.
- Jika readiness tinggi, naikkan intensitas bertahap.

Format

Day 1

Fokus

Latihan

Day 2

...

Day 7

...

Kesimpulan

...
"""

    response = ask_ai(prompt)

    return response.split("\n")

# =====================================================
# RULE BASED BACKUP
# =====================================================

def generate_coach_response(
    goal,
    training_load,
    recovery_score,
    readiness_score,
    sleep,
    bmi,
    hr_mean=None
):

    if readiness_score >= 80:
        return (
            "🟢 Kondisi tubuh sangat baik. "
            "Latihan intensitas tinggi masih dapat dilakukan secara bertahap."
        )

    if readiness_score >= 60:
        return (
            "🟡 Kondisi tubuh cukup baik. "
            "Pertahankan volume latihan dan monitor pemulihan."
        )

    if readiness_score >= 40:
        return (
            "🟠 Kesiapan latihan sedang. "
            "Disarankan mengurangi volume atau intensitas latihan."
        )

    return (
        "🔴 Recovery menjadi prioritas utama sebelum kembali menjalani latihan berat."
    )

# =====================================================
# RULE BASED PROGRESS
# =====================================================

def generate_progress_insight_backup(df):

    if df.empty:
        return "Belum ada data."

    avg = df["readiness_score"].mean()

    if avg >= 80:
        return (
            "Kondisi latihan sangat baik. Atlet memiliki kesiapan latihan yang tinggi."
        )

    if avg >= 60:
        return (
            "Kondisi latihan cukup stabil. Pertahankan keseimbangan latihan dan recovery."
        )

    if avg >= 40:
        return (
            "Recovery mulai menurun. Kurangi volume latihan untuk sementara."
        )

    return (
        "Recovery rendah. Disarankan meningkatkan waktu istirahat sebelum latihan berikutnya."
    )
