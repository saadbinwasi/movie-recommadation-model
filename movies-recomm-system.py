import streamlit as st
import pickle
import requests


movies_list = pickle.load(open('movies.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))


def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=41daead5bc32cd6eaef3240f1f08d145&language=en-US')
        response.raise_for_status()
        data = response.json()
        return "https://image.tmdb.org/t/p/w500/" + data.get('poster_path', '')  # Safe access
    except:
        return None  # Return None if poster not found


def recommend(movie):
    movie_index = movies_list[movies_list['title'] == movie].index[0]
    distances = similarity[movie_index]
    
    similar_movies = sorted(list(enumerate(distances)),reverse=True,key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_poster = []
    for i in similar_movies:
        movie_id = movies_list.iloc[i[0]].movie_id
        # fetch poster 
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_poster.append(fetch_poster(movie_id))
    return recommended_movies,recommended_poster


st.title('🎬 Movie Recommender System')

# Display a dropdown to select a movie
selected_movie = st.selectbox(
    'Select a movie you like:',  # Better prompt
    movies_list['title'].values,index=None
)

if st.button('Recommend') and selected_movie:
    names, posters = recommend(selected_movie)
    
    if names:  # Only show if we got recommendations
        cols = st.columns(5)  # Use st.columns() instead of st.beta_columns()
        for i in range(min(5, len(names))):  # Safe display for <5 recommendations
            with cols[i]:
               
                if posters[i]:  # Only show if poster exists
                    st.image(posters[i], width=700)
                else:
                    st.warning("Poster unavailable")
                st.subheader(names[i])
    else:
        st.warning("No recommendations available")


