# 🎬 Cinematch - Movie Recommendation System

Cinematch is a sophisticated content-based movie recommendation engine that suggests movies based on similarity to a user's selected title. Built with a high-performance FastAPI backend and a visually engaging Streamlit frontend, it leverages Machine Learning to provide personalized viewing experiences.

## 🚀 Features

- **Content-Based Filtering**: Uses TF-IDF Vectorization and Cosine Similarity to analyze movie metadata (overviews, genres, cast, crew).
- **Real-Time Data**: Integrates with the **TMDB API** to fetch high-quality movie posters and detailed overviews.
- **Dual Architecture**: Decoupled Client-Server architecture with:
    - **FastAPI** for high-speed computation and API responses.
    - **Streamlit** for a modern, responsive, and interactive user interface.
- **Search Functionality**: Instant search across thousands of movie titles.
- **Responsive Design**: Premium dark-themed UI that looks great on any screen.
- **Vibecoded Frontend/UI**: The frontend was vibecoded with anti-gravity to ensure a premium and fluid user experience.

## 🛠️ Tech Stack

- **Language**: Python 3.12+
- **Machine Learning**: Scikit-Learn (TF-IDF, Cosine Similarity), Pandas, NumPy
- **Backend**: FastAPI, Uvicorn
- **Frontend**: Streamlit
- **API**: The Movie Database (TMDB) API

## 📂 Project Structure

```bash
Project5-Movie_Recommendation_System/
├── artifacts/             # Pre-computed ML models (pickles)
│   ├── df.pkl             # Processed dataframe
│   ├── indices.pkl        # Movie title indices
│   ├── tfidf_matrix.pkl   # TF-IDF sparse matrix
│   └── tfidf.pkl          # Vectorizer object
├── dataset/               # Raw dataset
│   └── movies_metadata.csv
├── notebook/              # Jupyter notebooks for EDA and Model Training
├── backend.py             # FastAPI Server application
├── streamlit_app.py       # Streamlit Frontend application
├── requirements.txt       # Project dependencies
├── .env                   # Environment variables (API Keys)
└── README.md              # Project documentation
```

## ⚡ Getting Started

### Prerequisites

- Python 3.8 or higher
- A TMDB API Key (Get one [here](https://www.themoviedb.org/documentation/api))

### Installation

1. **Clone the repository**
   ```bash
   git https://github.com/coderkushonline/cinematch.git
   cd cinematch
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use: .venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up Environment Variables**
   Create a `.env` file in the root directory and add your TMDB API Key:
   ```env
   TMDB_API_KEY=your_tmdb_api_key_here
   ```

### Running the Application

This project requires both the backend and frontend to be running simultaneously.

1. **Start the Backend Server**
   Open a terminal and run:
   ```bash
   python backend.py
   ```
   *The server will start at `http://localhost:8000`*

2. **Start the Frontend Application**
   Open a second terminal and run:
   ```bash
   streamlit run streamlit_app.py
   ```
   *The application will open in your browser at `http://localhost:8501`*

## 🧠 How It Works

1. **Data Preprocessing**: The system uses a dataset of movies to clean and combine features like keywords, cast, genres, and overview into a single "tag".
2. **Vectorization**: TF-IDF (Term Frequency-Inverse Document Frequency) converts these text tags into numerical vectors.
3. **Similarity Calculation**: Cosine Similarity measures the angle between these vectors to determine how similar two movies are.
4. **Recommendation**: When a user selects a movie, the system finds the 5 closest vectors (movies) and returns them.
5. **Enrichment**: The ID of the recommended movies is mapped to the TMDB API to fetch the latest poster URL and overview for display.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---
*Created by coderkush*
