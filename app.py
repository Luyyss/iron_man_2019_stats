import pandas as pd
import streamlit as st
import utils.display as udisp
import resources.translate as translate

import src.pages.home
import src.pages.about
import src.pages.coutryes
import src.pages.dnsdnf
import src.pages.athlete
import src.pages.modality
import src.pages.compare_athletes
import src.pages.distribute
# import src.pages.medians
import src.pages.category


MENU = {
    "Top 10" : src.pages.home,
    "Estatísticas dos países" : src.pages.coutryes,
    "Estatísticas por modalidade" : src.pages.modality,
    "Estatísticas por categoria" : src.pages.category,
    "Estatísticas por atleta" : src.pages.athlete,
    "Comparar atletas" : src.pages.compare_athletes,
    "Estatísticas DNS, DNF e DQ" : src.pages.dnsdnf,
    "Distribuições" : src.pages.distribute,
    # "Médias por categoria" : src.pages.medians,
    "Sobre" : src.pages.about
}

LINGUAGENS = [
    'English',
    'Portugês'
]

linguagem_corrente = 0

def getLangText(ref):
    return translate.texts[linguagem_corrente][ref]

def main():
    # st.sidebar.title("Menu")
    menu_selection = st.sidebar.radio("Escolha entre as aplicações:", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Carregando {menu_selection} ..."):
        udisp.render_page(menu)

    # df = pd.DataFrame(LINGUAGENS)
    # option = st.sidebar.selectbox( getLangText('sel_lang'), df)

    # st.sidebar.info(
    #     "https://github.com/Luyyss/iron_man_2019_stats"
    # )

if __name__ == "__main__":
    main()