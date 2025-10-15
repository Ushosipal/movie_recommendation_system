# from flask import Flask, render_template, request
# import pickle
# import pandas as pd
# import requests

# app = Flask(__name__)

# # Load data
# movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl', 'rb'))

# # TMDB Poster API fetch function
# def fetch_poster(movie_id):
#     url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=db8e7adef6f8c8d812a373df04d2b6e1&language=en-US'
#     response = requests.get(url)
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# # Recommendation function
# def recommend(movie_title):
#     movie_index = movies[movies['title'] == movie_title].index[0]
#     distances = similarity[movie_index]
#     similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
#     recommended_titles = []
#     recommended_posters = []
#     for i in similar_movies:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_titles.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_id))
    
#     return recommended_titles, recommended_posters

# # Flask routes
# @app.route('/', methods=['GET', 'POST'])
# @app.route('/', methods=['GET', 'POST'])
# def index():
#     movie_list = movies['title'].values
#     combined = []

#     if request.method == 'POST':
#         selected_movie = request.form.get('movie')
#         recommendations, posters = recommend(selected_movie)
#         combined = zip(recommendations, posters)  # ✅ zip in Python, not in template

#     return render_template('index.html',
#                            movie_names=movie_list,
#                            combined=combined)


# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
import os
from dotenv import load_dotenv
import urllib.request

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")


app = Flask(__name__)

MOVIE_PATH = "movie_dict.pkl"
SIM_PATH = "similarity.pkl"
SIM_URL = "https://github.com/Ushosipal/movie_recommendation_system/releases/download/v1.0/similarity.pkl"

if not os.path.exists(SIM_PATH):
    print("🔽 Downloading similarity.pkl from GitHub Releases...")
    urllib.request.urlretrieve(SIM_URL, SIM_PATH)
    print("✅ Download complete from GitHub.")
else:
    print("✅ similarity.pkl already exists locally.")

movies_dict = pickle.load(open(MOVIE_PATH, 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIM_PATH, 'rb'))

def fetch_poster(movie_title):
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}'
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if data.get("Poster") and data["Poster"] != "N/A":
            return data["Poster"]
        else:
            return "https://via.placeholder.com/300x450?text=No+Poster+Available"
    except requests.exceptions.RequestException as e:
        print("⚠️ Error fetching poster:", e)
        return "https://via.placeholder.com/300x450?text=No+Poster+Available"

def fetch_trailer(movie_title):
    search_url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "part": "snippet",
        "q": f"{movie_title} official trailer",
        "key": YOUTUBE_API_KEY,
        "maxResults": 1,
        "type": "video"
    }
    try:
        response = requests.get(search_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        items = data.get("items")
        if items:
            video_id = items[0]["id"]["videoId"]
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except requests.exceptions.RequestException as e:
        print("⚠️ Error fetching trailer:", e)
        return None

def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_titles = []
    recommended_posters = []
    recommended_trailers = []

    for i in similar_movies:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))
        recommended_trailers.append(fetch_trailer(title))

    return recommended_titles, recommended_posters, recommended_trailers

@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    combined = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations, posters, trailers = recommend(selected_movie)
        combined = zip(recommendations, posters, trailers)

    return render_template('index.html',
                           movie_names=movie_list,
                           combined=combined)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))  
    app.run(host="0.0.0.0", port=port, debug=True)
