import streamlit as st
import uuid
from db_connection import db
import update

research_collection = db["research_details"]


def recommendation():
    user_name = st.session_state["user_name"]
    st.title("recommendation sytem")
    st.subheader("Enter research details to get recommendations!")
    # Insert data
    research_paper_name = st.text_input(
        "Enter Research paper name", key="research_paper_name")
    total_no_of_pages = st.text_input(
        "Enter total number of pages", key="total_no_of_pages")
    research_domain = st.text_input(
        "Enter Research domain", key="research_domain")
    areas_of_interest = st.text_input(
        "Enter areas of interest", key="areas_of_interest")
    input_list = areas_of_interest.split(",")
    if st.button("Save"):
        research_data = {
            "username": user_name,
            "research_paper_name": research_paper_name,
            "total_no_of_pages": total_no_of_pages,
            "research_domain": research_domain,
            "areas_of_interest": input_list
        }
        success = research_collection.insert_one(research_data)
        st.success("Data saved successfully!")
        st.subheader(
            "Go to Dashboard page to view your recommendations and other insights!")

        if success:
            st.subheader("Update your research details")
            update.update_research_details()
