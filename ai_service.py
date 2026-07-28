import streamlit as st
import requests

# ======================================
# OPENROUTER CONFIG
# ======================================

OPENROUTER_API_KEY = st.secrets["OPENROUTER_API_KEY"]
OPENROUTER_URL = st.secrets["OPENROUTER_URL"]

# ======================================
# SYSTEM PROMPT
# ======================================

SYSTEM_PROMPT = """
Anda adalah MMA Strength & Conditioning Coach profesional.

Tugas utama:
- Menganalisis kondisi atlet berdasarkan data fisiologis.
- Menginterpretasikan fatigue score.
- Memberikan rekomendasi latihan dan recovery.
- Memberikan saran yang aman dan realistis.

Aturan:
- Selalu gunakan Bahasa Indonesia.
- Jangan memberikan salam pembuka.
- Jangan menyebut diri sebagai AI atau chatbot.
- Gunakan gaya bahasa profesional, singkat, padat, dan jelas.
- Fokus pada sport science dan manajemen fatigue.
- Jangan memberikan diagnosis medis.
- Jika fatigue tinggi, prioritaskan recovery.
- Jika durasi tidur rendah, berikan perhatian khusus pada pemulihan.
- Jelaskan risiko secara objektif tanpa menakut-nakuti pengguna.

Format jawaban:
- Analisis kondisi
- Risiko
- Rekomendasi
"""

# ======================================
# OPENROUTER REQUEST
# ======================================

def ask_ai(prompt):

    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "MMA AI Assistant"
    }

    payload = {
        "model": "eleutherai/gpt-oss-20b",
        "messages": [
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.5,
        "max_tokens": 600
    }

    try:

        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=60
        )

        if response.status_code != 200:
            return f"⚠️ ERROR API: {response.text}"

        result = response.json()

        if (
            "choices" not in result
            or len(result["choices"]) == 0
        ):
            return "⚠️ AI tidak memberikan respons."

        return result["choices"][0]["message"]["content"]

    except requests.exceptions.Timeout:
        return "⚠️ Permintaan ke AI timeout. Silakan coba lagi."

    except requests.exceptions.ConnectionError:
        return "⚠️ Gagal terhubung ke OpenRouter."

    except Exception as e:
        return f"⚠️ AI tidak tersedia: {str(e)}"
