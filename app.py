from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests

app = Flask(__name__)

# Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# TMDB Poster API fetch function
def fetch_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=db8e7adef6f8c8d812a373df04d2b6e1&language=en-US'
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommendation function
def recommend(movie_title):
    movie_index = movies[movies['title'] == movie_title].index[0]
    distances = similarity[movie_index]
    similar_movies = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_titles = []
    recommended_posters = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_titles.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    
    return recommended_titles, recommended_posters

# Flask routes
@app.route('/', methods=['GET', 'POST'])
@app.route('/', methods=['GET', 'POST'])
def index():
    movie_list = movies['title'].values
    combined = []

    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        recommendations, posters = recommend(selected_movie)
        combined = zip(recommendations, posters)  # ✅ zip in Python, not in template

    return render_template('index.html',
                           movie_names=movie_list,
                           combined=combined)


if __name__ == '__main__':
    app.run(debug=True)
