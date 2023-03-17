import streamlit as st
import pymongo

# Initialize connection.
# Uses st.cache_resource to only run once.


@st.cache_resource
def init_connection():
    return pymongo.MongoClient(**st.secrets["mongo"])


client = init_connection()

# Pull data from the collection.
# Uses st.cache_data to only rerun when the query changes or after 10 min.

# database connection
db = client.summarizer_db

# get data


# @st.cache_data(ttl=600)
# def get_data():
#     items = db.summarized_text.find()
#     items = list(items)  # make hashable for st.cache_data
#     return items

# # insert data


# @st.cache_data(ttl=600)
# def insert_data():
#     # db.summarized_text.insert_one(data)
#     st.write("Saved!")
#     return True


# items = get_data()

# # Print results.
# for item in items:
#     st.write(f"{item['name']} has a :{item['pet']}:")
