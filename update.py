from db_connection import db
import streamlit as st

users_collection = db["researcher_details"]
research_collection = db["research_details"]
# class ReseacherPaper(BaseModel):
#     researcher_id: str
#     researcher_paper_id: str
#     research_paper_name: str
#     total_no_of_pages: int
#     research_domain: str
#     areas_of_interest: list

# Insert data
# st.write("Insert Data")
# name = st.text_input("Update your full name")
# email = st.text_input("Update your Email")
# if st.button("Save"):
#     data = {"name": name, "email": email}
#     users_collection.insert_one(data)
#     st.success("Data saved successfully!")

# Update data


def update_details():
    st.divider()
    st.subheader("Update General Details")
    user_name = st.session_state["user_name"]
    result = users_collection.find()
    name_list = [data["username"] for data in result]
    if user_name in name_list:
        new_email = st.text_input("Update email")
        if new_email == "":
            st.warning("enter valid email id")
        else:
            if st.button("Update email"):
                query = {"username": user_name}
                email_update = {"$set": {"email": new_email}}
                users_collection.update_one(query, email_update)
                st.success("email updated successfully!")

        institution = st.text_input("Update your institution")
        if institution == "":
            st.warning("should not be empty")
        else:
            if st.button("Update institution"):
                query = {"username": user_name}
                institution_update = {"$set": {"institution": institution}}
                users_collection.update_one(query, institution_update)
                st.success("institution updated successfully!")

        published_papers = st.text_input("Update your published papers")
        if published_papers == "":
            st.warning("enter valid number of published papers")
        else:
            if st.button("Update published papers"):
                query = {"username": user_name}
                published_papers_update = {
                    "$set": {"published_papers": published_papers}}
                users_collection.update_one(query, published_papers_update)
                st.success("published papers updated successfully!")


def update_research_details():
    st.divider()
    st.subheader("Update Research Details")
    user_name = st.session_state["user_name"]
    result = research_collection.find()
    name_list = [data["username"] for data in result]
    if user_name in name_list:
        research_paper_name = st.text_input("Update Research paper name")
        if research_paper_name == "":
            st.warning("Update valid research paper name")
        else:
            if st.button("Update research papername"):
                query = {"username": user_name}
                research_paper_name_update = {
                    "$set": {"research_paper_name": research_paper_name}}
                research_collection.update_one(
                    query,  research_paper_name_update)
                st.success("research paper name updated successfully!")

        total_no_of_pages = st.text_input("Update total number of pages")
        if total_no_of_pages == "":
            st.warning("Update valid total number of pages")
        else:
            if st.button("Update total number of pages"):
                query = {"username": user_name}
                total_no_of_pages_update = {
                    "$set": {"total_no_of_pages": total_no_of_pages}}
                research_collection.update_one(query, total_no_of_pages_update)
                st.success("total number of pages updated successfully!")

        research_domain = st.text_input("Update Research domain")
        if research_domain == "":
            st.warning("enter valid research domain")
        else:
            if st.button("Update research domain"):
                query = {"username": user_name}
                research_domain_update = {
                    "$set": {"research_domain": research_domain}}
                research_collection.update_one(query, research_domain_update)
                st.success("research domain updated successfully!")

        areas_of_interest = st.text_input("Update areas of interest")
        input_list = areas_of_interest.split(",")
        if areas_of_interest == "":
            st.warning("enter valid areas of interest separated by comma")
        else:
            if st.button("Update areas of interest"):
                query = {"username": user_name}
                areas_of_interest_update = {
                    "$set": {"areas_of_interest": input_list}}
                research_collection.update_one(query, areas_of_interest_update)
                st.success("areas of interest updated successfully!")
