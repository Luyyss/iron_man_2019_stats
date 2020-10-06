import numpy as np
import pandas as pd
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def removeAddicionalColumns(df):
    df = df.drop(['SwimN'], axis=1)
    df = df.drop(['BikeN'], axis=1)
    df = df.drop(['RunN'], axis=1)
    df = df.drop(['T1N'], axis=1)
    df = df.drop(['T2N'], axis=1)
    return df

def write():

    data = funcs.get_data()
    data['Swim'].fillna(0.0, inplace=True)
    data['Bike'].fillna(0, inplace=True)
    data['Run'].fillna(0, inplace=True)
    data['T1'].fillna(0, inplace=True)
    data['T2'].fillna(0, inplace=True)

    data = funcs.removeNotFinished(data)
    data = funcs.convertTimes(data)
    data['Country Name'] = data['Country'].apply(funcs.getCountryName)

    udisp.title_awesome('Melhor natação')
    d = data[data.SwimN == data.SwimN.min()]
    st.table( removeAddicionalColumns( d ) )

    udisp.title_awesome('Melhor T1')
    d = data[data.T1N == data.T1N.min()]
    st.table( removeAddicionalColumns( d ) )

    udisp.title_awesome('Melhor bike')
    d = data[data.BikeN == data.BikeN.min()]
    st.table( removeAddicionalColumns( d ) )

    udisp.title_awesome('Melhor T2')
    d = data[data.T2N == data.T2N.min()]
    st.table( removeAddicionalColumns( d ) )

    udisp.title_awesome('Melhor corrida')
    d = data[data.RunN == data.RunN.min()]
    st.table( removeAddicionalColumns( d ) )