# import streamlit as st
# import pickle
# import pandas as pd
# import requests
#
# def fetch_poster(movie_id):
#     response= requests.get('https://api.themoviedb.org/3/movie/{}?api_key=488dc5dfee0adba9d95f4443960e692b'.format(movie_id))
#     data= response.json()
#     print(data)
#     return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies=[]
#     recommended_movies_posters=[]
#
#     for i in movies_list:
#         movie_id=movies.iloc[i[0]].movie_id
#
#         recommended_movies.append(movies.iloc[i[0]].title)
#         #fetch poster from api
#         recommended_movies_posters.append(fetch_poster(movie_id))
#     return recommended_movies,recommended_movies_posters
#
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies= pd.DataFrame(movies_dict)
#
# similarity= pickle.load(open('similarity.pkl','rb'))
# st.title('Movie Recommender System')
# selected_movie_name= st.selectbox(
#  "How would you like to be contacted?",
# movies['title'].values)
#
# if st.button('Recommend'):
#     names,posters =recommend(selected_movie_name)
#
#     col1, col2, col3, col4, col5 =st.columns(5)
#     with col1:
#         st.header(names[0])
#         st.image(posters[0])
#     with col2:
#         st.header(names[1])
#         st.image(posters[1])
#     with col3:
#         st.header(names[2])
#         st.image(posters[2])
#     with col4:
#         st.header(names[3])
#         st.image(posters[3])
#     with col5:
#         st.header(names[4])
#         st.image(posters[4])
#     # for i in recommendations:
#     #  st.write(i)

     #2
# import streamlit as st
# import pickle
# import pandas as pd
# import requests
# import warnings
#
# warnings.filterwarnings('ignore')
#
# # ---------- Functions ----------
# def fetch_poster(movie_id):
#     try:
#         url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=488dc5dfee0adba9d95f4443960e692b"
#         response = requests.get(url)
#         data = response.json()
#         return "http://image.tmdb.org/t/p/w500/" + data['poster_path']
#     except:
#         return "https://via.placeholder.com/200x300?text=No+Image"
#
# def recommend(movie):
#     movie_index = movies[movies['title'] == movie].index[0]
#     distances = similarity[movie_index]
#     movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
#
#     recommended_movies = []
#     recommended_posters = []
#     for i in movies_list:
#         movie_id = movies.iloc[i[0]].movie_id
#         recommended_movies.append(movies.iloc[i[0]].title)
#         recommended_posters.append(fetch_poster(movie_id))
#     return recommended_movies, recommended_posters
#
# # ---------- Load Data ----------
# movies_dict = pickle.load(open('movie_dict.pkl','rb'))
# movies = pd.DataFrame(movies_dict)
# similarity = pickle.load(open('similarity.pkl','rb'))
#
# # ---------- UI ----------
# st.markdown("<h1 style='text-align: center; color: #6c63ff;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)
# selected_movie_name = st.selectbox("Select a movie you like:", movies['title'].values)
#
# if st.button('Recommend'):
#     names, posters = recommend(selected_movie_name)
#     cols = st.columns(5)
#     for i in range(5):
#         with cols[i]:
#             st.image(posters[i])
#             st.caption(names[i])
#
# # ---------- Footer ----------
# st.markdown("---")
# st.markdown("<p style='text-align: center; font-size: 14px;'>Made with ❤️ by Ashi Srivastava</p>", unsafe_allow_html=True)



import streamlit as st
import pickle
import pandas as pd
import requests
import warnings

warnings.filterwarnings('ignore')

# ---------------------------------------------
# Fetch movie details using TMDB API
def fetch_movie_data(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=488dc5dfee0adba9d95f4443960e692b"
        response = requests.get(url)
        data = response.json()

        poster_path = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        title = data['title']
        overview = data['overview']
        rating = data['vote_average']
        release_date = data['release_date']
        trailer_url = f"https://www.youtube.com/results?search_query={title.replace(' ', '+')}+trailer"

        return {
            'poster': poster_path,
            'title': title,
            'overview': overview,
            'rating': rating,
            'release_date': release_date,
            'trailer_url': trailer_url
        }
    except:
        return {
            'poster': "https://via.placeholder.com/200x300?text=No+Image",
            'title': "Unknown",
            'overview': "No info available.",
            'rating': "N/A",
            'release_date': "N/A",
            'trailer_url': "#"
        }

# ---------------------------------------------
# Recommend movies based on similarity
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    results = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        info = fetch_movie_data(movie_id)
        results.append(info)
    return results

# ---------------------------------------------
# Load Data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ---------------------------------------------
# 🌙 Dark Mode Toggle
dark_mode = st.toggle("🌙 Dark Mode", value=False)

# Inject dark/light CSS based on toggle
if dark_mode:
    st.markdown("""
        <style>
            body {
                background-color: #121212;
                color: #e0e0e0;
            }
            .stApp {
                background-color: #121212;
            }
            .stSelectbox, .stButton {
                background-color: #1f1f1f !important;
                color: white !important;
            }
            .css-1v0mbdj { color: white !important; }
        </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
        <style>
            body {
                background-color: white;
                color: black;
            }
            .stApp {
                background-color: white;
            }
        </style>
    """, unsafe_allow_html=True)

# UI
st.markdown("<h1 style='text-align: center; color: #6c63ff;'>🎬 Movie Recommender System</h1>", unsafe_allow_html=True)

selected_movie_name = st.selectbox("Select a movie you like:", movies['title'].values)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    cols = st.columns(5)
    for i in range(5):
        with cols[i]:
            st.image(recommendations[i]['poster'], use_container_width=True)
            st.markdown(f"**{recommendations[i]['title']}**", unsafe_allow_html=True)
            st.caption(f"⭐ {recommendations[i]['rating']} | 📅 {recommendations[i]['release_date']}")
            st.markdown(f"<small>{recommendations[i]['overview'][:200]}...</small>", unsafe_allow_html=True)
            st.markdown(f"[▶ Watch Trailer]({recommendations[i]['trailer_url']})", unsafe_allow_html=True)

# ---------------------------------------------
# Footer
st.markdown("---")
st.markdown("<p style='text-align: center; font-size: 14px;'>Made with ❤️ by Ashi Srivastava</p>", unsafe_allow_html=True)
