import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
df = pd.read_csv('manga.csv')

# Replace NaN with an empty string
df['genres'] = df['genres'].fillna('')

# Create a TfidfVectorizer and Remove stopwords
tfidf = TfidfVectorizer(stop_words='english')# Fit and transform the data to a tfidf matrix
tfidf_matrix = tfidf.fit_transform(df['title'])# Print the shape of the tfidf_matrix
print(tfidf_matrix.shape)

# Compute the cosine similarity between each movie description
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

indices = pd.Series(df.index, index=df['title']).drop_duplicates()


def get_recommendations(title, cosine_sim=cosine_sim, num_recommend = 10):
    idx = indices[title]# Get the pairwsie similarity scores of all manga with that manga
    sim_scores = list(enumerate(cosine_sim[idx]))# Sort the manga based on the similarity scores
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)# Get the scores of the 10 most similar manga
    top_similar = sim_scores[1:num_recommend+1]# Get the manga indices
    manga_indices = [i[0] for i in top_similar]# Return the top 10 most similar manga
    return df['title'].iloc[manga_indices]


print(get_recommendations('Berserk', num_recommend = 10))