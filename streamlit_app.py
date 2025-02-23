import streamlit as st
import pandas as pd

# Function to load Nasdaq-100 symbols from Wikipedia using pd.read_html
@st.cache_data
def load_symbols():
    url = "https://en.wikipedia.org/wiki/Nasdaq-100"
    tables = pd.read_html(url)
    # The Nasdaq-100 components table is assumed to be at index 5.
    nasdaq_table = tables[4]
    # Use "Symbol" or "Ticker" column based on availability.
    if "Symbol" in nasdaq_table.columns:
        symbols = nasdaq_table["Symbol"].tolist()
    elif "Ticker" in nasdaq_table.columns:
        symbols = nasdaq_table["Ticker"].tolist()
    else:
        st.error("Could not find the Symbol/Ticker column in the table.")
        symbols = []
    return symbols

# Load symbols from Wikipedia
symbols = load_symbols()

if not symbols:
    st.stop()

# Initialize the current symbol index in session state
if "index" not in st.session_state:
    st.session_state.index = 0

# Add a checkbox to toggle dark mode.
dark_mode = st.checkbox("Dark Mode", value=True)

# Create navigation buttons using columns.
col1, col2 = st.columns(2)
if col1.button("Previous"):
    st.session_state.index = (st.session_state.index - 1) % len(symbols)
if col2.button("Next"):
    st.session_state.index = (st.session_state.index + 1) % len(symbols)

# Get the current symbol and display it.
current_symbol = symbols[st.session_state.index]
st.write(f"### Chart for: {current_symbol}")

# Build the Finviz chart URL:
# Include the dark mode parameter if the checkbox is checked.
tm_param = "&tm=d" if dark_mode else ""
chart_url = (
    f"https://charts2-node.finviz.com/chart.ashx?"
    f"cs=&t={current_symbol}&tf=d&s=linear&ct=candle_stick"
    f"{tm_param}"
    f"&o[0][ot]=sma&o[0][op]=50&o[0][oc]=FF8F33C6"
    f"&o[1][ot]=sma&o[1][op]=200&o[1][oc]=DCB3326D"
    f"&o[2][ot]=patterns&o[2][op]=&o[2][oc]=000"
)

# Display the chart image.
st.image(chart_url, caption=f"{current_symbol} Chart")
