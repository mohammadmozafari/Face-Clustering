from utils.detection import Detection
from utils.face_dataset import FaceDataset
from utils.utility_functions import get_images_paths

paths = get_images_paths('.\\data')
d = Detection('./results/bounding_boxes.csv')
faces = d.detect_faces(paths)
print('Faces are detected')

face_ds = FaceDataset('bounding_boxes.csv')
for face in face_ds:
    pass
