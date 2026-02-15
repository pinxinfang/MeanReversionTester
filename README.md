

# 📈 Mean Reversion Backtester

A high-performance quantitative research tool for simulating **mean reversion trading strategies** on historical equity data.

Built with **Streamlit** for an interactive UI and powered by **vectorized backtesting logic** for fast, efficient performance evaluation.

---

## 🚀 Features

### 🎛 Dynamic Parameter Tuning

Adjust strategy inputs in real time:

* Buy Threshold (% below previous close)
* Take Profit (% target)
* Stop Loss (% risk control)
* Transaction Costs

All updates instantly reflect in performance metrics and charts.

---

### 📊 Institutional-Grade Performance Metrics

Automatically calculates:

* **Sharpe Ratio** – Risk-adjusted return measurement
* **Max Drawdown** – Peak-to-trough capital decline
* **Profit Factor** – Gross profits ÷ Gross losses
* Total Return
* Win Rate
* Trade Count

---

### 📈 Interactive Visualizations

* **Equity Curve** – Portfolio growth over time
* **Underwater Chart** – Visual drawdown analysis
* Trade signal overlays on price charts

All charts are powered by Plotly for smooth interactivity.

---

## 🧠 Strategy Logic

This application implements a simple **daily mean reversion strategy**:

### 📌 Setup

* Monitors the previous day’s closing price.

### 🟢 Entry Rule

* Buy when the current price drops a defined percentage below the previous close
  *(oversold condition)*

### 🔴 Exit Rules

* Take Profit: Price rises by a defined percentage
* Stop Loss: Price drops to risk threshold
* Optional transaction cost adjustment

---

## 🛠 Installation & Setup

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/pinxinfang/MeanReversionTester.git
cd MeanReversionTester
```

### 2️⃣ Install Dependencies

```bash
pip install streamlit pandas yfinance plotly numpy
```

Or use a virtual environment (recommended):

```bash
python -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
pip install -r requirements.txt
```

### 3️⃣ Run the App

```bash
streamlit run backtester.py
```

The application will open automatically in your browser.

---

## ⚡ Technical Highlights

* Fully vectorized performance calculations (no slow loops)
* Efficient pandas-based signal generation
* Real-time portfolio equity tracking
* Clean modular architecture for easy strategy expansion

---

## 📂 Project Structure

```
MeanReversionTester/
│
├── backtester.py        # Main Streamlit application
├── requirements.txt     # Dependencies
└── README.md
```

---

## 🔮 Future Improvements

* Multi-asset portfolio testing
* Walk-forward optimization
* Position sizing models
* Monte Carlo simulation
* Strategy comparison dashboard

---

## ⚠️ Disclaimer

This project is for **educational and research purposes only**.
It does **not** constitute financial advice, investment recommendation, or trading guidance.

Trading involves risk. Past performance does not guarantee future results.
