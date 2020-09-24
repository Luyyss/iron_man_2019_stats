import numpy as np
import pandas as pd
import streamlit as st

@st.cache
def get_data():
    data = pd.read_csv("results.csv")
    # data.
    data.drop(columns=['BIB'], axis=1, inplace=True)
    return data

def getCategories(df):
    r = df['Division'].str[1:].unique()
    # r = np.append(r, "PRO NEW", axis=0)
    return r

def strToSeconds(val):
    if ':' in str(val):
        h, m, s = val.split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))
    else:
        return str(val)