import os
import cv2
import mtcnn
import matplotlib.pyplot as plt
import matplotlib.image as matimg
from facenet_pytorch import MTCNN

def get_images_paths(folder_address, extensions=['.jpg', '.png']):
    paths = []
    for root, _, files in os.walk(folder_address):
        for f in files:
            for extension in extensions:
                if f.endswith(extension):
                    paths.append(os.path.join(root, f))
                    break
    return paths

def find_bounding_boxes(batches, thresh=0.95):
    # detector = mtcnn.MTCNN()
    detector = MTCNN()

    detected_faces = []
    for paths, size in batches:
        imgs = []
        for path in paths:
            img = cv2.imread(path)[:, :, ::-1]
            img = cv2.resize(img, size)
            imgs.append(img)

        bboxes_imgs, probs = detector.detect(imgs)
        for idx, (bbox_img, prob) in enumerate(zip(bboxes_imgs, probs)):
            for i in range(len(bbox_img)):
                if prob[i] > 0.95:
                    detected_faces.append((paths[idx], bbox_img[i][0], bbox_img[i][1], bbox_img[i][2], bbox_img[i][3]))
            
    print(detected_faces)

fi = get_images_paths('./data')
fi = [([fi[i], fi[i+1]], (1920, 1080)) for i in range(len(fi) - 1)]
find_bounding_boxes(fi)
