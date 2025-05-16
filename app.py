
import streamlit as st

st.set_page_config(page_title="Calculadora de Arbitragem", page_icon="🎯", layout="centered")

# Título
st.markdown(
    '''
    <h1 style='text-align: center; color: #4CAF50;'>🎯 Calculadora <span style="color:#f39c12">101% Sure BET</span></h1>
    <p style='text-align: center; color: #888;'>Simula apostas seguras com odds diferentes e vê o teu lucro garantido 💸</p>
    <hr style='margin-top:20px; margin-bottom:20px;'>
    ''',
    unsafe_allow_html=True
)

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

    st.markdown("### 📊 Resultados")
    st.info(f"🔹 **Aposta 1:** €{stake1:.2f} | Odd: {odd1}")
    st.info(f"🔹 **Aposta 2:** €{stake2:.2f} | Odd: {odd2}")
    st.markdown(f"<h3 style='color:#27ae60'>💸 Lucro garantido: €{lucro_minimo} ({lucro_percent}%)</h3>", unsafe_allow_html=True)
else:
    st.error("❌ Não há arbitragem possível com estas odds.")

# Rodapé
st.markdown("<hr>", unsafe_allow_html=True)
st.caption("Feito com ❤️ por afzfpk · Calculadora 101% Sure BET")
