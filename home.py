import streamlit as st

# Set page title and favicon
# st.set_page_config(page_title='Streamlit Home Page', page_icon=':rocket:')


def home_ui():

    # Define page header
    st.title('Welcome to Christograph!')
    st.write('A much needed website for researchers!')

    # Add page sections
    with st.expander('Section 1'):
        # Add content for section 1
        st.write('This is section 1. Add your content here.')

    with st.expander('Section 2'):
        # Add content for section 2
        st.write('This is section 2. Add your content here.')

    with st.expander('Section 3'):
        # Add content for section 3
        st.write('This is section 3. Add your content here.')

    # Add footer
    st.write('© 2023 Your Company Name. All rights reserved.')
