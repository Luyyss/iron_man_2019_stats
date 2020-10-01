import numpy as np
import pandas as pd
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def write():

    data = funcs.get_data()

    data['CountryName'] = data['Country'].apply(funcs.getCountryName)

    categorias = funcs.getCategories(data)

    option = st.selectbox( "Selecione a categoria", sorted(categorias))

    atletas_m = data.loc[data['Division'] == f'M{option}']
    atletas_f = data.loc[data['Division'] == f'F{option}']

    atletas_m.drop(columns=['Division', 'Division Rank', 'Gender', 'Gender Rank'], axis=1, inplace=True)
    atletas_f.drop(columns=['Division', 'Division Rank', 'Gender', 'Gender Rank'], axis=1, inplace=True)

    udisp.title_awesome("Top 10 registros masculinos")
    atletas_m.reset_index(drop=True)

    st.altair_chart( funcs.createStackPlot( funcs.getDataAndConvert(atletas_m.head(10)) ) )

    udisp.title_awesome("Top 10 registros femininos")
    atletas_f.reset_index(drop=True)

    st.altair_chart( funcs.createStackPlot( funcs.getDataAndConvert(atletas_f.head(10)) ) )