import numpy
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def write():

    data = funcs.get_data()

    ##
    ##   FIRST STEP, NUMBER OF ATHLETES FROM COUNTRY
    ##

    data['Country Name'] = data['Country'].apply(funcs.getCountryName)
    data['Atletas'] = 1

    countryes_sum = data.groupby(['Country', 'Country Name']).agg({"Atletas": np.sum})
    countryes_sum_values = np.array(countryes_sum['Atletas'].tolist())
    countryes_abrev = countryes_sum.index.get_level_values(0)
    countryes_names = countryes_sum.index.get_level_values(1)

    df = pd.DataFrame({
        'abrev': countryes_abrev,
        'name': countryes_names,
        'Atletas': countryes_sum_values
    })

    udisp.title_awesome("Quantidade de atletas por país")

    bars = alt.Chart(df).mark_bar().encode(
        alt.X('Atletas', type='quantitative', title='Quantidade de atletas'),
        alt.Y('name', type='nominal', title='País'),
        tooltip=['Atletas']
    ).properties(height=900, width=700)

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=2  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='abrev'
    )

    (bars + text).properties(widht=600)

    st.altair_chart(bars)


    ##
    ## 
    ##

    categorias = funcs.getCategories(data)

    option = st.selectbox( "Selecione a categoria", sorted(categorias) )

    atletas_m = data.loc[data['Division'] == f'M{option}']
    atletas_f = data.loc[data['Division'] == f'F{option}']

    st.dataframe(atletas_m.head(10))


    q = st.selectbox( "Quantidade de atletas", [5,10, 15,20] )

    division_sum = atletas_m.head( int(q) ).groupby(['Country', 'Country Name']).agg({"Atletas": np.sum})
    st.dataframe(division_sum)