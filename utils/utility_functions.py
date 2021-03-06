import os

def get_images_paths(folder_address, extensions=['.jpg', '.png']):
    """
    Walks through a given directory, finds all images
    in any folder and subfolder and returns the list of
    paths of images.
    """
    paths = []
    for root, _, files in os.walk(folder_address):
        for f in files:
            for extension in extensions:
                if f.endswith(extension):
                    paths.append(os.path.join(root, f))
                    break
    return paths
