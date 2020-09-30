import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def getDataAndConvert(data):

    data['SwimN'] = data['Swim'].apply(funcs.strToSeconds)
    data['BikeN'] = data['Bike'].apply(funcs.strToSeconds)
    data['RunN'] = data['Run'].apply(funcs.strToSeconds)
    data['T1N'] = data['T1'].apply(funcs.strToSeconds)
    data['T2N'] = data['T2'].apply(funcs.strToSeconds)

    df1 = prep_df(data, 'Swim', 1)
    df2 = prep_df(data, 'T1', 2)
    df3 = prep_df(data, 'Bike', 3)
    df4 = prep_df(data, 'T2', 4)
    df5 = prep_df(data, 'Run', 5)

    return pd.concat([df1, df2, df3, df4, df5])

def prep_df(data, name, ord):
    df = pd.DataFrame( {'Name':data['Name'].tolist(), 'Tempo':data[name].tolist(), 'Segundos':data[name+'N'].tolist(), 'c2':'N'}, columns=['Name', 'Tempo', 'Segundos'] )
    df['Classe'] = name
    df['Order'] = ord
    return df

def createPlot(df):
    return alt.Chart( df ).mark_bar().encode(
        x=alt.X('Segundos:Q', axis=alt.Axis(title=None)), # , format=("%H:%M:%S")  , timeUnit='hoursminutesseconds' 
        y=alt.Y('Name:N', axis=alt.Axis(grid=False, title=None)),
        # column=alt.Column('c2:N', title=None),
        color=alt.Color('Classe:N', sort=['SwimN', 'T1N', 'BikeN', 'T2N', 'RunN'], scale=alt.Scale(range=['#96ceb4', '#BF820E','#4BA55E', '#4FA7A5', '#CBBE00'])),
        tooltip=['Tempo:N'],
        order=alt.Order(
            'Order',
            sort='descending'
        )
    ).configure_view(
        strokeOpacity=0
    ).properties(height=400, width=700)


def write():

    data = funcs.get_data()

    data['CountryName'] = data['Country'].apply(funcs.getCountryName)

    categorias = funcs.getCategories(data)

    option = st.selectbox( "Selecione a categoria", sorted(categorias))

    atletas_m = data.loc[data['Division'] == f'M{option}']
    atletas_f = data.loc[data['Division'] == f'F{option}']

    atletas_m.drop(columns=['Division', 'Division Rank', 'Gender', 'Gender Rank'], axis=1, inplace=True)
    atletas_f.drop(columns=['Division', 'Division Rank', 'Gender', 'Gender Rank'], axis=1, inplace=True)

    udisp.title_awesome("Top 10 registros masculinos")
    atletas_m.reset_index(drop=True)

    st.altair_chart( createPlot( getDataAndConvert(atletas_m.head(10)) ) )

    udisp.title_awesome("Top 10 registros femininos")
    atletas_f.reset_index(drop=True)

    st.altair_chart( createPlot( getDataAndConvert(atletas_f.head(10)) ) )