import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Calculadora SUREBET101% by AFZF",
    page_icon="🎯🍕",
    layout="centered",
    initial_sidebar_state="expanded"
)

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

# CSS geral
css = """
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    transition: background-color 0.5s, color 0.5s;
    max-width: 700px;
    margin: auto;
    padding: 10px;
  }
  h1.title-anim {
    font-weight: 900;
    font-size: 3rem;
    text-align: center;
    color: #4CAF50;
    animation: pulseGlow 2.5s infinite;
    margin-bottom: 30px;
    user-select: none;
  }
  h1.title-anim span { color: #f39c12; }
  @keyframes pulseGlow {
    0%,100% { text-shadow: 0 0 10px #4CAF50, 0 0 20px #4CAF50; }
    50%   { text-shadow: 0 0 20px #f39c12, 0 0 30px #f39c12; }
  }
  .compact-table th, .compact-table td {
    padding: 4px 8px !important; font-size: 0.85rem; text-align: center;
  }
  .above-footer {
    font-size: 1.0rem;
    font-weight: 700;
    color: #99ffff;
    text-align: center;
    margin: 20px 0 10px 0;
    text-shadow: 1px 1px 3px #e6ffff;
    user-select: none;
  }
  .footer {
    opacity: 0.6;
    font-size: 13px;
    color: gray;
    text-align: center;
    margin-top: 20px;
    user-select: none;
  }
  .footer .afzf {
    font-weight: 900;
    color: #f39c12;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%   { transform: scale(1);   color: #f39c12; }
    50%  { transform: scale(1.2); color: #e67e22; }
    100% { transform: scale(1);   color: #f39c12; }
  }
  .stButton>button {
    width: 100%; margin-top: 10px;
  }
</style>
"""

def login():
    st.title("🔐 Apenas convidados! Faça o login")
    user = st.text_input("Usuário")
    pwd  = st.text_input("Senha", type="password")
    if st.button("Entrar"):
        if user in VALID_USERS and VALID_USERS[user] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success(f"✅ Bem-vindo, {user}!")
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")

def tabela_exemplos():
    odd1 = [1.20,1.30,1.40,1.50,1.60,1.80,2.00,2.20]
    exemplos = [{"Odd 1": o, "Odd 2 mínima": round(1/(1-1/o),2)} for o in odd1]
    df = pd.DataFrame(exemplos)
    st.dataframe(
        df.style
          .set_table_attributes('class="compact-table"')
          .format({"Odd 1":"{:.2f}","Odd 2 mínima":"{:.2f}"})
    , height=260, width=400)

def exportar_csv():
    df = pd.DataFrame(st.session_state.historico)
    csv = df.to_csv(index=False).encode()
    st.download_button("📥 Exportar histórico", csv, "historico.csv", "text/csv")

def calculadora():
    st.markdown(css, unsafe_allow_html=True)

    st.markdown("<h1 class='title-anim'>🎯 Calculadora <span>101%</span></h1>", unsafe_allow_html=True)

    if st.button("🔒 Logout"):
        st.session_state.clear()
        st.experimental_rerun()

    col1,col2 = st.columns(2)
    with col1: odd1 = st.number_input("Odd 1", 1.01, 100.0, 2.10, 0.01, "%.2f")
    with col2: odd2 = st.number_input("Odd 2", 1.01, 100.0, 1.05, 0.01, "%.2f")
    amount = st.number_input("Total a apostar (€)", 1.0, 1e6, 100.0, 1.0, "%.2f")

    inv1 = 1/odd1; inv2 = 1/odd2; arb = inv1+inv2
    st.markdown("---")

    if arb < 1:
        stake1 = amount*inv1/arb; stake2 = amount*inv2/arb
        lucro1 = stake1*odd1-amount; lucro2 = stake2*odd2-amount
        lucro = round(min(lucro1,lucro2),2)
        pct   = round(lucro/amount*100,2)
        st.success(f"✅ Arbitragem possível! Lucro: €{lucro} ({pct}%)")

        st.markdown("### Resultados")
        st.info(f"Aposta 1: €{stake1:.2f} | Odd {odd1:.2f}")
        st.info(f"Aposta 2: €{stake2:.2f} | Odd {odd2:.2f}")

        # gráfico
        dfg = pd.DataFrame({
            "Rodada":range(1,11),
            "Banca":np.cumsum([lucro]*10)+amount
        }).set_index("Rodada")
        st.line_chart(dfg)

        # histórico
        if "historico" not in st.session_state:
            st.session_state.historico=[]
        if st.button("💾 Guardar"):
            st.session_state.historico.append({
                "Data":datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Odd1":odd1,"Odd2":odd2,
                "Montante":amount,"Lucro":lucro
            })
            st.success("Guardado!")
        if st.session_state.historico:
            st.markdown("### Histórico")
            dfh=pd.DataFrame(st.session_state.historico)
            st.dataframe(dfh, height=220)
            exportar_csv()
    else:
        st.error("⚠️ Sem arbitragem possível.")

    tabela_exemplos()

    st.markdown("""
    <div class='above-footer'>
      Calculadora 101% Sure BET from AFZF to ÁLAMOS partners xD! 🧠🍕
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class='footer'>
      Dev with O P E N A I &amp; S T R E A M L I T — by <span class='afzf'>AFZF</span>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    if not st.session_state.get("logged_in", False):
        login()
    else:
        calculadora()
