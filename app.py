import streamlit as st
import pandas as pd
from groq import Groq

# ==========================
# 1. SETTING GROQ API
# ==========================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==========================
# 2. FUNGSI ANALISIS DENGAN AI
# ==========================
def audit_with_ai(text):
    prompt = f"""
    Kamu adalah auditor profesional.

    Analisis transaksi berikut secara rinci lalu berikan:
    1. Temuan utama
    2. Analisis risiko
    3. Indikasi transaksi mencurigakan
    4. Rekomendasi audit
    5. Kesimpulan ringkas

    Data Transaksi:
    {text}
    """

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Kamu adalah auditor keuangan profesional."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message["content"]


# ==========================
# 3. UI STREAMLIT
# ==========================
st.title("🔍 AI Audit Bot + Auto Analisis Transaksi")
st.write("Upload file Excel transaksi dan sistem akan melakukan analisis audit otomatis.")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📄 Data Transaksi")
        st.dataframe(df)

        # Convert ke text untuk AI
        csv_text = df.to_csv(index=False)

        st.subheader("🤖 Hasil Analisis AI")

        with st.spinner("Sedang menganalisis transaksi…"):
            result = audit_with_ai(csv_text)

        st.success("Analisis selesai!")
        st.write(result)

    except Exception as e:
        st.error("Terjadi kesalahan saat membaca file.")
        st.text(str(e))
