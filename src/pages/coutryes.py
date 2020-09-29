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
    data['Athetes'] = 1

    countryes_sum = data.groupby(['Country', 'Country Name']).agg({"Athetes": np.sum})
    countryes_sum_values = np.array(countryes_sum['Athetes'].tolist())
    countryes_abrev = countryes_sum.index.get_level_values(0)
    countryes_names = countryes_sum.index.get_level_values(1)

    df = pd.DataFrame({
        'abrev': countryes_abrev,
        'name': countryes_names,
        'Atletas': countryes_sum_values
    })

    udisp.title_awesome("Quantidade de atletas por país")

    bars = alt.Chart(df).mark_bar().encode(
        alt.Y('Atletas', type='quantitative', title='Quantidade de atletas'),
        alt.X('name', type='nominal', title='País'),
        tooltip=['Atletas']
    ).properties(height=500)

    text = bars.mark_text(
        align='left',
        baseline='middle',
        dx=1  # Nudges text to right so it doesn't appear on top of the bar
    ).encode(
        text='abrev'
    )

    (bars + text).properties(widht=500)

    st.altair_chart(bars) #, use_container_width=True


    ##
    ## {"yield": 55.2, "variety": "Glabron", "year": 1931, "site": "Waseca"},
    ##