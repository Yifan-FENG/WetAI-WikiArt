import requests, os


BASE_URL = "http://www.wikiart.org"
ENDPOINT = "/en/App/Painting/PaintingsByArtist"
ACCESS_KEY = ' ' # Please replace with your own access key
SECRET_KEY = ' '

def authenticate():
    """Authenticate with the WikiArt API and return a session key."""
    login_url = f"{BASE_URL}/en/Api/2/login"
    params = {
        'accessCode': ACCESS_KEY,
        'secretCode': SECRET_KEY,
    }
    response = requests.get(login_url, params=params)
    if response.status_code == 200:
        session_key = response.json().get('SessionKey')
        return session_key
    else:
        print(f"Failed to authenticate: {response.status_code}")
        return None

def get_artworks_by_artist(session_key, artist_url_name):
    """Fetch artworks for a specified artist from WikiArt using a session key."""
    url = f"{BASE_URL}{ENDPOINT}"
    headers = {
        'SessionKey': session_key
    }
    params = {
        'artistUrl': artist_url_name,
        'json': 2
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching artworks for {artist_url_name}: {response.status_code}")
        return None

def download_image(image_url, target_dir, image_title):
    """Download an image from a URL and save it to a specified directory."""
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    image_path = f"{target_dir}/{image_title}.jpg"
    response = requests.get(image_url)
    if response.status_code == 200:
        with open(image_path, 'wb') as f:
            f.write(response.content)
        print(f"Downloaded {image_path}")
    else:
        print(f"Failed to download image: {response.status_code}")

def main():
    session_key = authenticate()
    if session_key:
        artist_name = 'pierre-bonnard'
        target_dir = f'wikiart_images/{artist_name}'
        artworks = get_artworks_by_artist(session_key, artist_name)
        if artworks:
            for artwork in artworks:
                if 'image' in artwork:
                    image_url = artwork['image']
                    image_title = artwork['title'].replace('/', '_').replace(':', '_')
                    download_image(image_url, target_dir, image_title)

if __name__ == "__main__":
    main()
