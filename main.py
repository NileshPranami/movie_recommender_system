import streamlit as st
import pickle
import pandas as pd
import requests


def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=c5dfb38403e1827b05d5dad990c613c6&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/"+data['poster_path']


def recommend(movie,movies_d):
    movie_index = movies_d[movies_d['title']==movie].index[0]
    distances = similarity[movie_index]
    final_list = sorted(list(enumerate(distances)),reverse = True,key = lambda x:x[1])[1:6]
    recommend_movie = []
    recommended_poster = []
    for i in final_list:
        movie_id = movies_d.iloc[i[0]].movie_id
        recommend_movie.append(movies_d.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommend_movie,recommended_poster

movies_l = pickle.load(open('movies_dict.pkl','rb'))
movies_df = pd.DataFrame(movies_l)

similarity = pickle.load(open('vector.pkl','rb'))


st.title('Movie Recommender System')
movie_name = st.selectbox(
    'Please select movie to recommend',
    movies_df['title'].values
)
if st.button('Recommend'):
    recommendations,poster = recommend(movie_name,movies_df)
    # for i,mov in enumerate(recommendations):
    col = st.columns(5)
    for i,c in enumerate(col):
        with c:
            st.text(recommendations[i])
            st.image(poster[i])
