import time
from utils.detection import Detection
from utils.utility_functions import get_images_paths

def evaluate_detection():

    start = time.time()
    paths = get_images_paths('./data/lfw')
    end = time.time()
    print(len(paths))
    print('It took {:.2f} seconds to find all images.'.format(end - start))

    det = Detection('results/lfw_bounding_boxes.csv')
    faces = det.detect_faces(paths)
    print(len(faces))
