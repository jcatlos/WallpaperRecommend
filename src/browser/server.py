from load_data import load_data
from PIL import ImageColor
from pathlib import Path
import pandas as pd
from construct_results import construct_result_page
from urllib.parse import urlparse, parse_qs

from querying import *

import http.server
import socketserver

PORT = 8000

class CustomHttpRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def __init__(self, *args):
        self.images = load_data()
        self.images['pallette_path'] = 'palletes/' + self.images['name']

        image_names = pd.DataFrame(data = Path('wallpapers').glob('*/*'), columns=["image_path"])
        image_names['name'] = image_names['image_path'].apply(lambda x: x.name)
        self.images = self.images.set_index('name').join(image_names.set_index('name'))
        self.images.reset_index(inplace=True)

        http.server.SimpleHTTPRequestHandler.__init__(self, *args)
    
    def do_GET(self):

        parsed_path = urlparse(self.path)
        query = parse_qs(parsed_path.query)

        if parsed_path.path == '/':
            print(f'path: {parsed_path.path} | query: {query}')
            if query == {}:
                return http.server.SimpleHTTPRequestHandler.do_GET(self)
            
            else:
                valid = True
                pallette = []
                index = 1
                while True:
                    c_str = 'color'+str(index)
                    p_str = 'percentage'+str(index)

                    # at least 1 parameter for index
                    if (c_str not in query) and (p_str not in query):
                        break

                    # Are both color and percentage present?
                    if c_str not in query:
                        valid = False
                        break
                    
                    if p_str not in query:
                        valid = False
                        break
                
                    percent = query[p_str][0]
                    color = query[c_str][0]
                    rgb = ImageColor.getcolor(color, 'RGB')

                    pallette.append([int(percent), int(rgb[0]), int(rgb[1]), int(rgb[2])])

                    index += 1
                
                # check if percents add up to >100
                total = 0
                for color in pallette:
                    total += int(color[0])

                # print(f'pallette: {pallette}')

                if total >= 100 or pallette == []:
                    valid = False

                if not valid:
                    self.send_response(400)
                    self.end_headers()
                    return

                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                results = find_best_n_by_pallette(pallette, self.images, 9)
                site = construct_result_page(results)
                # print(site)
                self.wfile.write(bytes(site, "utf-8"))

                    
        elif parsed_path.path.count('/') == 1:
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            image_name = parsed_path.path.split('/')[-1]
            print(f'image name: {image_name}')
            first = self.images.query(f'name == "{image_name}"').iloc[0]
            print(f"first = {first.loc['name']}")
            results = find_best_n(first.loc['name'], self.images, 9)
            site = construct_result_page(results)
            # print(site)
            self.wfile.write(bytes(site, "utf-8"))

        else: 
            return http.server.SimpleHTTPRequestHandler.do_GET(self)

        

def find_image(name) -> Path:
    wallpapers = Path('wallpapers')
    # print(wallpapers.absolute())
    # print(name)
    results =  wallpapers.glob(f"**/{name}")

    # for result in results:
    #     print(result)

    return next(results)



handler = CustomHttpRequestHandler
server=socketserver.TCPServer(("", PORT), handler)
print(f"Server started at port {PORT}. Press CTRL+C to close the server.")

try:
	server.serve_forever()
except KeyboardInterrupt:
	server.server_close()
	print("Server Closed")	

