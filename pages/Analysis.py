import pandas as pd
import streamlit as st
import yfinance
from summarizer import summarize
from pymongo.mongo_client import MongoClient
import SessionState

uri = "mongodb+srv://stockmanager:mongo@ktscluster.fnabh5x.mongodb.net/?retryWrites=true&w=majority&appName=KTSCluster"
mongoclient = MongoClient(uri)


st.set_page_config(layout="wide")

@st.cache_data()
def load_data():
    components = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_S" "%26P_500_companies"
    )[0]
    return components.set_index("Symbol")

@st.cache_data()
def load_quotes(asset):
    return yfinance.download(asset)

def main():
    if not session_state.is_authenticated:
        st.error("You must be logged in to access this page.")
        return
    col1,col2 = st.columns(2)
    components = load_data()
    title = st.empty()
    st.sidebar.title("Options")

    def label(symbol):
        a = components.loc[symbol]
        return symbol + " - " + a.Security

    if st.sidebar.checkbox("View companies list"):
        st.dataframe(
            components[["Security", "GICS Sector","GICS Sub-Industry", 'Date added', "Founded"]]
        )

    st.sidebar.subheader("Select assets")
    asset1 = st.sidebar.selectbox(
        "Click below to select the first asset",
        components.index.sort_values(),
        index=3,
        format_func=label,
    )
    asset2 = st.sidebar.selectbox(
        "Click below to select the second asset",
        components.index.sort_values(),
        index=4,
        format_func=label,
    )

    data1 = load_quotes(asset1)
    data1 = data1.copy().dropna()
    data1.index.name = None

    data2 = load_quotes(asset2)
    data2 = data2.copy().dropna()
    data2.index.name = None

    section = st.sidebar.slider(
        "Number of quotes",
        min_value=30,
        max_value=min([2000, data1.shape[0], data2.shape[0]]),
        value=500,
        step=10,
    )

    data1_section = data1[-section:]["Adj Close"].to_frame(f"{asset1} Adj Close")
    data2_section = data2[-section:]["Adj Close"].to_frame(f"{asset2} Adj Close")

    sma = st.sidebar.checkbox("SMA")
    if sma:
        period1 = st.sidebar.slider(
            "SMA period", min_value=5, max_value=500, value=20, step=1
        )
        data1_section[f"SMA {period1}"] = data1_section[f"{asset1} Adj Close"].rolling(period1).mean()
        data2_section[f"SMA {period1}"] = data2_section[f"{asset2} Adj Close"].rolling(period1).mean()

    sma2 = st.sidebar.checkbox("SMA2")
    if sma2:
        period2 = st.sidebar.slider(
            "SMA2 period", min_value=5, max_value=500, value=100, step=1
        )
        data1_section[f"SMA2 {period2}"] = data1_section[f"{asset1} Adj Close"].rolling(period2).mean()
        data2_section[f"SMA2 {period2}"] = data2_section[f"{asset2} Adj Close"].rolling(period2).mean()

    if st.sidebar.checkbox("View company info", True):
        with col1:
            st.subheader(f"{asset1} Company Info")
            st.table(components.loc[asset1])
        with col2:    
            st.subheader(f"{asset2} Company Info")
            st.table(components.loc[asset2])

    if st.sidebar.checkbox("View statistic"):
        with col1:
            st.subheader(f"{asset1} Statistics")
            st.table(data1_section.describe())
        with col2:
            st.subheader(f"{asset2} Statistics")
            st.table(data2_section.describe())

    if st.sidebar.checkbox("View quotes"):
        with col1:
            st.subheader(f"{asset1} historical data")
            st.write(data1_section)
        with col2:
            st.subheader(f"{asset2} historical data")
            st.write(data2_section)

    st.sidebar.title("About")
    st.sidebar.info(
        "Check the code at https://github.com/KTS-o7/stockManager"
    )
    
    with col1:
        st.subheader(f"{asset1} Chart")
        st.area_chart(data1_section)
    
    with col2:
        st.subheader(f"{asset2} Chart")
        st.area_chart(data2_section)
        
    st.header("Notes of Analysis")
    notes = st.text_area("Enter your notes here, we will summarize it for you !")
    if st.button("Summarize"):
        with st.spinner("Summarizing your notes"):
            resp = summarize(notes)
            #st.write(resp)
            #print(type(resp))
            resp = {"user":session_state.username,"summary":resp}
            
            #print(type(resp))
            #st.write(resp)
            st.write("Summary is being saved to the database")
            with st.spinner("Saving to database"):
                db = mongoclient["stockmanager"]
                collection = db["analysisSummary"]
                inserted = collection.insert_one(resp)
                st.write("Acknowledgement",inserted.acknowledged,"Insertion ID ",inserted.inserted_id)
            
    
session_state = SessionState.get(is_authenticated=False, option=None, register=None,username=None,clientName=None,runBT=False)
main()
