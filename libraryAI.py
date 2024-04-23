import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from ast import literal_eval
import numpy as np
import math


def get_original_score(title):
    temp_df = pd.read_csv('manga.csv')
    queried_manga_details = temp_df[temp_df['title'].str.lower() == title].iloc[0]
    return queried_manga_details['score']


# Cargar datos desde un archivo CSV
def load_data(progress_bar=None):
    df = pd.read_csv('manga.csv')
    titles = df['title'].str.lower().tolist()
    # Actualizar barra de progreso al cargar datos
    if progress_bar:
        progress_bar.update(5)
    return df, titles


# Preprocesar los datos
def preprocess_data(df, progress_bar=None):
    df['genres'] = df['genres'].apply(literal_eval)
    df['themes'] = df['themes'].apply(literal_eval)
    df['demographics'] = df['demographics'].apply(literal_eval)
    df['score'] = df['score'].apply(lambda x: 0 if x is None else x)
    df['score'] = df['score'] / 10
    # Replace NaN values with 0
    df.fillna(0, inplace=True)
    # Actualizar barra de progreso después de preprocesar
    if progress_bar:
        progress_bar.update(25)
    return df


# Obtener los datos codificados
def get_encoded_data(df, progress_bar=None):
    genres_encoded = pd.get_dummies(df['genres'].str.join(',').str.get_dummies(sep=','))
    themes_encoded = pd.get_dummies(df['themes'].str.join(',').str.get_dummies(sep=','))
    demographics_encoded = pd.get_dummies(df['demographics'].str.join(',').str.get_dummies(sep=','))
    # Actualizar barra de progreso después de codificar
    if progress_bar:
        progress_bar.update(50)
    return genres_encoded, themes_encoded, demographics_encoded


# Concatenar características
def concatenate_features(score_reduced, genres_encoded, themes_encoded, demographics_encoded, progress_bar=None):
    features = pd.concat([score_reduced, genres_encoded, themes_encoded, demographics_encoded], axis=1)
    # Actualizar barra de progreso después de concatenar características
    if progress_bar:
        progress_bar.update(75)
    return features


# Convertir características a representación de matriz dispersa
def convert_to_sparse_matrix(features, progress_bar=None):
    sparse_features = csr_matrix(features)
    # Actualizar barra de progreso después de convertir características
    if progress_bar:
        progress_bar.update(100)
    return sparse_features


# Función para calcular la matriz de similitud con una barra de progreso
def calculate_similarity_matrix_with_progress(sparse_features, progress_bar=None, chunk_size=100):
    num_samples = sparse_features.shape[0]
    similarity_matrix = np.zeros((num_samples, num_samples))

    # Calcular la matriz de similitud por partes (chunk)
    for start_idx in range(0, num_samples, chunk_size):
        end_idx = min(start_idx + chunk_size, num_samples)

        # Calcular similitud para el bloque actual
        chunk_similarities = cosine_similarity(sparse_features[start_idx:end_idx], sparse_features)
        chunk_similarities[np.isnan(chunk_similarities)] = 0  # Replace NaN with 0
        similarity_matrix[start_idx:end_idx] = chunk_similarities

        # Actualizar la barra de progreso
        if progress_bar:
            progress = start_idx / num_samples * 100
            progress_bar.update(progress)

    # Actualizar la barra de progreso al 100% una vez que finaliza el cálculo
    if progress_bar:
        progress_bar.update(100)

    return similarity_matrix


# Función para obtener recomendaciones
def get_recommendations(title, similarity_matrix, titles, df, top_n=6):
    title = title.lower()
    if title in titles:
        idx = titles.index(title)
        df.loc[idx, "score"] = 1
        similarity_scores = similarity_matrix[idx]
        similar_indices = similarity_scores.argsort()[::-1][0:top_n]
        similar_manga_details = []
        for i in similar_indices:
            manga_details = {
                'Title': titles[i],
                'Score': 0 if math.isnan(get_original_score(titles[i])) else get_original_score(titles[i]),
                'Genres': df.loc[i, 'genres'],
                'Themes': df.loc[i, 'themes'],
                'Demographics': df.loc[i, 'demographics'],
                'Similarity': similarity_scores[i]
            }
            similar_manga_details.append(manga_details)
        return similar_manga_details
    else:
        return []


# Ejemplo de uso
def full_calc(title, progress_bar=None, progress_bar2=None):
    df, titles = load_data(progress_bar)
    df = preprocess_data(df, progress_bar)
    reduced_score = df["score"]
    genres_encoded, themes_encoded, demographics_encoded = get_encoded_data(df, progress_bar)
    features = concatenate_features(reduced_score, genres_encoded, themes_encoded, demographics_encoded, progress_bar)
    sparse_features = convert_to_sparse_matrix(features, progress_bar)
    similarity_matrix = calculate_similarity_matrix_with_progress(sparse_features, progress_bar2)

    recommended_manga = get_recommendations(title, similarity_matrix, titles, df)

    return recommended_manga, similarity_matrix, titles, df


def quick_calc(title, similarity_matrix, titles, df):
    recommended_manga = get_recommendations(title, similarity_matrix, titles, df)
    return recommended_manga
