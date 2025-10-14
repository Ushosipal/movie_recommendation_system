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
import gdown

app = Flask(__name__)

MOVIE_PATH = "movie_dict.pkl"
SIM_PATH = "similarity.pkl"
SIM_ID = "1Iji_peOVfBKg7YP7icEJKMsi7Sl1nJex"

# Download similarity file if not exists
if not os.path.exists(SIM_PATH):
    gdown.download(f"https://drive.google.com/uc?id={SIM_ID}", SIM_PATH, quiet=False)

# Load data
movies_dict = pickle.load(open(MOVIE_PATH, 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open(SIM_PATH, 'rb'))

# Fetch poster using OMDb API by movie title
def fetch_poster(movie_title):
    url = f'http://www.omdbapi.com/?t={movie_title}&apikey=7645fecd'
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

# Recommendation function
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_titles = []
    recommended_posters = []
    for i in similar_movies:
        title = movies.iloc[i[0]].title
        recommended_titles.append(title)
        recommended_posters.append(fetch_poster(title))
    
    return recommended_titles, recommended_posters


@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    combined = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations, posters = recommend(selected_movie)
        combined = zip(recommendations, posters)

    return render_template('index.html',
                           movie_names=movie_list,
                           combined=combined)

if __name__ == '__main__':
    app.run(debug=True)
