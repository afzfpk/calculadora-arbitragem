import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(
    page_title="🎯 Calculadora 101% Sure BET",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

# CSS para dark mode e animações suaves
css = """
<style>
    body {
        transition: background-color 0.5s ease, color 0.5s ease;
    }
    .footer {
        opacity: 0;
        animation: fadeIn 3s forwards;
        font-size: 14px;
        color: gray;
        text-align: center;
        margin-top: 30px;
    }
    @keyframes fadeIn {
        to { opacity: 1; }
    }
    .stButton>button {
        transition: background-color 0.3s ease;
    }
</style>
"""

def apply_dark_mode(dark_mode):
    if dark_mode:
        st.markdown(
            """
            <style>
            .main {
                background-color: #121212;
                color: #eee;
            }
            .stButton>button {
                background-color: #333;
                color: #eee;
            }
            .stTextInput>div>input, .stNumberInput>div>input {
                background-color: #333;
                color: #eee;
            }
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.markdown(
            """
            <style>
            .main {
                background-color: #fff;
                color: #000;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
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

def tabela_exemplos():
    st.markdown("### 📋 Exemplos comuns de Odds que dão Arbitragem (lucro garantido)")
    odd1_comuns = [1.20, 1.30, 1.40, 1.50, 1.60, 1.80, 2.00, 2.20]
    exemplos = []
    for o1 in odd1_comuns:
        o2_min = round(1 / (1 - 1/o1), 2)
        exemplos.append({"Odd 1": o1, "Odd 2 mínima para arbitragem": o2_min})

    df = pd.DataFrame(exemplos)
    st.dataframe(df.style.format({"Odd 1": "{:.2f}", "Odd 2 mínima para arbitragem": "{:.2f}"}), height=280)

def exportar_historico_csv():
    if 'historico' in st.session_state and st.session_state.historico:
        df_hist = pd.DataFrame(st.session_state.historico)
        csv = df_hist.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Exportar histórico para CSV",
            data=csv,
            file_name='historico_surebet.csv',
            mime='text/csv'
        )

def calculadora():
    dark_mode = st.sidebar.checkbox("Modo Escuro 🌙", value=False)
    apply_dark_mode(dark_mode)
    st.markdown(css, unsafe_allow_html=True)

    st.markdown(
        '''
        <h1 style='text-align: center; color: #4CAF50; font-weight: 800;'>🎯 Calculadora <span style="color:#f39c12">101% Sure BET</span></h1>
        <p style='text-align: center; color: #666; font-size:16px; margin-bottom:25px;'>Calcula apostas seguras e vê se consegues lucrar em qualquer resultado 💸</p>
        <hr>
        ''', unsafe_allow_html=True
    )

    if st.button("🔒 Logout", key="logout_btn"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.experimental_rerun()

    col1, col2 = st.columns([1,1])
    with col1:
        odd1 = st.number_input("🔢 Odd 1", min_value=1.01, step=0.01, value=2.10, format="%.2f")
    with col2:
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

        df = pd.DataFrame({
            'Rodadas': list(range(1, 11)),
            'Banca (€)': np.cumsum([lucro_minimo] * 10) + amount
        })
        st.line_chart(df.set_index('Rodadas'), use_container_width=True)

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
            st.markdown("### 🕒 Histórico de Apostas")
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
            }), height=280)
            exportar_historico_csv()

        if arbitrage_percent < 0.9:
            st.balloons()
            st.success("🎉 Wow! Lucro mega alto detectado! Parabéns, campeão! 🥳")

    else:
        st.error("❌ Não há arbitragem possível com estas odds. Tenta outras!")

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(
        """
        <div class="footer">
        Dev with <strong>O P E N A I</strong> &amp; <strong>S T R E A M L I T</strong> — configured and coded by <strong>AFZF</strong><br>
        Calculadora 101% Sure BET for <strong>ÁLAMOS partners xD!</strong> 🧠🍕
        </div>
        """,
        unsafe_allow_html=True
    )

def main():
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
        st.session_state["user"] = None

    if not st.session_state["logged_in"]:
        login()
    else:
        calculadora()
        tabela_exemplos()

if __name__ == "__main__":
    main()
