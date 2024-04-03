import streamlit as st
import SessionState
import backtrader as bt
import subprocess
import yfinance as yf


st.set_page_config(layout="wide")

def save_strategy(strategy_code):
        with open('strategies.py', 'w') as file:
                file.write(strategy_code)

def run_trader(principal_amount,filename):
    try:
        result = subprocess.run(['python', 'trader.py', str(principal_amount),str(filename)], capture_output=True, text=True, check=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return e.stderr
        
def print_aboutUs():
        st.title("About Us")
        st.markdown('<style>h1{color: #DDDDDD; text-align: center;}</style>', unsafe_allow_html=True)
    
        st.markdown("""
    <div style="color: #DDDDDD; font-size: 24px; font-weight: bold;">Welcome to our stock analysis and backtesting platform.</div>
    <ul>
        <li style="color: #DDDDDD; font-size: 20px;">We are a group of passionate undergraduate students who are on a mission to make life easier for people dipping their toes into the fintech world.</li>
        <li style="color: #DDDDDD; font-size: 20px;">Our platform provides users with the tools they need to backtest genetic algorithms and carry out successful trades.</li>
        <li style="color: #DDDDDD; font-size: 20px;">With our innovative approach, we aim to revolutionize the <span style="font-weight: bold;">way people interact with financial markets</span> and <span style="font-weight: bold;">empower them to make informed decisions</span>.</li>
    </ul>
    """, unsafe_allow_html=True)

        st.markdown('<style>h3{color: #DDDDDD; text-align: center;}</style>', unsafe_allow_html=True)
        st.subheader("Our Team")
        st.markdown("""<div style="color: #DDDDDD; font-size: 24px; font-weight: bold;">Meet our team of talented individuals who are dedicated to making a difference in the fintech world.</div>
        """,unsafe_allow_html=True)
        st.write("\n")
        col1, col2 = st.columns(2)
        with col1:
            #st.image("https://avatars.githubusercontent.com/u/45279662?v=4", use_column_width=False)
            st.markdown("""
            #### Krishnatejaswi S
            **Skills**:
            - LangChain
            - Ollama
            - Python
            - MongoDB
            - Streamlit
            """)
        with col2:
            #st.image("https://avatars.githubusercontent.com/u/45279662?v=4", use_column_width=False)
            st.markdown("""
            #### Likhith
            **Skills**:
            - Python
            - Databases
            - Numpy
            - C++
            """)        
def app():
    
    session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None,runBT=False)
    if session_state.username is None:
        st.header("Welcome to Stock Manager !")
        st.markdown(" **Current market levels**")
         # Fetching NASDAQ data
        nasdaq_data = yf.Ticker("^IXIC")
        nasdaq_info = nasdaq_data.info

        # Fetching NYSE data
        nyse_data = yf.Ticker("^NYA")
        nyse_info = nyse_data.info
        
        # Fetching Nifty 50 data
        nifty_data = yf.Ticker("^NSEI")
        nifty_info = nifty_data.info
        col1,col2,col3 = st.columns(3)
        with col1:
            if 'regularMarketPreviousClose' in nifty_info:
                nifty_price = nifty_info['regularMarketPreviousClose']
                st.metric("Current Levels","Nifty 50",f"{nifty_price} ",delta_color="off")
            
        with col2:  
            if 'regularMarketPreviousClose' in nasdaq_info:
                nasdaq_price = nasdaq_info['regularMarketPreviousClose']
                st.metric("Current Levels","NASDAQ",  f"{nasdaq_price}")


        with col3:
            if 'regularMarketPreviousClose' in nyse_info:
                nyse_price = nyse_info['regularMarketPreviousClose']
                st.metric("Current Levels","NYSE", f"{nyse_price}")
        
        print_aboutUs()
       
        
    else:
        st.header(f"Welcome, {session_state.clientName}!")
        st.write("\n\n\n\n")
        st.title("Automated Back Testing")

    # Text area for user input (strategy code)
        strategy_code = st.text_area("Enter your strategy code here:")
        f = st.file_uploader("Upload a file", type=(["tsv","csv","txt","tab","xlsx","xls"]))
        if f is not None:
            l = f.name.split(".")
            path_in = l[0]
            print(path_in)
        else:
            path_in = None

    # Input for initial principal amount
        principal_amount = st.number_input("Enter initial principal amount:", value=1000000000.0)
    
    # Button to save the strategy and run the trader
        if st.button("Save and Run Trader"):
            session_state.runBT = True
            if session_state.runBT:
                save_strategy(strategy_code)
                st.write("Strategy saved successfully!")
        
        # Run trader.py with initial principal amount as argument
                output = run_trader(principal_amount,path_in)
        
        # Display the output
                st.subheader("Trader Output:")
                st.text(output)
        
        

app()