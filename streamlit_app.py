import streamlit as st
import requests

st.set_page_config(page_title="Cinematch", layout="wide", page_icon="🎬")

# Custom CSS for a premium look
st.markdown("""
<style>
    /* Main background */
    .stApp {
        background-color: #0e1117;
    }
    
    /* Header */
    h1 {
        color: #E50914 !important; /* Netflix Red */
        text-align: center;
        font-family: 'Arial', sans-serif;
        font-weight: 800;
    }
    
    div[data-testid="stMarkdownContainer"] p {
        font-size: 1.1rem;
    }
    
    /* Button styling */
    .stButton>button {
        color: white;
        background-color: #E50914;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        background-color: #b20710;
        transform: scale(1.02);
    }
    
    /* Poster hover effect */
    div[data-testid="stImage"] img {
        border-radius: 8px;
        transition: transform 0.3s ease;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }
    div[data-testid="stImage"] img:hover {
        transform: scale(1.05);
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
        z-index: 10;
    }
    
    /* Text styling */
    .movie-title {
        color: #ffffff;
        font-weight: 600;
        margin-top: 5px;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎬 Cinematch")
st.markdown("<p style='text-align: center; color: #aaa;'>Your personal movie recommendation engine powered by AI.</p>", unsafe_allow_html=True)
st.markdown("---")

# Fetch titles from backend
@st.cache_data
def get_movie_titles():
    try:
        resp = requests.get("http://localhost:8000/titles")
        if resp.status_code == 200:
            return resp.json()
        else:
            return []
    except:
        return []

movie_list = get_movie_titles()

if not movie_list:
    st.warning("⚠️ Backend is not accessible. Please run `python backend.py`.")
else:
    # Centered layout for search
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        selected_movie = st.selectbox("Search for a movie you love:", movie_list)
        recommend_btn = st.button("Get Recommendations")

    if recommend_btn:
        with st.spinner("Analyzing viewing patterns..."):
            try:
                resp = requests.get(f"http://localhost:8000/recommend?title={selected_movie}")
                if resp.status_code == 200:
                    recommendations = resp.json()
                    
                    st.markdown("### 🍿 Top Picks for You")
                    
                    cols = st.columns(5)
                    for idx, movie in enumerate(recommendations):
                        with cols[idx]:
                            st.image(movie['poster'], width='stretch')
                            st.markdown(f"<div class='movie-title'>{movie['title']}</div>", unsafe_allow_html=True)
                            with st.expander("Details"):
                                st.caption(movie['overview'])
                else:
                    st.error("Movie not found or server error.")
            except Exception as e:
                st.error(f"Connection Error: {e}")
