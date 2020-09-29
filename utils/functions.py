import pycountry
import numpy as np
import pandas as pd
import streamlit as st

# @st.cache
def get_data():
    data = pd.read_csv("results.csv")
    data.drop(columns=['BIB'], axis=1, inplace=True)
    return data

def getCategories(df):
    r = df['Division'].str[1:].unique()
    return r

def strToSeconds(val):
    if ':' in str(val):
        h, m, s = str(val).split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))
    else:
        return str(val)

list_alpha_2 = [i.alpha_2 for i in list(pycountry.countries)]
list_alpha_3 = [i.alpha_3 for i in list(pycountry.countries)]    

def getCountryName(val):
    if(type(val) == str):
        if (len(val)==2 and val in list_alpha_2):
            return pycountry.countries.get(alpha_2=val).name
        elif (len(val)==3 and val in list_alpha_3):
            return pycountry.countries.get(alpha_3=val).name
    else:
        return 'Invalid Code'