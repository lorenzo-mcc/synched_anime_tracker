import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
access_token = os.getenv('ACCESS_TOKEN')

def fetch_anime_info(title):
    """
    Fetches anime information from AniList using the provided title.
    """
    api_url = "https://graphql.anilist.co"
    query = '''
    query ($search: String) {
      Page(page: 1, perPage: 10) {
        media(search: $search, type: ANIME) {
          title {
            english
            romaji
          }
          countryOfOrigin
          status
          format
          genres
          coverImage {
            extraLarge
          }
          bannerImage
          startDate {
            year
          }
          airingSchedule{
            nodes {
              episode
              timeUntilAiring
            }
          }
          studios {
            edges {
              node {
                name
                isAnimationStudio
              }
            }
          }
        }
      }
    }
    '''
    variables = {"search": title}
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }

    response = requests.post(api_url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json().get('data', {}).get('Page', {}).get('media', [])
        if not data:
            print(f"Error: No results found for '{title}'.")
            return None
        return data
    else:
        print(f"Error {response.status_code}: {response.text}")
        return None
