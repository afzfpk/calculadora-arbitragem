import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="Calculadora 101% . by AFZF",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

CSS = """
<style>
body {
    max-width: 700px;
    margin: 0 auto;
    padding: 0 20px 10px 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: background-color 0.5s ease, color 0.5s ease;
}
h1 {
    font-weight: 900;
    color: #4CAF50;
    margin-bottom: 5px;
    text-align: center;
}
h1 span {
    color: #f39c12;
}
p.subtitle {
    text-align: center;
    font-size: 16px;
    color: #666;
    margin-top: 0;
    margin-bottom: 10px;
}
.dataframe-container {
    max-height: 220px;
    overflow-y: auto;
    border: 1px solid #ddd;
    border-radius: 5px;
    padding: 5px;
    margin-bottom: 5px;
}
.text-below-table {
    text-align: center;
    font-style: italic;
    color: #777;
    margin: 0 0 20px 0;
    font-size: 14px;
}
.footer {
    font-size: 14px;
    color: gray;
    text-align: center;
    margin-top: 20px;
    margin-bottom: 10px;
}
.afzf-animated {
    font-weight: 900;
    color: #f39c12;
    animation: pulse 2s infinite;
    display: inline-block;
}
@keyframes pulse {
    0% { transform: scale(1); color: #f39c12; }
    50% { transform: scale(1.2); color: #e67e22; }
    100% { transform: scale(1); color: #f39c12; }
}
.stButton>button {
    width: 100%;
    margin-top: 10px;
}
</style>
"""

def apply_dark_mode(dark_mode):
    if dark_mode:
        st.markdown(
            """
            <style>
            body {
                background-color: #121212;
                color: #eee;
            }
            .stButton>button {
                background-color: #333 !important;
                color: #eee !important;
            }
            .stTextInput>div>input, .stNumberInput>div>input {
                background-color: #333 !important;
                color: #eee !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            body {
                background-color: #fff;
                color: #000;
            }
            .stButton>button {
                background-color: #4CAF50 !important;
                color: white !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

def login():
    st.title("🔐 Login para acessar a Calculadora")
    username = st.text_input("Usuário", placeholder="Digite seu usuário")
    password = st.text_input("Senha", type="password", placeholder="Digite sua senha")
    login_btn = st.button("Entrar")
    if login_btn:
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"Bem-vindo, {username}! 🎉")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")

def calculadora():
    st.markdown(CSS, unsafe_allow_html=True)

    dark_mode = st.sidebar.checkbox("Modo Escuro 🌙", value=False)
    apply_dark_mode(dark_mode)

    st.markdown("<h1>🎯 Calculadora <span>101%</span></h1>", unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Calcula apostas seguras e vê se consegues lucrar em qualquer resultado 💸</p>', unsafe_allow_html=True)

    if st.button("🔒 Logout", key="logout_btn"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.experimental_rerun()

    odd1 = st.number_input("🔢 Odd 1", min_value=1.01, step=0.01, value=2.10, format="%.2f")
    odd2 = st.number_input("🔢 Odd 2", min_value=1.01, step=0.01, value=1.05, format="%.2f")
    amount = st.number_input("💰 Montante Total a Apostar (€)", min_value=1.0, step=1.0, value=100.0, format="%.2f")

    inv1 = 1 / odd1
    inv2 = 1 / odd2
    arbitrage_percent = inv1 + inv2

    st.markdown("---")

    if arbitrage_percent < 1:
        st.success("✅ Arbitragem possível! Lucro garantido 🔒")

        stake1 = amount * inv1 / arbitrage_percent
        stake2 = amount * inv2 / arbitrage_percent

        lucro1 = stake1 * odd1 - amount
        lucro2 = stake2 * odd2 - amount
        lucro_minimo = round(min(lucro1, lucro2), 2)
        lucro_percent = round((lucro_minimo / amount) * 100, 2)

        st.markdown("### 📊 Resultados")
        st.info(f"🔹 **Aposta 1:** €{stake1:.2f} | Odd: {odd1:.2f}")
        st.info(f"🔹 **Aposta 2:** €{stake2:.2f} | Odd: {odd2:.2f}")
        st.markdown(f"<h3 style='color:#27ae60'>💸 Lucro garantido: €{lucro_minimo} ({lucro_percent}%)</h3>", unsafe_allow_html=True)

        if 'historico' not in st.session_state:
            st.session_state.historico = []

        if st.button("💾 Guardar esta aposta"):
            st.session_state.historico.append({
                'data': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'odd1': odd1,
                'odd2': odd2,
                'montante': amount,
                'lucro': lucro_minimo
            })
            st.success("✅ Aposta guardada no histórico. 🎉")

        if st.session_state.historico:
            st.markdown('<div class="dataframe-container">', unsafe_allow_html=True)
            df_hist = pd.DataFrame(st.session_state.historico)
            df_hist = df_hist.rename(columns={
                'data': 'Data',
                'odd1': 'Odd 1',
                'odd2': 'Odd 2',
                'montante': 'Montante (€)',
                'lucro': 'Lucro (€)'
            })
            st.dataframe(df_hist.style.format({
                'Odd 1': '{:.2f}',
                'Odd 2': '{:.2f}',
                'Montante (€)': '€ {:.2f}',
                'Lucro (€)': '€ {:.2f}'
            }), height=220)
            st.markdown('</div>', unsafe_allow_html=True)

            # Export CSV
            csv = df_hist.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="📥 Exportar histórico para CSV",
                data=csv,
                file_name='historico_surebet.csv',
                mime='text/csv'
            )

        # Texto coladinho abaixo da tabela
        st.markdown('<p class="text-below-table">Calculadora 101% Sure BET for ÁLAMOS partners xD! 🧠🍕</p>', unsafe_allow_html=True)

    else:
        st.error("❌ Não há arbitragem possível com estas odds. Tenta outras!")

    # Rodapé animado fixo e simples
    st.markdown("""
    <div class="footer">
        Dev with <strong>O P E N A I</strong> &amp; <strong>S T R E A M L I T</strong> — configured and coded by <span class="afzf-animated">AFZF</span>
    </div>
    """, unsafe_allow_html=True)

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None

    if not st.session_state["logged_in"]:
        login()
    else:
        calculadora()

if __name__ == "__main__":
    main()
