import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configurações da página com ícone simples (não duplicado)
st.set_page_config(
    page_title="Calculadora🎯SUREBET101% - by.AFZF🍕",
    page_icon="🎯🍕",
    layout="centered",
    initial_sidebar_state="expanded"
)

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

# CSS para animação título e estilos gerais
css = """
<style>
    body {
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        transition: background-color 0.5s ease, color 0.5s ease;
    }
    /* Animação título principal */
    .title-anim {
        font-weight: 800;
        font-size: 3rem;
        text-align: center;
        color: #4CAF50;
        margin-bottom: 30px;
        animation: pulseGlow 2.0s ease-in-out infinite;
        user-select: none;
    }
    .title-anim span {
        color: #f39c12;
    }
    @keyframes pulseGlow {
        0%, 100% {
            text-shadow: 0 0 9px #4CAF50, 0 0 15px #4CAF50;
        }
        50% {
            text-shadow: 0 0 19px #f39c12, 0 0 25px #f39c12;
        }
    }
    /* Rodapé discreto */
    .footer {
        opacity: 0.8;
        font-size: 13px;
        color: gray;
        text-align: center;
        font-style: italic;
        user-select: none;
        margin-bottom: 20px;
    }
    /* Tabela compacta estilizada */
    .compact-table th, .compact-table td {
        padding: 4px 8px !important;
        font-size: 0.85rem;
        text-align: center;
    }
    /* Botões e inputs */
    .stButton>button {
        transition: background-color 0.3s ease;
    }
</style>
"""

def login():
    st.title("🔐 Só convidados ahahah! Login para acessar à Calculadora101%?")
    username = st.text_input("Usuário", placeholder="O TEU NOME?")
    password = st.text_input("Senha", type="password", placeholder="A TUA PASSWORD?")
    login_btn = st.button("Entrar")
    if login_btn:
        if username in VALID_USERS and password == VALID_USERS[username]:
            st.session_state["logged_in"] = True
            st.session_state["user"] = username
            st.success(f"✅ Bem-vindo, {username}! 🍕")
            st.experimental_rerun()
        else:
            st.error("NOME E/OU PASSWORD INCORRETO/A ")

def tabela_exemplos():
    odd1_comuns = [1.20, 1.30, 1.40, 1.50, 1.60, 1.80, 2.00, 2.20]
    exemplos = []
    for o1 in odd1_comuns:
        o2_min = round(1 / (1 - 1/o1), 2)
        exemplos.append({"Odd 1": o1, "Odd 2 mínima p/ arbitragem": o2_min})

    df = pd.DataFrame(exemplos)
    styled = df.style.set_table_attributes('class="compact-table"')\
        .format({"Odd 1": "{:.2f}", "Odd 2 mínima p/ arbitragem": "{:.2f}"})\
        .set_properties(**{'text-align': 'center'})
    st.dataframe(styled, height=260, width=400)

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
    st.markdown(css, unsafe_allow_html=True)

    # Título animado (sem subtítulo)
    st.markdown("<h1 class='title-anim'>🎯 Calculadora <span>101%</span></h1>", unsafe_allow_html=True)

    # Botão logout
    if st.button("🔒 Logout 🍕", key="logout_btn"):
        st.session_state["logged_in"] = False
        st.session_state["user"] = None
        st.experimental_rerun()

    # Inputs lado a lado
    col1, col2 = st.columns(2)
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

        # Gráfico simples lucro acumulado em 10 rodadas
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
            }), height=280, width=450)
            exportar_historico_csv()

    else:
        st.error("⚠️ SUREBET NÃO possível com essas odds. Tenta outras!!!")

    tabela_exemplos()

    # Texto divertido e destacado abaixo da tabela
    st.markdown("""
    <div style="
        font-size: 1.0rem;
        font-weight: 700;
        color: #ff6f61;
        text-align: center;
        margin-top: 15px;
        margin-bottom: 10px;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        user-select: none;
        text-shadow: 1px 2px 1px #ffb3ab;
        ">
        Calculadora 101% Sure BET for ÁLAMOS partners xD! 🧠🍕
    </div>
    """, unsafe_allow_html=True)

    # Rodapé discreto, abaixo do texto destacado
    st.markdown("""
    <div class='footer'>
        Dev with O P E N A I &amp; S T R E A M L I T — configured and coded by <strong>AFZF</strong>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if "logged_in" not in st.session_state or not st.session_state["logged_in"]:
        login()
    else:
        calculadora()
