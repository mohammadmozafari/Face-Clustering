import time

from PIL.Image import Image
from utils.detection import Detection
from utils.image_discovery import ImageDiscovery

def evaluate_detection():

    start = time.time()
    discoverer = ImageDiscovery('.\\data\\temp', '.\\results\\temp_res2')
    discoverer.discover()
    end = time.time()
    print('It took {:.2f} seconds to find all images.'.format(end - start))

    # det = Detection('results/lfw_bounding_boxes.csv')
    # faces = det.detect_faces(paths)
    # print(len(faces))
