import streamlit as st
import SessionState
import backtrader as bt
import subprocess


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
        
        
def app():
    
    session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None,runBT=False)
    if session_state.username is None:
        st.write("Please sign in")
        col1, col2, col3 = st.columns(3)
        col1.metric("Stock Value", "70 $", "1.2%")
        col2.metric("IndexName", "22000", "+8%")
        col3.metric("IndexName2", "56000", "-4%")
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