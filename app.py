import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import film_utils
import series_utils
import data


df_movies = data.load_data("https://raw.githubusercontent.com/Marietou12/MatchMyStream/refs/heads/main/df_films.csv", index_col=None)
df_series = data.load_data("https://raw.githubusercontent.com/Marietou12/MatchMyStream/refs/heads/main/df_series.csv")

def background():
    st.markdown("""
    <style>
    /* Fond global pour l'application */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Marietou12/MatchMyStream/main/poster_film.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ciblage des widgets (conteneur principal) */
    div.block-container {
        background: rgba(0, 0, 0, 0.85); /* Transparence blanche */
        border-radius: 15px; /* Coins arrondis */
        padding: 20px; /* Espacement interne */
                }
                
    div.data-v-5af006b8{
                 border-radius: 15px;
                }
     }
    </style>
    """, unsafe_allow_html=True)
def background_series():
    st.markdown("""
    <style>
    /* Fond global pour l'application */
    .stApp {
        background-image: url("https://raw.githubusercontent.com/Marietou12/MatchMyStream/main/poster_series.jpg");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }

    /* Ciblage des widgets (conteneur principal) */
    div.block-container {
        background: rgba(0, 0, 0, 0.85); /* Transparence blanche */
        border-radius: 15px; /* Coins arrondis */
        padding: 20px; /* Espacement interne */
                }
                
    div.data-v-5af006b8{
                 border-radius: 15px;
                }
     }
    </style>
    """, unsafe_allow_html=True)
def center_content():
    st.markdown("""
    <style>
    .main {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100%;
        text-align: center;
    }
    </style>
    """, unsafe_allow_html=True)

st.set_page_config(
    page_title="MatchMyStream",
    page_icon="🍿",
    layout="centered",
    initial_sidebar_state="expanded"
)

if 'viewed_movies' not in st.session_state:
    st.session_state['viewed_movies'] = []

if 'viewed_series' not in st.session_state:
    st.session_state['viewed_series'] = []

background()

center_content()
st.markdown("""
    <style>
        /* Cibler les onglets spécifiquement dans Streamlit */
        .streamlit-expanderHeader, .css-1d391kg {
            font-size: 45px !important;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

# Ajout d'onglets pour basculer entre les films et les séries
tab1, tab2 = st.tabs(["🎥 Films", "📺 Séries"])

# Menu de navigation
with st.sidebar:
    selection = option_menu(
        menu_title="Menu",  # Titre du menu dans la sidebar
        options=["Accueil", "Recommendation par envies","Top 10","Ma liste","Déconnexion"],
        icons=["house-door", "film","bar-chart","clipboard2-check","power"],
        default_index=0,
        orientation="vertical",  # Menu vertical
        styles={
            "background-color" : "#000000",
            "container": {"padding": "5px"},
            "icon": {"font-size": "20px", "color": "#ffffff"},
            "nav-link": {
                "font-size": "16px", 
                "text-align": "left", 
                "margin": "10px", 
                "--hover-color": "#ff4242"
            },
            "nav-link-selected": {"background-color": "#7b0000"}
        }
    )
with tab1:
        
    if selection == "Accueil":
        st.title("Bienvenue sur MatchMyStream !")
        st.markdown("#### L'IA au service de vos soirées chill !")

        query = st.text_input("Recommandation pas titre, personne ou genre",key='queury film') 
        


        if query:
            
            results = film_utils.recommend_movies_keyword(df_movies, query, n_neighbors=10, threshold_distance=0.9, stopwords=None)
            
            if results:
                film_utils.afficher_films(results)
            else:
                st.write("Aucun film trouvé, veuillez écrire d'autres mots-clés.")
                
        st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
        # Interface Streamlit
        st.markdown("#### 🎬 À la recherche d'un film ? Laissez le hasard guider vos choix !")

        # Sélection du genre
        genres = ["Tous", "Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "War", "Western"]
        selected_genre = st.selectbox("📌 Choisissez un genre :", genres)

        if "selected_genre" not in st.session_state or st.session_state["selected_genre"] != selected_genre:
            st.session_state["random_movies"] = film_utils.get_random_movies(df_movies, selected_genre)
            st.session_state["selected_genre"] = selected_genre

        random_movies = st.session_state["random_movies"]

        if st.button("🔄 Changer les films"):
            st.session_state["random_movies"] = film_utils.get_random_movies(df_movies, selected_genre)

        num_lines = 3
        films_per_line = 4
        for i in range(num_lines):
            cols = st.columns(films_per_line) 
            for j, (_, row) in enumerate(random_movies.iloc[i * films_per_line:(i + 1) * films_per_line].iterrows()):
                with cols[j]: 
                    
                    tooltip_html = f"""
                    <div class="tooltip" style="text-align: center; position: relative; display: inline-block;">
                        <img src="{row['poster_path']}" alt="{row['title_y']}" style="width: 80%; border-radius: 8px; cursor: pointer;">
                        <span class="tooltiptext">{row['overview']}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 16px; color: white; text-align: center;">
                        <strong>{row['title_y']}</strong>
                    </div>
                    <div style="margin-top: 5px; font-size: 16px; color: white; text-align: center;">
                        <strong>Note: </strong>{row['averageRating']} / 10
                    </div>
                    <style>
                        .tooltip {{
                            position: relative;
                            display: inline-block;
                        }}
                        .tooltip .tooltiptext {{
                            visibility: hidden;
                            width: 250px;
                            background-color: rgba(0, 0, 0, 0.8);
                            color: #fff;
                            text-align: center;
                            border-radius: 5px;
                            padding: 10px;
                            position: absolute;
                            z-index: 1;
                            left: 100%;  /* Placer le tooltip à droite de l'image */
                            top: 50%;  /* Centrer le tooltip verticalement par rapport à l'image */
                            margin-left: 10px;  /* Espace entre l'image et le résumé */
                            transform: translateY(-50%);  /* Centrer le résumé verticalement par rapport à l'image */
                            opacity: 0;
                            transition: opacity 0.3s;  /* Animation pour un effet plus fluide */
                        }}
                        .tooltip:hover .tooltiptext {{
                            visibility: visible;
                            opacity: 1;  /* Rendre le tooltip visible au survol */
                        }}
                    </style>
                    """
                    
                    st.markdown(tooltip_html, unsafe_allow_html=True)

            # Ajouter un trait de séparation entre les lignes (sauf après la dernière ligne)
            if i < num_lines - 1:
                st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)

    elif selection == "Recommendation par envies":
        st.title("Recommandation de films selon vos envies")

        sentiment_to_genres = {
            "Excité": ["Action", "Adventure", "Science Fiction", "Mystery", "War"],
            "Curieux": ["Documentary", "Science Fiction", "Talk"],
            "Nostalgique": ["Comedy", "Drama", "Fantasy","History", "Western"],
            "Relaxé": ["Comedy", "Family", "Talk", "Music"],
            "Anxieux": ["Crime", "Mystery", "Thriller", "Horror"],
            "Romantique": ["Comedy", "Drama", "Romance", "Family"],
            "Émerveillé": ["Animation", "Science Fiction", "Action", "Family"]
        }

        # Options pour le choix des sentiments
        options = [
            "Excité", "Curieux", "Nostalgique", 
            "Relaxé", "Anxieux", "Romantique", "Émerveillé"
        ]


        selected_sentiment = st.pills("Sélectionnez votre humeur :", options=options, selection_mode="single", key="sentiment_pills_movies")

        st.markdown(f"Votre humeur sélectionnée : {selected_sentiment}.")

        # Sélectionner une plage d'années avec un select_slider
        selected_years = st.select_slider(
            "📅 Sélectionnez une plage d'années :",
            options=[str(year) for year in range(2000, 2025)],
            value=("2015", "2020")
        )

        start_year, end_year = map(int, selected_years)

        # Filtrer les films selon l'humeur et la plage d'années
        recommended_genres = sentiment_to_genres.get(selected_sentiment, [])
        filtered_movies = df_movies[
            (df_movies["startYear"] >= start_year) & 
            (df_movies["startYear"] <= end_year) & 
            df_movies["genres_x"].apply(lambda x: any(genre in x for genre in recommended_genres))  # Filtrage par genre
        ]

        # Initialiser le compteur dans session_state
        if "movies_offset" not in st.session_state:
            st.session_state.movies_offset = 0

        # Limite initiale de 5 films à afficher
        num_results = 5

        # Extraire les films à afficher
        displayed_movies = filtered_movies.iloc[st.session_state.movies_offset: st.session_state.movies_offset + num_results]

        # Afficher les films
        if not displayed_movies.empty:
            st.write(f"Voici les films recommandés pour votre humeur **{selected_sentiment}** :")
            
            for _, movie in displayed_movies.iterrows():
                col1, col2 = st.columns([1, 3])  # Crée deux colonnes, l'une pour l'image et l'autre pour le texte
                
                # Affichage de l'image dans la première colonne
                with col1:
                    st.image(movie['poster_path'], width=100)  # Remplacez 'poster_path' par l'URL de l'image
                
                # Affichage des détails du film dans la deuxième colonne
                with col2:
                    st.write(f"🎬 Film recommandé : **{movie['title_y']}**")
                    st.write(f"⭐ Note : {movie['averageRating']}/10")
                    st.write(f"📅 Année : {movie['startYear']}")
                    st.write(f"📝 Résumé : {movie['overview']}")
                    st.write("🎥 Type : Film")
                
                # Affichage d'un trait de séparation après chaque film
                st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
            
            # Ajouter un bouton "Voir plus"
            if len(filtered_movies) > st.session_state.movies_offset + num_results:
                if st.button("Voir plus"):
                    # Si le bouton "Voir plus" est cliqué, augmenter le compteur
                    st.session_state.movies_offset += num_results

        else:
            st.write("Aucun film ne correspond à vos critères.")

    elif selection == "Top 10":
        st.title("Top 10 des meilleurs films")
        st.subheader("Choisissez un genre pour découvrir les meilleurs films du genre")

        # Liste des genres
        genres = ["Action", "Adventure", "Animation", "Comedy", "Crime", "Drama", "Fantasy", "History", "Horror", "Music", "Mystery", "Romance", "Science Fiction", "Thriller", "War", "Western"]

        # Sélection du genre avec st.selectbox (ou st.radio si vous préférez)
        genre = st.pills("Choisissez un genre", options=genres)
        if genre:
        # Appeler la fonction pour filtrer et obtenir les films
            results = film_utils.top_10(df_movies, genre)
            # Vérifier si des films sont trouvés et les afficher
            film_utils.afficher_films(results)
        else:
            st.write("Veuillez sélectionner un genre pour voir les recommandations.")

    elif selection == "Ma liste":
        # Affichage des films vus
        st.title("Films à voir")
        
        # Si la liste des films vus contient des films
        film_utils.afficher_ma_liste(df_movies)

    elif selection == "Déconnexion":
        st.write("Vous êtes déconnecté.")

with tab2:
    background_series()
    if selection == "Accueil":
        st.title("Bienvenue sur MatchMyStream !")
        st.markdown("#### L'IA au service de vos soirées chill !")       


        query = st.text_input("Recommandation pas titre, personne ou genre", key='queury series')  # Ajout d'une clé unique
        if query:
            # Appeler la fonction de recommandation avec les mots-clés et les données des films
            results = series_utils.recommend_series_keyword(df_series, query, n_neighbors=10, threshold_distance=0.9, stopwords=None)
            # Appeler la fonction d'affichage de films
            if results:
                series_utils.afficher_series(results)
            else:
                st.write("Aucune série trouvée, veuillez écrire d'autres mots-clés.")
                
        st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
        # Interface Streamlit
        st.markdown("#### 🎬 À la recherche d'une série ? Laissez le hasard guider vos choix !")

        genres = ["Tous", 'Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids', 'Mystère', 'Reality', 'Science-Fiction & Fantastique', 'Soap', 'Talk', 'War & Politics', 'Western']
        selected_genre = st.selectbox("📌 Choisissez un genre :", genres)

        # Initialiser ou mettre à jour la session pour recharger les séries en fonction du genre sélectionné
        if "selected_genre" not in st.session_state or st.session_state["selected_genre"] != selected_genre:
            st.session_state["random_series"] = series_utils.get_random_series(df_series, selected_genre)
            st.session_state["selected_genre"] = selected_genre

        # Vérifier si "random_series" est dans session_state avant de l'utiliser
        if "random_series" in st.session_state:
            random_series = st.session_state["random_series"]
        else:
            random_series = pd.DataFrame()  # ou une autre valeur par défaut si la clé n'existe pas encore

        # Bouton pour recharger les séries
        if st.button("🔄 Changer les séries"):
            st.session_state["random_series"] = series_utils.get_random_series(df_series, selected_genre)

        # Disposition en lignes de 4 séries (3 lignes)
        num_lines = 3
        series_per_line = 4

        for i in range(num_lines):
            cols = st.columns(series_per_line)  # Crée 4 colonnes par ligne
            for j, (_, row) in enumerate(random_series.iloc[i * series_per_line:(i + 1) * series_per_line].iterrows()):
                with cols[j]:  # Afficher chaque série dans une colonne
                    tooltip_html = f"""
                    <div class="tooltip" style="text-align: center; position: relative; display: inline-block;">
                        <img src="{row['poster_path']}" alt="{row['name']}" style="width: 80%; border-radius: 8px; cursor: pointer;">
                        <span class="tooltiptext">{row['overview']}</span>
                    </div>
                    <div style="margin-top: 10px; font-size: 16px; color: white; text-align: center;">
                        <strong>{row['name']}</strong>
                    </div>
                    <div style="margin-top: 5px; font-size: 16px; color: white; text-align: center;">
                        <strong>Note: </strong>{row['averageRating']} / 10
                    </div>
                    <div style="margin-top: 5px; font-size: 16px; color: white; text-align: center;">
                        <strong>Saisons: </strong>{row['number_of_seasons']}  <!-- Ajout du nombre de saisons -->
                    </div>
                    <style>
                        .tooltip {{
                            position: relative;
                            display: inline-block;
                        }}
                        .tooltip .tooltiptext {{
                            visibility: hidden;
                            width: 250px;
                            background-color: rgba(0, 0, 0, 0.8);
                            color: #fff;
                            text-align: center;
                            border-radius: 5px;
                            padding: 10px;
                            position: absolute;
                            z-index: 1;
                            left: 100%;  /* Placer le tooltip à droite de l'image */
                            top: 50%;  /* Centrer le tooltip verticalement par rapport à l'image */
                            margin-left: 10px;  /* Espace entre l'image et le résumé */
                            transform: translateY(-50%);  /* Centrer le résumé verticalement par rapport à l'image */
                            opacity: 0;
                            transition: opacity 0.3s;  /* Animation pour un effet plus fluide */
                        }}
                        .tooltip:hover .tooltiptext {{
                            visibility: visible;
                            opacity: 1;  /* Rendre le tooltip visible au survol */
                        }}
                    </style>
                    """
                    
                    # Afficher le HTML pour chaque série
                    st.markdown(tooltip_html, unsafe_allow_html=True)

            # Ajouter un trait de séparation entre les lignes (sauf après la dernière ligne)
            if i < num_lines - 1:
                st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)


    elif selection == "Recommendation par envies":
        st.title("Recommandation de series selon vos envies")



# Sentiments et genres associés
        sentiment_to_genres = {
            "Excité": ["Action & Adventure", "Science-Fiction & Fantastique", "Mystère", "War & Politics"],
            "Fatigué": ["Drame", "Comédie", "Reality", "Soap"],
            "Curieux": ["Documentaire", "Talk"],
            "Nostalgique": ["Comédie", "Drame", "Familial", "Western"],
            "Relaxé": ["Comédie", "Familial", "Talk", "Reality"],
            "Anxieux": ["Crime", "Mystère", "Thriller", "Horror"],
            "Romantique": ["Comédie", "Drame", "Romance"],
            "Émerveillé": ["Animation", "Science-Fiction & Fantastique", "Action & Adventure", "Familial"]
        }

        # Options pour le choix des sentiments
        options = [
            "Excité", "Fatigué", "Curieux", "Nostalgique", 
            "Relaxé", "Anxieux", "Romantique", "Émerveillé"
        ]

        # Choisir l'humeur via st.pills avec un key unique
        selected_sentiment = st.pills("Sélectionnez votre humeur :", options=options, selection_mode="single", key="sentiment_pills_series")

        st.markdown(f"Votre humeur sélectionnée : {selected_sentiment}.")

        # Sélectionner une plage d'années avec un select_slider
        selected_years = st.select_slider(
            "📅 Sélectionnez une plage d'années :",
            options=[str(year) for year in range(1990, 2026)],
            value=("2000", "2020")
        )

        start_year, end_year = map(int, selected_years)

        min_seasons = int(df_series['number_of_seasons'].min())
        max_seasons = int(df_series['number_of_seasons'].max())

        selected_seasons = st.slider(
            "📅 Sélectionnez le nombre de saisons souhaité :",
            min_value=min_seasons,
            max_value=max_seasons,
            value=(min_seasons, max_seasons),  
            step=1
        )

        min_seasons, max_seasons = selected_seasons

        # Filtrer les séries selon l'humeur, la plage d'années et le nombre de saisons
        recommended_genres = sentiment_to_genres.get(selected_sentiment, [])
        filtered_series = df_series[
            (df_series["startYear"] >= start_year) & 
            (df_series["startYear"] <= end_year) & 
            df_series["genres"].apply(lambda x: any(genre in x for genre in recommended_genres)) &
            (df_series["number_of_seasons"] >= min_seasons) & 
            (df_series["number_of_seasons"] <= max_seasons)
        ]

        # Initialiser le compteur dans session_state
        if "series_offset" not in st.session_state:
            st.session_state.series_offset = 0

        # Limite initiale de 5 séries à afficher
        num_results = 5

        # Extraire les séries à afficher
        displayed_series = filtered_series.iloc[st.session_state.series_offset: st.session_state.series_offset + num_results]

        # Afficher les séries
        if not displayed_series.empty:
            st.write(f"Voici les séries recommandées pour votre humeur **{selected_sentiment}** :")
            
            for _, series in displayed_series.iterrows():
                col1, col2 = st.columns([1, 3])  # Crée deux colonnes, l'une pour l'image et l'autre pour le texte
                
                # Affichage de l'image dans la première colonne
                with col1:
                    st.image(series['poster_path'], width=100)  # Remplacez 'poster_path' par l'URL de l'image
                
                # Affichage des détails de la série dans la deuxième colonne
                with col2:
                    st.write(f"🎬 Série recommandée : **{series['name']}**")
                    st.write(f"⭐ Note : {series['averageRating']}/10")
                    st.write(f"📅 Année : {series['startYear']}")
                    st.write(f"📝 Résumé : {series['overview']}")
                    st.write(f"📺 Nombre de saisons : {series['number_of_seasons']}")
                
                # Affichage d'un trait de séparation après chaque série
                st.markdown("<hr style='border: 1px solid #444;'>", unsafe_allow_html=True)
            
            # Ajouter un bouton "Voir plus"
            if len(filtered_series) > st.session_state.series_offset + num_results:
                if st.button("Voir plus"):
                    # Si le bouton "Voir plus" est cliqué, augmenter le compteur
                    st.session_state.series_offset += num_results

        else:
            st.write("Aucune série ne correspond à vos critères.")


    elif selection == "Top 10":
        st.title("Top 10 des meilleurs séries")
        st.subheader("Choisissez un genre pour découvrir les meilleurs séries du genre")

        # Liste des genres
        genres = ['Action & Adventure', 'Animation', 'Comédie', 'Crime', 'Documentaire', 'Drame', 'Familial', 'Kids', 'Mystère', 'Reality', 'Science-Fiction & Fantastique', 'Soap', 'Talk', 'War & Politics', 'Western']

        # Sélection du genre avec st.selectbox (ou st.radio si vous préférez)
        genre = st.pills("Choisissez un genre", options=genres,key='series')
        if genre:
        # Appeler la fonction pour filtrer et obtenir les séries
            results = series_utils.top_10(df_series, genre)
            # Vérifier si des séries sont trouvés et les afficher
            series_utils.afficher_series(results)
        else:
            st.write("Veuillez sélectionner un genre pour voir les recommandations.")

    elif selection == "Ma liste":
        # Affichage des séries vus
        st.title("Séries dans votre liste")
        
        # Si la liste des séries vus contient des séries
        series_utils.afficher_ma_liste(df_series)
