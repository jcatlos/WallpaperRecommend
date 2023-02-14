from colorsys import rgb_to_hls
import pandas as pd
from skimage.color import rgb2lab, lab2rgb
from PIL import Image

HUE_WEIGHT = 10
LIGHTNESS_WEIGHT = 1
SATURATION_WEIGHT = 1


def color_distance(r1, g1, b1, r2, g2, b2) -> int:
    # print(f"first3 = {r1}, {g1}, {b1}")

    # h1, l1, s1 = rgb_to_hls(r1/255, g1/255, b1/255)
    # h2, l2, s2 = rgb_to_hls(r2/255, g2/255, b2/255)

    # return abs(h1-h2) * HUE_WEIGHT + abs(l1-l2) * LIGHTNESS_WEIGHT + abs(s1-s2) * 
    
    return 0.3 * (r1-r2)**2 + 0.59 * (g1-g2)**2 + 0.11 * (b1-b2)**2


def pallette_distance(pallette1: list, pallette2: list):
    """
    Pallette: [(percentage, red, green, blue), ...]
    """
    # print(f"pallette1 = {pallette1}")
    # print(f"pallette2 = {pallette2}")

    # pallette1 = pallette1.to_list()
    # pallette2 = pallette2.to_list()

    total_distance = 0

    processed_percents = 0

    pallette1.sort(key= lambda x: x[0], reverse=True)
    
    while len(pallette1) > 0 and len(pallette2) > 0:

        pallette2.sort(key= lambda x: color_distance(pallette1[0][1], pallette1[0][2], pallette1[0][3], x[1], x[2], x[3]))

        # print(f"pallette1 stats:\npercentage = {pallette1[0][0]}")
        # print(f"r = {pallette1[0][1]}")
        # print(f"g = {pallette1[0][2]}")
        # print(f"b = {pallette1[0][3]}")

        # print(f"pallette2 stats:\npercentage = {pallette2[0][0]}")
        # print(f"r = {pallette2[0][1]}")
        # print(f"g = {pallette2[0][2]}")
        # print(f"b = {pallette2[0][3]}")


        current_cut = min(pallette1[0][0], pallette2[0][0])

        total_distance += current_cut * color_distance(pallette1[0][1], pallette1[0][2], pallette1[0][3], pallette2[0][1], pallette2[0][2], pallette2[0][3])

        pallette1[0][0] -= current_cut
        pallette2[0][0] -= current_cut

        if pallette2[0][0] <= 0:
            del pallette2[0]

        if pallette1[0][0] <= 0:
            del pallette1[0]

    return total_distance


if __name__ == '__main__':

    from load_data import load_data
    from querying import compose_pallette

    image_df = load_data()

    nm1 = 'pexels-photo-4693135.jpeg'
    nm2 = 'pexels-photo-3609832.jpeg'

    image1 = image_df.query(f'name == "{nm1}"').iloc[0]
    image2 = image_df.query(f'name == "{nm2}"').iloc[0]

    pall1 = compose_pallette(image1)
    pall2 = compose_pallette(image2)

    pall_img1 = Image.open(f'palletes/{nm1}')
    pall_img2 = Image.open(f'palletes/{nm2}')
    pall_img1.show()
    pall_img2.show()

    print(pallette_distance(pall1, pall2))