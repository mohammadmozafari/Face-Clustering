import time

from PIL.Image import Image
from ..utils.detection import Detection
from ..utils.image_discovery import ImageDiscovery

def evaluate_detection():

    start = time.time()
    discoverer = ImageDiscovery('.\\data\\temp', '.\\results\\temp_res6', items_in_file=5)
    csv_files = discoverer.discover()
    end = time.time()
    print('It took {:.2f} seconds to find all images.'.format(end - start))

    det = Detection(csv_files, '.\\results\\bounding_boxes_2', 16)
    faces = det.detect_faces()
