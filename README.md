# 📈 Mean Reversion Backtester

A high-performance quantitative analysis tool built for simulating mean reversion strategies. This application leverages **Streamlit** for the interface and **Vectorized Backtesting** logic to evaluate trade performance over historical equity data.

## 🚀 Key Features
* **Dynamic Parameter Tuning:** Live sliders for Buy/Sell thresholds and transaction costs.
* **Institutional-Grade Metrics:** Automated calculation of:
    * **Sharpe Ratio:** Risk-adjusted return performance.
    * **Max Drawdown:** Peak-to-trough risk assessment.
    * **Profit Factor:** Gross gains vs. gross losses.
* **Interactive Visualizations:** * **Equity Curve:** Real-time portfolio value tracking.
    * **Underwater Chart:** Visual representation of drawdown periods.

## 🛠️ Installation & Setup
1. Clone the Repository:
   ```bash
   git clone [https://github.com/pinxinfang/MeanReversionTester.git](https://github.com/pinxinfang/MeanReversionTester.git)
   cd MeanReversionTester

2. Install dependencies:
    pip install streamlit pandas yfinance plotly numpy

3. Run the app:
    streamlit run backtester.py

🧠 Strategy Logic
This tool implements a Mean Reversion strategy:

The Setup: Monitors the previous day's closing price.

Entry: Triggers a 'Buy' when the price drops a specific percentage below that close (oversold).

Exit: Sells when the price hits a target profit percentage or triggers an emergency Stop Loss.

Disclaimer: For educational purposes only. Not financial advice.