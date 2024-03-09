import streamlit as st 
import SessionState
import mysql.connector
from mysql.connector import Error


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

# Function to calculate portfolio value
def calculate_portfolio_value(uid):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to fetch the current value of each stock in the user's portfolio
            query = """
                    SELECT SUM(TRANSACTS.quantity * STOCK.Curr) 
                    FROM TRANSACTS 
                    JOIN STOCK ON TRANSACTS.stockId = STOCK.stockID 
                    JOIN HAS ON TRANSACTS.stockId = HAS.stockId 
                    WHERE HAS.portId IN (SELECT portID FROM PORTFOLIO WHERE UID = %s)
                    """
            cursor.execute(query, (uid,))
            total_value = cursor.fetchone()[0]
            return total_value
        except Error as e:
            st.error(f"Error calculating portfolio value: {e}")
        finally:
            conn.close()

# Streamlit interface
def show(session_state):
    if not session_state.is_authenticated:
        st.error("You must be logged in to access this page.")
        return
    st.title("Portfolio Management")
    st.title("Stocks")
    
    # Get the user ID from session state
    uid = session_state.username
    # Calculate and display total value of portfolio
    total_value = calculate_portfolio_value(uid)
    if total_value is not None:
        st.metric("Total Portfolio Value", f"${total_value:.2f}")
        
        
# Initialize session state
session_state = SessionState.get(is_authenticated=False, option=None, register=None, username=None,clientName=None)
show(session_state)
