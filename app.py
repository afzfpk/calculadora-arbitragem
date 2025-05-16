import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Calculadora SUREBET101% by AFZF",
    page_icon="🎯",
    layout="centered",
    initial_sidebar_state="expanded"
)

VALID_USERS = {
    "afzfpk": "4124",
    "familia": "familia2025"
}

# CSS global
CSS = """
<style>
  body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
  /* Banner placeholder */
  .banner { width: 100%; margin-bottom: 20px; }
  /* Cabeçalho animado */
  .title-anim {
    font-weight: 900; font-size: 2.8rem; text-align: center;
    color: #4CAF50; animation: pulseGlow 2.5s infinite;
  }
  .title-anim span { color: #f39c12; }
  @keyframes pulseGlow {
    0%,100% { text-shadow: 0 0 8px #4CAF50; }
    50% { text-shadow: 0 0 16px #f39c12; }
  }
  /* Tabela compacta */
  .compact-table th, .compact-table td {
    padding: 4px 8px !important; font-size: 0.85rem; text-align: center;
  }
  /* Texto divertido */
  .fun-text {
    font-size:1.1rem; font-weight:600; color:#ff6f61;
    text-align:center; margin:15px 0 10px; text-shadow:1px 1px 2px #e6ffff;
  }
  /* Footer “cartão” */
  .footer-card {
    background:rgba(0,0,0,0.03); padding:12px; border-radius:8px;
    text-align:center; font-size:0.9rem; color:gray; margin:20px 0;
  }
  .footer-card .afzf {
    display:inline-block; font-weight:700; color:#f39c12;
    animation: pulse 2s infinite;
  }
  @keyframes pulse {
    0%,100% { transform:scale(1); } 50% { transform:scale(1.1); }
  }
</style>
"""

def login():
    st.markdown(CSS, unsafe_allow_html=True)
    # Banner de topo (troca a URL pela tua imagem)
    st.image("https://via.placeholder.com/1024x150.png?text=SureBet101%25+by+AFZF", use_column_width=True)
    st.markdown("<h2 style='text-align:center;color:#4CAF50;'>Bem-vindo ao SureBet101%</h2>", unsafe_allow_html=True)

    user = st.text_input("🔑 Usuário")
    pwd  = st.text_input("🔒 Password", type="password")
    if st.button("Entrar"):
        if user in VALID_USERS and pwd == VALID_USERS[user]:
            st.session_state.logged_in = True
            st.experimental_rerun()
        else:
            st.error("Usuário ou senha incorretos")

def tabela_exemplos():
    odd1_comuns = [1.20,1.30,1.40,1.50,1.60,1.80,2.00,2.20]
    exemplos = [{"Odd 1":o, "Odd 2 min.":round(1/(1-1/o),2)} for o in odd1_comuns]
    df = pd.DataFrame(exemplos)
    st.dataframe(df.style.set_table_attributes('class="compact-table"')\
        .format({"Odd 1":"{:.2f}","Odd 2 min.":"{:.2f}"}), height=260, width=400)

def calculadora():
    st.markdown(CSS, unsafe_allow_html=True)
    st.markdown("<h1 class='title-anim'>🎯 Calculadora <span>101%</span></h1>", unsafe_allow_html=True)

    if st.button("🔒 Terminar Sessão"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    col1,col2 = st.columns(2)
    odd1 = col1.number_input("Odd 1",1.01,100.0,2.10,0.01,format="%.2f")
    odd2 = col2.number_input("Odd 2",1.01,100.0,1.05,0.01,format="%.2f")
    amount = st.number_input("Montante (€)",1.0,1e6,100.0,1.0,format="%.2f")

    inv1,inv2 = 1/odd1,1/odd2
    arb = inv1+inv2

    st.markdown("---")
    if arb<1:
        st.success("✅ Arbitragem possível! Lucro garantido")
        s1 = amount*inv1/arb; s2 = amount*inv2/arb
        l1,l2 = s1*odd1-amount, s2*odd2-amount
        minl = round(min(l1,l2),2); pct = round(minl/amount*100,2)

        st.markdown("#### Resultados")
        st.write(f"Aposta1: €{s1:.2f} | Odd {odd1:.2f}")
        st.write(f"Aposta2: €{s2:.2f} | Odd {odd2:.2f}")
        st.markdown(f"<h3 style='color:#27ae60;'>Lucro: €{minl} ({pct}%)</h3>",unsafe_allow_html=True)

        df = pd.DataFrame({'Rodada':range(1,11),'Banca':np.cumsum([minl]*10)+amount})
        st.line_chart(df.set_index('Rodada'))

        if 'hist' not in st.session_state: st.session_state.hist=[]
        if st.button("💾 Guardar"):
            st.session_state.hist.append({
                'hora':datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                'odd1':odd1,'odd2':odd2,'valor':amount,'lucro':minl})
            st.success("Guardado!")

        if st.session_state.hist:
            st.markdown("#### Histórico")
            hist_df=pd.DataFrame(st.session_state.hist).rename(columns={
                'hora':'Data','odd1':'Odd1','odd2':'Odd2','valor':'Montante','lucro':'Lucro'})
            st.dataframe(hist_df.style.format({
                'Odd1':'{:.2f}','Odd2':'{:.2f}','Montante':'€ {:.2f}','Lucro':'€ {:.2f}'}),height=240)
            csv=hist_df.to_csv(index=False).encode()
            st.download_button("Exportar CSV",csv,"hist.csv","text/csv")

    else:
        st.error("⚠️ Sem arbitragem com estas odds")

    # tabela de exemplos
    tabela_exemplos()

    # texto divertido abaixo da tabela
    st.markdown("""
      <div class='fun-text'>
        Calculadora 101% Sure BET for ÁLAMOS partners xD! 🧠🍕
      </div>
    """,unsafe_allow_html=True)

    # footer estilizado
    st.markdown("""
      <div class='footer-card'>
        Dev with <strong>O P E N A I</strong> &amp; <strong>S T R E A M L I T</strong><br>
        configured and coded by <span class='afzf'>AFZF</span>
      </div>
    """,unsafe_allow_html=True)

if __name__=="__main__":
    if not st.session_state.get("logged_in"):
        login()
    else:
        calculadora()
