import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- Page Config ---
st.set_page_config(page_title="Quant Backtester | Mean Reversion", layout="wide")
st.title("📈 High-Performance Mean Reversion Backtester")
st.markdown("Developed for high-fidelity quantitative analysis.")

# --- Sidebar Inputs ---
st.sidebar.header("Strategy Parameters")
ticker = st.sidebar.text_input("Ticker Symbol", value="SPY")
start_date = st.sidebar.date_input("Start Date", datetime.now() - timedelta(days=365*5))
end_date = st.sidebar.date_input("End Date", datetime.now())

buy_threshold = st.sidebar.slider("Buy Threshold % (Below Prev Close)", 0.5, 5.0, 1.5, 0.1) / 100
sell_threshold = st.sidebar.slider("Sell Threshold % (Above Entry)", 0.5, 10.0, 3.0, 0.1) / 100
transaction_cost = st.sidebar.number_input("Transaction Cost %", value=0.1, step=0.01) / 100
initial_capital = 10000

# --- Data Engine ---
@st.cache_data
def get_data(symbol, start, end):
    df = yf.download(symbol, start=start, end=end)
    # Handle multi-index columns if yfinance returns them
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df

data = get_data(ticker, start_date, end_date)

if data.empty:
    st.error("No data found for the ticker. Please check the symbol and dates.")
    st.stop()

# --- Core Strategy Logic (Vectorized) ---
def run_backtest(df, buy_limit, sell_limit, fee, capital):
    df = df.copy()
    df['Prev_Close'] = df['Close'].shift(1)
    
    # State tracking
    cash = capital
    position = 0
    entry_price = 0
    equity = []
    trade_log = []

    # Iterative simulation for path-dependent logic (Entry/Exit)
    # While signal generation can be vectorized, portfolio accounting 
    # with specific entry-based sell targets is more robust via a loop.
    for date, row in df.iterrows():
        price = row['Close']
        prev_close = row['Prev_Close']
        
        # BUY Logic: If price drops below threshold and we are flat
        if position == 0 and not np.isnan(prev_close):
            if price <= prev_close * (1 - buy_limit):
                shares_to_buy = cash // (price * (1 + fee))
                if shares_to_buy > 0:
                    cost = shares_to_buy * price * (1 + fee)
                    cash -= cost
                    position = shares_to_buy
                    entry_price = price
                    trade_log.append({'Date': date, 'Side': 'BUY', 'Price': price, 'Value': cost})

        # SELL Logic: If price hits target above entry
        elif position > 0:
            if price >= entry_price * (1 + sell_limit):
                revenue = position * price * (1 - fee)
                cash += revenue
                trade_log.append({'Date': date, 'Side': 'SELL', 'Price': price, 'Value': revenue})
                position = 0
                entry_price = 0
        
        current_equity = cash + (position * price)
        equity.append(current_equity)

    df['Equity'] = equity
    return df, pd.DataFrame(trade_log)

df_results, trade_log = run_backtest(data, buy_threshold, sell_threshold, transaction_cost, initial_capital)

# --- Jane Street Analytics ---
def calculate_metrics(df, logs):
    returns = df['Equity'].pct_change().dropna()
    total_ret = (df['Equity'].iloc[-1] / initial_capital) - 1
    
    # Annualized Sharpe (assuming 252 trading days)
    sharpe = np.sqrt(252) * (returns.mean() / returns.std()) if returns.std() != 0 else 0
    
    # Max Drawdown
    rolling_max = df['Equity'].cummax()
    drawdown = (df['Equity'] - rolling_max) / rolling_max
    max_dd = drawdown.min()
    
    # Profit Factor
    if not logs.empty and 'SELL' in logs['Side'].values:
        gains = logs[logs['Side'] == 'SELL']['Value'].sum()
        losses = logs[logs['Side'] == 'BUY']['Value'].sum()
        # Simple PF approximation: Gross Wins / Gross Losses
        # More accurately: Sum of winning trades / Sum of losing trades
        pf = (df['Equity'].iloc[-1] / initial_capital) # Placeholder for complex PF
    else:
        pf = 0

    return total_ret, sharpe, max_dd, drawdown

total_ret, sharpe, max_dd, drawdown_series = calculate_metrics(df_results, trade_log)

# --- Display Metrics ---
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Return", f"{total_ret:.2%}")
m2.metric("Sharpe Ratio", f"{sharpe:.2f}")
m3.metric("Max Drawdown", f"{max_dd:.2%}")
m4.metric("Trades Executed", len(trade_log))

# --- Visualizations ---
# Equity Curve
fig_equity = go.Figure()
fig_equity.add_trace(go.Scatter(x=df_results.index, y=df_results['Equity'], name="Portfolio Value", line=dict(color='#00ff88')))
fig_equity.update_layout(template="plotly_dark", title="Equity Curve", margin=dict(l=20, r=20, t=40, b=20), height=400)
st.plotly_chart(fig_equity, use_container_width=True)

# Underwater Chart
fig_dd = go.Figure()
fig_dd.add_trace(go.Scatter(x=df_results.index, y=drawdown_series, fill='tozeroy', name="Drawdown", line=dict(color='#ff4b4b')))
fig_dd.update_layout(template="plotly_dark", title="Underwater Chart (Drawdown %)", margin=dict(l=20, r=20, t=40, b=20), height=250)
st.plotly_chart(fig_dd, use_container_width=True)

# --- Trade Log & Export ---
st.subheader("Trade Log")
if not trade_log.empty:
    st.dataframe(trade_log.style.format({"Price": "{:.2f}", "Value": "{:.2f}"}), use_container_width=True)
    csv = trade_log.to_csv(index=False).encode('utf-8')
    st.download_button("Download Trade Log CSV", csv, "trade_log.csv", "text/csv")
else:
    st.write("No trades executed with current parameters.")