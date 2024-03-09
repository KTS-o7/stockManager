import streamlit as st 
import SessionState
import mysql.connector
import yfinance as yf
import os
import pandas as pd

mysql_config = {
'user': 'mysql',
'password': 'mysql',
'host': '127.0.0.1',
'port': '3306',
'database': 'STOCKMANAGER',
'raise_on_warnings': True,}

conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

def plot_company_data(company_name):
    # Title for the plot
    st.subheader(f"Plot : {company_name}")

    # Construct the file path
    file_path = os.path.join("data", "companyData/US/", f"{company_name}.csv")

    # Read the CSV file into a DataFrame
    df = pd.read_csv(file_path)
    # Convert 'Date' column to datetime format
    df['Date'] = pd.to_datetime(df['Date'],utc=True)

    # Plot the data
    st.line_chart(df.set_index('Date')['Close'])


def show(session_state: SessionState):
    if not session_state.is_authenticated:
        st.error("You must be logged in to access this page.")
        return
    st.title(f"Hello {session_state.clientName}!")
    st.subheader("Welcome to your dashboard.")
    col1,col2,col3 = st.columns(3)
    query = f"""SELECT p.portID, p.portName, SUM(s.Curr) AS portfolioValue
                FROM HAS h, STOCK s, PORTFOLIO p, USER u
                WHERE h.stockId = s.stockID
                AND h.portId = p.portID
                AND p.UID = u.UID
                AND u.Name = "{session_state.clientName}"
                GROUP BY p.portID, p.portName;"""
    cursor.execute(query)
    result = cursor.fetchall()
    #print(result)
    # Fetching NASDAQ data
    nasdaq_data = yf.Ticker("^IXIC")
    nasdaq_info = nasdaq_data.info

    # Fetching NYSE data
    nyse_data = yf.Ticker("^NYA")
    nyse_info = nyse_data.info
    
    # Fetching Nifty 50 data
    nifty_data = yf.Ticker("^NSEI")
    nifty_info = nifty_data.info
    with col1:
        st.metric(f"{result[0][0]}", f"{result[0][1]}", f"{result[0][2]} $")
        # Print all available keys
        #st.write(nifty_info.keys())
    # # If 'regularMarketPreviousClose' is in the keys, display it
        if 'regularMarketPreviousClose' in nifty_info:
            nifty_price = nifty_info['regularMarketPreviousClose']
            st.metric("Current Levels","Nifty 50",f"{nifty_price} ",delta_color="off")
        
    with col2:
        st.metric(f"{result[1][0]}", f"{result[1][1]}", f"{result[1][2]} $")
        if 'regularMarketPreviousClose' in nasdaq_info:
            nasdaq_price = nasdaq_info['regularMarketPreviousClose']
            st.metric("Current Levels","NASDAQ",  f"{nasdaq_price}")


    with col3:
        st.metric(f"{result[2][0]}", f"{result[2][1]}", f"{result[2][2]} $")
        if 'regularMarketPreviousClose' in nyse_info:
            nyse_price = nyse_info['regularMarketPreviousClose']
            st.metric("Current Levels","NYSE", f"{nyse_price}")
            
            
            
    getTransactQuery = f"""SELECT DISTINCT TB.cCode
FROM USER U
JOIN PORTFOLIO P ON U.UID = P.UID
JOIN HAS H ON P.portID = H.portId
JOIN TRADEDBY TB ON H.stockId = TB.stockId
WHERE U.UID = '{session_state.username}';
"""
    cursor.execute(getTransactQuery)
    resultDF = cursor.fetchall()
    compList = []
    for i in range(len(resultDF)):
        compList.append(resultDF[i][0])
    
    with col1:
        plot_company_data(compList[0])
    with col2:
        plot_company_data(compList[1])
    with col3:
        plot_company_data(compList[2])

session_state = SessionState.get(is_authenticated=False, option=None, register=None, username=None,clientName=None)
show(session_state) 
conn.close()