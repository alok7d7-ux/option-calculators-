import streamlit as st

# Streamlit App Title & Setup
st.set_page_config(page_title="Spread Loss Calculator", layout="centered")
st.title("📊 Credit Spread Risk & Stop-Loss Calculator")

# Input Fields
st.subheader("1. Enter Spread Position")
spread_type = st.selectbox("Spread Type", ["Bull Put Spread", "Bear Call Spread"])
net_credit = st.number_input("Net Credit Received per Option ($/pts)", min_value=0.1, value=2.0, step=0.1)
strike_width = st.number_input("Strike Width ($/pts)", min_value=0.5, value=5.0, step=0.5)
lot_size = st.number_input("Total Contract Quantity / Lots", min_value=1, value=1, step=1)
multiplier = st.number_input("Contract Multiplier (e.g., 50 for Nifty, 100 for Stocks)", min_value=1, value=50, step=1)

st.subheader("2. Stop-Loss Trigger")
entry_spot = st.number_input("Entry Index Spot Level", min_value=1.0, value=24500.0, step=10.0)

if spread_type == "Bull Put Spread":
    sl_spot = st.number_input("Stop-Loss Index Spot Level (Lower)", min_value=0.0, value=entry_spot - 50.0, step=10.0)
    pts_move = entry_spot - sl_spot
else:
    sl_spot = st.number_input("Stop-Loss Index Spot Level (Higher)", min_value=0.0, value=entry_spot + 50.0, step=10.0)
    pts_move = sl_spot - entry_spot

est_spread_cost = st.slider("Estimated Spread Cost at SL Exit ($/pts)", min_value=float(net_credit), max_value=float(strike_width), value=min(net_credit * 2.0, strike_width), step=0.1)

# Profit & Loss Calculations
total_units = lot_size * multiplier
max_profit = net_credit * total_units
max_loss = (strike_width - net_credit) * total_units
est_sl_loss = (est_spread_cost - net_credit) * total_units

# Metrics Display
st.markdown("---")
col1, col2 = st.columns(2)
col1.metric("Max Profit (Total Credit)", f"${max_profit:,.2f}")
col2.metric("Max Capital Risk (Margin)", f"${max_loss:,.2f}")

col3, col4 = st.columns(2)
col3.metric("Index Points Move to SL", f"{pts_move:.1f} pts")
col4.metric("Est. Loss at Stop-Loss Exit", f"${est_sl_loss:,.2f}", delta=f"-{(est_sl_loss/max_profit)*100:.1f}% of Profit Buffer", delta_color="inverse")
