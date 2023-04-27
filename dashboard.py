import streamlit as st
from db_connection import db
import streamlit as st
from pymongo import MongoClient
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

research_collection = db["research_details"]


def dashboard_page():
    st.subheader("Dashboard page")


# connect to MongoDB
collection = db["research_details"]

# fetch all records
records = collection.find()

# create a list of dictionaries containing the areas of interest, research domain, and research paper name for each researcher
researchers = []
for record in records:
    researcher = {
        "username": record["username"],
        "research_domain": record["research_domain"],
        "research_paper_name": record["research_paper_name"],
        "areas_of_interest": " ".join(record["areas_of_interest"])
    }
    researchers.append(researcher)

print(researchers)
# create a TF-IDF vectorizer to convert the areas of interest, research domain, and research paper name of researchers to numerical vectors
tfidf_vectorizer = TfidfVectorizer()

# fit and transform the TF-IDF vectorizer on the areas of interest, research domain, and research paper name of researchers
researchers_tfidf = tfidf_vectorizer.fit_transform(
    [researcher["areas_of_interest"] + " " + researcher["research_domain"] + " " + researcher["research_paper_name"] for researcher in researchers])

# compute the cosine similarity matrix between the TF-IDF vectors of the researchers
cosine_similarities = cosine_similarity(researchers_tfidf, researchers_tfidf)

# define a function to recommend similar researchers based on a given username


def recommend(username):
    # get the index of the researcher with the given username
    index = [i for i, researcher in enumerate(
        researchers) if researcher["username"] == username][0]
    # get the cosine similarities between the researcher with the given username and all other researchers
    cosine_similarities_user = cosine_similarities[index]
    # get the indices of the top 5 most similar researchers
    similar_researcher_indices = cosine_similarities_user.argsort()[::-1][1:6]
    # get the usernames of the top 5 most similar researchers
    similar_researchers = [researchers[i]["username"]
                           for i in similar_researcher_indices]

    return similar_researchers


def recommend_page():
    # create a Streamlit app to allow researchers to enter their username and get recommended researchers
    st.title("Researcher Recommendation System")
    user_name = st.session_state["user_name"]
    # username = st.text_input("Enter your username:")
    if user_name:
        recommended_researchers = recommend(user_name)
        if recommended_researchers:
            st.write("Recommended Researchers:")
            for recommended_researcher in recommended_researchers:
                st.write("- " + recommended_researcher)
        else:
            st.write("No recommended researchers found.")
