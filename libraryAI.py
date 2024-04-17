import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from ast import literal_eval
import numpy as np


# Cargar datos desde un archivo CSV
def load_data(progress_bar=None):
    df = pd.read_csv('manga.csv')
    titles = df['title'].tolist()
    # Actualizar barra de progreso al cargar datos
    if progress_bar:
        progress_bar.update(5)
    return df, titles


# Preprocesar los datos
def preprocess_data(df, progress_bar=None):
    df['genres'] = df['genres'].apply(literal_eval)
    df['genres'] = df['genres'].apply(lambda x: 'NoGenres' if x is None else x)
    df['themes'] = df['themes'].apply(literal_eval)
    df['themes'] = df['themes'].apply(lambda x: 'NoThemes' if x is None else x)
    df['demographics'] = df['demographics'].apply(literal_eval)
    df['demographics'] = df['demographics'].apply(lambda x: 'NoDemographics' if x is None else x)
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
def concatenate_features(genres_encoded, themes_encoded, demographics_encoded, progress_bar=None):
    features = pd.concat([genres_encoded, themes_encoded, demographics_encoded], axis=1)
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
def get_recommendations(title, similarity_matrix, titles, top_n=5):
    idx = titles.index(title)
    similarity_scores = similarity_matrix[idx]
    similar_indices = similarity_scores.argsort()[::-1][1:top_n + 1]
    similar_manga = [titles[i] for i in similar_indices]
    return similar_manga


# Ejemplo de uso
def main(progress_bar=None):
    df, titles = load_data(progress_bar)
    df = preprocess_data(df, progress_bar)
    genres_encoded, themes_encoded, demographics_encoded = get_encoded_data(df, progress_bar)
    features = concatenate_features(genres_encoded, themes_encoded, demographics_encoded, progress_bar)
    sparse_features = convert_to_sparse_matrix(features, progress_bar)
    similarity_matrix = calculate_similarity_matrix_with_progress(sparse_features, progress_bar)

    query_title = 'Boku no Hero Academia'
    recommended_manga = get_recommendations(query_title, similarity_matrix, titles)

    print("Recommended manga for '{}' are:".format(query_title))
    for manga in recommended_manga:
        print(manga)


if __name__ == "__main__":
    main()
