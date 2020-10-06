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

    dfF = df.loc[ df["Gender"] == "Female" ]
    dfM = df.loc[ df["Gender"] == "Male" ]

    st.write( f'Mulheres: {dfF.shape[0]}, Homens: {dfM.shape[0]}' )

    countryes_sum = df.groupby(['Division']).agg({"Atletas": np.sum})
    countryes_sum_values = np.array(countryes_sum['Atletas'].tolist())
    # countryes_abrev = countryes_sum.index.get_level_values(0)
    # countryes_names = countryes_sum.index.get_level_values(1)

    st.table(countryes_sum)


def write():

    data = funcs.get_data().drop(['Overall', 'Run', 'Bike', 'Swim', 'T1', 'T2', 'Division Rank', 'Gender Rank'], axis=1).sort_values(['Division'], ascending=[1])
    data['Atletas'] = 1

    data = data.assign(hack='').set_index('hack')

    prepareBlock(data, 'DQ')

    prepareBlock(data, 'DNS')

    prepareBlock(data, 'DNF')

    # df = data[data['Overall Rank'] == 'DNF']
    # udisp.title_awesome(f'Atletas DNF ({df.shape[0]})')

    # dfF = df.loc[ df["Gender"] == "Female" ]
    # dfM = df.loc[ df["Gender"] == "Male" ]

    # st.write( f'Mulheres: {dfF.shape[0]}, Homens: {dfM.shape[0]}' )

    # countryes_sum = df.groupby(['Division']).agg({"Atletas": np.sum})
    # countryes_sum_values = np.array(countryes_sum['Atletas'].tolist())
    # # countryes_abrev = countryes_sum.index.get_level_values(0)
    # # countryes_names = countryes_sum.index.get_level_values(1)

    # st.table(countryes_sum)

    # st.table(atleta.assign(hack='').set_index('hack'))


    # st.table(df.drop(['Overall Rank'], axis=1))


    # df = data[data['Overall Rank'] == 'DQ']
    # udisp.title_awesome(f'Atletas DQ ({df.shape[0]})')
    # st.table(df.drop(['Overall Rank'], axis=1)) #.reset_index(drop=True)

    # df = data[data['Overall Rank'] == 'DNS']
    # udisp.title_awesome(f'Atletas DNS ({df.shape[0]})')
    # st.table(df.drop(['Overall Rank'], axis=1))