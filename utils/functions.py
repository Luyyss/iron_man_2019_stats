import pycountry
import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import datetime

# @st.cache
def get_data():
    data = pd.read_csv("results.csv")
    data.drop(columns=['BIB'], axis=1, inplace=True)
    return data


def _set_style():
    
    padding_top = 0
    padding_right = 1
    padding_left = 1
    padding_bottom = 10
    max_width_str = f"max-width: 100%;"

    st.markdown(
        f"""
            <style>
                .reportview-container .main .block-container{{
                    {max_width_str}
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
            </style>
            """,
        unsafe_allow_html=True,
    )


def getCategories(df):
    r = df['Division'].str[1:].unique()
    return r

def strToSeconds(val):
    if ':' in str(val):
        h, m, s = str(val).split(':')
        return int(int(h) * 3600 + int(m) * 60 + int(s))
    else:
        return str(val)

def secondsToTime(s):
    return str(datetime.timedelta(seconds=s))


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

def convertTimes(data):

    data = data.assign(SwimN=( data.apply(lambda row: strToSeconds(row.Swim), axis=1) ).values )
    data = data.assign(BikeN=( data.apply(lambda row: strToSeconds(row.Bike), axis=1) ).values )
    data = data.assign(RunN=( data.apply(lambda row: strToSeconds(row.Run), axis=1) ).values )
    data = data.assign(T1N=( data.apply(lambda row: strToSeconds(row.T1), axis=1) ).values )
    data = data.assign(T2N=( data.apply(lambda row: strToSeconds(row.T2), axis=1) ).values )

    return data

def getDataAndConvert(data):

    data = convertTimes(data)

    df1 = prep_df(data, 'Swim', 1)
    df2 = prep_df(data, 'T1', 2)
    df3 = prep_df(data, 'Bike', 3)
    df4 = prep_df(data, 'T2', 4)
    df5 = prep_df(data, 'Run', 5)

    return pd.concat([df1, df2, df3, df4, df5])

def prep_df(data, name, ord):
    df = pd.DataFrame( {'Name':data['Name'].tolist(), 'Tempo':data[name].tolist(), 'Segundos':data[name+'N'].tolist(), 'c2':'N'}, columns=['Name', 'Tempo', 'Segundos'] ) #'Total':data['Overall'].tolist(), 
    df['Classe'] = name
    df['Order'] = ord
    return df

def createStackPlot(df):
    return alt.Chart( df ).mark_bar().encode(
        x=alt.X('Segundos:Q', axis=alt.Axis( title=None)), #hoursminutes(
        y=alt.Y('Name:N', axis=alt.Axis(grid=False, title=None), sort=alt.EncodingSortField(field="Segundos", op="sum", order='ascending')),
        color=alt.Color('Classe:N', sort=['SwimN', 'T1N', 'BikeN', 'T2N', 'RunN'], scale=alt.Scale(scheme='tableau20') ), #scale=alt.Scale(range=['#96ceb4', '#BF820E','#4BA55E', '#4FA7A5', '#CBBE00'])
        tooltip=['Tempo:N'],
        order=alt.Order(
            'Order',
            sort='ascending'
        )
    ).configure_view(
        strokeOpacity=0
    ).properties( 
        height=400, width=900 
    )


def getValueUniq(df, field):
    return df[field].tolist()[0]


def removeNotFinished(data):

    data = data.drop(data[data['Overall Rank'] == 'DNF'].index)
    data = data.drop(data[data['Overall Rank'] == 'DNS'].index)
    data = data.drop(data[data['Overall Rank'] == 'DQ'].index)

    return data

def fillNa(df):
    for i in df.columns:
        if(type(df[i]) == int):
            df.fillna(df[i].mean(),inplace=True)
    return df