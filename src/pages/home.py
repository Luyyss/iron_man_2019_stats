import pandas as pd
import streamlit as st
import utils.display as udisp

@st.cache
def get_data():
    return pd.read_csv("results.csv")

def write():
    udisp.title_awesome("Top 10 registros")

    data = get_data()

    st.dataframe(data.head(10))