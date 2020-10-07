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

    udisp.title_awesome("Quantidade de Atletas por país")

    bars = alt.Chart(df).mark_bar().encode(
        alt.Y('Atletas', type='quantitative', title='Quantidade de Atletas'),
        alt.X('name:N', title='País'),
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


    # countries = alt.topo_feature('https://vega.github.io/vega-datasets/data/world-110m.json', 'countries')

    # b = alt.Chart(countries).mark_geoshape(
    #     fill='lightgray',
    #     stroke='white'
    # ).project(
    #     "equirectangular"
    # ).properties(
    #     width=900,
    #     height=500
    # )

    # st.altair_chart(b)

    ##
    ## 
    ##


    categorias = funcs.getCategories(data)

    option = st.sidebar.selectbox( "Selecione a categoria", sorted(categorias) )

    Atletas_m = data.loc[data['Division'] == f'M{option}']
    Atletas_f = data.loc[data['Division'] == f'F{option}']

    Atletas_m['Gender'] = 'Masculino'
    Atletas_f['Gender'] = 'Feminino'

    # st.dataframe(Atletas_m.head(10))

    q = st.sidebar.selectbox( "Quantidade de Atletas", [5,10, 15,20] )

    udisp.title_awesome(f'Top {q} atletas por país na categoria')

    division_sum_m = Atletas_m.head( int(q) ).groupby(['Country', 'Country Name', 'Gender']).agg({"Atletas": np.sum})
    # st.dataframe(division_sum_m)

    division_sum_f = Atletas_f.head( int(q) ).groupby(['Country', 'Country Name', 'Gender']).agg({"Atletas": np.sum})
    # st.dataframe(division_sum_f)

    topAtletas = pd.concat( [division_sum_f , division_sum_m] )
    # st.dataframe(topAtletas)

    source = pd.DataFrame({
        'abrev': topAtletas.index.get_level_values(0),
        'name': topAtletas.index.get_level_values(1),
        'Sexo': topAtletas.index.get_level_values(2),
        'Atletas': np.array(topAtletas['Atletas'].tolist())
    })

    # st.dataframe(source)

    c = alt.Chart(source).mark_bar().encode(
        x=alt.X('Sexo:N', axis=alt.Axis(title=None)),
        y=alt.Y('Atletas:Q', axis=alt.Axis(offset=1) ), #, scale=alt.Scale(round=True)
        color='Sexo:N',
        column=alt.Column('name:N', title='País', header=alt.Header(labelAngle=270, labelAlign='right')) 
    )

    st.altair_chart(c)

    # with Grid("1 1 1", color="#000000", background_color="#FFFFFF") as grid:

    #     grid.cell("a", 1, 2, 1, 2).markdown("**Masculino**")
    #     grid.cell("b", 2, 3, 1, 2).markdown("**Feminino**")

    #     grid.cell("c", 1, 2, 2, 3).dataframe(division_sum_m)
    #     grid.cell("d", 2, 3, 2, 3).dataframe(division_sum_f)

    ##
    ##  Países com mais Atletas entre os top 5
    ##

    udisp.title_awesome(f'Top {q} atletas por país em todas categorias')

    data = funcs.removeNotFinished(data)

    data = data.astype({"Division Rank": int})

    data = data[data['Division Rank'] <= q ] 

    countryes_sum = data.groupby(['Country', 'Country Name', 'Division']).agg({"Atletas": np.sum})

    # st.table( countryes_sum )

    source = pd.DataFrame({
        'abrev': countryes_sum.index.get_level_values(0),
        'name': countryes_sum.index.get_level_values(1),
        'Categoria': countryes_sum.index.get_level_values(2),
        'Atletas': np.array(countryes_sum['Atletas'].tolist())
    })

    # st.table(source)

    color_scale = alt.Scale(
        domain=np.array(countryes_sum.index.get_level_values(2)),
        range=["#c30d24", "#f3a583", "#cccccc", "#94c6da", "#1770ab"]
    )

    y_axis = alt.Axis(
        title=None, #'País',
        offset=1,
        ticks=False,
        minExtent=60,
        domain=False
    )

    c = alt.Chart( source ).mark_bar().encode(
        x='Atletas:Q',
        y=alt.Y('name:N', axis=y_axis),
        tooltip=['Atletas', 'Categoria'],
        color=alt.Color(
            'Categoria:N',
            legend=alt.Legend( title='Categoria'),
            scale=color_scale,
        )
    )

    st.altair_chart( (c).properties(width=900) )




    # exam_data  = {'name': ['Anastasia', 'Dima', 'Katherine', 'James', 'Emily', 'Michael', 'Matthew', 'Laura', 'Kevin', 'Jonas'],
    #     'score': [12.5, 9, 16.5, np.nan, 9, 20, 14.5, np.nan, 8, 19],
    #     'attempts': [1, 3, 2, 3, 2, 3, 1, 1, 2, 1],
    #     'qualify': ['yes', 'no', 'yes', 'no', 'no', 'yes', 'yes', 'no', 'no', 'yes']}

    # labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j']
    # df = pd.DataFrame(exam_data , index=labels)
    # st.write("Number of attempts in the examination is less than 2 and score greater than 15 :")
    # st.table(df[(df['attempts'] < 2) & (df['score'] > 15)])