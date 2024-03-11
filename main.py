import requests

api_url = "https://api.jikan.moe/v3"
search_endpoint = f"{api_url}/search/manga"


def search_manga(query, api_key):
    params = {"q": query, "api_key": api_key}
    response = requests.get(search_endpoint, params=params)

    if response.status_code == 200:
        return response.json()["results"]
    else:
        print(f"Error: {response.status_code}")
        return None


# Example usage:
api_key = "a044b8aedae39105b39e762df0b13409"
query = "One Piece"
results = search_manga(query, api_key)

if results:
    for result in results:
        print(result["title"])
# Future use with expanded features
# numerical_features = df[['score', 'members']]
# final_features = pd.concat([numerical_features, features], axis=1)