import time
from src.utils.detection import Detection

# start = time.time()
# discoverer = ImageDiscovery('.\\data\\lfw', '.\\results\\lfw_paths', items_in_file=5000)
# csv_files = discoverer.discover()
# end = time.time()
# print('It took {:.2f} seconds to find all images.'.format(end - start))

csv_files = ['.\\results\\lfw_paths\\paths_1_5000_.csv',
             '.\\results\\lfw_paths\\paths_2_5000_.csv',
             '.\\results\\lfw_paths\\paths_3_3233_.csv']

start_detection = time.time()
det = Detection(csv_files, '.\\results\\lfw_bboxes', 1, device='cuda:0')
faces = det.detect_faces()
end_detection = time.time()
print('It took {:.2f} seconds to detect all faces.'.format(end_detection - start_detection))

