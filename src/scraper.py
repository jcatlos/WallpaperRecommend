from apikey import API_KEY

import requests
import json
from typing import List
from pathlib import Path

destination = Path('data')

# get a Pexels collection by name
def fetch_collection(name: str):

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
        ).content

    
    photos = []                                             # Output list of photo links
    url = f'https://api.pexels.com/v1/collections/{name}'   # First url to look at

    # While there are pages to be processed
    while url != None:

        # Fetch jpage of results
        page = request_page(url)
        print(page)

        # Process the results
        for photo in page['media']:
            photos.append(photo['src']['small'])

        # Jump to next page of results
        url = page['next_page']

    return photos
