import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Calculadora 101% Sure BET", page_icon="🎯", layout="centered")

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

def login():
    st.title("🔐 Login para acessar a Calculadora")
    username = st.text_input("Usuário")
    password = st.text_input("Senha", type="password")
    login_btn = st.button("Entrar")
    if login_btn:
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"Bem-vindo, {username}! 🎉")
        else:
            st.error("Usuário ou senha incorretos")

def animar_afzf():
    pisca_css = """
    <style>
    @keyframes piscar {
        0% {opacity: 1; color: #f39c12;}
        50% {opacity: 0.5; color: #e74c3c;}
        100% {opacity: 1; color: #f39c12;}
    }
    .pisca-afzf {
        animation: piscar 2s infinite;
        font-weight: bold;
        text-align: center;
        font-size: 1.8em;
    }
    </style>
    <div class="pisca-afzf">by AFZF 🧠🍕</div>
    """
    st.markdown(pisca_css, unsafe_allow_html=True)

def tabela_exemplos():
    st.markdown("### 📋 Exemplos comuns de Odds que dão Arbitragem (lucro garantido)")
    # Odds comuns usadas em apostas (exemplo)
    odd1_comuns = [1.20, 1.30, 1.40, 1.50, 1.60, 1.80, 2.00, 2.20]
    exemplos = []
    for o1 in odd1_comuns:
        # Calcula a odd mínima para o parar arbitragem
        o2_min = round(1 / (1 - 1/o1), 2)
        exemplos.append({"Odd 1": o1, "Odd 2 mínima para arbitragem": o2_min})

    df = pd.DataFrame(exemplos)

    # Estilo simples e bonito para a tabela
    styled_df = df.style.set_properties(**{
        'background-color': '#f9f9f9',
        'color': '#333',
        'border': '1px solid #ddd',
        'text-align': 'center',
        'font-weight': 'bold',
        'font-size': '14px'
    }).set_table_styles([{
        'selector': 'th',
        'props': [('background-color', '#f39c12'), ('color', 'white'), ('font-size', '16px')]
    }]).hide_index()

    st.table(styled_df)

def calculadora():
    st.markdown(
        '''
        <h1 style='text-align: center; color: #4CAF50;'>🎯 Calculadora <span style="color:#f39c12">101% Sure BET</span></h1>
        <p style='text-align: center; color: #888;'>Calcula apostas seguras e vê se consegues lucrar em qualquer resultado 💸</p>
        <hr>
        ''', unsafe_allow_html=True
    )

    if st.button("🔒 Logout"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.experimental_rerun()

    col1, col2 = st.columns(2)
    with col1:
        odd1 = st.number_input("🔢 Odd 1", min_value=1.01, step=0.01, value=2.10)
    with col2:
        odd2 = st.number_input("🔢 Odd 2", min_value=1.01, step=0.01, value=1.05)

    amount = st.number_input("💰 Montante Total a Apostar (€)", min_value=1.0, step=1.0, value=100.0)

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
        st.info(f"🔹 **Aposta 1:** €{stake1:.2f} | Odd: {odd1}")
        st.info(f"🔹 **Aposta 2:** €{stake2:.2f} | Odd: {odd2}")
        st.markdown(f"<h3 style='color:#27ae60'>💸 Lucro garantido: €{lucro_minimo} ({lucro_percent}%)</h3>", unsafe_allow_html=True)

        df = pd.DataFrame({
            'Apostas': list(range(1, 11)),
            'Banca (€)': np.cumsum([lucro_minimo] * 10) + amount
        })
        st.line_chart(df.set_index('Apostas'))

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
            st.success("✅ Aposta guardada no histórico.")

        if st.session_state.historico:
            st.markdown("### 🕒 Histórico de Apostas")
            st.table(pd.DataFrame(st.session_state.historico))

        tabela_exemplos()

        # Surpresa extra: balões se lucro alto
        if arbitrage_percent < 0.9:
            st.balloons()
            st.success("🎉 Wow! Lucro mega alto detectado! Parabéns, campeão!")

    else:
        st.error("❌ Não há arbitragem possível com estas odds. Tenta outras!")
        tabela_exemplos()

    st.markdown("<hr>", unsafe_allow_html=True)
    animar_afzf()
    st.markdown(
        "<p style='text-align:center; color:gray;'>Dev with <strong>O P E N A I</strong> & <strong>S T R E A M L I T</strong> — configured and coded by <strong>AFZF</strong><br>Calculadora 101% Sure BET for <strong>ÁLAMOS partners xD! </strong> 🧠🍕</p>",
        unsafe_allow_html=True
    )

def surpresa_mega_secreta():
    # Botão surpresa que aparece no rodapé para o usuário descobrir
    if st.button("🎁 Surpresa? Clique aqui!"):
        st.balloons()
        st.success("Você encontrou o easter egg! 🥳 Que a sorte te acompanhe nas apostas!")

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
    st.session_state["user"] = None

if not st.session_state["logged_in"]:
    login()
else:
    calculadora()
    surpresa_mega_secreta()
