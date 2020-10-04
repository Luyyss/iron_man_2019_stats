import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def getValueUniq(df, field):
    return df[field].tolist()[0]

def write():

    data = funcs.get_data()
    data['Country Name'] = data['Country'].apply(funcs.getCountryName)

    # sentence = st.text_input('Input your sentence here:') 

    # if sentence:
    #     st.write(sentence)

    athletes = data['Name'].unique()

    option = st.selectbox('Buscar atleta pelo nome:', sorted(athletes) )

    atleta = data.loc[data['Name'] == option]

    # udisp.title_awesome("Resumo:")

    atleta = atleta.drop(['Country'], axis=1)

    st.table(atleta.assign(hack='').set_index('hack'))

    atleta = funcs.convertTimes( atleta )

    source = pd.DataFrame({
        'Atividade': ['Swim', 'T1', 'Bike', 'T2', 'Run'], 
        'TimeN': [getValueUniq(atleta, 'SwimN'), getValueUniq(atleta, 'T1N'), getValueUniq(atleta, 'BikeN'), getValueUniq(atleta, 'T2N'), getValueUniq(atleta, 'RunN')],
        'Tempo': [getValueUniq(atleta, 'Swim'), getValueUniq(atleta, 'T1'), getValueUniq(atleta, 'Bike'), getValueUniq(atleta, 'T2'), getValueUniq(atleta, 'Run')],
        'Ordem': [1, 2, 3, 4, 5]
    })

    if getValueUniq(atleta, 'Overall Rank') != 'DNF':

        st.altair_chart( 
            alt.Chart(source).transform_joinaggregate(
                TotalTime='sum(TimeN)',
            ).transform_calculate(
                PercentOfTotal="datum.TimeN / datum.TotalTime"
            ).mark_bar().encode(
                x=alt.X('PercentOfTotal:Q', axis=alt.Axis(format='.0%'), title='Porcentagem do total'),
                y=alt.Y('Atividade:N', sort=alt.EncodingSortField(field="Ordem",  order='ascending')),
                tooltip=['Tempo']
            )
            .properties(height=450, width=700)
        )

    # udisp.title_awesome("Detalhamento:")