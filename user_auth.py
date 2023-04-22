import streamlit as st
from streamlit import session_state
import pymongo

# Login Page


def login():
    # Collect user information
    email = st.text_input("Email")
    password = st.text_input("Password", type="password", value="")

    # Authenticate the user
    client = pymongo.MongoClient("mongodb://localhost:27017/")
    db = client["mydatabase"]
    users = db["users"]
    user = users.find_one({"email": email, "password": password})
    if user is not None:
        # Store the user ID in the session_state
        session_state = session_state.get(user_id=user["_id"])
        print(session_state)
        # Redirect to the user dashboard
        st.experimental_rerun()
    else:
        st.error("Invalid login credentials")

# User Dashboard


def user_dashboard():
    # Get the user ID from the session_state
    session_state = session_state.get(user_id=None)
    user_id = session_state.user_id

    if user_id is not None:
        # Fetch the user details from the database
        client = pymongo.MongoClient("mongodb://localhost:27017/")
        db = client["mydatabase"]
        users = db["users"]
        user = users.find_one({"_id": user_id})

        # Display the user dashboard details
        st.write(f"Welcome {user['name']}!")
        st.write(f"Email: {user['email']}")
    else:
        # Redirect to the login page
        st.redirect("login")

# Main App


def main():
    st.title("My App")

    # Check if the user is logged in
    session_state = session_state.get(user_id=None)
    if session_state.user_id is None:
        login()
    else:
        user_dashboard()


if __name__ == "__main__":
    main()
