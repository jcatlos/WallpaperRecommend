from apikey import API_KEY
from get_collections import get_collections

import requests
import urllib.request
import json
from typing import List, Dict
from pathlib import Path

destination = Path('data')

# get a Pexels collection by name
def fetch_collection(name: str) -> List[str]:

    # Helper method to get result from an url
    def request_page(url: str):
        return requests.get(
            url = url,
            headers = {"Authorization":API_KEY},
            params = {
                'per_page' : 80,
                'page' : 1,
                'type' : 'photo'
            }
        ).json()

    
    images = []                                             # Output list of photo links
    url = f'https://api.pexels.com/v1/collections/{name}'   # First url to look at

    # While there are pages to be processed
    while url != None:

        # Fetch jpage of results
        page = request_page(url)

        # Process the results
        for image in page['media']:
            images.append(image['src']['medium'])

        # Handle last page 
        if 'next_page' not in page:
            break

        # Jump to next page of results
        url = page['next_page']

    return images


def download_collection(name: str, path: Path):
    image_collection = fetch_collection(name=name)

    for image_url in image_collection:
        filename = image_url.split('?')[0].split('/')[-1]
        image_data = requests.get(
            url = image_url,
            headers = {"Authorization":API_KEY}
        )
        with open(path/filename, 'wb') as image:
            image.write(image_data.content)
        

for name, id in get_collections().items():
    print(f"Downloading collection {name} ")

    path = Path(r'C:\Users\Jakub\Documents\CUNI\5\Multimedia retrieval\WallpaperRecommend\data\\'+name)
    
    if not path.exists():
        path.mkdir()

    download_collection(name='id', path=path)
#print(fetch_collection(name='eulhibt'))