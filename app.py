import streamlit as st

st.set_page_config(page_title="Calculadora de Arbitragem", page_icon="🎯")
st.title("🎯 Calculadora de Arbitragem de Apostas")
st.markdown("Insere as odds e o montante total a apostar para ver se há arbitragem e qual o lucro garantido.")

# Inputs
odd1 = st.number_input("Odd 1", min_value=1.01, step=0.01, value=2.10)
odd2 = st.number_input("Odd 2", min_value=1.01, step=0.01, value=1.05)
total_stake = st.number_input("Montante total a apostar (€)", min_value=1.0, step=1.0, value=100.0)

# Cálculos
inv1 = 1 / odd1
inv2 = 1 / odd2
arb_percent = inv1 + inv2

if arb_percent < 1:
    st.success("✅ Arbitragem possível!")

    stake1 = total_stake * inv1 / arb_percent
    stake2 = total_stake * inv2 / arb_percent

    profit1 = stake1 * odd1 - total_stake
    profit2 = stake2 * odd2 - total_stake
    min_profit = round(min(profit1, profit2), 2)
    profit_percent = round((min_profit / total_stake) * 100, 2)

    st.write(f"**Aposta 1**: €{stake1:.2f}")
    st.write(f"**Aposta 2**: €{stake2:.2f}")
    st.write(f"**Lucro garantido**: €{min_profit} ({profit_percent}%)")
else:
    st.error("❌ Não há arbitragem possível com estas odds.")

