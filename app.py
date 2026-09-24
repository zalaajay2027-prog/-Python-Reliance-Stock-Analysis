import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Page Configuration

st.set_page_config(
    page_title="Reliance Stock Analysis",
    page_icon="📈",
    layout="wide"
)


# Title

st.title(" Reliance Stock Price Analysis")

st.write(
    "This application analyzes historical Reliance stock data "
    "using Python, Pandas, and Matplotlib."
)

# Load DataSet

@st.cache_data
def load_data():
    data = pd.read_csv("Reliance.csv")
    return data


data = load_data()


# Dataset Preview

st.subheader(" Dataset Preview")

st.dataframe(data, use_container_width=True)


# Dataset Information

st.subheader(" Dataset Information")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Total Rows",
        data.shape[0]
    )

with col2:
    st.metric(
        "Total Columns",
        data.shape[1]
    )

with col3:
    st.metric(
        "Missing Values",
        int(data.isnull().sum().sum())
    )

# Handel Missing Values

clean_data = data.dropna().copy()

st.subheader(" Cleaned Data")

st.write(
    f"Original rows: {len(data)} | "
    f"Rows after removing missing values: {len(clean_data)}"
)

# Check Required Columan


required_columns = ["Close"]

if "Volume" not in clean_data.columns:
    st.warning(
        " Volume column was not found in Reliance.csv. "
        "Trading Volume chart cannot be displayed."
    )

if "Close" not in clean_data.columns:
    st.error(
        " Close column was not found in Reliance.csv."
    )

    st.stop()


# Closing Price


st.subheader(" Reliance Closing Price")

fig1, ax1 = plt.subplots(figsize=(12, 5))

ax1.plot(
    clean_data["Close"],
    label="Closing Price"
)

ax1.set_title("Reliance Stock Closing Price")
ax1.set_xlabel("Trading Days")
ax1.set_ylabel("Price")
ax1.legend()
ax1.grid(True)

st.pyplot(fig1)


#  Trading Volume

if "Volume" in clean_data.columns:

    st.subheader(" Reliance Trading Volume")

    fig2, ax2 = plt.subplots(figsize=(12, 4))

    ax2.bar(
        clean_data.index,
        clean_data["Volume"]
    )

    ax2.set_title("Reliance Trading Volume")
    ax2.set_xlabel("Trading Days")
    ax2.set_ylabel("Volume")

    st.pyplot(fig2)


# Daily Return

clean_data["Daily Return"] = (
    clean_data["Close"].pct_change()
)


st.subheader(" Daily Returns")

fig3, ax3 = plt.subplots(figsize=(12, 5))

ax3.plot(
    clean_data["Daily Return"],
    label="Daily Return"
)

ax3.set_title("Reliance Daily Returns")
ax3.set_xlabel("Trading Days")
ax3.set_ylabel("Return")
ax3.legend()
ax3.grid(True)

st.pyplot(fig3)

# Summry

st.subheader(" Stock Summary")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Latest Close",
        f"₹{clean_data['Close'].iloc[-1]:.2f}"
    )

with col2:
    st.metric(
        "Highest Close",
        f"₹{clean_data['Close'].max():.2f}"
    )

with col3:
    st.metric(
        "Lowest Close",
        f"₹{clean_data['Close'].min():.2f}"
    )

with col4:
    avg_return = clean_data["Daily Return"].mean() * 100

    st.metric(
        "Average Daily Return",
        f"{avg_return:.2f}%"
    )


# Download  Cleaned Data

st.subheader(" Download Processed Data")

csv = clean_data.to_csv(index=False)

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="Reliance_Stock_Analysis.csv",
    mime="text/csv"
)

# Footer

st.markdown("---")

st.caption(
    "Reliance Stock Analysis | Python + Pandas + Matplotlib + Streamlit"
)