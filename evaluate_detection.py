import cv2
import time
import pandas as pd
from facenet_pytorch import MTCNN
from src.visualization import show_images
from src.utils.detection import Detection
from src.utils.image_discovery import ImageDiscovery

def run_discovery(root_folder, destination_folder):
    """
    Run image discovery on root folder, then save
    the results in csv files and return their paths.
    """
    start = time.time()
    discoverer = ImageDiscovery(root_folder, destination_folder, items_in_file=5000)
    csv_files = discoverer.discover()
    end = time.time()
    print('It took {:.2f} seconds to find all images.'.format(end - start))
    return csv_files

def run_detection(csv_files, destination_folder):
    """
    Run image discovery on root folder, then save
    the results in csv files and return their paths.
    """
    start_detection = time.time()
    det = Detection(csv_files, destination_folder, 32, one_face=True, device='cuda:0', default_height=540)
    csv_files = det.detect_faces()
    end_detection = time.time()
    print('It took {:.2f} seconds to detect all faces.'.format(end_detection - start_detection))
    return csv_files

def show_samples(bbox_csvs, n=5):
    """
    Get some random samples from face bounding boxes and plot.
    """
    faces = []
    i = 1
    for bbox_csv in bbox_csvs:
        df = pd.read_csv(bbox_csv)
        samples = df.sample(n=n)
        for _, sample in samples.iterrows():
            img = cv2.imread(sample['image_path'])[:, :, ::-1]
            x_from = max(sample['x_from_per'] * img.shape[1] // 100, 0)
            x_to = min(sample['x_to_per'] * img.shape[1] // 100, img.shape[1])
            y_from = max(sample['y_from_per'] * img.shape[0] // 100, 0)
            y_to = min(sample['y_to_per'] * img.shape[0] // 100, img.shape[0])
            face = img[y_from:y_to, x_from:x_to, :]
            face = cv2.resize(face, (112, 112))
            faces.append(face)
            print(i, sample['image_path'])
            i += 1
    show_images(faces)

def detect_one():
    path = '.\data\lfw\Tommy_Franks\Tommy_Franks_0004.jpg'
    img = cv2.imread(path)[:, :, ::-1]
    img = cv2.resize(img, (648, 540))
    mtcnn = MTCNN(select_largest=False)
    out = mtcnn.detect(img)
    print(out)
    
# paths_files = run_discovery('.\\data\\lfw', '.\\results\\temp_paths')

# paths_files = ['.\\results\\lfw_paths\\paths_1_5000_.csv',
#                '.\\results\\lfw_paths\\paths_2_5000_.csv',
#                '.\\results\\lfw_paths\\paths_3_3233_.csv']
# bbox_csvs = run_detection(paths_files, '.\\results\\lfw_bboxes')

# bbox_csvs = ['.\\results\\lfw_bboxes_540x648_1face\\bounding_boxes_1_5000_.csv',
#              '.\\results\\lfw_bboxes_540x648_1face\\bounding_boxes_2_5000_.csv',
#              '.\\results\\lfw_bboxes_540x648_1face\\bounding_boxes_3_3233_.csv']
# show_samples(bbox_csvs, n=10)

detect_one()