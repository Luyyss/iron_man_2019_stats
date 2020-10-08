import altair as alt
import streamlit as st
import utils.functions as funcs

def createPlot(data, col, color): 
    base = alt.Chart(data).encode(
        x=alt.X(f'{col}N:Q', bin=True, title='Tempo'),
        y=alt.Y('count()', title='Atletas'),
        # tooltip=[f'{col}:N'],
    )

    c = base.mark_bar()
    t = base.mark_text(dy=-6)

    b = alt.layer(c, t).properties(title=col)

    st.altair_chart((b).configure_mark(color=color))

def write():

    data = funcs.get_data()
    data = funcs.convertTimes(data)
    data = funcs.removeNotFinished(data)
    data['Country Name'] = data['Country'].apply(funcs.getCountryName)

    createPlot(data, 'Swim', 'green')

    createPlot(data, 'T1', 'red')

    createPlot(data, 'Bike', 'yellow')

    createPlot(data, 'T2', 'black')

    createPlot(data, 'Run', 'pink')