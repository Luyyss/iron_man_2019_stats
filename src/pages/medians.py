import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.functions as funcs


data = funcs.get_data()
data = funcs.convertTimes(data)
data = funcs.removeNotFinished(data)
data['Country Name'] = data['Country'].apply(funcs.getCountryName)
data.astype({'BikeN': int})


def calculeMedianFromCat(cat, n):

    df = data[data['Division'] == cat].head( n )

    aux = {
        'Name': cat,
        'SwimN': int( df['SwimN'].median() ),
        'T1N': int( df['T1N'].median() ),
        'BikeN': int( df['BikeN'].median() ),
        'T2N': int( df['T2N'].median() ),
        'RunN': int( df['RunN'].median() ),
    }

    aux['Swim'] = funcs.secondsToTime( aux['SwimN'] )
    aux['T1'] = funcs.secondsToTime( aux['T1N'] )
    aux['Bike'] = funcs.secondsToTime( aux['BikeN'] )
    aux['T2'] = funcs.secondsToTime( aux['T2N'] )
    aux['Run'] = funcs.secondsToTime( aux['RunN'] )

    return aux

def write():

    q = st.sidebar.selectbox( "Quantidade de Atletas", [10, 20, 30, 50] )

    cats = data['Division'].unique()
    
    arr = []

    for c in cats:
        arr.append( calculeMedianFromCat(c, q) )

    df = pd.DataFrame(arr)

    # st.table(df)

    df1 = funcs.prep_df(df, 'Swim', 1)
    df2 = funcs.prep_df(df, 'T1', 2)
    df3 = funcs.prep_df(df, 'Bike', 3)
    df4 = funcs.prep_df(df, 'T2', 4)
    df5 = funcs.prep_df(df, 'Run', 5)

    df = pd.concat([df1, df2, df3, df4, df5])

    st.altair_chart(
        alt.Chart( df ).mark_bar().encode(
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
            height=500, width=850 
        )
    )