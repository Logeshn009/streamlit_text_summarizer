import streamlit as st
from streamlit_option_menu import option_menu
import user_login
import home
import text_summarizer

# def run_login():
#     user_login.login_ui()


# def run_register():
#     user_login.register_ui()


# home.home_ui()


def main():
    with st.sidebar:
        selected = option_menu(
            menu_title="Christograph",
            options=["Home", "Summarizero", "Recommedatoro", "Contact"]
        )

    if selected == "Home":
        home.home_ui()
    if selected == "Summarizero":
        text_summarizer.call_text_summarizer()


if __name__ == "__main__":
    main()
