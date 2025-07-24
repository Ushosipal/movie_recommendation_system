# 🎬 Movie Recommendation System

A content-based movie recommendation web app built using **Flask**, **Python**, and **HTML/CSS**. It suggests similar movies based on the one selected by the user, using **cosine similarity** applied to vectorized movie metadata via `CountVectorizer`.

---

## 🚀 Features

- 🎯 **Content-Based Filtering** using `CountVectorizer` + Cosine Similarity
- 🎥 **Movie posters** fetched using the **TMDB API** for a visually rich experience
- 🌌 **Animated starry background** for an engaging UI (via CSS)
- 🔄 Dropdown resets to “Please select a movie” after recommendations
- ⚡ Fast response with all models serialized using `pickle`

---

## 🧠 How It Works

1. Movie data (genres, keywords, cast, crew, etc.) is combined into a single text-based column.
2. This text data is transformed into vectors using **`CountVectorizer`**.
3. **Cosine similarity** is computed between these vectors to find movies similar to the selected one.
4. The top 5 most similar movies are returned — complete with their posters fetched via **TMDB API**.

---

## 🛠️ Tech Stack

**Backend:**
- Python
- Flask
- Pickle (`movies.pkl`, `movie_dict.pkl`, `similarity.pkl`)

**Machine Learning:**
- `CountVectorizer` from `sklearn.feature_extraction.text`
- `cosine_similarity` from `sklearn.metrics.pairwise`

**Frontend:**
- HTML
- CSS (Animated Background)
- JavaScript (Optional for UI interactions)

**External APIs:**
- [TMDB API](https://www.themoviedb.org/documentation/api) for fetching movie posters

---

## 🗂️ Project Structure

📁 movie_recommendation_system/
│
├── static/
│ └── styles.css # Custom CSS with background animation
│
├── templates/
│ └── index.html # Frontend HTML template
│
├── movie_dict.pkl # Dictionary of movie metadata
├── similarity.pkl # Cosine similarity matrix
├── movies.pkl # Preprocessed movie data
├── app.py # Flask application
├── requirements.txt # Python dependencies
└── runtime.txt # Python version specification (e.g., 3.10.12)
