from pathlib import Path
import os

root = Path(os.getcwd())
print(f'root = {root}')

used_names = set()

with open('images.txt', 'w') as out_file:
    for image in root.glob('wallpapers/*/*'):

        path = image.resolve().name
        if path not in used_names:
            out_file.write(str(image.resolve().as_posix()))
            out_file.write('\n')
            used_names.add(path)