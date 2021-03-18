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
                        width, height = self.get_image_size(image_path)
                        ratio_gp = self.get_ratio_group(width, height)
                        paths.append((image_path, ratio_gp))
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
        df = pd.DataFrame(paths, columns=['path', 'ratio_group'])
        print('Split {} completed. Sorting started...'.format(self.current_split))
        df = df.sort_values(by=['ratio_group'])
        print('Sorting done. Saving in file...')
        save_path = os.path.join(self.save_folder, 'paths_{}_{}_.csv'.format(self.current_split, len(df)))
        df.to_csv(save_path, index=False)
        print('Saving in file is done.')
        print()
        self.current_split += 1
        return save_path

    def get_image_size(self, image_path):
        """
        Finds out the width and height of images.
        Some images are rotated by a tag that should be considered.  
        """
        size = (None, None)
        with Image.open(image_path) as i:
            size = i.size
            try:
                exif = {
                    ExifTags.TAGS[k]: v
                    for k, v in i._getexif().items()
                    if k in ExifTags.TAGS
                }
                if exif.get("Orientation", 0) > 4:
                    size = size[1], size[0]
            except:
                pass
        return size

    def get_ratio_group(self, width, height):
        """
        According to image ratio assign a
        group number for resizing images.
        """
        ratio = width / height
        gp = 1
        if ratio < 0.52:
            gp = -3
        elif ratio >= 0.52 and ratio < 0.71:
            gp = -2
        elif ratio >= 0.71 and ratio < 1:
            gp = -1
        elif ratio >= 1 and ratio < 1.4:
            gp = 1
        elif ratio >= 1.4 and ratio < 1.9:
            gp = 2
        elif ratio >= 1.9:
            gp = 3
        return gp
