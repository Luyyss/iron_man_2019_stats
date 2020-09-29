import numpy as np
import pandas as pd
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def iterDataAndConvert(data, arr):

    for row in data.itertuples():
        o = {}
        o['name'] = row.Name
        o['country'] = row.Country
        o['country_name'] = row.CountryName
        o['swim'] = row.Swim
        o['bike'] = row.Bike
        o['run'] = row.Run
        o['t1'] = row.T1
        o['t2'] = row.T2
        arr.append(o)

    return arr

def prep_df(df, name):
    df = df.stack().reset_index()
    df.columns = ['c1', 'c2', 'values']
    df['Classe'] = name
    return df

def write():

    data = funcs.get_data()

    data['CountryName'] = data['Country'].apply(funcs.getCountryName)

    categorias = funcs.getCategories(data)

    option = st.selectbox( "Selecione a categoria", sorted(categorias))

    atletas_m = data.loc[data['Division'] == f'M{option}']
    atletas_f = data.loc[data['Division'] == f'F{option}']

    atletas_m.drop(columns=['Division', 'Division Rank', 'Gender', 'Gender Rank'], axis=1, inplace=True)
    atletas_f.drop(columns=['Division', 'Division Rank','Gender', 'Gender Rank'], axis=1, inplace=True)

    udisp.title_awesome("Top 10 registros masculinos")
    atletas_m.reset_index(drop=True)
    st.dataframe(atletas_m.head(10))

    # arT = pd.DataFrame(iterDataAndConvert(atletas_m.head(10), []))

    udisp.title_awesome("Top 10 registros femininos")
    atletas_f.reset_index(drop=True)
    st.dataframe(atletas_f.head(10))

    atletas_m = atletas_m.head(10)

    atletas_m['SwimN'] = atletas_m['Swim'].apply(funcs.strToSeconds)
    atletas_m['BikeN'] = atletas_m['Bike'].apply(funcs.strToSeconds)
    atletas_m['RunN'] = atletas_m['Run'].apply(funcs.strToSeconds)
    atletas_m['T1N'] = atletas_m['T1'].apply(funcs.strToSeconds)
    atletas_m['T2N'] = atletas_m['T2'].apply(funcs.strToSeconds)

    df1=pd.DataFrame(atletas_m['SwimN'].tolist(), index=atletas_m['Name'], columns=["N"])
    df2=pd.DataFrame(atletas_m['T1N'].tolist(), index=atletas_m['Name'], columns=["N"])
    df3=pd.DataFrame(atletas_m['BikeN'].tolist(), index=atletas_m['Name'], columns=["N"])
    df4=pd.DataFrame(atletas_m['T2N'].tolist(), index=atletas_m['Name'], columns=["N"])
    df5=pd.DataFrame(atletas_m['RunN'].tolist(), index=atletas_m['Name'], columns=["N"])

    df1 = prep_df(df1, 'Swim')
    df2 = prep_df(df2, 'T1')
    df3 = prep_df(df3, 'Bike')
    df4 = prep_df(df4, 'Run')
    df5 = prep_df(df5, 'T2')

    df = pd.concat([df1, df2, df3, df4, df5])

    b = alt.Chart(df).mark_bar().encode(
        x=alt.Y('c1:N', title=None),
        y=alt.X('values:Q', axis=alt.Axis(grid=False, title=None)),
        column=alt.Column('c2:N', title=None),
        color=alt.Color('Classe:N', scale=alt.Scale(range=['#96ceb4', '#ffcc5c','#ff6f69']))
    ).configure_view(
        strokeOpacity=0
    )

    st.altair_chart(b)
