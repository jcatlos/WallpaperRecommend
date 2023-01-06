from apikey import API_KEY

import requests
import json
from typing import List, Dict
from pathlib import Path

def get_collections() -> Dict[str, str]:
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

    collections = {}                                            # Output list of collection tuples
    url = f'https://api.pexels.com/v1/collections/featured'     # First url to look at

    while True:

        # Fetch jpage of results
        page = request_page(url)

        # Process the results
        for collection in page['collections']:
            collections[collection['title']] = collection['id']

        # Handle last page 
        if 'next_page' not in page:
            break

        # Jump to next page of results
        url = page['next_page']

    return collections