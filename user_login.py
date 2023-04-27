from fastapi import FastAPI, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends, status
from datetime import timedelta
from fastapi.responses import JSONResponse
import streamlit_authenticator as stauth
from db_connection import db
from pydantic import BaseModel
import streamlit as st
import requests
import uuid
import json
from fastapi.middleware.cors import CORSMiddleware
import jwt
from datetime import datetime, timedelta
import navbar

# mongo collection
users_collection = db['researcher_details']

# Set up password hashing
pwd_context = CryptContext(schemes=["bcrypt"], bcrypt__default_rounds=12)

# Set up FastAPI
christograph = FastAPI()

# secret key
SECRET_KEY = "Asdfgf009***"

# Define user model


class User(BaseModel):
    researcher_name: str
    institution: str
    published_papers: int
    email: str
    username: str
    password: str


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
    user_login = users_collection.find_one(
        {"username": credentials.username})
    # full_name = users_collection.find_one({"full_name": user.researcher_name})
    if not user_login:
        raise HTTPException(
            status_code=401, detail="Invalid username of researcher name")
    hashed = user_login["password"]
    # Verify the password hash
    if not pwd_context.verify(credentials.password, hashed):
        raise HTTPException(
            status_code=401, detail="Invalid username or password")

    # Create JWT token with user data
    # access_token_expires = timedelta(minutes=10)
    # access_token = create_access_token(
    #     data={"sub": user_login["username"]},
    #     expires_delta=access_token_expires
    # )
    # response.set_cookie(key="Authorization",
    #                     value=f"Bearer {access_token}", httponly=True)
    return {"message": "login successful"}


# def create_access_token(data: dict, expires_delta: timedelta):
#     to_encode = data.copy()
#     if expires_delta:
#         expire = datetime.utcnow() + expires_delta
#     else:
#         expire = datetime.utcnow() + timedelta(minutes=15)
#     to_encode.update({"exp": expire})
#     encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm="HS256")
#     return encoded_jwt
# Streamlit UI


def register_ui():
    st.title("Create an Account")
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
        requests.post(
            'http://localhost:8000/christograph/register', json=user.dict())
        st.write("Account created successfully")


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
        credentials = {'usernames': username, 'password': password}
        requests.post(
            'http://localhost:8000/christograph/login', json=credentials)
        print("responsed")


def new_login():

    pipeline = [
        {
            "$match": {}
        },
        {
            "$project": {
                "_id": 0,
                "username": {
                    "email": "$email",
                    "name": "$full_name",
                    "password": "$password",
                    "username": "$username"
                }
            }
        }
    ]

    result = users_collection.aggregate(pipeline=pipeline)

    data = {"credentials": {"usernames": {}}}

    for doc in result:
        username = doc["username"]["username"]
        email = doc["username"]["email"]
        name = doc["username"]["name"]
        password = doc["username"]["password"]
        data["credentials"]["usernames"][username] = {
            "email": email, "name": name, "password": password}
    data_credentials = data["credentials"]
    # st.write(data_credentials)

    config = {
        "credentials":
            data_credentials,
        "cookie": {
            "expiry_days": 1,
            "key": "christograph_key",
            "name": "christograph_cookie"
        },
        "preauthorized": {
            "emails": [
                "logeshn1297@gmail.com"
            ]
        }
    }
    # st.write(config)

    authenticator = stauth.Authenticate(
        config['credentials'],
        config['cookie']['name'],
        config['cookie']['key'],
        config['cookie']['expiry_days'],
        config['preauthorized']
    )
    if "user_name" not in st.session_state:
        st.session_state["user_name"] = ""

    name, authentication_status, username = authenticator.login(
        'Login', 'main')
    if authentication_status:
        st.session_state["user_name"] = username
        authenticator.logout('Logout', 'sidebar')
        st.subheader(f'Welcome *{username}*')
        navbar.main()
    elif authentication_status is False:
        st.error('Username/password is incorrect')
    elif authentication_status is None:
        st.warning('Please enter your username and password')

# new_login()
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


if __name__ == '__main__':
    new_login()
