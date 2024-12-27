import streamlit as st
import pandas as pd
import pickle
import requests
import subprocess
from PIL import Image
import io

# Configure the page
st.set_page_config(
    page_title="Movie Recommender System",
    page_icon="🎬",
    layout="wide"
)

# Custom CSS to improve the appearance
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stTitle {
        font-size: 3rem !important;
        color: #1f77b4 !important;
    }
    .movie-poster {
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)


# Load the saved model and data
def load_model_and_data():
    with open("models/similarity.pkl", "rb") as f:
        similarity = pickle.load(f)

    with open("models/movies_dict.pkl", "rb") as f:
        movies_dict = pickle.load(f)


# Function to fetch movie poster
def fetch_poster(movie_id):
    try:
        # You'll need to sign up for TMDB API and get your API key
        API_KEY = "357cee4dae512f33a2c481260b69c62c"
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US'
        )
        data = response.json()
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
        return full_path
    except Exception as e:
        st.error(f"Error fetching poster: {str(e)}")
        return None


# Function to get movie recommendations
def recommend(movie, movies, similarity):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters


# Main function to run the Streamlit app
def main():
    st.title("🎬 Movie Recommender System")

    try:
        subprocess.run(["python", "download_models.py"], check=True)
        movies, similarity = load_model_and_data()
    except Exception as e:
        st.error("Error loading model and data. Please check if the required files exist.")
        st.stop()

    # Create a sidebar for additional information
    with st.sidebar:
        st.header("About")
        st.write("""
        This movie recommender system uses content-based filtering to suggest movies 
        similar to your selection. It analyzes movie features such as genres, cast, 
        crew, and plot keywords to make recommendations.
        """)

        st.header("How it works")
        st.write("""
        1. Select a movie from the dropdown
        2. Click 'Get Recommendations'
        3. View similar movies with their posters
        """)

    # Main content
    selected_movie = st.selectbox("Select a movie you like:",movies['title'].values,index=None,placeholder="Choose a movie...")

    if st.button('Get Recommendations'):
        if selected_movie:
            with st.spinner('Finding similar movies...'):
                names, posters = recommend(selected_movie, movies, similarity)

                # Display recommendations in a grid
                cols = st.columns(5)
                for idx, (name, poster) in enumerate(zip(names, posters)):
                    with cols[idx]:
                        st.image(poster, caption=name, use_container_width=True)
                        st.markdown(f"**{name}**")
        else:
            st.warning('Please select a movie first.')


if __name__ == '__main__':
    main()
