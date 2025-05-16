
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

st.set_page_config(page_title="Calculadora de Arbitragem", page_icon="🎯", layout="centered")

# Cabeçalho bonito
st.markdown(
    '''
    <h1 style='text-align: center; color: #4CAF50;'>🎯 Calculadora <span style="color:#f39c12">101% Sure BET</span></h1>
    <p style='text-align: center; color: #888;'>Calcula apostas seguras e vê se consegues lucrar em qualquer resultado 💸</p>
    <hr>
    ''',
    unsafe_allow_html=True
)

# Reset
if st.button("🔁 Recomeçar"):
    st.experimental_rerun()

# Entradas
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        odd1 = st.number_input("🔢 Odd 1", min_value=1.01, step=0.01, value=2.10)
    with col2:
        odd2 = st.number_input("🔢 Odd 2", min_value=1.01, step=0.01, value=1.05)

    amount = st.number_input("💰 Montante Total a Apostar (€)", min_value=1.0, step=1.0, value=100.0)

# Cálculo
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

    # Resultados
    st.markdown("### 📊 Resultados")
    st.info(f"🔹 **Aposta 1:** €{stake1:.2f} | Odd: {odd1}")
    st.info(f"🔹 **Aposta 2:** €{stake2:.2f} | Odd: {odd2}")
    st.markdown(f"<h3 style='color:#27ae60'>💸 Lucro garantido: €{lucro_minimo} ({lucro_percent}%)</h3>", unsafe_allow_html=True)

    # Simulação gráfica de lucro
    st.markdown("### 📈 Crescimento Simulado")
    df = pd.DataFrame({
        'Apostas': list(range(1, 11)),
        'Banca (€)': np.cumsum([lucro_minimo] * 10) + amount
    })
    st.line_chart(df.set_index('Apostas'))

    # Histórico (sessão atual)
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

else:
    st.error("❌ Não há arbitragem possível com estas odds. Tenta outras!")

# Rodapé personalizado
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align:center; color:gray;'>Dev with <strong>o p e n  a i</strong> & <strong>s t r e a m  l i t</strong> — config and coded by <strong>AFZF</strong><br>Calculadora 101% Sure BET for <strong>ÁLAMOS partners</strong> 🧠🍕</p>",
    unsafe_allow_html=True
)
