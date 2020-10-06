import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs
from src.classes.Grid import Grid

def write():

    data = funcs.get_data()
    data = funcs.convertTimes(data)
    data['Country Name'] = data['Country'].apply(funcs.getCountryName)

    data = funcs.removeNotFinished(data)

    ##
    ##  Gráfico
    ##

    athletes = data['Name'].unique()

    option1 = st.sidebar.selectbox('Buscar atleta pelo nome:', sorted(athletes) )
    atleta1 = data.loc[data['Name'] == option1].drop(['Country'], axis=1)

    option2 = st.sidebar.selectbox('Segundo atleta:', sorted(athletes) )
    atleta2 = data.loc[data['Name'] == option2].drop(['Country'], axis=1)

    df = pd.DataFrame([
        {'val':'1', 'Order':1, 'name': funcs.getValueUniq(atleta1, 'Name'), 'Tempo': funcs.getValueUniq(atleta1, 'Swim'), 'TempoN': funcs.getValueUniq(atleta1, 'SwimN'), 'Atividade':'Swim'},
        {'val':'2', 'Order':1, 'name': funcs.getValueUniq(atleta2, 'Name'), 'Tempo': funcs.getValueUniq(atleta2, 'Swim'), 'TempoN': funcs.getValueUniq(atleta2, 'SwimN'), 'Atividade':'Swim'},
        {'val':'1', 'Order':2, 'name': funcs.getValueUniq(atleta1, 'Name'), 'Tempo': funcs.getValueUniq(atleta1, 'T1'), 'TempoN': funcs.getValueUniq(atleta1, 'T1N'), 'Atividade':'T1'},
        {'val':'2', 'Order':2, 'name': funcs.getValueUniq(atleta2, 'Name'), 'Tempo': funcs.getValueUniq(atleta2, 'T1'), 'TempoN': funcs.getValueUniq(atleta2, 'T1N'), 'Atividade':'T1'},
        {'val':'1', 'Order':3, 'name': funcs.getValueUniq(atleta1, 'Name'), 'Tempo': funcs.getValueUniq(atleta1, 'Bike'), 'TempoN': funcs.getValueUniq(atleta1, 'BikeN'), 'Atividade':'Bike'},
        {'val':'2', 'Order':3, 'name': funcs.getValueUniq(atleta2, 'Name'), 'Tempo': funcs.getValueUniq(atleta2, 'Bike'), 'TempoN': funcs.getValueUniq(atleta2, 'BikeN'), 'Atividade':'Bike'},
        {'val':'1', 'Order':4, 'name': funcs.getValueUniq(atleta1, 'Name'), 'Tempo': funcs.getValueUniq(atleta1, 'T2'), 'TempoN': funcs.getValueUniq(atleta1, 'T2N'), 'Atividade':'T2'},
        {'val':'2', 'Order':4, 'name': funcs.getValueUniq(atleta2, 'Name'), 'Tempo': funcs.getValueUniq(atleta2, 'T2'), 'TempoN': funcs.getValueUniq(atleta2, 'T2N'), 'Atividade':'T2'},
        {'val':'1', 'Order':5, 'name': funcs.getValueUniq(atleta1, 'Name'), 'Tempo': funcs.getValueUniq(atleta1, 'Run'), 'TempoN': funcs.getValueUniq(atleta1, 'RunN'), 'Atividade':'Run'},
        {'val':'2', 'Order':5, 'name': funcs.getValueUniq(atleta2, 'Name'), 'Tempo': funcs.getValueUniq(atleta2, 'Run'), 'TempoN': funcs.getValueUniq(atleta2, 'RunN'), 'Atividade':'Run'}
    ])

    base = alt.Chart(df).properties( width=400 )

    color_scale = alt.Scale(domain=[option1, option2], range=['#1f77b4', '#1f77b4'])


    left = base.transform_filter(
        alt.datum.val == '1'
    ).encode(
        y=alt.Y('Atividade:N', axis=None, sort=alt.EncodingSortField(field="Order", order='ascending')),
        x=alt.X('sum(TempoN):Q', title='Tempo', sort=alt.SortOrder('descending')),
        color=alt.Color('name:N', scale=color_scale, legend=None),
        tooltip=['Tempo:N'],
        order=alt.Order(
            'Order',
            sort='ascending'
        )
    ).mark_bar().properties(title=option1)


    middle = base.encode(
        y=alt.Y('Atividade:N', axis=None, sort=alt.EncodingSortField(field="Order", order='ascending')),
        text=alt.Text('Atividade:N'),
        order=alt.Order(
            'Order',
            sort='ascending'
        )
    ).mark_text().properties(width=40)

    right = base.transform_filter(
        alt.datum.val == '2'
    ).encode(
        y=alt.Y('Atividade:N', axis=None, sort=alt.EncodingSortField(field="Order", order='ascending')),
        x=alt.X('sum(TempoN):Q', title='Tempo'),
        color=alt.Color('name:N', scale=color_scale, legend=None),
        tooltip=['Tempo:N']
    ).mark_bar().properties(title=option2)

    st.altair_chart( alt.concat(left, middle, right, spacing=5) )

    ##
    ##  Tabela
    ##

    df1 = pd.DataFrame([
        {'Atividade':'Swim', 'Tempo': funcs.getValueUniq(atleta1, 'Swim')},
        {'Atividade':'T1', 'Tempo': funcs.getValueUniq(atleta1, 'T1')},
        {'Atividade':'Bike', 'Tempo': funcs.getValueUniq(atleta1, 'Bike')},
        {'Atividade':'T2', 'Tempo': funcs.getValueUniq(atleta1, 'T2')},
        {'Atividade':'Run', 'Tempo': funcs.getValueUniq(atleta1, 'Run')},
        {'Atividade':'Total', 'Tempo': funcs.getValueUniq(atleta1, 'Overall')}
    ])

    df2 = pd.DataFrame([
        {'Atividade':'Swim', 'Tempo': funcs.getValueUniq(atleta2, 'Swim')},
        {'Atividade':'T1', 'Tempo': funcs.getValueUniq(atleta2, 'T1')},
        {'Atividade':'Bike', 'Tempo': funcs.getValueUniq(atleta2, 'Bike')},
        {'Atividade':'T2', 'Tempo': funcs.getValueUniq(atleta2, 'T2')},
        {'Atividade':'Run', 'Tempo': funcs.getValueUniq(atleta2, 'Run')},
        {'Atividade':'Total', 'Tempo': funcs.getValueUniq(atleta2, 'Overall')}
    ])

    with Grid("1 1", color="#000000", background_color="#FFFFFF") as grid:
        grid.cell("a", 1, 2, 1, 2).dataframe( df1.set_index('Atividade', inplace=False) )
        grid.cell("b", 2, 3, 1, 2).dataframe( df2.set_index('Atividade', inplace=False) )


    # st.write(funcs.secondsToTime( funcs.getValueUniq(atleta2, 'RunN') ))