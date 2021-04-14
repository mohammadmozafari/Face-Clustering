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
    discoverer = ImageDiscovery(root_folder, destination_folder)
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
    det = Detection(csv_files, destination_folder, 32, (250, 250), one_face=True, device='cuda:0', same=True, mode='center')
    csv_files = det.detect_faces(num_workers=2)
    end_detection = time.time()
    print('It took {:.2f} seconds to detect all faces.'.format(end_detection - start_detection))
    return csv_files

def show_samples(bbox_csvs, n=5):
    """
    Get some random samples from face bounding boxes and plot.
    """
    faces = []
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
    show_images(faces)

def detect_one():
    path = '.\data\lfw-subset\Ed_Rendell\Ed_Rendell_0001.jpg'
    img = cv2.imread(path)[:, :, ::-1]
    img = cv2.resize(img, (648, 540))
    mtcnn = MTCNN(select_largest=False)
    out = mtcnn.detect(img)
    print(out)
    
if __name__ == "__main__":
    paths_files = run_discovery('.\\data\\lfw', '.\\results\\lfw-paths')
    bbox_csvs = run_detection(paths_files, '.\\results\\lfw-bboxes')
    # show_samples(['results\\lfw-subset-bboxes\\bounding_boxes_1_1525_.csv'], n=40)
    # detect_one()
