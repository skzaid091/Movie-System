import pickle
import streamlit as st
import pandas as pd
import requests
from os import path
import zipfile

st.set_page_config(layout='wide')
st.title('Movie Recommender System')


def fetch_api(movie_id):
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key='
                     '750553a5d65f40cd8cf97f9dc22952fe&language=en-US'.format(movie_id))
    data = r.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie_name, df, sl):
    top5_movies = []
    recommended_movie_posters = []
    movie_index = df[df['title'] == movie_name].index[0]
    distances = sl[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:5]
    for i in movie_list:
        top5_movies.append(df.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_api(df.iloc[i[0]].id))
    return top5_movies, recommended_movie_posters

hindi_movies = pd.read_pickle('hindi_movies.pkl')
hindi_movies = hindi_movies[['movie_id', 'title']]
movies_hindi = pd.DataFrame(hindi_movies)
movies_hindi.rename(columns={'movie_id': 'id'}, inplace=True)

movies_list = pd.read_pickle('movies.pkl')
movies_list = movies_list[['id', 'title']]
movies = pd.DataFrame(movies_list)

if path.exists('models/similarity.pkl'):
    similarity_list = pickle.load(open('models/similarity.pkl', 'rb'))
else:
    with zipfile.ZipFile("similar.zip","r") as zip_ref:
        zip_ref.extractall("models")
    similarity_list = pickle.load(open('models/similarity.pkl', 'rb'))
    
if path.exists('models/hindi_similarity.pkl'):
    hindi_similarity_list = pickle.load(open('models/hindi_similarity.pkl', 'rb'))
else:
    with zipfile.ZipFile("hindi_similarity.zip","r") as zip_ref:
        zip_ref.extractall("models")
    hindi_similarity_list = pickle.load(open('models/hindi_similarity.pkl', 'rb'))

en_hi = ['English', 'Hindi']
col11, col12, col13, col14 = st.columns(4)
with col11:
    select_language = st.selectbox('Select Movie Type', en_hi)
with col12:
    pass
with col13:
    pass
with col14:
    pass

if select_language == 'English':
    selected_movie_name = st.selectbox('Enter Movie Name', movies_list['title'])
    df = movies
    sl = similarity_list
if select_language == 'Hindi':
    selected_movie_name = st.selectbox('Enter Movie Name', hindi_movies['title'])
    df = movies_hindi
    sl = hindi_similarity_list

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name, df, sl)
    st.write('Movies')
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(posters[0])
        st.header(recommendations[0])
    with col2:
        st.image(posters[1])
        st.header(recommendations[1])
    with col3:
        st.image(posters[2])
        st.header(recommendations[2])
    with col4:
        st.image(posters[3])
        st.header(recommendations[3])
    with col5:
        st.image(posters[4])
        st.header(recommendations[4])
