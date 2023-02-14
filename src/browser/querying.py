import pandas as pd
from color_similarity import pallette_distance
import numpy as np

def compose_pallette(row: pd.Series):
    pallette =  [
        [row['percentage_1'],
        row['centroid_1_channel1'],
        row['centroid_1_channel2'],
        row['centroid_1_channel3']],
        [row['percentage_2'],
        row['centroid_2_channel1'],
        row['centroid_2_channel2'],
        row['centroid_2_channel3']],
        [row['percentage_3'],
        row['centroid_3_channel1'],
        row['centroid_3_channel2'],
        row['centroid_3_channel3']],
        [row['percentage_4'],
        row['centroid_4_channel1'],
        row['centroid_4_channel2'],
        row['centroid_4_channel3']],
        [row['percentage_5'],
        row['centroid_5_channel1'],
        row['centroid_5_channel2'],
        row['centroid_5_channel3']],
        [row['percentage_6'],
        row['centroid_6_channel1'],
        row['centroid_6_channel2'],
        row['centroid_6_channel3']],
        [row['percentage_7'],
        row['centroid_7_channel1'],
        row['centroid_7_channel2'],
        row['centroid_7_channel3']],
        [row['percentage_8'],
        row['centroid_8_channel1'],
        row['centroid_8_channel2'],
        row['centroid_8_channel3']],
    ]

    new_pallette = []

    for color in pallette:
        is_nan = False
        for value in color:
            if np.isnan(value): 
                is_nan = True
            else: 
                value = float(value)
        if not is_nan:
            new_pallette.append(color)

    return new_pallette

def get_dist(pallette1: list, image2:pd.Series):
    # print(image2)
    # print(pallette1)
    # print(compose_pallette(image2))
    copy = []
    for color in pallette1:
        copy.append(color.copy())
    # print(f'copy: {copy}')
    return pallette_distance(copy, compose_pallette(image2))

def find_best_n(name: str, images: pd.DataFrame, n:int):
    image = images.query(f'name == "{name}"')
    pallete: list = image.apply(compose_pallette, axis=1).to_list()[0]

    images['dist'] = images.apply(lambda row: get_dist(pallete, row), axis=1)
    sorted_images = images.sort_values(['dist'], ascending=True).drop_duplicates(subset=['name'])

    return sorted_images.head(n)

def find_best_n_by_pallette(pallete:list, images: pd.DataFrame, n:int):
    images['dist'] = images.apply(lambda row: get_dist(pallete, row), axis=1)
    sorted_images = images.sort_values(['dist'], ascending=True).drop_duplicates(subset=['name'])

    return sorted_images.head(n)
