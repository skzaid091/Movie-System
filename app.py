import pickle
import streamlit as st
import pandas as pd
import requests

st.set_page_config(layout='wide')
st.title('Movie Recommender System')


def fetch_api(movie_id):
    r = requests.get('https://api.themoviedb.org/3/movie/{}?api_key='
                     '750553a5d65f40cd8cf97f9dc22952fe&language=en-US'.format(movie_id))
    data = r.json()
    return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie_name):
    top5_movies = []
    recommended_movie_posters = []
    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity_list[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[0:5]
    for i in movie_list:
        top5_movies.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_api(movies.iloc[i[0]].id))
    return top5_movies, recommended_movie_posters


movies_list = pickle.load(open('movies.pkl', 'rb'))
movies_list = movies_list[['id', 'title']]
movies = pd.DataFrame(movies_list)

similarity_list = pickle.load(open('similarity.pkl', 'rb'))

selected_movie_name = st.selectbox('Enter Movie Name', movies_list['title'])

if st.button('Recommend'):
    recommendations, posters = recommend(selected_movie_name)
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

    # col6, col7, col8, col9, col10 = st.columns(5)
    # with col6:
    #     st.image(posters[5])
    #     st.header(recommendations[5])
    # with col7:
    #     st.image(posters[6])
    #     st.header(recommendations[6])
    # with col8:
    #     st.image(posters[7])
    #     st.header(recommendations[7])
    # with col9:
    #     st.image(posters[8])
    #     st.header(recommendations[8])
    # with col10:
    #     st.image(posters[9])
    #     st.header(recommendations[9])
