import streamlit as st
import pandas as pd
from groq import Groq
import io

# ==============================
#   INIT GROQ CLIENT
# ==============================
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# ==============================
#   CONFIG STREAMLIT
# ==============================
st.set_page_config(
    page_title="AI Audit + Auto Analisis Transaksi",
    layout="wide"
)

st.title("🧾 AI Audit + Auto Analisis Transaksi")
st.write("Upload file transaksi & dapatkan analisis audit otomatis dengan AI.")


# ==============================
#   FUNCTION: Analisis dengan AI
# ==============================
def audit_with_ai(text):
    prompt = f"""
    Kamu adalah auditor profesional. 
    Lakukan analisis audit menyeluruh terhadap data transaksi berikut:

    {text}

    Buat output dengan struktur berikut:
    1. Temuan utama
    2. Transaksi tidak wajar / anomali
    3. Potensi fraud
    4. Kesalahan pencatatan akuntansi
    5. Kesimpulan audit
    """

    chat = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.3
    )

    return chat.choices[0].message["content"]


# ==============================
#   UPLOAD FILE
# ==============================
uploaded = st.file_uploader("Upload file transaksi (CSV / Excel)", type=["csv", "xlsx"])

if uploaded:
    st.subheader("📊 Data Transaksi")
    # baca file
    if uploaded.name.endswith(".csv"):
        df = pd.read_csv(uploaded)
    else:
        df = pd.read_excel(uploaded)

    st.dataframe(df, use_container_width=True)

    # convert df to text
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False)
    csv_text = csv_buffer.getvalue()

    st.subheader("🤖 Analisis Transaksi dengan AI")
    if st.button("Mulai Analisis Audit"):
        with st.spinner("Sedang menganalisis data..."):
            result = audit_with_ai(csv_text)
        st.success("Analisis selesai!")
        st.write(result)


# ==============================
#   CHATBOT AUDIT
# ==============================
st.subheader("💬 AI Audit Bot")

if "chat_history" not in st.session_state:
    st.session_state["chat_history"] = []

user_input = st.text_input("Tanya apa saja tentang audit:")

if st.button("Kirim"):
    if user_input.strip():
        st.session_state["chat_history"].append(("user", user_input))

        ai_response = client.chat.completions.create(
            model="llama-3.1-70b-versatile",
            messages=[
                {"role": m, "content": c}
                for m, c in st.session_state["chat_history"]
            ],
            temperature=0.3
        )

        reply = ai_response.choices[0].message["content"]
        st.session_state["chat_history"].append(("assistant", reply))

for role, msg in st.session_state["chat_history"]:
    if role == "user":
        st.markdown(f"*🧑 Anda:* {msg}")
    else:
        st.markdown(f"*🤖 Audit Bot:* {msg}")
