import pandas as pd
import streamlit as st
import utils.display as udisp
import resources.translate as translate

import src.pages.home
import src.pages.about

MENU = {
    "Top 10" : src.pages.home,
    "Sobre" : src.pages.about
}

LINGUAGENS = [
    'English',
    'Portugês'
]

linguagem_corrente = 0


def getLinguagemCorrente():
    return linguagem_corrente

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