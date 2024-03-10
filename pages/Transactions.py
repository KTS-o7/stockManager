import streamlit as st
import mysql.connector
from mysql.connector import Error
import pandas as pd
from datetime import datetime
import SessionState
st.set_page_config(layout="wide")
# Function to establish database connection
def connect_to_database():
    try:
        mysql_config = {
            'user': 'mysql',
            'password': 'mysql',
            'host': '127.0.0.1',
            'port': '3306',
            'database': 'STOCKMANAGER',
            'raise_on_warnings': True,
        }
        conn = mysql.connector.connect(**mysql_config)
        return conn
    except Error as e:
        st.error(f"Error connecting to database: {e}")
        return None
# Function to fetch user transactions
def fetch_user_transactions(username):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to fetch user transactions
            query = """
                    SELECT t.accNo, t.type, t.value, t.quantity, t.timestamp, p.portName, s.stockID, c.cName
                    FROM TRANSACTS t, PORTFOLIO p, STOCK s, COMPANY c, HAS h, USER u
                    WHERE t.portId = p.portID
                    AND t.stockId = s.stockID
                    AND p.portID = h.portId
                    AND s.stockID = h.stockId
                    AND p.UID = u.UID
                    AND u.Name =  %s;
                    """
            cursor.execute(query, (username,))
            result = cursor.fetchall()
            return result
        except Error as e:
            st.error(f"Error fetching user transactions: {e}")
        finally:
            conn.close()

# Streamlit interface
def show(session_state):
    if not session_state.is_authenticated:
        st.error("You must be logged in to access this page.")
        return

    st.title("Transaction History")

    # Get the clientname from session state
    clientname = session_state.clientName

    # Fetch and display user transactions
    transactions = fetch_user_transactions(clientname)
    #print(transactions)
    if transactions:
        #st.write(transactions)
        transactions_df = pd.DataFrame(transactions, columns=["Transaction ID", "Type", "Value", "Quantity", "Timestamp", "Portfolio", "Stock ID", "Company"])
        st.dataframe(transactions_df)
    else:
        st.info("No transactions found.")
        

# Initialize session state
session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None,runBT=False)
show(session_state)
