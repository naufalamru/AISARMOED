from ai_service import ask_ai

# =====================================================
# AI COACH
# =====================================================

def generate_ai_coach(
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

Format Output yang Harus Ditiru Secara Konsisten (Mulai dari 📊 Analisis Kondisi):

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

Training Load : {latest['training_load']}

Recovery Score : {latest['recovery_score']}

Readiness Score : {latest['readiness_score']}

Weight : {latest['weight']}

Sleep : {latest['sleep']}

Heart Rate : {latest['hr_mean']}

Tugas

Evaluasi kondisi atlet berdasarkan data tersebut.

Format Output yang Harus Ditiru Secara Konsisten (Mulai dari 📈 Progress):

📈 Progress

...

⚠️ Potensi Masalah

...

✅ Saran

...
"""

    return ask_ai(prompt)

# ======================================================
# TEMPLATE PROGRAM LATIHAN
# ======================================================

def get_weekly_template(goal, sport):

    templates = {

        "mma": [
            ("Senin","Striking + Conditioning"),
            ("Selasa","Strength Training"),
            ("Rabu","Recovery"),
            ("Kamis","Grappling + Conditioning"),
            ("Jumat","Sparring"),
            ("Sabtu","Endurance"),
            ("Minggu","Recovery")
        ],

        "boxing":[
            ("Senin","Footwork & Padwork"),
            ("Selasa","Strength"),
            ("Rabu","Recovery"),
            ("Kamis","Heavy Bag"),
            ("Jumat","Sparring"),
            ("Sabtu","Roadwork"),
            ("Minggu","Recovery")
        ],

        "muay_thai":[
            ("Senin","Kick & Clinch"),
            ("Selasa","Strength"),
            ("Rabu","Recovery"),
            ("Kamis","Padwork"),
            ("Jumat","Sparring"),
            ("Sabtu","Conditioning"),
            ("Minggu","Recovery")
        ],

        "bjj":[
            ("Senin","Guard Passing"),
            ("Selasa","Strength"),
            ("Rabu","Recovery"),
            ("Kamis","Submission Drill"),
            ("Jumat","Rolling"),
            ("Sabtu","Grip Strength"),
            ("Minggu","Recovery")
        ],

        "wrestling":[
            ("Senin","Takedown Drill"),
            ("Selasa","Strength"),
            ("Rabu","Recovery"),
            ("Kamis","Chain Wrestling"),
            ("Jumat","Live Wrestling"),
            ("Sabtu","Conditioning"),
            ("Minggu","Recovery")
        ],

        "running":[
            ("Senin","Easy Run"),
            ("Selasa","Interval"),
            ("Rabu","Recovery"),
            ("Kamis","Tempo Run"),
            ("Jumat","Easy Run"),
            ("Sabtu","Long Run"),
            ("Minggu","Recovery")
        ],

        "strength_training":[
            ("Senin","Upper Body"),
            ("Selasa","Lower Body"),
            ("Rabu","Recovery"),
            ("Kamis","Push"),
            ("Jumat","Pull"),
            ("Sabtu","Full Body"),
            ("Minggu","Recovery")
        ],

        "hiit":[
            ("Senin","HIIT"),
            ("Selasa","Mobility"),
            ("Rabu","Recovery"),
            ("Kamis","HIIT"),
            ("Jumat","Circuit"),
            ("Sabtu","Conditioning"),
            ("Minggu","Recovery")
        ]
    }

    template = templates.get(sport, templates["mma"])

    return template

def generate_weekly_plan(
    sport,
    training_load,
    recovery_score,
    readiness_score
):

    template = get_weekly_template(goal, sport)

    template_text = ""

    for day, focus in template:

        template_text += f"""

{day}
Fokus : {focus}

"""

    prompt = f"""
Anda adalah pelatih Strength & Conditioning MMA profesional.

Data Atlet

Jenis Latihan : {sport}

Training Load : {training_load:.1f}

Recovery Score : {recovery_score:.1f}

Readiness Score : {readiness_score:.1f}


Berikut adalah template latihan yang SUDAH DITENTUKAN.

{template_text}

Tugas Anda

1. Jangan mengubah nama hari.
2. Jangan mengubah fokus latihan.
3. Tambahkan rekomendasi latihan pada setiap hari.
4. Sesuaikan volume dan intensitas berdasarkan:
   - Training Load
   - Recovery Score
   - Readiness Score

Aturan

- Bahasa Indonesia.
- Maksimal dua kalimat pada setiap hari.
- Tidak perlu memberi salam.
- Jangan menjelaskan AI.
- Recovery jika Recovery Score rendah.
- Intensitas tinggi hanya jika Readiness Score tinggi.
- Jangan mengubah urutan hari.

Format Output yang Harus Ditiru Secara Konsisten (Mulai dari Senin):

### Senin
Fokus :
...

Latihan :
...

### Selasa
Fokus :
...

Latihan :
...

...

### Minggu
Fokus :
...

Latihan :
...

### Kesimpulan
Berikan evaluasi singkat terhadap program latihan minggu ini.
"""

    return ask_ai(prompt)
# =====================================================
# RULE BASED BACKUP
# =====================================================

def generate_coach_response(
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
