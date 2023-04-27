import streamlit as st
from streamlit_option_menu import option_menu

import home
import text_summarizer
import recommendation
import update
import dashboard


def main():
    st.write()
    with st.sidebar:
        selected = option_menu(
            menu_title="Christograph",
            options=["Home", "Summarizero",
                     "Recommedatoro",  "Dashboard", "Your Account", "Contact Us"],
            icons=["house", "textarea-t", "journal-code",
                   "search", "person-square", "envelope-plus"],
            default_index=0,
        )

    if selected == "Home":
        home.home_ui()  
    if selected == "Summarizero":
        text_summarizer.call_text_summarizer()
    if selected == "Recommedatoro":
        recommendation.recommendation()
    if selected == "Dashboard":
        dashboard.recommend_page()
    if selected == "Your Account":
        update.update_details()
        update.update_research_details()
    if selected == "Contact Us":
        home.contact_page()
