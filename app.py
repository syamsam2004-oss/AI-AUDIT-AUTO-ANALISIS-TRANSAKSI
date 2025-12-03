import streamlit as st
import pandas as pd
from groq import Groq

# ===========================
# KONFIGURASI API
# ===========================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ===========================
# FUNGSI ANALISIS AI
# ===========================
def analisis_transaksi(df):
    # Convert data ke teks untuk dikirim ke AI
    data_text = df.to_csv(index=False)

    prompt = f"""
Kamu adalah AI Auditor profesional. Analisis data transaksi berikut:

{data_text}

Berikan output dengan struktur:
1. Temuan utama
2. Transaksi mencurigakan
3. Pola anomali
4. Rekomendasi audit

Jawaban harus rapi dan mudah dibaca.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Kamu adalah auditor berpengalaman."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=500
    )

    return response.choices[0].message.content


# ===========================
# UI STREAMLIT
# ===========================
st.title("📊 AI Audit + Auto Analisis Transaksi")
st.write("Unggah file Excel untuk dianalisis AI Auditor.")

uploaded_file = st.file_uploader("Upload file Excel (.xlsx)", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📄 Data Transaksi")
    st.dataframe(df)

    if st.button("🔍 Jalankan Analisis AI"):
        with st.spinner("Sedang menganalisis data..."):
            try:
                hasil = analisis_transaksi(df)
                st.subheader("🧠 Hasil Analisis AI")
                st.write(hasil)
            except Exception as e:
                st.error(f"Error: {e}")
                st.info("Periksa API Key atau format file Excel kamu.")
