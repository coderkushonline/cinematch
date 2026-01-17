import pandas as pd
from fastapi import FastAPI, HTTPException
import pickle
from sklearn.metrics.pairwise import cosine_similarity
import uvicorn
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Load artifacts
indices = None
tfidf_matrix = None
df = None
title_to_id = {}

# TMDB API Key
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

def load_data():
    global indices, tfidf_matrix, df, title_to_id
    try:
        # Load artifacts
        with open('artifacts/indices.pkl', 'rb') as f:
            indices = pickle.load(f)
        with open('artifacts/tfidf_matrix.pkl', 'rb') as f:
            tfidf_matrix = pickle.load(f)
        with open('artifacts/df.pkl', 'rb') as f:
            df = pickle.load(f)
        print("Model loaded successfully")
        
        # Load CSV for ID mapping
        try:
            print("Loading movies_metadata.csv for ID mapping...")
            meta_df = pd.read_csv('dataset/movies_metadata.csv', low_memory=False)
            # Filter valid IDs
            meta_df = meta_df[pd.to_numeric(meta_df['id'], errors='coerce').notnull()]
            meta_df['id'] = meta_df['id'].astype(int)
            
            # Handle duplicates: keep the first occurrence
            meta_df = meta_df.drop_duplicates(subset=['title'])
            title_to_id = meta_df.set_index('title')['id'].to_dict()
            print(f"ID mapping created for {len(title_to_id)} titles.")
        except Exception as e:
            print(f"Error loading CSV for ID mapping: {e}")
            
    except Exception as e:
        print(f"Error loading model: {e}")

@app.on_event("startup")
async def startup_event():
    load_data()

def fetch_details(movie_id):
    if not TMDB_API_KEY:
        return "https://via.placeholder.com/500x750?text=API+Key+Missing", "No overview (API Key Check Failed)"
    
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
    try:
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            overview = data.get('overview', 'No overview available.')
            if poster_path:
                full_path = f"https://image.tmdb.org/t/p/w500/{poster_path}"
                return full_path, overview
        return "https://via.placeholder.com/500x750?text=No+Image", "Movie details not found."
    except Exception as e:
        print(f"Error fetching TMDB data: {e}")
        return "https://via.placeholder.com/500x750?text=Error", "Error fetching data."

@app.get("/")
def read_root():
    return {"message": "Movie Recommender API is running"}

@app.get("/titles")
def get_titles():
    if indices is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    if hasattr(indices, 'index'):
        vals = indices.index.tolist()
        return vals if isinstance(vals, list) else list(indices.keys())
    elif isinstance(indices, dict):
        return list(indices.keys())
    return []

@app.get("/recommend")
def recommend(title: str, n: int = 5):
    if indices is None:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    if title not in indices:
        raise HTTPException(status_code=404, detail="Movie not found")

    try:
        idx = indices[title]
        
        # Calculate similarity
        sim_score = cosine_similarity(tfidf_matrix[idx], tfidf_matrix).flatten()
        similar_idx = sim_score.argsort()[::-1][1:n+1]
        
        recommendations = []
        
        for i in similar_idx:
            movie_title = df['title'].iloc[i]
            
            # Get ID from mapping
            movie_id = title_to_id.get(movie_title)
            
            if movie_id:
                poster_url, overview = fetch_details(movie_id)
            else:
                poster_url = "https://via.placeholder.com/500x750?text=No+ID"
                overview = "Movie ID not found in metadata."

            recommendations.append({
                "title": movie_title,
                "poster": poster_url,
                "overview": overview,
                "id": int(movie_id) if movie_id else None
            })
            
        return recommendations
    except Exception as e:
        print(f"Error during recommendation: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
