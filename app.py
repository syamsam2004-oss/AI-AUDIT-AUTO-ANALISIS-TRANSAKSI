import streamlit as st
import pandas as pd
from groq import Client   # FIX IMPORT

# ======================
# 1. GROQ API CLIENT
# ======================
client = Client(api_key=st.secrets["GROQ_API_KEY"])   # FIX CLIENT

# ======================
# 2. AI AUDIT FUNCTION
# ======================
def audit_with_ai(text):
    prompt = f"""
    Kamu adalah auditor profesional. 
    Analisis transaksi berikut dan berikan:
    - Temuan utama
    - Risiko
    - Indikasi transaksi mencurigakan
    - Rekomendasi audit
    - Kesimpulan

    Data transaksi:
    {text}
    """

    response = client.chat.completions.create(   # FIX API CALL
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Kamu adalah auditor keuangan profesional."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=1500
    )

    return response.choices[0].message["content"]

# ======================
# 3. STREAMLIT UI
# ======================
st.title("🔍 AI Audit Bot + Auto Analisis Transaksi")
st.write("Upload file Excel transaksi dan sistem akan melakukan analisis audit otomatis.")

uploaded_file = st.file_uploader("Upload File Excel", type=["xlsx"])

if uploaded_file:
    try:
        df = pd.read_excel(uploaded_file)
        st.subheader("📄 Data Transaksi")
        st.dataframe(df)

        csv_text = df.to_csv(index=False)

        st.subheader("🤖 Hasil Analisis AI")
        with st.spinner("Sedang menganalisis..."):
            result = audit_with_ai(csv_text)

        st.success("Analisis selesai!")
        st.write(result)

    except Exception as e:
        st.error("Terjadi kesalahan saat membaca file.")
        st.text(str(e))
