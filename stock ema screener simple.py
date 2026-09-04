import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import plotly.graph_objects as go
import hashlib

# Page config
st.set_page_config(page_title="Stock EMA Screener", layout="wide")

# ============================================
# SIMPLE PASSWORD AUTHENTICATION
# ============================================

# User credentials (change these to your own!)
USERS = {
    "sahaz": "password123",
    "admin": "admin123",
    "user": "user123"
}

def hash_password(password):
    """Hash password for security"""
    return hashlib.sha256(password.encode()).hexdigest()

def check_login(username, password):
    """Check if username and password are correct"""
    if username in USERS:
        return USERS[username] == password
    return False

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.username = None

# ============================================
# LOGIN PAGE
# ============================================

if not st.session_state.logged_in:
    st.title("🔐 Stock EMA Screener")
    st.markdown("---")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        st.markdown("### 👤 Login")
        
        username = st.text_input("Username:", placeholder="Enter username")
        password = st.text_input("Password:", type="password", placeholder="Enter password")
        
        if st.button("🔓 Login", use_container_width=True):
            if username and password:
                if check_login(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("✅ Login successful!")
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
            else:
                st.warning("⚠️ Please enter username and password")
        
        st.markdown("---")
        st.markdown("""
        ### 📝 Test Credentials:
        
        | Username | Password |
        |----------|----------|
        | sahaz | password123 |
        | admin | admin123 |
        | user | user123 |
        """)

# ============================================
# MAIN APP (After Login)
# ============================================

else:
    
    # Top bar with logout
    col1, col2, col3 = st.columns([3, 1, 1])
    with col1:
        st.title("📈 Stock EMA Screener")
        st.markdown(f"**👤 Logged in as: {st.session_state.username}**")
    
    with col3:
        if st.button("🔓 Logout"):
            st.session_state.logged_in = False
            st.session_state.username = None
            st.rerun()
    
    st.markdown("**Check stocks trading above EMA 20, 50, 100, 150, 200**")
    st.markdown("---")
    
    # Initialize session state for app
    if 'stocks' not in st.session_state:
        st.session_state.stocks = []
    if 'results' not in st.session_state:
        st.session_state.results = None
    
    # Sidebar for adding stocks
    st.sidebar.header("➕ Add Stocks")
    col1, col2 = st.sidebar.columns([3, 1])
    with col1:
        stock_input = st.sidebar.text_input(
            "Enter stock symbol (e.g., RELIANCE, INFY, HDFC)",
            placeholder="RELIANCE"
        )
    with col2:
        add_btn = st.sidebar.button("Add", use_container_width=True)
    
    if add_btn and stock_input:
        if stock_input.upper() not in [s.replace('.NS', '') for s in st.session_state.stocks]:
            # Add .NS suffix for NSE if not present
            symbol = stock_input.upper() if ".NS" in stock_input.upper() else f"{stock_input.upper()}.NS"
            st.session_state.stocks.append(symbol)
            st.sidebar.success(f"✅ Added {symbol}")
        else:
            st.sidebar.warning(f"⚠️ {stock_input.upper()} already added")
    
    # Display added stocks
    if st.session_state.stocks:
        st.sidebar.markdown("---")
        st.sidebar.subheader(f"📊 Stocks ({len(st.session_state.stocks)})")
        for stock in st.session_state.stocks:
            col1, col2 = st.sidebar.columns([3, 1])
            with col1:
                st.write(f"• {stock}")
            with col2:
                if st.sidebar.button("✕", key=f"remove_{stock}", use_container_width=True):
                    st.session_state.stocks.remove(stock)
                    st.rerun()
    
    # Main analysis
    if st.session_state.stocks:
        # Download and calculate EMAs
        if st.button("🔍 Analyze Stocks", use_container_width=True, type="primary"):
            progress_bar = st.progress(0)
            status_text = st.empty()
            
            results_data = []
            
            for idx, stock in enumerate(st.session_state.stocks):
                status_text.text(f"⏳ Processing {stock}...")
                progress_bar.progress((idx + 1) / len(st.session_state.stocks))
                
                try:
                    # Download data - get last 300 days for EMA calculation
                    end_date = datetime.now()
                    start_date = end_date - timedelta(days=300)
                    
                    df = yf.download(stock, start=start_date, end=end_date, progress=False, interval="1d")
                    
                    if df.empty:
                        results_data.append({
                            'Stock': stock,
                            'Price': 'N/A',
                            'EMA20': 'N/A',
                            'EMA50': 'N/A',
                            'EMA100': 'N/A',
                            'EMA150': 'N/A',
                            'EMA200': 'N/A',
                            'Status': '❌ No Data',
                            'Above All': False
                        })
                        continue
                    
                    # Calculate EMAs
                    df['EMA20'] = df['Close'].ewm(span=20, adjust=False).mean()
                    df['EMA50'] = df['Close'].ewm(span=50, adjust=False).mean()
                    df['EMA100'] = df['Close'].ewm(span=100, adjust=False).mean()
                    df['EMA150'] = df['Close'].ewm(span=150, adjust=False).mean()
                    df['EMA200'] = df['Close'].ewm(span=200, adjust=False).mean()
                    
                    # Get latest values
                    latest = df.iloc[-1]
                    current_price = latest['Close']
                    ema20 = latest['EMA20']
                    ema50 = latest['EMA50']
                    ema100 = latest['EMA100']
                    ema150 = latest['EMA150']
                    ema200 = latest['EMA200']
                    
                    # Check if above all EMAs
                    above_all = (current_price > ema20 and 
                               current_price > ema50 and 
                               current_price > ema100 and 
                               current_price > ema150 and 
                               current_price > ema200)
                    
                    status = "✅ ABOVE ALL" if above_all else "❌ Below Some EMA"
                    
                    results_data.append({
                        'Stock': stock,
                        'Price': f"₹{current_price:.2f}",
                        'EMA20': f"₹{ema20:.2f}",
                        'EMA50': f"₹{ema50:.2f}",
                        'EMA100': f"₹{ema100:.2f}",
                        'EMA150': f"₹{ema150:.2f}",
                        'EMA200': f"₹{ema200:.2f}",
                        'Status': status,
                        'Above All': above_all,
                        'Price_Num': current_price,
                        'EMA20_Num': ema20,
                        'EMA50_Num': ema50,
                        'EMA100_Num': ema100,
                        'EMA150_Num': ema150,
                        'EMA200_Num': ema200,
                        'DF': df
                    })
                    
                except Exception as e:
                    results_data.append({
                        'Stock': stock,
                        'Price': 'Error',
                        'EMA20': 'Error',
                        'EMA50': 'Error',
                        'EMA100': 'Error',
                        'EMA150': 'Error',
                        'EMA200': 'Error',
                        'Status': f'❌ Error',
                        'Above All': False
                    })
            
            st.session_state.results = results_data
            progress_bar.empty()
            status_text.empty()
        
        # Display results
        if st.session_state.results:
            st.markdown("---")
            
            # Summary
            passing_stocks = [r for r in st.session_state.results if r['Above All']]
            st.subheader(f"📊 Results: {len(passing_stocks)}/{len(st.session_state.stocks)} stocks above all EMAs")
            
            if passing_stocks:
                st.success(f"✅ **{len(passing_stocks)} stock(s) qualify!**")
            else:
                st.warning("❌ No stocks above all EMAs currently")
            
            # Display table
            st.subheader("📋 Detailed Analysis")
            display_cols = ['Stock', 'Price', 'EMA20', 'EMA50', 'EMA100', 'EMA150', 'EMA200', 'Status']
            display_df = pd.DataFrame([{col: r[col] for col in display_cols} for r in st.session_state.results])
            
            # Create colored dataframe
            def color_status(val):
                if '✅' in str(val):
                    return 'background-color: #90EE90; font-weight: bold'
                elif '❌' in str(val):
                    return 'background-color: #FFB6C6'
                return ''
            
            try:
                styled_df = display_df.style.map(color_status, subset=['Status'])
            except AttributeError:
                styled_df = display_df.style.applymap(color_status, subset=['Status'])
            
            st.dataframe(styled_df, use_container_width=True)
            
            # Individual charts for qualifying stocks
            if passing_stocks:
                st.subheader("📈 Charts - Stocks Above All EMAs")
                
                for result in passing_stocks:
                    if 'DF' in result and result['DF'] is not None:
                        with st.expander(f"📊 {result['Stock']}", expanded=False):
                            df_chart = result['DF'].tail(100)  # Last 100 days
                            
                            fig = go.Figure()
                            
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['Close'], 
                                                    name='Close Price', line=dict(color='black', width=2)))
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA20'], 
                                                    name='EMA20', line=dict(color='blue')))
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA50'], 
                                                    name='EMA50', line=dict(color='green')))
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA100'], 
                                                    name='EMA100', line=dict(color='orange')))
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA150'], 
                                                    name='EMA150', line=dict(color='red')))
                            fig.add_trace(go.Scatter(x=df_chart.index, y=df_chart['EMA200'], 
                                                    name='EMA200', line=dict(color='purple')))
                            
                            fig.update_layout(
                                title=f"{result['Stock']} - EMA Analysis",
                                xaxis_title="Date",
                                yaxis_title="Price (₹)",
                                hovermode='x unified',
                                height=400
                            )
                            
                            st.plotly_chart(fig, use_container_width=True)
    
    else:
        st.info("👈 Stocks add करें sidebar से analysis शुरू करने के लिए")
        st.markdown("""
        ### 📖 कैसे इस्तेमाल करें:
        
        1. **Sidebar में stock symbol enter करें** (e.g., RELIANCE, INFY, HDFC)
        2. **Add button दबाएं**
        3. जितने stocks चाहें add करें
        4. **Analyze Stocks button** दबाएं
        5. देखें कौन से stocks सभी EMAs के above हैं
        
        ### 💡 EMA क्या है?
        - **EMA** = Exponential Moving Average
        - Stock के trend को दिखाता है
        - Strong uptrend = Price > EMA20 > EMA50 > EMA100 > EMA150 > EMA200
        
        ### 📊 Example Stocks:
        - RELIANCE - Reliance Industries
        - INFY - Infosys
        - HDFC - HDFC Bank
        - TCS - Tata Consultancy Services
        - WIPRO - Wipro
        """)
