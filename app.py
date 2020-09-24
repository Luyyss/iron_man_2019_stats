import streamlit as st
import utils.display as udisp

import src.pages.home
import src.pages.about

MENU = {
    "Home" : src.pages.home,
    "Sobre" : src.pages.about
}

def main():
    st.sidebar.title("Menu")
    menu_selection = st.sidebar.radio("Escolha entre as aplicações:", list(MENU.keys()))

    menu = MENU[menu_selection]

    with st.spinner(f"Carregando {menu_selection} ..."):
        udisp.render_page(menu)

    # st.sidebar.info(
    #     "https://github.com/Luyyss/iron_man_2019_stats"
    # )

if __name__ == "__main__":
    main()