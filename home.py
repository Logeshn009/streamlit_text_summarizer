import streamlit as st
from db_connection import db
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from PIL import Image

messages = db["messages"]
# Set page title and favicon
# st.set_page_config(page_title='Streamlit Home Page', page_icon=':rocket:')


def home_ui():

    # Define page header
    st.title('Welcome to Christograph!')
    st.write('A much needed website for researchers!')

    # Add page sections
    with st.expander('Text summarizer'):
        # Add content for section 1
        text_summarizer_img = Image.open('text_summarizer.png')
        st.image(text_summarizer_img, caption='Text summarizers')
        st.subheader('How to use text summarizer')
        st.write('1) Go to text summarizer ')
        st.write('2) Select any one of the model like the T5 or BART')
        st.write('3) Set Parameters click on enter')

    with st.expander('Recommendation System'):
        # Add content for section 2
        st.write('This is section 2. Add your content here.')

    with st.expander('Insights Page'):
        # Add content for section 3
        st.write('This is section 3. Add your content here.')

    # Add footer
    st.write('© 2023 Christograph. All rights reserved.')


def contact_page():
    st.header("Contact Us")

    with st.form(key='contact_form'):
        name = st.text_input("Name", key="name")
        email = st.text_input("Email", key="email")
        message = st.text_area("Message", key="message")
        submitted = st.form_submit_button("Submit")

        if submitted:

            # Save the message to the database
            try:
                message_data = {"name": name,
                                "email": email, "message": message}
                messages.insert_one(message_data)
                st.success(
                    "Thank you for your message! We'll get back to you as soon as possible.")

            except Exception as e:
                st.error(
                    "There was an error sending your message. Please try again later.", e)
