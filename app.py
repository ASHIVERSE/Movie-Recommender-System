# from flask import Flask, render_template, request
# import pickle
# import pandas as pd
# import requests
# import os

# app = Flask(__name__)
# @app.route('/')
# def index():
#     return render_template('index.html')
# @app.route('/')
# def index():
#     movie_titles = movies['title'].values  # Get list of movie titles from DataFrame
#     return render_template('index.html', movie_titles=movie_titles)
# @app.route('/recommend', methods=['POST'])
# def recommend():
#     movie_name = request.form['movie']
#     # Put your recommendation logic here
#     return f"You selected: {movie_name}"

# if __name__ == '__main__':
#     app.run(debug=True)

# # Load the pickled files
# movies_dict = pickle.load(open(os.path.join('model', 'movie_dict.pkl'), 'rb'))
# movies = pd.DataFrame(movies_dict)

# similarity = pickle.load(open(os.path.join('model', 'similarity.pkl'), 'rb'))

# # TMDB poster fetch function
# def fetch_poster(movie_id):
#     url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=488dc5dfee0adba9d95f4443960e692b&language=en-US"
#     response = requests.get(url)
#     data = response.json()
#     return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# # Recommender function
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

#     recommended_movies = []
#     recommended_posters = []

#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_id))

#     return recommended_movies, recommended_posters

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     movie_titles = movies['title'].values
#     if request.method == 'POST':
#         selected_movie = request.form.get('movie')
#         names, posters = recommend(selected_movie)
#         return render_template('index.html', movie_titles=movie_titles, names=names, posters=posters)
#     return render_template('index.html', movie_titles=movie_titles, names=[], posters=[])

# if __name__ == '__main__':
#     app.run(debug=True)

from flask import Flask, render_template, request
import pickle
import pandas as pd
import requests
import os

app = Flask(__name__)

# Load the pickled files
movies_dict = pickle.load(open(os.path.join('model', 'movie_dict.pkl'), 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open(os.path.join('model', 'similarity.pkl'), 'rb'))

# TMDB poster fetch function
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=488dc5dfee0adba9d95f4443960e692b&language=en-US"
    response = requests.get(url)
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Recommender function
def recommend_movies(movie):
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

# Single route for both GET and POST
@app.route('/', methods=['GET', 'POST'])
def index():
    movie_titles = movies['title'].values
    if request.method == 'POST':
        selected_movie = request.form.get('movie')
        names, posters = recommend_movies(selected_movie)
        return render_template('index.html', movie_titles=movie_titles, names=names, posters=posters, zip=zip)

    return render_template('index.html', movie_titles=movie_titles, names=[], posters=[])

# Start Flask app
if __name__ == '__main__':
    app.run(debug=True)
