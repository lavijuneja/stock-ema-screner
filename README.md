# 📈 Stock EMA Screener - Streamlit App

Ek powerful stock screening tool jo NSE stocks ko check karta hai ke woh **EMA 20, 50, 100, 150, 200 se upar** trading kar rahe hain ya nahi.

## Installation

### Step 1: Python install करें
Python 3.8+ होना चाहिए

### Step 2: Requirements install करें
```bash
pip install -r requirements.txt
```

## चलाने के लिए

```bash
streamlit run stock_ema_screener.py
```

यह command चलाने के बाद browser automatically खुल जाएगा।

## कैसे इस्तेमाल करें

1. **Left sidebar में stock symbol enter करें**
   - Example: `RELIANCE`, `INFY`, `HDFC`
   - .NS suffix automatic add हो जाएगा

2. **Add button दबाएं** 
   - Stock list में add हो जाएगा

3. **Multiple stocks add करें** (जितने चाहें)

4. **"Analyze Stocks" button दबाएं**
   - सभी stocks के data download होगा
   - EMAs calculate होंगे
   - Results दिखेंगे

## Features

✅ **Real-time data** - yfinance से latest data  
✅ **5 EMA calculation** - 20, 50, 100, 150, 200  
✅ **Quick screening** - कौन से stocks qualify करते हैं  
✅ **Interactive charts** - Plotly graphs  
✅ **Status indicator** - Green = ABOVE ALL, Red = Below Some  

## Output

### Table
- Current Price
- EMA values
- Status (✅ or ❌)

### Charts
- Line chart with Price + all 5 EMAs
- Last 100 days का data
- Hover करके exact values देख सकते हो

## Example Stocks (NSE)

```
RELIANCE    - Reliance Industries
INFY        - Infosys
HDFC        - HDFC Bank
TCS         - Tata Consultancy Services
WIPRO       - Wipro
HDFCBANK    - HDFC Bank
```

## Notes

- Calculation के लिए 300 days का historical data लेता है
- Chart में last 100 days दिखाता है
- EMA20 sabse sensitive है, EMA200 sabse stable है
- Strong uptrend में: Price > EMA20 > EMA50 > EMA100 > EMA150 > EMA200

---

**Happy Trading! 🚀**
