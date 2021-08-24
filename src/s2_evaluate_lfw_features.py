import os
import sys
import cv2
import torch
import argparse
import numpy as np
import pandas as pd
from sklearn import metrics
import matplotlib.pyplot as plt
from visualization import show_images
from utils.datasets import FaceDataset
from utils.feature_extraction import FeatureExtractor

def lfw_prepare_pairs(pairs_files, paths):
    """
    LFW dataset has a pair dataset for testing.
    This function converts that pair dataset
    to a more suitable form for our program
    """
    pairs_csv_file = './data/lfw-results/pairs.csv'
    df = pd.read_csv(paths)
    pairs = []
    print('Building tuples for evaluation ...')
    with open(pairs_files) as f:
        lines = f.readlines()
        for i, line in enumerate(lines):
            if i == 0:
                continue
            parts = line.split()
            target, name1, name2 = None, None, None
            if len(parts) == 3:
                target = 1
                name1 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[1]))
                name2 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[2]))
            elif len(parts) == 4:
                target = 0
                name1 = '{}_{:0>4d}.jpg'.format(parts[0], int(parts[1]))
                name2 = '{}_{:0>4d}.jpg'.format(parts[2], int(parts[3]))

            idx1 = df[df['path'].str.contains(
                '\{}'.format(name1), regex=False)].index.values[0]
            idx2 = df[df['path'].str.contains(
                '\{}'.format(name2), regex=False)].index.values[0]
            pairs.append((idx1, idx2, target))
            print('Pair {}/{} done.'.format(i, len(lines)-1))
        df = pd.DataFrame(pairs, columns=['first', 'second', 'target'])
        df.to_csv(pairs_csv_file, index=False)
    print('-----------------------')
    return pairs_csv_file


def check_mistakes(threshold=1.1):
    """
    It's important to know why mistakes have happened.
    This function shows pairs of images that are falsely classified.
    """
    pairs_csv_file = './results/pairs.csv'
    bboxes = './results/lfw-bboxes/bounding_boxes_1_13233_.csv'
    features = './results/lfw-features/features_1_13233_.csv'
    features = pd.read_csv(features).values
    data = pd.read_csv(pairs_csv_file).values

    first = features[data[:, 0]]
    second = features[data[:, 1]]
    labels = data[:, 2]
    diff = np.linalg.norm(first - second, axis=1)
    preds = (diff < threshold) * 1
    mistakes = np.where(preds != labels)[0]

    print('Accuracy =', np.mean(preds == labels))
    print('Number of mistakes =', mistakes.shape[0])
    fds = FaceDataset(bboxes, talk=True)
    for i, mistake in enumerate(mistakes):
        face1, path1 = fds.__getitem__(data[mistake, 0])
        face2, path2 = fds.__getitem__(data[mistake, 1])
        print()
        print('Pair', i+1)
        print(path1)
        print(path2)
        print('Target =', labels[mistake])
        print('Predicted =', preds[mistake])
        face1 = (face1.transpose((1, 2, 0)) * 255).astype('int')
        face2 = (face2.transpose((1, 2, 0)) * 255).astype('int')
        img1 = cv2.imread(path1)[:, :, ::-1]
        img1 = cv2.resize(img1, (112, 112))
        img2 = cv2.imread(path2)[:, :, ::-1]
        img2 = cv2.resize(img2, (112, 112))
        show_images([face1, face2, img1, img2])


def evaluate_on_lfw(pairs_csv_file, features):
    """
    We evaluate features extracted from lfw images
    and report best threshold, highest accuracy and area under ROC curve.
    """
    features = np.load(features)
    data = pd.read_csv(pairs_csv_file).values

    first = features[data[:, 0]]
    second = features[data[:, 1]]
    labels = data[:, 2]
    diff = np.linalg.norm(first - second, axis=1)
    sorted_diff = np.sort(diff)

    TPRs, FPRs = [], []
    best_accuracy = -1
    best_threshold = None
    for threshold in sorted_diff:
        preds = (diff < threshold) * 1
        tp = preds @ labels
        tn = (1 - preds) @ (1 - labels)
        fp = preds @ (1 - labels)
        fn = (1 - preds) @ labels
        tpr = tp / (tp + fn)
        fpr = fp / (tn + fp)
        acc = (tp + tn) / (tp + fp + tn + fn)
        if acc > best_accuracy:
            best_accuracy = acc
            best_threshold = threshold
        TPRs.append(tpr)
        FPRs.append(fpr)

    roc_auc = metrics.auc(FPRs, TPRs)
    print('Best threshold = {}'.format(best_threshold))
    print('Highest accuracy = {}'.format(best_accuracy))
    print('Area under ROC curve = {}'.format(roc_auc))
    plt.scatter(FPRs, TPRs, s=0.1)
    plt.show()

def main(images, pairs_path, features):
    csv_file = lfw_prepare_pairs(pairs_path, images)
    evaluate_on_lfw(csv_file, features)
    pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Feature Evaluation')
    parser.add_argument('--images', help='CSV file containing all image paths')
    parser.add_argument('--pairs_path', help='LFW pair csv dataset path')
    parser.add_argument('--features', help='Extracted features path')
    args = parser.parse_args()
    main(args.images, args.pairs_path, args.features)
    # lfw_prepare_pairs()
    # check_mistakes()
    # evaluate_on_lfw()
