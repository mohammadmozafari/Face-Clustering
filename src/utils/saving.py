import os
import cv2
import time
import shutil
import pandas as pd
from PIL import Image
import matplotlib.pyplot as plt

def add_bbox(img, x1, x2, y1, y2, thickness=10):
    temp = img[y1+thickness:y2-thickness, x1+thickness:x2-thickness, :].copy()
    img[y1:y2, x1:x2, 0] = 255
    img[y1:y2, x1:x2, 1] = 0
    img[y1:y2, x1:x2, 2] = 0
    img[y1+thickness:y2-thickness, x1+thickness:x2-thickness, :] = temp
    return img

def setup_empty_folder(path='./output'):
    if not os.path.exists(path):
        os.mkdir(path)
        return
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

def save_images_with_bboxes(clusters, csv_file, dest_folder, pbar_emit_signal):
    setup_empty_folder(dest_folder)
    df = pd.read_csv(csv_file)
    for i, row in df.iterrows():
        print(row['image_path'])
        img = cv2.imread(row.image_path)[:, :, ::-1]
        h, w, _ = img.shape
        x1 = max(int(row['x_from_per'] * w / 100), 0)
        x2 = min(int(row['x_to_per'] * w / 100), w)
        y1 = max(int(row['y_from_per'] * h / 100), 0)
        y2 = min(int(row['y_to_per'] * h / 100), h)
        img = add_bbox(img, x1, x2, y1, y2, thickness=30)
        folder = os.path.join(dest_folder, str(clusters[i]))
        if not os.path.exists(folder):
            os.mkdir(folder)
        img = Image.fromarray(img)
        dest = os.path.join(folder, '{}.jpeg'.format(i))
        img.save(dest)
        if pbar_emit_signal:
            pbar_emit_signal(max(13, (i+1)*1000/len(df)))

def main():
    save_images_with_bboxes([0, 1, 0, 0, 0, 1, 3, 2, 2], './data/program_data/bounding_boxes_.csv', './output')

if __name__ == "__main__":
    main()
