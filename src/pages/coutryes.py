import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs
from src.classes.Grid import Grid

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
        alt.Y('Atletas', type='quantitative', title='Quantidade de atletas'),
        alt.X('name', type='nominal', title='País'),
        tooltip=['Atletas']
    ).properties(height=450) #, width=700

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

    udisp.title_awesome("Top atletas por país")

    categorias = funcs.getCategories(data)

    option = st.sidebar.selectbox( "Selecione a categoria", sorted(categorias) )

    atletas_m = data.loc[data['Division'] == f'M{option}']
    atletas_f = data.loc[data['Division'] == f'F{option}']

    # st.dataframe(atletas_m.head(10))

    q = st.sidebar.selectbox( "Quantidade de atletas", [5,10, 15,20] )

    division_sum_m = atletas_m.head( int(q) ).groupby(['Country', 'Country Name']).agg({"Atletas": np.sum})
    # st.dataframe(division_sum_m)

    division_sum_f = atletas_f.head( int(q) ).groupby(['Country', 'Country Name']).agg({"Atletas": np.sum})
    # st.dataframe(division_sum_f)
    

    with Grid("1 1 1", color="#000000", background_color="#FFFFFF") as grid:
        # grid.cell(
        #     class_="a",
        #     grid_column_start=2,
        #     grid_column_end=3,
        #     grid_row_start=1,
        #     grid_row_end=2,
        # ).text("The cell to the left is a dataframe")

        grid.cell("a", 1, 2, 1, 2).markdown("**Masculino**")
        grid.cell("b", 2, 3, 1, 2).markdown("**Feminino**")

        grid.cell("c", 1, 2, 2, 3).dataframe(division_sum_m)
        grid.cell("d", 2, 3, 2, 3).dataframe(division_sum_f)

        # grid.cell("c", 3, 4, 2, 3).plotly_chart(get_plotly_fig())
        # grid.cell("d", 1, 2, 1, 3).dataframe(get_dataframe())
        # grid.cell("e", 3, 4, 1, 2).markdown(
        #     "Try changing the **block container style** in the sidebar!"
        # )
        # grid.cell("f", 1, 3, 3, 4).text(
        #     "The cell to the right is a matplotlib svg image"
        # )
        # grid.cell("g", 3, 4, 3, 4).pyplot(get_matplotlib_plt())
