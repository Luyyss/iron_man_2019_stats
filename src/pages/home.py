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

    
    # df = pd.DataFrame({
    #     'label': ['A', 'B', 'C', 'D', 'E', 'F', 'G'],
    #     'value1': [1, 3, 2, 4, 5, 6, 4],
    #     'value2': [2, 1, 2, 5, 3, 4, 2],
    # })

    # alt.Chart(df).transform_fold(
        # ['value1', 'value2'],
        # as_=['column', 'value']
    # ).mark_bar().encode(
        # x='label:N',
        # y='value:Q',
        # color='column:N'
    # )

    # df = pd.DataFrame({
    #     'label': atletas_m['Name'],
    #     'swim': atletas_m['Swim'],
    #     'T1': atletas_m['T1'],
    #     'bike': atletas_m['Bike'],
    #     'T2': atletas_m['T2'],
    #     'run': atletas_m['Run']
    # })

    # st.dataframe(df)

    # b = alt.Chart(df).transform_fold(
    #     ['swim', 'T1', 'bike', 'T2', 'run'],
    #     as_=['column', 'value']
    # ).mark_bar().encode(
    #     x='label:N',
    #     y='value:Q',
    #     color='column:N'
    # )

    # st.altair_chart(b)




    ##
    ##  Bar Charts
    ##
    ## {"yield": 33.06666, "variety": "No. 475", "year": 1931, "site": "Duluth"},

    # bars = alt.Chart(arT).mark_bar().encode(
    #     x=alt.X('bike:Q', stack='zero'),
    #     y=alt.Y('name:N'),
    #     color=alt.Color('bike')
    # )

    # text = alt.Chart(arT).mark_text(dx=-15, dy=3, color='white').encode(
    #     x=alt.X('bike:Q', stack='zero'),
    #     y=alt.Y('name:N'),
    #     detail='site:N',
    #     text=alt.Text('sum(yield):Q', format='.1f')
    # )

    # st.altair_chart(bars)


    # df1=pd.DataFrame(10*np.random.rand(6,1),index=["A","B","C","D", "E", "F"],columns=["N"])
    # df2=pd.DataFrame(10*np.random.rand(6,1),index=["A","B","C","D", "E", "F"],columns=["N"])
    # df3=pd.DataFrame(10*np.random.rand(6,1),index=["A","B","C","D", "E", "F"],columns=["N"])

    # df1 = prep_df(df1, 'DF1')
    # df2 = prep_df(df2, 'DF2')
    # df3 = prep_df(df3, 'DF3')

    # df = pd.concat([df1, df2, df3])

    # st.dataframe(df)

    # b = alt.Chart(df).mark_bar().encode(
    #     x=alt.X('c2:N', title=None),
    #     y=alt.Y('sum(values):Q', axis=alt.Axis(grid=False, title=None)),
    #     column=alt.Column('c1:N', title=None),
    #     color=alt.Color('DF:N', scale=alt.Scale(range=['#96ceb4', '#ffcc5c','#ff6f69']))
    # ).configure_view(
    #     strokeOpacity=0    
    # )

    # st.altair_chart(b)


    atletas_m = atletas_m.head(10)

    atletas_m['SwimN'] = atletas_m['Swim'].apply(funcs.strToSeconds)
    atletas_m['BikeN'] = atletas_m['Bike'].apply(funcs.strToSeconds)
    atletas_m['RunN'] = atletas_m['Run'].apply(funcs.strToSeconds)
    atletas_m['T1N'] = atletas_m['T1'].apply(funcs.strToSeconds)
    atletas_m['T2N'] = atletas_m['T2'].apply(funcs.strToSeconds)

    # st.dataframe(atletas_m)

    df1=pd.DataFrame(atletas_m['SwimN'].tolist(), index=atletas_m['Name'], columns=["N"])
    df2=pd.DataFrame(atletas_m['T1N'].tolist(), index=atletas_m['Name'], columns=["N"])
    df3=pd.DataFrame(atletas_m['BikeN'].tolist(), index=atletas_m['Name'], columns=["N"])
    df4=pd.DataFrame(atletas_m['T2N'].tolist(), index=atletas_m['Name'], columns=["N"])
    df5=pd.DataFrame(atletas_m['RunN'].tolist(), index=atletas_m['Name'], columns=["N"])

    # st.dataframe(df1)
    # st.dataframe(df2)
    # st.dataframe(df3)

    df1 = prep_df(df1, 'Swim')
    df2 = prep_df(df2, 'T1')
    df3 = prep_df(df3, 'Bike')
    df4 = prep_df(df4, 'Run')
    df5 = prep_df(df5, 'T2')

    df = pd.concat([df1, df2, df3, df4, df5])

    b = alt.Chart(df).mark_bar().encode(
        x=alt.X('c1:N', title=None),
        y=alt.Y('sum(values):Q', axis=alt.Axis(grid=False, title=None)),
        column=alt.Column('c2:N', title=None),
        color=alt.Color('Classe:N', scale=alt.Scale(range=['#96ceb4', '#ffcc5c','#ff6f69']))
    ).configure_view(
        strokeOpacity=0    
    )

    st.altair_chart(b)
