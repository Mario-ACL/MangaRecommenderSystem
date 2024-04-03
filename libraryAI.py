import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix
from ast import literal_eval

# Load data from CSV
df = pd.read_csv('manga.csv')
titles = df['title'].tolist()

# Preprocess the data
df['genres'] = df['genres'].apply(literal_eval)
df['genres'] = df['genres'].apply(lambda x: 'NoGenres' if x is None else x)
df['themes'] = df['themes'].apply(literal_eval)
df['themes'] = df['themes'].apply(lambda x: 'NoThemes' if x is None else x)
df['demographics'] = df['demographics'].apply(literal_eval)
df['demographics'] = df['demographics'].apply(lambda x: 'NoDemographics' if x is None else x)

# Get the data
genres_encoded = pd.get_dummies(df['genres'].str.join(',').str.get_dummies(sep=','))
themes_encoded = pd.get_dummies(df['themes'].str.join(',').str.get_dummies(sep=','))
demographics_encoded = pd.get_dummies(df['demographics'].str.join(',').str.get_dummies(sep=','))

# Concatenate features
features = pd.concat([genres_encoded, themes_encoded, demographics_encoded], axis=1)

# Convert features to sparse matrix representation
sparse_features = csr_matrix(features)

# Calculate cosine similarity matrix
similarity_matrix = cosine_similarity(sparse_features, sparse_features)


# Recommendation Generation
def get_recommendations(title, top_n=5):
    idx = titles.index(title)
    similarity_scores = similarity_matrix[idx]
    similar_indices = similarity_scores.argsort()[::-1][1:top_n + 1]
    similar_manga = [titles[i] for i in similar_indices]
    return similar_manga


# Example usage
query_title = 'Boku no Hero Academia'
recommended_manga = get_recommendations(query_title)
print("Recommended manga for '{}' are:".format(query_title))
for manga in recommended_manga:
    print(manga)
