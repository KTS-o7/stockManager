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

# Function to calculate portfolio value and profit/loss
def calculate_portfolio_stats(uid):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to fetch the current value, purchase value, and profit/loss for each stock in the user's portfolio
            query = """
                    SELECT SUM(TRANSACTS.quantity * STOCK.Curr) AS current_value,
                           SUM(TRANSACTS.value) AS purchase_value,
                           SUM(TRANSACTS.quantity * STOCK.Curr) - SUM(TRANSACTS.value) AS profit_loss
                    FROM TRANSACTS
                    JOIN STOCK ON TRANSACTS.stockId = STOCK.stockID
                    JOIN HAS ON TRANSACTS.stockId = HAS.stockId
                    WHERE HAS.portId IN (SELECT portID FROM PORTFOLIO WHERE UID = %s)
                    """
            cursor.execute(query, (uid,))
            result = cursor.fetchone()
            return result
        except Error as e:
            st.error(f"Error calculating portfolio stats: {e}")
        finally:
            conn.close()

# Function to add a stock to the portfolio
def add_stock_to_portfolio(uid, stock_id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to get the portfolio ID for the user
            query = "SELECT portID FROM PORTFOLIO WHERE UID = %s LIMIT 1"
            cursor.execute(query, (uid,))
            portfolio_id = cursor.fetchone()[0]

            # Insert the stock into the HAS table
            insert_query = "INSERT INTO HAS (dateCreate, ownType, portId, stockId) VALUES (CURRENT_DATE(), 'Individual', %s, %s)"
            cursor.execute(insert_query, (portfolio_id, stock_id))
            conn.commit()
            st.success(f"Stock with ID {stock_id} added to your portfolio.")
        except Error as e:
            st.error(f"Error adding stock to portfolio: {e}")
            conn.rollback()
        finally:
            conn.close()

# Function to remove a stock from the portfolio
def remove_stock_from_portfolio(uid, stock_id):
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to get the portfolio ID for the user
            query = "SELECT portID FROM PORTFOLIO WHERE UID = %s LIMIT 1"
            cursor.execute(query, (uid,))
            portfolio_id = cursor.fetchone()[0]

            # Remove the stock from the HAS table
            delete_query = "DELETE FROM HAS WHERE portId = %s AND stockId = %s"
            cursor.execute(delete_query, (portfolio_id, stock_id))
            conn.commit()
            st.success(f"Stock with ID {stock_id} removed from your portfolio.")
        except Error as e:
            st.error(f"Error removing stock from portfolio: {e}")
            conn.rollback()
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

    # Calculate and display total portfolio value, profit, and loss
    portfolio_stats = calculate_portfolio_stats(uid)
    if portfolio_stats:
        current_value, purchase_value, profit_loss = portfolio_stats
        st.metric("Total Portfolio Value", f"${current_value:.2f}")
        st.metric("Total Profit/Loss", f"${profit_loss:.2f}", delta_color="inverse")

    # Display available stocks to add
    st.subheader("Add Stock to Portfolio")
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to fetch available stocks not already in the user's portfolio
            query = """
                    SELECT STOCK.stockID, TRADEDBY.cName
                    FROM STOCK
                    JOIN TRADEDBY ON STOCK.stockID = TRADEDBY.stockId
                    WHERE STOCK.stockID NOT IN (
                        SELECT HAS.stockId
                        FROM HAS
                        JOIN PORTFOLIO ON HAS.portId = PORTFOLIO.portID
                        WHERE PORTFOLIO.UID = %s
                    )
                    """
            cursor.execute(query, (uid,))
            available_stocks = cursor.fetchall()

            # Display available stocks as a selectbox
            selected_stock = st.selectbox("Select a stock to add", [f"{stock[1]} ({stock[0]})" for stock in available_stocks], key="add_stock")
            if selected_stock:
                stock_id = selected_stock.split(" (")[1].split(")")[0]
                if st.button("Add Stock"):
                    add_stock_to_portfolio(uid, stock_id)

        except Error as e:
            st.error(f"Error fetching available stocks: {e}")
        finally:
            conn.close()

    # Display stocks in the user's portfolio
    st.subheader("Stocks in Your Portfolio")
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Query to fetch stocks in the user's portfolio
            query = """
                    SELECT STOCK.stockID, TRADEDBY.cName
                    FROM STOCK
                    JOIN TRADEDBY ON STOCK.stockID = TRADEDBY.stockId
                    JOIN HAS ON STOCK.stockID = HAS.stockId
                    JOIN PORTFOLIO ON HAS.portId = PORTFOLIO.portID
                    WHERE PORTFOLIO.UID = %s
                    """
            cursor.execute(query, (uid,))
            portfolio_stocks = cursor.fetchall()

            # Display portfolio stocks as a selectbox
            selected_stock = st.selectbox("Select a stock to remove", [f"{stock[1]} ({stock[0]})" for stock in portfolio_stocks], key="remove_stock")
            if selected_stock:
                stock_id = selected_stock.split(" (")[1].split(")")[0]
                if st.button("Remove Stock"):
                    remove_stock_from_portfolio(uid, stock_id)

        except Error as e:
            st.error(f"Error fetching portfolio stocks: {e}")
        finally:
            conn.close()

# Initialize session state
session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None,runBT=False)
show(session_state)