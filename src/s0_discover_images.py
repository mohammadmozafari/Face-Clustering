import os
import argparse
import pandas as pd
from retina_detect import main
from utils.image_discovery import ImageDiscovery

def iter_images(path, extensions=['.jpg', '.png']):
    index = 0
    for root, _, files in os.walk(path):
        for f in files:
            for extension in extensions:
                if f.endswith(extension):
                    image_path = os.path.join(root, f)
                    yield index, image_path
                    index += 1

def save_in_csv(paths, save_folder, split):
    df = pd.DataFrame(paths, columns=['index', 'path'])
    print('Split {} completed.'.format(split))
    save_path = os.path.join(save_folder, 'paths_{}_{}_.csv'.format(split, len(df)))
    df.to_csv(save_path, index=False)
    print('Saving in file is done.')
    print()
    return save_path

def main(folder_address, save_folder, items_in_file=100_000):
    image_paths = []
    file_num = 1
    for i, image_path in iter_images(folder_address):
        image_paths.append((i, image_path))
        if len(image_paths) == items_in_file:
            save_in_csv(image_paths, save_folder, file_num)
            image_paths = []
            file_num += 1
    if len(image_paths) > 0:
        save_in_csv(image_paths, save_folder, file_num)
        image_paths = []
        file_num += 1

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Discover all images in a folder')
    parser.add_argument('--folder', help='Where to look for images')
    parser.add_argument('--save_folder', help='Folder to save discovered images paths')
    parser.add_argument('--items_in_file', help='How many paths in each file?', type=int)
    args = parser.parse_args()

    main(args.folder, args.save_folder, args.items_in_file)
