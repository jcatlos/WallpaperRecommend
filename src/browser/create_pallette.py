import math
import pandas as pd
from PIL import Image

from load_data import load_data


def create_pallette(img_data: pd.Series):
    pallete = Image.new('RGB', (400, 10))
    total_offset = 0

    for i in range(1, 9):
        percentage = img_data[f'percentage_{i}']

        if math.isnan(percentage):
            break
        else:
            offset = int(percentage * 4)
            red    = int(img_data[f'centroid_{i}_channel1'])
            green  = int(img_data[f'centroid_{i}_channel2'])
            blue   = int(img_data[f'centroid_{i}_channel3'])

            color = Image.new('RGB', (offset,10), (red, green, blue))

            pallete.paste(color, (total_offset, 0))
            total_offset += offset

    pallete.resize(size=(total_offset, 10))
    return pallete

if __name__ == '__main__':

    image_df = load_data()

    for index, data in image_df.iterrows():
        pallete = create_pallette(data)
        pallete.save(f"palletes/{data['name']}")