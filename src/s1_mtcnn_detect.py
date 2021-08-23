import cv2
import time
import argparse
import pandas as pd
from facenet_pytorch import MTCNN
from detection import MTCNNDetection
from visualization import show_images

def main(images, save_folder, h, w):
    start_detection = time.time()
    det = MTCNNDetection([images], save_folder, 32, (h, w), one_face=True, device='cuda:0', same=True, mode='center')
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
    
    parser = argparse.ArgumentParser(description='Face detection')
    parser.add_argument('--images', help='CSV file containing image paths')
    parser.add_argument('--save_folder', help='Folder to save detected faces')
    parser.add_argument('--height', help='Resize height of images', type=int)
    parser.add_argument('--width', help='Resize width of images', type=int)
    args = parser.parse_args()
    main(args.images, args.save_folder, args.height, args.width)

    # paths_files = run_discovery('.\\data\\lfw', '.\\results\\lfw-paths')
    # bbox_csvs = run_detection(paths_files, '.\\results\\lfw-bboxes')
    # show_samples(['results\\lfw-bboxes\\bounding_boxes_1_13233_.csv'], n=25)

    # detect_one()
