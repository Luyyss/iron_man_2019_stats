import numpy
import pandas as pd
import numpy as np
import altair as alt
import streamlit as st
import utils.display as udisp
import utils.functions as funcs

def prepareBlock(data, t):

    df = data[data['Overall Rank'] == t]
    udisp.title_awesome(f'Atletas {t} ({df.shape[0]})')

    # dfF = df.loc[ df["Gender"] == "Female" ]
    # dfM = df.loc[ df["Gender"] == "Male" ]
    # st.write( f'Mulheres: {dfF.shape[0]}, Homens: {dfM.shape[0]}' )

    countryes_sum = df.groupby(['Division']).agg({"Atletas": np.sum})
    countryes_sum_values = np.array(countryes_sum['Atletas'].tolist())

    division_names = countryes_sum.index.get_level_values(0)

    df = pd.DataFrame({
        'Categoria': division_names,
        'Atletas': countryes_sum_values
    })

    bars = alt.Chart(df).mark_bar().encode(
        alt.Y('Atletas', type='quantitative', title='Quantidade de Atletas'),
        alt.X('Categoria:N', title=None),
        tooltip=['Atletas', 'Categoria']
    )

    st.altair_chart((bars).properties(width=800))

def write():

    data = funcs.get_data()
    data = funcs.convertTimes( data )

    ##
    ##  Tabela
    ##

    total = data.shape[0]

    df = pd.DataFrame({
        'Athletes': [total],
        # 'Swim Finish': [  showPorcent( 100 * ( (total - data[data['Swim'].isnull()].shape[0] ) / total) ) ],
        'Swim Finish': [  (total - data[data['Swim'].isnull()].shape[0] ) ],
        'Swim DNS/DNF': [ funcs.showPercent( 100 * ( data['Swim'].isnull() & ( data['Overall Rank'].eq('DNS') | data['Overall Rank'].eq('DNF') ) ).mean() ) ],
        # 'Bike Finish': [ showPorcent( 100 * ( (total - data[data['Bike'].isnull()].shape[0] ) / total) ) ],
        'Bike Finish': [ (total - data[data['Bike'].isnull()].shape[0]) ],
        'Bike DNF': [ showPorcent( 100 * ( data['Bike'].isnull() & ( data['Overall Rank'].eq('DNS') | data['Overall Rank'].eq('DNF') ) ).mean() ) ],
        # 'Run Finish': [ showPorcent( 100 * ( (total - data[data['Run'].isnull()].shape[0] ) / total) ) ],
        'Run Finish': [ (total - data[data['Run'].isnull()].shape[0] ) ],
        'Run DNF': [ showPorcent( 100 * ( data['Run'].isnull() & data['Overall Rank'].eq('DNF') ).mean() ) ],
        'Overall DNS/DNF': [ showPorcent( 100 * ( data['Overall Rank'].eq('DNS') | data['Overall Rank'].eq('DNF') ).mean() ) ],
    })

    df = df.assign(hack='').set_index('hack')

    st.table(df)

    ##
    ##  Gráficos
    ##

    data = data.drop(['Overall', 'Run', 'Bike', 'Swim', 'T1', 'T2', 'Division Rank', 'Gender Rank'], axis=1).sort_values(['Division'], ascending=[1])
    data['Atletas'] = 1

    prepareBlock(data, 'DQ')

    prepareBlock(data, 'DNS')

    prepareBlock(data, 'DNF')