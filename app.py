import streamlit as st
import pandas as pd
import pickle
import requests
import os

# ─────────────────────────────────────────────────────────────────────────────
# PAGE CONFIGURATION
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch | Movie Recommendations",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────────────────────────────────────
# CUSTOM STYLING
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=Outfit:wght@300;400;500;600;700&display=swap');
    
    /* Main container */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* Hide default header */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    
    /* Title styling */
    .main-title {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 4.5rem;
        background: linear-gradient(90deg, #E50914 0%, #ff6b6b 50%, #E50914 100%);
        background-size: 200% auto;
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
        animation: gradient 3s ease infinite;
        letter-spacing: 4px;
    }
    
    @keyframes gradient {
        0% { background-position: 0% center; }
        50% { background-position: 100% center; }
        100% { background-position: 0% center; }
    }
    
    .subtitle {
        font-family: 'Outfit', sans-serif;
        color: #8892b0;
        text-align: center;
        font-size: 1.1rem;
        margin-top: -10px;
        margin-bottom: 2rem;
        font-weight: 300;
        letter-spacing: 2px;
    }
    
    /* Movie card styling */
    .movie-card {
        background: linear-gradient(145deg, #1e1e30 0%, #252542 100%);
        border-radius: 16px;
        padding: 1rem;
        transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
        border: 1px solid rgba(229, 9, 20, 0.1);
        height: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-8px) scale(1.02);
        box-shadow: 0 20px 40px rgba(229, 9, 20, 0.2);
        border-color: rgba(229, 9, 20, 0.4);
    }
    
    .movie-title {
        font-family: 'Outfit', sans-serif;
        color: #ffffff;
        font-size: 0.95rem;
        font-weight: 600;
        text-align: center;
        margin-top: 0.8rem;
        line-height: 1.3;
    }
    
    .movie-poster {
        border-radius: 12px;
        width: 100%;
        box-shadow: 0 8px 24px rgba(0,0,0,0.4);
    }
    
    /* Selectbox styling */
    .stSelectbox > div > div {
        background: linear-gradient(145deg, #1e1e30 0%, #252542 100%);
        border: 2px solid rgba(229, 9, 20, 0.3);
        border-radius: 12px;
        font-family: 'Outfit', sans-serif;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #E50914;
    }
    
    /* Button styling */
    .stButton > button {
        font-family: 'Outfit', sans-serif;
        background: linear-gradient(90deg, #E50914 0%, #b20710 100%);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.8rem 2.5rem;
        font-size: 1.1rem;
        font-weight: 600;
        letter-spacing: 1px;
        transition: all 0.3s ease;
        width: 100%;
        max-width: 300px;
    }
    
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 30px rgba(229, 9, 20, 0.4);
    }
    
    .stButton > button:active {
        transform: scale(0.98);
    }
    
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
        border-right: 1px solid rgba(229, 9, 20, 0.2);
    }
    
    section[data-testid="stSidebar"] .stMarkdown h2 {
        font-family: 'Bebas Neue', sans-serif;
        color: #E50914;
        letter-spacing: 2px;
    }
    
    section[data-testid="stSidebar"] .stMarkdown p {
        font-family: 'Outfit', sans-serif;
        color: #8892b0;
        font-weight: 300;
    }
    
    /* Stats box */
    .stats-box {
        background: linear-gradient(145deg, #1e1e30 0%, #252542 100%);
        border-radius: 12px;
        padding: 1.2rem;
        border: 1px solid rgba(229, 9, 20, 0.2);
        margin: 0.5rem 0;
    }
    
    .stats-number {
        font-family: 'Bebas Neue', sans-serif;
        font-size: 2.5rem;
        color: #E50914;
        line-height: 1;
    }
    
    .stats-label {
        font-family: 'Outfit', sans-serif;
        color: #8892b0;
        font-size: 0.85rem;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Spinner */
    .stSpinner > div {
        border-top-color: #E50914 !important;
    }
    
    /* Warning/Info boxes */
    .stAlert {
        background: linear-gradient(145deg, #1e1e30 0%, #252542 100%);
        border: 1px solid rgba(229, 9, 20, 0.3);
        border-radius: 12px;
    }
    
    /* Divider */
    .custom-divider {
        height: 2px;
        background: linear-gradient(90deg, transparent, #E50914, transparent);
        margin: 2rem 0;
        border: none;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        color: #4a5568;
        font-family: 'Outfit', sans-serif;
        font-size: 0.85rem;
        margin-top: 3rem;
        padding: 1rem;
    }
    
    .footer a {
        color: #E50914;
        text-decoration: none;
    }
</style>
""", unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# API KEY MANAGEMENT
# ─────────────────────────────────────────────────────────────────────────────
def get_api_key():
    """Get API key from Streamlit secrets or environment variable."""
    # Try Streamlit secrets first (for cloud deployment)
    if hasattr(st, 'secrets') and 'TMDB_API_KEY' in st.secrets:
        return st.secrets['TMDB_API_KEY']
    # Fallback to environment variable (for local development)
    api_key = os.environ.get('TMDB_API_KEY')
    if api_key:
        return api_key
    return None


# ─────────────────────────────────────────────────────────────────────────────
# DATA LOADING WITH CACHING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner=False)
def load_movies_data():
    """Load and cache the movies dataframe."""
    try:
        movies_dict = pickle.load(open('models/movies_dict.pkl', 'rb'))
        return pd.DataFrame(movies_dict)
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading movie data: {str(e)}")
        return None


@st.cache_resource(show_spinner=False)
def load_similarity_matrix():
    """Load and cache the similarity matrix."""
    try:
        return pickle.load(open('models/similarity.pkl', 'rb'))
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"Error loading similarity matrix: {str(e)}")
        return None


# ─────────────────────────────────────────────────────────────────────────────
# POSTER FETCHING WITH CACHING
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(ttl=86400, show_spinner=False)  # Cache for 24 hours
def fetch_poster(movie_id, api_key):
    """Fetch movie poster from TMDB API with caching."""
    if not api_key:
        return None
    
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}',
            params={'api_key': api_key, 'language': 'en-US'},
            timeout=10
        )
        response.raise_for_status()
        data = response.json()
        
        if data.get('poster_path'):
            return f"https://image.tmdb.org/t/p/w500{data['poster_path']}"
        return None
    except requests.exceptions.RequestException:
        return None
    except Exception:
        return None


@st.cache_data(ttl=86400, show_spinner=False)
def fetch_movie_details(movie_id, api_key):
    """Fetch additional movie details from TMDB API."""
    if not api_key:
        return {}
    
    try:
        response = requests.get(
            f'https://api.themoviedb.org/3/movie/{movie_id}',
            params={'api_key': api_key, 'language': 'en-US'},
            timeout=10
        )
        response.raise_for_status()
        return response.json()
    except Exception:
        return {}


# ─────────────────────────────────────────────────────────────────────────────
# RECOMMENDATION ENGINE
# ─────────────────────────────────────────────────────────────────────────────
def get_recommendations(movie_title, movies_df, similarity_matrix, api_key, num_recommendations=5):
    """Get movie recommendations based on similarity scores."""
    try:
        movie_index = movies_df[movies_df['title'] == movie_title].index[0]
        distances = similarity_matrix[movie_index]
        movies_list = sorted(
            list(enumerate(distances)), 
            reverse=True, 
            key=lambda x: x[1]
        )[1:num_recommendations + 1]
        
        recommendations = []
        for idx, score in movies_list:
            movie_data = movies_df.iloc[idx]
            poster_url = fetch_poster(movie_data.movie_id, api_key)
            recommendations.append({
                'title': movie_data.title,
                'movie_id': movie_data.movie_id,
                'poster': poster_url,
                'similarity': round(score * 100, 1)
            })
        
        return recommendations
    except IndexError:
        st.error("Movie not found in database.")
        return []
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}")
        return []


# ─────────────────────────────────────────────────────────────────────────────
# UI COMPONENTS
# ─────────────────────────────────────────────────────────────────────────────
def render_movie_card(movie, show_similarity=True):
    """Render a styled movie card."""
    poster_url = movie['poster'] or "https://via.placeholder.com/500x750?text=No+Poster"
    
    similarity_badge = ""
    if show_similarity and movie.get('similarity'):
        similarity_badge = f'<div style="position:absolute;top:10px;right:10px;background:#E50914;color:white;padding:4px 8px;border-radius:8px;font-size:0.75rem;font-weight:600;">{movie["similarity"]}% Match</div>'
    
    st.markdown(f"""
        <div class="movie-card">
            <div style="position:relative;">
                <img src="{poster_url}" class="movie-poster" alt="{movie['title']}" 
                     onerror="this.src='https://via.placeholder.com/500x750?text=No+Poster'">
                {similarity_badge}
            </div>
            <p class="movie-title">{movie['title']}</p>
        </div>
    """, unsafe_allow_html=True)


def render_sidebar(movies_df):
    """Render the sidebar with app info and stats."""
    with st.sidebar:
        st.markdown("## 🎬 CINEMATCH")
        st.markdown("---")
        
        st.markdown("### About")
        st.markdown("""
        CineMatch uses **content-based filtering** to recommend movies similar to your selection.
        
        The algorithm analyzes:
        - 🎭 Genres & Keywords
        - 👥 Cast & Crew
        - 📝 Plot Overview
        """)
        
        st.markdown("---")
        
        st.markdown("### How It Works")
        st.markdown("""
        1. **Select** a movie you enjoyed
        2. **Click** Get Recommendations
        3. **Discover** similar movies
        """)
        
        st.markdown("---")
        
        # Stats
        if movies_df is not None:
            st.markdown("### Database Stats")
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                    <div class="stats-box">
                        <div class="stats-number">{len(movies_df):,}</div>
                        <div class="stats-label">Movies</div>
                    </div>
                """, unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("""
        <div style="text-align:center;color:#4a5568;font-size:0.8rem;">
            Powered by TMDB API<br>
            Made with ❤️ using Streamlit
        </div>
        """, unsafe_allow_html=True)


# ─────────────────────────────────────────────────────────────────────────────
# MAIN APPLICATION
# ─────────────────────────────────────────────────────────────────────────────
def main():
    # Get API key
    api_key = get_api_key()
    
    # Load data
    with st.spinner("Loading movie database..."):
        movies_df = load_movies_data()
        similarity_matrix = load_similarity_matrix()
    
    # Check if data loaded successfully
    if movies_df is None or similarity_matrix is None:
        st.error("⚠️ Could not load model files!")
        st.markdown("""
        ### Setup Required
        
        Please run the following command to download the model files:
        
        ```bash
        python download_models.py
        ```
        
        Or deploy with the model files in the `models/` directory.
        """)
        st.stop()
    
    # Check API key
    if not api_key:
        st.warning("""
        ⚠️ **TMDB API Key not configured!**
        
        Movie posters won't be displayed. To enable posters:
        
        **For Local Development:**
        1. Create `.streamlit/secrets.toml`
        2. Add: `TMDB_API_KEY = "your_key_here"`
        
        **For Streamlit Cloud:**
        1. Go to App Settings → Secrets
        2. Add: `TMDB_API_KEY = "your_key_here"`
        
        Get a free API key at [TMDB](https://www.themoviedb.org/settings/api)
        """)
    
    # Render sidebar
    render_sidebar(movies_df)
    
    # Main content
    st.markdown('<h1 class="main-title">CINEMATCH</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Discover Your Next Favorite Movie</p>', unsafe_allow_html=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Movie selection
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        selected_movie = st.selectbox(
            "🎬 Select a movie you enjoyed:",
            options=movies_df['title'].values,
            index=None,
            placeholder="Type or select a movie..."
        )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Center the button
        _, btn_col, _ = st.columns([1, 2, 1])
        with btn_col:
            recommend_btn = st.button("🎯 Get Recommendations", use_container_width=True)
    
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    
    # Show recommendations
    if recommend_btn:
        if selected_movie:
            with st.spinner("🔍 Finding similar movies..."):
                recommendations = get_recommendations(
                    selected_movie, 
                    movies_df, 
                    similarity_matrix, 
                    api_key
                )
            
            if recommendations:
                st.markdown(f"""
                    <h3 style="font-family:'Outfit',sans-serif;color:#fff;text-align:center;margin-bottom:1.5rem;">
                        Because you liked <span style="color:#E50914;">{selected_movie}</span>
                    </h3>
                """, unsafe_allow_html=True)
                
                # Display recommendations in a grid
                cols = st.columns(5)
                for idx, movie in enumerate(recommendations):
                    with cols[idx]:
                        render_movie_card(movie)
        else:
            st.warning("👆 Please select a movie first!")
    
    # Footer
    st.markdown("""
        <div class="footer">
            <p>Data provided by <a href="https://www.themoviedb.org/" target="_blank">TMDB</a> • 
            Built with <a href="https://streamlit.io/" target="_blank">Streamlit</a></p>
        </div>
    """, unsafe_allow_html=True)


if __name__ == '__main__':
    main()
