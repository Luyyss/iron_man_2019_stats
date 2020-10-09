import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def write():

    data = funcs.get_data()

    ##
    ##   Tempo dos vencedores por categoria
    ##

    df = data[ data['Division Rank'].eq('1') ]

    df = pd.DataFrame({
        'Categoria':df['Division'].tolist(),
        'Tempo': df['Overall'].tolist()
    })

    st.table( df.reset_index().assign(hack='').set_index('hack').drop(['index'], axis=1) )
