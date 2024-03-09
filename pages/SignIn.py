import streamlit as st
import SessionState
from passlib.hash import bcrypt
import time
import toml
import mysql.connector

# Load the MySQL connection details from secrets.toml
mysql_config = {
'user': 'mysql',
'password': 'mysql',
'host': '127.0.0.1',
'port': '3306',
'database': 'STOCKMANAGER',
'raise_on_warnings': True,}

# Establish a connection to the MySQL database
#@st.cache_resource


conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()
#conn.reconnect(mysql_config)

def authenticate(username, password):
    # Fetch the hashed password from the database
    query = "SELECT Password FROM USER WHERE UID = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        hashed_password = result[0]
        # Check if the provided password matches the hashed password
        if bcrypt.verify(password, hashed_password):
            return True
    return False

def register(username, password, name, email, phone_number):
    # Check if the username already exists
    query = "SELECT * FROM USER WHERE UID = %s"
    cursor.execute(query, (username,))
    result = cursor.fetchone()

    if result:
        return False

    # Hash the password
    hashed_password = bcrypt.hash(password)

    # Insert the new user into the database
    query = "INSERT INTO USER (UID, Name, Email, Password, PhoneNumber) VALUES (%s, %s, %s, %s, %s)"
    values = (username, name, email, hashed_password, phone_number)
    cursor.execute(query, values)
    conn.commit()

    return True

def show(session_state: SessionState):
    st.title("Sign In / Register")

    # Allow the user to choose between registering and logging in
    if  not session_state.option and  not session_state.register and not session_state.is_authenticated:
        session_state.option = st.button("Sign In")
        session_state.register = st.button("Register")

    if session_state.register:
        st.subheader("Register")
        reg_username = st.text_input("New Username")
        reg_password = st.text_input("New Password", type="password")
        reg_name = st.text_input("Name")
        reg_email = st.text_input("Email")
        reg_phone_number = st.text_input("Phone Number")
        if st.button("Submit Registration"):
            if reg_username != "" and register(reg_username, reg_password, reg_name, reg_email, reg_phone_number) and reg_password != "":
                st.success("Registration successful!")
                if(session_state.register):
                    session_state.register = False
            elif reg_username == "":
                st.error("Please enter a username!")
            elif reg_password == "":
                st.error("Please enter a password!")
            else:
                st.error("Username already exists!")
                if(session_state.register):
                    session_state.register = False

    elif session_state.option and not session_state.is_authenticated:
        st.subheader("Log In")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Submit Login"):
            if authenticate(username, password):
                session_state.is_authenticated = True
                session_state.username = username
                st.success("You have successfully logged in!")
                if(session_state.option):
                    session_state.option = False
                cursor.execute("SELECT Name FROM USER WHERE UID = %s", (username,))
                result = cursor.fetchone()
                session_state.clientName = result[0]
                print(session_state.clientName)
                with st.spinner("Redirecting..."):
                    time.sleep(2)
                    st.switch_page("./Home.py")
            else:
                st.error("Invalid username or password")

    # If the user is already authenticated, show the logout button
    if session_state.is_authenticated:
        if st.button("Logout"):
            session_state.is_authenticated = False
            session_state.username = None
            session_state.option = None
            session_state.register = None
            st.success("You have been logged out!")

    # Example of using st.connection to cache database queries
   # Example of using st.connection to cache database queries
    #conn = st.connection('mysql',type='sql')
    #cursor.execute("SELECT * FROM USER")
    #df = cursor.fetchall()
    #print(df)
    #for row in df:
        #st.write(f"{row[0]} - {row[1]} - {row[2]} - {row[3]}")

# Call the show() function to render the content
session_state = SessionState.get(is_authenticated=False, option=None, register=None, username=None,clientName=None)
show(session_state)

# Close the database connection
#print("closingConnection")
conn.close()    