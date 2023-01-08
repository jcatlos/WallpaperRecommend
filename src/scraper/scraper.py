from apikey import API_KEY

import requests
from typing import List, Dict
from pathlib import Path

def sanitize_dirname(name:str) -> str:
    for c in r"#%&{}<>*/\\?$!\"':@=|`+":
        name =  name.replace(c, '')
    return name.strip()

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
                'type' : 'photos'
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


def download_collection(name: str, path: Path) -> None:
    image_collection = fetch_collection(name=name)

    for image_url in image_collection:
        filename = image_url.split('?')[0].split('/')[-1]
        image_data = requests.get(
            url = image_url,
            headers = {"Authorization":API_KEY}
        )
        with open(path/filename, 'wb') as image:
            image.write(image_data.content)
        

# main
if __name__ == '__main__':
    with open('index.txt', 'r', encoding='utf-8') as index:
        for row in index:
            # Extract id and name from the row - divided by the last semicolon
            id, name = row[::-1].split(':', 1)
            name = name[::-1].strip()
            id = id[::-1].strip()

            # Sanitize the folder name from forbidden characters
            name= sanitize_dirname(name)

            print(f"Downloading collection {name} ")

            path = Path(r'C:\Users\Jakub\Documents\CUNI\5\Multimedia retrieval\WallpaperRecommend\data\\'+name)
            
            if not path.exists():
                path.mkdir()
                download_collection(name=id, path=path)
