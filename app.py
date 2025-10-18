import streamlit as st
import pandas as pd
import plotly.express as px

# --------------------------------
# PAGE CONFIG
# --------------------------------
st.set_page_config(
    page_title="Crypto Analyzer Pro (Offline)",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------
# CUSTOM THEME
# --------------------------------
st.markdown("""
    <style>
    body {
        background-color: #0E1117;
        color: #FAFAFA;
    }
    .stApp {
        background-color: #0E1117;
    }
    h1, h2, h3 {
        color: #00FFAA;
        font-weight: 600;
    }
    .stMetric {
        background-color: #1C1F26;
        border-radius: 12px;
        padding: 10px;
        margin: 5px;
    }
    .sidebar .sidebar-content {
        background-color: #11141A;
    }
    </style>
""", unsafe_allow_html=True)

# --------------------------------
# LOAD DEMO DATA (Offline)
# --------------------------------
@st.cache_data
def load_data():
    data = {
        'Date': pd.date_range(start='2024-01-01', periods=30),
        'Bitcoin': [42000 + i * 100 + (i % 5) * 50 for i in range(30)],
        'Ethereum': [2200 + i * 30 + (i % 4) * 25 for i in range(30)],
        'Dogecoin': [0.08 + i * 0.002 + (i % 3) * 0.001 for i in range(30)]
    }
    return pd.DataFrame(data)

df = load_data()

# --------------------------------
# SIDEBAR NAVIGATION
# --------------------------------
st.sidebar.title("🧭 Navigation")
page = st.sidebar.radio("Go to", ["📊 Price Visualizer", "💼 Portfolio Calculator"])

# --------------------------------
# PAGE 1: PRICE VISUALIZER
# --------------------------------
if page == "📊 Price Visualizer":
    st.title("🪙 Crypto Price Visualizer (Offline)")
    st.write("Explore offline demo crypto data in a modern dark theme.")

    # Sidebar filters
    st.sidebar.header("⚙️ Controls")
    selected_coin = st.sidebar.selectbox("Select Cryptocurrency", ['Bitcoin', 'Ethereum', 'Dogecoin'])
    show_table = st.sidebar.checkbox("Show Data Table", True)
    show_chart = st.sidebar.checkbox("Show Price Chart", True)
    show_summary = st.sidebar.checkbox("Show Summary Stats", True)

    # Display data
    st.subheader(f"📊 {selected_coin} Price Data")

    if show_table:
        st.dataframe(df[['Date', selected_coin]])

    if show_chart:
        st.subheader("📈 Trend Line")
        fig = px.line(df, x='Date', y=selected_coin, title=f'{selected_coin} Price Over Time', color_discrete_sequence=["#00FFAA"])
        fig.update_layout(
            paper_bgcolor="#0E1117",
            plot_bgcolor="#0E1117",
            font=dict(color="white"),
            title_font=dict(size=22, color="#00FFAA")
        )
        st.plotly_chart(fig, use_container_width=True)

    if show_summary:
        st.subheader("📊 Summary Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Max Price", f"${df[selected_coin].max():,.2f}")
        col2.metric("Min Price", f"${df[selected_coin].min():,.2f}")
        col3.metric("Average Price", f"${df[selected_coin].mean():,.2f}")

    st.subheader("📉 Comparison of All Coins")
    df_melt = df.melt(id_vars="Date", var_name="Coin", value_name="Price")
    fig2 = px.line(df_melt, x="Date", y="Price", color="Coin", title="Crypto Price Comparison (Offline)",
                   color_discrete_sequence=["#00FFAA", "#FF007F", "#00BFFF"])
    fig2.update_layout(
        paper_bgcolor="#0E1117",
        plot_bgcolor="#0E1117",
        font=dict(color="white"),
        title_font=dict(size=22, color="#00FFAA")
    )
    st.plotly_chart(fig2, use_container_width=True)

# --------------------------------
# PAGE 2: PORTFOLIO CALCULATOR
# --------------------------------
elif page == "💼 Portfolio Calculator":
    st.title("💼 Crypto Portfolio Profit Calculator (Offline Mode)")
    st.write("Estimate your portfolio value and profit with demo data.")

    current_prices = {
        'Bitcoin': df['Bitcoin'].iloc[-1],
        'Ethereum': df['Ethereum'].iloc[-1],
        'Dogecoin': df['Dogecoin'].iloc[-1]
    }

    st.subheader("🧾 Enter Your Holdings")
    col1, col2, col3 = st.columns(3)
    with col1:
        btc_qty = st.number_input("Bitcoin (BTC)", min_value=0.0, step=0.1)
    with col2:
        eth_qty = st.number_input("Ethereum (ETH)", min_value=0.0, step=0.1)
    with col3:
        doge_qty = st.number_input("Dogecoin (DOGE)", min_value=0.0, step=100.0)

    total_value = (
        btc_qty * current_prices['Bitcoin'] +
        eth_qty * current_prices['Ethereum'] +
        doge_qty * current_prices['Dogecoin']
    )

    st.subheader("💰 Portfolio Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Bitcoin Value", f"${btc_qty * current_prices['Bitcoin']:,.2f}")
    col2.metric("Ethereum Value", f"${eth_qty * current_prices['Ethereum']:,.2f}")
    col3.metric("Dogecoin Value", f"${doge_qty * current_prices['Dogecoin']:,.2f}")

    st.success(f"**Total Portfolio Worth:** ${total_value:,.2f}")

    # Fake profit simulation
    st.subheader("📈 Estimated Profit (Offline Example)")
    profit = total_value * 0.12
    st.info(f"📊 Estimated Profit: ${profit:,.2f}")

    # Download report
    report_text = f"""
    CRYPTO PORTFOLIO REPORT
    -----------------------
    Bitcoin: {btc_qty} BTC = ${btc_qty * current_prices['Bitcoin']:,.2f}
    Ethereum: {eth_qty} ETH = ${eth_qty * current_prices['Ethereum']:,.2f}
    Dogecoin: {doge_qty} DOGE = ${doge_qty * current_prices['Dogecoin']:,.2f}
    
    Total Worth: ${total_value:,.2f}
    Estimated Profit: ${profit:,.2f}
    """

    st.download_button(
        label="⬇️ Download Portfolio Report (TXT)",
        data=report_text,
        file_name="crypto_portfolio_report.txt",
        mime="text/plain"
    )

    st.markdown("---")
    st.caption("🌙 Designed by **Ammar Mughal** — Dark Theme Crypto App 🚀")


