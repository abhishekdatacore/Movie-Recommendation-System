import streamlit as st
import pickle
import pandas as pd
import requests
import time


session = requests.Session()
session.headers.update({"User-Agent":"MovieApp/1.0"})

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}"
    params = {
        "api_key": "04049895cbd96a98d29db4f1e2a85566",
        "language": "en-US"
    }

    for attempt in range(3):
        try:
            response = session.get(url, params=params, timeout=10)
            response.raise_for_status()
            data = response.json()
            poster_path = data.get('poster_path', None)
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        except requests.exceptions.RequestException:
            if attempt < 2:
                time.sleep(1)
                continue
            raise


def recommend(movie):
    movie_index=movies[movies['title']==movie].index[0]
    distances = similarity[movie_index]
    movie_list=sorted(list(enumerate(distances)),reverse =True, key = lambda x :x[1])[1:6]


    recommended_movies = []
    recommended_movies_posters = []
    for i in movie_list:
        movie_id= movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movies_posters


movie_dict=pickle.load(open('movie_dict.pkl', 'rb'))
movies=pd.DataFrame(movie_dict)

similarity =pickle.load(open('similarity.pkl','rb'))


st.title('MOVIE RECOMMENDATION SYSTEM')

selected_movie_name = st.selectbox(('Enter movie name ?'),movies['title'].values)

if st.button ('Recommend'):
    names,posters = recommend(selected_movie_name)


    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])
