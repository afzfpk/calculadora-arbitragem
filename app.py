import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="⚽ SUREBET - 101% by AFZF",
    page_icon="🍕",
    layout="centered"
)

# CSS geral (tema pizzaria + futebol)
st.markdown("""
<style>
  body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    max-width: 700px; margin: auto; padding: 10px;
    background: #fff8e1; /* creme pizzaria */
    color: #333;
  }
  h1.title-anim {
    font-weight: 900; font-size: 2.5rem; text-align: center;
    color: #d84315; /* vermelho tomate */
    margin-bottom: 20px;
  }
  .percent-anim {
    color: #f39c12;
    animation: pulse 2.5s infinite;
    display: inline-block;
    user-select: none;
  }
  @keyframes pulse {
    0%,100% { transform: scale(1);   color: #f39c12; }
    50%     { transform: scale(1.2); color: #e67e22; }
  }
  .compact-table th, .compact-table td {
    padding: 4px 8px!important; font-size: .85rem; text-align: center;
  }
  .footer-note {
    font-size: 1rem; font-weight: 700; color: #e2b200; /* verde relva */
    text-align: center; margin: 20px 0 10px;
    text-shadow: 1px 1px 2px #a5d6a7; user-select: none;
  }
  .footer {
    opacity: .8; font-size: 12px; color: gray;
    text-align: center; margin-top: 10px; user-select: none;
  }
  .footer .afzf {
    font-weight: 900; color: #00e8ff;
    animation: pulse 3s infinite;
  }
  .stButton > button {
    width: 100%; margin-top: 10px;
  }
</style>
""", unsafe_allow_html=True)

# Utilizadores válidos
VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

def login():
    st.title("🔐 Só pr'a malta! Mas.. Faz LOG-in primeiro...!")
    nome = st.text_input("Como te chamas mesmo?", placeholder="O teu nome???")
    pwd  = st.text_input("Qual é a password mesmo?", type="password", placeholder="A tua password???")
    if st.button("CLICAR PRA ENTRAR"):
        if nome in VALID_USERS and VALID_USERS[nome] == pwd:
            st.session_state.logged_in = True
            st.session_state.user = nome
            st.success(f"✨ BOAS {nome}, ESTÁS COM LOG-in FEITO!")
        else:
            st.error("⚠️Tens a certeza que sabes o teu nome e a tua password?? Tenta outra vez é melhor senão, liga-me para o WHATSAPP!")

def tabela_exemplos():
    odds = [1.20,1.30,1.40,1.50,1.60,1.80,2.00,2.20]
    exemplos = [
        {"Odd/Jogo 1;": o, "Odd/Jogo 2;": round(1/(1-1/o),2)}
        for o in odds
    ]
    df = pd.DataFrame(exemplos)
    st.dataframe(
        df.style
          .set_table_attributes('class="compact-table"')
          .format({"Odd/Jogo 1;":"{:.2f}","Odd/Jogo 2;":"{:.2f}"})
    , height=260, width=400)

def exportar_csv():
    df = pd.DataFrame(st.session_state.historico)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Descarregar histórico", csv, "historico.csv", "text/csv")

def calculadora():
    # Cabeçalho
    st.markdown(
        "<h1 class='title-anim'>⚽ CALCULATOR SureBet<span class='percent-anim'>🍕 101% 🍕</span> devloped by AFZF </h1>",
        unsafe_allow_html=True
    )

    # Logout
    if st.button("🔒 Sair"):
        st.session_state.clear()
        return

    # Inputs lado a lado
    col1, col2 = st.columns(2)
    with col1:
        odd1 = st.number_input(
            "🔢 Odd/Jogo 1",
            min_value=1.01, max_value=100.0, value=2.10, step=0.01,
            format="%.2f", help="Odd do primeiro mercado/jogo"
        )
    with col2:
        odd2 = st.number_input(
            "🔢 Odd/Jogo 2",
            min_value=1.01, max_value=100.0, value=1.05, step=0.01,
            format="%.2f", help="Odd do segundo mercado/jogo"
        )

    amount = st.number_input(
        "💰 Quanto vais pôr (€)?",
        min_value=1.0, max_value=1e6, value=100.0, step=1.0,
        format="%.2f", help="Total para repartir nas duas apostas"
    )

    inv1, inv2 = 1/odd1, 1/odd2
    soma = inv1 + inv2
    st.markdown("---")

    # Métrica de margem
    margem = round((1 - soma) * 100, 2)
    st.metric("Margem de Arbitragem (%)", f"{margem}%")

    if soma < 1:
        stake1 = amount * inv1 / soma
        stake2 = amount * inv2 / soma
        l1 = stake1 * odd1 - amount
        l2 = stake2 * odd2 - amount
        lucro = round(min(l1, l2), 2)
        pct = round(lucro / amount * 100, 2)
        st.success(f"✅ Dá para arbitragem! Lucro garantido: €{lucro} ({pct}%)")

        st.markdown("### 📊 Resultados")
        st.info(f"Aposta/Jogo 1: €{stake1:.2f} | Odd {odd1:.2f}")
        st.info(f"Aposta/Jogo 2: €{stake2:.2f} | Odd {odd2:.2f}")

        # Gráfico de banca acumulada
        df_g = pd.DataFrame({
            "Rodada": range(1, 11),
            "Banca (€)": np.cumsum([lucro] * 10) + amount
        }).set_index("Rodada")
        st.line_chart(df_g)

        # Histórico
        if "historico" not in st.session_state:
            st.session_state.historico = []
        if st.button("💾 Guarda aposta"):
            st.session_state.historico.append({
                "Data": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Odd/Jogo 1": odd1,
                "Odd/Jogo 2": odd2,
                "Montante (€)": amount,
                "Lucro (€)": lucro
            })
            st.success("Guardado no histórico! 🎉")
        if st.session_state.historico:
            st.markdown("### 🕒 Histórico de Apostas")
            dfh = pd.DataFrame(st.session_state.historico)
            st.dataframe(dfh, height=220)
            exportar_csv()
    else:
        st.error("⚠️ Sem arbitragem possível com essas odds. Tenta outras.")

    # Tabela de exemplos
    tabela_exemplos()

    # Mensagem final e rodapé
    st.markdown(
        "<div class='footer-note'>"
        "Calculadora 101% Sure BET — config and dev by AFZF para a malta! 🧠🍕"
        "</div>",
        unsafe_allow_html=True
    )
    st.markdown(
        "<div class='footer'>"
        "Dev with O P E N A I &amp; S T R E A M L I T — by <span class='afzf'>AFZF</span>"
        "</div>",
        unsafe_allow_html=True
    )

def main():
    if not st.session_state.get("logged_in", False):
        login()
    else:
        calculadora()

if __name__ == "__main__":
    main()
