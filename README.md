# 🎬 Movie Recommendation System

A content-based movie recommendation web app built using **Flask**, **Python**, and **HTML/CSS**. It suggests similar movies based on the one selected by the user, using **cosine similarity** applied to vectorized movie metadata via `CountVectorizer`. Posters and trailers are dynamically fetched using **OMDB** and **YouTube APIs**.

---

## 🚀 Features

- 🎯 **Content-Based Filtering** using `CountVectorizer` + Cosine Similarity  
- 🎥 **Movie posters and trailers** fetched dynamically via **OMDB & YouTube APIs**  
- 🌌 **Animated starry background** for an engaging UI (via CSS)  
- 🔄 Dropdown resets to “Please select a movie” after recommendations  
- ⚡ Fast response with all models serialized using `pickle`  

---

## 🧠 How It Works

1. Movie data (genres, keywords, cast, crew, etc.) is combined into a single text column.  
2. Text data is transformed into vectors using **`CountVectorizer`**.  
3. **Cosine similarity** is computed between these vectors to find movies similar to the selected one.  
4. The top 5 most similar movies are returned, along with their posters and trailers.  

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

**External APIs:**  
- [OMDB API](http://www.omdbapi.com/) for movie posters  
- [YouTube Data API](https://developers.google.com/youtube/v3) for trailers  

---

## 🗂️ Project Structure
movie_recommendation_system/
│
├── static/
│ └── style.css # Custom CSS with background animation
│
├── templates/
│ └── index.html # Frontend HTML template
│
├── movie_dict.pkl # Dictionary of movie metadata
├── similarity.pkl # Cosine similarity matrix
├── movies.pkl # Preprocessed movie data
├── app.py # Flask application
├── requirements.txt # Project dependencies
├── .env # API keys (not pushed to Git)


---

## 📦 Requirements

```text
blinker==1.9.0
certifi==2025.7.14
charset-normalizer==3.4.2
click==8.2.1
colorama==0.4.6
Flask==3.1.1
gunicorn==23.0.0
idna==3.10
itsdangerous==2.2.0
Jinja2==3.1.6
MarkupSafe==3.0.2
numpy==1.26.4
packaging==25.0
pandas==1.5.3
python-dateutil==2.9.0.post0
pytz==2025.2
requests==2.32.4
six==1.17.0
tzdata==2025.2
urllib3==2.5.0
Werkzeug==3.1.3
scikit-learn==1.2.2
joblib==1.4.2
gdown==4.7.1
python-dotenv==1.0.0

