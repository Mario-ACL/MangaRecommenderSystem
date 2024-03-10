import pandas as pd
import ast  # Module for literal string evaluation

# Load data from CSV
mangadata = pd.read_csv("manga.csv")


# Feature extractor
def extract_features(manga_title):
    # Features
    genres = {'Action', 'Adventure', 'Avant Garde', 'Award Winning', 'Boys Love',
              'Comedy', 'Drama', 'Fantasy', 'Girls Love', 'Gourmet', 'Horror',
              'Mystery', 'Romance', 'Sci-Fi', 'Slice of Life', 'Sports',
              'Supernatural', 'Suspense'}
    themes = {'Adult Cast', 'Anthropomorphic', 'CGDCT', 'Childcare', 'Combat Sports',
              'Crossdressing', 'Delinquents', 'Detective', 'Educational', 'Gag Humor',
              'Gore', 'Harem', 'High Stakes Game', 'Historical', 'Idols (Female)',
              'Idols (Male)', 'Isekai', 'Iyashikei', 'Love Polygon', 'Magical Sex Shift',
              'Mahou Shoujo', 'Martial Arts', 'Mecha', 'Medical', 'Military', 'Music',
              'Mythology', 'Organized Crime', 'Otaku Culture', 'Parody', 'Performing Arts',
              'Pets', 'Psychological', 'Racing', 'Reincarnation', 'Reverse Harem', 'Romantic Subtext'
                                                                                   'Samurai', 'School', 'Showbiz',
              'Space', 'Strategy Game', 'Super Power', 'Survival',
              'Team Sports', 'Time Travel', 'Vampire', 'Video Game', 'Visual Arts', 'Workplace'}
    demographics = {'Josei', 'Kids', 'Seinen', 'Shoujo', 'Shounen'}

    manga = mangadata[mangadata['title'] == manga_title].iloc[0]  # Find manga with the given title

    features = {}

    # Process Text Features
    features['title'] = manga['title']
    features['genres'] = [genre for genre in manga['genres'].strip("[]'").split("', '") if genre in genres]
    features['themes'] = [theme for theme in manga['themes'].strip("[]'").split("', '") if theme in themes]
    features['demographics'] = [demo for demo in manga['demographics'].strip("[]'").split("', '") if
                                demo in demographics]

    # Convert string representation of authors to dictionaries
    authors_list = ast.literal_eval(manga['authors'])
    features['authors'] = [author['first_name'] + ' ' + author['last_name'] for author in authors_list]

    features['synopsis'] = manga['synopsis']

    # Process Numbers Features
    features['score'] = float(manga['score'])
    features['members'] = int(manga['members'])

    return features


# Example usage
manga_title = "Berserk"
extracted_features = extract_features(manga_title)
print(extracted_features)
