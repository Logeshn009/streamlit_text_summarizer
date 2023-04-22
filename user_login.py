from fastapi import FastAPI, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from db_connection import db
from pydantic import BaseModel
import streamlit as st
import requests
import uuid
import time


# mongo collection
users_collection = db['researcher_details']

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__default_rounds=12)

# Set up FastAPI
christograph = FastAPI()

# Define user model


class User(BaseModel):
    researcher_name: str
    institution: str
    published_papers: int
    # areas_of_interest: list
    email: str
    username: str
    password: str


class ReseacherPaper(BaseModel):
    researcher_id: str
    researcher_paper_id: str
    research_paper_name: str
    total_no_of_pages: int
    research_domain: str
    areas_of_interest: list

# Get custom areas of interest from the user


def get_areas():

    # Define a list of pre-defined areas of interest
    predefined_areas_of_interest = ["Python", "Data Science", "Machine Learning", "Neural networks"
                                    "Web Development", "Deep Learning", "Networking", "Cloud computing"]

    areas_of_interest = st.multiselect(
        "Select your areas of interest", predefined_areas_of_interest)
    custom_areas_of_interest = st.text_input(
        "Enter your own areas of interest, separated by commas", key="areas_of_interest")
    # print(areas_of_interest, custom_areas_of_interest)
    if custom_areas_of_interest:

        # custom areas of interest
        total_interest = [area.strip()
                          for area in custom_areas_of_interest.split(",")]
        return total_interest

    if areas_of_interest:

        # pre-defined areas of interest
        total_interest = areas_of_interest
        return total_interest

    if custom_areas_of_interest and areas_of_interest:
        interest_2 = areas_of_interest
        interest_1 = [area.strip()
                      for area in custom_areas_of_interest.split(",")]
        total_interest = interest_1 + interest_2
        return total_interest


@christograph.post('/christograph/register')
def register_user(user: User):

    find_user = users_collection.find_one({'username': user.username})
    # Check if the username is already taken
    if find_user:
        raise HTTPException(status_code=400, detail="Username already taken")

    # Hash the password with salt
    password_hash = pwd_context.hash(user.password)

   # Generate a UUID version 4
    researcher_id = uuid.uuid4()
    researcher_id_str = str(researcher_id)

    # Save the user to the database
    user_data = {
        "full_name": user.researcher_name,
        "researcher_id": researcher_id_str,
        "institution": user.institution,
        "published_papers": user.published_papers,
        "email": user.email,
        "username": user.username,
        "password": password_hash,
    }
    users_collection.insert_one(user_data)
    return {'message': 'User registered successfully'}


# Set up HTTP basic authentication
security = HTTPBasic()


@christograph.post("/christograph/login")
async def login(credentials: HTTPBasicCredentials):
    # Find the user by username
    user_login = users_collection.find_one({"username": credentials.username})
    if not user_login:
        raise HTTPException(status_code=401, detail="Invalid username")
    # Verify the password hash
    if not pwd_context.verify(credentials.password, user_login["password"]):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")
    return {"message": "Login successful"}


# Streamlit UI
def register_ui():

    full_name = st.text_input("Enter your full name", key="full_name")
    institution = st.text_input(
        "Enter your institution name", key="institution_name")
    published_papers = st.text_input(
        "Enter the total number of research papers published", key="published_papers")
    email = st.text_input("Enter Email ID", key='email')
    username = st.text_input("Enter Username", key='username')
    password = st.text_input("Enter Password", key='password', type='password')
    if st.button('Register'):
        user = User(researcher_name=full_name, institution=institution,
                    published_papers=published_papers, username=username, password=password, email=email)
        response = requests.post(
            'http://localhost:8000/christograph/register', json=user.dict())
        st.write(response.json())


def login_ui():
    st.subheader('Login')
    if "username" not in st.session_state:
        st.session_state["username"] = ""

    username = st.text_input(
        'Enter Username', value=st.session_state["username"], key="login_username")
    password = st.text_input(
        'Enter Password', key='login_password', type='password')
    button = st.button("Login")
    if button:
        st.session_state["username"] = username
        requests.post(
            'http://localhost:8000/christograph/login', json={'username': username, 'password': password})
        st.write("Welcome ", username)
        # st.write(response.json())

        # progress_text = "Signing in... Please wait."
        # my_bar = st.progress(0, text=progress_text)

        # for percent_complete in range(100):
        #     time.sleep(0.01)
        #     my_bar.progress(percent_complete + 1, text=progress_text)
        return True


# def main():
#     st.title('User Authentication')
#     # Create a sidebar with a dropdown for user actions
#     action = st.sidebar.selectbox(
#         "Select an action", ["New Registration", "Login"])

#     # Create placeholders for the fields based on the selected action
#     if action == "New Registration":
#         register_ui()
#     if action == "Login":
#         login_ui()


# if __name__ == '__main__':
#     main()
