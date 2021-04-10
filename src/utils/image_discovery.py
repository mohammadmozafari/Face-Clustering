import os
import pandas as pd
from PIL import Image, ExifTags

class ImageDiscovery:
    """
    This class is responsible for walking through
    a given directory and finding all images
    and saving paths in some csv files.
    """

    def __init__(self, folder_address, save_folder, items_in_file=100_000, extensions=['.jpg', '.png']):
        self.folder_address = folder_address
        self.save_folder = save_folder
        self.items_in_file = items_in_file
        self.extensions = extensions
        self.current_split = 1
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        print('-----------------------')
        print('Image discovery phase has begun...\n')

    def discover(self):
        """
        Walks through a given directory, finds all images
        in any folder and subfolder and returns the list of
        paths of images.
        """
        paths = []
        result = []
        for root, _, files in os.walk(self.folder_address):
            for f in files:
                for extension in self.extensions:
                    if f.endswith(extension):
                        image_path = os.path.join(root, f)
                        paths.append((image_path))
                        break
                if len(paths) == self.items_in_file:
                    result.append(self.save_in_csv(paths))
                    paths = []
        if len(paths) != 0:
            result.append(self.save_in_csv(paths))
            paths = []

        print('Image discovery phase has finished')
        print('-----------------------')
        return result

    def save_in_csv(self, paths):
        """
        Saves a batch of paths in one csv file.
        """
        df = pd.DataFrame(paths, columns=['path'])
        print('Split {} completed.'.format(self.current_split))
        save_path = os.path.join(self.save_folder, 'paths_{}_{}_.csv'.format(self.current_split, len(df)))
        df.to_csv(save_path, index=False)
        print('Saving in file is done.')
        print()
        self.current_split += 1
        return save_path
        