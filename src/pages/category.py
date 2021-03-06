import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
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

def formatHour(t):
    h, m, s = str(t).split(':')

    if len(h) == 1:
        h = f'0{h}'

    return f'{h}:{m}:{s}'

def write():


     ##
    ##  Médias
    ##

    udisp.title_awesome('Médias por modalidade nas categorias')

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

    df['Time'] = df.apply(lambda x: f'2019-10-10T{formatHour(x["Tempo"])}Z', axis=1)

    # df['Time'] = pd.to_datetime(df['Time'])
    df = df.astype({'Time':'datetime64[ns]'})

    # st.table(df)

    st.altair_chart(
        alt.Chart( df ).mark_bar().encode(
            x=alt.X('Segundos:Q', axis=alt.Axis( title=None)), #hoursminutes( , format = ("%H:%M")
            # x=alt.X('hoursminutes(Time):O', axis=alt.Axis( title=None, format = ("%H:%M"))), #hoursminutes( , format = ("%H:%M")
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


    ##
    ##   Tempo dos vencedores por categoria
    ##

    udisp.title_awesome('Tempo dos vencedores por categoria')

    df = data[ data['Division Rank'].eq('1') ]

    df = pd.DataFrame({
        'Categoria':df['Division'].tolist(),
        'Tempo': df['Overall'].tolist()
    })

    st.table( df.reset_index().assign(hack='').set_index('hack').drop(['index'], axis=1) )

   