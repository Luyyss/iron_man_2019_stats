import numpy
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def write():

    data = funcs.get_data().drop(['Overall', 'Run', 'Bike', 'Swim', 'T1', 'T2', 'Division Rank', 'Gender Rank'], axis=1).sort_values(['Division'], ascending=[1])

    data = data.assign(hack='').set_index('hack')
    
    df = data[data['Overall Rank'] == 'DNF']
    udisp.title_awesome("Atletas DNF")
    st.table(df.drop(['Overall Rank'], axis=1))

    df = data[data['Overall Rank'] == 'DQ']
    udisp.title_awesome("Atletas DQ")
    st.table(df.drop(['Overall Rank'], axis=1)) #.reset_index(drop=True)

    df = data[data['Overall Rank'] == 'DNS']
    udisp.title_awesome("Atletas DNS")
    st.table(df.drop(['Overall Rank'], axis=1))