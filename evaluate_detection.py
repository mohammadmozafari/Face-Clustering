import cv2
import time
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from src.utils.detection import Detection

# start = time.time()
# discoverer = ImageDiscovery('.\\data\\lfw', '.\\results\\lfw_paths', items_in_file=5000)
# csv_files = discoverer.discover()
# end = time.time()
# print('It took {:.2f} seconds to find all images.'.format(end - start))

# csv_files = ['.\\results\\lfw_paths\\paths_1_5000_.csv',
#              '.\\results\\lfw_paths\\paths_2_5000_.csv',
#              '.\\results\\lfw_paths\\paths_3_3233_.csv']

# start_detection = time.time()
# det = Detection(csv_files, '.\\results\\lfw_bboxes', 32, one_face=True, device='cuda:0')
# faces = det.detect_faces()
# end_detection = time.time()
# print('It took {:.2f} seconds to detect all faces.'.format(end_detection - start_detection))

bbox_csvs = ['.\\results\\lfw_bboxes\\bounding_boxes_1_5000_.csv',
             '.\\results\\lfw_bboxes\\bounding_boxes_2_5000_.csv',
             '.\\results\\lfw_bboxes\\bounding_boxes_3_3233_.csv']

faces = []
for bbox_csv in bbox_csvs:
    df = pd.read_csv(bbox_csv)
    samples = df.sample(n=5)
    for _, sample in samples.iterrows():
        img = cv2.imread(sample['image_path'])[:, :, ::-1]
        x_from = max(sample['x_from_per'] * img.shape[1] // 100, 0)
        x_to = min(sample['x_to_per'] * img.shape[1] // 100, img.shape[1])
        y_from = max(sample['y_from_per'] * img.shape[0] // 100, 0)
        y_to = min(sample['y_to_per'] * img.shape[0] // 100, img.shape[0])
        face = img[y_from:y_to, x_from:x_to, :]
        try:
            face = cv2.resize(face, (112, 112))
        except:
            print(sample['x_from_per'],
                  sample['x_to_per'], sample['y_from_per'], sample['y_to_per'])
            print(x_from, x_to, y_from, y_to)
            print(face.shape)
        faces.append(face)

sqroot = math.sqrt(len(faces))
cols = math.ceil(sqroot)
rows = math.floor(sqroot)
while cols * rows < len(faces):
    rows += 1

rows = cols if (cols * cols > len(faces)) else (cols + 1)
big_image = np.ones((rows * 112, cols * 112, 3)) * 255

i, j = 0, 0
for face in faces:
    big_image[i*112:(i+1)*112, j*112:(j+1)*112, :] = face
    if i == cols - 1:
        i = 0
        j += 1
    else:
        i += 1
plt.imshow(big_image.astype('int'))
plt.axis('off')
plt.show()
